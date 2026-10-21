# WP-M-11 Impact analysis of the inherited Asimov v1 baseline and the concept-phase package (modification of existing machinery)

| Field | Value |
|---|---|
| Work product | WP-M-11 Impact analysis of the inherited Asimov v1 baseline and the concept-phase package (modification of existing machinery) |
| Standard reference | Machinery: 12100 §4; SRP/CS: 61508-1 §7.16 (modification); IEC 62443: 62443-4-1 SM-3; Other: Machinery Reg. Art. 3 (substantial modification); ASPICE: SUP.10 |
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

Impact analysis of using the inherited Asimov v1 baseline and the fork's concept-phase package as the starting point of a machine that is to carry a safety case: what is reused, what is reworked, what is discarded, and what each inherited element's state means for the lifecycle entry (WP-M-01 T-01).

## 2. Baseline

The commit of the gap assessment header; every finding GAP-01…GAP-34 is an input; the concept-phase package under [`00-assessment/concept-package/`](../00-assessment/concept-package/README.md).

## 3. Reuse classification per element

Per element: reuse unchanged (mechanical CAD, simulation model as functional inputs), reuse with hardening (motion control board design, harness), replace or create (the E-stop and motor-rail chain, the firmware safety layer, every safety work product), port (the concept-phase workbooks into WP-C-03, WP-C-04, WP-A-01, WP-S-02, WP-V-01). With the rationale and the gaps each inherits.

## 4. Consequences for the lifecycle

Full concept phase; no inherited safety work product counts as evidence; the firmware does not exist in any public repository, so the software work products start from the interface the manual describes.

## 5. Change impact analysis records

Later changes are analysed per change under [`07-supporting/impact/`](../07-supporting/impact/README.md); this document covers only the entry.

## 6. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G0 |
