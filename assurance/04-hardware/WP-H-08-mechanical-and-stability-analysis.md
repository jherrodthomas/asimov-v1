# WP-H-08 Mechanical, structural and stability analysis (mass, centre of gravity, tip-over, fall energy, fatigue of the hip yoke, pinch and crush points, guarding)

| Field | Value |
|---|---|
| Work product | WP-H-08 Mechanical, structural and stability analysis (mass, centre of gravity, tip-over, fall energy, fatigue of the hip yoke, pinch and crush points, guarding) |
| Standard reference | Machinery: 12100 §5.3, §6.2; 13482 §5.4, §5.13; 10218-1 §5.10; Other: ISO 13857; Machinery Reg. Annex III §1.3 |
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

Mechanical, structural and stability analysis of the robot: mass and centre of gravity, tip-over margin standing and walking and under an external load, the fall energy of a 35 kg body from 1.2 m, fatigue of the 7075-T6 hip yoke and the SLM 316L arm parts, pinch, crush and shear points at the 25 joints, guarding. Closes GAP-03 and GAP-04.

## 2. Mass properties

Mass 35 kg (upstream figure, to be weighed), centre of gravity from the CAD and the MuJoCo model, reach envelope about 1.5 m diameter, standing footprint about 0.4 m by 0.3 m.

## 3. Stability

Static tip-over margin, lateral load at the shoulder (SYRS-021: 50 N), slope limit 5°, the fall energy at the centre of mass. The fall energy and the tip-over margin are inputs to the fall-arrest budget of WP-S-04.

## 4. Structural

Hip-yoke fillet stress and fatigue life (FM-01, HWRS-002), material substitution (FM-02), harmonic gear derating (FM-04), SLM porosity (FM-30), fastener torque and threadlocker (FM-03).

## 5. Pinch, crush and shear points

Knee, elbow, hip, neck, waist yaw, the toe joint; gaps per ISO 13857; the labyrinth guard of SF-07.

## 6. Manual handling

35 kg lift (SF-18); lifting points.

## 7. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G2 |
