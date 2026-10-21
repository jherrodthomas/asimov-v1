# WP-M-06 Confirmation Measures Plan

| Field | Value |
|---|---|
| Work product | WP-M-06 Confirmation measures plan (reviews, validation independence, functional safety assessment, conformity assessment) |
| Standard reference | ISO 13849-1:2023 §8 (verification of the PL) and §10 (validation, performed by persons independent of the design where practicable); ISO 13849-2:2012 §4 (validation principles, independence); IEC 61508-1:2010 §8 (functional safety assessment, independence by consequence class); IEC 62061:2021 §5 (verification and validation planning); IEC 62443-4-1:2018 SM-13 (continuous improvement, reviews); Regulation (EU) 2023/1230 Art. 25 and Annexes VI–X (conformity assessment procedures) |
| Version | 0.1 (initial plan; 2026-10-21) |
| Status | Draft |
| PL / scope | All. Planned to PL d until the safety functions are approved (DQ-004) |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1); confirmation review of this plan by the external assessor (I3 planned) |
| Approver | Safety manager |
| Baseline | `3d4ec9d` (BL-001) |

## 1. Purpose

This plan defines the confirmation measures for the Asimov v1 fork: which work products get a confirmation review
and at what independence, when the functional safety audits and assessments take place, who may perform them, how
the independent cybersecurity and ML reviews and the regulatory conformity assessment fit in, and where the records
go.

No confirmation measure has been performed at baseline `3d4ec9d`. No assessor is engaged: the question is open
(DQ-010, recommended not for now), so every I2 and I3 measure in this plan is **unscheduled** until it is answered,
and no work product can leave Draft through a confirmation measure. The standards are not bought either (DQ-013),
so every clause reference stays marked as to be checked. The concept-phase package the fork inherited was itself
produced with AI assistance and never reviewed; it counts as an author-side pre-review at I0 and gives no credit
here.

The machinery standards do not define a confirmation review. ISO 13849-1 asks for verification (§8) and validation
(§10) and recommends that validation is done by persons independent of the design; IEC 61508-1 §8 defines the
functional safety assessment and its independence (independent person, department or organisation, rising with the
consequence of failure). This plan uses one vocabulary (confirmation reviews CR-nn at independence levels I0 to I3)
and maps it onto those requirements, so that one set of records, checkers and gate skeletons serves every measure.

Confirmation measures are separate from verification reviews. Verification reviews (normally by pull request, per
[WP-P-05](../07-supporting/WP-P-05-verification-review-procedure.md)) check a work product against its inputs and
requirements. Confirmation measures check that the work product, the process and the overall result meet the
standards and are adequate for the safety argument.

## 2. Planning assumptions

- **Required PL.** The safety functions are specified at concept level in WP-C-04 with the targets of the
  concept-phase package (PL d for the stop and fall functions, PL e for the battery protection). For planning,
  every measure is planned at the independence IEC 61508-1 §8 would set for the PL d consequence class. When the
  lead answers DQ-004 and WP-C-04 is approved, the safety manager re-plans (OI-2). Lowering independence needs a
  recorded rationale.
- **Tailoring.** WP-M-01 T-09: verification reviews may be done by project members at I0/I1. Confirmation measures at
  I2 and I3 are performed by an external party because the project has one maintainer.
- **Scope.** Confirmation measures apply to the reference configuration ([WP-M-01 §3.1](WP-M-01-assurance-strategy.md#31-reference-configuration-the-only-scope-claims-apply-to)).
- **Conformity assessment.** Whether a notified body examines the technical documentation depends on the frame and
  route (DQ-001, WP-M-13 §3) and on whether the learned locomotion policy becomes a safety component (DQ-006,
  Machinery Regulation Annex I Part A). NB-1 below is a placeholder until both are answered.

## 3. Independence levels

Summary in the project's own words, mapped onto IEC 61508-1 §8. The licensed standards are authoritative.

| Level | Meaning (summary) | IEC 61508-1 §8 counterpart | Who can do it in the fork today |
|---|---|---|---|
| I0 | The measure should be performed; it may be done by the person who produced the work | — | Maintainer (self-check) |
| I1 | Performed by a person other than the one who produced the work product | Independent person | Any competent contributor other than the author. Nobody available yet |
| I2 | Performed by a person independent of the team responsible for the work product | Independent department | External reviewer only |
| I3 | Performed by a person independent, in management, resources and release authority, of the organisation responsible for the work | Independent organisation | External assessor only |

## 4. Confirmation reviews

### 4.1 List and independence

| # | Confirmation review of | Work product(s) | Why this level | Planned | Performed by | Gate |
|---|---|---|---|---|---|---|
| CR-01 | Impact analysis of the inherited baseline and the concept-phase package | [WP-M-11](WP-M-11-impact-analysis.md) | Decides what is reused; high independence regardless of PL | I3 | External FS assessor | G0 |
| CR-02 | Risk assessment, including the hazard list and risk evaluation | [WP-C-03](../02-concept/WP-C-03-risk-assessment.md) (with [WP-C-01](../02-concept/WP-C-01-item-definition.md), [WP-C-06](../02-concept/WP-C-06-human-robot-interaction-and-misuse.md) as inputs) | The foundation of every claim; ISO 12100 §7 documentation is what an assessor reads first; the PL e readings of the inherited HARA need an outside eye | I3 | External FS assessor | G1 |
| CR-03 | Safety plan (incl. tailoring rationale) | [WP-M-02](WP-M-02-safety-plan.md), [WP-M-01 §5](WP-M-01-assurance-strategy.md#5-tailoring), this plan | Tailoring away from the manufacturer model, and the position on the learned policy, need an outside eye | I3 | External FS assessor | G0 (re-confirm at G1 after the risk assessment) |
| CR-04 | Safety functions with required PL, and the risk reduction concept | [WP-C-04](../02-concept/WP-C-04-safety-functions-and-plr.md), [WP-C-05](../02-concept/WP-C-05-risk-reduction-concept.md) | The PLr from the risk graph and the safe state of the biped fix the whole hardware budget | I3 | External FS assessor | G1 |
| CR-05 | Safety requirements specification and the stop chain and safety-layer architecture | [WP-S-02](../03-system/WP-S-02-safety-requirements.md), [WP-S-03](../03-system/WP-S-03-technical-safety-concept.md), [WP-S-04](../03-system/WP-S-04-response-time-and-stopping-budget.md), [WP-S-05](../03-system/WP-S-05-safety-chain-io-interface.md) | Category and designated architecture decided here | I3 | External FS assessor | G2 |
| CR-06 | Safety analyses (system, hardware, software) | [WP-A-01](../08-analyses/WP-A-01-system-fmea.md)…[WP-A-05](../08-analyses/WP-A-05-independence-of-the-safety-chain.md), [WP-H-08](../04-hardware/WP-H-08-mechanical-and-stability-analysis.md) at G2; [WP-H-03](../04-hardware/WP-H-03-hardware-failure-analysis.md), [WP-W-04](../05-software/WP-W-04-software-safety-analysis.md) at G3 | Fault exclusions, the fall energy and the independence argument are where optimism hides | I3 | External FS assessor | G2 (system), G3 (HW, SW) |
| CR-07 | PL calculation: MTTFD, DCavg, CCF scoring, SISTEMA project | [WP-H-04](../04-hardware/WP-H-04-reliability-data-and-pl-calculation.md) | The arithmetic the PL claim rests on | I3 | External FS assessor | G3 |
| CR-08 | Qualification of safety components | [WP-H-07](../04-hardware/WP-H-07-safety-component-qualification.md) | Certificates, well-tried arguments and fault exclusions per component; the actuators have none | I3 | External FS assessor | G3 |
| CR-09 | Software tool qualification | [WP-P-07](../07-supporting/WP-P-07-tool-classification-qualification.md) | Completeness of the tool record | I2 minimum, I3 if combined with the CR-08 session | External reviewer or assessor | G3 |
| CR-10 | Qualification of software components | [WP-P-08](../07-supporting/WP-P-08-software-component-qualification.md) | The real-time kernel, the CAN stack and the policy runtime are central to the functional layers | I2 minimum | External reviewer or assessor | G3 |
| CR-11 | Proven-in-use argument | [WP-P-09](../07-supporting/WP-P-09-proven-in-use.md) | **Not planned while no proven-in-use claim is made (T-06).** Becomes I3 if a claim is introduced | — | — | — |
| CR-12 | Safety case (completeness) | [WP-K-01](../10-safety-case/WP-K-01-safety-case.md) | The argument as a whole | I3 | External FS assessor | G5 (interim look at G1, G2 as part of the interim FSA) |

### 4.2 Procedure

1. The safety manager opens an issue `CR-nn <WP-ID>` in the gate milestone, naming the work product version and
   baseline commit.
2. Entry criteria: the work product is at least `Draft`, its verification review per WP-P-05 is complete, and its
   open items are listed.
3. The reviewer evaluates compliance with the cited standards (and, for CR-03, with the project's tailoring) and
   adequacy for the safety argument.
4. Outcome: `Confirmed`, `Confirmed with findings` (findings tracked as issues), or `Not confirmed`.
5. Record stored as `10-safety-case/confirmation/CR-nn-<WP-ID>-v<version>.md` (folder and naming rules:
   [`confirmation/README.md`](../10-safety-case/confirmation/README.md)).
6. If the work product changes after confirmation in a way that the change impact analysis
   ([WP-P-02](../07-supporting/WP-P-02-change-management.md)) classifies as safety-relevant, the confirmation review is
   repeated or its scope is extended.

## 5. Functional safety audit

**Purpose:** check that the processes in the safety plan are carried out as planned (IEC 61508-1 §6 management
requirements; ISO 13849-1 §4 planning).

| Item | Plan |
|---|---|
| Independence | I3 planned. Performed by the external FS assessor or an auditor of equivalent independence |
| AUD-1 | At G2: configuration management of the fork and the firmware, API and policy repositories, change control with impact analysis, review records, the decision register as a record of risk acceptance |
| AUD-2 | At G4: the bench and gantry campaign, test records, problem resolution, tool qualification in use |
| Record | `10-safety-case/confirmation/AUD-<n>.md` |

## 6. Functional safety assessment

**Purpose:** judge whether the safety functions achieve their required PL and whether the residual risk in the
claimed operating envelope is acceptable (IEC 61508-1 §8; ISO 13849-1 §10 validation of the achieved PL against the
PLr).

| Measure | When | Scope | Independence |
|---|---|---|---|
| FSA-I1 | G1 | Robot definition, risk assessment, safety functions and PLr, risk reduction concept (WP-C-01, C-03, C-04, C-05) | I3 |
| FSA-I2 | G2 | SRS, stop chain and safety-layer architecture, fall-arrest budget, system analyses (WP-S-02…S-05, WP-A-01…A-05) | I3 |
| FSA-F | G5 | Everything, against the safety case; report is [WP-K-04](../10-safety-case/WP-K-04-functional-safety-assessment.md); covers the validation report [WP-V-01](../06-validation/WP-V-01-safety-validation.md) | I3 |

### 6.1 Assessor qualification and independence

No authorship of or contribution to the assessed work; no reporting line to the maintainer; no financial interest
beyond the fee; no involvement in upstream Asimov Inc development; competence at the level
[WP-M-04 §4](WP-M-04-organization-competence-safety-culture.md) sets for robot and machinery functional safety
(ISO 13849-1, ISO 10218, ISO 13482, IEC 60204-1 experience, with evidence); declared in writing in each report.

## 7. Cybersecurity and ML reviews

| Measure | When | Scope | Independence |
|---|---|---|---|
| CS-I1 | G1 | Threat and risk assessment, requirements and security level target, links to the hazard list ([WP-C-07](../02-concept/WP-C-07-cybersecurity-threat-and-risk-assessment.md), [WP-C-08](../02-concept/WP-C-08-cybersecurity-requirements-and-sl-target.md)) | External reviewer with IEC 62443 competence |
| CS-A1 | G5 | Cybersecurity assessment; report is [WP-K-05](../10-safety-case/WP-K-05-cybersecurity-assessment.md); covers [WP-V-06](../06-validation/WP-V-06-cybersecurity-validation.md) and the cybersecurity case [WP-K-03](../10-safety-case/WP-K-03-cybersecurity-case.md) | External cybersecurity assessor |
| ML-R1 | G1 | Classification of the locomotion policy and the position DQ-006 settles; the insufficiency analysis ([WP-C-09](../02-concept/WP-C-09-ml-component-definition-and-safety-requirements.md), [WP-C-10](../02-concept/WP-C-10-functional-insufficiency-analysis.md)) | External reviewer with ML competence (may be the FS assessor) |
| ML-R2 | G3 | ML engineering evidence of the policy ([WP-W-10](../05-software/WP-W-10-ml-engineering.md)) | Same |
| ML-R3 | G5 | AI Act conformity record ([WP-K-07](../10-safety-case/WP-K-07-ai-act-conformity-record.md)), if the policy has become a safety component; otherwise a record that it has not | Same |

## 8. Conformity assessment

| Measure | When | Scope | Who |
|---|---|---|---|
| NB-1 (placeholder) | G5 | EU type-examination of the technical documentation ([WP-K-02](../10-safety-case/WP-K-02-technical-documentation-index.md)) and the declaration of conformity draft ([WP-K-06](../10-safety-case/WP-K-06-release-record.md)), if the route of WP-M-13 §3 selects Module B or H, or if Annex I Part A applies because the learned policy carries a safety function (DQ-006 B) | Notified body |

If Module A (internal control) is selected and the policy carries no safety function, NB-1 is withdrawn and the
manufacturer's own assessment of the technical documentation is covered by FSA-F and CR-12.
[WP-M-13](WP-M-13-regulatory-conformity-strategy.md) owns the route.

## 9. Schedule summary

| Gate | Confirmation measures due |
|---|---|
| G0 | CR-01, CR-03 |
| G1 | CR-02, CR-03 (re-confirm), CR-04; FSA-I1; CS-I1; ML-R1 |
| G2 | CR-05, CR-06 (system); FSA-I2; AUD-1 |
| G3 | CR-06 (HW, SW), CR-07, CR-08, CR-09, CR-10; ML-R2 |
| G4 | AUD-2 |
| G5 | CR-12; FSA-F (WP-K-04); CS-A1 (WP-K-05); ML-R3; NB-1 |

## 10. Records

All confirmation records are stored in [`assurance/10-safety-case/confirmation/`](../10-safety-case/confirmation/README.md).
Each record contains: identifier; object (work product ID, version, baseline commit); reviewer name and independence
declaration; date; method; findings with IDs; outcome. Findings are tracked as GitHub issues labelled
`confirmation-finding` and resolved via [WP-P-03](../07-supporting/WP-P-03-problem-resolution.md). The register
(WP-M-00 §4) points here for confirmation review and audit reports.

## 11. Open items

| ID | Open item | Owner | Due |
|---|---|---|---|
| OI-1 | Check every clause reference in this plan and in WP-M-00 against licensed copies of ISO 13849-1:2023, ISO 13849-2:2012, IEC 61508-1:2010, ISO 10218-1, ISO 13482:2014 and ISO 12100:2010 (decision DQ-013 on buying them; unscheduled until DQ-010) | SM | G0 |
| OI-2 | Re-plan independence after DQ-004 is answered and WP-C-04 is approved; record the rationale for any reduction from the PL d assumption | SM | G1 |
| OI-3 | Engage the external FS assessor or record the decision not to (DQ-010) | PM | G1 |
| OI-4 | Identify a cybersecurity assessor and a penetration tester; agree the independence statement | CSM | G1 |
| OI-5 | CR-01 and CR-03 are due at G0 but no assessor is engaged; decide whether G0 can pass with them scheduled rather than performed (ties to DQ-010) | SM | G0 |
| OI-6 | Confirm or withdraw NB-1 once DQ-001 and DQ-006 are answered | SM | G1 |
