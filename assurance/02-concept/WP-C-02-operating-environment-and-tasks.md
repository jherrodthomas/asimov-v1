# WP-C-02 Operating environment and task specification

| Field | Value |
|---|---|
| Work product | WP-C-02 Operating environment and task specification (operating envelopes OE-1…OE-4, floors, people, tether) |
| Standard reference | Machinery: 12100 §5.3; 13482 §5.2; 10218-2 §5; Other: ISO 21448 §5 (informative method); ASPICE: SYS.1 |
| Version | 0.4 (2026-10-21): DQ-027 A (gantry crane) and DQ-032 A (no walking in the first item) applied to §3 and §6. 0.3 (2026-10-21): DQ-021 A (OE-1 environmental limits adopted), DQ-014 A (joint limits) and DQ-022 A (two-person rule) applied to §3 and §4. 0.2 (2026-10-21): DQ-002 A applied (OE-1 the only envelope of the first item, OE-2 a second item); DQ-007 A (gantry and tether) and DQ-009 A (no battery on CFG-001) recorded. 0.1 (2026-10-21): the four operating envelopes of the concept package (`05_OpEnv`) as zones, with people presence, fall protection, speed limits and status; tasks T-01…T-08; environmental limits; exclusions; the development test area |
| Status | Draft |
| PL / scope | PL d target (DQ-004 A); OE-1 only in the first item (DQ-002 A, decided 2026-10-21); CFG-001 (DQ-003 A) |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1; someone who has run a humanoid on a gantry) |
| Approver | Safety manager |
| Baseline | BL-001 |

> [!WARNING]
> Draft. Upstream publishes no operating-environment specification; the manual's safety page is not published.
> Every numeric limit below marked **(TBC)** is a proposal for the lead or a value the tests of WP-V-02 and WP-V-03
> must set. Nothing here has been walked with the robot.

## 1. Purpose

Specifies the operating environment and the tasks the robot performs in it: operating envelopes, floors, people
presence, fall protection, speed limits. It is the machinery analogue of an operational design domain and the source
of every operating-environment limit the safety case relies on. The risk assessment
([WP-C-03](WP-C-03-risk-assessment.md)) rates its hazards per envelope; the information for use
([WP-O-03](../09-production-operation/WP-O-03-information-for-use.md)) carries the exclusions of §5 to the operator;
the test procedure ([WP-V-07](../06-validation/WP-V-07-test-operations.md)) uses the test area of §6 as its
condition C-4.

People presence per operating envelope is an input to the misuse analysis of WP-C-06.

## 2. Operating envelopes

An operating envelope is a place and a set of people with one set of environmental properties, one people-presence
class, one fall-protection rule and one speed limit. People-presence classes: **none** (nobody within reach of a
limb while powered), **briefed** (trained staff who know the robot, its stop devices and its modes), **public**
(anyone, including children and pets).

| Envelope | Name | Floor and slope | Fall protection | People | E-stop | Power | Speed limit | Robot class | Status at BL-001 |
|---|---|---|---|---|---|---|---|---|---|
| OE-0 | Excluded | anything in §5 | | | | | 0 | | the robot must not be powered there |
| OE-1 | Laboratory, supervised, tethered (§6) | level, dry, sealed floor; slope ≤ 1 % **(TBC)**; no threshold | overhead gantry and rated tether; feet on the floor only with the gantry lowered (DQ-007) | none within reach; one trained operator with the wired E-stop and at most one observer, both outside the reach envelope | wired pendant in the operator's hand plus the kit's wireless device (DQ-008) | bench supply, no battery | demonstration speed: joint velocity and torque per WP-W-09; half the simulation control range per joint and a velocity ceiling from WP-S-04 until measured (DQ-014 A, decided 2026-10-21) | none claimed (research machine) | **the only envelope in the first item** (DQ-002 A); permitted under WP-V-07 once the gantry (DQ-007 A) and the wired pendant (DQ-008 A) exist |
| OE-2 | Industrial collaborative cell | level, dry; defined cell with marked boundary | none (free-standing) | briefed workers in a permitted area; collaborative contact only under SF-04 and SF-20 | wireless with surveillance, plus a cell E-stop | battery with BMS interlock, dock | ISO/TS 15066 quasi-static and transient limits at the contact points | industrial robot system (ISO 10218-2) | **not permitted**: the second item (DQ-002 A), once the firmware and the policy are public; 12 package gaps to close; no fall-arrest function, no PFL measurement, no Category 3 chain |
| OE-3 | Home, untrained users | domestic floors, mixed surfaces, stairs | none | public, including children and pets | possibly absent | user-supplied battery | not declared | personal care robot Type 1 (ISO 13482) | **excluded**: 19 package gaps; ISO 13482 §7 verification, environmental robustness, policy verification |
| OE-4 | Public space, free roaming | outdoor, weather, kerbs | none | public, including elderly and disabled | not guaranteed | battery, dock | not declared | personal care robot Type 1 | **excluded** at any near-term revision: 21 gaps plus regulatory engagement |

The package's provisional acceptance of OE-1 became the scope of the first item on 2026-10-21 (DQ-002 A); OE-2 is
a second item once the firmware and the policy are public. The package's gap counts for OE-2 to OE-4 are the
defeaters DF-01…DF-34 of the safety case, not a second analysis.

## 3. Tasks

| Task | What the robot does | Envelope | Mode (WP-C-01 §5) | People during the task | Protective measure needed | Status at BL-001 |
|---|---|---|---|---|---|---|
| T-01 | Actuator bench: single actuators or a limb on a stand; may be run alone (DQ-022 A) | bench (not an envelope) | M4 | technician | fixed stand, current limit, wired E-stop | permitted; the only powered activity without the gantry |
| T-02 | Hang test: the robot on the gantry with feet off the floor, joints moved by tele-operation; two people (DQ-022 A) | OE-1 | M4 | operator, observer | gantry carrying the whole mass; SF-03 clamps; E-stop | permitted under WP-V-07 once the gantry exists |
| T-03 | Stand on the tether: feet on the floor, gantry lowered to take a fall, STAND under the controller | OE-1 | M2 | operator, observer | gantry and tether; E-stop; the controller's limits | **not permitted** until a controller exists and WP-V-07 conditions hold |
| T-04 | Move on the tether: tele-operated limb and torso motion in MOVE, feet on the floor | OE-1 | M3 | operator, observer | as T-03 plus SF-03, SF-23, SF-24 | not permitted until the safety layer exists |
| T-05 | Walk on the tether (CFG-002): locomotion under the policy within the gantry span | OE-1 | M3 | operator, observer | as T-04 plus the policy as a functional component (DQ-006 A) | **not in the first item** (DQ-032 A, decided 2026-10-21): standing, stepping in place and limb motion only; walking returns with the policy in the second item |
| T-06 | Controlled descent and fall tests: deliberate loss of balance, power cut, DAMP, caught by the tether or descending under SF-02 | OE-1 | M1…M3 | operator, observer | gantry sized for the dynamic load; nobody within the fall radius | the first test campaign of WP-V-02 |
| T-07 | Demonstration to visitors | OE-1 | any | public | none exists | **excluded** (people within reach, DQ-002) |
| T-08 | Collaborative task with a worker (CFG-002) | OE-2 | M3 | briefed | SF-04, SF-20, SF-06 measured | **excluded** from the first item |

## 4. Environmental limits

| Limit | Value | Basis | Consequence of exceeding |
|---|---|---|---|
| Ambient temperature | +10 to +35 °C (DQ-021 A) | package assumption; the Raspberry Pi 5 in the head shell has no thermal validation (GAP-25) | compute throttling or shutdown → comms loss → DAMP |
| Humidity | non-condensing, ≤ 80 % RH (DQ-021 A) | package assumption; no IP rating | electrical fault (H-09, H-20) |
| Dust, water | dry indoor only; no spills on the floor | no IP rating (SF-19) | slip, short circuit |
| Floor | level, slope ≤ 1 % in OE-1 (DQ-021 A), ≤ 5° anywhere (AOU-05); sealed, dry (DQ-021 A); friction μ ≥ 0.5 **(TBC)** | the policy is trained on a simulated floor whose friction is a randomisation parameter (GAP-21) | loss of balance (H-06) |
| Steps, thresholds, drops | none in OE-1 (DQ-021 A) | no perception of steps; the tether limits the fall | fall |
| Lighting | ≥ 200 lx (DQ-021 A) | the operator's camera view; the monocular camera cannot range a person | blind tele-operation (DFMEA FM-23) |
| Electromagnetic environment | laboratory per EN 61000-6-1 **(assumed, not tested)** | the wireless E-stop and the WebRTC link are radio links (H-11) | link loss → DAMP; E-stop ineffective |
| Wi-Fi coverage | continuous over the gantry span | loss of the heartbeat is a DAMP (SF-08) | a fall onto the tether |
| Overhead clearance | gantry height ≥ robot height plus tether travel **(TBC)** | DQ-007 | the robot reaches the floor in a fall |

## 5. What is outside the environment

Each exclusion becomes an operating limit in WP-O-03 §3 and a marking where it applies.

| Exclusion | Why |
|---|---|
| Any person within the reach envelope of a powered limb | No contact limit is measured (GAP-05); no fall-arrest function exists (GAP-10) |
| Free-standing operation without the tether | The fall of a 35 kg body is the dominant hazard and nothing arrests it (DQ-007) |
| A battery on the robot | No compliance gate, no BMS interlock (GAP-12, DQ-009) |
| Children, pets, visitors | Public presence belongs to OE-3 and OE-4 |
| Stairs, slopes above 1 %, thresholds, wet or soft floors | The controller is trained for a level simulated floor; no perception of the floor |
| Outdoors, rain, dust | No IP rating |
| Carrying a person, medical or child-care use | AOU-07 |
| Operation while a manual safety page is unpublished | GAP-02: the operator has nothing to be briefed from beyond this record |

## 6. The development test area (OE-1)

A marked rectangle at least the reach envelope (1.5 m diameter) plus 1 m on every side, under a rated portable
gantry crane with a trolley (DQ-027 A); since walking is not in the first item (DQ-032 A) the gantry needs no walking
span, only room to lower the robot to the floor; a level, dry, sealed floor; the operator's station outside the
rectangle with the wired E-stop and the bench supply switch within reach; the observer outside the rectangle on the
other side; nothing inside but the robot, its tether and test props; the camera view and the telemetry visible to the
operator. Sketch and dimensions to be recorded under [`06-validation/test-sites/`](../06-validation/test-sites/README.md)
before the first powered floor test (WP-V-07 condition C-4).

## 7. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Set the remaining **(TBC)** values (floor friction, overhead clearance) from the tests of WP-V-02; the environmental limits were adopted 2026-10-21 (DQ-021 A) | SM | G1 |
| OI-2 | Define and sketch the test area and the gantry once DQ-007 is answered | test bench owner | G1 |
| OI-3 | ~~Apply DQ-002 to §2 when answered~~ applied 2026-10-21 (A) | SM | G1 |
