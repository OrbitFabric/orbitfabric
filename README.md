<div align="center">
  <img src="assets/brand/orbitfabric-logo-horizontal-light.png" alt="OrbitFabric" width="760">
</div>

<p align="center">
  <strong>Define once. Validate. Simulate. Test. Document. Integrate.</strong>
</p>

# OrbitFabric Core

**One Mission Data Contract. Multiple engineering consumers. No parallel interpretation of mission meaning.**

Mission information is often copied into flight software declarations, ground dictionaries, test cases, engineering documents and integration configurations. Those copies can drift even when every team is working correctly.

OrbitFabric Core gives small-spacecraft engineering teams a **model-first Mission Data Fabric**: define the mission data contract in a structured Mission Model, validate it once, and derive inspectable engineering artifacts and explicit integration inputs from the same semantics.

Core owns the meaning of the Mission Data Contract. It does **not** replace the systems that implement or operate a spacecraft.

## What you can do today

| Engineering need | What Core provides |
| --- | --- |
| Define a coherent mission | Multi-file YAML Mission Model with spacecraft, subsystem, mode, telemetry, command, event, fault, packet, payload, data-product, contact and autonomy contracts |
| Detect contract inconsistencies | Structural validation and semantic lint with explicit diagnostics |
| Exercise declared behavior | Deterministic, host-side Scenario execution and structured evidence; Scenarios are separate from the Mission Model |
| Produce reviewable outputs | Generated mission/data-flow documentation, C++17 runtime-facing contract bindings and generic ground-facing artifacts |
| Inspect the contract without reparsing YAML | Core-owned Model Summary, Entity Index, Relationship Manifest and Mission Snapshot |
| Integrate external systems | Stable, coherent Core Integration Input Set plus independently versioned candidate extension contracts |
| Identify and manage external adapters | Candidate Adapter Manager lifecycle, exact Catalog selection and public GitHub Release-based installation composition |

The Mission Model is the **semantic source of truth**. Scenarios supply authored test intent, not a second Mission Model. Generated files are derived and normally disposable. Host-side Scenario evidence is not native flight or ground runtime evidence.

## Try Core on its synthetic demo

**Requirements:** Python 3.11+ and Git. These commands use the checked-out Core repository so the demo model and scenarios are available.

~~~bash
git clone https://github.com/OrbitFabric/orbitfabric.git
cd orbitfabric
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"

orbitfabric --version
orbitfabric inspect mission examples/demo-3u/mission/
orbitfabric lint examples/demo-3u/mission/
orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml
~~~

At the v1.4.0 baseline, `orbitfabric --version` reports `orbitfabric 1.4.0`. The demo commands inspect, lint and exercise a *synthetic* Mission Model. A successful simulation establishes bounded host-side contract evidence, not spacecraft behavior.

To see what Core can export from one validated contract:

~~~bash
orbitfabric export integration-input-set examples/demo-3u/mission/
~~~

This creates the stable coherent input boundary for downstream integration. For output paths, platform-specific setup and further commands, follow the [Quickstart](docs/QUICKSTART.md), then the [Demo Walkthrough](docs/DEMO_WALKTHROUGH.md).

## How the engineering boundary works

~~~text
Mission Model (YAML)  ---------------------+
  Semantic source of truth               |
                                         v
                               OrbitFabric Core
                               load / validate / lint
                               normalize / export / generate
                                  |          |
Operational Scenarios (YAML) -----+          |
  Separate evidence inputs        |          |
                                  v          v
                           Host-side     Core-owned facts
                           evidence      and generated artifacts
                                             |
                                             v
                              External integration consumers
                              and target-specific adapters
~~~

The diagram expresses **ownership**, not a required execution pipeline.

- **Core:** interprets the Mission Data Contract, validates and normalizes Core-owned information, publishes generic boundaries and governs the provider-neutral installed-adapter lifecycle.
- **External integration adapters:** consume explicit Core-owned inputs and authored Projection Profiles, then own target-specific validation, mapping, artifact generation and Integration Results.
- **Native flight and ground systems:** remain authoritative for implementation, execution and observations.
- **Studio:** helps engineers understand Core-owned facts; it does not become another semantic authority.

The public [OrbitFabric organization](https://github.com/OrbitFabric) explains the wider ecosystem. This repository documents **Core as an engineering product**, not the implementation of the other repositories.

## Two supported ways to get started

**Explore the Mission Data Contract:** use the source checkout above. It includes the example mission, CLI, development checks and reference documentation.

**Install published product wheels without cloning:** Core v1.4.0 and the external GitHub Release Source v0.1.0 have a coordinated GitHub Release-based installation manifest:

~~~bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r https://github.com/OrbitFabric/orbitfabric/releases/download/v1.4.0/orbitfabric-install.txt
orbitfabric --version
orbitfabric adapter install fprime --version 0.1.3
~~~

This path uses published wheels and an exact adapter release from the canonical Catalog. It is **not** a way to obtain the repository's demo files and it is not a PyPI publication. The GitHub provider remains a separate distribution and resolves exact release material outside the Core Adapter Manager. See [Public Adapter Onboarding](docs/reference/public-adapter-onboarding.md) for prerequisites, provenance, alternate exact selectors and verification steps.

## Version and compatibility

**Current published Core product:** [v1.4.0 (25 September 2026)](https://github.com/OrbitFabric/orbitfabric/releases/tag/v1.4.0).

**Stable commitments:** v1.0.0 established the documented Mission Data Contract. v1.2.0 added a stable Mission Snapshot, a coherent Integration Input Set and seven additive FDIR Relationship Manifest families. Existing format identifiers such as `0.1-candidate` can remain unchanged when a *separate compatibility decision* has already classified a surface as stable.

**Candidate, not silently stable:** Core Interface Manifest, Scenario Declaration, dashboard/scenario-run/coverage inspection surfaces, structured expectation accounting, generic integration/Scenario Projection Accounting/Evidence Set contracts and Adapter Management lifecycle/selection interfaces. The Core product release number never promotes those contracts automatically.

**Public-preview generated outputs:** runtime-facing C++17 bindings, generic ground artifacts and generated documentation. These do not constitute native runtime implementations.

For contractual details, consult [Stability and Compatibility](docs/reference/stability-compatibility-contract.md), [Mission Model Stability](docs/reference/mission-model-stability-contract.md), [Core Integration Input](docs/reference/core-integration-input-contract.md), [Core Interface Manifest](docs/reference/core-interface-manifest.md) and the [v1.4.0 release notes](docs/releases/v1.4.0.md).

## Where to read next

| Your goal | Start here |
| --- | --- |
| Run the first commands and see expected outputs | [Quickstart](docs/QUICKSTART.md) |
| Follow one contract through the synthetic evidence chain | [Demo Walkthrough](docs/DEMO_WALKTHROUGH.md) |
| Understand responsibilities, system boundaries and non-goals | [Architecture](docs/ARCHITECTURE.md) and [Project Charter](docs/PROJECT_CHARTER.md) |
| Build an integration against stable Core-owned inputs | [Core Integration Input Contract](docs/reference/core-integration-input-contract.md) |
| Inspect the CLI and machine-readable contracts | [CLI Contract](docs/reference/cli-contract-v1.md) and [JSON Report Compatibility](docs/reference/json-report-compatibility.md) |
| Install a published external adapter release | [Public Adapter Onboarding](docs/reference/public-adapter-onboarding.md) |
| Understand milestones and release evolution | [Roadmap](docs/ROADMAP.md), [Changelog](CHANGELOG.md) and [Releases](docs/releases/v1.4.0.md) |
| Work on the code or contribute | [Development Guide](docs/DEVELOPMENT.md) and [Contributing](CONTRIBUTING.md) |

Published documentation: https://orbitfabric.github.io/orbitfabric/

## Development and project boundaries

Core is not a flight software framework, mission control system, live ground segment, spacecraft dynamics simulator, hardware abstraction layer or provider-neutral package registry. It does not import ecosystem-specific adapter implementations in-process or infer undocumented target semantics.

For repository development:

~~~bash
ruff check .
pytest
mkdocs build --strict
~~~

CI tests Python 3.11 and 3.12. C++17 generated-binding smoke tests additionally need CMake and a C++17-capable compiler.

Contributions must be clean-room. Do not publish confidential, employer-owned, customer-owned, export-controlled or NDA-protected designs, source, logs or mission data. Use synthetic examples or material that may legally be redistributed. See [Clean-Room Policy](docs/CLEAN_ROOM_POLICY.md), [Security](SECURITY.md) and [Code of Conduct](CODE_OF_CONDUCT.md).

OrbitFabric is licensed under [Apache License 2.0](LICENSE). External project references do not imply endorsement, adoption or verified operational integration.
