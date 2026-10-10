# Demo Walkthrough

Follow the synthetic `demo-3u` mission from one Mission Data Contract to host-side Scenario evidence, structured Core exports and contract-facing generated artifacts.

**Current Core product release:** [v1.4.0](releases/v1.4.0.md), published 25 September 2026.

**Stability boundaries:** The documented Mission Data Contract is stable from v1.0.0; v1.2.0 introduced a stable coherent Core Integration Input Set and Mission Snapshot. Later Core inspection, adapter-management and generic integration contracts retain their individually documented candidate classifications. The product version does not promote them automatically.

The mission and scenarios are synthetic and clean-room. This walkthrough does not represent a real CubeSat, an actual flight run, a live ground segment, or observed spacecraft behavior.

## A short first run

Complete the repository installation from the [Quickstart](QUICKSTART.md) and run these commands from the checkout root:

```bash
orbitfabric inspect mission examples/demo-3u/mission/
orbitfabric sim examples/demo-3u/scenarios/payload_data_flow_evidence.yaml
```

Both commands should report `Result: PASSED` for the v1.4.0 baseline. The first checks that Core can load the declared Mission Model. The second evaluates a separate authored Scenario **on the host**, including expectations about payload commandability, data-product intent, storage, downlink assumptions and the selected contact window.

The two commands do **not** generate a native payload data product, use physical storage, schedule a radio link or execute flight software.

Continue below to see the source files, the relationships under test and the independently generated Core-owned outputs.

---

## 1. Demo purpose

The `demo-3u` mission demonstrates the OrbitFabric vertical slice:

```text
Define once. Validate. Simulate. Test. Document. Integrate.
```

The goal is not to model a real CubeSat.

The goal is to show how one Mission Data Contract is validated and reused in independently derived outputs: host-side Scenario evidence, stable structured inspection surfaces, a coherent external-integration input set, contract-facing generated artifacts, candidate inspection surfaces, golden signatures and explicit compatibility governance.

The built-in demo is not an Adapter Catalog, provider acquisition or public adapter installation demo. Core v1.4.0 offers a separate [published adapter onboarding workflow](reference/public-adapter-onboarding.md) backed by independently distributed releases. A successful `demo-3u` run is not evidence that public assets were installed or that a native adapter executed.

---

## 2. Demo structure

The demo lives under:

```text
examples/demo-3u/
├── mission/
│   ├── spacecraft.yaml
│   ├── subsystems.yaml
│   ├── modes.yaml
│   ├── telemetry.yaml
│   ├── commands.yaml
│   ├── events.yaml
│   ├── faults.yaml
│   ├── packets.yaml
│   ├── policies.yaml
│   ├── payloads.yaml
│   ├── data_products.yaml
│   ├── contacts.yaml
│   └── commandability.yaml
└── scenarios/
    ├── battery_low_during_payload.yaml
    ├── nominal_payload_acquisition.yaml
    └── payload_data_flow_evidence.yaml
```

The `mission/` directory contains the Mission Model.

The `scenarios/` directory contains executable host-side operational scenarios.

---

## 3. Scenario evidence chain

The selected Scenario is `examples/demo-3u/scenarios/payload_data_flow_evidence.yaml`. It references the Mission Model through `mission.path` and declares a contract-level sequence:

```text
payload.start_acquisition
    -> command accepted (Scenario expectation)
    -> payload.acquisition_started (Scenario expectation)
    -> payload lifecycle ACQUIRING (Scenario expectation)
    -> payload.radiation_histogram (declared data-product intent)
    -> science storage and next-contact downlink intent
    -> science_next_available_contact (declared eligible flow)
    -> demo_contact_001 (declared contact assumption)
```

The labels are claims exercised or checked by Core's deterministic host-side Scenario machinery. They do not assert that bytes were acquired, stored, transmitted or observed on a spacecraft.

**The derived outputs are siblings, not serial execution stages:**

```text
Mission Model (one source of mission semantics)
    |
    +--> Core structural validation and semantic lint
    |
    +--> Core-owned exports
    |      Mission Snapshot / Model Summary / Entity Index
    |      Relationship Manifest / coherent Integration Input Set
    |
    +--> Contract-facing generators
           mission docs / runtime bindings / ground artifacts

Scenario YAML (separate authored evidence input)
    |
    +--> Core host-side Scenario execution
           simulation report / expectation evidence / timeline log
```

In particular, generated C++ bindings and ground dictionaries are **not produced by the Scenario runner** and are not proof of successful flight or ground execution. The Scenario references Mission Model semantics; Core validates those references and owns the host-side interpretation.

The scenario's `data_flow` expectation explicitly names the data product, triggering command, storage/downlink intent, eligible flow and contact window. Those exact references are visible in the synthetic [Scenario source](https://github.com/OrbitFabric/orbitfabric/blob/main/examples/demo-3u/scenarios/payload_data_flow_evidence.yaml).

This demonstrates bounded Mission Data Contract continuity, not operational readiness or protocol compliance.

---

## 4. Run the scenarios

Battery-low recovery:

```bash
orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml
```

Payload data-flow evidence:

```bash
orbitfabric sim examples/demo-3u/scenarios/payload_data_flow_evidence.yaml
```

Expected result:

```text
Result: PASSED
```

Generate scenario JSON reports and logs:

```bash
orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml \
  --json examples/demo-3u/generated/reports/battery_low_during_payload_report.json \
  --log examples/demo-3u/generated/logs/battery_low_during_payload.log

orbitfabric sim examples/demo-3u/scenarios/payload_data_flow_evidence.yaml \
  --json examples/demo-3u/generated/reports/payload_data_flow_evidence_report.json \
  --log examples/demo-3u/generated/logs/payload_data_flow_evidence.log
```

The simulation JSON reports include additive v1.1.0 structured expectation accounting while preserving the legacy top-level `failed_expectations` compatibility list. Those additions remain candidate in v1.4.0.

---

## 5. Export stable Core-owned structured surfaces

The stable Core-owned inspection chain is:

```text
mission_snapshot.json       -> What complete Mission Model did Core load?
model_summary.json          -> What contract domains are present?
entity_index.json           -> What contract entities are defined?
relationship_manifest.json  -> Which admitted explicit relationships connect them?
```

Export the stable surfaces:

```bash
orbitfabric export mission-snapshot examples/demo-3u/mission/ \
  --json examples/demo-3u/generated/reports/mission_snapshot.json

orbitfabric export model-summary examples/demo-3u/mission/ \
  --json examples/demo-3u/generated/reports/model_summary.json

orbitfabric export entity-index examples/demo-3u/mission/ \
  --json examples/demo-3u/generated/reports/entity_index.json

orbitfabric export relationship-manifest examples/demo-3u/mission/ \
  --json examples/demo-3u/generated/reports/relationship_manifest.json
```

The seven FDIR relationship families admitted in v1.2.0 are additive stable-compatible families derived from explicit Mission Model fields. Unknown additive family semantics must never be guessed.

These reports are read-only Core-owned structured surfaces. They do not expose graph behavior, flight runtime behavior, ground behavior or Studio-specific APIs.

---

## 6. Export the stable Core Integration Input Set

The production-facing Core-to-external-integration boundary is:

```bash
orbitfabric export integration-input-set examples/demo-3u/mission/ \
  --output-dir examples/demo-3u/generated/reports/integration_input
```

The coherent set contains:

```text
integration_input_manifest.json
mission_snapshot.json
entity_index.json
relationship_manifest.json
lint_report.json
model_summary.json
```

The manifest records exact surface roles, availability, kind/version identity and SHA-256 digests plus a deterministic RFC 8785/JCS-based `input_set_sha256`.

The manifest is published last. Without a valid manifest, a directory of files is not a coherent Integration Input Set.

An external adapter must reject incompatible required surfaces and must not reconstruct semantics from raw Mission Model YAML.

---

## 7. Export candidate v1.1.0 Core-owned inspection surfaces

The candidate Core-owned inspection chain remains:

```text
dashboard_summary.json       -> Dashboard-ready aggregation of existing Core facts
scenario_run_index.json      -> Index of Core simulation JSON report runs
coverage_summary.json        -> Limited coverage derived from Core structured outputs
simulation JSON expectations -> Additive structured expectation accounting
```

Export the candidate surfaces:

```bash
orbitfabric export dashboard-summary examples/demo-3u/mission/

orbitfabric export scenario-run-index \
  --simulation-reports examples/demo-3u/generated/reports \
  --json examples/demo-3u/generated/reports/scenario_run_index.json

orbitfabric export coverage-summary examples/demo-3u/mission/
```

These surfaces remain candidate in Core v1.4.0. They do not make Core a dashboard backend, Studio API, graph engine, flight runtime framework or ground segment.


### Optional Core v1.4.0 candidate declarations

Core v1.4.0 also provides two independently versioned, machine-readable candidate declarations:

```bash
orbitfabric export core-interface \
  --json examples/demo-3u/generated/reports/core_interface.json

orbitfabric export scenario-declaration \
  examples/demo-3u/scenarios/payload_data_flow_evidence.yaml \
  --json examples/demo-3u/generated/reports/payload_data_flow_declaration.json
```

The Core Interface Manifest declares mission-independent supported capability contracts. The Scenario Declaration Surface describes the **authored** meaning of a validated Scenario, with exact source-byte identity and normalized atoms. Neither output represents native execution, and neither interface is a stable contract merely because Core v1.4.0 is published.

See the [Core Interface Manifest](reference/core-interface-manifest.md) and [Scenario Declaration Surface](reference/scenario-declaration-surface.md) references.

---

## 8. Generate runtime-facing contract bindings

```bash
orbitfabric gen runtime examples/demo-3u/mission/
```

Validate the generated C++17 host-build smoke target:

```bash
cmake -S examples/demo-3u/generated/runtime/cpp17 -B examples/demo-3u/generated/runtime/cpp17/build
cmake --build examples/demo-3u/generated/runtime/cpp17/build
```

The generated C++17 files expose deterministic identifiers, metadata registries, command argument structs and abstract adapter interfaces.

They do not implement command dispatch, telemetry polling, scheduling, HAL, drivers, storage, downlink or flight behavior.

---

## 9. Generate ground-facing integration artifacts

```bash
orbitfabric gen ground examples/demo-3u/mission/
```

Default omitted output path:

```text
examples/demo-3u/generated/ground/generic/
```

These artifacts expose the Mission Data Contract to ground-side review and downstream integration workflows.

They do not implement a ground segment, decoder, telemetry archive, database, operator console, command uplink service, Yamcs integration, OpenC3 integration or XTCE-compliant mission database.

---

## 10. Generate mission documentation

```bash
orbitfabric gen docs examples/demo-3u/mission/
```

Default omitted output path:

```text
examples/demo-3u/generated/docs/
```

A dedicated data-flow generator is also available:

```bash
orbitfabric gen data-flow examples/demo-3u/mission/ \
  --output-file examples/demo-3u/generated/docs/data_flow.md
```

Generated documentation describes the contract; it does not implement runtime behavior.

---

## 11. Review stability, integration and Adapter Management references

The current classification is documented through the following stable and candidate reference decisions:

```text
Stability and Compatibility Contract
Mission Model Stability Contract
Release Compatibility Policy
v1.0 Stable Surface Decision
v1.0 Demo Evidence Chain
v1.0 Compatibility and Migration Notes
Golden Output and Regression Confidence Policy
v1.2 Integration Input Stability Decision
Post-v1 Integration Surface Classification
Mission Snapshot Surface
Core Integration Input Contract
Relationship Manifest Surface
Projection Profile Contract
Integration Result Contract
Integration Package and Adapter Execution Contract
Integration Operation-Input Contract v1
Adapter Manager M0
Adapter Project Lock M1
Explicit-Source Install from Adapter Project Lock
Adapter Catalog CLI
Core Interface Manifest
Scenario Declaration Surface
Scenario Projection Accounting Contract
Evidence Set Manifest Contract
Public Adapter Onboarding
```

Projection Profile, Integration Result, Integration Package / Adapter Execution and operation-input v1 remain candidate integration-extension surfaces in Core v1.4.0.

The Adapter Manager lifecycle, Adapter Release Descriptor, Adapter Project Lock, source-neutral release attachment and Adapter Catalog surfaces also remain candidate in Core v1.4.0. The Core Interface Manifest, Scenario Declaration, Scenario Projection Accounting and Evidence Set Manifest are also candidate.

Provider-specific Release Sources remain outside Core.

---

## 12. What this demo proves

The built-in demo proves that OrbitFabric Core can:

- load and structurally validate a multi-file YAML Mission Model;
- run semantic lint rules;
- execute deterministic host-side scenario evidence;
- record contract-level data-flow evidence;
- export stable Core-owned structured surfaces;
- export a stable coherent Core Integration Input Set;
- emit additive stable-compatible FDIR relationship families;
- produce candidate downstream inspection surfaces;
- generate runtime-facing contract bindings;
- validate generated C++17 bindings with a host-build smoke target;
- generate ground-facing contract artifacts;
- protect selected stable surface fields with golden signatures.

The wider project additionally reference-proves the Core input boundary through external Integration Packages and independent OrbitFabric Studio consumption.

Core v1.4.0 public adapter onboarding is a different workflow involving the external GitHub Release Source, exact Catalog selection and Core-managed installed state. Publication metadata for those products must not be confused with clean-environment installation acceptance. No adapter download, install or native target execution is inferred from `demo-3u`.

---

## 13. What this demo does not prove

The built-in demo does not itself prove:

- flight readiness or real-time behavior;
- hardware integration;
- real onboard storage/downlink execution;
- real contact scheduling;
- orbit propagation or RF link budget simulation;
- CCSDS/PUS/CFDP compliance;
- compatibility with any particular downstream framework solely from the Core demo;
- XTCE compliance;
- binary decoder/encoder behavior;
- command uplink, telemetry archive, database or operator-console behavior;
- HAL or RTOS integration;
- relationship/dependency graph behavior;
- Core in-process third-party adapter discovery/loading/execution;
- provider-neutral provider dispatch, version-range solving or automatic adapter upgrades;
- qualification for operational spacecraft use.

Downstream-specific integration evidence lives in the corresponding external adapter repositories. Provider-specific acquisition evidence lives in the corresponding Release Source products.
