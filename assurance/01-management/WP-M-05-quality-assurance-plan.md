# WP-M-05 Quality management and quality assurance plan (design control, records, nonconformance)

| Field | Value |
|---|---|
| Work product | WP-M-05 Quality management and quality assurance plan (design control, records, nonconformance) |
| Standard reference | SRP/CS: 61508-1 §6.2; IEC 62443: 62443-4-1 SM-5; Other: ISO 9001 §7.5, §8.3, §8.7, §10.2 (informative); ASPICE: SUP.1 |
| Version | 0.0 (skeleton: structure, clause map and seeds from the concept-phase package; 2026-10-21) |
| Status | Skeleton |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `3d4ec9d` (BL-001) |

> [!NOTE]
> **Skeleton.** The structure and clause mapping exist; the content is still to be written. The gate that needs this
> work product is **G0** ([WP-M-00](WP-M-00-work-product-register.md#3-register)).

## 1. Purpose

Quality management and quality assurance for the fork: design control, records, calibration, nonconformance and corrective action, audits. ISO 9001 is informative; the concept-phase package rated the inherited project against it (six findings, GAP-27…GAP-32) and this plan is where they close.

## 2. Quality objectives

Records of design review, test, calibration and nonconformance exist and are kept under configuration control; every generated file is checked by CI.

## 3. Design and development control

Design reviews per gate with recorded attendees, decisions and actions (ISO 9001 §8.3, GAP-28).

## 4. Nonconformance and corrective action

A nonconformance register and a corrective-action procedure (ISO 9001 §8.7, §10.2; GAP-30, GAP-32), run through [WP-P-03](../07-supporting/WP-P-03-problem-resolution.md).

## 5. QA audits

Process and work-product audits per gate; independence per WP-M-06 §3.

## 6. DIY-kit production

Process controls the kit builder follows (ISO 9001 §8.5.1, GAP-29) are information for use (WP-O-01), with acceptance checks.

## 7. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G0 |
