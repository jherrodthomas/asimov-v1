# Asimov v1 — Concept-Phase Engineering Package (fork additions)

This folder contains an independent **concept-phase engineering package** added in this fork
(`jherrodthomas/asimov-v1`) by J. Herrod-Thomas. None of these documents are produced or
endorsed by the upstream maintainers (`asimovinc/asimov-v1`); they are a fork-level safety
analysis derived from the publicly published CAD, electrical schematics, MuJoCo simulation
model, and manual.

> **Important.** This is a **preliminary** safety case. The upstream release publishes
> mechanical CAD, electrical schematics, and a MuJoCo model only — no HARA, FMEA, FMEDA,
> controller code, E-Stop validation, or BMS specification is published. The argument
> structure here is a *scaffold* populated with concept-level evidence; every leaf claim
> links to the Gap Register in the safety-case workbook. **Provisional acceptance applies
> only to OE-1 (research lab, supervised, tethered).** Deployment beyond that requires
> closure of the high-severity gaps tracked in `safety-case/`.

---

## Standards framework

The analysis applies five primary standards plus three referenced:

| Standard | Coverage |
|---|---|
| ISO 12100:2010                  | Master risk-assessment method |
| ISO 10218-1/-2:2011 + ISO/TS 15066 | Industrial-robot envelope; collaborative-robot PFL |
| ISO 13849-1:2023 / -2:2012      | Safety-related parts of control systems — PL determination & validation |
| ISO 13482:2014                  | Personal-care robot — Type 1 mobile servant hazard catalogue |
| ISO 9001:2015                   | Quality management — design control, NCR, CAR |
| IEC 60204-1:2018 (ref.)         | Electrical equipment of machines |
| IEC 62133-2:2017 (ref.)         | Li-ion battery safety |
| ISO/IEC/IEEE 29148:2018         | Requirements engineering |
| ISO/IEC/IEEE 42010:2022         | Architecture description |

---

## Contents

| Folder / file | Purpose |
|---|---|
| `safety-case/Asimov_v1_Safety_Case.xlsx`         | 15-tab safety-case workbook — item def, hazard catalogue (32), HARA, FMEA, FSC (25 SFs), GSN argument, evidence + gap registers (28 gaps) |
| `safety-case/Asimov_v1_Safety_Case_Report.docx`  | Narrative safety case (9 sections) |
| `safety-case/Asimov_v1_Safety_Case_Summary.pdf`  | 2-page executive summary |
| `dfmea/Asimov_v1_DFMEA.xlsx`                     | AIAG-VDA 2019 DFMEA — 12 tabs, 32 failure modes (19 H · 11 M · 2 L) |
| `requirements/Asimov_v1_Requirements.xlsx`       | SyRS + SRS + HwRS — 9 tabs, 120 requirements (63 safety, 9 cyber), bidirectional trace |
| `architecture/Asimov_v1_Architecture.docx`       | Five architectural views with embedded SVG diagrams |
| `architecture/diagrams/01_system_boundary.svg`   | System boundary / context (ISO 12100 §5 / ISO 13482 §5) |
| `architecture/diagrams/02_functional_block.svg`  | Functional block diagram with six CAN buses |
| `architecture/diagrams/03_sf_allocation.svg`     | Safety-function allocation map (HW / SW / procedure × PL) |
| `architecture/diagrams/04_can_topology.svg`      | CAN bus topology (C0..C5) with termination strategy |
| `architecture/diagrams/05_state_machine.svg`     | Mode FSM (DAMP / STAND / MOVE) with watchdog gating |
| `test-plan/Asimov_v1_TestPlan.xlsx`              | V-model test plan — 10 tabs, 139 test cases (Unit 83 · Integration 24 · System 32), ISO 13849-2 validation matrix, ISO 13482 §7 V&V matrix |
| `verification/Asimov_v1_Trace_Memo.docx`         | Cross-package traceability verification memo |
| `Asimov_v1_Engineering_Bundle.pdf`               | Single-file stakeholder bundle (architecture + reqs + DFMEA + tests + gaps) |

PNG renders of each SVG diagram are alongside in `architecture/diagrams/` for easy preview on GitHub.

---

## Headline numbers

| Item | Count |
|---|---|
| Hazards catalogued                | 32 |
| Safety functions (FSC)            | 25 |
| Standards-clauses examined        | 30 |
| Open gaps                         | 28 (10 Very-High · 9 High · 7 Med · 2 Low) |
| Requirements (SyRS + SRS + HwRS)  | 120 |
| DFMEA failure modes               | 32 (19 High-AP) |
| Test cases                        | 139 |

---

## Reading order

If you have 5 minutes — read **`safety-case/Asimov_v1_Safety_Case_Summary.pdf`**.

If you have 30 minutes — read the **Engineering Bundle PDF** at the root of this folder.

If you're the integrator deciding whether to deploy:
1. `safety-case/Asimov_v1_Safety_Case_Report.docx` (sections 7 and 9 in particular)
2. `safety-case/Asimov_v1_Safety_Case.xlsx` tabs `12_Gaps` and `15_Dashboard`
3. `dfmea/Asimov_v1_DFMEA.xlsx` Action Plan Tracker tab
4. `test-plan/Asimov_v1_TestPlan.xlsx` ISO 13849-2 Validation Matrix tab

---

## Provisional deployment guidance

| Operating envelope | Acceptance | Reason |
|---|---|---|
| **OE-1** Lab, supervised, tethered            | **Provisional YES**           | Trained operator, no bystanders, low hazard profile |
| **OE-2** Industrial cobot, defined cell       | Not yet — **12 gaps** to close | Requires E-Stop architecture, PFL data, Cat 3 redundancy, MTTFD/DC/CCF figures |
| **OE-3** Home / consumer, untrained users     | Not yet — **19 gaps** to close | Adds ISO 13482 personal-care V&V, environmental robustness, locomotion-policy verification |
| **OE-4** Public space, free roaming           | **Not** at any near-term rev   | 21 gaps + regulatory engagement (CE, FCC, national robotics frameworks) |

---

## Licensing

Upstream hardware is **CERN-OHL-S-2.0** (strongly reciprocal); upstream software is
**GPL-2.0**. The documents in this folder are derivative analytical works of the
upstream specs; they are released under the same licences and follow the reciprocity
obligations.

---

## Author and contact

J. Herrod-Thomas — fork maintainer / independent assessor.
Issues, comments, or corrections are welcome via the GitHub Issues tab on this fork.
