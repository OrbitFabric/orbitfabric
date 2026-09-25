"""Build the no-clone product installation manifest from exact built wheels."""

from __future__ import annotations

import argparse
import hashlib
import zipfile
from email.parser import BytesParser
from pathlib import Path


def requirement(wheel: Path, base_url: str | None = None) -> str:
    with zipfile.ZipFile(wheel) as archive:
        metadata = [name for name in archive.namelist() if name.endswith(".dist-info/METADATA")]
        if len(metadata) != 1:
            raise ValueError("Expected exactly one wheel METADATA")
        message = BytesParser().parsebytes(archive.read(metadata[0]))
    name, version = message["Name"], message["Version"]
    repositories = {
        "orbitfabric": "orbitfabric",
        "orbitfabric-github-release-source": "orbitfabric-github-release-source",
    }
    if name not in repositories:
        raise ValueError(f"Unexpected product distribution: {name}")
    base = base_url or (
        f"https://github.com/OrbitFabric/{repositories[name]}/releases/download/v{version}"
    )
    digest = hashlib.sha256(wheel.read_bytes()).hexdigest()
    return f"{name} @ {base.rstrip('/')}/{wheel.name}#sha256={digest}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--core-wheel", type=Path, required=True)
    parser.add_argument("--provider-wheel", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--base-url", help="Artifact mirror used only for candidate acceptance")
    args = parser.parse_args()
    lines = [
        requirement(args.core_wheel, args.base_url),
        requirement(args.provider_wheel, args.base_url),
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "# Exact OrbitFabric product wheels; no VCS dependencies.\n" + "\n".join(lines) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
