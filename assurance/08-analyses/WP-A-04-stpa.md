# WP-A-04 System-theoretic process analysis (STPA) of the motion control chain (tele-operation, policy, MCB, actuators)

| Field | Value |
|---|---|
| Work product | WP-A-04 System-theoretic process analysis (STPA) of the motion control chain (tele-operation, policy, MCB, actuators) |
| Standard reference | Machinery: 12100 §5.4; Other: STPA Handbook 2018 |
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

System-theoretic process analysis of the motion control chain: controllers (operator, policy, mode machine, joint controllers), control actions, unsafe control actions, loss scenarios; the tele-operation latency and the DAMP transition as the central control problems.

## 2. Control structure

Operator app → edge board → MCB mode machine → joint controllers → actuators; the policy as a controller; the E-stop and tether as outside controls.

## 3. Unsafe control actions

UCA-nn: DAMP commanded mid-stride, STAND entered with a person leaning on the robot, MOVE accepted with a stale camera frame, a torque command above the limit, a mode transition without the IMU plausible.

## 4. Loss scenarios and requirements

To WP-S-02 and WP-W-02.

## 5. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G2 |
