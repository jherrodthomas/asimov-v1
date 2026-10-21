# WP-P-01 Configuration management plan (safety-relevant file list, baselines of the fork, the kit and the firmware)

| Field | Value |
|---|---|
| Work product | WP-P-01 Configuration management plan (safety-relevant file list, baselines of the fork, the kit and the firmware) |
| Standard reference | SRP/CS: 61508-1 §6.2.3; 13849-1 §12; IEC 62443: 62443-4-1 SM-6, SM-7; ASPICE: SUP.8 |
| Version | 0.0 (skeleton: structure, clause map and seeds from the concept-phase package; 2026-10-21) |
| Status | Skeleton |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `3d4ec9d` (BL-001) |

> [!NOTE]
> **Skeleton.** The structure and clause mapping exist; the content is still to be written. The gate that needs this
> work product is **G0** ([WP-M-00](../01-management/WP-M-00-work-product-register.md#3-register)).

## 1. Purpose

Configuration management for the fork: the configuration items in this repository (CAD, electrical, simulation model, the record), the firmware and policy repositories once they exist, the safety-relevant file list, baselines and tags, pins and how they move, and the branch rules.

## 2. Configuration items

This repository (`mechanical/`, `electrical/`, `sim-model/`, `assurance/`); the upstream repository as a remote; the kit BOM; the SISTEMA project; test logs; firmware, API and policy repositories when published.

## 3. Safety-relevant file list

The authoritative, machine-readable copy is [`safety-relevant-paths.txt`](safety-relevant-paths.txt): classes SR-A (safety-chain and motion-control-board design files, the firmware safety layer, safety parameter sets), SR-Q (functional layers that feed hazards or configure limits: mechanical CAD, the simulation model, harness), SR-T (build, CI, toolchain, pins). Anything else is NSR.

## 4. Baselines

`BL-nnn` records in the Living Safety Case (`case/baselines/`) at each gate and release; tags once the repository rules allow. Session records: the telemetry of every powered session is kept with the session record under `06-validation/test-sites/`; room video is kept for the campaign plus one gate, then deleted unless an anomaly report refers to it (DQ-040 A, 2026-10-21).

## 5. Branch and review rules

Pull requests only; two approvals on SR-A paths; CODEOWNERS.

## 6. Pins

How a pin moves: change record, impact analysis, one pull request.

## 7. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G0 |
