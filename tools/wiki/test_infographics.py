#!/usr/bin/env python3
"""Unit tests for infographics.py on a small fixture, plus a render of the real records."""
from __future__ import annotations

import sys
import tempfile
import unittest
import xml.dom.minidom
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import infographics

REGISTER = """\
- id: DQ-001
  status: applied
  reversibility: easy
  decider: claude
  gate: G1
  batch: 1
  answer: {via: inbox}
- id: DQ-002
  status: open
  reversibility: hard
  decider: lead
  gate: G2
  batch: 2
- id: DQ-003
  status: queued
  reversibility: revisit
  gate: G2
"""
PATHS = """\
# comment line
SR-A openamr-platform-fw/src/firmware.ino
SR-A openamr-platform-hw/electrical/safety/**
SR-T .github/**   # workflows
SR-Q openamr-platform-sw/ros2/src/openamrobot_docking/**
"""
WF_PR = "name: checks\non:\n  pull_request:\n  push:\n    branches: [main]\njobs: {}\n"
WF_MANUAL = "name: manual thing\non:\n  workflow_dispatch:\njobs: {}\n"
WP_REGISTER = """\
### 3.1 Management (`01-management/`)

| ID | Work product | Machinery | SRP/CS | IEC 62443 | Other | ASPICE | Gate | Status |
|---|---|---|---|---|---|---|---|---|
| [WP-M-00](WP-M-00-work-product-register.md) | Register | | | | | MAN.3 | G0 | D |
| [WP-M-03](WP-M-03-project-plan.md) | Plan | | | | | MAN.3 | G0 | S |

### 3.10 Safety case (`10-safety-case/`)

| ID | Work product | Machinery | SRP/CS | IEC 62443 | Other | ASPICE | Gate | Status |
|---|---|---|---|---|---|---|---|---|
| [WP-K-01](../10-safety-case/WP-K-01-safety-case.md) | Safety case | | | | UL 4600 | — | G1→G5 (living) | S |
"""


def make_root(tmp: Path) -> Path:
  root = tmp / "repo"
  (root / "assurance" / "01-management" / "decisions").mkdir(parents=True)
  (root / "assurance" / "07-supporting").mkdir(parents=True)
  (root / ".github" / "workflows").mkdir(parents=True)
  (root / "assurance" / "01-management" / "decisions" / "register.yaml").write_text(REGISTER, encoding="utf-8")
  (root / "assurance" / "01-management" / "WP-M-00-work-product-register.md").write_text(WP_REGISTER, encoding="utf-8")
  (root / "assurance" / "07-supporting" / "safety-relevant-paths.txt").write_text(PATHS, encoding="utf-8")
  (root / ".github" / "workflows" / "a.yaml").write_text(WF_PR, encoding="utf-8")
  (root / ".github" / "workflows" / "b.yaml").write_text(WF_MANUAL, encoding="utf-8")
  return root


class LoaderTests(unittest.TestCase):
  def test_classes_count_patterns_not_comments(self):
    with tempfile.TemporaryDirectory() as d:
      root = make_root(Path(d))
      self.assertEqual(infographics.load_classes(root / "assurance" / "07-supporting" / "safety-relevant-paths.txt"),
                       {"SR-A": 2, "SR-T": 1, "SR-Q": 1})

  def test_workflows_know_whether_they_run_on_pull_requests(self):
    with tempfile.TemporaryDirectory() as d:
      root = make_root(Path(d))
      self.assertEqual(infographics.load_workflows(root / ".github" / "workflows"),
                       [("checks", True), ("manual thing", False)])

  def test_wp_register_rows_carry_section_gate_and_status(self):
    with tempfile.TemporaryDirectory() as d:
      root = make_root(Path(d))
      rows = infographics.load_wp_register(root / "assurance" / "01-management" / "WP-M-00-work-product-register.md")
      self.assertEqual(rows, [("WP-M-00", "Management", "G0", "D"), ("WP-M-03", "Management", "G0", "S"),
                              ("WP-K-01", "Safety case", "G1", "S")])


class RenderTests(unittest.TestCase):
  def test_decision_register_figure_carries_the_counts(self):
    with tempfile.TemporaryDirectory() as d:
      root = make_root(Path(d))
      s = infographics.decision_register_svg(infographics.load_register(
        root / "assurance" / "01-management" / "decisions" / "register.yaml"))
      xml.dom.minidom.parseString(s)
      for needle in (">3<", "1 queued", "1 open", "1 applied", "G2 · 2", "1 easy", "1 the lead alone",
                     "1 on the inbox page", "1 waiting"):
        self.assertIn(needle, s, needle)
      self.assertNotIn("withdrawn", s, "a status with no entries is left out")

  def test_change_path_figure_carries_classes_and_workflows(self):
    with tempfile.TemporaryDirectory() as d:
      root = make_root(Path(d))
      s = infographics.change_path_svg(
        infographics.load_classes(root / "assurance" / "07-supporting" / "safety-relevant-paths.txt"),
        infographics.load_workflows(root / ".github" / "workflows"))
      xml.dom.minidom.parseString(s)
      for needle in ("2 patterns", "1 patterns", "1 WORKFLOWS CHECK IT", ">checks<", "manual thing"):
        self.assertIn(needle, s, needle)

  def test_register_status_figure_carries_the_counts(self):
    with tempfile.TemporaryDirectory() as d:
      root = make_root(Path(d))
      s = infographics.register_status_svg(infographics.load_wp_register(
        root / "assurance" / "01-management" / "WP-M-00-work-product-register.md"))
      xml.dom.minidom.parseString(s)
      for needle in (">3<", "2 Skeleton", "1 Draft", ">G0<", ">G1<"):
        self.assertIn(needle, s, needle)

  def test_write_then_check_round_trips_and_detects_staleness(self):
    with tempfile.TemporaryDirectory() as d:
      root = make_root(Path(d))
      out = Path(d) / "out"
      self.assertEqual(infographics.write_all(out, root), ["change-path.svg", "decision-register.svg", "register-status.svg"])
      self.assertEqual(infographics.check_all(out, root), [])
      (out / "change-path.svg").write_text("stale", encoding="utf-8")
      self.assertEqual(infographics.check_all(out, root), ["change-path.svg"])

  def test_the_real_records_render_to_well_formed_svg(self):
    for name, s in infographics.render_all().items():
      xml.dom.minidom.parseString(s)
      self.assertIn("<svg", s, name)


if __name__ == "__main__":
  unittest.main()
