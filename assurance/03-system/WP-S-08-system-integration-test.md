# WP-S-08 System integration and test strategy, specification and report

| Field | Value |
|---|---|
| Work product | WP-S-08 System integration and test strategy, specification and report |
| Standard reference | SRP/CS: 13849-1 §8; IEC 62443: 62443-4-1 SVV-1; ASPICE: SYS.4 |
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

System integration and test strategy, specification and report: how hardware, software and the chain are integrated on the bench and on the robot, in what order, with which tests at each step.

## 2. Strategy

Bench first (actuators on a stand, MCB with the MuJoCo model in the loop), then the robot on the gantry, then the robot on the floor under the tether, then free-standing in OE-1.

## 3. Specification

IT-nn integration tests: interface by interface, per WP-S-05.

## 4. Report

Results per baseline.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G4 |
