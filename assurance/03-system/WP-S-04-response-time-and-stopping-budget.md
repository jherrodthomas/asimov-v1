# WP-S-04 Response time, fall-arrest and stopping budget (controlled descent, joint stop, safe state per mode)

| Field | Value |
|---|---|
| Work product | WP-S-04 Response time, fall-arrest and stopping budget (controlled descent, joint stop, safe state per mode) |
| Standard reference | Machinery: 13482 §5.10, §5.13; SRP/CS: 13849-1 §5 (response time); ASPICE: SYS.3 |
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

Response time, fall-arrest and stopping budget: for each safety function the time from demand to the start of the safe state, and for the biped the controlled-descent and joint-stop budgets that replace a wheeled machine's stopping distance; what the actuators, the IMU and the chain contribute, and what the tests of WP-V-02 must measure.

## 2. Purpose, inputs and conventions

Response targets of WP-C-04 §2 (≤ 10 ms torque limit, ≤ 20 ms balance, ≤ 100 ms watchdog, ≤ 200 ms fall arrest, ≤ 500 ms E-stop); the mode machine; the MuJoCo model as the only dynamics data at BL-001.

## 3. Response time budget per safety function

Sensor, bus, controller, actuator and contactor contributions per function; the tele-operation heartbeat timeout of 250 ms with a one-sample grace (DQ-038 A, 2026-10-21) is the first term of the SF-08 budget; the tether catches the robot at knee height, about 0.4 m at the centre of mass, until the controlled descent is verified (DQ-043 A), which bounds the fall energy the budget must cover.

## 4. Fall-arrest and controlled-descent model

Time to detect a fall from IMU rate and attitude, time to reach a crouch or kneel, energy at contact. The controlled descent the budget assumes is bounded by the fall energy and tip-over margin of WP-H-08. The planning assumption that power removal (DAMP) is the safe state is decision DQ-005.

## 5. Safe state per mode

DAMP, STAND, MOVE: what the safe state is in each, how long it takes to reach, and what the tether carries meanwhile.

## 6. Speed and reach limits per operating envelope

Joint velocity and torque limits per envelope; demonstration speed in OE-1.

## 7. Verification: what is measured, where

WP-V-02 and WP-V-04; the parameters handed to WP-W-09.

## 8. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G2 |
