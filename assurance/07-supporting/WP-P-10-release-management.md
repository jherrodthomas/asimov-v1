# WP-P-10 Release management and baseline procedure

| Field | Value |
|---|---|
| Work product | WP-P-10 Release management and baseline procedure |
| Standard reference | SRP/CS: 61508-1 §6.2.3; IEC 62443: 62443-4-1 SUM-1…SUM-5; Other: Machinery Reg. Annex V; ASPICE: SUP.8 |
| Version | 0.0 (skeleton: structure, clause map and seeds from the concept-phase package; 2026-10-21) |
| Status | Skeleton |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `3d4ec9d` (BL-001) |

> [!NOTE]
> **Skeleton.** The structure and clause mapping exist; the content is still to be written. The gate that needs this
> work product is **G5** ([WP-M-00](../01-management/WP-M-00-work-product-register.md#3-register)).

## 1. Purpose

Release management and baseline procedure: what a fork release contains (record snapshot, firmware and policy images once they exist, parameter sets, information for use), how it is tagged, built reproducibly, verified and recorded (WP-K-06).

## 2. Release contents

Per release: baseline record, images, parameters, documents, checksums.

## 3. Procedure

Freeze, build, verify, sign, record, publish; updates per WP-O-05.

## 4. Rules

No release without a passed G5 and a signed release record.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G5 |
