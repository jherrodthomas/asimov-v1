# WP-W-10 ML engineering: data, training, simulation-to-real transfer, testing and deployment of the locomotion policy

| Field | Value |
|---|---|
| Work product | WP-W-10 ML engineering: data, training, simulation-to-real transfer, testing and deployment of the locomotion policy |
| Standard reference | Other: TR 5469 §8–§10; AI Act Art. 10, Art. 15; ASPICE: MLE.1–4, SUP.11 |
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

ML engineering of the locomotion policy: data and simulation provenance, training, domain randomisation, sim-to-real transfer, testing against the hazard list, deployment and versioning (ISO/IEC TR 5469 §8–§10).

## 2. Training and simulation

MuJoCo model, randomisation ranges, the sim-to-real coverage matrix (DFMEA FM-28). For the first item the policy is upstream's black box (DQ-050 A, 2026-10-21): this section records what upstream publishes, not evidence the fork produces.

## 3. Testing

Scenario tests against the 32 hazards; out-of-distribution detection; behaviour under the clamps of SF-03.

## 4. Deployment

Version pinning, rollback, runtime monitoring (SF-23).

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G3 |
