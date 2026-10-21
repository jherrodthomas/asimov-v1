# Contributing to the Asimov v1 assurance record

Contributions are welcome in machinery and robot safety, safety-related control systems, electrical and mechanical
engineering, firmware, legged locomotion, cybersecurity, verification, documentation and review. A review of an
analysis is as valuable as code. The [wiki's contributor guide](https://github.com/jherrodthomas/asimov-v1/wiki/Contributor-guide)
is the short version of this page.

## Where to start

- **Questions and bugs:** [open an issue](https://github.com/jherrodthomas/asimov-v1/issues) with the problem
  report or safety concern template.
- **Changes:** branch from `main` and open a pull request against `main`. The pull request template asks for a
  safety-impact statement; "none" is a valid answer with a reason.
- **Decisions for the project lead** are not issues. They go into the
  [decision register](assurance/01-management/decisions/README.md) as self-contained questions.
- **Upstream sources** (`mechanical/`, `electrical/`, `sim-model/`, the upstream part of the README) are changed only
  under the change process below, never silently; upstream's own repository is `asimovinc/asimov-v1` and its
  documentation stays where upstream keeps it.

## Safety-relevant changes

A change is safety-relevant if it touches a path on the
[safety-relevant file list](assurance/07-supporting/safety-relevant-paths.txt) or changes an assurance work product.
Such a pull request must include:

1. **Rationale:** what the change does and why.
2. **Impact analysis:** which hazards, safety functions, requirements and assumptions it affects, following
   [WP-M-11](assurance/01-management/WP-M-11-impact-analysis.md) and [WP-P-02](assurance/07-supporting/WP-P-02-change-management.md),
   recorded under [`assurance/07-supporting/impact/`](assurance/07-supporting/impact/README.md).
3. **Verification:** the tests or analyses that show the change is correct, and their results.
4. **Record updates:** the affected work products, with every generator re-run.

## Checks to run locally

Only Python 3 is needed (PyYAML for the decision register):

```sh
python3 assurance/case/tools/validate.py
python3 assurance/case/tools/generate_dashboard.py --check
python3 assurance/01-management/decisions/check_decisions.py
python3 assurance/01-management/decisions/fig_lifecycle.py --check
python3 assurance/tools/folder_index.py --check
python3 assurance/process/tools/process_model.py --check
python3 assurance/process/tools/process_figures.py --check
python3 docs/assets/asimov/make_assets.py --check
python3 assurance/tools/check_links.py
python3 assurance/tools/check_tables.py
python3 tools/wiki/build_wiki.py
```

CI runs the same checks on every pull request and fails if a generated file is out of date.

## What can and cannot change a review state

- A work product leaves `Draft` only through a verification review by someone other than its author
  ([WP-P-05](assurance/07-supporting/WP-P-05-verification-review-procedure.md)), and a claim is accepted only through
  a confirmation review at the independence [WP-M-06](assurance/01-management/WP-M-06-confirmation-measures-plan.md)
  requires.
- A passing CI run, a passing test or an existing file does not accept anything. It can be evidence that a reviewer
  accepts.
- An AI-generated review is not a substitute for the required independent confirmation. AI-drafted work is the
  committer's work at independence level I0 ([WP-M-02 §3.3](assurance/01-management/WP-M-02-safety-plan.md#33-ai-assisted-authoring)).
- Never edit generated files (process maps, swimlane figures, gate skeletons, folder READMEs, README figures, the
  dashboard) by hand. Change the source and regenerate.

## Working with Claude sessions

Much of the drafting is done in Claude Code sessions under the project lead's direction. The rules those sessions
follow are in [CLAUDE.md](CLAUDE.md): sort questions before asking, keep every question self-contained, ask in
batches of ten, record decisions in the register. A session's pull request is reviewed like any other.

## Licensing

Asimov v1 is published by Asimov Inc. under CERN-OHL-S-2.0 ([hardware](HARDWARE-LICENSE.txt)) and GPL-2.0
([software](SOFTWARE-LICENSE.txt)). Contributions to the record are derivative analytical works under the same
licences; forks must not imply Asimov Inc.'s endorsement.
