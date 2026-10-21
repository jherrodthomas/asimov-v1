# Confirmation measure records

Records of confirmation reviews (CR-01…CR-12), functional safety audits (`AUD-<n>.md`), interim functional safety
assessments (`FSA-I1.md`, `FSA-I2.md`), the cybersecurity review (`CS-I1.md`) and the ML reviews (`ML-R<n>.md`), as
planned in [WP-M-06](../../01-management/WP-M-06-confirmation-measures-plan.md). The final assessment reports are
[WP-K-04](../WP-K-04-functional-safety-assessment.md) and [WP-K-05](../WP-K-05-cybersecurity-assessment.md); a notified
body's type-examination certificate, if any, is filed under [WP-K-02](../WP-K-02-technical-documentation-index.md).

No confirmation measure has been performed yet.

## Rules

- Records use the review record template of [WP-P-05 §6](../../07-supporting/WP-P-05-verification-review-procedure.md)
  with review type `confirmation`, `audit` or `assessment`.
- Each record is written by the named reviewer, auditor or assessor at the independence level WP-M-06 requires, and
  states that independence in writing (WP-M-06 §6.1).
- Author-side self-checks and AI-generated pre-review audits are inputs to a confirmation measure. They are never
  stored here and never count as one.
- An accepted confirmation review is also entered in the Living Safety Case review records once those are ported,
  so a claim can reference it.

## File naming

| Measure | File |
|---|---|
| Confirmation review | `CR-<nn>-<WP-ID>-v<version>.md` (WP-M-06 §4.2 step 5), e.g. `CR-02-WP-C-03-v1.0.md` |
| Functional safety audit | `AUD-<n>.md` |
| Interim functional safety assessment | `FSA-I1.md`, `FSA-I2.md` |
| Cybersecurity review | `CS-I1.md` |
| ML review | `ML-R<n>-<gate>.md`, e.g. `ML-R1-G1.md` |
