from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest
from typer.testing import CliRunner

from orbitfabric import adapter_onboarding as onboarding
from orbitfabric.adapter_manager import AdapterCatalog, select_exact_release_by_logical_key
from orbitfabric.adapter_manager.errors import ReleaseResolutionError
from orbitfabric.entrypoint import app


def payload():
    # Historical immutable identity deliberately coexists with current authority.
    return {
        "kind": "orbitfabric.adapter_catalog",
        "catalog_version": "0.1-candidate",
        "adapters": [
            {
                "source_coordinate": {
                    "authority": authority,
                    "publisher": "orbitfabric",
                    "name": "openc3-cosmos",
                },
                "releases": [
                    {
                        "version": version,
                        "release_descriptor_digest": {"algorithm": "sha256", "value": "a" * 64},
                        "sources": [{"binding": "github-cosmos", "release_ref": "v" + version}],
                    }
                ],
            }
            for authority, version in [
                ("github.com/FAROTECH", "0.1.0"),
                ("github.com/OrbitFabric", "0.2.0"),
            ]
        ],
        "source_bindings": [
            {
                "id": "github-cosmos",
                "provider": "github-release",
                "config": {"repository": "OrbitFabric/orbitfabric-openc3-cosmos-adapter"},
            }
        ],
    }


@pytest.mark.parametrize(
    "identity",
    [
        "openc3-cosmos",
        "orbitfabric/openc3-cosmos",
        "github.com/OrbitFabric:orbitfabric/openc3-cosmos",
    ],
)
def test_exact_version_disambiguates_historical_authority(identity):
    result = onboarding.select_install_release(
        AdapterCatalog.model_validate(payload()), identity, "0.2.0"
    )
    assert result.source_coordinate.authority == "github.com/OrbitFabric"
    assert result.release_version == "0.2.0"


def test_historical_identity_is_preserved():
    result = select_exact_release_by_logical_key(
        AdapterCatalog.model_validate(payload()),
        publisher="orbitfabric",
        name="openc3-cosmos",
        release_version="0.1.0",
    )
    assert result.source_coordinate.authority == "github.com/FAROTECH"


@pytest.mark.parametrize("identity", ["openc3-cosmos", "orbitfabric/openc3-cosmos"])
def test_same_exact_version_across_authorities_fails(identity):
    data = payload()
    data["adapters"][0]["releases"][0]["version"] = "0.2.0"
    with pytest.raises(ReleaseResolutionError, match="found 2"):
        onboarding.select_install_release(AdapterCatalog.model_validate(data), identity, "0.2.0")


def test_bare_name_does_not_prefer_publisher():
    data = payload()
    other = deepcopy(data["adapters"][1])
    other["source_coordinate"]["publisher"] = "independent"
    data["adapters"].append(other)
    with pytest.raises(ReleaseResolutionError, match="found 2"):
        onboarding.select_install_release(
            AdapterCatalog.model_validate(data), "openc3-cosmos", "0.2.0"
        )


@pytest.mark.parametrize("version", ["9.0.0", "v0.2.0", "latest", "stable", ">=0.2", ""])
def test_no_version_normalization_or_fallback(version):
    with pytest.raises(ReleaseResolutionError):
        onboarding.select_install_release(
            AdapterCatalog.model_validate(payload()), "openc3-cosmos", version
        )


def test_default_acquisition_resolves_once_then_reads_immutable_snapshot(monkeypatch):
    calls = []
    revision = "b" * 40
    data = json.dumps(payload()).encode()

    def read(url):
        calls.append(url)
        return json.dumps({"sha": revision}).encode() if url.endswith("/commits/main") else data

    monkeypatch.setattr(onboarding, "_read_https", read)
    result = onboarding.acquire_catalog()
    assert calls == [
        f"https://api.github.com/repos/{onboarding.CATALOG_REPOSITORY}/commits/main",
        f"https://raw.githubusercontent.com/{onboarding.CATALOG_REPOSITORY}/{revision}/catalog.json",
    ]
    assert result.provenance() == {
        "repository": onboarding.CATALOG_REPOSITORY,
        "revision": revision,
        "path": "catalog.json",
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def test_pinned_revision_never_resolves_main(monkeypatch):
    calls = []
    monkeypatch.setattr(
        onboarding, "_read_https", lambda url: calls.append(url) or json.dumps(payload()).encode()
    )
    onboarding.acquire_catalog(revision="c" * 40)
    assert len(calls) == 1 and "/" + "c" * 40 + "/" in calls[0]


def test_local_catalog_never_uses_network(tmp_path, monkeypatch):
    monkeypatch.setattr(onboarding, "_read_https", lambda _: pytest.fail("unexpected network"))
    path = tmp_path / "catalog.json"
    path.write_text(json.dumps(payload()))
    result = onboarding.acquire_catalog(catalog_path=path)
    assert result.repository is None and result.revision is None
    assert result.path == str(path)


@pytest.mark.parametrize("revision", ["main", "latest", "b" * 39, "../main"])
def test_invalid_pin_fails_before_network(monkeypatch, revision):
    monkeypatch.setattr(onboarding, "_read_https", lambda _: pytest.fail("unexpected network"))
    with pytest.raises(ReleaseResolutionError, match="commit SHA"):
        onboarding.acquire_catalog(revision=revision)


def test_conflicting_catalog_options_fail_before_network(monkeypatch):
    monkeypatch.setattr(onboarding, "_read_https", lambda _: pytest.fail("unexpected network"))
    with pytest.raises(ReleaseResolutionError, match="mutually exclusive"):
        onboarding.acquire_catalog(catalog_path=Path("catalog.json"), revision="c" * 40)


@pytest.mark.parametrize("data", [b"not json", b"{}", b'{"sha":"main"}'])
def test_invalid_commit_response_fails_closed(monkeypatch, data):
    monkeypatch.setattr(onboarding, "_read_https", lambda _: data)
    with pytest.raises(ReleaseResolutionError):
        onboarding.acquire_catalog()


def test_invalid_snapshot_fails_without_retry(monkeypatch):
    calls = []
    monkeypatch.setattr(onboarding, "_read_https", lambda url: calls.append(url) or b"{}")
    with pytest.raises(ReleaseResolutionError, match="Invalid Adapter Catalog"):
        onboarding.acquire_catalog(revision="b" * 40)
    assert len(calls) == 1


def test_provider_rejection_does_not_install(tmp_path, monkeypatch):
    source = pytest.importorskip("orbitfabric_github_release_source")
    errors = pytest.importorskip("orbitfabric_github_release_source.errors")
    path = tmp_path / "catalog.json"
    path.write_text(json.dumps(payload()))

    class RejectingSource:
        def __init__(self, **kwargs):
            pass

        def resolve(self, *args, **kwargs):
            raise errors.GitHubReleaseSourceError("descriptor digest mismatch")

    monkeypatch.setattr(source, "GitHubReleaseSource", RejectingSource)
    result = CliRunner().invoke(
        app,
        ["adapter", "install", "openc3-cosmos", "--version", "0.2.0", "--catalog", str(path)],
        env={"ORBITFABRIC_STATE_DIR": str(tmp_path / "state")},
    )
    assert result.exit_code == 1
    assert "descriptor digest mismatch" in result.stderr
    assert not list((tmp_path / "state").glob("instances/*"))


def test_install_requires_explicit_mode():
    result = CliRunner().invoke(app, ["adapter", "install", "openc3-cosmos"])
    assert result.exit_code == 1 and "--version" in result.stderr
