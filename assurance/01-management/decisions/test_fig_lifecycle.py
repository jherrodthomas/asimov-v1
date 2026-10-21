#!/usr/bin/env python3
"""Tests for fig_lifecycle.py: sources present, SVG current and valid, every state drawn, drift detected."""

import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fig_lifecycle as fl

NS = "{http://www.w3.org/2000/svg}"


class TestLifecycleFigure(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.md = fl.README.read_text(encoding="utf-8")
    cls.svg = fl.build()

  def test_no_source_problems(self):
    self.assertEqual(fl.problems(self.md), [])

  def test_committed_output_current_and_deterministic(self):
    self.assertEqual(fl.OUT.read_text(encoding="utf-8"), self.svg, "stale; run fig_lifecycle.py")
    self.assertEqual(fl.build(), self.svg)

  def test_svg_valid_phone_width_dark_theme(self):
    root = ET.fromstring(self.svg)
    self.assertEqual(root.get("role"), "img")
    self.assertEqual(root.get("width"), str(fl.W))
    self.assertTrue(root.find(f"{NS}title").text)
    self.assertIn("prefers-color-scheme: dark", self.svg)

  def test_every_state_drawn_with_who_moves_it(self):
    desc = ET.fromstring(self.svg).find(f"{NS}desc").text
    for s, (_m, who) in fl.states(self.md).items():
      self.assertIn(f">{s}<", self.svg)
      self.assertIn(f"{s}: ", desc)
      self.assertIn(f"(moved by {who})", desc)

  def test_drift_is_reported(self):
    md = self.md.replace("| `withdrawn` |", "| `rejected` |")
    self.assertTrue(any("differs from check_decisions.STATUS" in p for p in fl.problems(md)))
    md = self.md.replace("No answer by `proceed_after`", "No reply by the deadline")
    self.assertTrue(any("open -> assumed" in p for p in fl.problems(md)))
    md = self.md.replace("](figures/fig-dr-1-lifecycle.svg)", "](figures/other.svg)")
    self.assertTrue(any("does not embed" in p for p in fl.problems(md)))


if __name__ == "__main__":
  unittest.main()
