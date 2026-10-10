# Core Reference Guide

This page helps you find the right OrbitFabric Core contract, explanation or historical decision without reading the entire reference section in release order.

**Published Core product:** [v1.4.0](../releases/v1.4.0.md).

**Key distinction:** a published Core package does not make every documented interface stable. Contract maturity is assigned through explicit compatibility decisions, separately from package versions and wire-format identifiers.

For a first execution, begin with the [Quickstart](../QUICKSTART.md) and [synthetic Demo Walkthrough](../DEMO_WALKTHROUGH.md). For the complete system boundary, see [Architecture](../ARCHITECTURE.md).

## How to read the reference

| Question | Start with | Boundary to remember |
| --- | --- | --- |
| What is stable in Core? | [Stability and Compatibility Contract](stability-compatibility-contract.md) | Stable classification is not inferred from an interface version string. |
| What version should a consumer check? | [Versioning Model](versioning.md) | Product versions, contract versions and exact source identities are separate. |
| How does Core preserve mission meaning? | [Mission Model Stability Contract](mission-model-stability-contract.md) | The Mission Model is the source of mission semantics. |
| What can an external adapter consume? | [Core Integration Input Contract](core-integration-input-contract.md) | Required surfaces must be validated as a coherent set. |
| What can Core declare without executing? | [Core Interface Manifest](core-interface-manifest.md) and [Scenario Declaration Surface](scenario-declaration-surface.md) | These declarations are candidate interfaces, not execution observations. |
| How do I install an exact external adapter release? | [Public Adapter Onboarding](public-adapter-onboarding.md) | Provider acquisition stays separate from the Core installation manager. |

## Reference topics

The left navigation includes every reference document, organized into the groups below. Pages keep their existing paths and identifiers.

### Compatibility and governance

Use [Stability and Compatibility](stability-compatibility-contract.md) for current maturity labels and [Post-v1 Surface Classification](post-v1-candidate-integration-surfaces.md) for the chronology of promotions and candidate additions. [Release Compatibility Policy](release-compatibility-policy.md) defines review obligations; [Versioning Model](versioning.md) distinguishes wire, product and adapter versions.

The [CLI Contract](cli-contract-v1.md), [JSON Report Compatibility](json-report-compatibility.md), [Extensibility Boundary](extensibility-boundary-contract.md) and [Generated Surfaces Stability](generated-surfaces-stability.md) provide further consumer and governance rules.

### Mission Model and Scenario contracts

Start with [Mission Model v0.1](mission-model-v0.1.md) and [Mission Model Stability](mission-model-stability-contract.md). Domain references cover [Payload](payload-contract-model.md), [Data Product and Storage](data-product-contract-model.md), [Contact and Downlink](contact-downlink-contract-model.md) and [Commandability and Autonomy](commandability-contract-model.md).

[Scenario Evidence Stability](scenario-evidence-stability.md) describes separate authored Scenario inputs. [Data Flow Evidence](data-flow-evidence.md) explains a contract-level chain; it does not imply real downlink execution.

### Stable structured outputs

The [Mission Snapshot](mission-snapshot-surface.md), [Entity Index](entity-index-surface.md) and [Relationship Manifest](relationship-manifest-surface.md) describe Core-owned structures. The [Core Integration Input Contract](core-integration-input-contract.md) specifies the coherent stable external input boundary.

These documents define their own supported fields and family semantics. The stable classification does not require changing historical `0.1-candidate` format identifiers.

### Candidate Core inspection

The [Dashboard Summary](dashboard-summary-surface.md), [Scenario Run Index](scenario-run-index-surface.md) and [Coverage Summary](coverage-summary-surface.md) remain candidate inspection surfaces. The [Scenario Declaration](scenario-declaration-surface.md) and [Core Interface Manifest](core-interface-manifest.md) are additional candidate declarations introduced in the Core v1.4.0 period.

An authored declaration, a host-side Scenario result and a native observation are different forms of information. One cannot substitute for another.

### Generated engineering artifacts

[Runtime Contract Bindings](runtime-contract-bindings.md) describe generated C++ contract-facing outputs, and [Ground Integration Artifacts](ground-integration-artifacts.md) describe generic ground-facing exports. Neither supplies onboard runtime behavior or a live ground segment.

### External integration contracts

[Projection Profile](projection-profile-contract.md) records authored target-specific intent. [Integration Package and Adapter Execution](integration-package-adapter-execution-contract.md) and [Integration Result](integration-result-contract.md) define explicit package/result boundaries. [Operation-Input v1](integration-contract-v1.md) and the [Compatibility Matrix](integration-contract-compatibility-matrix.md) clarify the independent candidate lanes.

[Scenario Projection Accounting](scenario-projection-accounting-contract.md) is an optional adapter-declared Result-owned artifact. [Evidence Set Manifest](evidence-set-manifest-contract.md) governs generic retained evidence identity, integrity and typed correlation without interpreting the producer's native content.

### Adapter management and onboarding

The [Adapter Manager](adapter-manager-m0.md), [Adapter Project Lock](adapter-project-lock-m1.md), [Catalog CLI](adapter-catalog-cli.md) and [Explicit-Source Install from Lock](adapter-install-from-lock-explicit-source.md) describe candidate lifecycle, desired-state and exact-selection surfaces.

[Public Adapter Onboarding](public-adapter-onboarding.md) describes Core v1.4.0 CLI composition with the separately distributed GitHub Release Source. That single supported provider route is not a general provider dispatch API.

### Historical decisions and evidence

The reference section also preserves the [v1.0 Candidate Surface Inventory](v1-candidate-surface-inventory.md), [v1.0 Stable Surface Decision](v1-stable-surface-decision.md), [v1.0 Demo Evidence Chain](v1-demo-evidence-chain.md) and [v1.2 Integration Input Stability Decision](v1.2-integration-input-stability-decision.md).

Historical documents remain authoritative for the decisions made at their respective baselines. Consult the current stability and versioning references for present-day classification. This navigation update does not rewrite past decisions.

## Scope of this guide

This guide is an index, not a new normative contract. When summaries differ in detail from a reference contract or an explicit release compatibility decision, follow the detailed source and its documented version boundary. Other OrbitFabric repositories maintain their own target-specific implementation and native evidence.
