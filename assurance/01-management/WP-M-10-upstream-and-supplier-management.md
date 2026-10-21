# WP-M-10 Upstream (Asimov Inc) and supplier management (kit, actuators, battery)

| Field | Value |
|---|---|
| Work product | WP-M-10 Upstream (Asimov Inc) and supplier management (kit, actuators, battery) |
| Standard reference | SRP/CS: 61508-1 §6.2 (subcontracted activities); IEC 62443: 62443-4-1 SM-9, SM-10; ASPICE: ACQ.4 |
| Version | 0.0 (skeleton: structure, clause map and seeds from the concept-phase package; 2026-10-21) |
| Status | Skeleton |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `3d4ec9d` (BL-001) |

> [!NOTE]
> **Skeleton.** The structure and clause mapping exist; the content is still to be written. The gate that needs this
> work product is **G0** ([WP-M-00](WP-M-00-work-product-register.md#3-register)).

## 1. Purpose

Management of upstream Asimov Inc (Menlo) as a supplier without a development interface agreement, and of the kit, actuator, battery and board suppliers the DIY build depends on.

## 2. Upstream

The `asimovinc/asimov-v1` repository, the manual at manual.asimov.inc, the DIY kit; what the fork takes (CAD, electrical, simulation model), what it waits for (firmware, API, locomotion policy), how upstream changes are tracked (WP-P-02).

## 3. Suppliers

Actuators (BLDC with harmonic gear and encoder, typical of 25), the motion control board fabrication (JLCPCB), the Radxa CM5 and Raspberry Pi 5, the user-supplied battery and BMS (DQ-009), the E-stop devices, 7075-T6 and 316L stock.

## 4. Supplier evidence

Certificates, failure rates and B10d values needed by WP-H-04 and WP-H-07; what is missing at BL-001 (GAP-14).

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G0 |
