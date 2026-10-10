# OrbitFabric Core documentation

**Start with a mission contract, then follow the same meaning into validation, evidence and integration.**

OrbitFabric Core is the semantic authority for a model-first Mission Data Fabric for small spacecraft. Its multi-file YAML Mission Model states mission data semantics once; Core validates and exports controlled representations so each downstream system does not invent its own interpretation.

This site is the **engineering documentation entry point**. For the short product introduction and first commands, see the [Core repository README](https://github.com/OrbitFabric/orbitfabric).

## Choose your path

### First-time user: run a real Core workflow

1. [Quickstart](QUICKSTART.md): install the checked-out Core and get a first PASS from its synthetic demo.
2. [Demo Walkthrough](DEMO_WALKTHROUGH.md): connect a payload command, data-product intent and host-side Scenario evidence.
3. [Architecture](ARCHITECTURE.md): understand what Core owns and what native systems still own.

These examples prove contract continuity and host-side execution only. They do not qualify flight software or demonstrate a live ground segment.

### Mission engineer: define and validate the contract

The [Mission Model Stability Contract](reference/mission-model-stability-contract.md) explains compatibility rules for documented model semantics. Explore the specific [Payload Contract Model](reference/payload-contract-model.md), [Data Product and Storage Model](reference/data-product-contract-model.md), [Contact and Downlink Model](reference/contact-downlink-contract-model.md), and [Commandability and Autonomy Model](reference/commandability-contract-model.md).

[Scenario Evidence Stability](reference/scenario-evidence-stability.md) describes separate Scenario inputs. [Lint Rule Code Stability](reference/lint-rule-code-stability.md) covers diagnostic compatibility.

### Integrator: consume Core-owned boundaries

The supported stable external-integration input is the [coherent Core Integration Input Set](reference/core-integration-input-contract.md), including the Mission Snapshot, Entity Index, Relationship Manifest, Model Summary and lint report. Required incompatibilities must fail closed; downstream tools must not reinterpret Mission Model YAML as a fallback.

The [Core Interface Manifest](reference/core-interface-manifest.md) is a **candidate** mission-independent capability declaration for negotiating structured interfaces. Extension contracts such as [Projection Profile](reference/projection-profile-contract.md), [Integration Result](reference/integration-result-contract.md), [operation-input v1](reference/integration-contract-v1.md) and [Scenario Projection Accounting](reference/scenario-projection-accounting-contract.md) retain independent candidate status.

### Adapter user: install an exact external release

[Public Adapter Onboarding](reference/public-adapter-onboarding.md) documents the published Core 1.4.0 + GitHub Release Source 0.1.0 route for exact Catalog-based installation without checking out the repositories.

The [Adapter Manager](reference/adapter-manager-m0.md), [Project Lock](reference/adapter-project-lock-m1.md) and [Catalog CLI](reference/adapter-catalog-cli.md) retain explicit lifecycle/desired-state/selection boundaries. Provider-specific download logic is **outside** Core's manager.

### Contributor or reviewer: inspect the decisions

[Project Charter](PROJECT_CHARTER.md), [Architecture](ARCHITECTURE.md), [Roadmap](ROADMAP.md), [Development Guide](DEVELOPMENT.md) and [Clean-Room Policy](CLEAN_ROOM_POLICY.md) cover engineering scope and development constraints.

The [Stability and Compatibility Contract](reference/stability-compatibility-contract.md), [Release Compatibility Policy](reference/release-compatibility-policy.md) and [versioning reference](reference/versioning.md) define how to interpret published, candidate and stable surfaces. ADRs record *why* decisions were made; release notes preserve *when* they were published. Historical decisions must not be retroactively rewritten.

## Core's ownership model at a glance

~~~text
Mission Model (semantic source of truth)
       |
       v
OrbitFabric Core
  load / validate / lint / normalize / generate / export
       |                                  |
       | separate Scenario inputs         | Core-owned structured exports
       v                                  v
host-side declared evidence       external consumers and adapters
                                        |
                                        v
                                 native integration / runtime
                                 (authority remains outside Core)
~~~

This is a map of responsibilities, **not** an obligatory sequential workflow.

The Mission Model remains the semantic source of truth; operational Scenarios are independent evidence inputs; generated artifacts and structured exports are derived. Integration adapters own target-specific projections. Native systems remain authoritative for implementation and observation. Studio presents Core-owned facts without redefining them.

## Publication and maturity

**Latest published Core product:** [v1.4.0, 25 September 2026](releases/v1.4.0.md).

- **Stable v1.x:** documented Mission Model semantics and selected Core-owned reports/exports, including the v1.2 Mission Snapshot and coherent Integration Input Set.
- **Candidate:** Core Interface Manifest, Scenario Declaration, inspection/coverage surfaces, adapter lifecycle and separately versioned extension/evidence contracts.
- **Generated preview:** C++17 runtime contract bindings, generic ground artifacts and generated Markdown.

A published `1.4.0` package is not a blanket stability promise for every interface. Some stable Core outputs retain previously assigned `0.1-candidate` format identifiers: wire identifiers and compatibility classification are different engineering decisions. Refer to the [authoritative classification](reference/stability-compatibility-contract.md), not this short summary, for consumer obligations.

## Practical boundaries

Core does not implement onboard scheduling, live command uplink, ground archives, spacecraft dynamics, CCSDS/PUS/CFDP stacks, flight qualification or adapter-specific runtime behavior. It does not load arbitrary target adapter logic into its own process.

The synthetic demo, reference integration contracts and published adapter onboarding demonstrate **different evidence scopes**. A successful host-side Scenario is not evidence of native target execution.

## Further reading

For the published release and prior release history, see the [Core Release Guide](releases/index.md). Earlier notes remain available but are not the current product instructions.

For the complete reference collection organized by topic, use the [Core Reference Guide](reference/index.md). It indexes the existing reference pages without changing their paths or compatibility commitments.

- [v1.4.0 release notes](releases/v1.4.0.md) and [Changelog](https://github.com/OrbitFabric/orbitfabric/blob/main/CHANGELOG.md)
- [CLI Contract v1](reference/cli-contract-v1.md) and [JSON Report Compatibility](reference/json-report-compatibility.md)
- [Generated Surfaces Stability](reference/generated-surfaces-stability.md) and [Evidence Set Manifest](reference/evidence-set-manifest-contract.md)
- [OrbitFabric repository and contribution guide](https://github.com/OrbitFabric/orbitfabric)
