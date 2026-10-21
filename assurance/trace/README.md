# WP-T-01 Requirements and traceability data

| Field | Value |
|---|---|
| Work product | WP-T-01 Requirements and traceability data (machine-readable), consistency evidence |
| Standard reference | SRP/CS: 13849-1 §5; 61508-3 §7.2; IEC 62443: 62443-4-1 SR-5; ASPICE: consistency evidence (SYS.2–5, SWE.1–6) |
| Version | 0.0 (skeleton: structure, clause map and seeds from the concept-phase package; 2026-10-21) |
| Status | Skeleton |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `3d4ec9d` (BL-001) |

> [!NOTE]
> **Skeleton.** The structure and clause mapping exist; the content is still to be written. The gate that needs this
> work product is **G1→G5** ([WP-M-00](../01-management/WP-M-00-work-product-register.md#3-register)).

## 1. Purpose

Machine-readable requirement and trace data: hazards, safety functions, requirements, parameters, tests and their links, with the consistency checks CI runs; the data behind the trace matrices. Tooling to be built with the first requirements.

## 2. Data files

`items/*.yaml` per identifier family: [`items/hazards.yaml`](items/hazards.yaml) (H-01…H-32 and SF-01…SF-25 from WP-C-03 and WP-C-04) and [`items/aou.yaml`](items/aou.yaml) (AOU-01…AOU-07 from WP-C-01) exist and are what the safety-case validator resolves references against; requirements and tests follow with WP-S-02, seeded from the concept-phase requirements workbook and test plan; `maps/` for the generated matrices.

## 3. Checks

Every hazard has a safety function or limit; every safety function has SRS rows; every SRS row has a test; every ID is unique and never reused.

## 4. Figures

Generated trace figures, checked by CI.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G1 |
