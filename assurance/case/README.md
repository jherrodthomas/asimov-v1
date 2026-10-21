# Living Safety Case records

| Field | Value |
|---|---|
| Work product | Living Safety Case data (machine-readable copy of [WP-K-01](../10-safety-case/WP-K-01-safety-case.md)), validator and dashboard generator |
| Standard reference | ISO 13849-1:2023 §10; Regulation (EU) 2023/1230 Annex IV; UL 4600 principles (living safety case, defeaters) |
| Version | 0.1 (2026-10-21): records, validator, dashboard generator, schema and tests; records at BL-001 from the concept-package GSN, evidence and gap registers |
| Status | Draft |
| Author | Assurance team |
| Reviewer(s) | TBD (I1) |
| Baseline | BL-001 |

## Record format and rules

Every record is a YAML file holding a list of flat mappings: one `- id:` entry per record, scalar values (quoted
strings, integers, `true`, `false`, `null`) or a flow list in brackets, no nested mappings, anchors, block scalars
or multi-document streams. The parser is [`tools/subsetyaml.py`](tools/subsetyaml.py), standard library only, so the
result never depends on what is installed. [`schema/case-schema.json`](schema/case-schema.json) names the fields,
identifier patterns and enumerations per kind.

The validator ([`tools/validate.py`](tools/validate.py)) applies:

| Rule | Checks |
|---|---|
| V1 | records parse, sit in the directory of their kind, carry every schema field and no others |
| V2 | identifiers match their pattern and are unique; field types and enumerations are valid |
| V3 | every reference resolves to a record, or to a trace item in [`../trace/items/`](../trace/items/), of the right kind |
| V4 | links are consistent in both directions (claim and evidence, claim and defeater, claim and argument) |
| V5 | every evidence location exists in the repository |
| V6 | acceptance: an accepted object needs an accepted review record that lists it; an accepted claim needs available, accepted evidence, accepted sub-claims and no open defeater; an assurance-supported configuration needs an accepted claim |
| V8 | the claims form one tree under a single top-level claim |
| X3 | the evidence, defeater and open-item tables of WP-K-01 match the records |

**Acceptance rule:** a claim counts as accepted only when a recorded review accepts it, every piece of evidence it
cites is available and accepted, and no defeater against it is open. A passing CI run never accepts a claim on its
own: it only confirms that the records say what the dashboard shows.

## Contents at BL-001

| Folder / file | Content at BL-001 |
|---|---|
| `claims/claims.yaml` | 29 claims: G0 and G1–G4 with sub-claims per safety function with a PLr (G1.1…G1.15), per complementary measure including the tether and gantry (G2.1…G2.4), the command path (G3.1) and the process (G4.1…G4.4) |
| `arguments/strategies.yaml` | 5 strategies |
| `evidence/evidence.yaml` | 22 evidence items (15 partial, 7 missing); the partial ones are the concept-package workbooks, the drafted work products and the upstream CAD, electrical and simulation sources |
| `defeaters/defeaters.yaml` | 34 open defeaters, one per gap-assessment finding (DF-nn is GAP-nn) |
| `actions/actions.yaml` | 10 open items of WP-K-01 §10 |
| `configurations/` | CFG-001, the kit robot tethered and bench-powered, classification `fork-evaluated`; CFG-002, the battery and policy robot, classification `upstream-compatible` |
| `baselines/baselines.yaml` | BL-001: fork `3d4ec9d` (upstream `5de64d3` plus the concept-phase package) |
| `reviews/reviews.yaml` | none |
| `schema/case-schema.json` | fields, identifier patterns and enumerations per kind; trace prefixes `H`, `HE`, `SF` (hazard log), `AOU` (assumptions), `SR`, `SF`, … (requirements) and the classifications |
| `tools/` | `validate.py`, `caselib.py`, `generate_dashboard.py`, `test_case.py`, `subsetyaml.py` (the YAML-subset parser shared with the trace data); a GSN diagram generator and a snapshot builder are still to come |

Trace items the validator resolves against live in [`../trace/items/`](../trace/items/): `hazards.yaml`
(H-01…H-32 from WP-C-03, with the package's HZ identifiers kept as `package_id`, and SF-01…SF-25 from WP-C-04) and
`aou.yaml` (AOU-01…AOU-07 from WP-C-01).

```sh
python3 assurance/case/tools/validate.py
python3 assurance/case/tools/test_case.py
python3 assurance/case/tools/generate_dashboard.py          # writes status.json, badge.json, the SVGs and the README blocks
python3 assurance/case/tools/generate_dashboard.py --check  # CI: fail if any output is stale
```
