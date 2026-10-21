# WP-S-07 Cybersecurity architecture (zones, conduits, controls)

| Field | Value |
|---|---|
| Work product | WP-S-07 Cybersecurity architecture (zones, conduits, controls) |
| Standard reference | IEC 62443: 62443-4-1 SD-1…SD-4; 62443-3-3 §5; ASPICE: SEC.1, SYS.3 |
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

The cybersecurity architecture (IEC 62443-4-1 SD, 62443-3-3 zones and conduits): which zones exist on the robot, which conduits connect them, which controls sit on each conduit, and how the safety chain is kept out of reach of the network.

## 2. Zones and conduits

Safety chain (E-stop devices, receiver, motor-rail contactors); motion control board and the six CAN buses; the Raspberry Pi 5 edge board with its tele-operation and media stack; the operator app; the update path; the site network (external). The safety chain is a zone of its own with no conduit from the tele-operation network.

## 3. Controls per conduit

DTLS and TLS 1.3 on the tele-operation channel, session tokens, idle lock, signed images, a closed UART debug port in the reference build, CAN message authentication for safety signals, an E-stop link with heartbeat and encryption.

## 4. Defence in depth and the safety argument

How the controls protect SF-13, SF-21, SF-22 and the mode machine; what remains for the chain if every control fails.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G2 |
