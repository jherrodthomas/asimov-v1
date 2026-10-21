# WP-H-05 Electrical and battery safety: supply disconnection, overcurrent protection, insulation, the lithium pack and its BMS, charger

| Field | Value |
|---|---|
| Work product | WP-H-05 Electrical and battery safety: supply disconnection, overcurrent protection, insulation, the lithium pack and its BMS, charger |
| Standard reference | Other: 60204-1 §5–§8, §18; 62133-2; UN 38.3 |
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

Electrical and battery safety of the robot: supply disconnection, overcurrent protection, protection against electric shock, bonding, the lithium battery pack and its BMS (IEC 62133-2, UN 38.3), the charger, and the verification of IEC 60204-1 §18.

## 2. Supply and disconnection

A lockable disconnector on the battery rail (GAP-08); the XT30 5 V input; the charger interface.

## 3. Overcurrent and short-circuit protection

Per-branch fuses on the motor rails (SF-11), fuse table in the PDB BOM (FM-16), harness protection.

## 4. Battery

The pack is user-supplied and excluded from the kit (GAP-12, DQ-009): compliance gate, certified-pack list, BMS interlock (SYRS-014), enclosure, thermal runaway containment, charging and storage rules.

## 5. Verification

Continuity, insulation, residual voltage, functional tests per IEC 60204-1 §18.

## 6. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G3 |
