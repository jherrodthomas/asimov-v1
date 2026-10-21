## What this changes and why

<!-- One paragraph. Name the work products touched. -->

## Safety-impact statement

<!-- Every pull request answers these; "none" is a valid answer with a reason (WP-P-02, WP-M-11). -->

- **Safety-relevant class** (`SR-A`, `SR-Q`, `SR-T`, or `NSR`; see `assurance/07-supporting/safety-relevant-paths.txt`):
- **Hazards, safety functions, requirements or assumptions affected:**
- **Impact analysis record** (`assurance/07-supporting/impact/`), if SR-A or SR-Q:
- **Verification done** (tests, analyses, generators re-run):

## Checks

- [ ] `python3 assurance/01-management/decisions/check_decisions.py`
- [ ] `python3 assurance/tools/folder_index.py --check`
- [ ] `python3 assurance/process/tools/process_model.py --check`
- [ ] `python3 docs/assets/asimov/make_assets.py --check`
- [ ] `python3 assurance/tools/check_links.py && python3 assurance/tools/check_tables.py`
- [ ] `python3 tools/wiki/build_wiki.py`
- [ ] Generated files (maps, skeletons, folder READMEs, figures) regenerated, never edited by hand
- [ ] No safety claim added that the evidence does not support; no status moved past Draft without a review record
