# WP-M-03 Project plan (scope, WBS, schedule, resources)

| Field | Value |
|---|---|
| Work product | WP-M-03 Project plan (scope, WBS, schedule, resources) |
| Standard reference | ASPICE: MAN.3 |
| Version | 0.0 (skeleton: structure, clause map and seeds from the concept-phase package; 2026-10-21) |
| Status | Skeleton |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `3d4ec9d` (BL-001) |

> [!NOTE]
> **Skeleton.** The structure and clause mapping exist; the content is still to be written. The gate that needs this
> work product is **G0** ([WP-M-00](WP-M-00-work-product-register.md#3-register)).

## 1. Purpose

Scope, work breakdown, effort, schedule logic, resources and tracking for taking the fork through the assurance path of [WP-M-01](WP-M-01-assurance-strategy.md). Safety responsibilities are in [WP-M-02](WP-M-02-safety-plan.md); risks to the plan in [WP-M-07](WP-M-07-risk-management.md).

## 2. Scope

In scope: the reference configuration of WP-M-01 §3.1 (the DIY-kit robot as published, tethered in a laboratory, OE-1), every work product of WP-M-00, the engineering changes that close the gap assessment's findings, and the infrastructure the fork lacks (a firmware repository, a bench, a gantry and tether, a test area). Out of scope: the home and public envelopes OE-3 and OE-4 until the lead widens the item (DQ-002).

## 3. Work breakdown structure

One element per phase P0…P6 and per work-product group, following [WP-M-01 §7](WP-M-01-assurance-strategy.md#7-phases-gates-and-sequence). To be drawn as a generated figure from this table.

## 4. Effort and staffing

Hours per element against the roles of WP-M-02 §3.1; the lead's available hours per week are a decision for the register.

## 5. Schedule and gate roadmap

Gate dates once the hours are known; the long-lead items are the firmware and API that upstream has not released (GAP-16, GAP-18), the E-stop architecture (DQ-008 A), the battery policy (DQ-009 A), the fork's minimal firmware (DQ-023 A) and the gantry (DQ-027); G0 passed with conditions on 2026-10-21 (DQ-020 A) and G1 waits on the first hang test (DQ-030). Upstream's DIY-kit shipping date (summer 2026, already passed at BL-001) is an external date the plan tracks, not depends on.

## 6. Interfaces

Upstream Asimov Inc ([WP-M-10](WP-M-10-upstream-and-supplier-management.md)), the assessor, a notified body if any (WP-M-13).

## 7. Tracking

Monthly progress review against WP-M-00 status, open items, risks and the decision register; gate reviews per WP-M-02 §10.

## 8. Backlog

B-nn items with status, drawn from the gap assessment's priority actions §10 and the DFMEA action plan tracker of the concept-phase package.

## 9. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G0 |
