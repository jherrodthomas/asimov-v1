# Frequently asked questions

Short answers with a link to the record that holds the long one.

## Is the robot safe, certified or CE-marked?

No. Asimov v1 is research hardware. As inherited it has no documented emergency-stop architecture, no fuse table, no
disconnect, no battery specification, no declared joint limits, no firmware in any public repository, and nothing
that arrests the fall of a 35 kg body when power is removed. The fork's record exists to change that in the open,
starting with the [gap assessment](../assurance/00-assessment/gap-assessment.md). No safety function reaches any
Performance Level today, no assessment has taken place, and nothing is approved for operation around people.
[For the assessor](For-the-assessor.md) says what an assessment would involve.

## Is the fork safer than upstream Asimov v1?

Not yet, and the project does not claim it is. The fork makes no change to the robot; what it adds today is the
record: the gap assessment, the strategy, the plans, the register, the process model, the Living Safety Case records
and the concept work products ported from the fork's earlier concept-phase package. The first engineering change will
be bench equipment for any unit the fork tests with: a gantry and tether, a wired E-stop and a bench supply. Buying it
waits on decisions by the lead.

## Why does a humanoid need a gantry?

Because removing power drops the robot. On a wheeled machine, cutting the motors is the safe state; on a 35 kg biped
standing 1.2 m tall it is a fall of roughly 400 J onto whoever is nearby. What the safe state should be (a controlled
descent, holding the pose, or power off) is an open question for the lead (DQ-005). Until a controlled-descent
function exists and is verified, the tether and gantry of the laboratory envelope carry the fall, and the record
says so as a claim of its own ([WP-K-01](../assurance/10-safety-case/WP-K-01-safety-case.md) G2.4,
[WP-V-07](../assurance/06-validation/WP-V-07-test-operations.md)).

## Why machinery and robot standards and not ISO 26262?

Because a humanoid is machinery under Regulation (EU) 2023/1230 and a robot that shares space with people, not a
road vehicle. The standards are ISO 12100, ISO 10218-1/-2 with ISO/TS 15066, ISO 13482, ISO 13849-1, IEC 60204-1,
IEC 62133-2, IEC 62443 and ISO/IEC TR 5469. ISO 3691-4, the driverless-truck standard, does not apply to a legged
robot either. [How we use each standard](How-we-use-each-standard.md) has the mapping.

## What is a Performance Level, and why PL d?

ISO 13849-1's measure of how reliably a safety function performs, PL a to PL e. The inherited hazard analysis reads
PL e for the fall and contact hazards of a free-standing robot near people; the record proposes PL d for the stop
and fall functions in the laboratory, with the tether as the complementary measure that lowers the exposure. Whether
the lead accepts that, or holds the functions to PL e, is an open decision (DQ-004). See the [glossary](Glossary.md).

## Where are the safety functions implemented?

In two places, neither of which exists yet. The limits and monitors (joint torque and velocity clamps, IMU
plausibility, the watchdog, the mode machine, the controlled descent) belong to a deterministic safety layer on the
motion control board, the last software before the actuators. Power removal (the emergency stop and its link
surveillance) belongs to a hardwired stop chain: dual-channel E-stop devices through a safety relay that drops the
actuator-rail contactors, with a BMS interlock on the battery configuration. The tele-operation stack and the
learned locomotion policy above them are hardened as defence in depth but carry no Performance Level claim. The
argument is in
[WP-M-01 §6](../assurance/01-management/WP-M-01-assurance-strategy.md#6-safety-architecture-argument-the-central-strategy).

## Can the learned locomotion policy keep the robot upright?

Nobody outside upstream has seen it; it is not in any public repository. Whether balance (SF-01) may rest on a
learned component, or stability is claimed only through the tether and gantry while the policy stays a functional
component, is a decision for the lead (DQ-006). Until it is answered the record allocates no safety function to a
learned component, which also keeps the robot out of the Machinery Regulation's Annex I Part A and the AI Act's
high-risk obligations ([WP-M-09](../assurance/01-management/WP-M-09-ml-safety-plan.md),
[WP-C-09](../assurance/02-concept/WP-C-09-ml-component-definition-and-safety-requirements.md)).

## Why a fork rather than contributing upstream?

The assurance work needs a record that moves at its own pace, with its own baselines, gates and decision authority,
and must be free to say what the evidence does not support. Upstream neither produced nor endorses the record. The
robot's sources stay in the same repository beside it, unchanged except through the change process, and upstream is
treated as a supplier ([WP-M-10](../assurance/01-management/WP-M-10-upstream-and-supplier-management.md)); its manual
and roadmap are quoted, never restated.

## Where is the Living Safety Case dashboard?

On the README, generated from the records in [`case/`](../assurance/case/README.md) by CI. No number on it is a
safety claim: a claim counts as accepted only when a recorded review accepts it, its evidence is available and
accepted, and no defeater against it is open. Today nothing is accepted and every defeater is open.

## Who decides what?

The project lead is the safety authority and decides risk acceptance, the required PL, the safe state of the biped,
robot behaviour defaults, operating-envelope limits, money, hardware, the assessor, roles and gates. Everything else
is a technical choice, recorded so the lead can change it. See [how decisions are made](How-decisions-are-made.md).

## I found a safety problem. Where do I report it?

- A security vulnerability: follow [SECURITY.md](../SECURITY.md).
- A hazard, a near miss, a fall or an event: the Safety concern issue template.
- Anything else: the Problem report template. See [reporting a safety concern](Reporting-a-safety-concern.md).

## Why is so much of it written with a coding assistant?

Drafting is done in assistant sessions under the project lead's direction; the working rules are in
[CLAUDE.md](../CLAUDE.md). Every change goes through pull request review and the workflows described in
[how the repository is organized](How-the-repository-is-organized.md). The lead holds every safety decision, AI-drafted
work counts at independence level I0, and no work product leaves draft without a review by someone else
([WP-M-02 §3.3](../assurance/01-management/WP-M-02-safety-plan.md#33-ai-assisted-authoring)).

## Something is missing here

Open an [issue](https://github.com/jherrodthomas/asimov-v1/issues). Questions that come up more than
once get added to this page by pull request against [`wiki/`](../wiki/README.md).
