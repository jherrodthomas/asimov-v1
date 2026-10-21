# WP-C-06 Human-robot interaction, collaborative operation, contact limits and reasonably foreseeable misuse analysis

| Field | Value |
|---|---|
| Work product | WP-C-06 Human-robot interaction, collaborative operation, contact limits and reasonably foreseeable misuse analysis |
| Standard reference | Machinery: 10218-2 §5; TS 15066 §5; 13482 §5.7, §5.8; 12100 §5.3; Other: ISO 13857 §4 |
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

Human-robot interaction, collaborative operation, contact limits and reasonably foreseeable misuse: who is near the robot in each operating envelope, how close, which contact is foreseeable (arm sweep, pinch at a joint, a fall onto a person, leaning on the robot), the force and energy limits of ISO/TS 15066 and ISO 13482 §5.7 that apply, and the misuse the design must survive.

## 2. Interaction scenarios

IS-nn per operating envelope: the operator within E-stop reach (OE-1), a co-worker in a defined cell (OE-2), a child or pet at home (OE-3), a bystander in public (OE-4). Operating envelopes and people presence are taken from WP-C-02.

## 3. Contact limits

Body-region limits of ISO/TS 15066 Annex A for transient and quasi-static contact; the fall energy of a 35 kg body from 1.2 m (about 411 J at the centre of mass per the concept-phase package) against them; what SF-04 and SF-20 must bound.

## 4. Collaborative operation

Whether any collaborative mode (OE-2) is claimed: power-and-force limiting only, with the measured limits; no hand-guiding, no speed-and-separation claim without a safety-rated sensor.

## 5. Reasonably foreseeable misuse

MU-nn: leaning on the robot, lifting it alone, removing the tether, a non-compliant battery, 6061 stock in place of 7075, running outdoors or on a wet floor, children near a standing robot, a bystander catching a falling robot.

## 6. Requirements derived here

HR-nn to WP-C-04, WP-S-02 and WP-O-03; the pinch-gap and reach requirements per ISO 13857.

## 7. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G1 |
