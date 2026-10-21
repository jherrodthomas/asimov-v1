# WP-W-08 Software validation on the target (MCB bench, hardware-in-the-loop with the MuJoCo model)

| Field | Value |
|---|---|
| Work product | WP-W-08 Software validation on the target (MCB bench, hardware-in-the-loop with the MuJoCo model) |
| Standard reference | SRP/CS: 13849-1 §10; 61508-3 §7.7; ASPICE: SWE.6 |
| Version | 0.0 (skeleton: structure, clause map and seeds from the concept-phase package; 2026-10-21) |
| Status | Skeleton |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `3d4ec9d` (BL-001) |

> [!NOTE]
> **Skeleton.** The structure and clause mapping exist; the content is still to be written. The gate that needs this
> work product is **G4** ([WP-M-00](../01-management/WP-M-00-work-product-register.md#3-register)).

## 1. Purpose

Software validation on the target: the MCB bench with actuators on a stand and the MuJoCo model in the loop, then the robot on the gantry; the hardware-in-the-loop rig and its owner.

## 2. Bench and rig

What the bench is, who owns it (WP-M-02 §3.1), how the MuJoCo model (`sim-model/xmls/asimov.xml`) is coupled.

## 3. Validation tests

Watchdog, mode transitions, clamps, fall-arrest, E-stop, bus-off, on the real boards.

## 4. Report

Results per baseline.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G4 |
