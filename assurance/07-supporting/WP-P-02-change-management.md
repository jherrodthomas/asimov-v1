# WP-P-02 Change management plan

| Field | Value |
|---|---|
| Work product | WP-P-02 Change management plan |
| Standard reference | SRP/CS: 61508-1 §7.16; IEC 62443: 62443-4-1 SM-3; ASPICE: SUP.10 |
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

Change management: how a change to a safety-relevant path or a work product is raised, impact-analysed, reviewed, verified and recorded; upstream changes pulled into the fork go through the same route.

## 2. Change request

Issue or pull request with the safety-impact statement of the template; classification by [`safety-relevant-paths.txt`](safety-relevant-paths.txt).

## 3. Impact analysis

Record under [`impact/`](impact/README.md) per WP-M-11; hazards, safety functions, requirements, assumptions, work products re-opened.

## 4. Review and verification

Per WP-P-05; confirmation review repeated if a confirmed work product changes.

## 5. Upstream changes

Each upstream release is pulled as a change with its own impact record.

## 6. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G0 |
