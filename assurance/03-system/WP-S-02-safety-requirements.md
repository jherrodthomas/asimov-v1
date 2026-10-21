# WP-S-02 Safety requirements specification for the SRP/CS

| Field | Value |
|---|---|
| Work product | WP-S-02 Safety requirements specification for the SRP/CS |
| Standard reference | Machinery: 10218-1 §5.4; 13482 §6; SRP/CS: 13849-1 §5; 62061 §6; Other: 60204-1 §9; ASPICE: SYS.2 |
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

Safety requirements specification for the safety-related parts of the control system: one block per safety function of WP-C-04, each requirement SR-nn.mm testable, with category, response time, fault reaction and verification method; ported and reworked from the 63 safety requirements of the concept-phase workbook (SYRS, SRS, HwRS).

## 2. Conventions

SR-<SF>.<nn>; every requirement names its safety function, its verification method (I, A, T, D) and the test case that verifies it.

## 3. Requirements common to every safety function

Priority over every command, reset rules, indication, parameter protection, behaviour on power loss.

## 4. Requirements per safety function

SF-01 stability, SF-02 fall arrest and controlled descent, SF-03 joint torque and velocity limits, SF-04 force-limited contact, SF-06 speed reduction near people, SF-08 safe stop on watchdog or comms loss, SF-11 overcurrent, SF-13 E-stop link surveillance, SF-14 stator over-temperature, SF-15 battery protection, SF-16 audio limiter, SF-20 power-and-force limiting, SF-21 authenticated tele-operation, SF-22 session lock, SF-23 IMU plausibility, SF-24 scheduler watchdog, SF-25 joint limits.

## 5. Security requirements supporting the safety functions

From WP-C-08.

## 6. Verification plan summary

Which test of WP-V-01…WP-V-05 verifies each block; the 139 test cases of the concept-phase test plan are the seed.

## 7. Traceability

To WP-C-03 hazards, WP-C-04 functions, WP-H-01, WP-W-02, and the trace data of WP-T-01.

## 8. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G2 |
