# WP-S-01 System requirements specification (functional, non-safety)

| Field | Value |
|---|---|
| Work product | WP-S-01 System requirements specification (functional, non-safety) |
| Standard reference | ASPICE: SYS.2 |
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

System requirements specification for the functional (non-safety) behaviour: locomotion, tele-operation, telemetry, audio, API; ported from the SyRS of the concept-phase requirements workbook (35 system requirements, of which the safety ones go to WP-S-02).

## 2. Requirements

SYS-nn ported from `Asimov_v1_Requirements.xlsx` tab 02_SyRS with their type, priority, rationale, allocation and verification method.

## 3. Interfaces

Tele-operation channel, Asimov API, six CAN buses (C0 left leg, C1 right leg, C2 right arm, C3 left arm, C4 waist and neck, C5 BMS), the motion-control-board ports.

## 4. Traceability

To WP-C-01 functions F-01…F-nn; the safety requirements are in WP-S-02.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G2 |
