# WP-C-09 ML component definition and safety requirements (locomotion policy, perception models)

| Field | Value |
|---|---|
| Work product | WP-C-09 ML component definition and safety requirements (locomotion policy, perception models) |
| Standard reference | Other: TR 5469 §6–§8 (classes, usage levels, properties); AI Act Annex IV; ASPICE: MLE.1 |
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

Defines the learned components in or planned for the stack (the locomotion policy, perception models), classifies each under ISO/IEC TR 5469 (AI technology class, usage level) and states the requirements that bound them.

## 2. Inventory of learned components

The locomotion policy trained in MuJoCo against `sim-model/xmls/asimov.xml` (unreleased upstream at BL-001, GAP-17); any perception model behind the speed-reduction trigger of SF-06; voice recognition (not safety-related).

## 3. Classification

Per component: technology class, usage level, the independent safeguard and why it is sufficient.

## 4. Position

SF-01 bipedal stability is the one safety function a learned component may carry; the position is decision DQ-006, answered A on 2026-10-21: SF-01 is withdrawn and no safety function is allocated to a learned component: stability in OE-1 rests on the tether and gantry of WP-V-07, the policy's outputs pass through the torque and velocity clamps of the MCB safety layer (SF-03), and the fall-arrest function SF-02 is a deterministic controlled descent. If the lead allocates SF-01 to the policy, WP-M-13 §5 applies, the AI Act record WP-K-07 becomes a full technical documentation, and this document is rewritten.

## 5. Requirements

AIR-nn: bounded outputs (SRS-006 of the concept-phase package), pass-through of the MCB clamps, runtime monitoring by IMU plausibility (SF-23), version pinning, data provenance, a sim-to-real coverage matrix against the hazard list (DFMEA FM-28).

## 6. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G1 |
