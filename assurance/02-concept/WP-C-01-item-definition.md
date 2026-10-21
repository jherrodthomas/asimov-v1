# WP-C-01 Item Definition and Limits of the Machinery

| Field | Value |
|---|---|
| Work product | WP-C-01 Item definition and limits of the machinery |
| Standard reference | ISO 12100:2010 §5.3 (determination of the limits of the machinery), §5.4 (hazard identification inputs); ISO 10218-1:2011 §3, §5 (terms, robot requirements); ISO 13482:2014 §4 (robot types, use); ISO 13849-1:2023 §4.5; Regulation (EU) 2023/1230 Annex III §1.1.2, Annex IV Part A (technical documentation) |
| Version | 0.1 (2026-10-21): ported from the concept-package item definition (`03_ItemDef`) and re-stated against the repository at BL-001; two configurations CFG-001 and CFG-002; assumptions AOU-01…AOU-07; element and interface IDs |
| Status | Draft |
| PL / scope | PL d target for the stop and fall functions (DQ-004, open); operating envelope OE-1 only (DQ-002, open); CFG-001 the kit robot as published, tethered and bench-powered; CFG-002 the battery-powered robot under the locomotion policy, every value quoted from upstream and unverified |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1; someone who has built or operated the robot) |
| Approver | Project lead |
| Baseline | BL-001 (`baselines.yaml`): the fork at `3d4ec9d` |

> [!WARNING]
> Draft prepared for engineering review. Values marked **(unknown)** are not stated anywhere in the record and must
> be measured or decided before the risk assessment (WP-C-03) can be rated with confidence. Nothing here has been
> verified on a robot. Everything said about CFG-002 (§1.2, §2.3, §4.4) is quoted from upstream's README and roadmap;
> no repository holds the firmware, the API or the policy, so each row is a claim to verify when it does, never
> evidence (gap assessment §8).

## 1. Item identification

| Field | Value |
|---|---|
| Item | Asimov v1, an open-source bipedal humanoid robot: 1.2 m, 35 kg, 25 actuated degrees of freedom and two passive toes, on two configurations. **CFG-001**, the DIY-kit robot as published (§1.1): what a builder can make from the repository and the kit today, suspended from a gantry, powered from a bench supply, moved by tele-operation; the reference configuration of the first safety case. **CFG-002**, the battery-powered robot walking under the locomotion policy through the Asimov API (§1.2): what upstream intends to sell, decided but not public |
| Fork | `jherrodthomas/asimov-v1` from `asimovinc/asimov-v1` at BL-001 (upstream content as of `5de64d3`, 2026-04-30) |
| Product class | Machinery (a drive system and a function of its own); a robot under ISO 10218-1 when operated in an industrial envelope (OE-2); a personal care robot of Type 1 (mobile servant) under ISO 13482 only if the lead widens the item to OE-3 or OE-4 (DQ-002). The first item is a research machine in a laboratory (OE-1) and claims neither class |
| Upstream designation | "Asimov v1", DIY kit at a target price of 15,000 USD, shipping announced for summer 2026; the Asimov API, the locomotion policy and the mobile app marked as upcoming in the roadmap |
| Manufacturer of record | Asimov Inc (Menlo) for the design and the kit; whoever assembles the kit makes the machine (WP-M-13 §2). The fork assigns no manufacturer and places no product on the market |

### 1.1 Reference configuration CFG-001, the kit robot as published

| Element | Value | Source |
|---|---|---|
| Structure | 7075 aluminium machined parts, MJF PA12 nylon parts, SLM 316L stainless parts (arm zone), off-the-shelf fasteners and bearings; seven subassemblies ASV1_100 (pelvis) to ASV1_700 (head) | `mechanical/ASV1/*/FABRICATION/`; README specifications |
| Degrees of freedom | Legs 6 DOF × 2 plus a passive toe each; arms 5 DOF × 2 (shoulder pitch, roll, yaw, elbow, wrist yaw); waist yaw; neck yaw and pitch; 25 actuated, 2 passive | README specifications; `sim-model/xmls/asimov.xml` (25 motor elements) |
| Actuators | BLDC with harmonic gear and encoder, typical of 25; each on an XT30(2+2) connector carrying BATT+, BATT−, CAN_H, CAN_L; MuJoCo control ranges 36 to 145 N m per joint **(simulation values; declared limits unknown)** | `electrical/wiring/wiring.yaml`; `sim-model/xmls/asimov.xml` |
| Motion control board | Radxa CM5 carrier (MCB v0.1.4): 3 native CAN, 3 SPI-CAN, 3 USB 2.0, 1 Gbps Ethernet, 2 RS485, I2C; LSM6DSV 6-DOF IMU on the board; 5 V input on an XT30; UART TTL debug port; JST-GH signal connectors | `electrical/motion_control/board/`; `electrical/README.md` |
| CAN buses | C0 left leg, C1 right leg, C2 right arm, C3 left arm, C4 waist and neck (waist → neck yaw → neck pitch → C4), C5 BMS; 5 at 1 Mbps and 1 at 500 kbps | `electrical/README.md` port mapping; README specifications |
| Edge board | Raspberry Pi 5 (media and network), 2 MP monocular camera, quad microphone array, 10 W 4 Ω speaker; 4G/5G modules not included | README specifications and DIY-kit table |
| Power | 5 V to the motion control board; the actuator battery rail through the harness; a "power distribution board" listed in the kit but **not in the repository**; **no battery** (excluded from the kit); on CFG-001 a bench supply replaces it | README DIY-kit table; `electrical/README.md` |
| Emergency stop | A "wireless E-Stop" listed in the kit; **architecture, receiver, contactor and stop category unknown** (GAP-07); on CFG-001 the fork adds a wired E-stop in the operator's hand (DQ-008) | README DIY-kit table |
| Modes | DAMP (motors limp; the default on disconnect or E-stop release), STAND (controller holds a standing pose, ramps in about 2 s), MOVE (accepts position and velocity commands) | package `03_ItemDef`; README |
| Software | **None in any public repository** at BL-001: no firmware, no API, no policy, no app (GAP-16…GAP-18) | README roadmap |
| Fall protection (fork) | Overhead gantry and rated tether, quick-release; the robot's feet reach the floor only when the gantry is lowered (DQ-007) | WP-V-07 §2 |
| Operator interface | Tele-operation from an operator device over a WebRTC data channel (per the package); the kit's wireless E-stop transmitter | package `03_ItemDef` information boundaries |

### 1.2 Reference configuration CFG-002, the battery-powered robot under the policy (unverified)

| Element | Value (as announced upstream) | Source |
|---|---|---|
| Power | A user-supplied lithium pack with BMS on bus C5; charger not specified; runtime not specified | README DIY-kit table; package `03_ItemDef` time limits |
| Locomotion | A learned policy trained in MuJoCo for standing and walking; deployed through the Asimov API; hardware-in-the-loop setup described in the manual's locomotion guide | `sim-model/README.md`; README roadmap |
| Control interface | The Asimov API (pre-1.0) and a mobile app | README roadmap |
| Loads | Squat 5 kg, bicep curl 15 kg per arm, lateral raise 18 kg per arm | README specifications |
| Everything else | As CFG-001 | — |

## 2. Intended use and functions

### 2.1 Intended use (ISO 12100 §5.3.2)

- **Use:** an open-source humanoid platform for research, education and DIY assembly: bipedal locomotion (when the
  policy is released), upper-body reach without an end effector in v1, sensing (camera, microphones, IMU, joint
  states) streamed to an operator, audio output, tele-operation. Upstream addresses builders, researchers and
  robotics enthusiasts and offers the robot for deployment through a business contact.
- **Users:** builders (assemble and wire the kit), researchers and developers (train and deploy policies, use the
  API), operators (tele-operate, monitor, stop), bystanders (share the room). The kit buyer is the manufacturer of
  the unit they build (WP-M-13 §2).
- **Level of training:** none assumed by upstream beyond its manual, whose safety pages are not yet published; the
  fork assumes a trained operator present during every powered run (AOU-01).
- **Modes of use foreseen by the record:** bench test of actuators on a stand; the robot on the gantry with feet off
  the floor; the robot on the gantry with feet on the floor, tele-operated; standing under the policy (CFG-002);
  walking under the policy (CFG-002); demonstration to visitors (excluded in OE-1, WP-C-02).

### 2.2 Functions

| ID | Function | Implemented by | Notes |
|---|---|---|---|
| F-01 | Stand: maintain bipedal balance in STAND | Locomotion policy or balance controller on the CM5, IMU, 12 leg actuators | **The controller is not public.** Whether it may carry a safety function is DQ-006 |
| F-02 | Walk: forward, backward and turning locomotion in MOVE | Locomotion policy (CFG-002 only) | Unreleased |
| F-03 | Manipulate: upper-body reach with the two 5-DOF arms; no end effector in v1 | Position and velocity commands to 10 arm actuators | Loads per §1.2 on CFG-002 |
| F-04 | Sense: camera, quad microphones, IMU, joint encoders, streamed to the operator | Edge board, motion control board | Monocular camera: no range to a person |
| F-05 | Speak: audio output through the 10 W speaker | Edge board | A limiter is a safety function (SF-16) |
| F-06 | Accept tele-operation commands and mode changes from the operator | Edge board over WebRTC → motion control board | Authentication unknown (GAP-19) |
| F-07 | Enter DAMP on disconnect or E-stop release; ramp into STAND; accept MOVE | Mode machine on the CM5 (unreleased) | DAMP drops the robot (GAP-10) |
| F-08 | Remove motor power on an E-stop press | Wireless E-stop (architecture unknown); on CFG-001 the wired pendant | GAP-07 |
| F-09 | Distribute power to 25 actuators over six CAN harness branches | Power distribution board (not in the repository), harness | GAP-08 |
| F-10 | Run and deploy a locomotion policy from the MuJoCo model (CFG-002) | Training stack, Asimov API | A learned component (WP-C-09) |

### 2.3 Functions the item does not provide (and the record says so)

A documented emergency-stop chain, a fall-arrest or controlled-descent function, declared joint torque and velocity
limits, a BMS interlock, authenticated tele-operation, a disconnection device, any verification record. See the gap
assessment. On CFG-002 the policy, the API and the battery are announced but nothing names their safety behaviour.

## 3. Item boundary

### 3.1 Inside the item

| Element | Name and content | Role |
|---|---|---|
| E-01 | Structure: 7075 machined parts, PA12 parts, 316L parts, fasteners, bearings; the hip yoke as the highest-stress part | mechanical |
| E-02 | Actuators: 25 BLDC with harmonic gear and encoder, on six CAN buses | the last electrical stage before motion |
| E-03 | Motion control board: Radxa CM5 carrier with IMU, CAN transceivers, UART debug port | the only thing between a command and the actuators |
| E-04 | Edge board: Raspberry Pi 5 with camera, microphones, speaker, Wi-Fi and Ethernet | tele-operation endpoint, media |
| E-05 | Harness: XT30(2+2) power and CAN to every actuator, JST-GH signals, Molex KK to the BMS stub | power and signal distribution |
| E-06 | Power distribution board (not in the repository) and the 5 V XT30 input | motor rail and logic supply |
| E-07 | Wireless E-stop receiver (architecture unknown) | stop device |
| E-08 | Battery and BMS (user-supplied; absent on CFG-001) | energy store |
| E-09 | Fork bench equipment on CFG-001: gantry, tether, wired E-stop pendant, bench supply | complementary measures |

### 3.2 Outside the item

The operator and their device, the Wi-Fi or cellular network, the charger, the laboratory floor and furniture,
visitors, the MuJoCo training environment, the kit supplier's logistics.

### 3.3 Interfaces

| ID | Interface | Between | Notes |
|---|---|---|---|
| IF-01 | Tele-operation data channel (WebRTC) | operator device ↔ E-04 | authentication unknown |
| IF-02 | Edge to motion control (Ethernet or USB) | E-04 ↔ E-03 | protocol unknown |
| IF-03 | Six CAN buses C0…C5 | E-03 ↔ E-02, E-08 | 5 × 1 Mbps, 1 × 500 kbps |
| IF-04 | Motor rail and 5 V supply | E-06 → E-02, E-03 | protection unknown |
| IF-05 | E-stop link (wireless) and the wired pendant (CFG-001) | transmitter ↔ E-07 → E-06 | surveillance unknown |
| IF-06 | UART TTL debug port | E-03 ↔ a technician's laptop | open by design |
| IF-07 | Tether and gantry (CFG-001) | E-01 ↔ the laboratory structure | rated for a 35 kg dynamic load |
| IF-08 | Charger (CFG-002) | mains ↔ E-08 | not specified |

## 4. Limits of the machinery (ISO 12100 §5.3)

### 4.1 Use limits

| Limit | Value | Source and status |
|---|---|---|
| Mass | 35 kg (upstream figure) **(to be weighed)** | README; GAP-03 |
| Height | 1.2 m standing; overhead reach to about 2.0 m | README; package `03_ItemDef` |
| Footprint and reach | about 0.4 m × 0.3 m standing; reach envelope about 1.5 m diameter centred on the torso | package `03_ItemDef` |
| Joint torque | MuJoCo control ranges 36 to 145 N m per joint **(simulation values; declared limits unknown, DQ-014)** | `sim-model/xmls/asimov.xml`; GAP-06 |
| Joint velocity | **(unknown)** | GAP-06 |
| Payload (CFG-002) | squat 5 kg, bicep curl 15 kg per arm, lateral raise 18 kg per arm (upstream) | README |
| Speed of locomotion | **(unknown)**; demonstration speed only in OE-1 | package `05_OpEnv` |
| Fall energy | about 411 J at the centre of mass for a 35 kg body from 1.2 m (package estimate) **(to be bounded by WP-H-08)** | package `06_Hazards` HZ-M01 |
| Operators | one trained operator, at most one observer, in OE-1 | WP-C-02 |

### 4.2 Space limits

Operating envelope OE-1 of WP-C-02: a laboratory with a level, dry floor; a cleared and marked area at least the
reach envelope plus 1 m on every side; the gantry span as the walking range; nobody within reach of a limb while
powered.

### 4.3 Time limits

Runtime bounded by the bench supply on CFG-001; by an unspecified battery on CFG-002. Service life, maintenance
intervals and the fatigue life of the hip yoke **(unknown)** (GAP-04). Ambient +10 to +35 °C, below 80 % RH,
non-condensing (package assumptions; WP-C-02 §4).

### 4.4 Limits of CFG-002 (quoted, unverified)

Battery-powered walking under the locomotion policy at a speed the policy sets, carrying the loads of §1.2, through
the Asimov API, with the kit's wireless E-stop as the only stop device. None of it is in the first item.

## 5. Operating modes and states

| Mode | Behaviour | Entered | Safety relevance |
|---|---|---|---|
| M0 Off | No power on the motor rail | power off, E-stop pressed | the robot is a dead weight on the tether |
| M1 DAMP | Motors limp; the declared safe default | disconnect, E-stop release, fault | **a fall unless the tether holds** (GAP-10, DQ-005) |
| M2 STAND | The controller holds a standing pose, ramping in over about 2 s | operator command from DAMP | balance rests on the controller (DQ-006) |
| M3 MOVE | Position and velocity commands accepted | operator command from STAND | every limb hazard of WP-C-03 |
| M4 Bench | Actuators on a stand or the robot with feet off the floor | technician | the only powered mode permitted without the gantry lowered (WP-V-07) |

## 6. Legal requirements and standards

Per [WP-M-13](../01-management/WP-M-13-regulatory-conformity-strategy.md) (frame pending DQ-001) and
[WP-M-01 §4](../01-management/WP-M-01-assurance-strategy.md#4-the-standards-and-how-each-one-is-used).

## 7. Known hazards and experience from similar items

Humanoid research platforms of this size fall; falls are the dominant hazard in every published humanoid safety
discussion, and the industry practice is a gantry during development. The package's hazard catalogue (32 rows from
ISO 12100 Annex B and ISO 13482 Annex A) is carried into WP-C-03. No field history exists for Asimov v1.

## 8. Assumptions of use and external measures

| ID | Assumption | Status at BL-001 |
|---|---|---|
| AOU-01 | A trained operator is present and within E-stop reach at all times in MOVE | Procedural only |
| AOU-02 | The battery, when fitted, is a UN 38.3 and IEC 62133-2 compliant lithium pack with an integrated BMS | Not enforced (DQ-009) |
| AOU-03 | The structure is genuine 7075-T6 aluminium and MJF PA12; no substitution during the DIY build | Not enforced |
| AOU-04 | The CAN harness is built per the WireViz record with correct termination and crimps | Not enforced |
| AOU-05 | The operating surface is level (slope at most 5°), dry and free of obstacles | Assumed |
| AOU-06 | No human body part enters the swept volume of any actuated joint while in STAND or MOVE | Procedural only |
| AOU-07 | The robot is not a medical device, a child-care robot or a load-bearing person carrier | Project scope |

Machine-readable copy: [`trace/items/aou.yaml`](../trace/items/aou.yaml).

## 9. Out of scope for this item

OE-2, OE-3 and OE-4 (DQ-002); any battery-powered or policy-driven operation (CFG-002); collaborative tasks;
carrying a person; outdoor use; medical or child-care use.

## 10. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Weigh the robot, measure the centre of gravity, bound the fall energy (ACT-001) | EM | G1 |
| OI-2 | Set the battery policy (DQ-009) and record the resulting limit here (ACT-008) | PM | G1 |
| OI-3 | Obtain from upstream the declared joint torque and velocity limits, or set them (DQ-014) | SRP | G1 |
| OI-4 | Apply DQ-002 and DQ-003 to §1 and §9 when answered | SM | G1 |
