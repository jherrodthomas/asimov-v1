# WP-C-07 Cybersecurity threat and risk assessment (tele-operation channel, API, update path)

| Field | Value |
|---|---|
| Work product | WP-C-07 Cybersecurity threat and risk assessment (tele-operation channel, API, update path) |
| Standard reference | IEC 62443: 62443-4-1 SR-2; 62443-3-2 §5; ASPICE: SEC.1 |
| Version | 0.0 (skeleton: structure, clause map and seeds from the concept-phase package; 2026-10-21) |
| Status | Skeleton |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `3d4ec9d` (BL-001) |

> [!NOTE]
> **Skeleton.** The structure and clause mapping exist; the content is still to be written. The gate that needs this
> work product is **G1** ([WP-M-00](../01-management/WP-M-00-work-product-register.md#3-register)).

## 1. Purpose

Threat and risk assessment of the robot under IEC 62443-4-1 SR-2 and 62443-3-2: assets, zones and conduits, threat scenarios TS-nn, attack paths, likelihood and impact, with the safety impact rated against the hazard list.

## 2. Assets and zones

The WebRTC tele-operation data channel, the Asimov API (unreleased), the Raspberry Pi 5 edge board and its Wi-Fi, 4G or Ethernet links, the Radxa CM5 motion-control board and its UART debug port, the six CAN buses, the wireless E-stop link, firmware and policy images, the update path.

## 3. Threat scenarios

Seeded from GAP-19, GAP-20, GAP-22 and the DFMEA: an unauthenticated or replayed tele-operation command (HZ-C02), a jammed or spoofed wireless E-stop link (HZ-E04), a tampered policy or firmware image, a hostile device on a CAN bus, an open UART debug port, an unpinned supply chain.

## 4. Risk rating

Likelihood and impact per scenario; Safety impact is anchored to the hazard list of WP-C-03 (the hazard each scenario can cause).

## 5. Treatment

Security level target (WP-C-08), requirements CSR-nn, residual risk accepted by the lead (DQ-012).

## 6. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G1 |
