# WP-H-02 Electrical and safety-chain design (motion control board, power distribution, harness, E-stop receiver, wiring)

| Field | Value |
|---|---|
| Work product | WP-H-02 Electrical and safety-chain design (motion control board, power distribution, harness, E-stop receiver, wiring) |
| Standard reference | SRP/CS: 13849-1 §6; IEC 62443: 62443-4-2 CR 2.13 (physical); Other: 60204-1 §5–§13; ASPICE: HWE.2 |
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

Electrical and safety-chain design: the motion control board (Radxa CM5 carrier, KiCad sources under `electrical/motion_control/`), the power distribution board (not in the repository at BL-001), the WireViz harness (`electrical/wiring/`), the E-stop devices and receiver, and the motor-rail removal path; schematics, wiring, enclosure.

## 2. What the inherited record holds

The MCB schematics and PCB (v0.1.4), the harness (XT30(2+2) power and CAN to every actuator, JST-GH signals, Molex KK to the BMS), the port map C0…C5; no E-stop, no contactor, no PDB, no battery in the repository (GAP-07, GAP-08).

## 3. Signal chain

E-stop devices → receiver → motor-rail contactors; the MCB safety layer's enable; the BMS handshake; category and DC per WP-S-03. Decided 2026-10-21: a second IMU of a different type on a separate supply as the second channel of SF-23 (DQ-034 A); the UART debug port behind a cover with a tamper label, disabled in firmware unless a maintenance mode is armed (DQ-033 A).

## 4. Response time budget

Per WP-S-04.

## 5. Power

5 V XT30 input to the MCB, the battery rail to the actuators, fusing per branch, disconnection device (IEC 60204-1 §5.3, GAP-08).

## 6. Diagnostics

Diagnostic signals from the chain to the firmware are informative only.

## 7. Estimated PL

To be recalculated in WP-H-04.

## 8. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G3 |
