# WP-H-01 Hardware safety requirements (E-stop chain, motor-rail contactor, BMS interlock, thermistors, encoders)

| Field | Value |
|---|---|
| Work product | WP-H-01 Hardware safety requirements (E-stop chain, motor-rail contactor, BMS interlock, thermistors, encoders) |
| Standard reference | Machinery: 10218-1 §5.4; 13482 §5.16; SRP/CS: 13849-1 §5, §6; Other: 60204-1 §9.2; ASPICE: HWE.1 |
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

Hardware safety requirements for the E-stop chain, the motor-rail removal, the BMS interlock, the thermistors and the encoders: HWSR-nn derived from WP-S-02 and WP-S-03, with the category, DC and environmental requirements each component must meet; the 36 hardware requirements of the concept-phase workbook are the seed.

## 2. Requirements

HWSR-nn: E-stop devices (wired for OE-1, wireless receiver with heartbeat), motor-rail contactors with mirror contacts, per-rail fuses (SF-11), BMS handshake interlock (SYRS-014), stator thermistors with a hardware cutoff (SF-14), a second IMU for cross-checking (FM-12), encoder plausibility, UVLO and power-good on the power distribution board (FM-31), reverse-polarity protection on the XT30 input (FM-17), a keyed supply connector.

## 3. Environmental and electrical requirements

Temperature +10 to +35 °C, humidity, no ingress protection claimed, supply tolerance, EMC.

## 4. Traceability

To WP-S-02 and WP-S-03; verified by WP-H-06.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G3 |
