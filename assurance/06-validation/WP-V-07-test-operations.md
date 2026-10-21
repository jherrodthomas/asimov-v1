# WP-V-07 Test Operations and Safety Procedures for Powered Testing

| Field | Value |
|---|---|
| Work product | WP-V-07 Test operations and safety procedures for powered testing (hold point: tether, gantry, E-stop, cleared area) |
| Standard reference | ISO 12100:2010 §6.4 (information for use, including for the development phase), §6.3 (safeguarding and complementary protective measures); ISO 13482:2014 §7 (verification and validation, test conditions); ISO 10218-2:2011 §5 (safeguarding during commissioning); ISO 13850:2015 §4 (emergency stop function, as bench equipment); IEC 60204-1:2018 §5.3 (supply disconnecting device), §7.2 (overcurrent protection); ASPICE 4.0 VAL.1 |
| Version | 0.3 (2026-10-21): DQ-021 A, DQ-022 A, DQ-014 A and DQ-024 A applied to §2, §3 and §4. 0.2 (2026-10-21): the bench equipment decided (DQ-007 A, DQ-008 A, DQ-009 A); the two-person rule is DQ-022. 0.1 (initial procedure; 2026-10-21) |
| Status | Draft |
| PL / scope | Development testing only. No PL is claimed for the bench equipment |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `3d4ec9d` (BL-001) |

## 1. Purpose

This procedure is the **hold point** of [WP-M-01 §7](../01-management/WP-M-01-assurance-strategy.md#7-phases-gates-and-sequence):
no Asimov v1 unit is powered with its feet on the floor under the fork's control until the conditions below hold. It
exists because the kit robot as inherited has no documented emergency stop, no fall-arrest function, no declared
joint limits, no power distribution record and no safe state better than a fall ([gap assessment](../00-assessment/gap-assessment.md)
GAP-07, GAP-08, GAP-10, GAP-06). The procedure makes the next months of testing defensible without claiming any
Performance Level: it relies on a gantry, bench equipment and the operator, and says so.

It applies to every powered test with the robot assembled, from the first hang test to the validation runs of
[WP-V-01](WP-V-01-safety-validation.md). Actuator tests on a bench stand with a single limb (WP-C-02 T-01) are
outside it but follow §3.

## 2. Conditions before any powered test with the robot assembled

| # | Condition | Evidence | Closes |
|---|---|---|---|
| C-1 | An overhead gantry or rated anchor point with a tether rated for the robot's mass under a dynamic load (fall factor and shock allowance **(TBC)**), a quick-release the operator can reach, and a lowering mechanism so that the feet touch the floor only when intended (DQ-007) | Rating labels, photo and sketch in the change record under [`07-supporting/impact/`](../07-supporting/impact/README.md); a static load test to **(TBC: 2×)** the robot's mass before first use | GAP-03 (bench), H-01, H-06, H-23, H-28 |
| C-2 | A wired, dual-channel emergency stop (two NC contacts, red mushroom button, latching) on a pendant in the operator's hand, through a safety relay or two contactors, that removes the actuator rail; re-arm needs a deliberate action at the pendant with the button released. The kit's wireless E-stop may be fitted in addition but does not count until its link is surveilled (DQ-008) | Wiring sketch in the change record; a functional test before every session (§4) | GAP-07, GAP-11 (bench) |
| C-3 | A bench power supply with a current limit and a switch within the operator's reach feeds the actuator rail in place of a battery; no battery is on the robot (DQ-009) | Supply model and settings in the test log | GAP-08, GAP-12 (bench) |
| C-4 | The test area meets the OE-1 limits of WP-C-02 §4 (10 to 35 °C, non-condensing, sealed dry floor with slope at most 1 %, at least 200 lux, no steps, indoors; DQ-021 A) and is defined, level, dry and marked: the reach envelope plus 1 m on every side; nobody inside it while the rail is powered except as §3 allows; the operator's station and the observer's station outside it on opposite sides (WP-C-02 §6) | Area sketch in the test log | WP-C-02 OE-1 |
| C-5 | Every joint's torque and velocity limit the firmware enforces is known and recorded, or the test runs with the actuators' hardware current limits set to a value the test plan names (DQ-014) | Parameter record; the firmware version read before the test | GAP-06 (bench) |
| C-6 | The firmware or controller build is identifiable (version, hash) and its behaviour on heartbeat loss, E-stop and fault is written down before the test; where upstream's firmware is used as released, its release notes are the record | Build manifest in the test log | GAP-16 (bench) |
| C-7 | The robot has been weighed, its lifting points and two-person lift are agreed, and the material and harness acceptance checks of WP-O-01 (as far as they exist) are recorded for the unit | Acceptance record | GAP-04, GAP-22 (bench) |
| C-8 | Two people for every powered test with the robot assembled (DQ-022 A, decided 2026-10-21): the operator, who has read this procedure, is trained per WP-M-04 and has run the pre-session checks of §4, and one observer; single-limb bench tests on a stand (T-01) may be run alone | Signed lines of both in the test log | WP-M-04 competence; WP-C-02 T-01 |

Conditions C-1 to C-3 are the bench equipment of [WP-M-02 §4.1](../01-management/WP-M-02-safety-plan.md#41-early-implementation-of-at-risk-work);
the lead decided them on 2026-10-21 (DQ-007 A: gantry and rated tether; DQ-008 A: wired dual-channel pendant
plus the surveilled wireless device; DQ-009 A: bench supply, no battery on CFG-001). Until the equipment exists, every
activity on the kit robot is bench work with single limbs on a stand or the robot hanging with its feet off the floor
(WP-C-02 T-01, T-02), under C-2 to C-8 as far as they apply.

## 3. Limits during development testing

| Limit | Value | Source |
|---|---|---|
| People inside the area while the rail is powered | None. A technician may enter only with the rail switched off at the bench supply and the E-stop pressed | No contact limit is measured (GAP-05); AOU-06 |
| Joint torque and velocity | The limits of C-5: half the MuJoCo control range per joint and the velocity ceiling of WP-S-04 until measured (DQ-014 A, decided 2026-10-21) | WP-C-01 §4 |
| Feet on the floor | Only with the gantry lowered to a tether slack that lets the robot stand but not fall below **(TBC: knee height)** | C-1 |
| Walking | Not before a controller exists, is identified (C-6) and has been run in the hang test; within the gantry span only | WP-C-02 T-05 |
| Deliberate falls and power cuts | Only as the bounded campaign of WP-V-02 (DQ-024 A, decided 2026-10-21): from standing, caught by the tether above knee height, nobody inside the area, an inspection after each and the spares budget of DQ-026 agreed before the first | WP-V-02 |
| Battery | None on the robot | C-3; DQ-009 |
| Session length | Thermal readout of every actuator logged every **(TBC: 10 min)**; stop at 60 °C stator temperature | H-12 |
| Wireless E-stop | Carried by the observer if fitted; not relied on | C-2 |

## 4. Pre-session and per-session checks

1. Inspect the gantry, tether, shackles and quick-release; confirm the rating labels; log it.
2. With the robot hanging and the rail powered, press and release the pendant E-stop: every actuator must lose
   power and not restart until the re-arm is pressed. Log the result.
3. Read the firmware or controller version and compare with the planned build (C-6). Log it.
4. Confirm the bench supply model, voltage and current limit; confirm no battery is fitted.
5. Walk the area; confirm markings and the absence of other people; confirm the observer's station.
6. Move one joint of one limb at the planned limit with the robot hanging and press the E-stop; confirm the stop.
7. Confirm the observer is present and at their station (DQ-022 A); a session with the assembled robot does not start without them.
8. Only then start the planned test.

A failed check ends the session.

## 5. Test log

Every session has a log entry in [`06-validation/test-sites/`](test-sites/README.md): date, operator, observer,
build, supply settings, tether configuration, pre-session check results, the tests run with their references (WP-V-02,
V-03, V-04, V-05, V-01), anomalies, falls or tether loads, and the E-stop presses with their reasons.

## 6. Anomalies

Any unexpected motion, any fall or tether load that was not planned, any contact with a person or object, any
failure of a pre-session check, and any E-stop press that was not planned is a safety anomaly
([WP-M-02 §9](../01-management/WP-M-02-safety-plan.md#9-safety-anomaly-handling)). Testing stops; the anomaly is
raised as an issue labelled `safety-anomaly`; the safety manager lifts the stop in writing after the cause is
understood.

## 7. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Specify and buy or build the gantry and tether (DQ-007 A, decided 2026-10-21; ACT-009); record the rating and the load test | test bench owner | Before the first hang test |
| OI-2 | Specify and build the wired E-stop pendant and contactor chain (DQ-008 A, decided 2026-10-21; ACT-004) | EM | Before the first hang test |
| OI-3 | Name and train the test operator(s) (WP-M-02 §3.1) | PM | Before the first powered test |
| OI-4 | Replace the §3 limits with the budget of WP-S-04 and the parameters of WP-W-09 once set (DQ-014) | SRP | G2 |
| OI-5 | Define the test area in WP-C-02 §6 with a sketch and reference it here | SM | G1 |
