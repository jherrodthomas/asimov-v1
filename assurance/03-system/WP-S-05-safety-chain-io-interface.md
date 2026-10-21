# WP-S-05 Hardware-software interface of the safety chain (I/O map, CAN buses, E-stop receiver, BMS handshake, signal semantics)

| Field | Value |
|---|---|
| Work product | WP-S-05 Hardware-software interface of the safety chain (I/O map, CAN buses, E-stop receiver, BMS handshake, signal semantics) |
| Standard reference | SRP/CS: 13849-1 §6, §7; ASPICE: SYS.3 |
| Version | 0.0 (skeleton: structure, clause map and seeds from the concept-phase package; 2026-10-21) |
| Status | Skeleton |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `3d4ec9d` (BL-001) |

> [!NOTE]
> **Skeleton.** The structure and clause mapping exist; the content is still to be written. The gate that needs this
> work product is **G2** ([WP-M-00](../01-management/WP-M-00-work-product-register.md#3-register)).

## 1. Purpose

The hardware-software interface of the safety chain: every signal between the motion control board, the actuators, the E-stop receiver, the power distribution board and the BMS, with its semantics, timing and failure behaviour (I/O map).

## 2. I/O map

MCB ports C0…C5, the UART debug port, the IMU on I2C, the E-stop receiver output, the motor-rail enable, the BMS handshake on C5, power-good and under-voltage signals of the power distribution board, the pendant's reset input to the safety relay (the only re-arm path, DQ-048 A) and the start command from the operator app, which never re-arms; the pendant's three-position enabling switch as a dual input to the safety layer (motion in M3 only while held, DQ-058 A).

## 3. Signal semantics

Per signal: direction, electrical form, rate, valid range, timeout, what the safety layer does when it is missing or implausible.

## 4. CAN buses

Bit rates (5 × 1 Mbps, 1 × 500 kbps), termination, bus-off handling (SYRS-023: DAMP within 100 ms), message authentication where a safety signal crosses a bus.

## 5. Diagnostic signals

Chain state to the firmware: informative only, never a channel of a safety function.

## 6. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G2 |
