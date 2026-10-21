# WP-V-03 Human detection, speed reduction and power-and-force limiting validation

| Field | Value |
|---|---|
| Work product | WP-V-03 Human detection, speed reduction and power-and-force limiting validation |
| Standard reference | Machinery: 10218-2 §5; TS 15066 §5.5; 13482 §5.7, §7; SRP/CS: 13849-1 §10; Other: ISO 13857; ASPICE: VAL.1 |
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

Human detection, speed reduction and power-and-force limiting validation: that SF-06 reduces speed when a person is in the shared region, that SF-04 and SF-20 keep contact forces and pressures within ISO/TS 15066 Annex A, and that the pinch gaps of SF-07 meet ISO 13857. Contact and speed limits are those of WP-S-04 at the measured descent and stop times of WP-V-02.

## 2. Test specification

PD-nn: body-region test fixtures, approach cases, expected force and pressure, per joint and per operating envelope. Pass criteria are the ISO/TS 15066 Annex A values with the 0.75 factor on the arm and hand values (DQ-028 A, 2026-10-21); a measured contact above the factored value fails even below the published one.

## 3. Blind zones

What the camera and IMU do not detect (WP-C-10), and the operating-envelope limit that covers it.

## 4. Report

Results; the hold point for operation with people in reach (WP-M-01 §7).

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G4 |
