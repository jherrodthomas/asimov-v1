# WP-C-04 Safety functions specification with required Performance Level, stop category and response time

| Field | Value |
|---|---|
| Work product | WP-C-04 Safety functions specification with required Performance Level, stop category and response time |
| Standard reference | ISO 13849-1:2023 §5 (safety requirements specification of each safety function), Annex A (PLr); ISO 10218-1:2011 §5.4 (safety-related control system performance), §5.5 (robot stopping functions), §5.6 (speed control), §5.10 (collaborative operation); ISO 13482:2014 §5.16 (emergency stop), §6 (safety-related control system); ISO 13850:2015 §4; IEC 60204-1:2018 §9.2.2 (stop categories); ISO/TS 15066:2016 §5.5 |
| Version | 0.4 (2026-10-21): DQ-028 A (contact limits) and DQ-034 A (second IMU) applied. 0.3 (2026-10-21): DQ-014 A applied to SF-03. 0.2 (2026-10-21): the lead's answers of 2026-10-21 applied: PL d (DQ-004 A); the safe state is a controlled descent to a kneel or crouch, then power removal, the E-stop removes power at once (DQ-005 A, closing DQ-016); SF-01 withdrawn as a safety function (DQ-006 A); SF-13 devices (DQ-008 A); SF-15 battery policy (DQ-009 A). 0.1 (2026-10-21): the 25 functions of the concept-package FSC (`09_FSC`) with their targets, reaction times and allocations, re-stated per function with demand, safe state, response, stop category, PLr, category, modes and the open decisions; the four decisions that shape them (DQ-004, DQ-005, DQ-006, DQ-008) marked |
| Status | Draft |
| PL / scope | PL d target for the stop and fall functions (DQ-004 A, decided 2026-10-21); CFG-001 in OE-1; the collaborative functions SF-04, SF-06, SF-20 specified but not claimed in the first item |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Project lead |
| Baseline | BL-001 |

> [!WARNING]
> Draft. The reaction times and allocations are the package's concept-level targets, not measured or designed
> values. The safe state of the biped was decided on 2026-10-21 (DQ-005 A: a controlled descent to a kneel or
> crouch, then power removal; the E-stop removes power at once). Nothing here has been implemented: no firmware exists.

## 1. Purpose

Specifies the safety functions of the robot (ISO 13849-1 §5): for each, the triggering condition, the safe state,
the response time, the stop category (IEC 60204-1 §9.2), the required Performance Level from the risk graph, and the
operating modes it applies in. SF-nn IDs are never reused and keep the package's numbering (DQ-018). The functions
are identified in [WP-C-03](WP-C-03-risk-assessment.md) §7; this document is their specification;
[WP-S-02](../03-system/WP-S-02-safety-requirements.md) breaks each into testable requirements SR-nn.mm;
[WP-S-03](../03-system/WP-S-03-technical-safety-concept.md) designs the safety-related parts that implement them;
[WP-S-04](../03-system/WP-S-04-response-time-and-stopping-budget.md) budgets the response times, the controlled
descent and the fall energy against measurement.

Conventions: a **demand** is the event the function must respond to; the **safe state** is what the function
achieves and holds; the **response time** runs from the demand at the sensor or device to the start of the safe
state. For a standing biped the safe state is not power removal alone: power removal (DAMP) is a fall (WP-C-03 H-28).
The safe state is **controlled descent to a kneel or crouch under a deterministic sequence, then power removal**
(DQ-005 A, decided 2026-10-21); the E-stop removes power at once (stop category 0; DQ-016 withdrawn as settled)
and the tether carries the fall in OE-1. Stop categories
per IEC 60204-1 §9.2.2: category 0 is immediate removal of power (a fall onto the tether); category 1 is a
controlled stop with power removed when stopped (the controlled descent).

The contact limits behind SF-03, SF-04 and SF-20 are the ISO/TS 15066 Annex A body-region values with the head and neck excluded from contact by design and a project factor of 0.75 on the arm and hand values until measured (DQ-028 A, decided 2026-10-21; WP-C-06 §3). The perception trigger of SF-06 and the limits of SF-02 are bounded in WP-C-10. The allocation of SF-01 to the learned locomotion policy is decided in WP-C-09 and DQ-006. The answer (DQ-006 A, 2026-10-21) withdraws SF-01 as a safety function: the policy is a functional component.

## 2. Safety functions

| ID | Safety function | Demand | Safe state | PLr | Cat. | Stop cat. | Response target (package) | Allocation (package) | Hazards |
|---|---|---|---|---|---|---|---|---|---|
| SF-01 | Maintain bipedal stability while standing and moving | Every control cycle in STAND and MOVE: a disturbance, a step, an external push within the limits | The robot keeps its balance | d (package); **withdrawn, DQ-006 A** | — | — | ≤ 20 ms | locomotion policy as a functional component; bounded by SF-03, SF-23; the tether carries stability (G2.4) | H-01, H-06, H-22 |
| SF-02 | Detect an impending fall and arrest it by a controlled descent before impact | IMU attitude or rate outside the recoverable envelope; loss of torque on a load-bearing joint; SF-08 or SF-13 demand while standing | A controlled descent to a kneel or crouch, then power removal **(DQ-005)**; on the tether, the tether carries what the descent does not | d | 3 | 1 then 0 | ≤ 200 ms to the start of the descent | MCB safety layer, IMU, actuators | H-01, H-06, H-23, H-28 |
| SF-03 | Joint torque and velocity limit per joint | A commanded or measured torque or velocity above the limit of the active envelope | The command is clamped; a sustained violation is a fault (SF-08) | d | 3 | — | ≤ 10 ms | MCB safety layer, drive current limit | H-02, H-04, H-24 |
| SF-04 | Force-limited contact in collaborative regions | Contact force or pressure above the ISO/TS 15066 body-region limit | Joint torque reduced and motion stopped at the contact | d | 3 | 1 | ≤ 100 ms | MCB safety layer, sensorised links (none exist) | H-02, H-04, H-24 |
| SF-05 | Fastener torque and secure-by-design; chamfered edges | — (static) | — | — | — | — | static | mechanical design | H-03 |
| SF-06 | Speed reduction in human-shared regions on a perception trigger | A person detected in the shared region | Joint velocities reduced to the collaborative limit | c | 2 | — | ≤ 200 ms | edge perception → MCB | H-04 |
| SF-07 | Guarding at the waist yaw and neck yaw rotational interfaces | — (static) | — | — | — | — | static | mechanical guarding, gaps ≤ 4 mm | H-05 |
| SF-08 | Safe stop on watchdog timeout or communication loss | No tele-operation heartbeat for 250 ms; a control-loop deadline miss; a CAN bus-off on a leg bus; a fault classified critical | The safe state of DQ-005 as a stop category 1 (controlled descent), power removed when reached; latched until re-armed | d | 3 | 1 | ≤ 100 ms | MCB watchdog and safety layer | H-06, H-23, H-26, H-28 |
| SF-09 | Cable management and a visible tether route | — (procedure) | — | — | — | — | — | procedure, harness clips | H-07 |
| SF-10 | Power isolation: lockable disconnector and insulation class | — (static) | — | — | — | — | — | power distribution board, connectors | H-08, H-09 |
| SF-11 | Overcurrent protection on each motor branch | Branch current above the fuse rating | The branch is opened | c | 2 | — | ≤ 50 ms | per-rail fuse, MCB current sense | H-09 |
| SF-12 | ESD-safe assembly process | — (procedure) | — | — | — | — | — | assembly process | H-10 |
| SF-13 | Emergency-stop devices and wireless link surveillance | A person actuates the wired pendant (OE-1) or the wireless transmitter; the wireless heartbeat is lost; a channel fault | Motor power removed by two independent paths; latched until a deliberate re-arm; the tether carries the fall (DQ-016) | d | 3 | 0 **(DQ-016)** | ≤ 500 ms (package); ≤ 200 ms proposed for the wired device | E-stop devices, receiver, motor-rail contactors **(DQ-008)** | H-11, H-28, every limb hazard |
| SF-14 | Stator over-temperature shutdown | Stator thermistor above the limit | The joint is de-rated, then stopped; a hardware cut-off backs the firmware | c | 2 | 1 | ≤ 200 ms | thermistor, MCB, PTC backup | H-12 |
| SF-15 | Battery thermal and cell-voltage protection by the BMS | Cell voltage, temperature or current outside the safe operating area; no BMS handshake on C5 | The pack is isolated; the motor rails are not enabled without the handshake | e (package) | 4 | 0 | ≤ 1 s | BMS (user-supplied), rail interlock **(DQ-009)** | H-13, H-23 |
| SF-16 | Audio limiter at or below 80 dBA at 1 m | — (continuous) | Output bounded | b | 1 | — | static | MCB firmware, hardware limiter | H-14 |
| SF-17 | Respiratory protection during MJF dust generation | — (procedure) | — | — | — | — | — | information for use | H-17 |
| SF-18 | Two-person lift for the 35 kg robot | — (procedure) | — | — | — | — | — | information for use | H-18 |
| SF-19 | Indoor-only operating envelope until an IP-rated build exists | — (restriction) | — | — | — | — | — | operating restriction | H-19, H-20 |
| SF-20 | Power-and-force limiting per ISO/TS 15066 in collaborative mode | Collaborative mode active (OE-2) | Commanded forces bounded by the body-region limits | d | 3 | — | ≤ 100 ms | MCB safety layer, design | H-24 |
| SF-21 | Authenticated, integrity-protected tele-operation channel | A command arrives without a valid session or integrity check | The command is refused; no motion | c | 2 | — | ≤ 100 ms | edge board, WebRTC | H-29 |
| SF-22 | Operator session lock and idle timeout | No operator input for 30 s | The session locks; motion commands refused until re-authentication | b | 1 | — | ≤ 30 s | edge board, API | H-27, H-29 |
| SF-23 | IMU plausibility and cross-check | IMU rate integrated over dt disagrees with the accelerometer attitude; stale sample; saturation | The attitude estimate is rejected; a persistent fault triggers SF-08; a second IMU gives the second channel | d | 3 | — | ≤ 50 ms | MCB safety layer, two IMUs | H-30 |
| SF-24 | Real-time scheduler watchdog and deadline monitor | A control-loop deadline missed; the watchdog not fed within its window | SF-08 (controlled descent); a hardware watchdog resets the SoC if the firmware hangs | d | 3 | 1 | ≤ 50 ms | MCB safety layer, hardware watchdog | H-31 |
| SF-25 | Software joint limits inside the mechanical end-stops | A position command beyond the software limit (≥ 5° inboard of the end-stop) | The command is clamped to the limit | c | 2 | — | static | MCB firmware, mechanical end-stops | H-32 |

## 3. Specification per function

Each function with a PLr carries the items ISO 13849-1 §5.1 expects of a safety requirements specification; the
requirements SR-nn.mm of WP-S-02 are the testable form. "Today" is the kit robot at BL-001. Functions without a PLr
(SF-05, SF-07, SF-09, SF-10, SF-12, SF-17, SF-18, SF-19) are static measures and procedures; they are specified in
WP-C-05 and WP-O-03 and verified by inspection.

### 3.1 SF-01 Maintain bipedal stability

| Item | Specification |
|---|---|
| Demand | Every control cycle in STAND and MOVE: gravity, a step, an external disturbance within the limits of WP-C-01 §4 |
| Safe state | The robot keeps its balance within the recoverable envelope; outside it SF-02 takes over |
| Response time | ≤ 20 ms control cycle (package) |
| PLr | **none: withdrawn as a safety function** (DQ-006 A, decided 2026-10-21). The package's d is kept in the table of §2 for traceability only |
| Allocation | The package allocated it to the locomotion policy, the IMU and the MCB. **The policy is a learned component nobody outside upstream has seen (GAP-13, GAP-17).** The lead's decision (DQ-006 A) withdraws SF-01 as a safety function: stability in OE-1 rests on the gantry and tether (claim G2.4), the policy is a functional component whose output is bounded by SF-03 and watched by SF-23, and no learned component implements a safety function. Annex I Part A of the Machinery Regulation and the AI Act high-risk file are not triggered (WP-M-13 §5). A free-standing robot is not in the case until a deterministic balance safeguard exists |
| Modes | M2 STAND, M3 MOVE |
| Verification | WP-V-02 stability tests on the tether; the policy's sim-to-real coverage (WP-W-10) if allocated |
| Today | No controller exists in public; the robot has never stood under the fork |

### 3.2 SF-02 Fall arrest by controlled descent

| Item | Specification |
|---|---|
| Demand | IMU attitude or angular rate outside the recoverable envelope **(TBC from WP-S-04)**; loss of torque or encoder on a load-bearing joint; a demand of SF-08 or SF-13 while standing |
| Safe state | **Decided (DQ-005 A, 2026-10-21):** a deterministic descent sequence lowers the centre of mass to a kneel or crouch within the budget of WP-S-04, then motor power is removed; the robot ends de-energised and low. On the tether the tether carries whatever the descent does not. Option B (power removal only) makes this function a tether rule; option C (hold) is not a safe state |
| Response time | ≤ 200 ms to the start of the descent (package); the descent itself **(TBC)**; the fall energy at contact bounded by WP-H-08 |
| Stop category | 1, then 0 |
| PLr | d |
| Category, DC | 3, medium or better: two IMUs (SF-23), redundant detection of loss of torque, the hardware watchdog as the second path to power removal |
| Modes | M2, M3 |
| Priority | Below SF-13 (the E-stop removes power at once); above every tele-operation and policy command |
| Fault reaction | A fault in the descent sequence ends in power removal (the fall onto the tether) rather than a held pose |
| Verification | WP-V-02 deliberate-fall and power-cut tests on the gantry with the tether slack enough to let the descent happen and tight enough to catch a failure |
| Today | Does not exist; the declared behaviour on a fault is DAMP, a fall (GAP-10) |

### 3.3 SF-03 Joint torque and velocity limit

| Item | Specification |
|---|---|
| Demand | A commanded torque or velocity above the limit of the active envelope; a measured torque or velocity above the limit for more than **(TBC: 20 ms)** |
| Safe state | The command is clamped before it reaches the joint controller; a sustained measured violation is classified a critical fault and triggers SF-08 |
| Response time | ≤ 10 ms (package) |
| PLr | d |
| Category, DC | 3: the firmware clamp as channel 1, the drive's hardware current limit as channel 2, encoder and current read-back as diagnostics |
| Limits | Per joint and per envelope, from WP-W-09. In OE-1: half the MuJoCo control range per joint and a velocity ceiling set by WP-S-04, until measured (DQ-014 A, decided 2026-10-21); the MuJoCo control ranges are the only published values and are simulation values (GAP-06) |
| Modes | M2, M3, M4 |
| Verification | WP-W-06 unit tests of the clamp, WP-V-03 measured torques at the joints |
| Today | Nothing published enforces any limit |

### 3.4 SF-08 Safe stop on watchdog timeout or communication loss

| Item | Specification |
|---|---|
| Demand | No tele-operation heartbeat for 250 ms (package SRS-004); a control-loop deadline missed (SF-24); a CAN bus-off on a leg bus (package SYRS-023); a fault classified critical (package SRS-013) |
| Safe state | The controlled descent of DQ-005 A reached as a stop category 1 (SF-02's descent), power removed when reached; latched until a deliberate re-arm with the cause cleared |
| Response time | ≤ 100 ms to the start of the stop (package) |
| PLr | d |
| Category, DC | 3: the firmware watchdog as channel 1, the hardware watchdog on the SoC as channel 2 (package SRS-002) |
| Modes | M2, M3 |
| Verification | WP-V-04 heartbeat-loss and bus-off tests; WP-V-02 for the descent |
| Today | Upstream describes a watchdog that enters DAMP on disconnect; DAMP is a fall (GAP-10); nothing is public (GAP-16) |

### 3.5 SF-13 Emergency-stop devices and wireless link surveillance

| Item | Specification |
|---|---|
| Demand | A person actuates the wired, dual-channel pendant device on the tether (OE-1, DQ-008 A) or the kit's wireless transmitter (ISO 13850 devices: red mushroom on yellow, positive-opening contacts, latching); the wireless heartbeat is missed for **(TBC)** periods; a channel fault |
| Safe state | Motor power removed from every actuator by two independent paths (motor-rail contactors in series and the drive enables); latched until a deliberate re-arm at the robot or the pendant with every device released (no automatic re-arm, DFMEA FM-20); the tether carries the fall in OE-1 |
| Response time | ≤ 500 ms (package SYRS-003); ≤ 200 ms proposed for the wired device to power removal |
| Stop category | 0 (DQ-005 A, decided 2026-10-21; DQ-016 withdrawn as settled): no software in the path, power removed at once, the tether carries the fall in OE-1; a category 1 E-stop would run through the controller the operator may be stopping |
| PLr | d |
| Category, DC | 3, medium or better: dual channel, cross-monitored, contactor feedback in the re-arm loop; the wireless receiver counts only with heartbeat surveillance that fails safe (SF-13's own diagnostic) |
| Modes | Every mode |
| Priority | Highest; overrides every other command and function |
| Fault reaction | A single fault in either channel, a welded contactor or a lost heartbeat is detected at or before the next demand and prevents re-arm |
| Verification | WP-V-04: each device, each channel, link loss, dead transmitter battery, welded-contact simulation, re-arm held |
| Today | A "wireless E-Stop" is listed; nothing documents what it switches or how (GAP-07, GAP-11) |

### 3.6 SF-23 IMU plausibility and cross-check

| Item | Specification |
|---|---|
| Demand | The integrated angular rate over dt disagrees with the accelerometer-derived attitude beyond **(TBC)**; a sample is stale; a sensor is saturated; the two IMUs disagree |
| Safe state | The attitude estimate is rejected for that cycle; a persistent fault (**TBC:** 3 cycles) is critical and triggers SF-08 |
| Response time | ≤ 50 ms (package) |
| PLr | d |
| Category, DC | 3: a second IMU of a different type on a separate supply, read by the safety layer and cross-checked against the first (DQ-034 A, decided 2026-10-21; DFMEA FM-12) |
| Modes | M2, M3 |
| Verification | WP-V-05 fault injection: frozen, saturated and biased IMU data |
| Today | One LSM6DSV on the motion control board; an external IMU connector exists (electrical README) |

### 3.7 SF-24 Scheduler watchdog and deadline monitor

| Item | Specification |
|---|---|
| Demand | The motion-control loop misses its deadline; the firmware fails to feed the hardware watchdog within its window |
| Safe state | SF-08; if the firmware itself has hung, the hardware watchdog resets the SoC and the actuators lose their enable (power removed: the fall onto the tether) |
| Response time | ≤ 50 ms (package); hardware watchdog window **(TBC: 100 ms)** |
| PLr | d |
| Category, DC | 3: software deadline observer and hardware watchdog |
| Verification | WP-V-05 injected loop stalls; WP-V-04 power-cycle test that the watchdog fires |
| Today | Nothing public |

### 3.8 SF-04, SF-06, SF-20: the collaborative functions

Specified for OE-2 and not claimed in the first item: nobody is within reach of a powered limb in OE-1 (AOU-06,
WP-C-02 §5). SF-04 and SF-20 need measured contact forces against the ISO/TS 15066 Annex A body-region limits
(GAP-05) and sensing the robot does not have; SF-06 needs a perception trigger whose limits WP-C-10 must bound.
They stay in the register so that the OE-2 item can take them up without re-rating.

### 3.9 SF-11, SF-14, SF-15, SF-16, SF-21, SF-22, SF-25

Conventional functions whose package rows (§2) are adopted as the specification at v0.1; their requirements are
ported from the package's SYRS, SRS and HwRS into WP-S-02. SF-15 is absent on CFG-001 (no battery) and its interlock
was decision DQ-009, answered 2026-10-21 (A): a certified-pack list in the information for use and a hardware interlock that refuses the motor rails without a compliant BMS handshake on C5. The interlock is designed in WP-H-05 and WP-H-02; CFG-001 carries no battery.

## 4. Required Performance Level

PLr per function follows WP-C-03 §5 and §7: the package's reading as the unmitigated value, the OE-1 reading with
the complementary measures, and the ISO 10218-1 §5.4 default of PL d, Category 3 as the floor for the stop and fall
functions (DQ-004 A, decided 2026-10-21). SF-15 keeps the package's PL e on CFG-002 because a thermal runaway inside a home is S2 F2
P2 and no complementary measure applies; on CFG-001 the function is absent.

## 5. Allocation

| Element | Functions | Claim |
|---|---|---|
| Hardwired stop chain: E-stop devices, surveilled receiver, motor-rail contactors, BMS handshake interlock | SF-13, the power-removal leg of SF-08 and SF-02, SF-15 interlock | PL d (SF-15: e) with certified components; nothing in software can hold a contactor closed |
| MCB safety layer (deterministic firmware) | SF-02, SF-03, SF-08, SF-14, SF-16, SF-23, SF-24, SF-25; SF-04, SF-06, SF-20 in OE-2 | PL at the PLr with the ISO 13849-1 §7 lifecycle (WP-W-*); does not exist today |
| Power distribution board | SF-10, SF-11, under-voltage lockout | PL c for SF-11 |
| Edge board | SF-21, SF-22 | PL c and b |
| Locomotion policy | none: SF-01 withdrawn (DQ-006 A) | none |
| Gantry and tether, procedures, information for use | the fall hazard in OE-1; SF-05, SF-07, SF-09, SF-12, SF-17, SF-18, SF-19 | complementary measures, verified by inspection |

## 6. Response time and stop category per function

Per the §2 table; the budget against actuator, bus and contactor data is [WP-S-04](../03-system/WP-S-04-response-time-and-stopping-budget.md),
which also owns the controlled-descent model. No value is measured.

## 7. Applicability per task and mode

| Task (WP-C-02) | Mode | Functions active | Functions claimed |
|---|---|---|---|
| T-01 bench | M4 | SF-03, SF-11, SF-13, SF-14, SF-24, SF-25 | none until implemented |
| T-02 hang test | M4 | as T-01 plus SF-08, SF-23 | none until implemented |
| T-03, T-04 stand and move on the tether | M2, M3 | every function with a PLr except SF-04, SF-06, SF-15, SF-20 | none until implemented; the gantry carries the fall |
| T-05 walk on the tether (CFG-002) | M3 | as T-04; SF-01 withdrawn (DQ-006 A), the tether carries stability | not in the first item |
| T-06 fall tests | M1–M3 | SF-02, SF-08, SF-13 under test | — |

## 8. Traceability

Hazards: WP-C-03 §4 and `trace/items/hazards.yaml`. Requirements: WP-S-02 (to be ported from the package's 63 safety
requirements). Architecture: WP-S-03. Budget: WP-S-04. Tests: WP-V-01…WP-V-05 (to be ported from the package's 139
test cases). Claims: WP-K-01 G1.1…G1.15, G2.4.

## 9. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | ~~Apply DQ-005 (safe state) to SF-02, SF-08, SF-13 and §1; apply DQ-016 (stop category) to SF-13~~ applied 2026-10-21 (DQ-005 A; DQ-016 settled by it) (ACT-002) | SM | G1 |
| OI-2 | ~~Apply DQ-006 to SF-01 and §5~~ applied 2026-10-21 (A: withdrawn); carry the withdrawal into WP-C-09 and WP-M-09 (ACT-003) | ML | G1 |
| OI-3 | Design the E-stop architecture behind SF-13 (DQ-008 A decided 2026-10-21: wired dual-channel pendant plus surveilled wireless device; ACT-004) | EM | G1 |
| OI-4 | Set every remaining **(TBC)** value from WP-S-04; the joint limits are half the MuJoCo range until measured (DQ-014 A, decided 2026-10-21) | SRP | G2 |
| OI-5 | Port the package's safety requirements into WP-S-02 under these functions (ACT-007) | SRP | G2 |
