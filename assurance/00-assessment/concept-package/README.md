# Concept-phase engineering package

The package the fork published before the assurance record existed, kept here as inherited (a baseline input, see
[the gap assessment](../gap-assessment.md) §2 and BL-001 in
[`case/baselines/baselines.yaml`](../../case/baselines/baselines.yaml)). None of it is produced or endorsed by the
upstream maintainers (`asimovinc/asimov-v1`); it is a fork-level analysis derived from the published CAD, electrical
schematics, MuJoCo model and manual. It is AI-assisted and unreviewed (GAP-33), and its files are **not edited**: the
record supersedes them work product by work product and this note says how.

## Contents

| File | What it holds | Where the record takes it |
|---|---|---|
| `Asimov_v1_Safety_Case.xlsx` | 15 tabs: item definition, standards matrix, the four operating envelopes, 32 hazards, HARA, FMEA, functional safety concept with 25 safety functions, GSN, evidence register, 28 gaps, assumptions A-01…A-07 and open items OI-01…OI-05 | [WP-C-01](../../02-concept/WP-C-01-item-definition.md), [WP-C-02](../../02-concept/WP-C-02-operating-environment-and-tasks.md), [WP-C-03](../../02-concept/WP-C-03-risk-assessment.md), [WP-C-04](../../02-concept/WP-C-04-safety-functions-and-plr.md), [WP-K-01](../../10-safety-case/WP-K-01-safety-case.md) and the [case records](../../case/README.md); the gaps become GAP-01…GAP-28 of the gap assessment and defeaters DF-01…DF-28 |
| `Asimov_v1_Safety_Case_Report.docx`, `Asimov_v1_Safety_Case_Summary.pdf` | Narrative safety case and its two-page summary | WP-K-01 (the argument), WP-M-01 (the strategy) |
| `Asimov_v1_DFMEA.xlsx` | AIAG-VDA DFMEA: 32 failure modes, 19 at high action priority | Seeds [WP-H-03](../../04-hardware/WP-H-03-hardware-failure-analysis.md) and [WP-A-01](../../08-analyses/WP-A-01-system-fmea.md); the failure modes are quoted there, not re-derived |
| `Asimov_v1_Requirements.xlsx` | 120 requirements (35 system, 45 software, 40 hardware; 63 safety, 9 cybersecurity) with trace | To be ported into [WP-S-01](../../03-system/WP-S-01-system-requirements.md), [WP-S-02](../../03-system/WP-S-02-safety-requirements.md), [WP-W-02](../../05-software/WP-W-02-software-safety-requirements.md) and [WP-H-01](../../04-hardware/WP-H-01-hardware-safety-requirements.md) (WP-K-01 OI-7) |
| `Asimov_v1_TestPlan.xlsx` | 139 test cases (83 unit, 24 integration, 32 system); ISO 13849-2 validation matrix; ISO 13482 §7 matrix | To be ported into [WP-V-01](../../06-validation/WP-V-01-safety-validation.md) and the verification work products (WP-K-01 OI-7) |
| `Asimov_v1_Architecture.docx`, `01_system_boundary.png` … `05_state_machine.png` | Five architecture views: system boundary, functional blocks with six CAN buses, safety-function allocation, CAN topology C0…C5, the DAMP/STAND/MOVE mode machine | [WP-C-01 §5](../../02-concept/WP-C-01-item-definition.md) (modes), [WP-S-03](../../03-system/WP-S-03-technical-safety-concept.md), [WP-S-05](../../03-system/WP-S-05-safety-chain-io-interface.md) |
| `Asimov_v1_Trace_Memo.docx` | Cross-package traceability memo | [WP-T-01](../../trace/README.md) |
| `Asimov_v1_Engineering_Bundle.pdf` | Single-file bundle of the above | reference only |
| `01_hero_banner.png`, `02_kpi_infographic.png`, `03_op_envelope.png` | The fork README's former illustrations | replaced by the generated figures under [`docs/assets/asimov/`](../../../docs/assets/asimov/) |

## What the record keeps, changes and drops

- **Kept:** the 32 hazards in the package's order (its `HZ-nn` identifiers stay as `package_id` in
  [`trace/items/hazards.yaml`](../../trace/items/hazards.yaml)); the 25 safety functions with their numbering and
  the package's PLr proposals; the four operating envelopes; the seven assumptions as AOU-01…AOU-07; the 28 gaps.
- **Changed:** the gap severities are re-expressed on the record's three-level scale (the package's Very High and
  High both become High); the package's "provisional YES" for OE-1 becomes a proposal for the lead (DQ-002) with
  the conditions of [WP-V-07](../../06-validation/WP-V-07-test-operations.md), not an acceptance; every PLr is
  pending DQ-004 and the re-rating of WP-C-03.
- **Added:** six gaps the package did not raise (GAP-04 structural evidence, GAP-10 the undefined safe state,
  GAP-13 the allocation of balance to the policy, GAP-20 the unprotected E-stop link and debug port, GAP-21 the
  unpinned simulation model, GAP-33 the package's own review status); the tether and gantry as an explicit claim
  (G2.4).
- **Dropped:** the package's acceptance language and its dashboard; the record's dashboard is generated from the
  case records.

## Licensing

Upstream hardware is CERN-OHL-S-2.0 and upstream software GPL-2.0. The package was published under those licences
and stays so; the record that supersedes it is under CC BY-SA 4.0 ([LICENSE-RECORD.md](../../../LICENSE-RECORD.md), DQ-060 A).
