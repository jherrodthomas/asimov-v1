#!/usr/bin/env python3
"""Self-tests for the Living Safety Case validator (assurance/case/tools/caselib.py).

Each test copies the real records, plants one defect and checks that the validator reports it
with the expected check code. The acceptance tests make sure nothing can be marked accepted
without a recorded review.

Usage: python3 assurance/case/tools/test_case.py
"""
from __future__ import annotations

import copy
import unittest

from caselib import Case, Report, load_case, summarize, validate


def fresh() -> Case:
  base = load_case()
  return Case(base.schema, copy.deepcopy(base.records), dict(base.trace_ids), Report())


def codes(case: Case) -> set[str]:
  return {e.split("]")[0].lstrip("[") for e in validate(case).errors}


def add_review(case: Case, objects: list[str], outcome: str = "accepted") -> None:
  case.records["REV-001"] = {
    "id": "REV-001", "kind": "review", "_file": "test", "title": "Test review", "reviewed_objects": objects,
    "reviewer": "Reviewer", "independence": "I1", "review_date": "2026-01-31", "outcome": outcome,
    "baseline": "BL-001", "record": "test", "source_revision": "8a7a5b1",
  }


def accept(obj: dict) -> None:
  obj.update(review_state="accepted", reviewer="Reviewer", review_date="2026-01-31", review_ref="REV-001")


class TestRecords(unittest.TestCase):
  def test_repository_records_are_valid(self):
    self.assertEqual(validate(fresh()).errors, [])

  def test_summary_counts_records(self):
    case = fresh()
    s = summarize(case)
    self.assertEqual(s["claims"]["registered"], len(case.of_kind("claim")))
    self.assertEqual(s["evidence"]["registered"], len(case.of_kind("evidence")))
    self.assertEqual(s["claims"]["accepted"], 0)
    self.assertEqual(s["configurations"]["assurance_supported"], 0)


class TestStructure(unittest.TestCase):
  def test_dangling_reference(self):
    case = fresh()
    case.records["G1.1"]["evidence_refs"] = case.records["G1.1"]["evidence_refs"] + ["Sn-99"]
    self.assertIn("V3", codes(case))

  def test_unknown_trace_id(self):
    case = fresh()
    case.records["G1.1"]["related_hazards"] = ["SG-99"]
    self.assertIn("V3", codes(case))

  def test_one_directional_link(self):
    case = fresh()
    case.records["Sn-01"]["related_claims"] = [c for c in case.records["Sn-01"]["related_claims"] if c != "G0"]
    self.assertIn("V4", codes(case))

  def test_bad_enum_and_missing_field(self):
    case = fresh()
    case.records["Sn-01"]["evidence_status"] = "done"
    del case.records["Sn-02"]["location"]
    self.assertTrue({"V1", "V2"} <= codes(case))

  def test_missing_location(self):
    case = fresh()
    case.records["Sn-01"]["location"] = "assurance/does-not-exist.md"
    self.assertIn("V5", codes(case))


class TestAcceptanceRules(unittest.TestCase):
  def test_claim_cannot_be_accepted_without_review(self):
    case = fresh()
    case.records["G1.7"]["lifecycle_status"] = "accepted"
    self.assertIn("V6", codes(case))

  def test_review_state_needs_a_review_record(self):
    case = fresh()
    case.records["Sn-10"].update(review_state="accepted", reviewer="CI", review_date="2026-01-31", review_ref=None)
    self.assertIn("V6", codes(case))

  def test_rejected_review_does_not_accept(self):
    case = fresh()
    add_review(case, ["Sn-10"], outcome="rejected")
    accept(case.records["Sn-10"])
    self.assertIn("V6", codes(case))

  def test_available_evidence_needs_acceptance(self):
    case = fresh()
    case.records["Sn-10"]["evidence_status"] = "available"
    self.assertIn("V6", codes(case))

  def test_missing_evidence_cannot_be_accepted(self):
    case = fresh()
    add_review(case, ["Sn-11"])
    accept(case.records["Sn-11"])
    self.assertIn("V6", codes(case))

  def test_accepted_claim_with_open_defeater_is_refused(self):
    case = fresh()
    claim = case.records["G1.4"]
    add_review(case, [claim["id"]] + claim["evidence_refs"])
    for ref in claim["evidence_refs"]:
      case.records[ref]["evidence_status"] = "available"
      accept(case.records[ref])
    claim["lifecycle_status"] = "accepted"
    accept(claim)
    errors = validate(case).errors
    self.assertTrue(any("open defeater" in e for e in errors))

  def test_reviewed_claim_is_accepted_cleanly(self):
    case = fresh()
    claim = case.records["G1.7"]
    add_review(case, [claim["id"]] + claim["evidence_refs"])
    for ref in claim["evidence_refs"]:
      case.records[ref]["evidence_status"] = "available"
      accept(case.records[ref])
    for ref in claim["defeaters"]:
      case.records[ref]["lifecycle_status"] = "closed"
    claim["lifecycle_status"] = "accepted"
    accept(claim)
    v6 = [e for e in validate(case).errors if e.startswith("[V6]")]
    self.assertEqual(v6, [])
    self.assertEqual(summarize(case)["claims"]["accepted"], 1)

  def test_assurance_supported_needs_accepted_claim(self):
    case = fresh()
    case.records["CFG-001"]["classification"] = "assurance-supported"
    self.assertIn("V6", codes(case))


if __name__ == "__main__":
  unittest.main()
