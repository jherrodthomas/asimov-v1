# WP-H-03 Hardware failure analysis (FMEA, fault lists, fault exclusions; seeded by the concept-package DFMEA)

| Field | Value |
|---|---|
| Work product | WP-H-03 Hardware failure analysis (FMEA, fault lists, fault exclusions; seeded by the concept-package DFMEA) |
| Standard reference | SRP/CS: 13849-1 §6; 13849-2 Annex A–D; Other: IEC 60812; ASPICE: HWE.2 |
| Version | 0.0 (skeleton: structure, clause map and seeds from the concept-phase package; 2026-10-21) |
| Status | Skeleton |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `3d4ec9d` (BL-001) |

> [!NOTE]
> **Skeleton.** The structure and clause mapping exist; the content is still to be written. The gate that needs this
> work product is **G3** ([WP-M-00](../01-management/WP-M-00-work-product-register.md#3-register)).

## 1. Purpose

Hardware failure analysis of the safety-related hardware: FMEA, fault lists and fault exclusions per ISO 13849-2 Annexes A–D for the E-stop chain, the contactors, the actuators, the IMU, the CAN transceivers, the power distribution board and the BMS. Seeded by the 32 failure modes of the concept-phase DFMEA (`Asimov_v1_DFMEA.xlsx`).

## 2. Scope

Elements E-nn of WP-S-03.

## 3. Failure modes

FM-nn ported from the DFMEA worksheet with severity, occurrence, detection and action priority; the 19 high-priority items first (hip-yoke fatigue, material substitution, actuator runaway, CAN bus-off, watchdog not armed, E-stop link silent failure, BMS missing).

## 4. Fault lists and exclusions

Per component: the ISO 13849-2 fault list applied, each exclusion with its justification.

## 5. Fault reaction

What detects each fault and within what time (WP-S-04).

## 6. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G3 |
