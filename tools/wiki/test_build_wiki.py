#!/usr/bin/env python3
"""Unit tests for build_wiki.py and a check of the real wiki/ folder."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_wiki

VALUES = {"REPO": "o/r", "BRANCH": "b", "SYNC_COMMIT": "abc1234", "SYNC_DATE": "2026-10-20"}


def make_wiki(tmp: Path, files: dict[str, str]) -> tuple[Path, Path]:
  root = tmp / "repo"
  src = root / "wiki"
  src.mkdir(parents=True)
  (root / "README.md").write_text("# repo\n", encoding="utf-8")
  (root / "assurance").mkdir()
  (root / "assurance" / "README.md").write_text("# assurance\n", encoding="utf-8")
  for name, text in files.items():
    (src / name).write_text(text, encoding="utf-8")
  return root, src


class RewriteTests(unittest.TestCase):
  def test_page_links_lose_their_extension(self):
    with tempfile.TemporaryDirectory() as d:
      root, src = make_wiki(Path(d), {"Home.md": "", "Glossary.md": "", "_Sidebar.md": ""})
      problems: list[str] = []
      out = build_wiki.rewrite("see [the glossary](Glossary.md#codes)", src / "Home.md", src, root, VALUES, problems)
      self.assertEqual(out, "see [the glossary](Glossary#codes)")
      self.assertEqual(problems, [])

  def test_repository_links_become_absolute(self):
    with tempfile.TemporaryDirectory() as d:
      root, src = make_wiki(Path(d), {"Home.md": "", "_Sidebar.md": ""})
      problems: list[str] = []
      out = build_wiki.rewrite("[a](../assurance/README.md#x) [d](../assurance)", src / "Home.md", src, root, VALUES, problems)
      self.assertEqual(out, "[a](https://github.com/o/r/blob/b/assurance/README.md#x) [d](https://github.com/o/r/tree/b/assurance)")
      self.assertEqual(problems, [])

  def test_repository_images_use_the_raw_address(self):
    with tempfile.TemporaryDirectory() as d:
      root, src = make_wiki(Path(d), {"Home.md": "", "_Sidebar.md": ""})
      (root / "docs").mkdir()
      (root / "docs" / "fig.svg").write_text("<svg/>", encoding="utf-8")
      problems: list[str] = []
      out = build_wiki.rewrite("![A figure](../docs/fig.svg) and [the file](../docs/fig.svg)", src / "Home.md", src, root, VALUES, problems)
      self.assertEqual(out, "![A figure](https://raw.githubusercontent.com/o/r/b/docs/fig.svg) and [the file](https://github.com/o/r/blob/b/docs/fig.svg)")
      self.assertEqual(problems, [])

  def test_generated_figures_are_left_alone(self):
    with tempfile.TemporaryDirectory() as d:
      root, src = make_wiki(Path(d), {"Home.md": "", "_Sidebar.md": ""})
      problems: list[str] = []
      out = build_wiki.rewrite("![x](register-status.svg)", src / "Home.md", src, root, VALUES, problems)
      self.assertEqual(out, "![x](register-status.svg)")
      self.assertEqual(problems, [])

  def test_missing_targets_are_reported(self):
    with tempfile.TemporaryDirectory() as d:
      root, src = make_wiki(Path(d), {"Home.md": "", "_Sidebar.md": ""})
      problems: list[str] = []
      build_wiki.rewrite("[p](Nope.md) [r](../nope.md) [x](nope)", src / "Home.md", src, root, VALUES, problems)
      self.assertEqual(len(problems), 3)
      self.assertIn("page link target does not exist: Nope.md", problems[0])
      self.assertIn("repository link target does not exist: nope.md", problems[1])
      self.assertIn("neither a page", problems[2])

  def test_urls_anchors_and_placeholders(self):
    with tempfile.TemporaryDirectory() as d:
      root, src = make_wiki(Path(d), {"Home.md": "", "_Sidebar.md": ""})
      problems: list[str] = []
      out = build_wiki.rewrite("[u](https://example.org/a.md) [s](#top) {{REPO}}@{{SYNC_COMMIT}} {{SYNC_DATE}} {{BRANCH}}",
                               src / "Home.md", src, root, VALUES, problems)
      self.assertEqual(out, "[u](https://example.org/a.md) [s](#top) o/r@abc1234 2026-10-20 b")
      self.assertEqual(problems, [])


class BuildTests(unittest.TestCase):
  def test_build_writes_pages_and_skips_readme(self):
    with tempfile.TemporaryDirectory() as d:
      root, src = make_wiki(Path(d), {
        "Home.md": "[g](Glossary.md) [r](../README.md)",
        "Glossary.md": "{{SYNC_COMMIT}}",
        "_Sidebar.md": "[Home](Home.md)\n[Glossary](Glossary.md)",
        "_Footer.md": "{{SYNC_DATE}}",
        "README.md": "folder notes",
      })
      out = Path(d) / "out"
      problems = build_wiki.build(src, out, root, repo="o/r", branch="b", commit="abc1234def", date="2026-10-20")
      self.assertEqual(problems, [])
      self.assertEqual(sorted(p.name for p in out.iterdir()), ["Glossary.md", "Home.md", "_Footer.md", "_Sidebar.md"])
      self.assertEqual((out / "Home.md").read_text(), "[g](Glossary) [r](https://github.com/o/r/blob/b/README.md)")
      self.assertEqual((out / "Glossary.md").read_text(), "abc1234")
      self.assertEqual((out / "_Footer.md").read_text(), "2026-10-20")

  def test_unlinked_page_and_missing_home_are_problems(self):
    with tempfile.TemporaryDirectory() as d:
      root, src = make_wiki(Path(d), {"Orphan.md": "", "_Sidebar.md": ""})
      out = Path(d) / "out"
      problems = build_wiki.build(src, out, root)
      self.assertIn("Home.md is missing", problems)
      self.assertIn("Orphan.md: not linked from _Sidebar.md", problems)
      self.assertFalse(out.exists(), "nothing is written when a check fails")


class MergeLogTests(unittest.TestCase):
  def test_no_git_checkout_gives_the_fallback_text(self):
    with tempfile.TemporaryDirectory() as d:
      self.assertEqual(build_wiki.git_merges(Path(d)), [])
      self.assertEqual(build_wiki.render_merge_log([], "o/r"), build_wiki.NO_MERGE_LOG)

  def test_entries_render_grouped_by_date_newest_first(self):
    entries = [("2026-10-20", 3, "Build out the record", "7c00aa4"), ("2026-10-20", 2, "Add the wiki", "4d3fdac"),
               ("2026-10-19", 1, "Gap assessment", "abc1234")]
    out = build_wiki.render_merge_log(entries, "o/r")
    self.assertEqual(out.splitlines(), [
      "### 2026-10-20", "",
      "- [#3](https://github.com/o/r/pull/3) Build out the record",
      "- [#2](https://github.com/o/r/pull/2) Add the wiki", "",
      "### 2026-10-19", "",
      "- [#1](https://github.com/o/r/pull/1) Gap assessment",
    ])

  def test_only_pull_request_merges_are_listed(self):
    import subprocess
    with tempfile.TemporaryDirectory() as d:
      root = Path(d)
      env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@x", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@x",
             "GIT_AUTHOR_DATE": "2026-10-20T00:00:00Z", "GIT_COMMITTER_DATE": "2026-10-20T00:00:00Z", "PATH": "/usr/bin:/bin"}

      def git(*args):
        subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, env=env)

      def commit(msg):
        (root / "f").write_text(msg)
        git("add", "f")
        git("commit", "-q", "-m", msg)

      git("init", "-q", "-b", "main")
      commit("base")
      git("checkout", "-q", "-b", "feature")
      commit("work")
      git("checkout", "-q", "main")
      git("merge", "--no-ff", "-q", "-m", "Merge pull request #7 from o/feature\n\nThe PR title", "feature")
      git("checkout", "-q", "-b", "other")
      commit("other work")
      git("checkout", "-q", "main")
      git("merge", "--no-ff", "-q", "-m", "Merge branch 'other' into main", "other")
      self.assertEqual(build_wiki.git_merges(root), [("2026-10-20", 7, "The PR title", build_wiki.git_merges(root)[0][3])])

  def test_merge_log_placeholder_is_filled_from_the_checkout(self):
    with tempfile.TemporaryDirectory() as d:
      root, src = make_wiki(Path(d), {"Home.md": "{{MERGE_LOG}}", "_Sidebar.md": "[Home](Home.md)"})
      out = Path(d) / "out"
      self.assertEqual(build_wiki.build(src, out, root, repo="o/r"), [])
      self.assertEqual((out / "Home.md").read_text(), build_wiki.NO_MERGE_LOG)


class RealWikiTests(unittest.TestCase):
  def test_the_wiki_folder_checks_clean(self):
    self.assertEqual(build_wiki.build(), [])


if __name__ == "__main__":
  unittest.main()
