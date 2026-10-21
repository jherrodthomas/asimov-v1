# WP-C-08 Cybersecurity requirements and security level target

| Field | Value |
|---|---|
| Work product | WP-C-08 Cybersecurity requirements and security level target |
| Standard reference | IEC 62443: 62443-4-1 SR-3…SR-5; 62443-4-2 CR 1–7, SL-T; ASPICE: SEC.1 |
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

Cybersecurity requirements CSR-nn and the security level target per foundational requirement (IEC 62443-4-2), derived from the threat assessment and the safety functions they protect (SF-13 E-stop link surveillance, SF-21 authenticated tele-operation, SF-22 session lock).

## 2. Security level target

SL-T per FR 1–7, decided by the lead (DQ-012); planning assumption SL 2 for identification, integrity, data flow and availability, SL 1 otherwise.

## 3. Requirements

CSR-nn per CR: DTLS and TLS 1.3 on the tele-operation channel, session tokens with expiry, idle lock, audit logging, signed images, a closed UART debug port in the reference build, CAN message authentication where a safety signal crosses a bus, E-stop link heartbeat and encryption.

## 4. Traceability

To the threat scenarios of WP-C-07 and to SF-13, SF-21, SF-22 of WP-C-04.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G1 |
