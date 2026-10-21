# Asimov v1 assurance record

This tree holds the engineering assurance work products for the Asimov v1 fork: machinery risk assessment
(ISO 12100), robot and personal-care-robot safety requirements (ISO 10218-1/-2, ISO/TS 15066, ISO 13482),
safety-related control (ISO 13849-1/-2, with IEC 62061 and IEC 61508 where 13849 runs out), electrical and battery
safety (IEC 60204-1, IEC 62133-2), cybersecurity (IEC 62443-4-1/-4-2), machine learning in safety functions
(ISO/IEC TR 5469) and the regulatory file for Regulation (EU) 2023/1230. Safety-case structure follows UL 4600
principles. The robot's own sources (mechanical, electrical, simulation) sit beside this tree in the same repository.

> [!WARNING]
> Everything here is a **draft prepared for engineering review**. None of it has passed verification review,
> confirmation review or a functional safety assessment. A document existing here does not mean the activity behind
> it is complete. Read the `Status` field of each work product and the register in
> [`01-management/WP-M-00-work-product-register.md`](01-management/WP-M-00-work-product-register.md).

## Living Safety Case

<p align="center">
  <img src="../docs/assets/assurance/dashboard.svg" width="100%" alt="Living Safety Case dashboard generated from the assurance records: assurance state, baseline, claims with accepted evidence, evidence items accepted, open defeaters, records digest.">
</p>
<p align="center">
  <img src="../docs/assets/assurance/lifecycle.svg" width="100%" alt="Status of the six lifecycle areas, derived from the evidence records.">
</p>

The records (claims, arguments, evidence, defeaters, actions, configurations, baselines, reviews) live in
[`case/`](case/README.md); [`case/tools/validate.py`](case/tools/validate.py) checks them and
[`case/tools/generate_dashboard.py`](case/tools/generate_dashboard.py) draws the figures above and fills the table
below. CI fails if any of them is stale. The document form of the same argument is
[WP-K-01](10-safety-case/WP-K-01-safety-case.md); check X3 keeps its tables equal to the records.

<details>
<summary><b>Recorded values as text</b></summary>

<!-- BEGIN GENERATED: assurance-summary (assurance/case/tools/generate_dashboard.py) -->

| Indicator | Recorded value |
|---|---|
| Assurance state | Development |
| Engineering baseline | `BL-001` at `3d4ec9d` (under development) |
| Registered safety claims | 29 |
| Claims with accepted supporting evidence | 0 |
| Registered evidence items | 22 (0 available, 15 drafted, 7 not yet performed) |
| Evidence requiring review | 15 |
| Open assurance actions | 10 |
| Open defeaters (known counter-evidence) | 34 |
| Evaluated configurations | 1 |
| Assurance-supported configurations | 0 |
| Records digest | `d9cd5af97b39` |

| Lifecycle area | Status | Evidence (drafted / missing / accepted) |
|---|---|---|
| Safety Management | In Progress | 2 (2 / 0 / 0) |
| Hazard Analysis | In Progress | 4 (4 / 0 / 0) |
| Safety Concepts | In Progress | 2 (1 / 1 / 0) |
| Technical Implementation | In Progress | 5 (4 / 1 / 0) |
| Verification and Validation | In Progress | 7 (2 / 5 / 0) |
| Safety Case and Review | In Progress | 2 (2 / 0 / 0) |

<!-- END GENERATED: assurance-summary -->

</details>

**What the dashboard guarantees:** a claim counts as accepted only when a recorded review accepts it, every piece
of evidence it cites is available and accepted, and no defeater against it is open. A passing CI run never accepts
a claim on its own, and no figure here is a safety claim.

## Start here

| Document | Why read it |
|---|---|
| [00-assessment/gap-assessment.md](00-assessment/gap-assessment.md) | Baseline review of the inherited Asimov v1 repository and the concept-phase package: GAP-01…GAP-34 |
| [01-management/WP-M-01-assurance-strategy.md](01-management/WP-M-01-assurance-strategy.md) | The assurance path: what is claimed, the three-layer architecture argument, how each standard is used, tailoring, phases and gates |
| [01-management/WP-M-00-work-product-register.md](01-management/WP-M-00-work-product-register.md) | Every required work product, its clauses, gate and status |
| [01-management/WP-M-02-safety-plan.md](01-management/WP-M-02-safety-plan.md) | Roles, activities per phase, the early-implementation rule for the gantry, the wired E-stop and the bench supply, gate reviews |
| [01-management/WP-M-06-confirmation-measures-plan.md](01-management/WP-M-06-confirmation-measures-plan.md) | Which work products get an independent review, at what independence, at which gate |
| [process/README.md](process/README.md) | The integrated process model: swimlane maps per phase, cross-domain interfaces, gate readiness |
| [06-validation/WP-V-07-test-operations.md](06-validation/WP-V-07-test-operations.md) | The hold point: what must be true before the robot is powered with its feet on the floor under the fork's control |
| [01-management/decisions/README.md](01-management/decisions/README.md) | Questions that wait on the project lead |

## Layout

![The seven phases P0 to P6, each closed by its gate G0 to G6; today is P0 and no gate is passed; hold points at G1 and G4.](../docs/assets/asimov/lifecycle.svg)

*Generated by [`make_assets.py`](../docs/assets/asimov/make_assets.py); CI fails if stale. A gate counts as passed only when its record in [`10-safety-case/gates/`](10-safety-case/gates/README.md) says Pass.*

| Folder | Content | Primary standard clauses |
|---|---|---|
| [`00-assessment/`](00-assessment/README.md) | Baseline gap assessment of the inherited repository and the concept-phase package it was seeded from | n/a |
| [`01-management/`](01-management/README.md) | Assurance strategy, safety plan, confirmation measures, regulatory strategy, upstream management, the decision register | ISO 13849-1 §4, IEC 62061 §5, IEC 61508-1 §6 and §8, Machinery Reg. Art. 25 |
| [`02-concept/`](02-concept/README.md) | Item definition and limits, operating envelopes, risk assessment, safety functions and their required PL, risk reduction concept, interaction, contact and misuse, cybersecurity and ML concepts, insufficiency analysis of the locomotion policy | ISO 12100 §5–§6, ISO 10218, ISO/TS 15066, ISO 13482 §5–§6, ISO 13849-1 §5 and Annex A, IEC 62443-4-1 SR, TR 5469 |
| [`03-system/`](03-system/README.md) | Safety requirements specification, SRP/CS architecture, response-time, fall-arrest and stopping budget, safety-chain I/O, installation and tether requirements, cybersecurity architecture, system verification | ISO 13849-1 §5–§6 and §8, IEC 60204-1 §9, ISO 13482 §6 |
| [`04-hardware/`](04-hardware/README.md) | Safety-chain hardware, electrical and battery safety, failure analysis, MTTFD, DCavg, CCF and PL calculation, component qualification, structural and stability analysis | ISO 13849-1 §6 and Annexes C–F, ISO 13849-2, IEC 60204-1, IEC 62133-2 |
| [`05-software/`](05-software/README.md) | Firmware safety layer and control software: requirements, architecture, safety analysis, units, verification, safety parameters, ML engineering of the locomotion policy, cybersecurity implementation | ISO 13849-1 §7, IEC 61508-3, IEC 62443-4-1 SI and SVV |
| [`06-validation/`](06-validation/README.md) | Validation plan and records: stability, fall and controlled descent, human detection and contact force, E-stop, fault injection, cybersecurity validation, test operations, supervised trials | ISO 13849-1 §10, ISO 13849-2, ISO 13482 §7, ISO/TS 15066 |
| [`07-supporting/`](07-supporting/README.md) | Configuration, change and problem management, documentation, review, traceability, tool and component qualification, release | IEC 61508-1 §6–§7, ISO 13849-1 §12, Machinery Reg. Annex IV |
| [`08-analyses/`](08-analyses/README.md) | System FMEA, FTA, common cause failure, STPA, independence of the safety chain from the policy and the tele-operation stack | ISO 13849-1 §6 and Annex F, IEC 60812, IEC 61025 |
| [`09-production-operation/`](09-production-operation/README.md) | Kit assembly and commissioning, operation, information for use, field monitoring, incident response | ISO 12100 §6.4, ISO 13482 §6.7, Machinery Reg. Art. 10 |
| [`10-safety-case/`](10-safety-case/README.md) | Safety case, technical documentation index, cybersecurity case, assessment reports, release record and declaration draft; gate and confirmation records | UL 4600, IEC 61508-1 §8, Machinery Reg. Annexes IV–V |
| [`process/`](process/README.md) | Integrated process model: activities, lanes, cross-domain interfaces and gates as data; generated maps and gate skeletons | ISO 13849-1 §4, IEC 61508-1 §6, MAN.3 |
| [`trace/`](trace/README.md) | Machine-readable hazards, safety functions and assumptions of use (`items/`), later requirements and trace matrices | ISO 13849-1 §5 |
| [`case/`](case/README.md) | Living Safety Case records (claims, evidence, defeaters, actions, configurations, baselines, reviews), validator and dashboard generator | UL 4600 |
| [`tools/`](tools/) | Folder index generator, link and table checkers | WP-P-04 |

## Conventions

### Identifiers

| Prefix | Meaning | Example |
|---|---|---|
| `WP-<area>-<nn>` | Work product; areas M, C, S, H, W, V, P, A, O, K, T as in the register | `WP-C-04` (safety functions and PLr) |
| `H-<nn>` | Hazard from the ISO 12100 risk assessment; the concept package's `HZ-nn` is kept as its `package_id` | `H-01` (fall of the robot) |
| `SF-<nn>` | Safety function, with its required Performance Level `PLr`; numbering follows the concept package | `SF-02` (fall arrest by controlled descent, PLr d) |
| `SR-<nn>` | Safety requirement of the SRP/CS (WP-S-02) | `SR-012` |
| `HWSR-<nn>` / `SWSR-<nn>` | Hardware / software safety requirement | `SWSR-031` |
| `CSR-<nn>` / `TS-<nn>` | Cybersecurity requirement / threat scenario | `CSR-04` |
| `AIR-<nn>` | Requirement on a learned component | `AIR-02` |
| `FI-<nn>` / `TC-<nn>` | Functional insufficiency / triggering condition (WP-C-10) | `TC-05` |
| `PAR-<nn>` | Safety-related parameter (WP-W-09) | `PAR-07` |
| `AOU-<nn>` | Assumption of use (on the environment, the operator, the site) | `AOU-05` |
| `VS-<area>-<nn>` | Verification specification (test case) | `VS-UV-03` |
| `DF-<nn>` | Defeater: known counter-evidence against a claim | `DF-12` |
| `GAP-<nn>` | Finding of the baseline gap assessment; never reused | `GAP-17` |
| `OI-<nn>` | Open item to resolve before the next gate (per document) | `OI-3` |
| `IX-<nn>` / `FB-<nn>` | Cross-domain interface / feedback route in the process model | `IX-02` |
| `DQ-<nnn>` | Decision question for the project lead | `DQ-005` |
| `G0`…`G6` | Lifecycle gates | `G1` |

Requirement IDs never get reused. A withdrawn requirement keeps its ID and is marked `Withdrawn`.

### Document control header

Every work product starts with this block:

```
| Field | Value |
|---|---|
| Work product | WP-x-nn <name> |
| Standard reference | <clause list> |
| Version | 0.1 |
| Status | Skeleton / Draft / In review / Approved / Baselined |
| PL / scope | <highest PLr addressed, or process / cybersecurity / ML> |
| Author | <name> |
| Reviewer(s) | <name, independence level I0–I3> |
| Approver | <name> |
| Baseline | <git commit or tag the content refers to> |
```

### Status meanings

| Status | Meaning |
|---|---|
| Skeleton | Structure and clause mapping exist; content still to be written |
| Draft | Content written, derived from code review and engineering judgement; not yet verified |
| In review | Verification review open (pull request) |
| Approved | Verification review passed and approved by the approver named in the safety plan |
| Baselined | Approved and frozen in a tagged configuration baseline |

### Changing a work product

Work products change through pull requests in the same way code does (see
[WP-P-02 change management](07-supporting/WP-P-02-change-management.md)). If a pull request touches a safety-relevant
path (see [`07-supporting/safety-relevant-paths.txt`](07-supporting/safety-relevant-paths.txt), owned by
[WP-P-01](07-supporting/WP-P-01-configuration-management-plan.md)), it updates the affected work products or records an
impact analysis that says why none are affected.

Some files are generated from others and checked in CI. If you edit a source, run the generator and commit its
output:

| Generator (run this) | Its outputs | Sources it reads |
|---|---|---|
| `python3 assurance/tools/folder_index.py` | `assurance/<folder>/README.md` for the numbered folders | WP-M-00 §3 |
| `python3 assurance/process/tools/process_model.py` | `process/maps/*.md`, `10-safety-case/gates/skeletons/*.md` | `process/model/*.yaml`, WP-M-00 §2–§3, WP-M-02 §3.1, WP-M-06 §9, the confirmation records |
| `python3 assurance/01-management/decisions/fig_lifecycle.py` | `decisions/figures/fig-dr-1-lifecycle.svg` | The lifecycle table of the decisions README |
| `python3 docs/assets/asimov/make_assets.py` | The README figures | The data at the top of the generator |

### Reference configuration

The assessed configuration is **CFG-001, the kit robot as the fork evaluates it**: the 1.2 m, 35 kg, 25-DOF biped
built from the published CAD and the motion control board, hanging from or standing under a gantry on a rated tether,
fed from a bench supply with no battery, tele-operated, with the bench equipment the fork adds before any powered
test ([WP-V-07](06-validation/WP-V-07-test-operations.md)). **CFG-002, the battery and policy robot** as upstream
intends it (user-supplied battery with a BMS, the learned locomotion policy, the wireless E-stop) is
upstream-compatible and unverified: its firmware, API and policy are not in any public repository, so its decisions
are tracked, not assessed ([WP-C-01 §1](02-concept/WP-C-01-item-definition.md#1-item-identification)).

### Standards text

The standards are copyrighted and are not reproduced here. Clause references point to the editions named in
[WP-M-01 §4](01-management/WP-M-01-assurance-strategy.md#4-the-standards-and-how-each-one-is-used) and must be
checked against a licensed copy before an audit ([WP-M-06](01-management/WP-M-06-confirmation-measures-plan.md) OI-1).
