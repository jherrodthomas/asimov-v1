# WP-W-01 SW development environment, languages and coding guidelines

| Field | Value |
|---|---|
| Work product | WP-W-01 SW development environment, languages and coding guidelines |
| Standard reference | SRP/CS: 13849-1 §7; 61508-3 §7.4.4; IEC 62443: 62443-4-1 SI-1, SI-2; Other: MISRA C:2012 (firmware); ASPICE: SWE.3 |
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

Software development environment, languages and coding guidelines for the motion-control firmware, the edge software and the policy runtime: toolchains, pins, static analysis, coding rules, reproducible builds.

## 2. Environment

Radxa CM5 (PREEMPT_RT Linux, motion control) and Raspberry Pi 5 (media, tele-operation); C and C++ with MISRA C:2012 for the safety layer; Python for tooling and training; the MuJoCo model for simulation; pinned images.

## 3. Guidelines

Coding rules, review rules, test rules, the separation of the safety layer from the policy runtime.

## 4. What exists at BL-001

No firmware, API or policy is in any public repository (GAP-16, GAP-17); the environment is defined ahead of the code.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G3 |
