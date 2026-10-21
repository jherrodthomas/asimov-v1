# WP-K-01 Safety Case

| Field | Value |
|---|---|
| Work product | WP-K-01 Safety case for the laboratory configuration (UL 4600 structure: claims, arguments, evidence, defeaters) |
| Standard reference | ISO 13849-1:2023 §4.7, §10 (information); ISO 12100 §7 (documentation); ISO 13482:2014 §7 (verification and validation, as the test matrix of the argument); Regulation (EU) 2023/1230 Annex IV Part A (technical documentation); UL 4600 §5, §6. Every clause to be checked against a licensed copy |
| Version | 0.1 (2026-10-21): initial structure from the concept-package GSN (`09_GSN`), evidence register (`10_Evidence`) and gap register (`11_Gaps`); every claim draft, every defeater open; 22 evidence items, 34 defeaters, 10 open items |
| Status | Draft |
| PL / scope | PL d target (DQ-004); CFG-001 kit robot, tethered, bench-powered, fork-evaluated; CFG-002 battery and policy robot, upstream-compatible, unverified; OE-1 only (DQ-002) |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I2 for the safety case) |
| Approver | Project lead |
| Baseline | BL-001 |

> [!WARNING]
> Draft. No claim is accepted, no evidence is available, every defeater is open. The machine-readable copy of
> this document lives in `assurance/case/`; the validator fails if the two disagree (check X3). The dashboard in
> the README is generated from those records.

## 1. Purpose and scope

This document argues, for the two configurations of [WP-C-01](../02-concept/WP-C-01-item-definition.md) §1
(CFG-001, the kit robot as the fork evaluates it: tethered under a gantry, bench-powered, no battery, tele-operated;
CFG-002, the upstream-compatible robot with a battery and the locomotion policy, unverified), that the robot poses
no unreasonable risk when operated within the laboratory envelope OE-1 of
[WP-C-02](../02-concept/WP-C-02-operating-environment-and-tasks.md). At BL-001 the argument is a structure with
open defeaters: it records what would have to be true, what evidence would show it, and what is known to contradict
it today. The concept package's GSN (`09_GSN`) is its seed; the package's evidence register is the source of the
Partial statuses, and its gap register is the source of the defeaters, one per gap.

## 2. Argument structure

Goal G0 is argued over four strategies: S1 per safety function (G1.x), S2 over the complementary measures (G2.x),
S3 over the command path (G3.x), S4 over the process (G4.x). GSN diagrams are generated from the records
(`case/tools`), not drawn by hand.

Two claims carry what makes a biped different from a wheeled machine. G1.1 (bipedal stability, SF-01) is at
present allocated to a learned locomotion policy that has not been released; whether it may stay there, or whether
the deterministic layer must bound it, is DQ-006, and until that is answered G1.1 rests on simulation alone. G2.4
(the tether and gantry of OE-1) carries the fall hazard in place of a fall-arrest function: it is the complementary
measure that makes testing defensible while G1.2 (controlled descent, SF-02) has no implementation, and the
case for the first item depends on it more than on any safety function.

The cybersecurity branch of the argument is WP-K-03 ([cybersecurity case](WP-K-03-cybersecurity-case.md)); claims there that protect a safety function are referenced from the claims below, and the evidence for the safety functions themselves stays in this document.

## 3. Claims

Status rule: draft = stated, no evidence accepted; supported = evidence available and reviewed; accepted = the
project lead has accepted it at a named baseline. "Open defeaters" counts the defeaters of §7 that name the claim.

| ID | Claim | Parent | Status | Evidence | Open defeaters |
|---|---|---|---|---|---|
| G0 | Asimov v1 in its laboratory envelope poses no unreasonable risk | — | draft | Sn-01, Sn-02, Sn-03, Sn-05, Sn-06 | 2 |
| G1 | The safety functions with a required Performance Level reach it | G0 | draft | Sn-04, Sn-08, Sn-09 | 2 |
| G1.1 | SF-01 bipedal stability is maintained at PL d | G1 | draft | Sn-04, Sn-18 | 5 |
| G1.2 | SF-02 fall arrest by controlled descent is implemented at PL d | G1 | draft | Sn-04, Sn-11 | 3 |
| G1.3 | SF-03 joint torque and velocity limits are enforced at PL d | G1 | draft | Sn-04, Sn-18 | 1 |
| G1.4 | SF-04 force-limited contact is implemented at PL d | G1 | draft | Sn-04, Sn-13 | 1 |
| G1.5 | SF-06 speed reduction in human-shared regions is implemented at PL c | G1 | draft | Sn-04 | 1 |
| G1.6 | SF-08 safe stop on watchdog timeout or communication loss is implemented at PL d | G1 | draft | Sn-04, Sn-22 | 4 |
| G1.7 | SF-11 overcurrent protection on each motor branch is implemented at PL c | G1 | draft | Sn-04, Sn-17 | 1 |
| G1.8 | SF-13 emergency-stop link surveillance is implemented at PL d | G1 | draft | Sn-04, Sn-12 | 4 |
| G1.9 | SF-14 stator over-temperature shutdown is implemented at PL c | G1 | draft | Sn-04 | 1 |
| G1.10 | SF-15 battery protection by the BMS is implemented at PL e | G1 | draft | Sn-04 | 1 |
| G1.11 | SF-16 the audio limiter holds 80 dBA at 1 m (PL b) | G1 | draft | Sn-04 | 0 |
| G1.12 | SF-20 power-and-force limiting in collaborative mode is implemented at PL d | G1 | draft | Sn-04, Sn-13 | 1 |
| G1.13 | SF-23 IMU plausibility and cross-check is implemented at PL d | G1 | draft | Sn-04, Sn-22 | 1 |
| G1.14 | SF-24 the scheduler watchdog and deadline monitor are implemented at PL d | G1 | draft | Sn-04, Sn-22 | 1 |
| G1.15 | SF-25 software joint limits inside the mechanical end-stops are implemented at PL c | G1 | draft | Sn-04, Sn-10 | 0 |
| G2 | The complementary mechanical, electrical and procedural measures are implemented | G0 | draft | — | 0 |
| G2.1 | Structure, guarding and edges are as designed | G2 | draft | Sn-10, Sn-19 | 3 |
| G2.2 | Electrical isolation, protection and the battery are as designed | G2 | draft | Sn-17 | 3 |
| G2.3 | Procedures and operating restrictions are in place and known to the people who need them | G2 | draft | Sn-21 | 1 |
| G2.4 | The tether and gantry of OE-1 carry the fall hazard while no fall-arrest function exists | G2 | draft | Sn-21 | 1 |
| G3 | The command path cannot defeat the safety functions | G0 | draft | — | 0 |
| G3.1 | Tele-operation and the API are authenticated, integrity-protected and bounded | G3 | draft | Sn-20 | 3 |
| G4 | The evidence was produced under a controlled process | G0 | draft | — | 0 |
| G4.1 | A configuration baseline exists and the fork is pinned to it | G4 | draft | Sn-15 | 0 |
| G4.2 | Hazards are identified completely and rated | G4 | draft | Sn-02, Sn-01, Sn-06 | 2 |
| G4.3 | Verification and review evidence exists for the safety-related software and firmware | G4 | draft | Sn-22, Sn-16 | 8 |
| G4.4 | The DIY-kit build is controlled | G4 | draft | Sn-19 | 3 |

## 4. Assumptions of use

AOU-01 to AOU-07 of WP-C-01 §8 apply to every claim ([trace/items/aou.yaml](../trace/items/aou.yaml)). At BL-001
each holds only procedurally: a trained operator (AOU-01), the tether and gantry (AOU-02), a level dry floor
(AOU-05) and nobody within reach of a powered limb (AOU-06) are conditions of WP-V-07, not properties of the robot.

## 5. Safety functions and Performance Levels

Seventeen of the 25 safety functions of [WP-C-04](../02-concept/WP-C-04-safety-functions-and-plr.md) carry a PLr:
SF-01, SF-02, SF-03, SF-04, SF-08, SF-13, SF-20, SF-23, SF-24 at PLr d; SF-06, SF-11, SF-14, SF-25 at PLr c;
SF-15 at PLr e (battery protection, the BMS as a certified component); SF-16 at PLr b. The remaining eight are
static or procedural measures (guarding, markings, materials, the mechanical end-stops) argued under G2. The
PLr values are the concept package's proposal pending DQ-004 and the re-rating of WP-C-03 OI-2. None reaches
any PL at BL-001: no safety function has an implementation in any public repository (GAP-16), no reliability
figure exists (GAP-14) and no single-fault tolerance is designed (GAP-09).

## 6. Evidence

Status rule: Available = performed and approved at a named baseline; Partial = drafted analysis or
specification, not reviewed; Missing = not yet performed.

**Available 0, Partial 15, Missing 7** (22 evidence items)

| ID | Evidence | Location | Status | Supports |
|---|---|---|---|---|
| Sn-01 | Item definition and limits of the machinery | `assurance/02-concept/WP-C-01-item-definition.md` | Partial | G0, G4.2 |
| Sn-02 | Risk assessment and PLr determination | `assurance/02-concept/WP-C-03-risk-assessment.md` | Partial | G0, G4.2 |
| Sn-03 | Baseline gap assessment GAP-01 to GAP-34 | `assurance/00-assessment/gap-assessment.md` | Partial | G0 |
| Sn-04 | Safety functions specification SF-01 to SF-25: demand, safe state, response, stop category, PLr, allocation | `assurance/02-concept/WP-C-04-safety-functions-and-plr.md` | Partial | G1, G1.1, G1.2, G1.3, G1.4, G1.5, G1.6, G1.7, G1.8, G1.9, G1.10, G1.11, G1.12, G1.13, G1.14, G1.15 |
| Sn-05 | Operating environment and task specification: the four operating envelopes | `assurance/02-concept/WP-C-02-operating-environment-and-tasks.md` | Partial | G0 |
| Sn-06 | Concept-package safety-case workbook: hazard catalogue, HARA, FSC, GSN, evidence and gap registers | `assurance/00-assessment/concept-package/Asimov_v1_Safety_Case.xlsx` | Partial | G0, G4.2 |
| Sn-07 | Concept-package DFMEA: 32 failure modes, 19 at high action priority | `assurance/00-assessment/concept-package/Asimov_v1_DFMEA.xlsx` | Partial |  |
| Sn-08 | Concept-package requirements workbook: 120 requirements (63 safety) with trace | `assurance/00-assessment/concept-package/Asimov_v1_Requirements.xlsx` | Partial | G1 |
| Sn-09 | Concept-package test plan: 139 test cases, ISO 13849-2 and ISO 13482 §7 matrices | `assurance/00-assessment/concept-package/Asimov_v1_TestPlan.xlsx` | Partial | G1 |
| Sn-10 | Mechanical CAD of the seven subassemblies (STEP) | `mechanical/README.md` | Partial | G1.15, G2.1 |
| Sn-11 | Stability, fall and controlled-descent test record | `assurance/06-validation/README.md` | Missing | G1.2 |
| Sn-12 | Emergency-stop and safety-chain test record (each device, link loss, welded contact, re-arm) | `assurance/06-validation/README.md` | Missing | G1.8 |
| Sn-13 | Contact force, pressure and power-and-force-limiting measurement | `assurance/06-validation/README.md` | Missing | G1.4, G1.12 |
| Sn-14 | Fault injection record | `assurance/06-validation/README.md` | Missing |  |
| Sn-15 | Baseline record BL-001 | `assurance/case/baselines/baselines.yaml` | Partial | G4.1 |
| Sn-16 | Safety case WP-K-01 | `assurance/10-safety-case/WP-K-01-safety-case.md` | Partial | G4.3 |
| Sn-17 | Electrical record: motion control board KiCad sources and the WireViz harness | `electrical/README.md` | Partial | G1.7, G2.2 |
| Sn-18 | MuJoCo simulation model with the per-joint control ranges | `sim-model/xmls/asimov.xml` | Partial | G1.1, G1.3 |
| Sn-19 | Material and build acceptance record (mill certificates, harness pull test, commissioning checks) | `assurance/06-validation/README.md` | Missing | G2.1, G4.4 |
| Sn-20 | Tele-operation and API security concept and test | `assurance/06-validation/README.md` | Missing | G3.1 |
| Sn-21 | Test operations procedure for powered testing (the hold point) | `assurance/06-validation/WP-V-07-test-operations.md` | Partial | G2.3, G2.4 |
| Sn-22 | Firmware safety-layer verification (tests in CI, static analysis, bench results) | `assurance/06-validation/README.md` | Missing | G1.6, G1.13, G1.14, G4.3 |

## 7. Defeaters

One defeater per gap of the [gap assessment](../00-assessment/gap-assessment.md): DF-nn is GAP-nn. A defeater is
closed when the gap closes with evidence the case accepts; none is closed at BL-001.

| ID | Defeater | Gap | Claims | Status |
|---|---|---|---|---|
| DF-01 | Adequacy-of-risk-reduction record absent for 18 of the 32 hazards | GAP-01 | G0, G4.2 | open |
| DF-02 | Information for use not published; the manual's safety, quick-start and BOM pages return 404 | GAP-02 | G2.3 | open |
| DF-03 | No tip-over or stability analysis; the fall energy of the 35 kg body is unbounded | GAP-03 | G1.1, G1.2, G2.4 | open |
| DF-04 | No structural fatigue or material evidence: hip-yoke fillet, 7075 substitution, SLM porosity | GAP-04 | G2.1 | open |
| DF-05 | Force, pressure and energy contact limits not declared | GAP-05 | G1.4, G1.12 | open |
| DF-06 | Joint speed, torque and momentum limits not declared; the MuJoCo ctrlrange values are the only published limits | GAP-06 | G1.3 | open |
| DF-07 | E-stop architecture undocumented: no device, receiver or contactor in the electrical record | GAP-07 | G1.8 | open |
| DF-08 | No power distribution board, fuse table, disconnection device or battery in the repository | GAP-08 | G1.7, G2.2 | open |
| DF-09 | Single-fault tolerance (Category 3) not implemented for any safety function | GAP-09 | G1.1, G1.6, G1.8 | open |
| DF-10 | The safe state of the biped is undefined: DAMP drops the robot and no controlled-descent function exists | GAP-10 | G1.2, G1.6 | open |
| DF-11 | Wireless E-stop link: no surveillance, latency, fail-safe or re-arm behaviour documented | GAP-11 | G1.8 | open |
| DF-12 | The battery is user-supplied with no compliance gate and no BMS interlock | GAP-12 | G1.10, G2.2 | open |
| DF-13 | Bipedal stability (SF-01) is allocated to an unreleased learned locomotion policy with no independent safeguard specified | GAP-13 | G1.1 | open |
| DF-14 | MTTFD, DC and CCF figures absent; no actuator or board reliability data from upstream | GAP-14 | G1 | open |
| DF-15 | No validation plan or test report exists for any safety function | GAP-15 | G1 | open |
| DF-16 | No firmware or motion-control software in any public repository | GAP-16 | G1.6, G1.13, G1.14, G4.3 | open |
| DF-17 | The locomotion policy is unreleased; its training, simulation-to-real evidence and behaviour are undefined | GAP-17 | G1.1, G1.5 | open |
| DF-18 | The Asimov API contract is pre-1.0 and unstable | GAP-18 | G3.1 | open |
| DF-19 | The tele-operation authentication scheme is not documented | GAP-19 | G3.1 | open |
| DF-20 | The wireless E-stop link and the UART debug port have no documented protection | GAP-20 | G1.8, G3.1 | open |
| DF-21 | The simulation model is the only dynamics data and is not pinned to any hardware revision | GAP-21 | G1.1, G4.3 | open |
| DF-22 | The CAN harness depends on DIY crimp quality and termination with no acceptance criterion | GAP-22 | G1.6, G4.4 | open |
| DF-23 | No under-voltage lockout or power-good specification; mid-stride power loss goes unflagged | GAP-23 | G1.2, G2.2 | open |
| DF-24 | No mechanical BOM, torque table or threadlocker specification in the repository | GAP-24 | G2.1, G4.4 | open |
| DF-25 | No stator thermistor cut-off or head-shell thermal validation documented | GAP-25 | G1.9 | open |
| DF-26 | Guarding gaps at the waist and neck yaw unverified against ISO 13857 | GAP-26 | G2.1 | open |
| DF-27 | Records of test, calibration and nonconformance are not maintained | GAP-27 | G4.3 | open |
| DF-28 | Design review and design verification records are absent | GAP-28 | G4.3 | open |
| DF-29 | Production process controls are undeclared for the DIY-kit assembly | GAP-29 | G4.4 | open |
| DF-30 | No nonconformance procedure | GAP-30 | G4.3 | open |
| DF-31 | No internal audit or monitoring | GAP-31 | G4.3 | open |
| DF-32 | No corrective-action system | GAP-32 | G4.3 | open |
| DF-33 | The concept-phase package is unreviewed, AI-assisted and outside the record's conventions | GAP-33 | G0, G4.2 | open |
| DF-34 | Process capability estimated at CL0 for every engineering process | GAP-34 | G4.3 | open |

## 8. Reviews

None at BL-001. The concept package's own review status is "unreviewed" (DF-33); the first review of this case is
the I2 review planned at G1 ([WP-M-06 §9](../01-management/WP-M-06-confirmation-measures-plan.md#9-schedule-summary)).

## 9. Residual risk statement

Not yet possible: no safety function exists on either configuration, no fall-arrest or controlled-descent function
exists, and no contact limit is measured, so no operation with people within reach of a powered limb and no
free-standing operation is within this case ([WP-C-03 §8](../02-concept/WP-C-03-risk-assessment.md#8-residual-risk-and-conditions)).
Powered testing proceeds only under the hold point of [WP-V-07](../06-validation/WP-V-07-test-operations.md), with
the gantry, the wired E-stop and the bench supply standing in for G1 and G2.

## 10. Open items

Each open item is an action record in `assurance/case/actions/`; the work product it comes from is named in brackets.

| ID | Item | Needed by | Claims |
|---|---|---|---|
| OI-1 | Weigh the robot, measure the centre of gravity and bound the fall energy (WP-C-01 OI-1) | G1 | G1.2, G2.4, G4.2 |
| OI-2 | Decide the safe state of the biped: controlled descent, hold, or power removal (DQ-005) (WP-C-04 OI-1) | G1 | G1.2, G1.6 |
| OI-3 | Decide whether the learned locomotion policy may carry SF-01 (DQ-006) (WP-C-04 OI-2) | G1 | G1.1 |
| OI-4 | Obtain or design the E-stop architecture: devices, receiver, contactors, stop category (DQ-008) (WP-C-04 OI-3) | G1 | G1.8 |
| OI-5 | Obtain actuator, encoder and board reliability data from upstream or the suppliers (WP-M-10 OI-1) | G2 | G1 |
| OI-6 | Reviewer with build or operating experience confirms every rating in WP-C-03 (WP-C-03 OI-2) | G1 | G4.2 |
| OI-7 | Port the 120 requirements and 139 test cases of the concept package into WP-S-02 and WP-V-01 (WP-S-02 OI-1) | G2 | G1 |
| OI-8 | Set the battery policy: certified pack list and BMS handshake interlock (DQ-009) (WP-C-01 OI-2) | G1 | G1.10, G2.2 |
| OI-9 | Specify the tether and gantry of OE-1 and record them as the complementary measure (DQ-007) (WP-V-07 OI-1) | G1 | G2.4 |
| OI-10 | Get the manual's safety, quick-start and BOM pages published, or write the information for use (WP-O-03 OI-1) | G1 | G2.3 |
