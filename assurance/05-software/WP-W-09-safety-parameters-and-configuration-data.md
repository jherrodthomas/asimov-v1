# WP-W-09 Safety-related parameters and configuration data (joint torque and velocity limits, watchdog timeouts, PFL thresholds, mode limits)

| Field | Value |
|---|---|
| Work product | WP-W-09 Safety-related parameters and configuration data (joint torque and velocity limits, watchdog timeouts, PFL thresholds, mode limits) |
| Standard reference | Machinery: 13482 §5.10; TS 15066 §5.5; SRP/CS: 13849-1 §7 (parameterization); IEC 62443: 62443-4-2 CR 3.4; ASPICE: SWE.3 |
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

Safety-related parameters and configuration data: joint torque and velocity limits per joint and per operating envelope, watchdog and heartbeat timeouts, power-and-force-limiting thresholds, IMU plausibility bounds, mode limits; with their source, allowed range, verification and protection against unauthorised change (ISO 13849-1 §7 parameterisation).

## 2. Parameter register

The first parameter set for OE-1 is decided (DQ-014 A, 2026-10-21): half the MuJoCo `ctrlrange` torque limit per joint and a velocity ceiling set by WP-S-04, until measured.

PAR-nn: value, unit, source (WP-S-04 budget, ISO/TS 15066 Annex A, measurement), range, where it lives, who may change it, how it is verified after loading. The MuJoCo `ctrlrange` torque limits per joint are the only published limits at BL-001 and are simulation values, not declared robot limits (GAP-06).

## 3. Integrity

Parameter integrity is a cybersecurity requirement verified in WP-W-11: signed parameter sets, read-back, no runtime change without arming.

## 4. Simulation and real robot

One parameter file per configuration; what differs between the MuJoCo model and the hardware.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G3 |
