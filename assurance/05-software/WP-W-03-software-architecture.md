# WP-W-03 Software architectural design (MCB safety layer and mode machine, separation from the locomotion policy and the tele-operation stack)

| Field | Value |
|---|---|
| Work product | WP-W-03 Software architectural design (MCB safety layer and mode machine, separation from the locomotion policy and the tele-operation stack) |
| Standard reference | SRP/CS: 13849-1 §7; 61508-3 §7.4.3; IEC 62443: 62443-4-1 SD-2; ASPICE: SWE.2 |
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

The software architecture: the motion-control-board safety layer and its separation from the rest of the firmware, the mode machine (DAMP, STAND, MOVE), the locomotion policy runtime and the tele-operation stack on the Raspberry Pi 5, and the interfaces between them and the chain. The I/O semantics of WP-S-05 are the firmware's contract with the safety chain.

## 2. Firmware architecture

The lead decided on 2026-10-21 (DQ-023 A) that the fork writes a minimal firmware of its own for the motion control board before upstream's is public: CAN actuator control with the clamps SF-03, the watchdog SF-24, the E-stop input and a DAMP-only fallback, enough for the hang tests of WP-V-07; the controlled descent SF-02 waits for a controller. This section describes that firmware first and upstream's, when it arrives, against it. It is written in Rust (DQ-063 B) and its actuator interface waits for documented protocols (DQ-064 B); until then the layer is built and tested against a CAN loopback.

Command intake (policy or tele-operation) → validation and clamps → mode machine → joint controllers → CAN; watchdog; fault handling; status publication.

## 3. Edge architecture

WebRTC tele-operation, media, the Asimov API, authentication; what may command the MCB and how.

## 4. Policy runtime

Where the learned policy runs, how its outputs are bounded, how it is versioned (WP-C-09).

## 5. Separation

What runs on the CM5, what on the Pi 5, what in hardware; shared resources and how WP-A-05 analyses them.

## 6. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G3 |
