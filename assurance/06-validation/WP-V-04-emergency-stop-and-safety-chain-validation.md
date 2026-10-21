# WP-V-04 Emergency stop and safety-chain validation (wired and wireless devices, link loss, re-arm)

| Field | Value |
|---|---|
| Work product | WP-V-04 Emergency stop and safety-chain validation (wired and wireless devices, link loss, re-arm) |
| Standard reference | Machinery: 13850 §4; 13482 §5.16; SRP/CS: 13849-2 §5; Other: 60204-1 §9.2, §18; ASPICE: VAL.1 |
| Version | 0.0 (skeleton: structure, clause map and seeds from the concept-phase package; 2026-10-21) |
| Status | Skeleton |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `3d4ec9d` (BL-001) |

> [!NOTE]
> **Skeleton.** The structure and clause mapping exist; the content is still to be written. The gate that needs this
> work product is **G4** ([WP-M-00](../01-management/WP-M-00-work-product-register.md#3-register)).

## 1. Purpose

Emergency stop and safety-chain validation: each device (wired tether E-stop, wireless transmitter), each channel, link loss, jammed link, dead transmitter battery, welded contact, re-arm with the operator out of position; per ISO 13850 and ISO 13849-2.

## 2. Test specification

ES-nn per device and fault; timing from press to motor-rail removal (≤ 500 ms, SYRS-003); heartbeat loss to fail-safe (SF-13). In OE-1 a lost wireless heartbeat is a warning, not a stop demand (DQ-039 A, 2026-10-21): the test shows the warning and the log entry, and the wired pendant stops the robot; the safety relay module's monitored reset and the contactors' mirror contacts (DQ-036 A) are tested with a simulated welded contact; a re-arm attempted from the operator app must fail and only the pendant's reset with the button released may re-arm (DQ-048 A).

## 3. Report

Results per baseline.

## 4. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G4 |
