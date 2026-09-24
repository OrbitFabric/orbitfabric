# Public adapter onboarding

This is the coordinated **unpublished** Core 1.4.0 / GitHub Release Source 0.1.0 / F Prime 0.1.3 candidate. The commands below become public acceptance commands only after approved publication and the exact F Prime descriptor digest is added to the canonical Catalog. No PyPI publication is assumed.

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

## Release order

Prepare and review all candidates before tagging. After approval: publish GitHub Release Source 0.1.0, Core 1.4.0 (including its generated installation manifest), then F Prime 0.1.3. Add the SHA-256 of the exact published descriptor to the Catalog, retaining historical entries. Only then run the public clean-environment commands above against GitHub. Candidate replay tests before publication exercise real wheels, provider integrity and Core lifecycle while substituting only unavailable release HTTP responses; they are not evidence of public asset availability.
