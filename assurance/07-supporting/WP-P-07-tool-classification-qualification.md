# WP-P-07 Software tool classification and qualification

| Field | Value |
|---|---|
| Work product | WP-P-07 Software tool classification and qualification |
| Standard reference | SRP/CS: 61508-3 §7.4.4 (T1–T3); 13849-1 §7; IEC 62443: 62443-4-1 SM-7 |
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

Software tool classification and qualification (IEC 61508-3 §7.4.4 T1–T3): compilers, static analysers, the MuJoCo simulator and training stack, the CAD and KiCad tools, the SISTEMA tool, the record's generators and checkers, and the AI assistant used for drafting.

## 2. Tool list

Per tool: use, class, qualification method, evidence. The Rust toolchain of the safety layer (DQ-063 B, 2026-10-21) needs its own qualification argument here: compiler version pinning, the language specification cited, the lint set enforced in CI (DQ-074), and the evidence that the build is reproducible.

## 3. AI-assisted drafting

Classified as a T1 drafting aid whose output is reviewed as the committer's work (WP-M-02 §3.3).

## 4. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G3 |
