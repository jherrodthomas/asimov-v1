# WP-O-04 Field monitoring and incident reporting

| Field | Value |
|---|---|
| Work product | WP-O-04 Field monitoring and incident reporting |
| Standard reference | SRP/CS: 61508-1 §7.15; IEC 62443: 62443-4-1 DM-1; Other: Machinery Reg. Art. 10; AI Act Art. 72 |
| Version | 0.0 (skeleton: structure, clause map and seeds from the concept-phase package; 2026-10-21) |
| Status | Skeleton |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `3d4ec9d` (BL-001) |

> [!NOTE]
> **Skeleton.** The structure and clause mapping exist; the content is still to be written. The gate that needs this
> work product is **G6** ([WP-M-00](../01-management/WP-M-00-work-product-register.md#3-register)).

## 1. Purpose

Field monitoring and incident reporting: how events in operation and in testing are collected, triaged and fed back into the analyses; obligations of a manufacturer under the Machinery Regulation (Art. 10) and, if ever applicable, AI Act post-market monitoring.

## 2. Signals monitored

Test logs, anomalies, E-stop presses and their causes, falls and near-falls, contacts, near misses, upstream advisories, component recalls, battery incidents. Anomalies, logs and results are published as they happen; video behind the consent of the people in it (DQ-051 A, 2026-10-21).

## 3. Procedure

Intake → triage within two business days → classification → containment → root cause → corrective action → verification → closure.

## 4. Metrics

Demands on each safety function per operating hour; uncontrolled falls; contacts above the limit; unplanned DAMP transitions.

## 5. Feeding the analyses

Routing of a confirmed finding back into the work products that own it:

| Finding | Re-opens |
|---|---|
| Potential safety function failure or fault in the field | WP-C-03 risk assessment, WP-A-01 system FMEA |
| New performance limit or triggering condition | WP-C-10 insufficiency analysis, WP-V-08 field trials |
| New misuse pattern | WP-C-06 interaction and misuse, WP-O-03 information for use |
| Learned-component anomaly | WP-W-10 ML engineering, WP-C-09 ML component definition |
| Operating-environment limit found not to hold | WP-C-02 operating environment, WP-C-03 risk assessment |
| Counter-evidence to the safety case | WP-K-01 safety case |

## 6. Reporting to authorities

What, when and to whom under the Machinery Regulation once a unit is placed on the market.

## 7. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G6 |
