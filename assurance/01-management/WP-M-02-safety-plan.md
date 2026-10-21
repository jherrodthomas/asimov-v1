# WP-M-02 Functional Safety Plan

| Field | Value |
|---|---|
| Work product | WP-M-02 Functional safety plan |
| Standard reference | ISO 13849-1:2023 §4 (planning of the SRP/CS, roles, documentation); IEC 62061:2021 §5 (management of functional safety: planning, competence, configuration management, modification); IEC 61508-1:2010 §6 (management of functional safety); ISO 12100:2010 §4 (strategy); ISO 10218-1:2011 §5.4 (safety-related control system performance); ASPICE 4.0 MAN.3 |
| Version | 0.5 (2026-10-21): DQ-055 A and DQ-062 B applied to §3.1 and §9. 0.4 (2026-10-21): DQ-029 A (public call for a reviewer) and DQ-030 A (G1 after the first hang test) applied to §3.1 and §10. 0.3 (2026-10-21): DQ-011 A (self-approval recorded at I0) and DQ-023 A (the fork writes a minimal firmware) applied. 0.2 (2026-10-21): DQ-004 A and DQ-010 A applied; DQ-011 opened. 0.1 (initial plan; 2026-10-21) |
| Status | Draft |
| PL / scope | All. Planned to PL d until the risk assessment ([WP-C-03](../02-concept/WP-C-03-risk-assessment.md)) and the safety function specification ([WP-C-04](../02-concept/WP-C-04-safety-functions-and-plr.md)) are approved; the target is PL d (DQ-004 A, decided 2026-10-21) |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1); confirmation review TBD (external assessor, I3 planned, see [WP-M-06](WP-M-06-confirmation-measures-plan.md)) |
| Approver | Safety manager |
| Baseline | `3d4ec9d` (BL-001) |

## 1. Purpose and scope

This plan sets out how functional safety is managed for the Asimov v1 reference configuration defined in
[WP-M-01 §3.1](WP-M-01-assurance-strategy.md#31-reference-configuration-the-only-scope-claims-apply-to): the DIY-kit
robot as published, suspended from a gantry by a tether, powered from a bench supply, tele-operated in a supervised
laboratory (operating envelope OE-1 of [WP-C-02](../02-concept/WP-C-02-operating-environment-and-tasks.md)).

It implements the [assurance strategy (WP-M-01)](WP-M-01-assurance-strategy.md) for the machinery and robot safety
standards (ISO 12100, ISO 10218-1/-2 and ISO/TS 15066, ISO 13482 as the hazard catalogue, ISO 13849-1/-2, IEC 60204-1,
ISO 13850, IEC 62133-2) and, where those run out, IEC 62061 and IEC 61508. It does not repeat the strategy. The
companion plans cover the other disciplines:

| Discipline | Plan |
|---|---|
| Cybersecurity (IEC 62443) | [WP-M-08](WP-M-08-cybersecurity-plan.md) |
| Machine learning (ISO/IEC TR 5469): the locomotion policy | [WP-M-09](WP-M-09-ml-safety-plan.md) |
| Regulatory conformity (Machinery Regulation, AI Act, US frame) | [WP-M-13](WP-M-13-regulatory-conformity-strategy.md) |
| Project scope, effort, schedule | [WP-M-03](WP-M-03-project-plan.md) |

This plan is a living document. It is updated at every gate review (§10) and whenever an approved change alters
scope, required PL, roles or tailoring.

## 2. Safety objectives

| # | Objective | Measured by |
|---|---|---|
| SO-1 | Identify the hazards of the robot within its limits and operating envelopes, estimate and evaluate their risk, and derive the safety functions with their required PL | Approved risk assessment ([WP-C-03](../02-concept/WP-C-03-risk-assessment.md)) and safety function specification ([WP-C-04](../02-concept/WP-C-04-safety-functions-and-plr.md)) with I3 confirmation review |
| SO-2 | Show that each safety function with a PLr is implemented by a safety-related part of the control system that achieves it regardless of what the locomotion policy or the tele-operator commands, and that the safe state of the biped is defined and reached | Architecture, PL calculation, independence analysis and validation evidence (WP-S-03, WP-S-04, WP-H-04, WP-A-05, WP-V-01…V-05); decisions DQ-005 and DQ-006 applied |
| SO-3 | Keep the fall hazard out of every test through the tether and gantry until a fall-arrest function is verified, and never claim a free-standing robot near people before it is | [WP-V-07](../06-validation/WP-V-07-test-operations.md) conditions; claim G2.4 of the safety case |
| SO-4 | Close the high-severity gaps of the gap assessment (GAP-01…GAP-17, GAP-19) or argue their residual risk | Defeaters closed in the safety case; change requests closed |
| SO-5 | Keep every safety-relevant change under configuration and change control, with impact analysis, across the fork and the firmware, API and policy repositories once they exist | [WP-P-01](../07-supporting/WP-P-01-configuration-management-plan.md), [WP-P-02](../07-supporting/WP-P-02-change-management.md) records |
| SO-6 | Provide independent confirmation that the work and its results are adequate | Confirmation reviews, audits and assessment per [WP-M-06](WP-M-06-confirmation-measures-plan.md) |
| SO-7 | Make no claim that the evidence does not support; treat the inherited concept-phase package as seed material, never as evidence | Safety case ([WP-K-01](../10-safety-case/WP-K-01-safety-case.md)) reviewed against this plan at each gate; the package recorded as partial, unreviewed evidence |
| SO-8 | Run no powered test with the robot's feet on the floor without the gantry and tether, a wired E-stop in the operator's hand, a cleared area and an approved test procedure | [WP-V-07](../06-validation/WP-V-07-test-operations.md) hold point (§4.1) |

## 3. Roles and responsibilities

### 3.1 Role assignments

The project has one maintainer today. One person holding several roles is allowed for planning and authoring. It is
not allowed where independence is required (verification review of own work at I1 or higher, confirmation
measures, QA audits). Roles marked TBD must be filled before the gate shown.

| Role | Responsibilities | Assigned to | Needed by |
|---|---|---|---|
| Safety manager | Owns this plan; plans and coordinates safety activities; tracks progress; approves safety work products (except own-authored ones that need independent approval); maintains the safety case; initiates confirmation measures; decides on safety anomaly escalation; chairs gate reviews | Jherrod Thomas (acting) | G0 |
| Project maintainer | Overall project responsibility; resource and scope decisions; the strategic decisions of WP-M-01 §8; release decision (with the safety manager) | Jherrod Thomas | G0 |
| Configuration and change manager | CM plan, baselines of the fork and the firmware, API and policy repositories, pins, change board | Jherrod Thomas (acting) | G0 |
| Cybersecurity manager | Owns [WP-M-08](WP-M-08-cybersecurity-plan.md); threat and risk assessment of the tele-operation channel and the API; interface to safety on threats that can cause a hazard | Jherrod Thomas (acting); permanent holder TBD | G1 |
| ML safety lead | Owns [WP-M-09](WP-M-09-ml-safety-plan.md); classification of the locomotion policy; evidence for the position DQ-006 settles | Jherrod Thomas (acting); permanent holder TBD | G1 |
| Safety-related control system engineer | Stop chain and safety-layer architecture, category and diagnostics, PL calculation, fault lists, validation of the chain (WP-S-02…S-05, WP-H-01, H-03, H-04, H-07) | Jherrod Thomas (acting); additional contributors TBD | G2 |
| Electrical and mechanical engineer | E-stop and motor-rail wiring, IEC 60204-1 electrical safety, the battery and BMS interlock, structural and stability analysis, guarding (WP-H-02, H-05, H-08) | TBD (likely external) | G2 |
| Firmware and software engineer(s) | The fork's minimal firmware for the motion control board (DQ-023 A: CAN actuator control with clamps, watchdog, E-stop input, DAMP-only fallback), the safety layer, the mode machine, unit and integration verification (WP-W-*) | Jherrod Thomas; additional contributors TBD | G2 |
| Verification reviewer(s) | Verification reviews of work products and code (PR reviews) at the independence level set in [WP-P-05](../07-supporting/WP-P-05-verification-review-procedure.md) | TBD; a public call for one reviewer with machinery-safety or robotics experience is open in CONTRIBUTING.md (DQ-029 A, decided 2026-10-21) and is posted by the lead on upstream's Discord and forum (DQ-046 A; draft in WP-M-10 §5), starting with WP-C-03 and WP-C-04; that reviewer may also perform the G1 confirmation reviews at I1 as a recorded deviation (DQ-055 A) | G0 (carried to G1 as a condition of the G0 record) |
| Quality assurance | Process and work product audits per [WP-M-05](WP-M-05-quality-assurance-plan.md) | TBD (independent of the author) | G0 |
| Test bench owner | Builds and maintains the actuator bench, the hardware-in-the-loop rig with the MuJoCo model, and the gantry (WP-W-08, WP-V-07) | TBD | G3 |
| Test operator(s) | Powered tests under [WP-V-07](../06-validation/WP-V-07-test-operations.md), hand on the wired E-stop | TBD (trained per WP-M-04) | G1 (before any powered floor test) |
| External functional safety assessor | Confirmation reviews at I3, functional safety audits, functional safety assessment | None for now (DQ-010 A, decided 2026-10-21): every I2 and I3 measure unscheduled; revisit at G1 | G1 (revisit) |
| External cybersecurity assessor | Cybersecurity assessment ([WP-K-05](../10-safety-case/WP-K-05-cybersecurity-assessment.md)) | TBD | G5 (interim earlier, see WP-M-06) |
| Notified body | Only if the lead's frame and route (DQ-001, WP-M-13 §3) or Annex I Part A (DQ-006) need one | TBD | G5 |

**Interim limitation (DQ-011 A, decided 2026-10-21):** while the project has one person, the safety manager approves the work
products they author. Every such approval is self-approval at independence I0 and is recorded as that in the
Approver field of the work product's header as it is next revised; no verification review above I0 and no
confirmation measure exists until a second person or an assessor joins (DQ-010 A: not for now).

Competence requirements and evidence for each role are in [WP-M-04](WP-M-04-organization-competence-safety-culture.md).

### 3.2 RACI per activity

R = responsible, A = accountable, C = consulted, I = informed. SM = safety manager, PM = project maintainer,
CSM = cybersecurity manager, ML = ML safety lead, SRP = safety-related control system engineer, EM = electrical and
mechanical engineer, SW = firmware and software engineer, VR = verification reviewer, QA = quality assurance,
EA = external functional safety assessor.

| Activity | SM | PM | CSM | ML | SRP | EM | SW | VR | QA | EA |
|---|---|---|---|---|---|---|---|---|---|---|
| Safety plan and updates | A/R | C | C | C | C | I | I | R (review) | C | C (CR) |
| Impact analysis of the baseline and the concept-phase package (WP-M-11) | A | R | C | C | C | C | C | R | I | R (CR) |
| Robot definition, operating envelopes, risk assessment, safety functions and PLr | A/R | C | C | C | C | C | I | R | I | R (CR) |
| Risk reduction concept, contact limits, safe state of the biped | A/R | C | C | C | C | C | I | R | I | R (CR) |
| SRS, stop chain and safety-layer architecture, fall-arrest budget, PL calculation | A | I | C | C | R | C | C | R | I | R (CR) |
| Electrical and battery design, structural and stability analysis | A | C | I | I | C | R | I | R | I | R (CR) |
| System analyses (FMEA, FTA, CCF, STPA, independence) | A | I | C | C | R | C | R | R | I | R (CR) |
| Safety layer and tele-operation stack: requirements, design, code, unit verification | A | I | C | C | C | I | R | R | I | I |
| Locomotion policy: classification, engineering evidence, sim-to-real | A | I | I | R | C | I | C | R | I | I (ML-R) |
| Bench build, gantry, integration, fault injection | A | C | C | I | R | R | R | R | I | I |
| Stability, fall, contact and E-stop tests; safety validation | A | C | I | I | R | C | C | R | I | I |
| CM, change control | C | A | C | I | I | I | R | I | C | I |
| QA audits | I | A | I | I | I | I | I | I | R | I |
| Safety case, technical documentation | A/R | C | R | R | C | C | C | R | I | R (CR) |
| Functional safety audit and assessment | C | A | I | I | I | I | I | I | C | R |
| Release decision | R | A | R | C | C | I | I | I | C | C |

"CR" means the assessor performs the confirmation review. The assessor is never responsible for producing a work
product.

### 3.3 AI-assisted authoring

The concept-phase package and most work products to date were drafted with an AI coding assistant working under
the maintainer's direction. Rules:

- An AI-drafted work product or code change is the author's work. The person who commits it is the author for
  independence purposes (WP-P-05) and answers for its content.
- AI drafting is not a verification activity. An AI-produced audit or checklist run is an author-side pre-review at
  I0. It gives no review credit at I1 or above. The concept-phase package is such a pre-review: it is recorded as
  partial, unreviewed evidence (WP-K-01 Sn-06…Sn-09) and ported into work products that then go through review.
- Tool classification of the assistant belongs in [WP-P-07](../07-supporting/WP-P-07-tool-classification-qualification.md) (OI-4). Until it is closed,
  every AI-drafted change to safety-relevant code is covered by the same verification as hand-written code: CI,
  the bench campaign and human review.
- The working rules for the assistant are in [CLAUDE.md](../../CLAUDE.md): sort before asking, every question
  stands on its own, batches of ten, record decisions in the register.

## 4. Lifecycle activities per phase

Phases and gates are defined in [WP-M-01 §7](WP-M-01-assurance-strategy.md#7-phases-gates-and-sequence) and
[WP-M-00 §2](WP-M-00-work-product-register.md#2-gates). This table assigns the safety activities in each phase; the
[process model](../process/README.md) draws them as swimlane maps with the other disciplines.

| Phase | Safety activities | Responsible | Key outputs | Gate entry criteria |
|---|---|---|---|---|
| P0 Governance | Approve plans; assign roles; take configuration control of the fork (baseline BL-001, pins, CODEOWNERS, branch protection); impact analysis of the inherited baseline and the concept-phase package; decide the frame (DQ-001), the envelopes (DQ-002) and the reference configuration (DQ-003); engage an assessor or record the decision not to (DQ-010) | SM, PM | WP-M-00…M-13, WP-P-01…P-06, WP-P-11 | — |
| P1 Concept | Robot definition and limits (weigh the robot, measure the centre of gravity, GAP-03); operating envelopes; risk assessment on the ISO 12100 Annex B and ISO 13482 Annex A catalogues, rated per envelope; safety functions SF-01…SF-25 with PLr, stop category and response time (DQ-004, DQ-005, DQ-006); risk reduction concept with the tether and gantry as the OE-1 complementary measure (DQ-007); interaction, contact limits and misuse; insufficiency analysis of perception and the policy; test operations hold point; initial safety case argument and hazard log | SM (risk assessment, safety functions), SRP (PLr), ML (policy), CSM | WP-C-01…C-10, WP-V-07, WP-K-01 v1, WP-T-01 | G0 passed |
| P2 System design | SRS for the SRP/CS, ported from the concept-package requirements and reworked; stop chain and safety-layer architecture with designated architecture, category, DC and channels (DQ-008); fall-arrest and response-time budget; I/O map; requirements for installation and operation; cybersecurity architecture; structural and stability analysis; system FMEA (from the DFMEA), FTA, CCF, STPA, independence of the chain | SRP, EM, SM | WP-S-01…S-07, WP-H-08, WP-A-01…A-05 | G1 passed incl. confirmation review of the risk assessment |
| P3 HW/SW development | E-stop and motor-rail hardware, power distribution and battery interlock (DQ-009), electrical and battery safety; hardware failure analysis and fault lists; MTTFD, DCavg, CCF and PL calculation (needs upstream's actuator data, GAP-14); qualification of safety components; software environment, requirements, architecture, safety analysis, unit design and verification of the safety layer (which does not exist at BL-001, GAP-16); safety parameters (DQ-014); ML engineering evidence for the policy; tool and component qualification | SRP, EM, SW, ML | WP-H-01…H-07, WP-W-01…W-06, W-09…W-11, WP-P-07…P-09 | G2 passed |
| P4 Integration and verification | Build the actuator bench, the hardware-in-the-loop rig and the gantry; hardware, software and system integration; PL verification; stability, fall and controlled-descent tests on the gantry; contact and power-and-force measurements; E-stop and chain validation; fault injection against the 13849-2 fault lists | SRP, SW, test bench owner | WP-S-08, S-09, WP-H-06, WP-W-07, W-08, WP-V-02…V-05 | G3 passed; bench and gantry available |
| P5 Validation and release | Safety validation on the robot under WP-V-07; unknown-scenario trials; cybersecurity validation; safety case completion; technical documentation; functional safety assessment; conformity assessment per WP-M-13; release record | SM, SRP, EA | WP-V-01, V-06, V-08, WP-K-01…K-07, WP-O-01…O-03, WP-P-10 | G4 passed |
| P6 Operation | Field monitoring, safety anomaly handling after release, controlled updates, incident response | SM, CSM | WP-O-04, O-05, WP-P-03 | G5 passed; release record signed |

### 4.1 Early implementation of at-risk work

Some changes cannot wait for their phase. The gap assessment's priority action 3 (a gantry and rated tether, a
wired dual-channel E-stop in the operator's hand that removes motor power, a cleared and marked area, and a bench
supply instead of a battery) is bench equipment that makes every powered test defensible. It is implemented in P0/P1
under this rule:

1. The change is recorded as an impact-analysed change under [`07-supporting/impact/`](../07-supporting/impact/README.md),
   naming the hazards it mitigates and the work products that will later specify it properly.
2. It is **not** claimed as a safety function with a PL until WP-C-04 specifies it and WP-H-04 calculates it. Until
   then it is bench equipment, and the test procedure ([WP-V-07](../06-validation/WP-V-07-test-operations.md)) relies on the
   tether, the operator's hand on the button and the cleared area, not on a PL.
3. Its design is carried forward, not thrown away: the bench E-stop chain becomes the first draft of WP-H-02 and the
   tether and gantry become the complementary measure of WP-C-05 and claim G2.4.

The purchases themselves are decisions DQ-007 and DQ-008 for the lead.

## 5. Tailoring of the standards

Tailoring decisions T-01…T-14 are recorded in [WP-M-01 §5](WP-M-01-assurance-strategy.md#5-tailoring). This plan
applies them; it adds none.

## 6. Supporting processes

| Process | Work product | State |
|---|---|---|
| Configuration management, baselines, safety-relevant file list | [WP-P-01](../07-supporting/WP-P-01-configuration-management-plan.md) | Skeleton; the safety-relevant file list exists as [`safety-relevant-paths.txt`](../07-supporting/safety-relevant-paths.txt) |
| Change management, impact analysis | [WP-P-02](../07-supporting/WP-P-02-change-management.md), [WP-M-11](WP-M-11-impact-analysis.md) | Skeleton |
| Problem resolution, safety anomalies | [WP-P-03](../07-supporting/WP-P-03-problem-resolution.md) | Skeleton; GitHub issue templates in place |
| Documentation management, technical file | [WP-P-04](../07-supporting/WP-P-04-documentation-management.md), [WP-K-02](../10-safety-case/WP-K-02-technical-documentation-index.md) | Skeleton |
| Verification and review | [WP-P-05](../07-supporting/WP-P-05-verification-review-procedure.md) | Skeleton |
| Requirements management and traceability | [WP-P-06](../07-supporting/WP-P-06-requirements-management-traceability.md), [`trace/`](../trace/README.md) | Skeleton; hazards, safety functions and assumptions recorded; the 120 requirements and 139 test cases of the concept-phase package wait to be ported |
| Tool and component qualification | [WP-P-07](../07-supporting/WP-P-07-tool-classification-qualification.md), [WP-P-08](../07-supporting/WP-P-08-software-component-qualification.md) | Skeleton |
| Release | [WP-P-10](../07-supporting/WP-P-10-release-management.md) | Skeleton |
| Integrated process model | [WP-P-11](../process/README.md) | Draft; maps and gate skeletons generated |

## 7. Work products and documentation

The list of work products, their clauses, gates and status is [WP-M-00](WP-M-00-work-product-register.md). Every work
product carries the document-control header of the [assurance README](../README.md#document-control-header) and
changes by pull request. Technical documentation for the Machinery Regulation (Annex IV) is assembled by
[WP-K-02](../10-safety-case/WP-K-02-technical-documentation-index.md) from the register.

## 8. Confirmation measures

Confirmation reviews, functional safety audits, the functional safety assessment, the cybersecurity and ML reviews
and the conformity assessment are planned in [WP-M-06](WP-M-06-confirmation-measures-plan.md), with the gate at which
each is due in its §9. No measure has been performed and no assessor is engaged.

## 9. Safety anomaly handling

A safety anomaly is any observed or suspected behaviour that could violate a safety function, an operating limit
or an assumption of the risk assessment, during development testing or in operation: an uncommanded motion, a fall
or a near-fall, a contact with a person, a stop that did not happen or was late, a tether that took load. It is
raised as a GitHub issue labelled `safety-anomaly` using the problem report template, triaged by the safety manager
within one working day, and handled under [WP-P-03](../07-supporting/WP-P-03-problem-resolution.md). An anomaly with
injury or property damage also follows the field monitoring procedure ([WP-O-04](../09-production-operation/WP-O-04-field-monitoring.md)).
Testing stops until the safety manager lifts the stop (WP-V-07 §6). The safety manager lifts it alone, always
(DQ-062 B, decided 2026-10-21); while the project has one person this is the operator clearing their own anomaly, and
every anomaly issue states that no independent step exists (GAP-30, GAP-32 stay open in substance).

## 10. Progress tracking and gate reviews

Progress is tracked against the register (status column), the open items of each work product, the open risks in
[WP-M-07](WP-M-07-risk-management.md) and the decision register. A gate review is held by the safety manager with the
roles of the phase and, where engaged, the assessor. Its inputs are the status of the gate's work products, open
anomalies, open risks, the confirmation measures assigned to the gate and their results, QA findings and the open
items of the phase's work products. A gate cannot pass if a confirmation review assigned to it has not been
performed, unless the safety manager and the assessor agree a documented deferral. G0 was passed with conditions on
2026-10-21 (DQ-020 A); G1 is held after the first hang test, once the measured mass, centre of gravity and fall data
are in WP-C-01, WP-C-03 and WP-S-04 (DQ-030 A). Records go to
[`10-safety-case/gates/`](../10-safety-case/gates/README.md); a pre-filled skeleton per gate is generated by the
[process model](../process/README.md).

## 11. Safety case content per gate

| Gate | Safety case content due |
|---|---|
| G1 | Top-level claim and sub-claims (WP-M-01 §3.2); hazard log; GAP-01…GAP-34 registered as defeaters; assumptions on the operating envelope and the tether |
| G2 | Argument for G1 (PL per safety function) structured on the stop chain and safety-layer architecture; defeaters from the system analyses |
| G3 | Evidence items for the PL calculation, component qualification and software verification, recorded, not yet accepted |
| G4 | Test results as evidence; fault-injection outcome; defeaters closed or carried |
| G5 | Complete case with accepted evidence per confirmation review; assessment report; release conditions |
| G6 | Field findings as new defeaters; periodic re-review |

## 12. Open items

| ID | Item | Owner | Gate |
|---|---|---|---|
| OI-1 | Fill the verification reviewer and QA roles; until then every review is I0 and no work product can leave Draft | PM | G0 |
| OI-2 | Decide who approves work products the safety manager authors (DQ-011, queued behind DQ-010) | PM | G0 |
| OI-3 | ~~Engage the external assessor or record the decision not to for now (DQ-010)~~ decided 2026-10-21 (A: not for now); revisit at G1 | PM | G1 |
| OI-4 | Classify the AI assistant and the other drafting tools in WP-P-07 | SM | G3 |
| OI-5 | Replace §4 with a generated lifecycle figure pinned to this table | SM | G1 |
