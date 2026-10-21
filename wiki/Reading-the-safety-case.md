# Reading the safety case

The safety argument is published while it is being built. This page explains what the safety case is today, what
the Living Safety Case dashboard shows, and what it does and does not promise.

## Today

The safety case is the document [WP-K-01](../assurance/10-safety-case/WP-K-01-safety-case.md), a draft with the
claim structure of [WP-M-01 §3.2](../assurance/01-management/WP-M-01-assurance-strategy.md#32-top-level-claim),
seeded from the fork's concept-phase package and reworked to the record's rules:

- **G0** The reference configuration CFG-001, operated within its laboratory envelope OE-1 by briefed personnel,
  does not expose people to unacceptable risk.
- **G1** Every safety function with a required Performance Level reaches it, with one sub-claim per function:
  bipedal stability, controlled descent, the joint torque and velocity clamps, the emergency stop and its link
  surveillance, the watchdog, IMU plausibility and the rest.
- **G2** The complementary mechanical, electrical and procedural measures are implemented, including the claim that
  the tether and gantry carry the fall hazard while no fall-arrest function exists (G2.4).
- **G3** The command path (tele-operation and the API) cannot defeat the safety functions.
- **G4** The evidence was produced under a controlled process, and the DIY-kit build is controlled.

No claim has accepted evidence. The known counter-evidence is GAP-01…GAP-34 in the
[gap assessment](../assurance/00-assessment/gap-assessment.md), registered one for one as the first defeaters, all
open. The position on the learned locomotion policy sits inside G1 and G2.4: until the lead decides otherwise, no
safety function is allocated to a learned component and stability in the laboratory is claimed only through the
gantry.

## What the dashboard shows

[`assurance/case/`](../assurance/case/README.md) holds claims, arguments, evidence items, defeaters, actions,
configurations, baselines and reviews as machine-readable records, a validator, and a generator that draws the
README dashboard and a one-line headline: the lifecycle stage, the baseline, the number of claims and how many have
accepted evidence, the evidence items and how many are accepted, the open defeaters, and a digest of every record.
These rules apply:

- A claim counts as accepted only when a recorded review accepts it, every piece of evidence it cites is available
  and accepted, and no defeater against it is open. The validator refuses anything else.
- A passing CI run, a passing test or the existence of a document never accepts a claim on its own, and an
  AI-generated review is not a substitute for independent confirmation.
- Every figure is generated from the records, never typed by hand, and the assurance workflow fails when the
  committed dashboard is out of date.

## Why zero accepted is the honest number

Evidence becomes *accepted* only after a confirmation review by someone independent of the author
([WP-M-06](../assurance/01-management/WP-M-06-confirmation-measures-plan.md)). No work product has had one, no
assessor is engaged, and the project has one person. The evidence items that exist are the concept-phase workbooks,
the drafted work products and the upstream sources, recorded as partial and unreviewed; the rest are not yet
performed. A dashboard that showed accepted evidence before any review had happened would be the one to distrust.

## How the records fit together

1. **Hazards and safety functions**, from the [risk assessment](../assurance/02-concept/WP-C-03-risk-assessment.md)
   and the [safety function specification](../assurance/02-concept/WP-C-04-safety-functions-and-plr.md), as trace
   items under [`trace/`](../assurance/trace/README.md). Each function carries a required PL, pending the lead.
2. **Claims**: the argument that each function achieves its PL, each complementary measure is in place and each
   hazard is reduced, broken into statements that can be evidenced.
3. **Evidence**, linked to claims: the PL calculation, the component certificates, the fall and controlled-descent
   tests on the gantry, the contact measurements, the E-stop tests, the fault-injection results, each with a review
   state.
4. **Defeaters**, attached to claims: the gap assessment, the open interfaces of the process model, the
   performance limits of the insufficiency analysis.
5. **Configurations, baselines and reviews**: which robot the claims are about (CFG-001 evaluated, CFG-002 tracked),
   named states of the whole, and the confirmation reviews recorded against them.

- [Read the safety case, WP-K-01](../assurance/10-safety-case/WP-K-01-safety-case.md)
- [The records, validator and dashboard generator](../assurance/case/README.md)
- [Known gaps](../assurance/00-assessment/gap-assessment.md)
- [Gate skeletons](../assurance/10-safety-case/gates/skeletons/), generated from the process model

> Assurance status represents recorded engineering evidence and review state. It does not constitute
> certification or approval for operation around people.
