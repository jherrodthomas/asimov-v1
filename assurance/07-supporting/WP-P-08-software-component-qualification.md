# WP-P-08 Qualification of software components (RT kernel, CAN stack, WebRTC, MuJoCo, policy runtime, third-party)

| Field | Value |
|---|---|
| Work product | WP-P-08 Qualification of software components (RT kernel, CAN stack, WebRTC, MuJoCo, policy runtime, third-party) |
| Standard reference | SRP/CS: 61508-3 §7.4.2.12; IEC 62443: 62443-4-1 SM-9, SM-10 |
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

Qualification of software components the safety-related software depends on: the real-time kernel on the CM5, the CAN stack, the WebRTC and media stack on the Pi 5, the MuJoCo runtime and the policy inference runtime, third-party libraries.

## 2. Component list

Per component: version, role, safety relevance, qualification route (proven in use not claimed, T-06; testing, isolation).

## 3. Arguments

Isolation of the safety layer from unqualified components (WP-A-05).

## 4. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G3 |
