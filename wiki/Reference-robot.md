# Reference robot

The first configuration the assurance work analyses is **CFG-001, the kit robot as published**: the Asimov v1 a
builder can make from the repository and the DIY kit today, hanging from or standing under a gantry on a rated
tether, fed from a bench supply with no battery, moved by tele-operation. It is a starting point, not a limit:
**CFG-002**, the battery-powered robot walking under the learned locomotion policy that upstream intends to sell, is
tracked and joins the claimed scope when its firmware, API and policy reach a public repository, through a
documented impact analysis. This page says what the reference configuration is, why it was proposed, and what the
fork adds to it before any test.

> **Nothing about this robot is approved for operation around people.** As inherited it has no documented
> emergency-stop architecture, no contactor, no fuse table, no disconnect, no battery specification, no declared
> joint limits, no firmware in any public repository, and its only declared safe state, motors limp, drops a 35 kg
> body from 1.2 m ([gap assessment](../assurance/00-assessment/gap-assessment.md)).

## CFG-001 at a glance

| Attribute | Value | Source |
|---|---|---|
| Body | 1.2 m, 35 kg biped; 25 actuated degrees of freedom (two 6-DOF legs with a passive toe each, two 5-DOF arms, waist yaw, 2-DOF neck); machined 7075 aluminium, MJF PA12 nylon, SLM 316L stainless; seven subassemblies from pelvis to head | [WP-C-01 §1.1](../assurance/02-concept/WP-C-01-item-definition.md); [`mechanical/`](../mechanical/) |
| Actuators | BLDC with harmonic gear and encoder, one type for all 25, each on a connector carrying battery power and CAN; the only published limits are simulation control ranges | WP-C-01 §1.1; GAP-06 |
| Compute | Raspberry Pi 5 edge board in the head (camera, microphones, speaker, WebRTC, the Asimov API); Radxa CM5 motion control board with an on-board IMU, six CAN ports (five at 1 Mbps, one for the BMS at 500 kbps), a UART debug port | [`electrical/`](../electrical/README.md); [architecture overview](../docs/architecture.md) |
| Sensing | 2 MP monocular camera (no range to a person), quad microphone array, 6-DOF IMU, joint encoders | WP-C-01 §1.1 |
| Power | 5 V to the motion control board; the actuator rail through the harness; a power distribution board listed in the kit but not in the repository; no battery in the kit; on CFG-001 a bench supply with a current limit | GAP-08, GAP-12 |
| Emergency stop | A wireless E-stop listed in the kit; architecture, receiver, contactor and stop category unknown; on CFG-001 the fork adds a wired pendant | GAP-07, GAP-11 |
| Modes | DAMP (motors limp; the default on disconnect or E-stop release), STAND, MOVE | WP-C-01 §5 |
| Software | None in any public repository: no firmware, no API, no policy, no app | GAP-16…GAP-18 |
| Mass, centre of gravity, tip-over margin, fall energy | Not measured anywhere; the package estimates roughly 400 J at the centre of mass in a fall | GAP-03 |
| Fall protection (fork) | Overhead gantry and rated tether with a quick-release; the feet reach the floor only when the gantry is lowered | [WP-V-07 §2](../assurance/06-validation/WP-V-07-test-operations.md) |

## What the fork adds before any test

The hold point [WP-V-07](../assurance/06-validation/WP-V-07-test-operations.md) requires bench equipment on any unit
the fork powers: a gantry or rated anchor point with a tether sized for the robot's mass under a dynamic load and a
lowering mechanism; a wired, dual-channel emergency stop on a pendant in the operator's hand, through a safety relay
or two contactors, that removes the actuator rail and needs a deliberate re-arm; a bench supply with a current limit
and a switch within reach, in place of a battery; known joint torque and velocity limits, or the actuators' hardware
current limits set to a named value; an identifiable controller build whose behaviour on heartbeat loss, E-stop and
fault is written down; the robot weighed; a marked, empty test area with the operator and the observer outside it.
Buying the gantry and the pendant are decisions for the lead (DQ-007, DQ-008); the battery policy is DQ-009. The
bench chain is carried forward as the first draft of the product chain, and the tether and gantry become a
complementary measure of the risk reduction concept, not thrown away.

## What the reference configuration fixes

[WP-M-01 §3.1](../assurance/01-management/WP-M-01-assurance-strategy.md#31-reference-configuration-the-only-scope-claims-apply-to)
makes the reference configuration the only scope the claims apply to:

| Element | Reference configuration |
|---|---|
| Robot | The kit robot as published plus the bench equipment; later the product stop chain and safety layer of WP-S-03 |
| Function | Standing and tele-operated motion of the limbs in a supervised laboratory; walking only on the gantry. No autonomous locomotion policy, no battery, no collaborative task (DQ-002, DQ-003) |
| Software | None published yet. When upstream releases the firmware, the API and the policy, a tagged fork release pins them by commit; until then the software work products define the interface the record needs |
| Operating environment | Defined in [WP-C-02](../assurance/02-concept/WP-C-02-operating-environment-and-tasks.md): envelope OE-1, a laboratory with a level dry floor, a cleared and marked area, a trained operator and at most one observer, nobody within reach of a limb while powered |
| Operator | A trained test operator with a hand on the wired E-stop during development; briefed personnel after release |

## Why CFG-001 and not the battery and policy robot

Upstream's roadmap marks the Asimov API, the locomotion policy and the mobile app as upcoming; the battery is
excluded from the kit and user-supplied. None of it is in a public repository. A safety case can only be built on
what can be read and tested, and a learned balance controller nobody can inspect cannot carry a safety function
until the lead says so (DQ-006). The recommendation (decision DQ-003) is to assess the kit robot now, tethered and
bench-powered, and to track CFG-002's announced properties as claims to verify: the policy, the battery with its
BMS, the wireless E-stop and its link. Most of the record carries over, because the structure, the actuators, the
motion control board and the CAN topology are the same; the software and battery findings will be re-stated when the
code and the pack specification arrive.

## Adding CFG-002, or a wider envelope

1. Record the new configuration with its item boundary and the interface assumptions the base case already states
   (the BMS handshake, the policy's inputs and outputs, the wireless link).
2. Write the impact analysis ([WP-M-11](../assurance/01-management/WP-M-11-impact-analysis.md) format): which
   hazards, safety functions, requirements and assumptions hold, which differ, and what evidence each needs.
3. For an industrial cell (OE-2), extend the risk assessment with the collaborative-operation hazards of ISO 10218-2
   and ISO/TS 15066 and measure the contact limits; a home or public envelope (OE-3, OE-4) is a second item under
   ISO 13482 and a decision for the lead (DQ-002).
4. Verify the policy, the firmware and the battery pack against the claims recorded from upstream's announcements
   once their sources are public, under the upstream management process
   ([WP-M-10](../assurance/01-management/WP-M-10-upstream-and-supplier-management.md)).
5. Run the generators and open a pull request.
