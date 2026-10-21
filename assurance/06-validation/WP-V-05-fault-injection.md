# WP-V-05 Fault injection and fault-list validation specification and report

| Field | Value |
|---|---|
| Work product | WP-V-05 Fault injection and fault-list validation specification and report |
| Standard reference | SRP/CS: 13849-2 §5, Annex A–D; ASPICE: SYS.4, SWE.6 |
| Version | 0.0 (skeleton: structure, clause map and seeds from the concept-phase package; 2026-10-21) |
| Status | Skeleton |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `3d4ec9d` (BL-001) |

> [!NOTE]
> **Skeleton.** The structure and clause mapping exist; the content is still to be written. The gate that needs this
> work product is **G4** ([WP-M-00](../01-management/WP-M-00-work-product-register.md#3-register)).

## 1. Purpose

Fault injection and fault-list validation: the faults of WP-H-03 and WP-W-04 injected on the bench and the robot, with the expected reaction of WP-S-03 and the observed one.

## 2. Test specification

FI-nn per fault: encoder stuck, IMU saturated, CAN bus-off on a leg bus, loss of a thermistor, actuator runaway command, watchdog not fed, BMS handshake absent, policy output out of range.

## 3. Report

Results; faults not injectable and why.

## 4. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G4 |
