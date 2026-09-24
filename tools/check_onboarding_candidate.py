"""Exercise installed product wheels with an unpublished F Prime release HTTP replay.

Only Catalog/GitHub HTTP responses are substituted. Integrity, pip-managed adapter
installation, inventory, verification and lock handling run unchanged. Run outside
source checkouts with PATH containing only the clean product environment's bin.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

from orbitfabric_github_release_source import GitHubApiClient
from typer.testing import CliRunner

from orbitfabric.adapter_manager import AdapterManager, ProjectLockInstallService
from orbitfabric.entrypoint import app


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wheel", type=Path, required=True)
    parser.add_argument("--descriptor", type=Path, required=True)
    parser.add_argument("--lock", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    assert shutil.which("git") is None, "Acceptance must run without Git on PATH"
    descriptor_bytes = args.descriptor.read_bytes()
    wheel_bytes = args.wheel.read_bytes()
    descriptor = json.loads(descriptor_bytes)
    assert descriptor["source_coordinate"] == {
        "authority": "github.com/OrbitFabric",
        "publisher": "orbitfabric",
        "name": "fprime",
    }
    assert descriptor["release_version"] == "0.1.3"
    wheel_url = (
        "https://github.com/OrbitFabric/orbitfabric-fprime-adapter/releases/download/v0.1.3/"
        + args.wheel.name
    )
    descriptor_url = wheel_url.rsplit("/", 1)[0] + "/adapter-release.json"
    downloads = {descriptor_url: descriptor_bytes, wheel_url: wheel_bytes}
    release = {
        "id": 1,
        "tag_name": "v0.1.3",
        "draft": False,
        "prerelease": False,
        "immutable": True,
        "assets": [
            {"name": name, "browser_download_url": url}
            for name, url in [
                ("adapter-release.json", descriptor_url),
                (args.wheel.name, wheel_url),
            ]
        ],
    }
    current = {
        "source_coordinate": descriptor["source_coordinate"],
        "releases": [
            {
                "version": "0.1.3",
                "release_descriptor_digest": {
                    "algorithm": "sha256",
                    "value": digest(descriptor_bytes),
                },
                "sources": [{"binding": "github-orbitfabric-fprime", "release_ref": "v0.1.3"}],
            }
        ],
    }
    historical = json.loads(json.dumps(current))
    historical["source_coordinate"]["authority"] = "github.com/FAROTECH"
    historical["releases"][0]["version"] = "0.1.2"
    historical["releases"][0]["sources"][0]["release_ref"] = "v0.1.2"
    catalog = {
        "kind": "orbitfabric.adapter_catalog",
        "catalog_version": "0.1-candidate",
        "adapters": [historical, current],
        "source_bindings": [
            {
                "id": "github-orbitfabric-fprime",
                "provider": "github-release",
                "config": {"repository": "OrbitFabric/orbitfabric-fprime-adapter"},
            }
        ],
    }
    catalog_bytes = json.dumps(catalog).encode()
    revision = "a" * 40  # Explicit synthetic HTTP replay; not a claimed public commit.
    requests = []

    def catalog_http(url):
        requests.append(url)
        if (
            url
            == "https://api.github.com/repos/OrbitFabric/orbitfabric-adapter-catalog/commits/main"
        ):
            return json.dumps({"sha": revision}).encode()
        assert (
            url
            == f"https://raw.githubusercontent.com/OrbitFabric/orbitfabric-adapter-catalog/{revision}/catalog.json"
        )
        return catalog_bytes

    def release_http(_self, repository, ref):
        assert repository == "OrbitFabric/orbitfabric-fprime-adapter" and ref == "v0.1.3"
        return release

    runner = CliRunner()
    checks = []

    def cli(arguments, success=True):
        result = runner.invoke(app, ["adapter", *arguments])
        assert (result.exit_code == 0) == success, (arguments, result.output, result.exception)
        return result.output

    with tempfile.TemporaryDirectory(prefix="onboarding-acceptance-") as temporary:
        os.environ["ORBITFABRIC_STATE_DIR"] = str(Path(temporary) / "state")
        local_catalog = Path(temporary) / "catalog.json"
        local_catalog.write_bytes(catalog_bytes)
        with (
            patch("orbitfabric.adapter_onboarding._read_https", catalog_http),
            patch.object(GitHubApiClient, "release_by_ref", release_http),
            patch.object(GitHubApiClient, "download", lambda _self, url: downloads[url]),
        ):
            # Both integrity failures must leave inventory empty.
            for url in (descriptor_url, wheel_url):
                original = downloads[url]
                downloads[url] += b"tampered"
                cli(
                    ["install", "fprime", "--version", "0.1.3", "--catalog", str(local_catalog)],
                    False,
                )
                assert AdapterManager().list() == []
                downloads[url] = original
            checks += ["descriptor integrity failure", "artifact integrity failure"]
            result = json.loads(cli(["install", "fprime", "--version", "0.1.3", "--json"]))
            assert len(requests) == 2 and result["catalog_snapshot"]["revision"] == revision
            assert result["catalog_snapshot"]["sha256"] == digest(catalog_bytes)
            record = result["installed"]
            assert record["source_coordinate"] == descriptor["source_coordinate"]
            checks += [
                "logical exact install with historical coexistence",
                "main resolved before pinned retrieval",
            ]
            requests.clear()
            full = json.loads(
                cli(
                    [
                        "install",
                        "github.com/OrbitFabric:orbitfabric/fprime",
                        "--version",
                        "0.1.3",
                        "--catalog-revision",
                        revision,
                        "--json",
                    ]
                )
            )
            assert len(requests) == 1 and full["installed"]["release_version"] == "0.1.3"
            checks += ["full coordinate install", "explicit pinned snapshot"]
            cli(["install", "fprime", "--version", "9.0.0", "--catalog", str(local_catalog)], False)
            historical["releases"][0]["version"] = "0.1.3"
            local_catalog.write_text(json.dumps(catalog))
            cli(["install", "fprime", "--version", "0.1.3", "--catalog", str(local_catalog)], False)
            checks += ["zero match failure", "multiple exact matches failure"]
        # HTTP replay is gone; retained descriptor and managed material must still verify.
        for installed in AdapterManager().list():
            verified = json.loads(cli(["verify", installed.instance_id, "--json"]))
            assert all(
                verified[k]["status"] == "PASS"
                for k in (
                    "release_descriptor_integrity",
                    "manifest_integrity",
                    "manifest_conformance",
                    "execution_binding",
                    "backend_materialization",
                )
            )
        cli(["list"])
        # Also invoke the installed executable as a subprocess, outside source trees.
        subprocess.run(
            [
                str(Path(sys.executable).parent / "orbitfabric"),
                "adapter",
                "verify",
                record["instance_id"],
            ],
            check=True,
        )
        checks += ["inventory", "adapter verify PASS after temporary acquisition cleanup"]
        before = len(AdapterManager().list())
        coordinate = AdapterManager().list()[0].source_coordinate
        with patch.object(
            AdapterManager, "install_resolved", side_effect=AssertionError("NOOP installed")
        ):
            report = ProjectLockInstallService().install_entry(
                args.lock, coordinate, "/missing-descriptor", "/missing-wheel"
            )
        assert report.action == "NOOP" and report.before_status == "MATCH"
        assert len(AdapterManager().list()) == before
        checks += ["Project Lock MATCH -> NOOP without source files"]
        cli(["install", str(args.descriptor), "--artifact", str(args.wheel)])
        assert len(AdapterManager().list()) == before + 1
        checks += ["old explicit local install", "no Git executable"]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(
            {
                "scope": "unpublished release HTTP replay; real installed wheels",
                "descriptor_sha256": digest(descriptor_bytes),
                "wheel_sha256": digest(wheel_bytes),
                "passed": checks,
            },
            indent=2,
        )
        + "\n"
    )
    print(json.dumps(checks, indent=2))


if __name__ == "__main__":
    main()
