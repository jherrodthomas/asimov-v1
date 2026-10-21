#!/usr/bin/env python3
"""Tests for check_decisions.py and build_inbox.py."""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_inbox  # noqa: E402
import check_decisions as cd  # noqa: E402

BASE = {
  "id": "DQ-900", "question": "Q?", "context": "Why.", "reversibility": "easy", "blocks": "x",
  "gate": "G1", "asked": "2026-10-14", "status": "open",
  "options": [{"key": "A", "title": "a", "detail": "da", "recommended": True},
              {"key": "B", "title": "b", "detail": "db"}],
}


def entry(**kw) -> dict:
  d = copy.deepcopy(BASE)
  d.update(kw)
  return d


def errors(d: dict) -> list[str]:
  return cd.check([d], HERE)


class Queue(unittest.TestCase):
  def test_queued_needs_no_asked_or_gate(self):
    d = entry(status="queued")
    del d["asked"]
    del d["gate"]
    self.assertEqual(errors(d), [])

  def test_open_still_needs_asked(self):
    d = entry()
    del d["asked"]
    self.assertTrue(any("missing asked" in e for e in errors(d)))

  def test_decider_and_after(self):
    self.assertTrue(any("decider" in e for e in errors(entry(decider="bot"))))
    self.assertTrue(any("unknown decision DQ-999" in e for e in errors(entry(after=["DQ-999"]))))

  def test_queued_entries_are_listed_not_carded(self):
    page = build_inbox.build([entry(), entry(id="DQ-901", status="queued", decider="claude")], HERE)
    reg = page.split("const REG = ", 1)[1].split(";\n", 1)[0]
    self.assertIn("DQ-900", reg)
    self.assertNotIn("DQ-901", reg)
    self.assertIn('"id": "DQ-901"', page.split("const QUEUE = ", 1)[1].split(";\n", 1)[0])


class Register(unittest.TestCase):
  def test_register_is_clean(self):
    self.assertEqual(cd.check(cd.load(), HERE), [])

  def test_ids_unique_and_shaped(self):
    self.assertTrue(any("duplicate" in e for e in cd.check([entry(), entry()], HERE)))
    self.assertTrue(errors(entry(id="Q1")))

  def test_exactly_one_recommendation(self):
    opts = [{"key": "A", "title": "a", "detail": "d", "recommended": True},
            {"key": "B", "title": "b", "detail": "d", "recommended": True}]
    self.assertTrue(any("exactly one" in e for e in errors(entry(options=opts))))

  def test_proceed_after_only_on_easy(self):
    self.assertEqual(errors(entry(proceed_after="2026-10-15")), [])
    self.assertTrue(any("only on easy" in e for e in errors(entry(reversibility="hard", proceed_after="2026-10-15"))))

  def test_hard_is_never_assumed(self):
    d = entry(reversibility="hard", status="assumed", answer={"choice": "A", "via": "assumed", "at": "2026-10-15"})
    self.assertTrue(any("only easy" in e for e in errors(d)))

  def test_assumed_takes_the_recommendation_after_the_date(self):
    ok = entry(proceed_after="2026-10-15", status="assumed", answer={"choice": "A", "via": "assumed", "at": "2026-10-15"})
    self.assertEqual(errors(ok), [])
    wrong = entry(proceed_after="2026-10-15", status="assumed", answer={"choice": "B", "via": "assumed", "at": "2026-10-15"})
    self.assertTrue(any("recommended" in e for e in errors(wrong)))
    early = entry(proceed_after="2026-10-15", status="assumed", answer={"choice": "A", "via": "assumed", "at": "2026-10-14"})
    self.assertTrue(any("before proceed_after" in e for e in errors(early)))

  def test_answered_needs_the_lead(self):
    d = entry(status="answered", answer={"choice": "A", "via": "assumed", "at": "2026-10-15"}, proceed_after="2026-10-15")
    self.assertTrue(any("from the lead" in e for e in errors(d)))
    self.assertEqual(errors(entry(status="answered", answer={"choice": "B", "via": "inbox", "at": "2026-10-15"})), [])

  def test_other_needs_a_note(self):
    d = entry(status="answered", answer={"choice": "other", "via": "inbox", "at": "2026-10-15"})
    self.assertTrue(any("needs a note" in e for e in errors(d)))

  def test_applied_needs_ref_and_record(self):
    ans = {"choice": "A", "via": "chat", "at": "2026-10-15"}
    self.assertTrue(any("applied.ref" in e for e in errors(entry(status="applied", answer=ans))))
    ok = entry(status="applied", answer=ans, applied={"ref": "abc1234", "record": "WP-M-07 D-14", "at": "2026-10-16"})
    self.assertEqual(errors(ok), [])
    self.assertTrue(any("only status applied" in e for e in errors(entry(applied={"ref": "x", "record": "y"}))))

  def test_open_cannot_carry_an_answer(self):
    self.assertTrue(errors(entry(answer={"choice": "A", "via": "chat", "at": "2026-10-15"})))

  def test_figures_exist(self):
    self.assertTrue(any("not found" in e for e in errors(entry(figure="figures/none.svg", caption="c"))))


class Page(unittest.TestCase):
  def setUp(self):
    self.page = build_inbox.build(cd.load(), HERE)

  def test_every_decision_is_on_the_page(self):
    for d in cd.load():
      self.assertIn(f'"id": "{d["id"]}"', self.page)

  def test_payload_cannot_close_the_script(self):
    body = self.page[self.page.index("const REG"):self.page.index("const REV")]
    self.assertNotIn("</", body.replace("<\\/", ""))

  def test_text_is_escaped_and_bold_converted(self):
    self.assertEqual(build_inbox.inline_md("a <x> **b**"), "a &lt;x&gt; <b>b</b>")

  def test_refs_link_to_github(self):
    self.assertTrue(build_inbox.ref_url("2b06293").endswith("/commit/2b06293"))
    self.assertTrue(build_inbox.ref_url("#72").endswith("/pull/72"))
    self.assertIsNone(build_inbox.ref_url("WP-M-07"))

  def test_page_contract(self):
    self.assertTrue(self.page.startswith("<title>"))
    self.assertNotIn("<html", self.page.lower())
    self.assertIn("d.data()", self.page)


if __name__ == "__main__":
  unittest.main()
