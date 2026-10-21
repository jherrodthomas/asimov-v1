# WP-H-04 Reliability data and PL calculation (MTTFD, DCavg, CCF, SISTEMA)

| Field | Value |
|---|---|
| Work product | WP-H-04 Reliability data and PL calculation (MTTFD, DCavg, CCF, SISTEMA) |
| Standard reference | SRP/CS: 13849-1 §6, Annex C–F, Annex K |
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

Reliability data and the PL calculation per safety function: MTTFD per channel, DCavg, CCF score (Annex F) and the resulting PL against the PLr, in a SISTEMA project. The concept-phase package could not compute any of it because upstream publishes no actuator or board failure rates (GAP-14).

## 2. Reliability data

Per component: source (certificate, B10d, datasheet, Annex C table), value, justification; the actuator and encoder data upstream must supply (WP-M-10).

## 3. Calculation per safety function

Category, MTTFD, DCavg, CCF, PL; margins.

## 4. SISTEMA project

Kept under configuration control as a configuration item.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G3 |
