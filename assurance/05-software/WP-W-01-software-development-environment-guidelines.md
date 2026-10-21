# WP-W-01 SW development environment, languages and coding guidelines

| Field | Value |
|---|---|
| Work product | WP-W-01 SW development environment, languages and coding guidelines |
| Standard reference | SRP/CS: 13849-1 §7; 61508-3 §7.4.4; IEC 62443: 62443-4-1 SI-1, SI-2; Other: MISRA C:2012 (firmware); ASPICE: SWE.3 |
| Version | 0.1 (2026-10-21): DQ-063 B (Rust) and DQ-064 B (no reverse-engineering of the actuator protocol) applied to §2 and §4. 0.0 (skeleton: structure, clause map and seeds from the concept-phase package; 2026-10-21) |
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

Radxa CM5 (PREEMPT_RT Linux, motion control) and Raspberry Pi 5 (media, tele-operation); **Rust for the safety layer** (DQ-063 B, decided 2026-10-21, not the recommendation: a coding standard to adopt, DQ-074, and a toolchain qualification argument to write in WP-P-07); C and C++ only where a vendor library forces it; Python for tooling and training; the MuJoCo model for simulation; pinned images.

## 3. Guidelines

Coding rules, review rules, test rules, the separation of the safety layer from the policy runtime. The UART debug port is open in development builds and closed in the reference build (DQ-033 A, 2026-10-21): the two builds differ in that one flag, recorded in the build manifest.

## 4. What exists at BL-001

No firmware, API or policy is in any public repository (GAP-16, GAP-17); the environment is defined ahead of the code. The actuators' CAN protocol is not documented either, and the fork does not observe or reverse-engineer it (DQ-064 B, decided 2026-10-21): the firmware's actuator interface waits for the supplier's or upstream's documentation (requested under DQ-047 A); the layer above it (watchdog, mode machine, clamps, E-stop input) is written against a CAN loopback meanwhile.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G3 |
