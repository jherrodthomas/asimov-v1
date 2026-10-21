# WP-M-09 Machine-learning safety plan (learned locomotion policy, perception)

| Field | Value |
|---|---|
| Work product | WP-M-09 Machine-learning safety plan (learned locomotion policy, perception) |
| Standard reference | Other: TR 5469 (AI technology classes, usage levels); AI Act Art. 9; ASPICE: MLE.1–4 |
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

Machine-learning safety plan under ISO/IEC TR 5469: how the learned locomotion policy and any perception model are classified, what evidence their engineering produces, and the independent reviews ML-R1…ML-R3.

## 2. Learned components

The locomotion policy (MuJoCo-trained, unreleased upstream at BL-001), any perception model used for the speed-reduction trigger of SF-06, voice recognition (not safety-related).

## 3. Position

Whether the learned policy may carry the bipedal stability function SF-01 is decision DQ-006; until answered the plan assumes it does not, stability in OE-1 rests on the tether and gantry, and the policy is a functional component checked by the MCB safety layer.

## 4. Activities

Classification (WP-C-09), insufficiency analysis (WP-C-10), ML engineering evidence (WP-W-10), field trials (WP-V-08), AI Act record (WP-K-07).

## 5. Reviews

ML-R1 at G1, ML-R2 at G3, ML-R3 at G5 (WP-M-06 §7).

## 6. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G0 |
