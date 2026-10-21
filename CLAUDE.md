# Working with the project lead

This repository is a fork of the Asimov v1 open-source humanoid robot that carries its safety-assurance record under
`assurance/`. The project lead is its safety authority and often reviews from a phone. Keep the decisions asked of
them few, and make each one quick to answer.

## Decisions

Every question for the lead lives in the decision register,
[`assurance/01-management/decisions/register.yaml`](assurance/01-management/decisions/register.yaml). Its
[README](assurance/01-management/decisions/README.md) has the lifecycle and the inbox page it builds.

1. **Sort before asking.** Ask the lead only what they alone can decide: risk acceptance, Performance Level or
   hazard scope, the safe state of the biped, robot behaviour defaults, operating-envelope limits, money or hardware,
   the assessor, roles and independence, gate go/no-go. A reversible technical choice gets `decider: claude`: go with
   the recommendation and say so. A task is not a decision; it stays in its work product.
2. **Every question stands on its own.** Never send a bare ID ("decide F-3"). An entry has the question in plain
   words, two or three lines on what is at stake, two to four options with what each does and costs, the
   recommendation first, how hard it is to undo, what it blocks, and its sources. Add one picture when it shows the
   difference between the options; skip it when it would only decorate.
3. **Batches of ten.** Keep about ten questions open, those that unblock the most. When the lead has answered a
   batch, open the next ten from the queue and rewrite each to the standard above. Everything else waits as `queued`.
4. **Start of a session, and whenever the inbox page sends a note:** read the inbox page's `answers`, `explain` and
   `signals` collections, copy answers into the register, apply them, and answer explanation requests before asking
   anything new.
5. **In chat**, name a decision by its question, not its ID. Ask in chat only when blocked right now: multiple choice
   with the recommendation first.

## The record

- The standards are the machinery and robot set (ISO 12100, ISO 10218-1/-2 with ISO/TS 15066, ISO 13482,
  ISO 13849-1, IEC 60204-1, IEC 62133-2, IEC 62443, ISO/IEC TR 5469, the Machinery Regulation); how each is used is
  [WP-M-01 §4](assurance/01-management/WP-M-01-assurance-strategy.md#4-the-standards-and-how-each-one-is-used). No
  standard is held: mark every clause reference as to be checked against a licensed copy.
- A biped is not a wheeled machine: removing power is itself a hazard. Never write a safe state, a stop category or a
  fall-arrest claim as settled while DQ-005 (safe state) and DQ-006 (whether the learned policy may carry balance) are
  open; the tether and gantry carry the fall in the laboratory until then.
- Generated files are never edited by hand: folder READMEs (`assurance/tools/folder_index.py`), process maps and
  gate skeletons (`assurance/process/tools/process_model.py`), process swimlane figures
  (`assurance/process/tools/process_figures.py`), README and wiki figures (`docs/assets/asimov/make_assets.py`),
  the safety-case dashboard (`assurance/case/tools/generate_dashboard.py`), the decision lifecycle figure. Run the
  generator and commit its output.
- A new work product goes into [WP-M-00](assurance/01-management/WP-M-00-work-product-register.md) first, with the
  document-control header of the [assurance README](assurance/README.md#document-control-header); then the process
  model gets an activity that produces it.
- The wiki is kept in [`wiki/`](wiki/README.md) and mirrored on merge; it explains and links, never claims.
- Before pushing, run the checks in [CONTRIBUTING.md](CONTRIBUTING.md); CI runs the same.

## Upstream

The robot is published by Asimov Inc. in `asimovinc/asimov-v1`; its CAD, boards and simulation model live in this
repository under `mechanical/`, `electrical/` and `sim-model/` and change only through the change process
(WP-P-02), never silently. The firmware, the Asimov API and the locomotion policy are not published; quote upstream's
manual and README for them, do not restate or invent them. The concept-phase package under
`assurance/00-assessment/concept-package/` is an inherited input: never edit its files; the record supersedes them.
