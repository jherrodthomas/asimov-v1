# WP-M-10 Upstream (Asimov Inc) and supplier management (kit, actuators, battery)

| Field | Value |
|---|---|
| Work product | WP-M-10 Upstream (Asimov Inc) and supplier management (kit, actuators, battery) |
| Standard reference | SRP/CS: 61508-1 §6.2 (subcontracted activities); IEC 62443: 62443-4-1 SM-9, SM-10; ASPICE: ACQ.4 |
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

Management of upstream Asimov Inc (Menlo) as a supplier without a development interface agreement, and of the kit, actuator, battery and board suppliers the DIY build depends on.

## 2. Upstream

The `asimovinc/asimov-v1` repository, the manual at manual.asimov.inc, the DIY kit; what the fork takes (CAD, electrical, simulation model), what it waits for (firmware, API, locomotion policy), how upstream changes are tracked (WP-P-02).

## 3. Suppliers

Actuators (BLDC with harmonic gear and encoder, typical of 25), the motion control board fabrication (JLCPCB), the Radxa CM5 and Raspberry Pi 5, the user-supplied battery and BMS (DQ-009), the E-stop devices, 7075-T6 and 316L stock.

## 4. Supplier evidence

Certificates, failure rates and B10d values needed by WP-H-04 and WP-H-07; what is missing at BL-001 (GAP-14).

## 5. Messages to upstream and the community

The lead decided on 2026-10-21 to post two messages (DQ-046 A, DQ-047 A). Both are the lead's to post; the drafts
below are the record's, and what comes back is entered in §2 and §4 as a design input, silence included.

**Reviewer call, for upstream's Discord and forum (DQ-046 A):**

> I maintain a fork of asimov-v1 that carries a safety-assurance record for the kit robot: a risk assessment, safety
> functions with a required Performance Level, a hold point for powered tests, and a safety case that publishes its
> own gaps. It is independent of Asimov Inc and claims nothing about their product. I am looking for one person
> with machinery-safety or robotics experience to review two documents, a few hours each: the risk assessment and
> the safety functions. Details and the two documents: [CONTRIBUTING](https://github.com/jherrodthomas/asimov-v1/blob/main/CONTRIBUTING.md).

**Request for design inputs, one public discussion on the upstream repository (DQ-047 A):**

> I am building a safety-assurance record for a tethered laboratory configuration of Asimov v1, published at
> jherrodthomas/asimov-v1. Three things would let the record rest on your data rather than on estimates:
> (1) failure-rate or B10d data for the actuators and their encoders, or the supplier's part numbers so I can ask
> them; (2) the design of the wireless E-stop: receiver, what it switches, stop category, re-arm behaviour;
> (3) the mode machine's specification (DAMP, STAND, MOVE: transitions, timeouts, watchdog). The record's findings
> about the kit are public and yours to use. Where you prefer not to answer, the record will state that the data
> was requested and not available.

## 6. Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Write the content; the sections above are the clause map and the seed from the gap assessment and the concept-phase package | Safety manager | G0 |
