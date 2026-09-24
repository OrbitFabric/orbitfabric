"""Application composition for the supported GitHub installation lane.

This is not a provider registry. Catalog and lifecycle semantics remain in
adapter_manager; release transport remains in orbitfabric_github_release_source.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from orbitfabric.adapter_manager import (
    AdapterCatalog,
    AdapterManager,
    ExactCatalogReleaseSelection,
    InstalledAdapterRecord,
    select_exact_release,
    select_exact_release_by_logical_key,
)
from orbitfabric.adapter_manager.errors import AdapterManagerError, ReleaseResolutionError
from orbitfabric.adapter_manager.models import AdapterSourceCoordinate

CATALOG_REPOSITORY = "OrbitFabric/orbitfabric-adapter-catalog"
CATALOG_PATH = "catalog.json"
_COMMIT = re.compile(r"[0-9a-f]{40}\Z")
_MAX_RESPONSE = 8 * 1024 * 1024


@dataclass(frozen=True)
class CatalogSnapshot:
    catalog: AdapterCatalog
    repository: str | None
    revision: str | None
    path: str
    sha256: str

    def provenance(self) -> dict[str, str | None]:
        return {
            "repository": self.repository,
            "revision": self.revision,
            "path": self.path,
            "sha256": self.sha256,
        }


def _read_https(url: str) -> bytes:
    headers = {"User-Agent": "orbitfabric-adapter-onboarding"}
    if url.startswith("https://api.github.com/"):
        headers["Accept"] = "application/vnd.github+json"
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
    try:
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read(_MAX_RESPONSE + 1)
        if len(data) > _MAX_RESPONSE:
            raise ReleaseResolutionError("Canonical Catalog response exceeds size limit")
        return data
    except (OSError, urllib.error.URLError) as exc:
        raise ReleaseResolutionError(f"Cannot acquire canonical Catalog: {url}") from exc


def acquire_catalog(
    *,
    catalog_path: Path | None = None,
    revision: str | None = None,
) -> CatalogSnapshot:
    if catalog_path is not None and revision is not None:
        raise ReleaseResolutionError("--catalog and --catalog-revision are mutually exclusive")
    if catalog_path is not None:
        path = catalog_path.expanduser().resolve()
        try:
            data = path.read_bytes()
        except OSError as exc:
            raise ReleaseResolutionError(f"Cannot read Catalog: {path}") from exc
        repository = None
        snapshot_path = str(path)
    else:
        repository = CATALOG_REPOSITORY
        snapshot_path = CATALOG_PATH
        if revision is None:
            try:
                result = json.loads(
                    _read_https(f"https://api.github.com/repos/{repository}/commits/main")
                )
                revision = result["sha"]
            except (ValueError, KeyError, TypeError) as exc:
                raise ReleaseResolutionError("Invalid canonical Catalog commit response") from exc
        if not isinstance(revision, str) or not _COMMIT.fullmatch(revision):
            raise ReleaseResolutionError(
                "Catalog revision must be an exact 40-character commit SHA"
            )
        data = _read_https(
            f"https://raw.githubusercontent.com/{repository}/{revision}/{CATALOG_PATH}"
        )
    try:
        catalog = AdapterCatalog.model_validate_json(data)
    except ValueError as exc:
        raise ReleaseResolutionError("Invalid Adapter Catalog snapshot") from exc
    return CatalogSnapshot(
        catalog, repository, revision, snapshot_path, hashlib.sha256(data).hexdigest()
    )


def select_install_release(
    catalog: AdapterCatalog,
    identity: str,
    version: str,
) -> ExactCatalogReleaseSelection:
    if not version or not version.strip():
        raise ReleaseResolutionError("An exact release version is required")
    if ":" in identity:
        authority, logical = identity.split(":", 1)
        parts = logical.split("/")
        if not authority or len(parts) != 2 or not all(parts):
            raise ReleaseResolutionError("Use AUTHORITY:PUBLISHER/NAME for a Source Coordinate")
        return select_exact_release(
            catalog,
            AdapterSourceCoordinate(authority=authority, publisher=parts[0], name=parts[1]),
            version,
        )
    parts = identity.split("/")
    if len(parts) == 2 and all(parts):
        return select_exact_release_by_logical_key(
            catalog,
            publisher=parts[0],
            name=parts[1],
            release_version=version,
        )
    if len(parts) != 1 or not identity:
        raise ReleaseResolutionError("Use NAME, PUBLISHER/NAME or AUTHORITY:PUBLISHER/NAME")
    matches = [
        adapter
        for adapter in catalog.adapters
        if adapter.source_coordinate.name == identity
        and any(release.version == version for release in adapter.releases)
    ]
    if len(matches) != 1:
        candidates = ", ".join(a.source_coordinate.display() for a in matches)
        raise ReleaseResolutionError(
            f"Expected one exact Catalog release for {identity}@{version}, found {len(matches)}"
            + (f"; use a full Source Coordinate: {candidates}" if candidates else "")
        )
    return select_exact_release(catalog, matches[0].source_coordinate, version)


def install_from_catalog(
    identity: str,
    version: str,
    *,
    catalog_path: Path | None = None,
    revision: str | None = None,
    artifact_id: str | None = None,
    manager: AdapterManager | None = None,
) -> tuple[InstalledAdapterRecord, CatalogSnapshot]:
    snapshot = acquire_catalog(catalog_path=catalog_path, revision=revision)
    selection = select_install_release(snapshot.catalog, identity, version)
    # One supported lane, with no provider preference or mirror fallback.
    if len(selection.sources) != 1:
        raise ReleaseResolutionError("Installation requires exactly one Catalog source binding")
    if selection.sources[0].binding.provider != "github-release":
        raise ReleaseResolutionError("Installation currently supports only github-release bindings")
    try:
        from orbitfabric_github_release_source import GitHubReleaseSource
        from orbitfabric_github_release_source.errors import GitHubReleaseSourceError
    except ImportError as exc:
        raise ReleaseResolutionError(
            "GitHub acquisition package is unavailable; install the OrbitFabric product bundle"
        ) from exc
    try:
        with tempfile.TemporaryDirectory(prefix="orbitfabric-adapter-") as temporary:
            resolution = GitHubReleaseSource(token=os.environ.get("GITHUB_TOKEN")).resolve(
                selection,
                Path(temporary),
                artifact_id=artifact_id,
            )
            record = (manager or AdapterManager()).install_resolved(resolution.resolved_release)
    except GitHubReleaseSourceError as exc:
        raise AdapterManagerError(str(exc)) from exc
    return record, snapshot
