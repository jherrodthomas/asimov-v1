# WP-M-01 Assurance Strategy and Lifecycle Tailoring

| Field | Value |
|---|---|
| Work product | WP-M-01 Assurance strategy and lifecycle tailoring |
| Standard reference | ISO 12100:2010 §4 (strategy for risk assessment and risk reduction); ISO 13849-1:2023 §4 (overview, planning); IEC 61508-1:2010 §6 (management of functional safety, tailoring of the lifecycle); IEC 62443-4-1:2018 SM-1 (development process); ISO/IEC TR 5469:2024 (AI in safety functions, informative); UL 4600 (safety case structure, informative); Regulation (EU) 2023/1230 Art. 25 (conformity assessment procedures) |
| Version | 0.7 (2026-10-21): batch 6 applied and batch 7 opened in §8. 0.6 (2026-10-21): batch 5 applied (DQ-054 A in §7) and batch 6 opened in §8. 0.5 (2026-10-21): batch 4 applied and batch 5 opened in §8. 0.4 (2026-10-21): batch 3 applied and batch 4 opened in §8. 0.3 (2026-10-21): batch 2 applied (DQ-015 A editions, DQ-023 A the fork's firmware) and batch 3 opened in §8. 0.2 (2026-10-21): the ten decisions of batch 1 applied to §2, §4 and §8; batch 2 opened. 0.1 (initial strategy; 2026-10-21) |
| Status | Draft |
| PL / scope | All (machinery and robot safety, SRP/CS, cybersecurity, ML, process) |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1); confirmation review of the tailoring rationale by an independent assessor (I3) |
| Approver | Project maintainer (acting safety manager). Self-approval is an accepted interim limitation until a second person takes the safety manager or reviewer role ([WP-M-02](WP-M-02-safety-plan.md) OI-2, DQ-011) |
| Baseline | `3d4ec9d` (BL-001) |

## 1. Purpose

This document is the assurance path for the Asimov v1 fork. It sets out:

1. what the fork will claim, and for which configuration of the robot,
2. the safety architecture argument that makes those claims achievable on a bipedal humanoid built from an open
   hardware record whose firmware and controller are not yet public,
3. which standards apply to a humanoid robot, how each one is used and where it is tailored, with rationale,
4. the phases, gates and work products that take the project from today's baseline to a release decision,
5. the strategic decisions the project must take, and the risks to the plan.

The [safety plan (WP-M-02)](WP-M-02-safety-plan.md), [cybersecurity plan (WP-M-08)](WP-M-08-cybersecurity-plan.md),
[ML safety plan (WP-M-09)](WP-M-09-ml-safety-plan.md) and [regulatory conformity strategy (WP-M-13)](WP-M-13-regulatory-conformity-strategy.md)
carry out this strategy for their own disciplines. The [work product register (WP-M-00)](WP-M-00-work-product-register.md)
lists every output. The standards are the machinery and robot set, because a humanoid that stands, walks and reaches
among people is machinery under Regulation (EU) 2023/1230 and a robot under ISO 10218 and ISO 13482, not a road
vehicle and not a driverless truck.

## 2. Starting point

From the [baseline gap assessment](../00-assessment/gap-assessment.md), at the commit in its header:

- The fork carries no change to the robot. It carries a **concept-phase engineering package** written in May 2026
  with AI assistance and never reviewed: a safety-case workbook with 32 hazards, a HARA, 25 safety functions and
  28 gaps, a DFMEA with 32 failure modes, 120 requirements, 139 test cases and an architecture description. It is
  the seed of this record and is recorded as partial, unreviewed evidence, never as a finding closed.
- **The robot that exists is a mechanical and electrical record.** Mechanical CAD of seven subassemblies, the
  motion control board (a Radxa CM5 carrier with six CAN buses and an IMU), a WireViz harness that feeds every
  actuator battery power and CAN, and a MuJoCo model with per-joint control ranges. No firmware, no API, no
  locomotion policy and no app are in any public repository; upstream marks them as upcoming (GAP-16, GAP-17,
  GAP-18).
- **No safety function reaches any Performance Level.** The kit declares a wireless E-stop and nothing about its
  architecture; there is no power distribution board, fuse table, disconnection device or battery in the record;
  the three operating modes DAMP, STAND and MOVE are described in a manual whose safety pages return 404 (GAP-02,
  GAP-07, GAP-08).
- **The safe state is the problem.** For a wheeled machine the safe state is power off. For a 35 kg biped standing
  1.2 m tall, power off is a fall of about 411 J at the centre of mass; the package lists the DAMP mode itself as
  a hazard (HZ-C01) and its DFMEA asks for a controlled descent that does not exist (GAP-10).
- **Balance is a learned function.** The package allocates the stability function SF-01 to the locomotion policy,
  a neural network trained in simulation that nobody outside upstream has seen (GAP-13). Whether a learned
  component may carry a safety function, and what that means under ISO/IEC TR 5469 and the AI Act, is the
  strategic question of this record (DQ-006; answered A on 2026-10-21: the policy carries no safety function).
- **The risk graph reads PL e for the worst rows.** A 35 kg body falling onto a person is S2 F2 P2 in the inherited
  HARA, which gives PL e for tip-over, loss of balance, arm sweep, pinch, policy edge cases and communication loss.
  PL e is not reachable with single-channel actuators and an unreleased controller; a complementary measure that
  removes the fall (a gantry and tether in the laboratory) is what makes PL d a defensible target (DQ-004 A and DQ-007 A, decided 2026-10-21).
- **The battery is somebody else's.** The kit ships without one; what a builder installs is uncontrolled, and the
  DFMEA rates the missing BMS as the one failure mode with no detection at all (GAP-12).
- **Process is honest and thin.** Upstream publishes its hardware under CERN-OHL-S-2.0 and its software under
  GPL-2.0, keeps the design in git with pull requests, and says plainly what is not yet released. There is no risk
  assessment, no safety function, no verification record and no quality system behind the kit (GAP-27…GAP-34).

## 3. What the fork will claim

### 3.1 Reference configuration (the only scope claims apply to)

| Element | Reference configuration |
|---|---|
| Robot | The **Asimov v1 DIY-kit robot as published** at BL-001: 1.2 m, 35 kg, 25 actuated joints (two 6-DOF legs with passive toes, two 5-DOF arms, waist yaw, 2-DOF neck), BLDC actuators with harmonic gears and encoders on six CAN buses, a Radxa CM5 motion control board with an LSM6DSV IMU, a Raspberry Pi 5 edge board with camera, microphones and speaker, 7075-T6 aluminium and MJF PA12 structure; **plus the bench equipment the fork adds before any powered test** (§4.1 of WP-M-02, [WP-V-07](../06-validation/WP-V-07-test-operations.md)): a gantry and rated tether, a wired E-stop in the operator's hand, a bench power supply in place of a battery. Recorded as `CFG-001` in the Living Safety Case |
| Function | Standing and tele-operated motion of the limbs in a supervised laboratory; walking only on the gantry. No autonomous locomotion policy, no battery, no collaborative task ([decision register](decisions/register.yaml) DQ-002, DQ-003) |
| Software | None published at BL-001. When upstream releases the firmware, the API and the policy, a tagged fork release pins them by commit; until then the software work products define the interface the record needs |
| Operating environment | Defined in [WP-C-02](../02-concept/WP-C-02-operating-environment-and-tasks.md): operating envelope OE-1, a laboratory with a level dry floor, a cleared and marked area, a trained operator and at most one observer, nobody within reach of a limb while powered |
| Operator | A trained test operator with a hand on the wired E-stop during development ([WP-V-07](../06-validation/WP-V-07-test-operations.md)). After release: personnel briefed per [WP-O-03](../09-production-operation/WP-O-03-information-for-use.md) |

The choice of the kit robot as published over waiting for upstream's software is decision DQ-003 (A, decided
2026-10-21). Because no firmware exists in public, the fork writes a minimal firmware of its own for the motion
control board (DQ-023 A, decided 2026-10-21): CAN actuator control with the clamps, the watchdog, the E-stop input
and a DAMP-only fallback, enough for the hang tests; the controlled descent waits for a controller. The battery-powered, free-standing robot under the locomotion policy is tracked as `CFG-002`, every statement
about it a claim to verify, never evidence, until its code is public.

Any other configuration, including OE-2 (an industrial cell), OE-3 (a home) and OE-4 (public space), needs an impact
analysis ([WP-M-11](WP-M-11-impact-analysis.md)) and supporting evidence before it joins the claimed scope.

### 3.2 Top-level claim

> **G0**: The Asimov v1 reference configuration (CFG-001), operated within its operating envelope OE-1 by personnel
> briefed as its information for use requires, does not expose people to unacceptable risk. The residual risk after
> the three-step method of ISO 12100 is acceptable for the robot's intended use and reasonably foreseeable misuse.

Sub-claims that structure the [safety case (WP-K-01)](../10-safety-case/WP-K-01-safety-case.md):

| Sub-claim | Standards | Core argument |
|---|---|---|
| G1 Every safety function with a required Performance Level reaches it | ISO 13849-1/-2, ISO 10218-1 §5.4, EN 60204-1, ISO 13850 | The safety functions (WP-C-04) are implemented by a hardwired stop chain and a deterministic safety layer on the motion control board whose category, MTTFD, DCavg and CCF are calculated (WP-H-04) and validated (WP-V-01…V-05), and the policy and tele-operation layers above them cannot defeat them (WP-A-05) |
| G2 The complementary mechanical, electrical and procedural measures are implemented, including the tether and gantry that carry the fall hazard in OE-1 | ISO 12100 §6, ISO 13482 §5.4, §5.13, IEC 60204-1, IEC 62133-2 | Structure, guarding, electrical protection, the battery policy and the procedures of WP-C-05 are in place and verified; the gantry removes the fall onto a person while no fall-arrest function exists |
| G3 The command path cannot defeat the safety functions | IEC 62443-4-1/-4-2 | The threat assessment (WP-C-07) covers the tele-operation channel, the API, the debug ports and the E-stop link; the stop chain is a zone with no network conduit (WP-S-07) |
| G4 The evidence was produced under a controlled process and the kit build is controlled | IEC 61508-1 §6, §8; ASPICE; ISO 9001 (informative) | Plans, configuration management, change control, reviews, the confirmation measures of WP-M-06, and the build acceptance checks of WP-O-01 |

The position on the learned policy is carried inside G1.1 (SF-01) and G2.4 (the tether): until the lead decides
DQ-006, no safety function is allocated to a learned component and stability in OE-1 is claimed only through the
gantry.

**No claim is made, now or as a target, for a free-standing robot near people, for a battery-powered robot, for any
collaborative task, for operation outside the laboratory, or for any configuration outside §3.1.**

## 4. The standards and how each one is used

Asimov v1 is machinery and a robot. The method is one hazard log, one requirements database, generated figures and
a Living Safety Case; the standards that feed it are these.

| Question | Answered with | Where |
|---|---|---|
| What are the hazards and how much risk reduction does each need? | **ISO 12100** risk assessment (three-step method) on the hazard catalogues of **ISO 12100 Annex B** and **ISO 13482 Annex A** (the only standard with a personal-care hazard list: falls, contact, restraint, autonomous decisions); **ISO 10218-1** Annex A for the robot-system hazards; required **Performance Level** from the ISO 13849-1 Annex A risk graph | WP-C-01, C-03, C-04, C-05 |
| Which safety functions must the robot have? | **ISO 10218-1:2025 §5** (the 2025 editions are cited, DQ-015 A; the package's 2011 clause references are remapped under WP-M-06 OI-1): emergency stop, protective stop, speed and force limits, singularity and axis limits; **ISO 13482 §5 and §6**: stability, contact force and energy, E-stop, safety-related control; **ISO 13850** for the emergency stop; **EN 60204-1 §9** for stop categories | WP-C-04 |
| How much contact is allowed? | **ISO/TS 15066** Annex A body-region limits (the source of the limits until the 2025 annex of ISO 10218-2 is checked, DQ-015 A) for transient and quasi-static contact; **ISO 13482 §5.7** limits to forces, pressures and energies; **ISO 13857** reach and gap distances | WP-C-06, S-04, V-03 |
| How good must the control system be, and how is that shown? | **ISO 13849-1** categories B to 4, MTTFD, DCavg, CCF, PL a to e; **ISO 13849-2** validation and fault lists; **IEC 62061 / IEC 61508** where 13849 runs out (software beyond 13849-1 §7, management, assessment) | WP-S-02…S-05, WP-H-01…H-07, WP-W-01…W-09, WP-V-01…V-05 |
| Is the electrical installation and the battery safe? | **IEC 60204-1**: supply disconnecting device, overcurrent protection, protection against electric shock, control circuits, verification; **IEC 62133-2** and UN 38.3 for the lithium pack | WP-H-02, H-05 |
| What if nothing fails but the policy or the perception gets it wrong? | No machinery standard covers performance limits of a learned balance controller. **ISO 21448 is used as an informative method** (triggering conditions, known and unknown scenarios) inside WP-C-10 and WP-V-08; the resulting limits become operating-environment limits or safety functions | WP-C-10, V-08 |
| What if someone attacks it? | **IEC 62443-4-1** (secure development lifecycle) and **62443-4-2** (component requirements, security level target); 62443-3-2 for the zone and conduit model | WP-M-08, C-07, C-08, S-07, W-11, V-06, O-05 |
| How far can a learned component be trusted? | **ISO/IEC TR 5469**: AI technology class and usage level; the fork's position until DQ-006 is answered is that no learned component implements a safety function. **AI Act** Annex I lists the Machinery Regulation, so a learned safety component would be a high-risk AI system | WP-M-09, C-09, W-10, K-07 |
| Is the whole argument convincing? | **UL 4600** principles for the safety case; the Living Safety Case records and generators | WP-K-01, `case/` |
| What does the law require? | **Regulation (EU) 2023/1230** (Machinery Regulation, applies from 20 January 2027): essential health and safety requirements (Annex III), technical documentation (Annex IV), conformity assessment (Art. 25, Annexes VI–X) with third-party assessment mandatory for machinery with self-evolving safety behaviour (Annex I Part A); **Regulation (EU) 2024/1689** (AI Act) for a learned safety component; and, since the lead chose both frames (DQ-001 C), the US workplace frame as a cross-reference: ANSI/RIA R15.06, ANSI/A3 R15.08, NFPA 79, OSHA (WP-M-13 §6) | WP-M-13, K-02, K-06, K-07 |
| Are the processes capable? | **ASPICE 4.0** kept as the process capability frame (self-assessment); **ISO 9001** cited by the package for design control and records, used informatively in WP-M-05 | WP-M-12, WP-M-05 |

How each standard is cited: work products are structured after these standards and cite their clauses. **No
compliance is claimed**, because no assessment has been performed and the drafting environment has no licensed copy
of any standard (WP-M-06 OI-1). The wiki page [How we use each standard](../../wiki/How-we-use-each-standard.md)
is the plain-language version of this table.

## 5. Tailoring

The machinery standards assume a manufacturer placing a finished machine on the market. The fork is an open-source
assurance record for a DIY kit designed by someone else and built by whoever buys it. The table records each
tailoring decision. Each one needs confirmation review by an independent assessor.

| # | Topic | Decision | Rationale |
|---|---|---|---|
| T-01 | Lifecycle entry | Treat the fork as a **modification of existing machinery**: impact analysis ([WP-M-11](WP-M-11-impact-analysis.md)), then a full concept phase. The concept-phase package is seed material ported into the work products and reviewed there, never reused as a finished work product | Upstream has no safety work product; the package is unreviewed AI-assisted drafting at I0 |
| T-02 | Machine boundary | The machine is the kit robot as built plus the bench equipment the fork adds (gantry, tether, wired E-stop, bench supply). The operator's device, the Wi-Fi network, the charger and the battery are outside the machine, with interface assumptions | The fork controls the robot's build and configuration; it does not control the site network or what a builder plugs in |
| T-03 | Safety function allocation | **The stops that remove motor power (the E-stop SF-13 and the power-removal leg of SF-08) are implemented by a hardwired chain alone** (devices, receiver, contactors). **The limits and monitors (SF-03, SF-23, SF-24, SF-25, SF-14, SF-11) are implemented by a deterministic safety layer on the motion control board**, which carries a PL claim at their PLr and the ISO 13849-1 §7 lifecycle. **The fall-arrest function SF-02 is a deterministic controlled-descent sequence in the same layer** (DQ-005). **The locomotion policy and the tele-operation stack are functional layers with no PL claim**; SF-01 is withdrawn as a safety function unless the lead allocates it to the policy (DQ-006) | Keeps the PL d argument inside deterministic code and certified components; avoids a TR 5469 argument for a network nobody has seen; matches the package's own request for a controlled descent |
| T-04 | Firmware as safety-related embedded software | No firmware exists at BL-001. The safety layer is specified by the fork (WP-W-02, WP-W-03) against the interface the manual describes, and **claimed** only once its evidence exists: reproducible build, coding rules, static analysis, unit and integration tests with coverage, a software safety analysis and independent review (WP-W-01…WP-W-08 at PL d). Until then no software claim is made | The layer is the only thing that can give a biped a safe state better than a fall |
| T-05 | Hardware | Safety components are bought with certificates (E-stop devices, safety relay or contactors, a certified battery pack with BMS) and qualified under ISO 13849-1 as well-tried or certified components; the actuators, encoders, IMU and boards are safety-related parts whose reliability data upstream must supply (GAP-14) or which the fork derates and monitors | No supplier evidence exists for the actuators; the chain removes power upstream of them |
| T-06 | Proven in use | **Not claimed** for any element. Upstream's build history is supporting evidence only ([WP-P-09](../07-supporting/WP-P-09-proven-in-use.md)) | No controlled configuration or field-problem history that would meet IEC 61508 |
| T-07 | Production | Tailored to the DIY-kit build: assembly, commissioning and acceptance checks of a kit ([WP-O-01](../09-production-operation/WP-O-01-assembly-installation-commissioning.md)). The fork manufactures nothing; the instructions, the material certificates and the acceptance checks are the product | The robot is built by whoever follows the instructions; material substitution and harness quality are the DFMEA's highest-detection-score failures |
| T-08 | Upstream | Asimov Inc is treated as an upstream supplier with no development interface agreement; the supplier-side activities fall to the fork ([WP-M-10](WP-M-10-upstream-and-supplier-management.md)). Upstream's manual and roadmap are quoted, never restated | Upstream is under no contract |
| T-09 | Independence | Verification reviews may be done by project members (I0/I1), never by the author. With one maintainer, I1 review needs an external reviewer and self-review is recorded as I0. Confirmation reviews of the risk assessment, the safety plan and the safety case, and the functional safety assessment, need an **external** assessor (I2/I3) ([WP-M-06](WP-M-06-confirmation-measures-plan.md)) | One maintainer today |
| T-10 | Performance limits of perception and the policy | ISO 21448 is used as a method, not a standard to comply with, inside WP-C-10 and WP-V-08 | No machinery standard covers it and the package's worst rows (policy edge cases, DAMP as a hazard) are performance limits, not faults |
| T-11 | Cybersecurity scope | IEC 62443-4-1 practices are applied to the fork's software once it exists; IEC 62443-4-2 component requirements to the robot as one component with the security level target the lead sets (DQ-012). The site network and the operator's device are external zones | The fork controls the robot's software and configuration, not the network it is deployed on |
| T-12 | Process capability | ASPICE 4.0 is used for a self-assessment of process capability ([WP-M-12](WP-M-12-process-capability-baseline.md)), target CL2 for management, support, system and software processes, CL1 for hardware and ML. No ASPICE assessment is claimed; the package's ISO 9001 findings are closed through WP-M-05 | Continues the gap assessment's GAP-34 rating; gives the fork a process model the robot standards lack |
| T-13 | Regulatory | EU frame recommended (DQ-001): Machinery Regulation and the harmonised route through ISO 10218, ISO 13482 and ISO 13849-1. The conformity module follows in WP-M-13 §3. The AI Act applies only if a learned component becomes a safety component, which T-03 avoids unless DQ-006 says otherwise | Where the richest robot-safety standards are; one technical file |
| T-14 | Operating envelopes | **OE-1 only** in the first item (DQ-002 recommended A): a supervised, tethered laboratory. OE-2 (industrial cell), OE-3 (home) and OE-4 (public) are a second item each, with their own hazard rows already rated in WP-C-03 so that the base case need not be rewritten when they come | The robot cannot be run anywhere else today; the package counts 12, 19 and 21 open gaps for the other envelopes |

## 6. Safety architecture argument (the central strategy)

### 6.1 Doer, checker, and a checker of last resort, with a safe state that is not a fall

```
 ┌──────────────── humanoid ─────────────────────────────────────────────────────────────────┐
 │  Raspberry Pi 5 (edge)             Radxa CM5 motion control board           Hardwired     │
 │  ┌──────────────────────────┐      ┌────────────────────────────────┐      stop chain     │
 │  │ tele-operation (WebRTC)  │      │ SAFETY LAYER: clamps (SF-03),  │     ┌────────────┐  │
 │  │ Asimov API, media, voice │─────▶│ IMU plausibility (SF-23),      │────▶│ E-stop     │  │
 │  │ locomotion policy        │ cmd  │ watchdog (SF-24, SF-08),       │ CAN │ devices    │──┼─▶ motor rail
 │  │ (learned, when released) │◀─────│ mode machine DAMP/STAND/MOVE,  │     │ receiver   │  │   contactors
 │  └──────────────────────────┘      │ controlled descent (SF-02)     │     │ BMS h'shake│  │   actuators
 │        FUNCTIONAL (no PL claim)    └────────────────────────────────┘     └────────────┘  │
 │                                       PL d target · deterministic           PL d target   │
 └───────────────────────────────────────────────────────────────────────────────────────────┘
          Gantry and tether: carry the fall while no fall-arrest function is verified (OE-1)
          Operator: hand on the wired E-stop during development (WP-V-07)
```

- **Doer:** the tele-operation stack and, when released, the locomotion policy. They decide where each joint goes.
  Everything they publish is a request. They are functional software with no safety claim.
- **Checker (SRP/CS):** the safety layer on the motion control board. The last software before the actuators. It
  clamps every torque and velocity command (SF-03), rejects an implausible attitude estimate (SF-23), runs a
  deadline monitor backed by a hardware watchdog (SF-24), enforces the mode machine, and on a fault or a lost
  heartbeat performs the controlled descent that is the biped's safe state (SF-02, SF-08). This is where the PL d
  argument for the limits and monitors is made, with the ISO 13849-1 §7 software lifecycle.
- **Checker of last resort (SRP/CS):** the hardwired stop chain. E-stop devices and a surveilled wireless receiver
  drop the motor-rail contactors; a BMS handshake keeps the rails off without a compliant battery. Nothing in
  software can hold a contactor closed. This is where the PL d argument for power removal is made, with certified
  components and calculated MTTFD, DCavg and CCF.
- **The fall:** power removal drops the robot. In OE-1 the gantry and tether carry that fall (G2.4); the controlled
  descent of SF-02 is what will one day let the robot be lowered rather than dropped. Until it is verified, no
  free-standing operation is in the case.

### 6.2 Consequences that shape the plan

1. **The safe state must be decided before anything else is designed.** Controlled descent, hold, or power off
   (DQ-005) fixes SF-02, SF-08, the E-stop's stop category (DQ-016) and the fall-arrest budget of
   [WP-S-04](../03-system/WP-S-04-response-time-and-stopping-budget.md).
2. **Balance is either a learned safety function or not a safety function.** DQ-006 decides whether the record
   argues a TR 5469 class for the policy and files under the AI Act, or withdraws SF-01 and claims stability only
   through the gantry. The recommendation is the latter until the policy is public.
3. **The gantry is the first hardware.** Nothing powered touches the floor without it ([WP-V-07](../06-validation/WP-V-07-test-operations.md),
   DQ-007); it is what turns the PL e rows of the inherited HARA into PL d rows in OE-1 (DQ-004).
4. **The software starts from nothing.** No firmware, API or policy exists in public; the software work products
   begin with the environment ([WP-W-01](../05-software/WP-W-01-software-development-environment-guidelines.md)) and the
   interface the manual describes, and every software claim waits for upstream's release or a fork implementation.
5. **Reliability data decides whether PL d is even computable.** Twenty-five actuators of one type with no failure
   rate, no B10d and no certificate (GAP-14); the PL calculation ([WP-H-04](../04-hardware/WP-H-04-reliability-data-and-pl-calculation.md))
   waits on upstream or a supplier.
6. **The battery is a policy, not a part.** A certified-pack list and a BMS handshake interlock (DQ-009) are the only
   way to turn the package's worst-rated assumption into a measure.
7. **Independence of the chain from the stack is the hinge.** The safety layer shares the CM5 with the policy
   runtime and the CAN buses with every actuator; shared processors, buses and power are each analysed in
   [WP-A-05](../08-analyses/WP-A-05-independence-of-the-safety-chain.md).

## 7. Phases, gates and sequence

The lifecycle has seven phases, each closed by a gate; gate names and exit criteria are in
[WP-M-00 §2](WP-M-00-work-product-register.md#2-gates), the activities per phase in [WP-M-02 §4](WP-M-02-safety-plan.md#4-lifecycle-activities-per-phase),
and the integrated maps in the [process model (WP-P-11)](../process/README.md).
The second item (OE-2) starts after G5 of this one (DQ-054 A, decided 2026-10-21).

| Phase | Gate | What it settles | Hold points |
|---|---|---|---|
| P0 Governance | G0 | Plans, roles, configuration control, the frame (DQ-001), the envelopes (DQ-002), the reference configuration (DQ-003) | None; the fork powers nothing |
| P1 Concept | G1 | Robot limits, the first site and the bench equipment (DQ-044, DQ-035), operating envelopes, risk assessment, safety functions with PLr, the safe state (DQ-005), the policy position (DQ-006), the gantry and E-stop (DQ-007, DQ-008), the battery policy (DQ-009), cybersecurity and ML concepts, test operations | **Hold point:** no powered test with the feet on the floor without the gantry, the wired E-stop and WP-V-07 approved |
| P2 System design | G2 | SRS, stop chain and safety-layer architecture, fall-arrest and response-time budget, I/O map, structural and stability analysis, system analyses | |
| P3 HW/SW development | G3 | Chain hardware and PL calculation, the safety layer and its verification, qualification of components and tools, ML engineering evidence | |
| P4 Integration and verification | G4 | Integration, PL verification, stability and fall tests on the gantry, contact measurements, E-stop tests, fault injection | **Hold point:** no person within reach of a powered limb before WP-V-03 passes |
| P5 Validation and release | G5 | Validation on the robot, cybersecurity validation, safety case, assessment, technical file, release record | |
| P6 Operation | G6 | Field monitoring, incident response, updates | |

## 8. Strategic decisions required

Each decision is asked of the project lead through the [decision register](decisions/README.md); this table is the
index, the register entry is the question.

| # | Decision | Register | Status |
|---|---|---|---|
| D-01 | Regulatory frame: EU machinery, US, or both | DQ-001 | Decided 2026-10-21: C, both; one EU technical file with a US cross-reference (WP-M-13 §6) |
| D-02 | Operating envelopes in the first item: OE-1 only | DQ-002 | Decided 2026-10-21: A |
| D-03 | Reference configuration: the kit robot as published, tethered and bench-powered | DQ-003 | Decided 2026-10-21: A (CFG-001) |
| D-04 | Required PL for the stop and fall functions: PL d with the tether as complementary measure | DQ-004 | Decided 2026-10-21: A |
| D-05 | Safe state of the biped: controlled descent, hold, or power removal | DQ-005 | Decided 2026-10-21: A, controlled descent then power removal; the E-stop removes power at once |
| D-06 | Allocation of the stability function SF-01 to the learned policy | DQ-006 | Decided 2026-10-21: A, not allocated; SF-01 withdrawn |
| D-07 | Fall protection for the laboratory: gantry and tether | DQ-007 | Decided 2026-10-21: A |
| D-08 | Emergency-stop devices: wired tether E-stop plus the surveilled wireless device | DQ-008 | Decided 2026-10-21: A |
| D-09 | Battery policy: certified-pack list and BMS handshake interlock | DQ-009 | Decided 2026-10-21: A |
| D-10 | Independent assessor: when | DQ-010 | Decided 2026-10-21: A, not for now; revisit at G1 |
| D-11 | Roles and self-approval while the project has one person | DQ-011 | Decided 2026-10-21: A |
| D-12 | Cybersecurity security level target | DQ-012 | Decided 2026-10-21: A, SL 2 for FR 1, 3, 5, 7; SL 1 otherwise |
| D-13 | Buying the standards | DQ-013 | Decided 2026-10-21: A, not until an assessor is engaged |
| D-14 | Joint torque and velocity limits in the laboratory | DQ-014 | Decided 2026-10-21: A, half the MuJoCo range until measured |
| D-15 | Editions of ISO 10218 to cite | DQ-015 | Decided 2026-10-21: A, the 2025 editions |
| D-16 | Stop category of the emergency stop on a biped | DQ-016 | Withdrawn 2026-10-21: settled by D-05 (category 0) |
| D-17 | Hold or pass G0 with the confirmation measures scheduled, not performed | DQ-020 | Decided 2026-10-21: A, passed with conditions ([G0 record](../10-safety-case/gates/G0-2026-10-21.md)) |
| D-18 | The environmental limits of the laboratory envelope OE-1 | DQ-021 | Decided 2026-10-21: A |
| D-19 | Two-person rule for every powered test | DQ-022 | Decided 2026-10-21: A |
| D-20 | Write the fork's own safety layer for the motion control board before upstream's firmware is public | DQ-023 | Decided 2026-10-21: A, a minimal fork firmware for the hang tests |
| D-21 | Deliberate fall and power-cut tests on the kit robot | DQ-024 | Decided 2026-10-21: A, a bounded campaign |
| D-22 | Residual pinch and crush risk to the bench technician in OE-1 | DQ-025 | Decided 2026-10-21: A, accepted for OE-1 until G2 |
| D-23 | Spares budget and damage limit for the fall campaign | DQ-026 | Decided 2026-10-21: A, parts-based |
| D-24 | Buy a rated gantry crane or build a frame | DQ-027 | Decided 2026-10-21: A, buy |
| D-25 | ISO/TS 15066 contact limits as design targets | DQ-028 | Decided 2026-10-21: A, with a 0.75 factor on arm and hand values |
| D-26 | Recruit a second contributor as verification reviewer | DQ-029 | Decided 2026-10-21: A, public call open |
| D-27 | When G1 is held | DQ-030 | Decided 2026-10-21: A, after the first hang test |
| D-28 | Kit-assembly hazards in or out of the item | DQ-031 | Decided 2026-10-21: A, in |
| D-29 | Walking in the first item | DQ-032 | Decided 2026-10-21: A, not in the first item |
| D-30 | The UART debug port in the reference build | DQ-033 | Decided 2026-10-21: A, closed in the reference build |
| D-31 | A second IMU for SF-23 | DQ-034 | Decided 2026-10-21: A |
| D-32 | The bench equipment purchase | DQ-035 | Decided 2026-10-21: A, one purchase |
| D-33 | Certified safety relay or plain relays | DQ-036 | Decided 2026-10-21: A, certified module |
| D-34 | What feeds the actuator rail on the bench | DQ-037 | Decided 2026-10-21: A, a current-limited laboratory supply |
| D-35 | Tele-operation heartbeat timeout | DQ-038 | Decided 2026-10-21: A, 250 ms |
| D-36 | Lost wireless heartbeat: stop demand or warning in OE-1 | DQ-039 | Decided 2026-10-21: A, a warning |
| D-37 | Session recording and retention | DQ-040 | Decided 2026-10-21: A |
| D-38 | The tether's own hazards accepted with rigging checks | DQ-041 | Decided 2026-10-21: A, accepted for OE-1 |
| D-39 | Stator temperature cut-off and session readout | DQ-042 | Decided 2026-10-21: A, 60 °C |
| D-40 | Tether catch height | DQ-043 | Decided 2026-10-21: A, knee height |
| D-41 | Where the laboratory is | DQ-044 | Decided 2026-10-21: A, the lead's own premises |
| D-42 | Hours per week | DQ-045 | Decided 2026-10-21: A, about eight |
| D-43 | Where the reviewer call is posted | DQ-046 | Decided 2026-10-21: A, upstream's Discord and forum (draft in WP-M-10 §5) |
| D-44 | Ask upstream in public for reliability data and the E-stop design | DQ-047 | Decided 2026-10-21: A (draft in WP-M-10 §5) |
| D-45 | Re-arm after an E-stop: pendant only | DQ-048 | Decided 2026-10-21: A |
| D-46 | Laboratory joint velocity ceiling | DQ-049 | Decided 2026-10-21: A, 1.0 rad/s |
| D-47 | The policy as a black box or weights under agreement | DQ-050 | Decided 2026-10-21: A, black box |
| D-48 | Publishing anomalies, results and video | DQ-051 | Decided 2026-10-21: A, as they happen; video behind consent |
| D-49 | Who may be the observer | DQ-052 | Decided 2026-10-21: A, any briefed adult |
| D-50 | Liability insurance before powered tests | DQ-053 | Decided 2026-10-21: A, check first; cover before the first floor test |
| D-51 | When the second item starts | DQ-054 | Decided 2026-10-21: A, after G5 |
| D-52 | The recruited reviewer performing the G1 confirmation reviews at I1 | DQ-055 | Decided 2026-10-21: A, as a recorded deviation |
| D-53 | Which robot unit is the reference unit | DQ-056 | Decided 2026-10-21: C, none yet; the kit order is DQ-065 |
| D-54 | A dedicated isolated Wi-Fi network | DQ-057 | Decided 2026-10-21: B, the household network; residual risk DQ-067 |
| D-55 | Hold-to-run enabling switch on the pendant | DQ-058 | Decided 2026-10-21: A |
| D-56 | G1 target date | DQ-059 | Decided 2026-10-21: B, end of June 2027 |
| D-57 | Licence of the record | DQ-060 | Decided 2026-10-21: A, CC BY-SA 4.0; tools GPL-2.0 |
| D-58 | Visitors outside the cleared area | DQ-061 | Decided 2026-10-21: A, at most two behind a second line |
| D-59 | Who lifts a stop after an anomaly | DQ-062 | Decided 2026-10-21: B, the safety manager alone |
| D-60 | Firmware language | DQ-063 | Decided 2026-10-21: B, Rust |
| D-61 | Observing the actuator CAN protocol if undocumented | DQ-064 | Decided 2026-10-21: B, wait for documentation |
| D-62 | Order the kit when orderable | DQ-065 | Open, batch 7 |
| D-63 | Buy a CM5 for the firmware now | DQ-066 | Open, batch 7 |
| D-64 | Accept the shared-network exposure for OE-1 | DQ-067 | Open, batch 7 |
| D-65 | G1 on the record if no unit by the target | DQ-068 | Open, batch 7 |
| D-66 | Budget cap through G1 | DQ-069 | Open, batch 7 |
| D-67 | The lead as test operator of record | DQ-070 | Open, batch 7 |
| D-68 | ML-R1 at I1 by the recruited reviewer | DQ-071 | Open, batch 7 |
| D-69 | Dated copies of upstream manual pages | DQ-072 | Open, batch 7 |
| D-70 | Second IMU type (decider: claude) | DQ-073 | Open, batch 7 |
| D-71 | Rust coding rules | DQ-074 | Open, batch 7 |

## 9. Top risks to the assurance path

Project risks are managed in [WP-M-07](WP-M-07-risk-management.md). The ones that shape this strategy:

| Risk | Effect | Response |
|---|---|---|
| Upstream never publishes the firmware, the API or the policy | No software to assess; every software claim stays a defeater | DQ-003 option A keeps the case on what exists; the fork can specify and, if it must, implement the safety layer (DQ-003 C) |
| The lead cannot fund a gantry, a wired E-stop and certified components | No complementary measure for the fall; the risk graph stays at PL e | DQ-007 and DQ-008; without them no powered floor test runs |
| The learned policy is the only thing that keeps the robot up | A safety function on a component nobody can inspect; AI Act and Annex I Part A exposure | T-03 withdraws SF-01 unless DQ-006 allocates it; the gantry carries the fall meanwhile |
| One person holds every role | No I1 review, no confirmation measure, self-approval everywhere | T-09; DQ-010, DQ-011; verification reviews by any second contributor count |
| The standards are not available to the authors | Clause numbers wrong; tailoring argued against memory; the package's 2011 editions of ISO 10218 may be superseded | DQ-013, DQ-015; every clause reference marked to check; WP-M-06 OI-1 |
| No actuator reliability data ever arrives | The PL of every function that runs through an actuator cannot be computed | Derating and monitoring in the safety layer; the chain removes power upstream of the actuators; WP-M-10 asks upstream |

## 10. Open items

| ID | Item | Owner | Gate |
|---|---|---|---|
| OI-1 | Apply DQ-001…DQ-010 to this document and to WP-C-01…WP-C-04 when answered; rewrite T-03 and T-14 if DQ-006 or DQ-002 go against the recommendation | Safety manager | G1 |
| OI-2 | Replace the text diagram of §6.1 with a generated figure pinned to §6.1 and §6.2 so CI detects when it may be stale | Safety manager | G1 |
| OI-3 | Confirm the tailoring table with the assessor once engaged (DQ-010) | Safety manager | G1 |
| OI-4 | Obtain from upstream the firmware interface, the mode-machine specification and the E-stop design, or record their absence as the fork's own design input (GAP-07, GAP-16) | Project maintainer | G1 |
