# WP-P-05 Verification and review procedure

| Field | Value |
|---|---|
| Work product | WP-P-05 Verification and review procedure |
| Standard reference | SRP/CS: 13849-1 §8; 61508-1 §7.18; IEC 62443: 62443-4-1 SVV-1; ASPICE: SUP.2 |
| Version | 0.0 (skeleton: structure, clause map and seeds from the concept-phase package; 2026-10-21) |
| Status | Skeleton |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `3d4ec9d` (BL-001) |

> [!NOTE]
> **Skeleton.** The structure and clause mapping exist; the content is still to be written. The gate that needs this
> work product is **G0** ([WP-M-00](../01-management/WP-M-00-work-product-register.md#3-register)).

## 1. Purpose

Verification and review procedure: how a work product or code change is reviewed, by whom, at what independence level, and what record is kept; what moves a work product from Draft to Approved.

## 2. Review types

Verification review (pull request), confirmation review (WP-M-06), audit, assessment.

## 3. Independence

I0…I3 per WP-M-06 §3; the author never reviews own work above I0; AI-generated reviews are I0 inputs.

## 4. Record

Review record template (identifier, object, version, reviewer, independence, findings, outcome); pull-request review as the record for verification reviews.

## 5. Status changes

Draft → In review on opening the review; → Approved on acceptance by the approver named in WP-M-02; → Baselined by a tagged baseline.

## 6. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G0 |
