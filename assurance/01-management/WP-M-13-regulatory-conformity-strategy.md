# WP-M-13 Regulatory Conformity Strategy

| Field | Value |
|---|---|
| Work product | WP-M-13 Regulatory conformity strategy (Machinery Regulation, AI Act, US frame) |
| Standard reference | Regulation (EU) 2023/1230 (Machinery Regulation): Art. 3 (definitions, substantial modification), Art. 10 (obligations of manufacturers), Art. 20 (presumption of conformity), Art. 21 (EU declaration of conformity), Art. 25 (conformity assessment procedures), Annex I (high-risk categories; Part A: safety components with self-evolving behaviour using machine learning), Annex III (essential health and safety requirements), Annex IV (technical documentation), Annex V (declaration), Annexes VI–X (modules A, B, C, H, G); Regulation (EU) 2024/1689 (AI Act): Art. 6 (classification), Art. 43 (conformity assessment), Annex I (Union harmonisation legislation), Annex IV (technical documentation); ANSI/RIA R15.06-2012 and ANSI/A3 R15.08 (US, deferred, see §6) |
| Version | 0.1 (initial strategy; 2026-10-21) |
| Status | Draft |
| PL / scope | Regulatory (all) |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1); legal review TBD |
| Approver | Project maintainer |
| Baseline | `3d4ec9d` (BL-001) |

> [!NOTE]
> This document is engineering planning, not legal advice. Article and annex numbers are quoted from the Official
> Journal texts as understood by the authors and must be checked by someone qualified before any declaration is
> drafted (OI-1).

## 1. Purpose

Asimov v1 is machinery, and in the EU machinery is placed on the market under Regulation (EU) 2023/1230, which
applies from 20 January 2027 and replaces Directive 2006/42/EC. This document records which regulations apply to the
fork, which route to conformity is recommended, what the technical documentation must contain, and how the
assurance work products of [WP-M-00](WP-M-00-work-product-register.md) map onto it. The frame itself is decision
DQ-001 (EU recommended); the route follows from it and from the position on the learned policy (DQ-006).

## 2. What the fork is, in regulatory terms

| Question | Position | Consequence |
|---|---|---|
| Is the fork a manufacturer? | Only if a fork build is placed on the market or put into service by the project. Today the fork is an assurance record for a DIY kit sold by Asimov Inc and built by its buyers; a unit the maintainer builds and runs in a laboratory is "putting into service for own use" at most | The obligations of Art. 10 are planned for, not yet incurred; the hold point WP-V-07 governs own use |
| Who is the manufacturer of a DIY-kit robot? | Whoever assembles the kit and puts it into service makes the machine; Asimov Inc supplies a kit of parts and a design. The Regulation's treatment of kits supplied for assembly by the user must be checked (OI-1) | The fork plans the whole technical file as if it were the manufacturer of the unit it builds |
| Is a humanoid "machinery" or "partly completed machinery"? | Machinery: it has a drive system and performs a function on its own (standing, walking, reaching). Without its locomotion policy it is still machinery under tele-operation | One declaration of conformity for the robot in its claimed envelope |
| Is any safety component a product in its own right? | The E-stop devices, the safety relay or contactors, and a certified battery pack with BMS are bought safety components with their own declarations; the fork integrates them | Their certificates are evidence in WP-H-07, not something the fork issues |
| Does Annex I Part A apply (mandatory third-party assessment)? | Part A lists safety components and machinery with "fully or partially self-evolving behaviour using machine learning approaches ensuring safety functions". If the learned locomotion policy carries the stability function SF-01 (DQ-006 option B), Part A **is triggered**. The recommended position (DQ-006 A) keeps every safety function on deterministic code and hardware, so Part A is **not triggered** | The route depends on DQ-006: Module A is available only under option A |
| Is the robot a "personal care robot"? | Only if the lead widens the item to OE-3 or OE-4 (DQ-002). ISO 13482 is used as the hazard catalogue regardless | No personal-care claim in the first item |

## 3. Route to conformity (decision pending DQ-001 and DQ-006)

Art. 25 offers internal production control (Module A, Annex VI) where the machinery is not in Annex I and the
harmonised standards covering all the essential requirements are applied; otherwise EU type-examination plus
conformity to type (Modules B and C, Annexes VII and VIII), full quality assurance (Module H, Annex IX) or unit
verification (Module G, Annex X).

| Option | What it means for the fork | Cost | Recommendation |
|---|---|---|---|
| A: Module A, harmonised standards in full (ISO 10218-1/-2, ISO 13849-1, EN 60204-1, ISO 13850; ISO 13482 if a personal-care envelope is ever claimed) | The fork self-declares against Annex III using the presumption of conformity of Art. 20. The technical documentation must still be complete and available for ten years | No notified body fee. The standards must be bought and applied in full; any deviation voids the presumption for that requirement | **Recommended**, conditional on DQ-006 option A (no safety function on the learned policy) and DQ-004 option A (PL d with the tether) |
| B: Module B + C, EU type-examination | A notified body examines the technical documentation and the type; gives an independent view the project otherwise lacks | Fee (indicative four to five figures); scheduling | **Mandatory** if DQ-006 allocates SF-01 to the policy (Annex I Part A); worth it anyway once the robot is to stand free near people |
| C: Module H | A certified quality system covering design and production | Out of proportion for a one-person open-source project | Not recommended |

Whichever module is chosen, the harmonised standards are listed in the Official Journal under the Regulation only
once the Commission cites them; until then the standards give state of the art, not presumption. OI-2 tracks the
citation status of ISO 10218-1/-2 (2025 editions), ISO 13482 and ISO 13849-1:2023 under the new Regulation.

## 4. Technical documentation (Annex IV)

Annex IV requires, in summary: a general description; the complete drawings and the calculations, test results and
certificates needed to check conformity; the risk assessment documentation (the hazards identified, the essential
requirements that apply, the measures taken and the residual risks); the standards applied; technical reports with
test results; the instructions for use; the declaration of incorporation for any partly completed machinery; the
declaration of conformity; and, for machinery with self-evolving behaviour, the data and logs that describe it.

[WP-K-02](../10-safety-case/WP-K-02-technical-documentation-index.md) is the index. The mapping from Annex IV items to
work products:

| Annex IV item (summary) | Work products |
|---|---|
| General description, intended use, limits | WP-C-01, WP-C-02 |
| Drawings, circuit diagrams, calculations | WP-H-02, WP-H-04, WP-H-05, WP-H-08, WP-S-03, WP-S-04; the mechanical CAD and the motion control board sources of the repository |
| Risk assessment documentation | WP-C-03, WP-C-04, WP-C-05, WP-C-06, WP-C-10 |
| Standards and specifications applied | WP-M-00 (clause columns), WP-M-01 §4 |
| Technical reports and test results | WP-V-01…WP-V-05, WP-V-08, WP-S-09, WP-H-06, WP-W-06…W-08 |
| Certificates of safety components | WP-H-07 |
| Instructions for use | WP-O-01, WP-O-02, WP-O-03 |
| Software description, configuration, parameters | WP-W-03, WP-W-09, WP-P-01 (baselines) |
| Cybersecurity (Annex III §1.1.9 protection against corruption, §1.2.1 safety and reliability of control systems) | WP-C-07, WP-C-08, WP-S-07, WP-W-11, WP-V-06, WP-K-03 |
| Self-evolving behaviour: the data and logs (only if DQ-006 B) | WP-W-10, WP-K-07 |
| Declaration of conformity | WP-K-06 |
| Safety case (not required by the Regulation; the project's own argument) | WP-K-01 |

## 5. The AI Act threshold

Regulation (EU) 2024/1689 Art. 6(1) makes an AI system high-risk when it is a safety component of a product covered
by the Union harmonisation legislation listed in Annex I and that product must undergo third-party conformity
assessment. The Machinery Regulation is in Annex I Section A. The locomotion policy is an AI system. Whether it is a
safety component is exactly decision DQ-006:

- **Option A (recommended):** the fork keeps the policy outside every safety function (WP-M-01 T-03;
  [WP-C-09](../02-concept/WP-C-09-ml-component-definition-and-safety-requirements.md)), stability in OE-1 rests on the
  gantry and tether, and the AI Act's high-risk obligations do not apply. [WP-K-07](../10-safety-case/WP-K-07-ai-act-conformity-record.md)
  records that position with its evidence.
- **Option B:** SF-01 is allocated to the policy. The robot is in Annex I Part A of the Machinery Regulation,
  third-party assessment is mandatory (Module B), the policy is a high-risk AI system, and WP-K-07 is rewritten as a
  full Annex IV technical documentation with the data governance, logging, robustness and human-oversight
  requirements of the AI Act.

ML-R3 in [WP-M-06 §7](WP-M-06-confirmation-measures-plan.md#7-cybersecurity-and-ml-reviews) reviews the record at
G5. The threshold is also crossed if a learned perception model is ever made the trigger of SF-06 without a
deterministic bound.

## 6. Other markets

If the lead chooses the US frame (DQ-001 B or C), ANSI/RIA R15.06-2012 (industrial robots, adopting ISO 10218),
ANSI/A3 R15.08 (industrial mobile robots) and the OSHA general duty clause apply at a workplace, and consumer use
falls under the CPSC. The plan is a cross-reference table from the ISO 10218 and ISO 13849-1 requirements to
R15.06 added to this document, with any additional tests appended to WP-V-01, not a second technical file. Nothing is
done on it until DQ-001 is answered.

## 7. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Have the article and annex references of this document, and the treatment of a kit assembled by its buyer, checked against the Official Journal text by someone qualified | PM | G1 |
| OI-2 | Track the citation of ISO 10218-1/-2:2025, ISO 13482:2014 and ISO 13849-1:2023 as harmonised standards under Regulation (EU) 2023/1230; until cited, state "state of the art" rather than "presumption of conformity" everywhere | SM | G1 |
| OI-3 | Decide the module once DQ-001 and DQ-006 are answered; confirm or withdraw NB-1 in WP-M-06 | PM | G1 |
| OI-4 | Confirm with the lead that no fork build will be made available to anyone outside the project before G5 | PM | G0 |
