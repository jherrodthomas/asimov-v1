# WP-S-03 Technical safety concept: stop chain and safety-related control architecture (E-stop and motor-rail removal, the MCB safety layer, designated architectures, categories, channels, diagnostics, allocation of SF-01…SF-25)

| Field | Value |
|---|---|
| Work product | WP-S-03 Technical safety concept: stop chain and safety-related control architecture (E-stop and motor-rail removal, the MCB safety layer, designated architectures, categories, channels, diagnostics, allocation of SF-01…SF-25) |
| Standard reference | Machinery: 10218-1 §5.4, §5.5; SRP/CS: 13849-1 §6; Other: 60204-1 §9.4; ASPICE: SYS.3 |
| Version | 0.0 (skeleton: structure, clause map and seeds from the concept-phase package; 2026-10-21) |
| Status | Skeleton |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `3d4ec9d` (BL-001) |

> [!NOTE]
> **Skeleton.** The structure and clause mapping exist; the content is still to be written. The gate that needs this
> work product is **G2** ([WP-M-00](../01-management/WP-M-00-work-product-register.md#3-register)).

## 1. Purpose

The technical safety concept: the stop chain and the safety-related control architecture that implement the safety functions of WP-C-04 at their required PL, with designated architectures, categories, channels, diagnostic coverage and the allocation of SF-01…SF-25 to elements.

## 2. The argument in one paragraph

A hardwired E-stop chain removes motor power independently of every processor (SF-13 with the wired device of OE-1); the motion-control-board safety layer is a deterministic checker between the locomotion policy or the tele-operator and the actuators (torque and velocity clamps, IMU plausibility, watchdog, mode machine); the locomotion policy and the tele-operation stack are functional layers with no PL claim. The chain has no network input: every element that can remove motor power is wired, so no input of the safety chain is reachable from the network; the cybersecurity architecture (WP-S-07) keeps it a zone of its own. The safe state of a biped is not power removal alone (DQ-005): the architecture must say what removes power, what holds position and what lowers the robot.

## 3. Allocation of safety functions to elements

E-nn elements (E-stop devices and receiver, motor-rail contactors, the MCB safety layer, actuator drive limits, thermistors, the BMS, the tether) against SF-01…SF-25 with channel structure and category.

## 4. Architecture

Per function: Category B to 4 designated architecture, diagnostics, fault reaction, reset. The wired dual-channel pendant on the tether plus the kit's wireless device with heartbeat surveillance (DQ-008 A, decided 2026-10-21); stop category 0 (DQ-005 A).

## 5. Command arbitration and modes

DAMP, STAND, MOVE and the transitions the safety layer allows (SRS-003 of the concept-phase package); who may command what.

## 6. Safety parameters

The parameters of WP-W-09 the architecture relies on.

## 7. Indication and diagnostics

Armed state, mode, fault class, visible and audible.

## 8. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G2 |
