#!/usr/bin/env python3
"""Tests for check_tables.py, check_links.py and folder_index.py."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_links
import check_tables
import folder_index


class TestCheckTables(unittest.TestCase):
  def test_consistent_table(self):
    self.assertEqual(check_tables.check_text("| A | B |\n|---|---|\n| 1 | 2 |\n", "t"), [])

  def test_missing_cell(self):
    self.assertEqual(check_tables.check_text("| A | B | C |\n|---|---|---|\n| 1 | 2 |\n", "t"),
                     ["t:3: 2 cells, the table header (line 1) has 3"])

  def test_text_after_last_pipe_is_a_cell(self):
    self.assertEqual(check_tables.check_text("| ID | Status |\n|---|---|\n| X-1 | old | new \n", "t"),
                     ["t:3: 3 cells, the table header (line 1) has 2"])

  def test_escaped_pipe_is_not_a_separator(self):
    self.assertEqual(check_tables.check_text("| A | B |\n|---|---|\n| a \\| b | 2 |\n", "t"), [])

  def test_fenced_block_ignored(self):
    self.assertEqual(check_tables.check_text("```\n| a | b |\n| c |\n```\n", "t"), [])

  def test_the_repository_tables_are_consistent(self):
    _, errors = check_tables.check(check_tables.DEFAULT_ROOT)
    self.assertEqual(errors, [])


class TestCheckLinks(unittest.TestCase):
  def test_broken_and_good_links(self):
    with tempfile.TemporaryDirectory() as d:
      root = Path(d)
      (root / "a.md").write_text("[ok](b.md) [bad](nope.md) [url](https://x) [anchor](#x) `[code](x.md)`\n<img src=\"b.md\"> <img src=\"missing.svg\">\n```\n[fence](zzz.md)\n```\n", encoding="utf-8")
      (root / "b.md").write_text("", encoding="utf-8")
      total, broken = check_links.check(root)
      self.assertEqual(total, 4)
      self.assertEqual(broken, ["a.md:1: nope.md", "a.md:2: missing.svg"])

  def test_the_repository_has_no_broken_links(self):
    _, broken = check_links.check(check_links.DEFAULT_ROOT)
    self.assertEqual(broken, [])


class TestFolderIndex(unittest.TestCase):
  def test_register_rows_are_grouped_by_folder(self):
    rows = folder_index.load_rows()
    self.assertIn("02-concept", rows)
    self.assertTrue(all(len(r) == 5 for r in rows["02-concept"]))
    self.assertEqual(rows["02-concept"][0][0], "WP-C-01")

  def test_committed_indexes_are_current(self):
    self.assertEqual(folder_index.main(["--check"]), 0)


if __name__ == "__main__":
  unittest.main()
