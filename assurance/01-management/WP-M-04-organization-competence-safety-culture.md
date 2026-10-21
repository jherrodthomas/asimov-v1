# WP-M-04 Organization-specific rules, safety culture, competence management

| Field | Value |
|---|---|
| Work product | WP-M-04 Organization-specific rules, safety culture, competence management |
| Standard reference | SRP/CS: 61508-1 §6.2 (competence); 13849-1 §4; IEC 62443: 62443-4-1 SM-4 |
| Version | 0.0 (skeleton: structure, clause map and seeds from the concept-phase package; 2026-10-21) |
| Status | Skeleton |
| PL / scope | All |
| Author | Assurance team (AI-assisted draft, I0) |
| Reviewer(s) | TBD (I1) |
| Approver | Safety manager |
| Baseline | `3d4ec9d` (BL-001) |

> [!NOTE]
> **Skeleton.** The structure and clause mapping exist; the content is still to be written. The gate that needs this
> work product is **G0** ([WP-M-00](WP-M-00-work-product-register.md#3-register)).

## 1. Purpose

Organisation-specific rules, safety culture and competence management for a one-maintainer open-source fork: who may author, review and approve what, the competence each role needs and how it is evidenced.

## 2. Organisation

Roles per WP-M-02 §3.1; one maintainer holds most of them; the independence rules of WP-M-01 T-09.

## 3. Safety culture rules

No claim without evidence; every clause reference marked to be checked; every safety-relevant change carries an impact record; anomalies stop testing; AI-drafted work is the committer's work at I0 (WP-M-02 §3.3).

## 4. Competence

Per role: machinery and robot safety (ISO 12100, ISO 10218, ISO 13482, ISO 13849-1), electrical (IEC 60204-1), lithium batteries (IEC 62133-2), real-time firmware and CAN, learned control policies, cybersecurity (IEC 62443); evidence kept here.

## 5. Training

Operator training for WP-V-07; builder briefing for the DIY-kit assembly (WP-O-01); the observer briefing (DQ-052 A, 2026-10-21): any briefed adult may observe once WP-V-07 has been read aloud to them, the stations and the E-stop shown, and a line signed in the session log; the observer never enters the area.

## 6. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G0 |
