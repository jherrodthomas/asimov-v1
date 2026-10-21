#!/usr/bin/env python3
"""Tests for process_figures.py: well-formed SVG, every activity drawn in its phase, --check round trip."""
from __future__ import annotations

import sys
import tempfile
import unittest
import xml.dom.minidom
from xml.sax.saxutils import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import process_figures as pf  # noqa: E402
import process_model as pm  # noqa: E402


class FigureTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.view = pf.View()
    cls.figs = pf.render_all(cls.view)

  def test_every_figure_is_well_formed_svg_with_a_title_and_description(self):
    self.assertEqual(tuple(self.figs), pf.NAMES)
    for name, s in self.figs.items():
      xml.dom.minidom.parseString(s)
      self.assertTrue(s.startswith("<svg"), name)
      self.assertIn("<title", s, name)
      self.assertIn("<desc", s, name)

  def test_every_activity_review_and_interface_is_drawn_in_its_phase(self):
    for g in pm.GATES:
      s = self.figs[f"{g.lower()}.svg"]
      for a in self.view.model.activities.values():
        if a["phase"] == g:
          self.assertIn(f">{a['id']}<", s, f"{a['id']} missing from {g}")
      for r in self.view.model.reviews.values():
        if r["phase"] == g:
          self.assertIn(pm.measure_id(r["id"]), s, f"{r['id']} missing from {g}")
      for ix in self.view.model.interfaces.values():
        if ix["phase"] == g:
          self.assertIn(ix["id"], s, f"{ix['id']} missing from {g}")
      self.assertIn(self.view.ctx.gates[g][0], s)

  def test_the_lifecycle_figure_carries_every_lane_and_gate(self):
    s = self.figs["lifecycle-swimlanes.svg"]
    for lane in self.view.model.lanes:
      self.assertIn(escape(pf.LANE_SHORT[lane]), s)
    for g in pm.GATES:
      self.assertIn(f">{g}<", s)
    self.assertIn(f"{len(self.view.model.activities)} activities", s)

  def test_the_interfaces_figure_lists_every_interface_with_its_status(self):
    s = self.figs["interfaces.svg"]
    for ix in self.view.model.interfaces.values():
      self.assertIn(f">{ix['id']}<", s)
      self.assertIn(ix["pattern"], s)
    self.assertIn(">OPEN<", s)

  def test_write_then_check_round_trips_and_detects_staleness(self):
    with tempfile.TemporaryDirectory() as d:
      out = Path(d)
      self.assertEqual(pf.main(["--out", str(out)]), 0)
      self.assertEqual(pf.check_dir(out), 0)
      (out / "g1.svg").write_text("stale", encoding="utf-8")
      self.assertEqual(pf.check_dir(out), 1)

  def test_the_committed_figures_are_current(self):
    self.assertEqual(pf.check_dir(pf.OUT_DIR), 0)


if __name__ == "__main__":
  unittest.main()
