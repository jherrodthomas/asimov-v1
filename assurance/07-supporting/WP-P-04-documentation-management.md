# WP-P-04 Documentation management

| Field | Value |
|---|---|
| Work product | WP-P-04 Documentation management |
| Standard reference | Machinery: 12100 §7; SRP/CS: 13849-1 §12; IEC 62443: 62443-4-1 SG-1; Other: Machinery Reg. Annex IV; ASPICE: SUP.7 |
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

Documentation management: the document-control header, status meanings, identifiers, generated files and their generators, the link and table checks, and the retention rules of the technical file.

## 2. Rules

Those of the [assurance README](../README.md#conventions).

## 3. Generated files

Folder READMEs, process maps and gate skeletons, swimlane and README figures, the dashboard, the decision lifecycle figure; never edited by hand; checked by CI.

## 4. Retention

Ten years after the last unit (Machinery Regulation Annex IV); git history and release snapshots.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G0 |
