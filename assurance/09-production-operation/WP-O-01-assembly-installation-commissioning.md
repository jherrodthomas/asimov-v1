# WP-O-01 Assembly, installation and commissioning instructions (the DIY kit build, acceptance checks)

| Field | Value |
|---|---|
| Work product | WP-O-01 Assembly, installation and commissioning instructions (the DIY kit build, acceptance checks) |
| Standard reference | Machinery: 12100 §6.4; 13482 §7; Other: Machinery Reg. Annex III §1.7.4; ISO 9001 §8.5.1 (informative) |
| Version | 0.0 (skeleton: structure, clause map and seeds from the concept-phase package; 2026-10-21) |
| Status | Skeleton |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `3d4ec9d` (BL-001) |

> [!NOTE]
> **Skeleton.** The structure and clause mapping exist; the content is still to be written. The gate that needs this
> work product is **G5** ([WP-M-00](../01-management/WP-M-00-work-product-register.md#3-register)).

## 1. Purpose

Assembly, installation and commissioning instructions for a DIY-kit build: material and part verification, harness build and pull test, board installation, E-stop and BMS fitting, the acceptance checks that make a unit fit for OE-1.

## 2. Build

The kit-assembly hazards are inside the item (DQ-031 A, 2026-10-21): ESD during board handling (H-10, SF-12), MJF PA12 dust during post-processing and repair (H-17, SF-17), and the two-person lift of the 35 kg robot (H-18, SF-18) are procedural measures of this document, rated in WP-C-03, with no Performance Level.

Per subassembly ASV1_100…ASV1_700; torque and threadlocker tables (FM-03); mill certificates for 7075-T6 (FM-02); pre-crimped harness or pull-test (FM-18).

## 3. Commissioning checks

Watchdog self-test, E-stop test from every device, BMS handshake, encoder direction, IMU plausibility, thermistor readout, CAN termination. After every deliberate fall test: the inspection of the fall campaign (DQ-026 A): yokes, printed shells, harness connectors, actuator free play; structural aluminium damage ends the campaign.

## 4. Acceptance record

Per unit; kept under WP-P-01.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G5 |
