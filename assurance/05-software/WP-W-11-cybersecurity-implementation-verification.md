# WP-W-11 Cybersecurity implementation and verification

| Field | Value |
|---|---|
| Work product | WP-W-11 Cybersecurity implementation and verification |
| Standard reference | IEC 62443: 62443-4-1 SI-1, SI-2, SVV-1…SVV-4; 62443-4-2 CR; ASPICE: SEC.2, SEC.3 |
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

Implementation and verification of the cybersecurity requirements of WP-C-08 (IEC 62443-4-1 SI and SVV): secure coding, security static analysis, requirement tests, and the threat-mitigation tests per scenario of WP-C-07.

## 2. Implementation

DTLS and TLS 1.3, session tokens, idle lock, audit log, signed images, closed debug port, CAN message authentication; per CSR-nn.

## 3. Protected assets

Safety parameters of WP-W-09 are protected assets; firmware and policy images; keys; the E-stop link.

## 4. Verification

Security requirement tests, threat mitigation tests, vulnerability scanning of the SBOM; penetration testing is WP-V-06.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G3 |
