#!/usr/bin/env python3
"""Self-tests for process_model.py: the committed model passes, and each check rejects a broken copy."""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import process_model as pm


class ProcessModelTest(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.base = pm.load_model()
    cls.ctx = pm.load_context()

  def run_check(self, mutate=None) -> list[str]:
    model = copy.deepcopy(self.base)
    model.errors = []
    if mutate:
      mutate(model)
    pm.check(model, self.ctx)
    return model.errors

  def assertFails(self, check: str, mutate) -> None:
    errors = self.run_check(mutate)
    self.assertTrue(any(e.startswith(f"[{check}]") for e in errors), f"expected a {check} error, got {errors}")

  def test_committed_model_passes(self):
    self.assertEqual(self.run_check(), [])

  def test_committed_maps_are_current(self):
    self.assertEqual(pm.main(["process_model.py", "--check"]), 0)

  def test_yaml_subset_parses_flow_lists_and_scalars(self):
    items = pm.load_subset("- id: X\n  kind: phase\n  modelled: true\n  n: 3\n  l: [a, b]\n  e: []\n  s: \"a, b\"\n")
    self.assertEqual(items, [{"id": "X", "kind": "phase", "modelled": True, "n": 3, "l": ["a", "b"], "e": [], "s": "a, b"}])
    with self.assertRaises(ValueError):
      pm.load_subset("- id: X\n    nested: 1\n")

  def test_unknown_role(self):
    self.assertFails("P2", lambda m: m.lanes["cs"].update(role="Security wizard"))

  def test_unregistered_work_product(self):
    self.assertFails("P3", lambda m: m.activities["CON-01"].update(produces=["WP-C-99"]))

  def test_work_product_in_wrong_phase(self):
    self.assertFails("P3", lambda m: m.activities["CON-12"].update(produces=["WP-T-01", "WP-K-01", "WP-S-01"]))

  def test_g1_work_product_without_activity(self):
    self.assertFails("P4", lambda m: m.activities.pop("CON-11"))

  def test_input_from_later_activity(self):
    self.assertFails("P5", lambda m: m.activities["CON-02"]["inputs"].append("WP-C-03"))

  def test_input_from_later_gate(self):
    self.assertFails("P5", lambda m: m.activities["CON-02"]["inputs"].append("WP-S-01"))

  def test_review_set_differs_from_wp_m_06(self):
    self.assertFails("P6", lambda m: m.reviews.pop("ML-R1"))

  def test_missing_anchor_text(self):
    self.assertFails("P7", lambda m: m.interfaces["IX-01"].update(anchors=["WP-C-03:text that is not in the risk assessment"]))

  def test_open_interface_needs_open_item(self):
    open_ix = next(i for i, x in self.base.interfaces.items() if x["status"] == "open")
    self.assertFails("P7", lambda m: m.interfaces[open_ix].update(open_item=None))

  def test_review_gate_suffix_matches_phase(self):
    self.assertFails("P6", lambda m: m.reviews["CR-06@G2"].update(phase="G1"))

  def test_mermaid_node_ids_are_plain(self):
    self.assertEqual(pm._nid("CR-06@G2"), "CR_06_G2")

  def test_roles_of_lanes_idle_in_a_phase_are_still_listed(self):
    # The electrical and mechanical lane has no G5 activity, but WP-M-02 needs its role by G2.
    model = copy.deepcopy(self.base)
    orders = pm.check(model, self.ctx)
    g5 = pm.render_phase("G5", orders["G5"], model, self.ctx)
    self.assertIn("needs by G5:** ", g5)
    self.assertIn("Electrical and mechanical engineer", g5.split("needs by G5:** ")[1].splitlines()[0])

  def test_interface_due_before_its_phase(self):
    self.assertFails("P7", lambda m: m.interfaces["IX-09"].update(due="G3"))

  def test_update_of_non_living_work_product(self):
    self.assertFails("P3", lambda m: m.activities["REL-11"].update(updates=["WP-K-01", "WP-C-03"]))

  def test_update_outside_living_range(self):
    self.assertFails("P3", lambda m: m.activities["CON-12"].update(updates=["WP-K-01"]))

  def test_input_from_later_update(self):
    self.assertFails("P5", lambda m: m.activities["REL-04"]["inputs"].append("WP-K-01"))

  def test_assessor_report_counts_as_confirmation_of_its_inputs(self):
    model = copy.deepcopy(self.base)
    orders = pm.check(model, self.ctx)
    g5 = pm.render_phase("G5", orders["G5"], model, self.ctx)
    line = next(ln for ln in g5.splitlines() if ln.startswith("**Work products with no confirmation measure"))
    for wp in ("WP-K-03", "WP-K-04", "WP-K-05", "WP-V-06"):
      self.assertNotIn(wp, line)

  def test_feedback_into_a_later_phase(self):
    self.assertFails("P9", lambda m: m.feedback["FB-01"].update(targets=["WP-O-05"]))

  def test_feedback_anchor_missing(self):
    self.assertFails("P9", lambda m: m.feedback["FB-03"].update(anchors=["WP-O-04:no such routing row"]))

  def test_gate_without_measures_renders_without_empty_lane(self):
    model = copy.deepcopy(self.base)
    orders = pm.check(model, self.ctx)
    g6 = pm.render_phase("G6", orders["G6"], model, self.ctx)
    self.assertNotIn("L_assess", g6)
    self.assertIn("none planned at this gate", g6)
    self.assertNotRegex(g6, r"\n  class +review")

  def test_plan_role_table_is_parsed(self):
    roles = pm.load_plan_roles("x\n| Role | Holder (today) | Duty |\n|---|---|---|\n| ML safety lead | A. Person | x |\n\nafter")
    self.assertEqual(roles, {"ML safety lead": "A. Person"})

  def test_role_disagreement_is_reported(self):
    ctx = copy.deepcopy(self.ctx)
    ctx.plan_roles["WP-M-08"] = {"Cybersecurity manager": "TBD"}
    out = pm.role_disagreements(ctx, self.base)
    self.assertEqual(len(out), 1)
    self.assertIn("Cybersecurity manager", out[0])

  def test_gate_measures_regex_knows_every_measure_family(self):
    text = "| G5 | CR-12; FSA-F (WP-K-04); CS-A1 (WP-K-05); ML-R3; NB-1 |\n| G1 | CS-I1; AUD-1 |"
    self.assertEqual(pm.load_gate_measures(text), {"G5": ["CR-12", "FSA-F", "CS-A1", "ML-R3", "NB-1"], "G1": ["CS-I1", "AUD-1"]})

  def test_record_patterns(self):
    self.assertEqual(pm.record_pattern("CR-06@G2"), "CR-06-*.md")
    self.assertEqual(pm.record_pattern("ML-R1"), "ML-R1.md")
    self.assertEqual(pm.record_pattern("SR-01@G2"), "SR-01-G2.md")


if __name__ == "__main__":
  unittest.main()
