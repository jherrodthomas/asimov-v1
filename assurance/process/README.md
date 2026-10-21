# WP-P-11 Integrated Process Model and Process Maps

| Field | Value |
|---|---|
| Work product | WP-P-11 Integrated process model and generated process maps (all phases G0–G6 modelled) |
| Standard reference | ISO 12100:2010 §4 (strategy: the iterative risk assessment and reduction process); ISO 13482:2014 §4 (the risk assessment and reduction process for personal care robots, informative here); ISO 13849-1:2023 §4 (planning and the design process of the SRP/CS); IEC 61508-1:2010 §6 and §7 (management and overall safety lifecycle); IEC 62443-4-1:2018 SM-1 (secure development process); ISO/IEC TR 5469:2024 (AI lifecycle, informative); ASPICE 4.0 MAN.3 (project lifecycle definition) |
| Version | 0.1 (all phases G0 governance to G6 operation modelled for the humanoid; 2026-10-21) |
| Status | Draft |
| PL / scope | Process (all disciplines) |
| Author | Assurance team (initial draft) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `3d4ec9d` (BL-001) |

## 1. Purpose

The plans ([WP-M-02](../01-management/WP-M-02-safety-plan.md), [WP-M-08](../01-management/WP-M-08-cybersecurity-plan.md),
[WP-M-09](../01-management/WP-M-09-ml-safety-plan.md), [WP-M-13](../01-management/WP-M-13-regulatory-conformity-strategy.md))
say *what* each discipline produces. The [register (WP-M-00)](../01-management/WP-M-00-work-product-register.md) says
*which gate* needs each work product. Neither says how the disciplines' work fits together inside a phase: which
analysis waits for which, and where two disciplines must agree.

This folder records that as one integrated lifecycle. The
principle is one lifecycle, not parallel lifecycles per standard:

- each phase is a set of **activities** in discipline **lanes** (machinery and robot risk assessment, safety-related control
  system, electrical and mechanical, software, cybersecurity, machine learning, and joint work);
- activities are linked by the **work products** they consume and produce;
- explicit **cross-domain interfaces** mark where one discipline's result depends on another's;
- one **gate** collects the work and the **confirmation measures**.

The model is data, so a checker keeps it consistent with the documents and a generator draws the maps and the gate
review skeletons from it.

| Map | Content |
|---|---|
| [maps/lifecycle.md](maps/lifecycle.md) | L0: the seven phases G0…G6, the feedback from operation into earlier phases, their exit criteria |
| [maps/g0-governance.md](maps/g0-governance.md) | L1 for the governance phase: the plans and procedures the later phases read from, G0 readiness including role records that disagree |
| [maps/g1-concept.md](maps/g1-concept.md) | L1 for the concept phase: swimlane map, interface map, activity table with clauses, clause coverage per standard, G1 readiness |
| [maps/g2-system-design.md](maps/g2-system-design.md) | L1 for the system design phase, same sections, G2 readiness |
| [maps/g3-hw-sw-development.md](maps/g3-hw-sw-development.md) | L1 for the hardware and software development phase, same sections, G3 readiness |
| [maps/g4-integration-and-verification.md](maps/g4-integration-and-verification.md) | L1 for the integration and verification phase, same sections, G4 readiness |
| [maps/g5-validation-and-release.md](maps/g5-validation-and-release.md) | L1 for the validation and release phase, same sections, G5 readiness |
| [maps/g6-operation.md](maps/g6-operation.md) | L1 for the operation phase, same sections plus the feedback routes into earlier phases, G6 readiness |
| [`10-safety-case/gates/skeletons/`](../10-safety-case/gates/skeletons/) | One pre-filled gate review skeleton per gate, following the gate record template ([gates README](../10-safety-case/gates/README.md)) |

The same model is drawn as figures by [`tools/process_figures.py`](tools/process_figures.py) into
[`docs/assets/asimov/process/`](../../docs/assets/asimov/process/): a lifecycle grid (lanes by phases), one
vertical swimlane per phase with the activities in dependency order, and the cross-domain interfaces as a list.
They are checked by CI like the maps, and the wiki's [Process maps](../../wiki/Process-maps.md) page embeds them.

L2 (how to perform an activity) remains the procedures and plans the activities point to; it is not modelled here.
The wiki's [Processes](../../wiki/Processes.md) and [Process maps](../../wiki/Process-maps.md) pages are the
plain-language version.

## 2. Single source of truth

The model holds only what no other document holds: the activities, their lanes, their inputs and the interfaces.
Everything else is read at generation time:

| Fact | Read from |
|---|---|
| Gate names and exit criteria | WP-M-00 §2 |
| Clause references, ASPICE process, gate and status of each work product | WP-M-00 §3 (the row of each produced work product) |
| Who holds each lane's role, and by which gate | WP-M-02 §3.1 |
| Which confirmation measures a gate needs | WP-M-06 §9 |
| Whether a confirmation measure has been performed | A record in `10-safety-case/confirmation/` named as its README requires: `CR-<nn>-<WP-ID>-v<version>.md` for a confirmation review, `<measure>.md` otherwise. A measure whose record is itself a work product (FSA-F → WP-K-04, CS-A1 → WP-K-05) counts as performed once that work product is approved |

A change to the register, the safety plan or the confirmation plan therefore shows up in the maps on the next
run, and `--check` fails in CI until the maps are regenerated.

## 3. Record format

Records use a flat YAML subset: a top-level list of mappings with scalar or flow-list values. Flow-list items
cannot contain commas. One record per item, with a `kind`:

| Kind | File | Fields |
|---|---|---|
| `phase` | [`model/lifecycle.yaml`](model/lifecycle.yaml) | `id` (gate G0…G6), `modelled` |
| `lane` | `model/lifecycle.yaml` | `id`, `name`, `role` (a role in WP-M-02 §3.1), `plan` (the plan that governs the lane) |
| `activity` | [`model/governance.yaml`](model/governance.yaml), [`model/concept.yaml`](model/concept.yaml), [`model/design.yaml`](model/design.yaml), [`model/development.yaml`](model/development.yaml), [`model/integration.yaml`](model/integration.yaml), [`model/release.yaml`](model/release.yaml), [`model/operation.yaml`](model/operation.yaml) | `id` (`GOV-nn` governance, `CON-nn` concept, `DES-nn` system design, `DEV-nn` HW/SW development, `INT-nn` integration and verification, `REL-nn` validation and release, `OPS-nn` operation), `phase`, `lane`, `name`, `produces`, `inputs`; optional `updates` |
| `review` | same files as the phase's activities | `id` (the WP-M-06 measure; `<measure>@<gate>` when WP-M-06 plans it at several gates, e.g. `CR-06@G2`), `phase`, `name`, `covers`, `independence`; optional `record_wp` when the measure's record is itself a work product, which then counts as performed once approved |
| `interface` | [`model/interfaces.yaml`](model/interfaces.yaml) | `id` (`IX-nn`), `phase`, `between` (two work products), `pattern`, `topic`, `anchors`, `status`, `open_item`, `due` |
| `feedback` | `model/operation.yaml` | `id` (`FB-nn`), `phase`, `source` (the work product that raises the finding), `targets` (work products of earlier phases it re-opens), `finding`, `anchors` |

Rules the records follow:

- **Living work products are produced once and updated later.** A work product whose WP-M-00 gate is a range
  (`G1→G5`) is produced by one activity in its first phase. Activities of later phases in the range list it under
  `updates`. Inputs and map edges in a phase use the latest activity of that phase that produces or updates it.
- **Independent assessments are activities in the confirmation lane** when they produce a work product of their
  own (the FSA report WP-K-04, the cybersecurity assessment WP-K-05). Readiness counts such an activity as checking
  its inputs.
- **Activity IDs follow execution order.** An activity's inputs from the same phase come from activities with lower
  IDs. Work that goes back and forth between disciplines is an interface, not an input, so the input graph has no
  cycles.
- **Interfaces are anchored.** Each anchor `WP-x-nn:text` names text that occurs verbatim in that work product. If
  the documents stop making the link, the check fails.
- **Interface status** is `documented` (both documents refer to each other; nobody has reviewed the agreement yet)
  or `open` (a recorded open item still has to settle it, named in `open_item`). There is no "agreed" status yet; it
  will come from a recorded review once the Living Safety Case records are ported.

## 4. Checks

`python3 assurance/process/tools/process_model.py --check` runs these checks. CI runs it in the `assurance` workflow.

| Check | Rule |
|---|---|
| P1 | Records parse; required fields present; list fields are lists; IDs unique |
| P2 | Every gate G0…G6 has a phase record and a WP-M-00 §2 entry; every lane's role exists in WP-M-02 §3.1 and its plan in WP-M-00 |
| P3 | Each activity's phase and lane exist; each produced work product is registered, has exactly one producing activity, is gated in the activity's phase and exists on disk; an updated work product is living and the phase lies within its gate range |
| P4 | In a modelled phase, every work product WP-M-00 gates there is produced by an activity |
| P5 | Each input is produced by an earlier activity of the same phase or gated at an earlier gate |
| P6 | The phase's confirmation measures equal the WP-M-06 §9 row for its gate, are defined in WP-M-06, and cover registered work products |
| P7 | Interfaces connect two work products produced by activities; anchors occur verbatim; `open_item` is set exactly when the status is `open`; an interface is not due before its own phase |
| P8 | The committed maps and gate skeletons equal what the model generates (`--check` only) |
| P9 | Feedback comes from a work product produced in its own phase, goes only to work products of earlier phases, and its anchors occur verbatim |

`tools/test_process_model.py` shows that the committed model passes and that each check rejects a broken copy.

## 5. Changing the model

1. Edit the records in `model/`. Do not edit `maps/` or the gate skeletons.
2. Run `python3 assurance/process/tools/process_model.py` to check the model and regenerate the maps.
3. Commit the records, the maps and the skeletons together.

A new or renamed work product goes into WP-M-00 first; the model then refers to it.

## 6. What the model shows

These findings come from the generated maps at BL-001, where every work product but twelve is a skeleton and
the concept-phase package is the only analysis. They are observations for the safety manager, not decisions.

### 6.0 Governance phase ([G0 map](maps/g0-governance.md))

1. **"Roles assigned" is part of the G0 exit criterion, and it is not met.** WP-M-02 lists the verification
   reviewer, QA and the external functional safety assessor as TBD. Every later gate inherits these gaps.
2. **One person holds almost every role.** Safety manager, maintainer, configuration manager, cybersecurity
   manager, ML safety lead, SRP/CS engineer and software engineer. The electrical and mechanical engineer is TBD and
   needed by G2; the test bench owner, who builds the gantry, is TBD and needed before the first hang test. Independent
   checking rests entirely on the two G0 confirmation measures and the assessor, who is not engaged (DQ-010).
3. **Two decisions shape everything below G0 and are open:** the regulatory frame (DQ-001) and the first item's
   operating envelope (DQ-002). The regulatory strategy (WP-M-13) carries both as its assumptions until answered.
4. **The process model is itself a G0 work product.** GOV-21 produces WP-P-11 from the register, the safety plan
   and the confirmation plan, so this model can only be as current as those three documents.
5. **The governance phase begins with an impact analysis of a package, not a product.** GOV-01 reconciles the
   concept-phase package (five workbooks, three documents) with the fork's record; the package's 28 gaps become the
   defeaters of the safety case before any design work.

### 6.1 Concept phase ([G1 map](maps/g1-concept.md))

1. **Two interfaces block G1: IX-02 and IX-03.** The safe state of a biped (DQ-005) decides what the fall-arrest
   function SF-02 and the stop functions deliver; the allocation of balance SF-01 (DQ-006) decides whether the
   learned policy is inside or outside the safety-related control system. Everything that follows (the fall-arrest
   budget, the independence argument, the ML plan) depends on these two answers.
2. **The risk lane carries most of the phase.** Five of the twelve activities (CON-02, CON-03, CON-04, CON-06,
   CON-07) sit in the risk assessment lane, all held by the safety manager.
3. **The test operations hold point (CON-11) is a G1 work product,** but its conditions (gantry, wired E-stop,
   bench supply: DQ-007, DQ-008, DQ-009) are needed before the first hang test, which the concept itself depends on
   (mass, centre of gravity, fall energy: GAP-03). Expect the first powered test inside P1, under the at-risk rule
   of WP-M-02 §4.1.
4. **Four G1 work products have no confirmation measure at G1:** WP-C-02, WP-V-07, WP-T-01, WP-K-01. They are
   reviewed only through verification review (WP-P-05), and the verification reviewer role is unassigned.

### 6.2 System design phase ([G2 map](maps/g2-system-design.md))

1. **The critical path is one serial chain in one lane.** SRS, fall-arrest budget, stop-chain architecture, I/O,
   FMEA, FTA, CCF, independence (DES-03 → DES-04 → DES-05 → DES-06 → DES-09 → DES-10 / DES-11 → DES-13) run one
   after another in the SRP/CS lane, held today by the maintainer.
2. **The mechanical lane comes first and has no owner.** The structural and stability analysis (DES-02) bounds the
   fall energy that the fall-arrest budget needs (IX-06) and needs the electrical and mechanical engineer, TBD and
   needed by G2. The package's DFMEA already names the hip-yoke fillet and the 7075 substitution (GAP-04).
3. **Safety and security meet once in the architecture** (IX-05): the stop chain must be a zone without a conduit
   from the tele-operation network, and the safety parameters of WP-W-09 are protected assets (IX-07). That is one
   design decision seen from two standards, so WP-S-03 and WP-S-07 cannot be reviewed apart.
4. **The independence activity (DES-13) is where the policy question lands.** If DQ-006 keeps SF-01 on the learned
   policy, DES-13 has to show how the deterministic layer bounds it; if not, DES-13 shows the policy is outside the
   chain and the tether carries the fall.

### 6.3 Hardware and software development phase ([G3 map](maps/g3-hw-sw-development.md))

1. **The PL calculation waits on three lanes.** DEV-08 needs the fault lists (SRP/CS), the component data (hardware
   and supplier management: upstream publishes no actuator or board reliability figures, GAP-14) and the CCF score
   (from G2). Obtaining or substituting certified components is the long-lead item.
2. **Firmware development starts from no code.** DEV-01 (environment and a reproducible build) precedes every
   software activity; no firmware or motion-control software exists in any public repository (GAP-16), so the
   safety layer is written, not hardened.
3. **Thirteen of the twenty G3 work products get only verification review at G3** (counting the two living
   updates): the hardware requirements and design, electrical safety, the software environment, requirements,
   architecture, units, unit verification, parameters, cybersecurity implementation, and proven in use (deliberate,
   T-06). WP-M-06 plans no confirmation measure for them.

### 6.4 Integration and verification phase ([G4 map](maps/g4-integration-and-verification.md))

1. **The phase cannot start: there is no bench.** INT-03 and INT-04 need the actuator bench and the
   hardware-in-the-loop rig of WP-W-08 (built around the MuJoCo model, which is itself unpinned to any hardware
   revision, GAP-21); its owner is TBD and needed by G3.
2. **Every powered test in this phase runs under WP-V-07.** INT-05, INT-06 and INT-07 list it as an input; the hold
   point conditions must already be met, including the gantry sized for a dynamic fall load.
3. **G4 has no independent check of its results.** The only measure WP-M-06 plans at G4 is the process audit AUD-2.
   None of the test reports gets a confirmation measure before the final assessment at G5.

### 6.5 Validation and release phase ([G5 map](maps/g5-validation-and-release.md))

1. **Release depends on parties nobody has engaged.** The final functional safety assessment (REL-12, WP-K-04),
   the cybersecurity assessment (REL-13, WP-K-05), the penetration tester (REL-06) and, if DQ-001 selects a frame
   or DQ-006 a position that needs one, a notified body (NB-1).
2. **The three arguments meet once,** in REL-11 where the safety case is completed with the cybersecurity case
   (IX-10) and the technical documentation; the assessment and the release record then depend on that single step.
3. **The operation documents get no confirmation measure:** WP-O-01, WP-O-02, WP-O-03 and WP-P-10 are reviewed
   only by verification review, although information for use carries the residual risks of WP-C-05 and the manual's
   own safety page is unpublished (GAP-02).

### 6.6 Operation phase ([G6 map](maps/g6-operation.md))

1. **Field monitoring is needed five gates before it is gated.** WP-O-04 is gated at G6, but WP-V-07 already
   routes test anomalies, falls and unplanned tether loads through the same path from the first hang test. Either
   the register entry or the hold point needs a monitoring slice gated at G1.
2. **Every field finding re-opens a G1 work product.** All six feedback routes end in the concept phase: the risk
   assessment, the operating envelopes, the insufficiency analysis, the misuse analysis, the ML definition or the
   safety case. A confirmed work product that changes in a safety-relevant way triggers its confirmation review again.
3. **Operation has no independent check.** WP-M-06 plans no confirmation measure at G6.

## 7. Open items

| ID | Item | Owner | Gate |
|---|---|---|---|
| OI-1 | Add an "agreed" interface status set only through a recorded review once the first I2 review of the safety case is held | Safety manager | G2 |
| OI-2 | Derive pull-request checklists from the model: which activities and interfaces a change to a work product re-opens | Configuration and change manager | G2 |
| OI-3 | Decide whether field monitoring gets a G1 slice (finding 6.6.1) | Safety manager | G1 |
