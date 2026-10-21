# Baseline Gap Assessment

| Field | Value |
|---|---|
| Work product | Baseline gap assessment (supporting document, not a registered work product) |
| Standard reference | ISO 12100:2010; ISO 10218-1:2011/-2:2011; ISO/TS 15066:2016; ISO 13482:2014; ISO 13849-1:2023 and 13849-2:2012; IEC 60204-1:2018; IEC 62133-2:2017; ISO 13850:2015; IEC 62443-4-1/-4-2; ISO/IEC TR 5469:2024; Regulation (EU) 2023/1230 |
| Version | 0.1: initial assessment (2026-10-21) |
| Status | Draft |
| Author | Assurance team (AI-assisted review of the repository and the concept-phase package, I0) |
| Reviewer(s) | TBD |
| Baseline | `jherrodthomas/asimov-v1@3d4ec9d` (2026-05-03), which is upstream `asimovinc/asimov-v1@5de64d3` (2026-04-30) plus the fork's concept-phase package of 2026-05-03 |

## 1. Scope and method

This was a static review of the fork repository at the baseline above and of the concept-phase engineering package
the fork added to it. No code was built or executed (there is none to build) and no robot was operated.

- **Areas reviewed:**
  1. the hardware record: mechanical CAD (`mechanical/ASV1/`, seven subassemblies as STEP), the motion control board
     (`electrical/motion_control/`, KiCad sources, v0.1.4), the wiring harness (`electrical/wiring/`, WireViz);
  2. the simulation model (`sim-model/xmls/asimov.xml`, MuJoCo, 25 actuated joints with control ranges);
  3. the published description: the upstream README (specifications, DIY kit contents, roadmap) and what the
     manual at `manual.asimov.inc` does and does not publish;
  4. the concept-phase package ([`concept-package/`](concept-package/README.md)): the safety-case workbook (item
     definition, 32 hazards, HARA, system FMEA, 25 safety functions, GSN, evidence and gap registers), the DFMEA
     (32 failure modes), the requirements workbook (120 requirements), the test plan (139 test cases), the
     architecture description and the trace memo.
- **Configuration:** findings are stated for the **DIY-kit robot as published**: 1.2 m, 35 kg, 25 actuated joints
  plus two passive toes, a Radxa CM5 motion control board with six CAN buses and an LSM6DSV IMU, a Raspberry Pi 5
  edge board with a 2 MP camera, a quad microphone array and a 10 W speaker, 7075 aluminium and MJF PA12
  structure, three operating modes DAMP, STAND and MOVE. The firmware, the Asimov API, the locomotion policy and the
  mobile app are marked as upcoming in the roadmap and are covered in §8 as absences, not as assessed design.
- **Not reviewed:** upstream's manual pages behind the 404s; the DIY-kit contents beyond the README table; the
  Raspberry Pi 5 "edge board" and the "power distribution board" the kit lists, neither of which is in the
  repository.
- **Numbering:** IDs run GAP-01…GAP-34 and are grouped by area, not in numeric order. The 28 gaps of the
  concept-phase package are re-stated here with their package ID in the evidence column; six findings (GAP-04,
  GAP-10, GAP-13, GAP-20, GAP-21, GAP-33) are new. IDs are never reused.
- **Standards text:** the standards are copyrighted and not reproduced. Clause references are to the editions in
  the header and must be checked against a licensed copy before an audit.

**Provenance.** The fork carries no change to the robot. Every finding below about the robot is a finding about
upstream Asimov v1 as inherited; upstream's own README says plainly what is not yet released. The concept-phase
package is the fork's own work, produced with AI assistance and never reviewed; where it already states a gap, that
is recorded here as a strength of the package (§9) and the gap stays a gap.

## 2. Summary

| Area | Assessment |
|---|---|
| Safety architecture | The shape is there: a dedicated motion control board (Radxa CM5) between the edge board and 25 actuators on six CAN buses, with a hardware IMU, and a declared mode machine (DAMP, STAND, MOVE). But nothing of the control software exists in public, the wireless E-stop has no documented architecture, and the only declared safe state (DAMP, motors limp) **drops a 35 kg body from 1.2 m** |
| Stop and fall functions | **No safety function reaches any Performance Level.** No E-stop device, receiver, contactor or stop category is in the record; no fall-arrest or controlled-descent function exists; the safe state of a standing biped is undefined |
| Mechanical | No mass measurement, centre of gravity, tip-over margin, fatigue analysis or fall-energy bound. The package estimates 411 J at the centre of mass in a fall and rates hip-yoke fatigue and material substitution as high-priority failure modes with no detection |
| Electrical | The motion control board is well documented (KiCad, LCSC IDs). The power distribution board, the fuse table, any disconnection device and the battery are absent from the repository; the battery is excluded from the kit and uncontrolled |
| Risk assessment, requirements, analyses | Upstream has none. The fork's package has a hazard catalogue, a HARA, an FMEA, 120 requirements and 139 test cases, all unreviewed, with 18 of 32 hazards lacking an adequacy-of-risk-reduction record |
| Software and the policy | No firmware, API or locomotion policy in any public repository. Balance is a learned function nobody outside upstream has seen. The MuJoCo model is the only dynamics data |
| Process capability | Upstream: git and pull requests, honest roadmap, open licences; no safety or quality process. The fork: a package without document control, baseline or review |
| Cybersecurity | Tele-operation over a WebRTC data channel from an operator app through an unpublished API; no authentication scheme documented; the wireless E-stop link and the UART debug port have no documented protection |

## 3. Risk assessment and risk reduction (ISO 12100, ISO 13482)

| ID | Finding | Evidence | Standard | Severity |
|---|---|---|---|---|
| GAP-01 | **Adequacy-of-risk-reduction record absent for 18 of the 32 hazards.** The package rates every hazard and names safety functions, but records no argument that the reduction is adequate for more than half of them | package `12_Gaps` GAP-12100-01; `07_HARA` residual column | 12100 §5.6, §6.1; Machinery Reg. Annex III §1.1.2 | High |
| GAP-02 | **Information for use is not published.** The manual's safety, quick-start and BOM pages (`/v1/safety`, `/v1/quickstart`, `/v1/bom`) return 404; no residual-risk statement, warnings or operator manual exist | package `12_Gaps` GAP-12100-02, GAP-DOC-01; `13_Assumptions` OI-04 | 12100 §6.4; 13482 §7.2; Machinery Reg. Annex III §1.7 | High |
| GAP-03 | **No tip-over or stability analysis, and the fall energy is unbounded.** Mass (35 kg) and height (1.2 m) are README figures; no centre of gravity, static or dynamic tip-over margin, slope limit or fall-energy calculation exists beyond the package's 411 J estimate; the robot has not been weighed | package `12_Gaps` GAP-13482-03; `03_ItemDef` space limits; README specifications | 13482 §5.13; 12100 §5.3; 10218-1 §5.10 | High |
| GAP-04 | **No structural fatigue or material evidence.** The DFMEA rates hip-yoke fatigue (FM-01), 6061 substituted for 7075 in a DIY build (FM-02, detection 9 of 10) and SLM 316L porosity (FM-30) as high-priority failure modes; no FEA, fatigue test, mill certificate or incoming inspection exists | package DFMEA `05_DFMEA_Worksheet` FM-01, FM-02, FM-30 | 12100 §6.2; 13482 §5.4; Machinery Reg. Annex III §1.3.2 | High |
| GAP-05 | **Force, pressure and energy contact limits not declared.** No body-region limit, contact area or peak energy is stated for any joint or for the falling body; the ISO/TS 15066 Annex A limits are cited but not applied | package `12_Gaps` GAP-13482-01, GAP-15066-01; `09_FSC` SF-04, SF-20 | 13482 §5.7; TS 15066 §5.5; 10218-1 §5.10 | High |
| GAP-06 | **Joint speed, torque and momentum limits not declared.** The only published limits are the MuJoCo `ctrlrange` values (36 to 145 N m per joint), which are simulation values; nothing states what the firmware enforces | package `12_Gaps` GAP-13482-02; `sim-model/xmls/asimov.xml` motor elements | 13482 §5.10; 10218-1 §5.4 | High |

## 4. Safety functions and the stop chain (ISO 10218-1, ISO 13482 §5.16, ISO 13849)

| ID | Finding | Evidence | Standard | Severity |
|---|---|---|---|---|
| GAP-07 | **The emergency-stop architecture is undocumented.** The kit lists a "wireless E-Stop"; the repository holds no E-stop device, receiver, contactor, stop category, channel structure or reset rule. The harness feeds every actuator battery power and CAN with nothing in between that could remove power | README DIY-kit table; `electrical/wiring/wiring.yaml` (XT30(2+2) BATT+/BATT−/CAN per actuator); package `12_Gaps` GAP-10218-03 | 13850 §4; 60204-1 §9.2.3.4; 10218-1 §5.5; 13482 §5.16 | High |
| GAP-08 | **No power distribution board, fuse table, disconnection device or battery in the repository.** The kit lists a "power distribution board"; the record has none; the motion control board takes 5 V on an XT30; nothing documents the motor rail, its protection or how it is switched off | `electrical/README.md`; README DIY-kit table; package `12_Gaps` GAP-60204-01 | 60204-1 §5.3, §7.2 | High |
| GAP-09 | **Single-fault tolerance is not implemented for any safety function.** Every function the package allocates at Category 3 (SF-01…SF-04, SF-08, SF-13, SF-15, SF-20, SF-23, SF-24) runs through one IMU, one controller and single actuators | package `12_Gaps` GAP-10218-01, GAP-13849-01; DFMEA FM-05, FM-11, FM-12 | 13849-1 §6; 10218-1 §5.4.2 | High |
| GAP-10 | **The safe state of the biped is undefined.** The declared default on disconnect or E-stop release is DAMP (motors limp), which drops the robot; the package lists DAMP itself as a hazard (HZ-C01) and its DFMEA asks for a controlled descent (FM-06, FM-14) that no document specifies | README specifications (modes); package `06_Hazards` HZ-C01, HZ-P03; DFMEA FM-06, FM-10, FM-14 | 13849-1 §5.2 (safe state); 13482 §5.13; 60204-1 §9.2.2 | High |
| GAP-11 | **The wireless E-stop link has no surveillance, latency, fail-safe or re-arm behaviour.** A dead transmitter battery or a jammed link leaves the button ineffective (FM-19, severity 10, detection 4); an automatic re-arm restarts the robot with the operator out of position (FM-20) | package `12_Gaps` GAP-13482-04; DFMEA FM-19, FM-20 | 13850 §4; 13849-1 §6; 13482 §5.16 | High |
| GAP-12 | **The battery is user-supplied with no compliance gate and no BMS interlock.** The kit excludes the battery; nothing checks what is installed; the DFMEA gives the missing BMS the only detection score of 10 in the worksheet (FM-22) | README DIY-kit table; package `12_Gaps` GAP-BMS-01; `13_Assumptions` ASS-A-02, OI-05; DFMEA FM-21, FM-22 | 62133-2; UN 38.3; 60204-1 §7 | High |
| GAP-13 | **Bipedal stability is allocated to an unreleased learned policy with no independent safeguard.** The package puts SF-01 (PL d, Category 3) on "loco. policy + IMU + MCB"; the policy is a neural network trained in simulation that upstream has not published; no deterministic function keeps the robot up if it misbehaves | package `09_FSC` SF-01; README roadmap (locomotion policy upcoming); package `12_Gaps` GAP-LP-01 | 13849-1 §4.5, §7; TR 5469 §6–§8; Machinery Reg. Annex I Part A | High |

## 5. Control system reliability and validation (ISO 13849)

| ID | Finding | Evidence | Standard | Severity |
|---|---|---|---|---|
| GAP-14 | **MTTFD, DC and CCF figures are absent.** Upstream publishes no failure rate, B10d or certificate for the actuators, encoders, IMU or boards; the achievable PL of any function cannot be computed | package `12_Gaps` GAP-13849-02; `04_StdMatrix` ISO 13849-1 §7 row | 13849-1 §6, Annex C–F | High |
| GAP-15 | **No validation plan or test report exists for any safety function.** The package's test plan has 139 test cases and two validation matrices; none has been executed, and no robot has been run under any procedure | package `12_Gaps` GAP-13849-03, GAP-13482-06, GAP-10218-02; test plan `Asimov_v1_TestPlan.xlsx` | 13849-2 §4–§5; 13482 §7; 10218-1 §6 | High |

## 6. Software, firmware and the learned policy

| ID | Finding | Evidence | Standard | Severity |
|---|---|---|---|---|
| GAP-16 | **No firmware or motion-control software is in any public repository.** The mode machine, the watchdog, the CAN handling and every limit the package assumes exist only in upstream's description; the repository holds a KiCad project and a device tree overlay for the board, nothing that runs | `electrical/motion_control/` (board sources, `mcb-io.dts`, `scripts/serial.sh`); README roadmap | 13849-1 §7; 61508-3 §7 | High |
| GAP-17 | **The locomotion policy is unreleased.** Its training data, randomisation, simulation-to-real evidence and behaviour on hardware are undefined; the DFMEA rates a policy out-of-distribution scenario at severity 9 with detection 7 (FM-28) | README roadmap; package `12_Gaps` GAP-LP-01; DFMEA FM-28 | TR 5469 §8–§10; 13482 §5.6 | High |
| GAP-18 | **The Asimov API contract is pre-1.0 and unstable.** The interface the operator app uses to command the robot is marked as upcoming; a contract change can change how a command is interpreted (FM-32) | README roadmap; package `12_Gaps` GAP-API-01; DFMEA FM-32 | 13849-1 §7; 62443-4-1 SR-5 | Medium |
| GAP-19 | **The tele-operation authentication scheme is not documented.** Commands arrive over a WebRTC data channel; nothing states how an operator is authenticated, how a session is bound, or how replay is prevented (FM-15, severity 9) | package `12_Gaps` GAP-CYB-01; DFMEA FM-15; package `03_ItemDef` information boundaries | 62443-4-2 CR 1.1, CR 3.1; 13482 §5.18 | High |
| GAP-20 | **The wireless E-stop link and the UART debug port have no documented protection.** The link's technology and encryption are unknown; the motion control board exposes a UART TTL debug port by design | package `13_Assumptions` OI-03; `electrical/README.md` (debug port) | 62443-4-2 CR 2.13, CR 3.8 | Medium |
| GAP-21 | **The simulation model is the only dynamics data and is not pinned to any hardware revision.** The MuJoCo model carries the joint ranges, masses and control limits the policy is trained with; nothing ties it to a CAD or board revision, and the package's FMEA rates the sim-to-real gap at severity 8, occurrence 5 | `sim-model/xmls/asimov.xml`; `sim-model/README.md`; package `08_FMEA` sim model row | 13849-2 §5; TR 5469 §9 | Medium |

## 7. Hardware record (electrical, mechanical, harness)

| ID | Finding | Evidence | Standard | Severity |
|---|---|---|---|---|
| GAP-22 | **The CAN harness depends on DIY crimp quality and termination with no acceptance criterion.** Six buses carry every actuator command; a missing terminator or a poor crimp is a bus-off and the loss of a leg (FM-11 severity 9, FM-18 occurrence 5) | `electrical/wiring/wiring.yaml`; `electrical/README.md` (C4 cabling note); DFMEA FM-11, FM-18 | 13849-1 §6; 60204-1 §13 | Medium |
| GAP-23 | **No under-voltage lockout or power-good specification.** A 5 V brown-out resets the motion control board silently; a mid-stride power loss is an uncontrolled fall (FM-31, HZ-P03) | DFMEA FM-17, FM-31; package `06_Hazards` HZ-P03 | 13849-1 §6 (behaviour on power loss); 60204-1 §7.5 | Medium |
| GAP-24 | **No mechanical BOM, torque table or threadlocker specification in the repository.** The CAD names fabrication groups (ALU_7075, MJF_PA12, SML_316L, OFF_THE_SHELF) but no part list, fastener torque or locking compound; the manual BOM page returns 404 | `mechanical/README.md`; `mechanical/ASV1/*/FABRICATION/`; DFMEA FM-03 | 12100 §6.4; 13849-1 §12; Machinery Reg. Annex IV | Medium |
| GAP-25 | **No stator thermistor cut-off or head-shell thermal validation documented.** Actuator over-temperature (FM-08) and the Raspberry Pi 5 in the head shell (FM-29) rest on assumed design margins | DFMEA FM-08, FM-29; package `06_Hazards` HZ-T01 | 12100 §6.2; 60204-1 §7.3 | Medium |
| GAP-26 | **Guarding gaps at the waist and neck yaw are unverified.** The package requires gaps of at most 4 mm (SYRS-029) but nothing in the CAD record or the manual shows a guard or a measurement | package requirements SYRS-029; DFMEA FM-27; package `06_Hazards` HZ-M05 | 13857 §4; 13482 §5.4 | Medium |

## 8. Quality and process (ISO 9001 informative, ASPICE)

| ID | Finding | Evidence | Standard | Severity |
|---|---|---|---|---|
| GAP-27 | **Records of test, calibration and nonconformance are not maintained** | package `12_Gaps` GAP-9001-01 | ISO 9001 §7.5 (informative); 61508-1 §6.2 | Medium |
| GAP-28 | **Design review and design verification records are absent** | package `12_Gaps` GAP-9001-02 | ISO 9001 §8.3 (informative); 13849-1 §8 | Medium |
| GAP-29 | **Production process controls are undeclared for the DIY-kit assembly** | package `12_Gaps` GAP-9001-03 | ISO 9001 §8.5.1 (informative); Machinery Reg. Annex III §1.7.4 | Medium |
| GAP-30 | **No nonconformance procedure** | package `12_Gaps` GAP-9001-04 | ISO 9001 §8.7 (informative); 61508-1 §6.2 | Medium |
| GAP-31 | **No internal audit or monitoring** | package `12_Gaps` GAP-9001-05 | ISO 9001 §9.1 (informative) | Low |
| GAP-32 | **No corrective-action system** | package `12_Gaps` GAP-9001-06 | ISO 9001 §10.2 (informative) | Low |
| GAP-33 | **The concept-phase package is unreviewed, AI-assisted and outside the record's conventions.** Nine documents at the repository root with no document-control header, no baseline commit, no reviewer, no CI check; its own control sheet lists every approval as "to be filled"; its folder index names sub-folders that do not exist | `concept-package/README.md` (paths `safety-case/`, `dfmea/`, …); workbook `02_DocCtrl`; DFMEA `01_Document_Control` | 13849-1 §12; 61508-1 §6.2; Machinery Reg. Annex IV | Medium |
| GAP-34 | **Process capability (estimated):** SUP.8 at CL1 on upstream's git and pull-request practice; MAN.3, SYS.1–SYS.3, SWE.1–SWE.6, HWE.1–HWE.4, VAL.1 at CL0 (no requirements, architecture, code, tests or analyses in any repository); the fork's package raises nothing above CL0 because it is unreviewed and uncontrolled | upstream commit history; package control sheets | ASPICE PAM 4.0; 61508-1 §6 | Medium |

## 9. Existing strengths to build on

- **The architecture is the right shape.** A dedicated motion control board sits between the edge board and the
  actuators, with its own IMU and six CAN buses, so a deterministic safety layer has a place to live and a hardwired
  stop chain can remove the motor rail upstream of every actuator.
- **The hardware record is open and buildable.** CAD for every subassembly as STEP with a naming convention, a
  KiCad board with LCSC part IDs for direct fabrication, a WireViz harness with every connector and pin label, and a
  MuJoCo model with 25 actuated joints; CERN-OHL-S-2.0 and GPL-2.0 licences.
- **Upstream is honest about what is not there.** The roadmap marks the API, the policy and the app as upcoming;
  the kit table says the battery is not included; nothing claims the robot is safe.
- **The concept-phase package is a complete first pass.** Thirty-two hazards from two catalogues, a HARA with the
  risk graph read per row, 25 safety functions with targets, a DFMEA with 32 failure modes and an action plan,
  120 requirements traced to hazards, functions, failure modes, gaps and test cases, 139 test cases with two
  validation matrices, and a gap register that already names most of what this assessment names. It is the seed of
  WP-C-03, WP-C-04, WP-A-01, WP-H-03, WP-S-02 and WP-V-01.
- **The package already knows its worst problems.** It calls DAMP a hazard, rates the missing BMS as undetectable,
  gives provisional acceptance to the laboratory envelope only, and lists the policy as "a blank cheque".

## 10. Priority actions (feed into the G0/G1 plan)

1. **Decide the frame, the envelopes and the reference configuration** (register DQ-001, DQ-002, DQ-003): EU
   machinery frame, OE-1 laboratory only, the kit robot as published, tethered and bench-powered. Everything below
   assumes those answers.
2. **Decide the safe state and the policy position** (DQ-005, DQ-006): a controlled descent as the safe state, and
   no safety function on the learned policy until it is public. These two decisions fix SF-01, SF-02, SF-08, the
   E-stop's stop category and the fall-arrest budget.
3. **Buy or build the laboratory complementary measures before any powered floor test** (DQ-007, DQ-008): a gantry
   and rated tether sized for a 35 kg dynamic load, a wired dual-channel E-stop in the operator's hand that removes
   the motor rail, a bench supply in place of a battery, a cleared and marked area. This is bench equipment, not the
   product design; it is what makes the next months of testing defensible ([WP-V-07](../06-validation/WP-V-07-test-operations.md)).
4. **Port the package into the record** (GAP-33): hazards and safety functions into WP-C-03 and WP-C-04 (done at
   v0.1), the DFMEA into WP-H-03 and WP-A-01, the requirements into WP-S-01, WP-S-02, WP-H-01 and WP-W-02, the test
   plan into WP-V-01, each under document control and review.
5. **Weigh the robot and bound the fall** (GAP-03, GAP-04): mass, centre of gravity, tip-over margin, fall energy;
   the hip-yoke FEA and material certificates the DFMEA asks for.
6. **Specify the stop chain** (GAP-07, GAP-08, GAP-11): E-stop devices, a surveilled wireless receiver, motor-rail
   contactors, a power distribution board with a fuse table and a disconnection device, the BMS handshake interlock
   (DQ-009); map SF-13, SF-08 and SF-15 onto it and record the open items as defeaters.
7. **Specify the safety layer ahead of the firmware** (GAP-16): WP-W-02 and WP-W-03 against the interface the
   manual describes, so that upstream's firmware, when it arrives, is assessed against a specification rather than
   read for one.
8. **Ask upstream for reliability data and the plan documents** (GAP-14, GAP-07): actuator and encoder failure
   rates, the E-stop design, the mode-machine specification; record their absence as the fork's design input.
9. **Set the limits and the security target** (DQ-012, DQ-014): joint torque and velocity limits the firmware
   enforces, and the security level for the tele-operation channel.
10. **Build the Living Safety Case tooling** and register GAP-01…GAP-34 as the first defeaters against the
    top-level claim (done at v0.1).
