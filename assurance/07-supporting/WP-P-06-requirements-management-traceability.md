# WP-P-06 Requirements management and traceability procedure

| Field | Value |
|---|---|
| Work product | WP-P-06 Requirements management and traceability procedure |
| Standard reference | SRP/CS: 13849-1 §5; 61508-3 §7.2; IEC 62443: 62443-4-1 SR-5; ASPICE: SYS.2, SWE.1 |
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

Requirements management and traceability: identifier families, the trace data under `trace/`, bidirectional links hazard → safety function → requirement → test, consistency checks CI runs, change rules.

## 2. Identifier families

H, SF, SR, HWSR, SWSR, CSR, AIR, FI, TC, PAR, AOU, VS, DF, GAP, OI, DQ (assurance README).

## 3. Trace data

[`trace/items/`](../trace/README.md); the concept-phase trace memo and requirements workbook as the seed (120 requirements, 139 test cases, fully traced in the package).

## 4. Checks

Every hazard has a safety function or limit; every safety function has requirements; every requirement has a test; IDs unique and never reused.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G0 |
