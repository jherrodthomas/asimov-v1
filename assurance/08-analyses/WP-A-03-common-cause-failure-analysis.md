# WP-A-03 Common cause failure analysis

| Field | Value |
|---|---|
| Work product | WP-A-03 Common cause failure analysis |
| Standard reference | SRP/CS: 13849-1 §6, Annex F |
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

Common cause failure analysis of the two-channel functions (ISO 13849-1 Annex F scoring): shared power, shared CAN buses, shared IMU, shared firmware, the same connector family on every actuator, environmental stresses.

## 2. Scoring

Per two-channel function: separation, diversity, design, assessment, competence, environment; score against the 65 threshold.

## 3. Measures

Second IMU on a separate bus (FM-12), separate E-stop channels, diverse monitoring.

## 4. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G2 |
