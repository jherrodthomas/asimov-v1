# Glossary

The codes that appear in file names, commit messages, the records and the maps, decoded in one place.

## Work product prefixes

Each work product is named `WP`, a letter for its area, and a number, for example `WP-C-04` is the safety function
specification. The [work product register](../assurance/01-management/WP-M-00-work-product-register.md) lists every
one with its clauses, gate and status.

| Prefix | Area | Folder |
|---|---|---|
| `WP-M` | Management: strategy, plans, confirmation measures, regulatory strategy, upstream management, impact analysis | `01-management/` |
| `WP-C` | Concept: item definition and limits, operating envelopes, risk assessment, safety functions and PLr, risk reduction, interaction and contact limits, cybersecurity and ML concepts, insufficiency analysis | `02-concept/` |
| `WP-S` | System: safety requirements, stop-chain and safety-layer architecture, fall-arrest and response-time budget, I/O, cybersecurity architecture | `03-system/` |
| `WP-H` | Hardware: stop-chain hardware, electrical and battery safety, failure analysis, PL calculation, component qualification, structural and stability analysis | `04-hardware/` |
| `WP-W` | Software: the safety layer on the motion control board, requirements, architecture, verification, parameters, ML engineering of the policy | `05-software/` |
| `WP-V` | Validation: stability and fall tests, contact and detection, E-stop, fault injection, cybersecurity, test operations, field trials | `06-validation/` |
| `WP-P` | Supporting processes: configuration, change, problem resolution, documentation, review, tools, release, the process model | `07-supporting/`, `process/` |
| `WP-A` | Analyses: FMEA, FTA, CCF, STPA, independence of the chain from the policy and the tele-operation stack | `08-analyses/` |
| `WP-O` | Operation: kit assembly and commissioning, operation, information for use, field monitoring, incident response | `09-production-operation/` |
| `WP-K` | Safety case, technical documentation, cybersecurity case, assessments, release record, AI Act record | `10-safety-case/` |
| `WP-T` | Traceability data | `trace/` |

## Record identifiers

| Code | Reads as | Where it lives |
|---|---|---|
| `H-` | Hazard; the concept package's `HZ-` identifier is kept as a cross-reference | [Risk assessment, WP-C-03](../assurance/02-concept/WP-C-03-risk-assessment.md) |
| `SF-` | Safety function, with its required Performance Level `PLr` | [WP-C-04](../assurance/02-concept/WP-C-04-safety-functions-and-plr.md) |
| `OE-` | Operating envelope: OE-1 the supervised, tethered laboratory; OE-2 an industrial cell; OE-3 a home; OE-4 public space | [WP-C-02](../assurance/02-concept/WP-C-02-operating-environment-and-tasks.md) |
| `CFG-` | Robot configuration: CFG-001 the kit robot tethered and bench-powered, CFG-002 the battery and policy robot | [`case/configurations/`](../assurance/case/configurations/); [Reference robot](Reference-robot.md) |
| `SR-` | Safety requirement of the SRP/CS | [WP-S-02](../assurance/03-system/WP-S-02-safety-requirements.md) |
| `HWSR-`, `SWSR-` | Hardware and software safety requirement | [WP-H-01](../assurance/04-hardware/WP-H-01-hardware-safety-requirements.md), [WP-W-02](../assurance/05-software/WP-W-02-software-safety-requirements.md) |
| `CSR-`, `TS-` | Cybersecurity requirement, threat scenario | [WP-C-08](../assurance/02-concept/WP-C-08-cybersecurity-requirements-and-sl-target.md), [WP-C-07](../assurance/02-concept/WP-C-07-cybersecurity-threat-and-risk-assessment.md) |
| `AIR-` | Requirement on a learned component | [WP-C-09](../assurance/02-concept/WP-C-09-ml-component-definition-and-safety-requirements.md) |
| `FI-`, `TC-` | Functional insufficiency, triggering condition | [WP-C-10](../assurance/02-concept/WP-C-10-functional-insufficiency-analysis.md) |
| `PAR-` | Safety-related parameter | [WP-W-09](../assurance/05-software/WP-W-09-safety-parameters-and-configuration-data.md) |
| `AOU-` | Assumption of use: what the analysis assumes about the environment, the operator or the site | [WP-C-01](../assurance/02-concept/WP-C-01-item-definition.md); [`trace/items/`](../assurance/trace/README.md) |
| `VS-` | Verification specification (test case) | The verification work products |
| `DF-` | Defeater: known counter-evidence against a claim; DF-nn is GAP-nn at the first baseline | [Safety case, WP-K-01](../assurance/10-safety-case/WP-K-01-safety-case.md); [`case/defeaters/`](../assurance/case/defeaters/defeaters.yaml) |
| `GAP-` | A finding of the baseline gap assessment; never reused | [Gap assessment](../assurance/00-assessment/gap-assessment.md) |
| `OI-` | Open item of a work product, due at a gate | The last section of every work product |
| `ACT-` | Open action of the safety case | [`case/actions/`](../assurance/case/actions/actions.yaml) |
| `BL-` | Baseline: a named state of the fork and the upstream commit its sources came from | [`case/baselines/`](../assurance/case/baselines/baselines.yaml) |
| `IX-`, `FB-` | Cross-domain interface, feedback route | [Process model](../assurance/process/README.md) |
| `GOV-`, `CON-`, `DES-`, `DEV-`, `INT-`, `REL-`, `OPS-` | Activities of the process model, by phase | [Process maps](Process-maps.md) |
| `CR-`, `FSA-`, `AUD-`, `CS-`, `ML-R`, `NB-` | Confirmation reviews, functional safety assessments, audits, cybersecurity review and assessment, ML reviews, notified body | [WP-M-06](../assurance/01-management/WP-M-06-confirmation-measures-plan.md) |
| `DQ-` | Decision question for the project lead | [Decision register](How-decisions-are-made.md) |
| `T-`, `D-` | Tailoring decision, strategic decision | [WP-M-01 §5, §8](../assurance/01-management/WP-M-01-assurance-strategy.md) |
| `G0` to `G6` | Lifecycle gates | [WP-M-00 §2](../assurance/01-management/WP-M-00-work-product-register.md#2-gates) |

## Machinery and robot safety vocabulary

| Term | Meaning |
|---|---|
| **Performance Level (PL)** | ISO 13849-1's measure of a safety function's ability to perform under foreseeable conditions, PL a (lowest) to PL e. The **required** PL, `PLr`, comes from the risk graph on the hazard; the **achieved** PL from the control system's category, MTTFD, DCavg and CCF. |
| **Category** | The designated architecture of a safety-related part: B, 1, 2, 3 or 4. Category 3 and 4 have two channels so that a single fault does not lose the function. |
| **MTTFD, DCavg, CCF** | Mean time to dangerous failure per channel; average diagnostic coverage; the common cause failure score. The three numbers the PL calculation needs. |
| **SRP/CS** | Safety-related part of a control system: everything from the button or sensor through the logic to the contactor that implements a safety function. Here the safety layer and the stop chain. |
| **Safety function** | A function of the machine whose failure can immediately increase risk: emergency stop, controlled descent, joint torque and velocity limit, power-and-force limiting, and so on. |
| **Safe state** | The condition a safety function brings the machine to. On a wheeled machine, power off. On a biped, undecided (DQ-005): a controlled descent, holding the pose, or power off, which is a fall. |
| **Controlled descent, fall arrest** | Lowering the robot to a kneel or crouch before impact when a fall is impending or power must be removed (SF-02). Until it exists and is verified, the tether and gantry carry the fall. |
| **Tether and gantry** | The overhead anchor and rated line that carry the robot's mass in a fall in the laboratory envelope. A complementary protective measure under ISO 12100, a condition of every powered floor test, and a claim of its own (G2.4), never a safety function with a PL. |
| **Emergency stop, protective stop** | A stop a person triggers (ISO 13850) versus a stop a safeguard or monitor triggers. On a biped the stop category of the emergency stop is itself a decision (DQ-016). |
| **Stop category 0 / 1** | IEC 60204-1: immediate removal of power (0) or a controlled stop followed by removal of power (1). |
| **Power-and-force limiting (PFL), contact limits** | The collaborative mode of ISO 10218 and ISO/TS 15066 in which contact is allowed but bounded by body-region force, pressure and energy limits. Not claimed in the laboratory: nobody is within reach of a powered limb until the limits are measured. |
| **Reach envelope, fall radius** | The space a limb can reach, and the space the robot can fall into. The test area is the reach envelope plus a margin, with nobody inside while the actuator rail is powered. |
| **Mode machine DAMP / STAND / MOVE** | Upstream's declared modes: motors limp, the controller holding a standing pose, and accepting motion commands. DAMP is the default on disconnect or E-stop release and drops the robot. |
| **BMS interlock** | A handshake with the battery management system without which the actuator rails are not enabled; the proposed answer to a user-supplied battery (DQ-009). |
| **Three-step method** | ISO 12100's order of risk reduction: inherently safe design first, then safeguarding and complementary protective measures, then information for use. |
| **Technical documentation** | The file Regulation (EU) 2023/1230 Annex IV requires a manufacturer to hold; [WP-K-02](../assurance/10-safety-case/WP-K-02-technical-documentation-index.md) indexes it. |
| **Annex I Part A** | The Machinery Regulation's list of machinery needing mandatory third-party assessment, including safety components with self-evolving behaviour; the threshold a learned balance function would cross. |
| **Security level target (SL-T)** | IEC 62443's target per foundational requirement, SL 1 to SL 4; set by the lead (DQ-012). |
| **Doer, checker, checker of last resort** | The tele-operation stack and the policy propose; the safety layer on the motion control board checks; the hardwired stop chain acts regardless of software. |
| **Kit robot (CFG-001)** | The robot a builder can make from the repository and the DIY kit today, tethered, bench-powered, tele-operated: the reference configuration. See [Reference robot](Reference-robot.md). |
| **Hold point** | A condition no test proceeds past: [WP-V-07](../assurance/06-validation/WP-V-07-test-operations.md) before any powered test with the feet on the floor, and [WP-V-03](../assurance/06-validation/WP-V-03-personnel-detection-validation.md) before anyone comes within reach of a powered limb. |

## Safety-case vocabulary

| Term | Meaning |
|---|---|
| **Claim** | A statement the safety case argues is true. |
| **Evidence item** | A test result, analysis or review that supports a claim. Each carries a review state; it is *accepted* only after confirmation review. |
| **Defeater** | Known counter-evidence, or a reason the argument might not hold. Open defeaters are published, not hidden. GAP-01…GAP-34 are the first. |
| **Confirmation review** | An independent check that a work product does what its standard asks. Nothing leaves draft without a verification review; nothing is accepted without a confirmation measure. |
| **Baseline** | A frozen, named state of the whole record. BL-001 is the fork as inherited with the concept-phase package. |
| **Independence I0 to I3** | Who may review: the author, another person, someone outside the team, someone outside the organisation. |
| **Concept-phase package** | The five workbooks and three documents the fork published before the record existed; seed material, kept unedited, never evidence on its own. |
