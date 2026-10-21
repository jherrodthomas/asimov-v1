# WP-M-08 Cybersecurity plan

| Field | Value |
|---|---|
| Work product | WP-M-08 Cybersecurity plan |
| Standard reference | IEC 62443: 62443-4-1 §5 (SM-1…SM-13); 62443-4-2 §4; ASPICE: MAN.7 (CS) |
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

Cybersecurity plan under IEC 62443-4-1: the secure development practices applied to the fork's software, the roles, the security level target the lead sets and the schedule of cybersecurity work products.

## 2. Scope and assets

The tele-operation channel (WebRTC data channel from the operator app to the Raspberry Pi 5), the Asimov API, the Raspberry Pi 5 to motion-control-board link, the firmware and policy images, the update path, the wireless E-stop link.

## 3. Practices

SM-1…SM-13, SR, SD, SI, SVV, DM, SUM, SG with the work product that evidences each.

## 4. Roles

Cybersecurity manager; external cybersecurity reviewer and assessor (WP-M-06 §7).

## 5. Security level target

Decision DQ-012; the target per foundational requirement is recorded in WP-C-08 once answered.

## 6. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G0 |
