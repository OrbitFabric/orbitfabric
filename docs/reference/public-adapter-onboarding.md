# Public adapter onboarding

Status: **Published GitHub Release-based product onboarding (2026-09-25)**. Core [1.4.0](https://github.com/OrbitFabric/orbitfabric/releases/tag/v1.4.0), [GitHub Release Source 0.1.0](https://github.com/OrbitFabric/orbitfabric-github-release-source/releases/tag/v0.1.0), and [F Prime Adapter 0.1.3](https://github.com/OrbitFabric/orbitfabric-fprime-adapter/releases/tag/v0.1.3) are published releases, not unpublished candidates. **Their adapter lifecycle and integration contract surfaces retain candidate maturity.** No PyPI publication is assumed.

The canonical Catalog currently includes `github.com/OrbitFabric:orbitfabric/fprime@0.1.3` with Release Descriptor SHA-256 `b5e078ccf5a8ae61575b1a69dd6dafcf925cdebb4900e20c25a27efffdf23be1`, matching GitHub's published descriptor asset digest. Catalog `main` may change: select an exact `--catalog-revision` or local snapshot when repeatability matters.

## Clean Python 3.11+ environment

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r https://github.com/OrbitFabric/orbitfabric/releases/download/v1.4.0/orbitfabric-install.txt
orbitfabric adapter install fprime --version 0.1.3
orbitfabric adapter list
orbitfabric adapter verify <instance-id>
```

The installation manifest names exact Core and GitHub Release Source wheels with SHA-256 URL fragments. Runtime Python dependencies are resolved by pip. Neither repository clones nor Git are required. Adapter descriptor and artifact downloads are automatic. No Project Lock is needed for this path.

```bash
orbitfabric adapter install orbitfabric/fprime --version 0.1.3
orbitfabric adapter install github.com/OrbitFabric:orbitfabric/fprime --version 0.1.3
orbitfabric adapter install fprime --version 0.1.3 --catalog-revision <40-character-commit-sha>
orbitfabric adapter install fprime --version 0.1.3 --catalog ./catalog.json --json
```

The default Catalog repository is `OrbitFabric/orbitfabric-adapter-catalog`. Each invocation resolves `main` to an exact commit, fetches `catalog.json` at that commit, validates it and reports repository, revision, path and byte SHA-256. A pinned revision skips mutable-ref resolution. A local snapshot makes no Catalog network request and reports its absolute path and digest. The two overrides are mutually exclusive. There is no persistent cache, refresh timer or fallback to another snapshot.

Logical selection filters by both key and exact version across Catalog records before counting matches. One match succeeds; zero or multiple matches fail closed. Bare names also require uniqueness across publishers. `openc3-cosmos --version 0.2.0` selects `github.com/OrbitFabric:orbitfabric/openc3-cosmos@0.2.0`; historical FAROTECH 0.1.0 is retained without causing ambiguity. There are no authority aliases, preferred authorities, version ranges, latest, stable or automatic upgrades. The full coordinate and exact version remain the installed identity.

Core application composition calls `GitHubReleaseSource.resolve(...)`, then `AdapterManager.install_resolved(...)`. The provider verifies the Catalog-bound descriptor digest, exact identity/version and selected artifact digest/size. Core owns acceptance, managed environment installation, inventory and verification. GitHub transport stays outside the lifecycle layer. Only one GitHub Release binding is supported for this command; no provider registry or mirror preference is introduced.

Remote `--json` output contains `installed` and `catalog_snapshot`. Existing local JSON output remains the installed record. The old explicit path remains available:

```bash
orbitfabric adapter install ./adapter-release.json --artifact ./adapter.whl
```

Project Locks remain exact reproducible project desired state. Existing ensure MATCH returns NOOP without acquisition. Snapshot provenance describes Catalog bytes; it does not turn Catalog membership into publisher authentication.

## Published release record and acceptance boundary

The coordinated release sequence completed on **2026-09-25**: GitHub Release Source 0.1.0, Core 1.4.0 with its installation manifest, and F Prime Adapter 0.1.3. The exact published F Prime Release Descriptor digest is present in the canonical Catalog, while historical entries remain available.

The [Core release assets](https://github.com/OrbitFabric/orbitfabric/releases/tag/v1.4.0) include the wheel, source distribution, `orbitfabric-install.txt`, and `SHA256SUMS`. The GitHub Release API confirms public publication and uploaded assets. The published download manifest uses exact wheel hashes; a separate clean-environment replay remains necessary to establish end-to-end installation acceptance. Pre-publication candidate replay tests are not a substitute for that test.

Core ownership does not change: the external GitHub Release Source fetches and verifies provider release bytes, while Core validates resolved release identity and owns installation and installed state. Adapter-related contracts remain candidate even though the coordinated **products** are publicly released.
