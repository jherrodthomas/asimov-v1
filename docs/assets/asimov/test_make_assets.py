#!/usr/bin/env python3
"""Tests for make_assets.py: well-formed SVG, the data lands in the figures, --check detects staleness."""
from __future__ import annotations

import sys
import tempfile
import unittest
import xml.dom.minidom
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_assets as ma


class RenderTests(unittest.TestCase):
  def test_every_figure_is_well_formed_svg(self):
    for name, s in ma.render_all().items():
      xml.dom.minidom.parseString(s)
      self.assertTrue(s.startswith("<svg"), name)
      self.assertIn("<title", s, name)
      self.assertIn("<desc", s, name)

  def test_data_lands_in_the_figures(self):
    figs = ma.render_all()
    for chip in ma.CHIPS:
      self.assertIn(chip, figs["hero.svg"])
    for name, _, question, _ in ma.STANDARDS:
      self.assertIn(question, figs["standards.svg"])
      self.assertIn(name.split(" ")[0], figs["standards.svg"])
    for _, title, _, _ in ma.LAYERS:
      self.assertIn(title, figs["architecture.svg"])
    for _, name, status, _ in ma.ROADMAP:
      self.assertIn(name, figs["roadmap.svg"])
      self.assertIn(status, figs["roadmap.svg"])
    for g, _, _ in ma.GATES:
      self.assertIn(f">{g}<", figs["lifecycle.svg"])
    self.assertIn("TODAY · " + ma.TODAY_PHASE, figs["lifecycle.svg"])

  def test_status_card_and_headline_come_from_the_records(self):
    r = ma.load_records()
    self.assertGreater(r["wp_total"], 0)
    self.assertEqual(r["wp_total"], sum(r["wp"].values()))
    self.assertEqual(r["gaps_total"], sum(r["gaps"].values()))
    self.assertEqual(len(r["digest"]), 12)
    s = ma.status_svg(r)
    xml.dom.minidom.parseString(s)
    self.assertIn(f">{r['wp_total']}<", s)
    self.assertIn(f">{r['gaps_total']}<", s)
    self.assertIn(r["digest"], s)
    h = ma.headline(r)
    self.assertIn(f"{r['wp_total']} work products", h)
    self.assertIn(f"{r['gaps_total']} gap findings", h)
    self.assertIn(r["digest"], h)

  def test_the_standards_map_is_counted_from_the_register(self):
    r = ma.load_records()
    names = [n for n, _, _ in ma.STANDARD_PATTERNS]
    self.assertEqual(list(r["std_matrix"]), names)
    self.assertGreater(sum(r["std_matrix"]["ISO 13849-1 / -2"].values()), 0)
    self.assertGreater(sum(r["std_matrix"]["IEC 62443-4-1 / -4-2"].values()), 0)
    s = ma.standards_map_svg(r)
    xml.dom.minidom.parseString(s)
    for n in names:
      self.assertIn(n.replace("&", "&amp;"), s)
    self.assertIn(r["digest"], s)

  def test_the_repository_map_names_the_code_the_record_and_the_outputs(self):
    s = ma.repo_map_svg()
    xml.dom.minidom.parseString(s)
    for name, _, _ in ma.REPO_CODE:
      self.assertIn(name, s)
    for _, folder, _ in ma.REPO_RECORD:
      self.assertIn(folder, s)
    for what, _, _ in ma.REPO_OUTPUTS:
      self.assertIn(what.split(",")[0], s)

  def test_headline_block_is_replaced_in_place(self):
    r = ma.load_records()
    doc = f"before\n{ma.HEADLINE_BEGIN}\n\nold\n\n{ma.HEADLINE_END}\nafter"
    out = ma.with_headline(doc, r)
    self.assertTrue(out.startswith("before\n") and out.endswith("\nafter"))
    self.assertIn(ma.headline(r), out)
    self.assertNotIn("old", out)
    self.assertEqual(ma.with_headline("no markers", r), "no markers")

  def test_the_readme_headline_is_current(self):
    r = ma.load_records()
    readme = ma.README.read_text(encoding="utf-8")
    self.assertIn(ma.HEADLINE_BEGIN, readme)
    self.assertEqual(ma.with_headline(readme, r), readme)

  def test_check_detects_staleness(self):
    with tempfile.TemporaryDirectory() as d:
      out = Path(d)
      self.assertEqual(ma.main(["--out", str(out)]), 0)
      figs = ma.render_all()
      for n in ma.NAMES:
        self.assertEqual((out / n).read_text(encoding="utf-8"), figs[n])
      (out / "hero.svg").write_text("stale", encoding="utf-8")
      stale = [n for n in ma.NAMES if (out / n).read_text(encoding="utf-8") != figs[n]]
      self.assertEqual(stale, ["hero.svg"])

  def test_committed_figures_are_current(self):
    self.assertEqual(ma.main(["--check"]), 0)


if __name__ == "__main__":
  unittest.main()
