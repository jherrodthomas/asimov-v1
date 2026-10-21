# WP-W-02 Software safety requirements specification (SRESW, SRASW)

| Field | Value |
|---|---|
| Work product | WP-W-02 Software safety requirements specification (SRESW, SRASW) |
| Standard reference | SRP/CS: 13849-1 §7; 61508-3 §7.2; ASPICE: SWE.1 |
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

Software safety requirements (SRESW and SRASW per ISO 13849-1 §7) for the motion-control-board safety layer: SWSR-nn derived from WP-S-02 and the 45 software requirements of the concept-phase workbook.

## 2. Requirements

SWSR-nn: loop deadline monitor (SRS-001), hardware-backed watchdog (SRS-002), mode transition guards (SRS-003), heartbeat keep-alive at ≥ 4 Hz with a 250 ms timeout (SRS-004), policy output clamping (SRS-006), encoder plausibility (SRS-010), bus-off response (SRS-011), fault classification (SRS-013), IMU cross-check (SF-23), controlled descent (SF-02).

## 3. Traceability

To WP-S-02, WP-C-04 and the trace data; verified by WP-W-06.

## 4. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G3 |
