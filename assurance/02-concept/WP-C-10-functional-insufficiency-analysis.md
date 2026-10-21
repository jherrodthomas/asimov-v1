# WP-C-10 Functional insufficiency analysis of perception and the locomotion policy (performance limits, triggering conditions)

| Field | Value |
|---|---|
| Work product | WP-C-10 Functional insufficiency analysis of perception and the locomotion policy (performance limits, triggering conditions) |
| Standard reference | Machinery: 13482 §5.6, §5.10; 12100 §5.4; Other: ISO 21448 §6–§7 (informative method) |
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

Analyses the performance limits of perception and the locomotion policy that cause hazardous behaviour without any fault, using ISO 21448's method as an informative frame (triggering conditions, functional insufficiencies, known and unknown scenarios). Each limit is closed by a safety function, an operating-environment limit, or stays as an open defeater.

## 2. Functional insufficiencies

FI-nn seeded from the gap assessment and the DFMEA: a policy out-of-distribution scenario (FM-28, HZ-P02), a sim-to-real gap on friction and inertia, a monocular camera that cannot range a person, no perception of a person behind the robot, IMU saturation in a fall, DAMP as a safe state that itself drops the robot (HZ-C01), a frozen camera frame (FM-23).

## 3. Triggering conditions

TC-nn per insufficiency: a slope above 5°, a soft or wet floor, a child at knee height, a hand on the shoulder, a tether that goes slack, a lost Wi-Fi link mid-step.

## 4. Detection means and the claims SF-02 and SF-06 can make

What the camera and the IMU cannot see bounds the claim SF-06 and SF-02 can make: the speed-reduction trigger of SF-06 has no safety-rated sensor behind it, and the fall-arrest function SF-02 can only act within the IMU's range and the actuators' torque. The safe state of the biped is decision DQ-005.

## 5. Known and unknown scenarios

Known ones go to WP-V-02, WP-V-03 and WP-V-05 as tests; the unknown residual is the subject of WP-V-08 field trials.

## 6. Closure table

FI/TC → safety function, operating-environment limit, or open defeater DF-nn.

## 7. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G1 |
| OI-2 | Bound what the perception trigger of SF-06 and the IMU can and cannot detect once the safe state is decided (DQ-005); until then IX-02 stays open | SM | G1 |
