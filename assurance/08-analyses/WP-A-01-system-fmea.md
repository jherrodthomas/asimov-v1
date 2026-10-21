# WP-A-01 System FMEA (seeded by the concept-package system FMEA and DFMEA)

| Field | Value |
|---|---|
| Work product | WP-A-01 System FMEA (seeded by the concept-package system FMEA and DFMEA) |
| Standard reference | SRP/CS: 13849-1 §6; Other: IEC 60812 |
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

System FMEA of the robot's safety-related elements and functions, seeded by the system-level FMEA (23 rows) and the DFMEA (32 failure modes) of the concept-phase package.

## 2. Scope

Actuators, motion control board, IMU, CAN buses, edge board, power distribution, BMS, wireless E-stop, harness, structure, the simulation model and the locomotion policy.

## 3. Worksheet

Element, function, failure mode, effect, cause, S, O, D, action priority, mitigation and the safety function it maps to; ported from `08_FMEA` and `05_DFMEA_Worksheet`.

## 4. Findings

Requirements to WP-S-02 and WP-H-01; defeaters to WP-K-01.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G2 |
