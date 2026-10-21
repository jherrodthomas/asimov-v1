# WP-C-03 Risk Assessment and Required Performance Levels

| Field | Value |
|---|---|
| Work product | WP-C-03 Risk assessment (ISO 12100) and determination of the required Performance Level per safety function (ISO 13849-1) |
| Standard reference | ISO 12100:2010 §5.4–§5.6, Annex B; ISO 13482:2014 §5, Annex A; ISO 10218-1:2011 §5, Annex A; ISO 13849-1:2023 §5, Annex A (risk graph); ISO 13850:2015; IEC 60204-1:2018 §9.2.2 (stop categories); Regulation (EU) 2023/1230 Annex III §1.1.2 |
| Version | 0.1 (2026-10-21): the 32 hazards of the concept-package catalogue (`06_Hazards`) ported as H-01…H-32 with their package IDs; the risk graph readings of the package HARA (`07_HARA`) carried as the unmitigated rating per operating envelope and re-read for OE-1 with the gantry and tether; the 25 safety functions identified; measures DM-01…DM-06 |
| Status | Draft |
| PL / scope | Highest PLr in OE-1: **d** proposed (DQ-004, open); the inherited HARA reads **e** for nine rows in OE-2…OE-4, which stay excluded rather than argued down; CFG-001 |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1); the ratings need a reviewer who has built or operated the robot |
| Approver | Project lead |
| Baseline | BL-001; item as defined in [WP-C-01](WP-C-01-item-definition.md) |

> [!WARNING]
> Draft. Severity and probability ratings below are engineering judgement from the record and from the concept
> package, not from measurement: the robot has not been weighed, its centre of gravity, joint limits and fall energy
> are unknown (WP-C-01 §10). The lead has not yet set the target PL (DQ-004) or the safe state (DQ-005). Nothing here
> lowers a rating to fit the existing hardware; where the gantry and tether change a reading, the row says so.

## 1. Scope and inputs

- **Item:** the kit robot of WP-C-01 on CFG-001 in modes M0–M4 within the limits of WP-C-01 §4, in operating
  envelope OE-1 (WP-C-02). Rows for OE-2…OE-4 are rated so that the later items need not re-rate them; they are
  excluded from the first safety case.
- **Inputs:** WP-C-01 (item, functions, modes, assumptions of use); [WP-C-02](WP-C-02-operating-environment-and-tasks.md)
  (envelopes, tasks, exclusions); the concept-package hazard catalogue, HARA, system FMEA and DFMEA; ISO 12100
  Annex B and ISO 13482 Annex A hazard lists; the gap assessment GAP-01…GAP-34. The interaction and misuse analysis
  ([WP-C-06](WP-C-06-human-robot-interaction-and-misuse.md)) is a skeleton at v0.1; its scenarios will re-rate §5.
- **Outputs:** the hazard list H-nn (§4), the risk estimation per envelope (§5), the measures (§6) and the safety
  functions SF-nn with their PLr (§7). The specification of each safety function is
  [WP-C-04](WP-C-04-safety-functions-and-plr.md).
- **Out of scope:** the battery (absent on CFG-001; its rows are rated for CFG-002); collaborative tasks; the
  locomotion policy's behaviour beyond what the gantry bounds.

Cyber-induced hazards are analysed in WP-C-07; their safety impact is rated here (H-29) against the same graph.

## 2. Method

1. **Hazard identification** (§4): the ISO 12100 Annex B origins and the ISO 13482 Annex A personal-care list,
   crossed with the functions and modes of WP-C-01 and the tasks of WP-C-02. The package did this traversal; its 32
   rows are kept in order (DQ-018) with the package ID beside each.
2. **Risk estimation** (§5): ISO 13849-1 Annex A risk graph for each hazard a control function must address:
   severity S1 (slight, normally reversible) or S2 (serious, normally irreversible, or death); frequency or exposure
   F1 (seldom to less often, or short) or F2 (frequent to continuous, or long); possibility of avoiding P1 (possible
   under specific conditions) or P2 (scarcely possible). The graph gives PLr a–e. The package's reading is kept as
   the **unmitigated** rating for the envelope it applies to; a second reading for **OE-1 with the gantry, the
   tether, the bench supply and the cleared area** records what the complementary measures change (F or P), never
   S. Where a rating depends on another safety function already being in place, the dependency is written in the row
   and carried into WP-C-04.
3. **Type-C check.** ISO 10218-1 §5.4 sets PL d, Category 3 as the default for a robot's safety-related control
   functions; ISO 13482 §6 allows a PL from the risk assessment (**to be checked against licensed copies**). Where
   the type-C value and the risk graph differ, the higher is adopted unless the row says why not; where the graph
   gives **e** the situation is excluded from the operating envelope or carried by a complementary measure rather
   than argued down.
4. **Risk evaluation** (§6): adequate risk reduction per ISO 12100 §6: inherently safe design first, then
   safeguarding and complementary measures (the safety functions `SF-nn` with their PLr, the gantry), then
   information for use.
5. **Safety functions** (§7): each `SF-nn` with its adopted PLr and the hazards it addresses; the specification
   goes to WP-C-04.

### 2.1 Severity scale used

S2 for any contact with a 35 kg body falling or a limb driven at full torque (irreversible injury is plausible),
for electric shock from the battery rail, for a lithium fire; S1 for pinches at low torque, hot surfaces, noise,
dust, trips.

### 2.2 Risk graph

Read as ISO 13849-1 Annex A: S1 → a, b (F1) or b, c (F2) by P; S2 → c, d (F1) or d, e (F2) by P. The graph is a
tool for the PLr of a control function; a hazard without a control function (H-03, H-17, H-18) carries a severity
and a measure, not a PLr.

## 3. Situations

| ID | Situation | Envelope | Mode | People | Scenarios |
|---|---|---|---|---|---|
| OS-01 | Actuator or limb on the bench stand | bench | M4 | technician at the bench | T-01 |
| OS-02 | Robot hanging on the gantry, feet off the floor, joints moved | OE-1 | M4 | operator, observer outside reach | T-02 |
| OS-03 | Robot standing on the tether under its controller | OE-1 | M2 | operator, observer | T-03 |
| OS-04 | Robot moving limbs and torso on the tether | OE-1 | M3 | operator, observer | T-04 |
| OS-05 | Deliberate fall, power cut or DAMP on the tether | OE-1 | M1–M3 | operator, observer | T-06 |
| OS-06 | Walking on the tether under the policy (CFG-002) | OE-1 | M3 | operator, observer | T-05 |
| OS-07 | Building, wiring, lifting, repairing the robot | workshop | M0 | builder | assembly, maintenance |
| OS-08 | Charging or handling a battery (CFG-002) | OE-2…OE-4 | M0 | builder, user | — |
| OS-09 | Free-standing robot in a cell with a briefed worker (CFG-002) | OE-2 | M2, M3 | briefed | T-08 |
| OS-10 | Free-standing robot in a home or public space (CFG-002) | OE-3, OE-4 | M2, M3 | public, children, pets | excluded |
| OS-11 | Tele-operation with a lost or spoofed link, a stale camera frame or an unauthorised operator | any | M3 | as the envelope | H-28, H-29 |

## 4. Hazard identification

| ID | Package | Origin (ISO 12100 Annex B, ISO 13482 Annex A) | Hazardous event | Hazard zone | Situations |
|---|---|---|---|---|---|
| H-01 | HZ-M01 | Mechanical: crushing | Tip-over onto a person: a 35 kg body falling from 1.2 m, about 411 J at the centre of mass | the fall radius, about 1.5 m | OS-03…OS-06, OS-09, OS-10 |
| H-02 | HZ-M02 | Mechanical: shearing, pinch | Joint pinch or shearing: knee, elbow, hip, neck trap fingers or a limb during MOVE | every actuated joint | OS-01, OS-02, OS-04, OS-09, OS-10 |
| H-03 | HZ-M03 | Mechanical: cutting | Sharp edges on machined 7075 parts; a loose fastener as a projectile | the structure | OS-07, any |
| H-04 | HZ-M04 | Mechanical: impact | An arm sweep strikes the head or torso of a bystander during MOVE | the reach envelope | OS-04, OS-09, OS-10 |
| H-05 | HZ-M05 | Mechanical: drawing-in | Hair or clothing caught at the waist yaw or neck yaw rotation | waist, neck | OS-09, OS-10 |
| H-06 | HZ-M07 | Mechanical: stability | Loss of balance during STAND or MOVE: an uncommanded fall | the fall radius | OS-03…OS-06, OS-09, OS-10 |
| H-07 | HZ-M08 | Slip, trip, fall of a person | A person trips over the robot, its tether or its harness | the test area | OS-02…OS-06 |
| H-08 | HZ-E01 | Electrical: shock | Shock at the XT30 input, the charger or the battery pack | connectors, battery bay | OS-07, OS-08 |
| H-09 | HZ-E02 | Electrical: arc, short | Arc or short circuit on the power distribution board or a damaged CAN harness | inside the robot | any powered |
| H-10 | HZ-E03 | Electrical: static | Electrostatic damage to the motion control board, CM5 or IMU during assembly | workshop | OS-07 |
| H-11 | HZ-E04 | Electromagnetic disturbance | Interference disrupts the tele-operation link or the wireless E-stop | the radio environment | OS-03…OS-06, OS-09 |
| H-12 | HZ-T01 | Thermal: burn | Actuator stators above 60 °C under sustained load | every actuator housing | OS-02…OS-04, OS-07 |
| H-13 | HZ-T02 | Thermal, chemical: battery | Thermal runaway of the lithium pack: fire, venting | battery bay, the room | OS-08…OS-10 (CFG-002) |
| H-14 | HZ-N01 | Noise | The 10 W speaker above 85 dBA at the user's ear | near the torso | any |
| H-15 | HZ-V01 | Vibration | Hand-arm vibration holding the tele-operation tablet | operator | any (low) |
| H-16 | HZ-R01 | Radiation | Optical radiation from the camera module | the head | any (low) |
| H-17 | HZ-X01 | Materials | Inhalation of MJF PA12 dust during fabrication or repair | workshop | OS-07 |
| H-18 | HZ-G01 | Ergonomic | Manual-handling injury lifting the 35 kg robot | wherever it is lifted | OS-07 |
| H-19 | HZ-V02 | Environment | Operation outside +10 to +35 °C: torque drift, BMS cut-off, plastic embrittlement | the robot | OS-10 |
| H-20 | HZ-V03 | Environment | Wet floor or moisture ingress: short circuit or slip | the floor, the robot | OS-10 |
| H-21 | HZ-P01 | Personal care: restraint | Inadequate restraint: the robot grasps or leans on a person | reach envelope | scoped out (AOU-07) |
| H-22 | HZ-P02 | Personal care: autonomous decision | A locomotion-policy edge case commands a hazardous trajectory | the reach and fall envelope | OS-06, OS-09, OS-10 |
| H-23 | HZ-P03 | Personal care: battery-powered emergency | Power loss mid-stride: an uncontrolled fall | the fall radius | OS-05, OS-06, OS-09, OS-10 |
| H-24 | HZ-P04 | Personal care: allowed contact | Contact above the force and pressure limits | contact points | OS-09, OS-10 |
| H-25 | HZ-P05 | Personal care: restraint | The robot pins or leans on a person | reach envelope | scoped out (AOU-07) |
| H-26 | HZ-P06 | Personal care: stability under load | A person leans on the robot: tip-over under external load | the fall radius | OS-09, OS-10 |
| H-27 | HZ-P07 | Personal care: cognitive overload | A confusing interface or failure annunciation | operator | OS-11 |
| H-28 | HZ-C01 | Control: loss of communication | Link lost in MOVE: the watchdog drops the robot to DAMP, and DAMP itself is a fall | the fall radius | OS-04…OS-06, OS-09, OS-11 |
| H-29 | HZ-C02 | Control, cyber: unauthorised command | An unauthorised or replayed tele-operation command moves the robot | the reach envelope | OS-11 |
| H-30 | HZ-C03 | Control: sensor failure | IMU stuck or out of range: the balance controller diverges | the fall radius | OS-03…OS-06, OS-09 |
| H-31 | HZ-C04 | Control: software fault | The control loop deadlocks and the motors hold the last command | the reach envelope | OS-02…OS-06, OS-09 |
| H-32 | HZ-C05 | Control: joint limit | A position command drives a joint into its mechanical end-stop | every joint | OS-02, OS-04, OS-09 |

Machine-readable copy: [`trace/items/hazards.yaml`](../trace/items/hazards.yaml).

## 5. Risk estimation

Two readings per row: the package's unmitigated reading for the envelope named, and the OE-1 reading with the
gantry, the tether, the bench supply, the cleared area and the operator outside reach. A dash means the hazard is
absent or carried by a measure that is not a control function.

| Hazard · situation | Envelope | S | F | P | Unmitigated PLr | OE-1 reading with the complementary measures | OE-1 PLr | Functions |
|---|---|---|---|---|---|---|---|---|
| H-01 tip-over onto a person | OE-2…OE-4 | S2 | F2 | P2 | **e** | The tether carries the fall and nobody is within the fall radius: F1, P1 | **c** (d by the same hardware) | SF-02, SF-01 (DQ-006), gantry (DM-01) |
| H-02 joint pinch in MOVE | OE-2…OE-4 | S2 | F2 | P2 | **e** | Nobody within reach of a powered limb (AOU-06); exposure only on the bench with a technician's hand: S2 F1 P1 | **c** | SF-03, SF-04, SF-25 |
| H-03 sharp edge, loose fastener | any | S1 | F2 | P1 | b (no control function) | unchanged | — | SF-05 (design), SF-12 |
| H-04 arm sweep strike | OE-2…OE-4 | S2 | F2 | P2 | **e** | Nobody within reach: F1 P1 | **c** | SF-03, SF-04, SF-06 |
| H-05 hair or clothing drawn in | OE-3, OE-4 | S2 | F1 | P2 | d | Not present in OE-1 (nobody within reach) | — | SF-07 (guarding) |
| H-06 loss of balance, uncommanded fall | all | S2 | F2 | P2 | **e** | The tether carries the fall: F2 P1 | **d** | SF-02, SF-01 (DQ-006), SF-08, SF-23 |
| H-07 trip over robot or tether | OE-3, OE-4 | S1 | F2 | P1 | b | The tether route is marked (SF-09); one observer | b | SF-09 (procedure) |
| H-08 electric shock | all | S2 | F1 | P2 | d | Bench supply at 5 V and the motor rail voltage **(unknown)**; no battery | d | SF-10 (design) |
| H-09 arc or short | all | S2 | F1 | P1 | c | Unchanged; the bench supply's current limit is a measure | c | SF-10, SF-11 |
| H-10 ESD during assembly | workshop | S1 | F2 | P1 | b | Unchanged | b | SF-12 (procedure) |
| H-11 EMI disrupts link or E-stop | OE-3, OE-4 | S2 | F1 | P2 | d | The wired pendant does not depend on radio (DQ-008): P1 | c | SF-13, SF-02 |
| H-12 hot stator | all | S1 | F2 | P1 | b | Unchanged | b | SF-14 |
| H-13 battery thermal runaway | CFG-002 | S2 | F1 | P2 | d (package: residual still very high) | No battery on CFG-001 | — | SF-15 (PL e target on CFG-002), DQ-009 |
| H-14 speaker above 85 dBA | all | S1 | F2 | P2 | c | Unchanged | c | SF-16 |
| H-15 hand-arm vibration | all | S1 | F1 | P1 | a | Unchanged | — | none (inherently low) |
| H-16 optical radiation | all | S1 | F1 | P1 | a | Unchanged | — | none (inherently low) |
| H-17 PA12 dust | workshop | S1 | F1 | P1 | a | Unchanged | — | SF-17 (PPE) |
| H-18 lifting 35 kg | all | S2 | F2 | P1 | d (no control function) | Unchanged; two-person lift | — | SF-18 (procedure) |
| H-19 outside temperature range | OE-3, OE-4 | S1 | F2 | P1 | b | Laboratory climate | — | SF-19 (restriction) |
| H-20 wet floor, moisture | OE-3, OE-4 | S2 | F1 | P2 | d | Excluded in OE-1 | — | SF-19 (restriction) |
| H-21 inadequate restraint | excluded | S2 | F1 | P2 | d | Scoped out by AOU-07 | — | — |
| H-22 policy edge case | OE-1 (CFG-002), OE-2…OE-4 | S2 | F2 | P2 | **e** | On the tether with nobody within reach: F1 P1 | **c** | SF-03 clamps, SF-23, SF-08; the policy position DQ-006 |
| H-23 power loss mid-stride | all | S2 | F1 | P2 | d | The tether carries the fall: P1 | c | SF-08, SF-02, SF-15 (CFG-002) |
| H-24 contact above limits | OE-2…OE-4 | S2 | F2 | P2 | **e** | Nobody within reach: F1 P1 | **c** | SF-04, SF-20 |
| H-25 restraint of a human | excluded | S2 | F1 | P2 | d | Scoped out by AOU-07 | — | — |
| H-26 person leans on robot | OE-3, OE-4 | S2 | F1 | P2 | d | Nobody within reach | — | SF-08, structural margin (WP-H-08) |
| H-27 cognitive overload | all | S1 | F2 | P1 | b | Unchanged | b | SF-22, information for use |
| H-28 link loss → DAMP drops the robot | all | S2 | F2 | P2 | **e** | The tether carries the fall: P1 | **d** | SF-08, SF-02; the safe state DQ-005 |
| H-29 unauthorised command | OE-2…OE-4 | S2 | F1 | P2 | d | Nobody within reach; the pendant E-stop: P1 | c | SF-21, SF-22 |
| H-30 IMU failure → divergence | all | S2 | F2 | P2 | **e** | The tether carries the fall: P1 | **d** | SF-23 |
| H-31 control-loop deadlock | all | S2 | F2 | P2 | **e** | The tether carries the fall; nobody within reach: P1 | **d** | SF-24, SF-08 |
| H-32 joint limit overshoot | OE-2…OE-4 | S1 | F2 | P2 | c | Unchanged | c | SF-25 |

### 5.1 Counts

Nine rows read **e** unmitigated (H-01, H-02, H-04, H-06, H-22, H-24, H-28, H-30, H-31). With the OE-1
complementary measures none stays at e: four read d (H-06, H-28, H-30, H-31), the rest c or lower. The package's
ISO 10218-1 default of PL d, Category 3 is adopted as the floor for every stop and fall function regardless of a
lower graph reading (§2 step 3), pending DQ-004. Rows for OE-2…OE-4 stay at their unmitigated reading and are
excluded from the first item (DQ-002).

### 5.2 What the second reading relies on

The OE-1 reading is only as good as the gantry (DQ-007), the cleared area, the wired E-stop (DQ-008) and the operator
outside reach (AOU-01, AOU-06). Each is a complementary measure of WP-C-05 and a condition of WP-V-07; if any is
absent the unmitigated reading applies and no powered floor test runs.

## 6. Risk evaluation and reduction

| Measure | Kind (ISO 12100 step) | Reduces | Status at BL-001 |
|---|---|---|---|
| DM-01 Gantry and rated tether, quick-release, dynamic-load sized | Complementary protective measure (step 2) | H-01, H-06, H-22, H-23, H-28, H-30, H-31 in OE-1 | Does not exist; DQ-007 |
| DM-02 Wired dual-channel E-stop in the operator's hand removing the motor rail; surveilled wireless receiver | Safeguarding (step 2), SF-13 | H-11, H-28, H-29, every limb hazard | Does not exist; DQ-008 |
| DM-03 Bench supply with current limit in place of a battery | Inherently safe design of the configuration (step 1) | H-08, H-09, H-13, H-23 in OE-1 | Procedure; DQ-009 for CFG-002 |
| DM-04 Cleared and marked area; nobody within reach of a powered limb | Information for use and organisation (step 3) | H-02, H-04, H-05, H-24, H-26 | Procedure; WP-V-07 |
| DM-05 Mechanical end-stops, chamfered edges, locked fasteners, labyrinth guards at waist and neck | Inherently safe design (step 1), SF-05, SF-07, SF-25 | H-02, H-03, H-05, H-32 | Partly in the CAD; unverified (GAP-24, GAP-26) |
| DM-06 Material certificates, harness acceptance test, commissioning checks | Information for use and production control (step 3) | H-01, H-06, H-09 via FM-02, FM-18 | Does not exist; WP-O-01 |

The adequacy argument per row is [WP-C-05](WP-C-05-risk-reduction-concept.md) (skeleton at v0.1; GAP-01).

## 7. Safety functions

The 25 functions of the package are kept with their numbers. Seventeen carry a PLr; eight are static measures or
procedures and carry none.

| ID | Safety function | PLr (package) | PLr adopted for OE-1 | Hazards | Note |
|---|---|---|---|---|---|
| SF-01 | Maintain bipedal stability while standing and moving | d | d, **allocation pending DQ-006**; withdrawn as a safety function if the policy may not carry it | H-01, H-06, H-22 | the gantry carries stability meanwhile |
| SF-02 | Detect an impending fall and arrest it by a controlled descent before impact | d | d | H-01, H-06, H-23, H-28 | the safe state is DQ-005 |
| SF-03 | Joint torque and velocity limit per joint | d | d | H-02, H-04, H-24 | limits DQ-014 |
| SF-04 | Force-limited contact in collaborative regions | d | d (not claimed in OE-1: nobody within reach) | H-02, H-04, H-24 | OE-2 |
| SF-05 | Fastener torque and secure-by-design; chamfered edges | — | — | H-03 | static |
| SF-06 | Speed reduction in human-shared regions on a perception trigger | c | c (not claimed in OE-1) | H-04 | the trigger has no safety-rated sensor (WP-C-10) |
| SF-07 | Guarding at the waist yaw and neck yaw | — | — | H-05 | static |
| SF-08 | Safe stop on watchdog timeout or communication loss (stop category 1) | d | d | H-06, H-23, H-26, H-28 | ends in the safe state of DQ-005 |
| SF-09 | Cable management and a visible tether route | — | — | H-07 | procedure |
| SF-10 | Power isolation: lockable disconnector and insulation class | — | — | H-08, H-09 | static |
| SF-11 | Overcurrent protection on each motor branch | c | c | H-09 | |
| SF-12 | ESD-safe assembly process | — | — | H-10 | procedure |
| SF-13 | Emergency-stop devices and wireless link surveillance | d | d | H-11, H-28, every limb hazard | devices DQ-008; stop category DQ-016 |
| SF-14 | Stator over-temperature shutdown | c | c | H-12 | |
| SF-15 | Battery thermal and cell-voltage protection by the BMS | e | e on CFG-002; absent on CFG-001 | H-13, H-23 | DQ-009 |
| SF-16 | Audio limiter at or below 80 dBA at 1 m | b | b | H-14 | |
| SF-17 | Respiratory protection during MJF dust generation | — | — | H-17 | procedure |
| SF-18 | Two-person lift for the 35 kg robot | — | — | H-18 | procedure |
| SF-19 | Indoor-only operating envelope until an IP-rated build exists | — | — | H-19, H-20 | restriction |
| SF-20 | Power-and-force limiting per ISO/TS 15066 in collaborative mode | d | d (not claimed in OE-1) | H-24 | OE-2 |
| SF-21 | Authenticated, integrity-protected tele-operation channel | c | c | H-29 | SL target DQ-012 |
| SF-22 | Operator session lock and idle timeout | b | b | H-27, H-29 | |
| SF-23 | IMU plausibility and cross-check | d | d | H-30 | second IMU for the second channel (DFMEA FM-12) |
| SF-24 | Real-time scheduler watchdog and deadline monitor | d | d | H-31 | |
| SF-25 | Software joint limits inside the mechanical end-stops | c | c | H-32 | |

Machine-readable copy: [`trace/items/hazards.yaml`](../trace/items/hazards.yaml); specification: [WP-C-04](WP-C-04-safety-functions-and-plr.md).

## 8. Residual risk and conditions

No powered floor test is inside this assessment until DM-01, DM-02, DM-03 and DM-04 exist (WP-V-07). No operation
with a person within reach of a powered limb is inside it at all (OE-2…OE-4 excluded). With those conditions the
residual risk of OE-1 is dominated by the bench technician's exposure to pinches (H-02, OE-1 reading c) and by the
tether's own integrity (a new hazard the gantry introduces, to be rated in WP-C-05 §3.3).

## 9. Hazard log cross-references

| Hazard | Package ID | Gap findings | Safety functions | Defeaters |
|---|---|---|---|---|
| H-01, H-06 | HZ-M01, HZ-M07 | GAP-03, GAP-04, GAP-09, GAP-10, GAP-13 | SF-01, SF-02, SF-08 | DF-03, DF-04, DF-09, DF-10, DF-13 |
| H-02, H-04, H-24 | HZ-M02, HZ-M04, HZ-P04 | GAP-05, GAP-06 | SF-03, SF-04, SF-06, SF-20 | DF-05, DF-06 |
| H-08, H-09, H-13, H-23 | HZ-E01, HZ-E02, HZ-T02, HZ-P03 | GAP-08, GAP-12, GAP-23 | SF-10, SF-11, SF-15 | DF-08, DF-12, DF-23 |
| H-11, H-28 | HZ-E04, HZ-C01 | GAP-07, GAP-10, GAP-11, GAP-20 | SF-08, SF-13 | DF-07, DF-10, DF-11, DF-20 |
| H-22, H-30, H-31 | HZ-P02, HZ-C03, HZ-C04 | GAP-13, GAP-16, GAP-17, GAP-21 | SF-23, SF-24, SF-03 | DF-13, DF-16, DF-17, DF-21 |
| H-29, H-27 | HZ-C02, HZ-P07 | GAP-18, GAP-19 | SF-21, SF-22 | DF-18, DF-19 |

## 10. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Apply DQ-004 (target PL) and DQ-005 (safe state) to §5 and §7 when answered | SM | G1 |
| OI-2 | Reviewer with build or operating experience confirms every rating (ACT-006) | VR | G1 |
| OI-3 | Re-rate §5 against the interaction scenarios and misuse cases of WP-C-06 once written | SM | G1 |
| OI-4 | Rate the hazards the gantry and tether introduce (tether failure, entanglement, a suspended robot swinging) in WP-C-05 §3.3 and here | SM | G1 |
| OI-5 | Weigh the robot and bound the fall energy (ACT-001); replace the package's 411 J estimate | EM | G1 |
