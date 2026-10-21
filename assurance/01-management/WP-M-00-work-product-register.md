# WP-M-00 Work Product Register

| Field | Value |
|---|---|
| Work product | WP-M-00 Work product register |
| Standard reference | ISO 13849-1:2023 §4 (planning of the SRP/CS development); IEC 62061:2021 §5 (management of functional safety, documentation); IEC 61508-1:2010 §6 (management of functional safety); Regulation (EU) 2023/1230 Annex IV (technical documentation, as the index it needs); ASPICE 4.0 MAN.3 (define work products), SUP.8 (configuration items) |
| Version | 0.1 (initial register: gates, 89 work products, clause map; 2026-10-21) |
| Status | Draft |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `3d4ec9d` (fork head, BL-001: the inherited repository and the concept-phase package) |

## 1. Purpose

This register lists every work product the Asimov v1 assurance path requires. For each one it records the source
clauses, the gate that needs it, and its current status. The [safety plan (WP-M-02)](WP-M-02-safety-plan.md) refers to
this register as its list of work products, and [configuration management (WP-P-01)](../07-supporting/WP-P-01-configuration-management-plan.md)
puts each entry under configuration control. The [technical documentation index (WP-K-02)](../10-safety-case/WP-K-02-technical-documentation-index.md)
maps these work products onto the technical documentation that Regulation (EU) 2023/1230 Annex IV requires.

Tailoring decisions are recorded in [WP-M-01 §5](WP-M-01-assurance-strategy.md#5-tailoring). If a work product is
tailored out, it stays in this register with status `N/A (tailored)` and a reference to its rationale.

Asimov v1 is a machine: a 35 kg, 1.2 m bipedal humanoid with 25 actuated joints, built from an open hardware record.
The columns name the machinery and robot standards ([WP-M-01 §4](WP-M-01-assurance-strategy.md#4-the-standards-and-how-each-one-is-used)
explains how each one is used). The concept-phase package the fork already holds
([`00-assessment/concept-package/`](../00-assessment/concept-package/README.md): safety-case workbook, DFMEA,
requirements, test plan, architecture) is the seed of the work products below, not a work product itself; the
[gap assessment](../00-assessment/gap-assessment.md) says what it covers and what it does not.

> [!NOTE]
> Clause numbers are given for the editions named in [WP-M-01 §4](WP-M-01-assurance-strategy.md#4-the-standards-and-how-each-one-is-used).
> ISO 13849-1:2023 renumbered its clauses against the 2015 edition (software is now §7, verification §8, validation
> §10, documentation §12, information for use §13). ISO 10218-1/-2 were revised in 2025 and absorb most of
> ISO/TS 15066; the 2011 editions cited by the concept-phase package are kept until the lead decides the edition
> (decision register). The standards are not available in the drafting environment; every clause reference must be
> checked against a licensed copy before an audit ([WP-M-06](WP-M-06-confirmation-measures-plan.md) OI-1).

## 2. Gates

| Gate | Name | Exit criterion (summary) |
|---|---|---|
| G0 | Governance | Plans approved; roles assigned; configuration and change control running |
| G1 | Concept | Machine limits, operating envelopes, risk assessment, safety functions with their required PL, risk reduction concept, cybersecurity and ML concepts approved; confirmation review of the risk assessment passed |
| G2 | System design | Safety requirements specification, safety-related control architecture with categories and diagnostics, response-time and fall-arrest budget, mechanical and stability analysis and system-level analyses approved |
| G3 | HW/SW development | Safety-chain hardware and PL calculation, software requirements, architecture, units and unit verification approved for every safety-related part |
| G4 | Integration and verification | Hardware, software and system integration and PL verification complete; stability, fall, E-stop and detection tests passed; fault-injection campaign closed |
| G5 | Validation and release | Safety validation on the robot, cybersecurity validation, safety case, functional safety assessment and technical documentation complete; release record signed |
| G6 | Operation | Field monitoring, incident response and update processes running |

## 3. Register

Column legend. **Machinery**: ISO 12100:2010 (risk assessment and reduction), ISO 10218-1:2011/-2:2011 and
ISO/TS 15066:2016 (industrial robots, collaborative operation, power and force limiting), ISO 13482:2014 (personal
care robots, for the home and public operating envelopes), ISO 13850:2015 (emergency stop), ISO 13857:2019 (safety
distances, reach). **SRP/CS**: ISO 13849-1:2023 and ISO 13849-2:2012 (safety-related parts of control systems),
IEC 62061:2021 and IEC 61508:2010 where 13849 runs out (software, management, assessment). **IEC 62443**:
62443-4-1:2018 (secure development lifecycle practices SM, SR, SD, SI, SVV, DM, SUM, SG) and 62443-4-2:2019
(component requirements CR/EDR, security levels). **Other**: IEC 60204-1:2018, IEC 62133-2:2017 (lithium cells and
batteries), ISO/IEC TR 5469:2024 (AI in safety functions), ISO 9001:2015 (informative, quality management),
Regulation (EU) 2023/1230 (Machinery Regulation), Regulation (EU) 2024/1689 (AI Act), UL 4600, IEC 60812, IEC 61025,
ISO 21448 (used as a method). **ASPICE**: process IDs from ASPICE PAM 4.0, used as the process capability frame
([WP-M-01 §5](WP-M-01-assurance-strategy.md#5-tailoring) T-12). **Status**: S = Skeleton, D = Draft, R = In review,
A = Approved, B = Baselined, N/A = tailored out.

### 3.1 Management (`01-management/`)

| ID | Work product | Machinery | SRP/CS | IEC 62443 | Other | ASPICE | Gate | Status |
|---|---|---|---|---|---|---|---|---|
| [WP-M-00](WP-M-00-work-product-register.md) | Work product register | | 13849-1 §4; 62061 §5 | | Machinery Reg. Annex IV (index) | MAN.3 | G0 | D |
| [WP-M-01](WP-M-01-assurance-strategy.md) | Assurance strategy and lifecycle tailoring | 12100 §4 | 13849-1 §4; 61508-1 §6 | 62443-4-1 SM-1 | TR 5469 (AI lifecycle), UL 4600 (safety case), Machinery Reg. Art. 25 | MAN.3 | G0 | D |
| [WP-M-02](WP-M-02-safety-plan.md) | Functional safety plan | 12100 §4 | 13849-1 §4; 62061 §5; 61508-1 §6 | | | MAN.3 | G0 | D |
| [WP-M-03](WP-M-03-project-plan.md) | Project plan (scope, WBS, schedule, resources) | | | | | MAN.3 | G0 | S |
| [WP-M-04](WP-M-04-organization-competence-safety-culture.md) | Organization-specific rules, safety culture, competence management | | 61508-1 §6.2 (competence); 13849-1 §4 | 62443-4-1 SM-4 | | — | G0 | S |
| [WP-M-05](WP-M-05-quality-assurance-plan.md) | Quality management and quality assurance plan (design control, records, nonconformance) | | 61508-1 §6.2 | 62443-4-1 SM-5 | ISO 9001 §7.5, §8.3, §8.7, §10.2 (informative) | SUP.1 | G0 | S |
| [WP-M-06](WP-M-06-confirmation-measures-plan.md) | Confirmation measures plan (reviews, validation independence, functional safety assessment, conformity assessment) | | 13849-1 §8, §10; 61508-1 §8 | 62443-4-1 SM-13 | Machinery Reg. Art. 25, Annexes VI–X | — | G0 | D |
| [WP-M-07](WP-M-07-risk-management.md) | Project risk management plan and register | | | | | MAN.5 | G0 | S |
| [WP-M-08](WP-M-08-cybersecurity-plan.md) | Cybersecurity plan | | | 62443-4-1 §5 (SM-1…SM-13); 62443-4-2 §4 | | MAN.7 (CS) | G0 | S |
| [WP-M-09](WP-M-09-ml-safety-plan.md) | Machine-learning safety plan (learned locomotion policy, perception) | | | | TR 5469 (AI technology classes, usage levels); AI Act Art. 9 | MLE.1–4 | G0 | S |
| [WP-M-10](WP-M-10-upstream-and-supplier-management.md) | Upstream (Asimov Inc) and supplier management (kit, actuators, battery) | | 61508-1 §6.2 (subcontracted activities) | 62443-4-1 SM-9, SM-10 | | ACQ.4 | G0 | S |
| [WP-M-11](WP-M-11-impact-analysis.md) | Impact analysis of the inherited Asimov v1 baseline and the concept-phase package (modification of existing machinery) | 12100 §4 | 61508-1 §7.16 (modification) | 62443-4-1 SM-3 | Machinery Reg. Art. 3 (substantial modification) | SUP.10 | G0 | S |
| [WP-M-12](WP-M-12-process-capability-baseline.md) | Process capability baseline (ASPICE self-assessment) | | | | | All in scope | G0 | S |
| [WP-M-13](WP-M-13-regulatory-conformity-strategy.md) | Regulatory conformity strategy (Machinery Regulation, AI Act, US frame) | | | | Machinery Reg. Art. 25, Annex I, Annexes VI–X; AI Act Art. 6, Art. 43, Annex I | — | G0 | D |

### 3.2 Concept phase (`02-concept/`)

| ID | Work product | Machinery | SRP/CS | IEC 62443 | Other | ASPICE | Gate | Status |
|---|---|---|---|---|---|---|---|---|
| [WP-C-01](../02-concept/WP-C-01-item-definition.md) | Item definition and limits of the machinery (intended use, foreseeable misuse, use, space and time limits) | 12100 §5.3; 10218-1 §3, §5; 13482 §4 | 13849-1 §5 (inputs) | 62443-4-1 SR-1 | Machinery Reg. Annex III §1.1.2 | SYS.1 | G1 | D |
| [WP-C-02](../02-concept/WP-C-02-operating-environment-and-tasks.md) | Operating environment and task specification (operating envelopes OE-1…OE-4, floors, people, tether) | 12100 §5.3; 13482 §5.2; 10218-2 §5 | | | ISO 21448 §5 (informative method) | SYS.1 | G1 | D |
| [WP-C-03](../02-concept/WP-C-03-risk-assessment.md) | Hazard identification and risk assessment (hazard list, risk estimation and evaluation) | 12100 §5.4–§5.6, Annex B; 13482 Annex A; 10218-1 Annex A | 13849-1 Annex A (risk graph inputs) | | Machinery Reg. Annex III §1 | — | G1 | D |
| [WP-C-04](../02-concept/WP-C-04-safety-functions-and-plr.md) | Safety functions specification with required Performance Level, stop category and response time | 10218-1 §5.4, §5.5; 13482 §5.16, §6; 13850 §4 | 13849-1 §5, Annex A (PLr) | | 60204-1 §9.2 (stop categories) | SYS.2 | G1 | D |
| [WP-C-05](../02-concept/WP-C-05-risk-reduction-concept.md) | Risk reduction concept (three-step method: inherently safe design, safeguarding, information for use) | 12100 §6; 13482 §6; 10218-1 §5 | 13849-1 §5 | | Machinery Reg. Annex III §1.1.2 | SYS.2 | G1 | S |
| [WP-C-06](../02-concept/WP-C-06-human-robot-interaction-and-misuse.md) | Human-robot interaction, collaborative operation, contact limits and reasonably foreseeable misuse analysis | 10218-2 §5; TS 15066 §5; 13482 §5.7, §5.8; 12100 §5.3 | | | ISO 13857 §4 | — | G1 | S |
| [WP-C-07](../02-concept/WP-C-07-cybersecurity-threat-and-risk-assessment.md) | Cybersecurity threat and risk assessment (tele-operation channel, API, update path) | | | 62443-4-1 SR-2; 62443-3-2 §5 | | SEC.1 | G1 | S |
| [WP-C-08](../02-concept/WP-C-08-cybersecurity-requirements-and-sl-target.md) | Cybersecurity requirements and security level target | | | 62443-4-1 SR-3…SR-5; 62443-4-2 CR 1–7, SL-T | | SEC.1 | G1 | S |
| [WP-C-09](../02-concept/WP-C-09-ml-component-definition-and-safety-requirements.md) | ML component definition and safety requirements (locomotion policy, perception models) | | | | TR 5469 §6–§8 (classes, usage levels, properties); AI Act Annex IV | MLE.1 | G1 | S |
| [WP-C-10](../02-concept/WP-C-10-functional-insufficiency-analysis.md) | Functional insufficiency analysis of perception and the locomotion policy (performance limits, triggering conditions) | 13482 §5.6, §5.10; 12100 §5.4 | | | ISO 21448 §6–§7 (informative method) | — | G1 | S |

### 3.3 System level (`03-system/`)

| ID | Work product | Machinery | SRP/CS | IEC 62443 | Other | ASPICE | Gate | Status |
|---|---|---|---|---|---|---|---|---|
| [WP-S-01](../03-system/WP-S-01-system-requirements.md) | System requirements specification (functional, non-safety) | | | | | SYS.2 | G2 | S |
| [WP-S-02](../03-system/WP-S-02-safety-requirements.md) | Safety requirements specification for the SRP/CS | 10218-1 §5.4; 13482 §6 | 13849-1 §5; 62061 §6 | | 60204-1 §9 | SYS.2 | G2 | S |
| [WP-S-03](../03-system/WP-S-03-technical-safety-concept.md) | Technical safety concept: stop chain and safety-related control architecture (E-stop and motor-rail removal, the MCB safety layer, designated architectures, categories, channels, diagnostics, allocation of SF-01…SF-25) | 10218-1 §5.4, §5.5 | 13849-1 §6 | | 60204-1 §9.4 | SYS.3 | G2 | S |
| [WP-S-04](../03-system/WP-S-04-response-time-and-stopping-budget.md) | Response time, fall-arrest and stopping budget (controlled descent, joint stop, safe state per mode) | 13482 §5.10, §5.13 | 13849-1 §5 (response time) | | | SYS.3 | G2 | S |
| [WP-S-05](../03-system/WP-S-05-safety-chain-io-interface.md) | Hardware-software interface of the safety chain (I/O map, CAN buses, E-stop receiver, BMS handshake, signal semantics) | | 13849-1 §6, §7 | | | SYS.3 | G2 | S |
| [WP-S-06](../03-system/WP-S-06-requirements-installation-operation.md) | Requirements for installation, operation, maintenance and decommissioning | 12100 §6.4; 13482 §7 | 13849-1 §11 | 62443-4-1 SG-1…SG-7 | | SYS.2 | G2 | S |
| [WP-S-07](../03-system/WP-S-07-cybersecurity-architecture.md) | Cybersecurity architecture (zones, conduits, controls) | | | 62443-4-1 SD-1…SD-4; 62443-3-3 §5 | | SEC.1, SYS.3 | G2 | S |
| [WP-S-08](../03-system/WP-S-08-system-integration-test.md) | System integration and test strategy, specification and report | | 13849-1 §8 | 62443-4-1 SVV-1 | | SYS.4 | G4 | S |
| [WP-S-09](../03-system/WP-S-09-system-verification.md) | System verification: PL verification and fault behaviour | | 13849-1 §8; 13849-2 §4–§5 | | 60204-1 §18 | SYS.5 | G4 | S |

### 3.4 Hardware: electrical and mechanical (`04-hardware/`)

| ID | Work product | Machinery | SRP/CS | IEC 62443 | Other | ASPICE | Gate | Status |
|---|---|---|---|---|---|---|---|---|
| [WP-H-01](../04-hardware/WP-H-01-hardware-safety-requirements.md) | Hardware safety requirements (E-stop chain, motor-rail contactor, BMS interlock, thermistors, encoders) | 10218-1 §5.4; 13482 §5.16 | 13849-1 §5, §6 | | 60204-1 §9.2 | HWE.1 | G3 | S |
| [WP-H-02](../04-hardware/WP-H-02-electrical-and-safety-chain-design.md) | Electrical and safety-chain design (motion control board, power distribution, harness, E-stop receiver, wiring) | | 13849-1 §6 | 62443-4-2 CR 2.13 (physical) | 60204-1 §5–§13 | HWE.2 | G3 | S |
| [WP-H-03](../04-hardware/WP-H-03-hardware-failure-analysis.md) | Hardware failure analysis (FMEA, fault lists, fault exclusions; seeded by the concept-package DFMEA) | | 13849-1 §6; 13849-2 Annex A–D | | IEC 60812 | HWE.2 | G3 | S |
| [WP-H-04](../04-hardware/WP-H-04-reliability-data-and-pl-calculation.md) | Reliability data and PL calculation (MTTFD, DCavg, CCF, SISTEMA) | | 13849-1 §6, Annex C–F, Annex K | | | — | G3 | S |
| [WP-H-05](../04-hardware/WP-H-05-electrical-safety.md) | Electrical and battery safety: supply disconnection, overcurrent protection, insulation, the lithium pack and its BMS, charger | | | | 60204-1 §5–§8, §18; 62133-2; UN 38.3 | — | G3 | S |
| [WP-H-06](../04-hardware/WP-H-06-hardware-integration-verification.md) | Hardware integration and verification specification and report | | 13849-1 §8 | | 60204-1 §18 | HWE.3, HWE.4 | G4 | S |
| [WP-H-07](../04-hardware/WP-H-07-safety-component-qualification.md) | Qualification of safety components (E-stop devices and receiver, contactors, BMS, actuators, encoders, well-tried components) | | 13849-1 §6 (well-tried components); 13849-2 Annex A–D; 62061 §7 (subsystems) | | 62133-2 (pack certificate) | — | G3 | S |
| [WP-H-08](../04-hardware/WP-H-08-mechanical-and-stability-analysis.md) | Mechanical, structural and stability analysis (mass, centre of gravity, tip-over, fall energy, fatigue of the hip yoke, pinch and crush points, guarding) | 12100 §5.3, §6.2; 13482 §5.4, §5.13; 10218-1 §5.10 | | | ISO 13857; Machinery Reg. Annex III §1.3 | — | G2 | S |

### 3.5 Software level (`05-software/`)

| ID | Work product | Machinery | SRP/CS | IEC 62443 | Other | ASPICE | Gate | Status |
|---|---|---|---|---|---|---|---|---|
| [WP-W-01](../05-software/WP-W-01-software-development-environment-guidelines.md) | SW development environment, languages and coding guidelines | | 13849-1 §7; 61508-3 §7.4.4 | 62443-4-1 SI-1, SI-2 | MISRA C:2012 (firmware) | SWE.3 | G3 | S |
| [WP-W-02](../05-software/WP-W-02-software-safety-requirements.md) | Software safety requirements specification (SRESW, SRASW) | | 13849-1 §7; 61508-3 §7.2 | | | SWE.1 | G3 | S |
| [WP-W-03](../05-software/WP-W-03-software-architecture.md) | Software architectural design (MCB safety layer and mode machine, separation from the locomotion policy and the tele-operation stack) | | 13849-1 §7; 61508-3 §7.4.3 | 62443-4-1 SD-2 | | SWE.2 | G3 | S |
| [WP-W-04](../05-software/WP-W-04-software-safety-analysis.md) | Software safety analysis | | 13849-1 §7; 61508-3 §7.4.3 | | IEC 60812 (software FMEA) | SWE.2 | G3 | S |
| [WP-W-05](../05-software/WP-W-05-software-unit-design.md) | Software unit design and implementation | | 13849-1 §7; 61508-3 §7.4.5, §7.4.6 | 62443-4-1 SI-1 | | SWE.3 | G3 | S |
| [WP-W-06](../05-software/WP-W-06-software-unit-verification.md) | Software unit verification specification and report (static analysis, tests, coverage) | | 13849-1 §7, §8; 61508-3 §7.4.7 | 62443-4-1 SVV-1 | | SWE.4 | G3 | S |
| [WP-W-07](../05-software/WP-W-07-software-integration-verification.md) | Software integration and verification specification and report | | 13849-1 §7, §8; 61508-3 §7.5 | | | SWE.5 | G4 | S |
| [WP-W-08](../05-software/WP-W-08-software-validation-on-target.md) | Software validation on the target (MCB bench, hardware-in-the-loop with the MuJoCo model) | | 13849-1 §10; 61508-3 §7.7 | | | SWE.6 | G4 | S |
| [WP-W-09](../05-software/WP-W-09-safety-parameters-and-configuration-data.md) | Safety-related parameters and configuration data (joint torque and velocity limits, watchdog timeouts, PFL thresholds, mode limits) | 13482 §5.10; TS 15066 §5.5 | 13849-1 §7 (parameterization) | 62443-4-2 CR 3.4 | | SWE.3 | G3 | S |
| [WP-W-10](../05-software/WP-W-10-ml-engineering.md) | ML engineering: data, training, simulation-to-real transfer, testing and deployment of the locomotion policy | | | | TR 5469 §8–§10; AI Act Art. 10, Art. 15 | MLE.1–4, SUP.11 | G3 | S |
| [WP-W-11](../05-software/WP-W-11-cybersecurity-implementation-verification.md) | Cybersecurity implementation and verification | | | 62443-4-1 SI-1, SI-2, SVV-1…SVV-4; 62443-4-2 CR | | SEC.2, SEC.3 | G3 | S |

### 3.6 Validation (`06-validation/`)

| ID | Work product | Machinery | SRP/CS | IEC 62443 | Other | ASPICE | Gate | Status |
|---|---|---|---|---|---|---|---|---|
| [WP-V-01](../06-validation/WP-V-01-safety-validation.md) | Safety validation plan, specification and report | 13482 §7; 10218-1 §6 | 13849-1 §10; 13849-2 §4 | | 60204-1 §18 | VAL.1 | G5 | S |
| [WP-V-02](../06-validation/WP-V-02-stopping-braking-stability-tests.md) | Stability, fall and controlled-descent tests (tip-over, external load, loss of power, stop from each mode) | 13482 §5.13, §7; 12100 §5.3 | | | | VAL.1 | G4 | S |
| [WP-V-03](../06-validation/WP-V-03-personnel-detection-validation.md) | Human detection, speed reduction and power-and-force limiting validation | 10218-2 §5; TS 15066 §5.5; 13482 §5.7, §7 | 13849-1 §10 | | ISO 13857 | VAL.1 | G4 | S |
| [WP-V-04](../06-validation/WP-V-04-emergency-stop-and-safety-chain-validation.md) | Emergency stop and safety-chain validation (wired and wireless devices, link loss, re-arm) | 13850 §4; 13482 §5.16 | 13849-2 §5 | | 60204-1 §9.2, §18 | VAL.1 | G4 | S |
| [WP-V-05](../06-validation/WP-V-05-fault-injection.md) | Fault injection and fault-list validation specification and report | | 13849-2 §5, Annex A–D | | | SYS.4, SWE.6 | G4 | S |
| [WP-V-06](../06-validation/WP-V-06-cybersecurity-validation.md) | Cybersecurity validation and penetration testing | | | 62443-4-1 SVV-3, SVV-4 | | SEC.4 | G5 | S |
| [WP-V-07](../06-validation/WP-V-07-test-operations.md) | Test operations and safety procedures for powered testing (hold point: tether, gantry, E-stop, cleared area) | 12100 §6.4; 13482 §7; 10218-2 §5 | | | | VAL.1 | G1 | D |
| [WP-V-08](../06-validation/WP-V-08-unknown-scenarios-and-field-trials.md) | Evaluation of unknown scenarios and field trials | 13482 §7 | | | ISO 21448 §11 (informative) | VAL.1 | G5 | S |

### 3.7 Supporting processes (`07-supporting/`)

| ID | Work product | Machinery | SRP/CS | IEC 62443 | Other | ASPICE | Gate | Status |
|---|---|---|---|---|---|---|---|---|
| [WP-P-01](../07-supporting/WP-P-01-configuration-management-plan.md) | Configuration management plan (safety-relevant file list, baselines of the fork, the kit and the firmware) | | 61508-1 §6.2.3; 13849-1 §12 | 62443-4-1 SM-6, SM-7 | | SUP.8 | G0 | S |
| [WP-P-02](../07-supporting/WP-P-02-change-management.md) | Change management plan | | 61508-1 §7.16 | 62443-4-1 SM-3 | | SUP.10 | G0 | S |
| [WP-P-03](../07-supporting/WP-P-03-problem-resolution.md) | Problem resolution management | | 61508-1 §6.2 (anomaly handling) | 62443-4-1 DM-1…DM-6 | | SUP.9 | G0 | S |
| [WP-P-04](../07-supporting/WP-P-04-documentation-management.md) | Documentation management | 12100 §7 | 13849-1 §12 | 62443-4-1 SG-1 | Machinery Reg. Annex IV | SUP.7 | G0 | S |
| [WP-P-05](../07-supporting/WP-P-05-verification-review-procedure.md) | Verification and review procedure | | 13849-1 §8; 61508-1 §7.18 | 62443-4-1 SVV-1 | | SUP.2 | G0 | S |
| [WP-P-06](../07-supporting/WP-P-06-requirements-management-traceability.md) | Requirements management and traceability procedure | | 13849-1 §5; 61508-3 §7.2 | 62443-4-1 SR-5 | | SYS.2, SWE.1 | G0 | S |
| [WP-P-07](../07-supporting/WP-P-07-tool-classification-qualification.md) | Software tool classification and qualification | | 61508-3 §7.4.4 (T1–T3); 13849-1 §7 | 62443-4-1 SM-7 | | — | G3 | S |
| [WP-P-08](../07-supporting/WP-P-08-software-component-qualification.md) | Qualification of software components (RT kernel, CAN stack, WebRTC, MuJoCo, policy runtime, third-party) | | 61508-3 §7.4.2.12 | 62443-4-1 SM-9, SM-10 | | — | G3 | S |
| [WP-P-09](../07-supporting/WP-P-09-proven-in-use.md) | Proven-in-use argument evaluation | | 61508-2 §7.4.10; 61508-3 §7.4.2.12 | | | — | G3 | S |
| [WP-P-10](../07-supporting/WP-P-10-release-management.md) | Release management and baseline procedure | | 61508-1 §6.2.3 | 62443-4-1 SUM-1…SUM-5 | Machinery Reg. Annex V | SUP.8 | G5 | S |
| [WP-P-11](../process/README.md) | Integrated process model and generated process maps (all phases G0–G6 modelled) | 12100 §4 | 13849-1 §4; 61508-1 §6 | 62443-4-1 SM-1 | TR 5469 (AI lifecycle) | MAN.3 | G0 | D |

### 3.8 Safety analyses (`08-analyses/`)

| ID | Work product | Machinery | SRP/CS | IEC 62443 | Other | ASPICE | Gate | Status |
|---|---|---|---|---|---|---|---|---|
| [WP-A-01](../08-analyses/WP-A-01-system-fmea.md) | System FMEA (seeded by the concept-package system FMEA and DFMEA) | | 13849-1 §6 | | IEC 60812 | — | G2 | S |
| [WP-A-02](../08-analyses/WP-A-02-fault-tree-analysis.md) | Fault tree analysis, one tree per safety function | | 13849-1 §6 | | IEC 61025 | — | G2 | S |
| [WP-A-03](../08-analyses/WP-A-03-common-cause-failure-analysis.md) | Common cause failure analysis | | 13849-1 §6, Annex F | | | — | G2 | S |
| [WP-A-04](../08-analyses/WP-A-04-stpa.md) | System-theoretic process analysis (STPA) of the motion control chain (tele-operation, policy, MCB, actuators) | 12100 §5.4 | | | STPA Handbook 2018 | — | G2 | S |
| [WP-A-05](../08-analyses/WP-A-05-independence-of-the-safety-chain.md) | Independence of the safety chain from the policy and tele-operation stack (freedom from interference) | | 13849-1 §6, §7; 61508-3 Annex F | 62443-3-3 §5 (zoning) | | — | G2 | S |

### 3.9 Production, operation and decommissioning (`09-production-operation/`)

| ID | Work product | Machinery | SRP/CS | IEC 62443 | Other | ASPICE | Gate | Status |
|---|---|---|---|---|---|---|---|---|
| [WP-O-01](../09-production-operation/WP-O-01-assembly-installation-commissioning.md) | Assembly, installation and commissioning instructions (the DIY kit build, acceptance checks) | 12100 §6.4; 13482 §7 | | | Machinery Reg. Annex III §1.7.4; ISO 9001 §8.5.1 (informative) | — | G5 | S |
| [WP-O-02](../09-production-operation/WP-O-02-operation-maintenance-decommissioning.md) | Operation, maintenance and decommissioning | 12100 §6.4; 13482 §7 | 13849-1 §11 | 62443-4-1 SG-1…SG-7 | | — | G5 | S |
| [WP-O-03](../09-production-operation/WP-O-03-information-for-use.md) | Information for use, markings and warnings | 12100 §6.4; 13482 §7.2 | 13849-1 §13 | | Machinery Reg. Annex III §1.7 | — | G5 | S |
| [WP-O-04](../09-production-operation/WP-O-04-field-monitoring.md) | Field monitoring and incident reporting | | 61508-1 §7.15 | 62443-4-1 DM-1 | Machinery Reg. Art. 10; AI Act Art. 72 | — | G6 | S |
| [WP-O-05](../09-production-operation/WP-O-05-cybersecurity-incident-response-updates.md) | Cybersecurity incident response, vulnerability management and software updates | | | 62443-4-1 DM-1…DM-6, SUM-1…SUM-5 | | SEC.* | G6 | S |

### 3.10 Safety case, assessment and conformity (`10-safety-case/`)

| ID | Work product | Machinery | SRP/CS | IEC 62443 | Other | ASPICE | Gate | Status |
|---|---|---|---|---|---|---|---|---|
| [WP-K-01](../10-safety-case/WP-K-01-safety-case.md) | Safety case (claims, arguments, evidence, defeaters) | | 61508-1 §8 (assessment input) | | UL 4600; Machinery Reg. Annex IV | — | G1→G5 (living) | D |
| [WP-K-02](../10-safety-case/WP-K-02-technical-documentation-index.md) | Technical documentation index (the technical file) | 12100 §7 | 13849-1 §12 | | Machinery Reg. Annex IV | — | G5 | S |
| [WP-K-03](../10-safety-case/WP-K-03-cybersecurity-case.md) | Cybersecurity case | | | 62443-4-1 (practice evidence); 62443-4-2 (CR evidence) | | — | G5 | S |
| [WP-K-04](../10-safety-case/WP-K-04-functional-safety-assessment.md) | Functional safety assessment report (performed independently) | | 61508-1 §8 | | | — | G5 | S |
| [WP-K-05](../10-safety-case/WP-K-05-cybersecurity-assessment.md) | Cybersecurity assessment report (performed independently) | | | 62443-4-1 §4.3 (conformance) | | — | G5 | S |
| [WP-K-06](../10-safety-case/WP-K-06-release-record.md) | Release record and EU declaration of conformity (unsigned draft) | | | | Machinery Reg. Art. 21, Annex V | SUP.8 | G5 | S |
| [WP-K-07](../10-safety-case/WP-K-07-ai-act-conformity-record.md) | AI Act conformity record (learned locomotion policy as a machinery safety component) | | | | AI Act Art. 6, Art. 43, Annex IV | — | G5 | S |

### 3.11 Traceability (`trace/`)

| ID | Work product | Machinery | SRP/CS | IEC 62443 | Other | ASPICE | Gate | Status |
|---|---|---|---|---|---|---|---|---|
| [WP-T-01](../trace/README.md) | Requirements and traceability data (machine-readable), consistency evidence | | 13849-1 §5; 61508-3 §7.2 | 62443-4-1 SR-5 | | consistency evidence (SYS.2–5, SWE.1–6) | G1→G5 | S |

## 4. Work products the standards define that are covered elsewhere

| Standard work product | Where it is covered |
|---|---|
| Documentation of the risk assessment (ISO 12100 §7) | [WP-C-01](../02-concept/WP-C-01-item-definition.md), [WP-C-03](../02-concept/WP-C-03-risk-assessment.md), [WP-C-05](../02-concept/WP-C-05-risk-reduction-concept.md), indexed by [WP-K-02](../10-safety-case/WP-K-02-technical-documentation-index.md) |
| Safety requirements specification (ISO 13849-1 §5) | [WP-C-04](../02-concept/WP-C-04-safety-functions-and-plr.md) at concept level, [WP-S-02](../03-system/WP-S-02-safety-requirements.md) for the SRP/CS |
| Validation plan and report (ISO 13849-1 §10, ISO 13849-2; ISO 13482 §7) | [WP-V-01](../06-validation/WP-V-01-safety-validation.md), with the test work products [WP-V-02](../06-validation/WP-V-02-stopping-braking-stability-tests.md)…[WP-V-05](../06-validation/WP-V-05-fault-injection.md) |
| Technical documentation (ISO 13849-1 §12; Machinery Reg. Annex IV) | [WP-K-02](../10-safety-case/WP-K-02-technical-documentation-index.md) indexes this register |
| Information for use (ISO 12100 §6.4; ISO 13849-1 §13) | [WP-O-01](../09-production-operation/WP-O-01-assembly-installation-commissioning.md)…[WP-O-03](../09-production-operation/WP-O-03-information-for-use.md) |
| Verification review reports | Pull request review records, logged through [WP-P-05](../07-supporting/WP-P-05-verification-review-procedure.md) |
| Confirmation review and assessment reports | Records under [`10-safety-case/confirmation/`](../10-safety-case/confirmation/README.md), created per [WP-M-06](WP-M-06-confirmation-measures-plan.md) |
| Gate review records | [`10-safety-case/gates/`](../10-safety-case/gates/README.md), skeletons generated by the [process model](../process/README.md) |
| Change impact analysis records | [`07-supporting/impact/`](../07-supporting/impact/README.md) per [WP-M-11](WP-M-11-impact-analysis.md) |
| Decisions that wait on the project lead | [Decision register](decisions/README.md) |
| The concept-phase package (safety-case workbook, DFMEA, requirements, test plan, architecture, trace memo) | Seed material under [`00-assessment/concept-package/`](../00-assessment/concept-package/README.md), ported into the work products above; never evidence on its own |

## 5. Not applicable

| Standard or part | Rationale |
|---|---|
| ISO 26262, ISO 21448, ISO/SAE 21434, ISO/PAS 8800 | Road-vehicle standards. Asimov v1 is machinery. The standard-agnostic method is kept (one hazard log, one requirements database, the Living Safety Case); ISO 21448 is cited only as an informative method for the insufficiency analysis (WP-C-10, WP-V-08) because no machinery standard covers performance limits of a learned balance controller; the concept-package requirements workbook cites ISO 26262-3 §6 for its format only |
| ISO 3691-4 (driverless industrial trucks) | Asimov v1 is a legged robot, not a truck; the AMR-specific functions (protective field, braking distance) do not apply. ISO 13482 and ISO 10218 carry the mobility and manipulation hazards |
| ISO 13482 as a conformity claim | Used as the hazard catalogue and for the home and public operating envelopes OE-3 and OE-4, which are excluded from the first safety case (WP-C-02). A personal-care-robot claim is a lead decision (decision register) |
| ANSI/A3 R15.08, ANSI/RIA R15.06 (US) | Deferred pending the regulatory frame decision ([decision register](decisions/register.yaml) DQ-001). If the US market is the frame, a cross-reference from ISO 10218 to R15.06 is added to WP-M-13, not a second technical file |
| ISO 14971 | Medical-device risk management. Cited by the concept-phase package for technique only; the robot is not a medical device (AOU-07) |
| UL 4600 conformance | Used as guidance for structuring the safety case (WP-K-01). No conformance claim is made |
| IEC 61508 as a full lifecycle | Applied only where ISO 13849-1 runs out: management and assessment (Part 1 §6, §8), software beyond §7 of 13849-1 (Part 3). No SIL claim is made; the target measure is the Performance Level |
