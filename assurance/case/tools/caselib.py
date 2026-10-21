"""Shared loading, validation and summary logic for the Living Safety Case records.

The records live in assurance/case/<kind dir>/*.yaml and use the restricted YAML subset of
assurance/case/README.md (subsetyaml.py). They are parsed with the same subset parser as the trace
data (never PyYAML), so the result does not depend on what is installed.

Nothing in this module changes a review or lifecycle state. It only reports what the records say,
and refuses records that claim acceptance without a recorded review.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
CASE_DIR = TOOLS_DIR.parent
ASSURANCE_DIR = CASE_DIR.parent
REPO_ROOT = ASSURANCE_DIR.parent
SCHEMA_PATH = CASE_DIR / "schema" / "case-schema.json"
TRACE_ITEMS_DIR = ASSURANCE_DIR / "trace" / "items"
SAFETY_CASE_MD = ASSURANCE_DIR / "10-safety-case" / "WP-K-01-safety-case.md"
GATES_DIR = ASSURANCE_DIR / "10-safety-case" / "gates"

from subsetyaml import _load_subset

DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
REV_RE = re.compile(r"^[0-9a-f]{7,40}$")
ID_TOKEN_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")

AREA_TITLES = {
  "safety-management": "Safety Management",
  "hazard-analysis": "Hazard Analysis",
  "safety-concepts": "Safety Concepts",
  "technical-implementation": "Technical Implementation",
  "verification-validation": "Verification and Validation",
  "safety-case-review": "Safety Case and Review",
}


@dataclass
class Report:
  errors: list[str] = field(default_factory=list)

  def err(self, check: str, where: str, msg: str) -> None:
    self.errors.append(f"[{check}] {where}: {msg}")


@dataclass
class Case:
  schema: dict
  records: dict[str, dict]          # id -> record (with "_file")
  trace_ids: dict[str, str]         # trace item id -> kind
  report: Report

  def of_kind(self, kind: str) -> list[dict]:
    return [r for r in self.records.values() if r["kind"] == kind]


def rel(path: Path) -> str:
  return path.relative_to(REPO_ROOT).as_posix()


def load_case() -> Case:
  rep = Report()
  schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
  records: dict[str, dict] = {}
  for kind, spec in schema["kinds"].items():
    for path in sorted((CASE_DIR / spec["dir"]).glob("*.yaml")):
      try:
        items = _load_subset(path.read_text(encoding="utf-8"))
      except ValueError as e:
        rep.err("V1", rel(path), f"parse error: {e}")
        continue
      for it in items:
        it["_file"] = rel(path)
        iid = it.get("id")
        if it.get("kind") != kind:
          rep.err("V1", f"{rel(path)}:{iid}", f"kind {it.get('kind')!r} does not belong in {spec['dir']}/ (expected {kind!r})")
          continue
        if not isinstance(iid, str) or not re.match(spec["id_pattern"], iid):
          rep.err("V2", rel(path), f"id {iid!r} does not match {spec['id_pattern']}")
          continue
        if iid in records:
          rep.err("V2", rel(path), f"duplicate id {iid} (also in {records[iid]['_file']})")
          continue
        records[iid] = it
  trace_ids: dict[str, str] = {}
  for path in sorted(TRACE_ITEMS_DIR.glob("*.yaml")):
    for it in _load_subset(path.read_text(encoding="utf-8")):
      trace_ids[it["id"]] = it["kind"]
  return Case(schema, records, trace_ids, rep)


# ---------------------------------------------------------------- validation

def _check_fields(case: Case) -> None:
  rep, enums = case.report, case.schema["enums"]
  for iid, r in case.records.items():
    spec = case.schema["kinds"][r["kind"]]
    where = f"{r['_file']}:{iid}"
    allowed = set(spec["fields"]) | {"id", "kind", "_file"}
    for k in r:
      if k not in allowed:
        rep.err("V1", where, f"unknown field {k!r}")
    for k, t in spec["fields"].items():
      if k not in r:
        rep.err("V1", where, f"missing field {k!r}")
        continue
      v = r[k]
      optional = t.endswith("?")
      base = t.rstrip("?")
      if v is None:
        if not optional:
          rep.err("V2", where, f"{k} must not be null")
        continue
      if base == "text" and not (isinstance(v, str) and v.strip()):
        rep.err("V2", where, f"{k} must be a non-empty string")
      elif base == "id" and not (isinstance(v, str) and ID_TOKEN_RE.match(v)):
        rep.err("V2", where, f"{k} must be one identifier, got {v!r}")
      elif base == "ids":
        if not isinstance(v, list) or not all(isinstance(x, str) and ID_TOKEN_RE.match(x) for x in v):
          rep.err("V2", where, f"{k} must be a list of identifiers, got {v!r}")
        elif len(set(v)) != len(v):
          rep.err("V2", where, f"{k} lists an identifier twice")
      elif base == "date" and not (isinstance(v, str) and DATE_RE.match(v)):
        rep.err("V2", where, f"{k} must be a quoted YYYY-MM-DD date, got {v!r}")
      elif base == "rev" and not (isinstance(v, str) and REV_RE.match(v)):
        rep.err("V2", where, f"{k} must be a quoted git revision, got {v!r}")
      elif base.startswith("enum:") and v not in enums[base[5:]]:
        rep.err("V2", where, f"{k}={v!r} not in {enums[base[5:]]}")


def _check_refs(case: Case) -> None:
  rep, prefixes = case.report, case.schema["trace_prefixes"]
  for iid, r in case.records.items():
    where = f"{r['_file']}:{iid}"
    for k, targets in case.schema["kinds"][r["kind"]]["refs"].items():
      v = r.get(k)
      for ref in (v if isinstance(v, list) else [v] if isinstance(v, str) else []):
        ok = False
        for t in targets:
          if t.startswith("trace:"):
            allowed = prefixes[t[6:]]
            ok = ok or (ref in case.trace_ids and ref.split("-")[0] in allowed)
          else:
            ok = ok or (ref in case.records and case.records[ref]["kind"] == t)
        if not ok:
          rep.err("V3", where, f"{k} -> {ref} does not resolve to {' or '.join(targets)}")


def _check_structure(case: Case) -> None:
  rep = case.report
  claims = {r["id"]: r for r in case.of_kind("claim")}
  roots = [c for c in claims.values() if c.get("parent") is None]
  if len(roots) != 1:
    rep.err("V8", "claims", f"expected exactly one top-level claim, found {[c['id'] for c in roots]}")
  for cid, c in claims.items():
    seen, cur = set(), c
    while cur is not None and cur.get("parent"):
      if cur["id"] in seen:
        rep.err("V8", cid, "parent chain has a cycle")
        break
      seen.add(cur["id"])
      cur = claims.get(cur["parent"])
    arg = case.records.get(c.get("argument") or "")
    if c.get("parent") and arg is not None and arg.get("claim") != c["parent"]:
      rep.err("V4", f"{c['_file']}:{cid}", f"argument {arg['id']} argues {arg.get('claim')}, but parent is {c['parent']}")
  for a in case.of_kind("argument"):
    expected = sorted(cid for cid, c in claims.items() if c.get("argument") == a["id"])
    if sorted(a.get("subclaims") or []) != expected:
      rep.err("V4", f"{a['_file']}:{a['id']}", f"subclaims {a.get('subclaims')} differ from claims that cite it {expected}")
  pairs = [("evidence_refs", "evidence"), ("defeaters", "defeater")]
  for field_name, kind in pairs:
    for cid, c in claims.items():
      for ref in c.get(field_name) or []:
        other = case.records.get(ref)
        if other and other["kind"] == kind and cid not in (other.get("related_claims") or []):
          rep.err("V4", f"{c['_file']}:{cid}", f"{field_name} lists {ref}, but {ref}.related_claims does not list {cid}")
    for o in case.of_kind(kind):
      for cid in o.get("related_claims") or []:
        if cid in claims and o["id"] not in (claims[cid].get(field_name) or []):
          rep.err("V4", f"{o['_file']}:{o['id']}", f"related_claims lists {cid}, but {cid}.{field_name} does not list {o['id']}")


def _check_evidence_locations(case: Case) -> None:
  for e in case.of_kind("evidence"):
    loc = e.get("location")
    if isinstance(loc, str) and not (REPO_ROOT / loc.split("#")[0]).exists():
      case.report.err("V5", f"{e['_file']}:{e['id']}", f"location {loc!r} does not exist in the repository")


def _accepted_review_lists(case: Case, obj: dict) -> bool:
  rev = case.records.get(obj.get("review_ref") or "")
  return bool(rev and rev["kind"] == "review" and rev.get("outcome") == "accepted"
              and obj["id"] in (rev.get("reviewed_objects") or []) and rev.get("baseline") == obj.get("baseline"))


def _check_acceptance_rules(case: Case) -> None:
  """Acceptance needs a recorded review; nothing is accepted because a file exists or CI passed."""
  rep = case.report
  for r in case.records.values():
    if r.get("review_state") == "accepted":
      where = f"{r['_file']}:{r['id']}"
      if not (r.get("reviewer") and r.get("review_date") and r.get("review_ref")):
        rep.err("V6", where, "review_state accepted needs reviewer, review_date and review_ref")
      elif not _accepted_review_lists(case, r):
        rep.err("V6", where, f"review_ref {r.get('review_ref')} is not an accepted review of this object at baseline {r.get('baseline')}")
  for e in case.of_kind("evidence"):
    where = f"{e['_file']}:{e['id']}"
    if e.get("evidence_status") == "available" and e.get("review_state") != "accepted":
      rep.err("V6", where, "evidence_status available means performed and approved (WP-K-01 §6); review_state must be accepted")
    if e.get("evidence_status") == "missing" and e.get("review_state") == "accepted":
      rep.err("V6", where, "missing evidence cannot be accepted")
  for c in case.of_kind("claim"):
    if c.get("lifecycle_status") != "accepted":
      continue
    where = f"{c['_file']}:{c['id']}"
    if c.get("review_state") != "accepted":
      rep.err("V6", where, "an accepted claim needs review_state accepted")
    for ref in c.get("evidence_refs") or []:
      ev = case.records.get(ref, {})
      if ev.get("evidence_status") != "available" or ev.get("review_state") != "accepted":
        rep.err("V6", where, f"accepted claim relies on {ref}, which is not available and accepted")
    for ref in c.get("defeaters") or []:
      if case.records.get(ref, {}).get("lifecycle_status") == "open":
        rep.err("V6", where, f"accepted claim has open defeater {ref}")
    for child in case.of_kind("claim"):
      if child.get("parent") == c["id"] and child.get("lifecycle_status") != "accepted":
        rep.err("V6", where, f"accepted claim has sub-claim {child['id']} that is not accepted")
    if not (c.get("evidence_refs") or any(x.get("parent") == c["id"] for x in case.of_kind("claim"))):
      rep.err("V6", where, "an accepted claim needs evidence or accepted sub-claims")
  for cfg in case.of_kind("configuration"):
    if cfg.get("classification") != "assurance-supported":
      continue
    where = f"{cfg['_file']}:{cfg['id']}"
    if cfg.get("review_state") != "accepted":
      rep.err("V6", where, "assurance-supported needs review_state accepted")
    if not any(c.get("configuration") == cfg["id"] and c.get("lifecycle_status") == "accepted" for c in case.of_kind("claim")):
      rep.err("V6", where, "assurance-supported needs at least one accepted claim for this configuration")


def _check_against_safety_case(case: Case) -> None:
  """X3: the evidence, defeater and open-item tables of WP-K-01 match the records."""
  rep = case.report
  text = SAFETY_CASE_MD.read_text(encoding="utf-8")
  md_sn = set(re.findall(r"^\| (Sn-[0-9]+) \|", text, re.M))
  md_df = set(re.findall(r"^\| (DF-[0-9]+) \|", text, re.M))
  md_oi = set(re.findall(r"^\| (OI-[0-9]+) \|", text.split("## 10. Open items")[-1], re.M))
  rec_sn = {r["id"] for r in case.of_kind("evidence")}
  rec_df = {r["id"] for r in case.of_kind("defeater")}
  rec_oi = {r.get("source_ref") for r in case.of_kind("action") if r.get("source") == "WP-K-01"}
  for name, md, recs in (("evidence", md_sn, rec_sn), ("defeater", md_df, rec_df), ("action", md_oi, rec_oi)):
    for x in sorted(md - recs):
      rep.err("X3", "WP-K-01", f"{x} is in WP-K-01 but has no {name} record")
    for x in sorted(recs - md):
      rep.err("X3", "WP-K-01", f"{name} record {x} is not in WP-K-01")
  for row in re.findall(r"^\| (Sn-[0-9]+) \|.*\| (Available|Partial|Missing) \|[^|]*\|$", text, re.M):
    sn, status = row
    if sn in case.records and case.records[sn].get("evidence_status") != status.lower():
      rep.err("X3", sn, f"evidence_status {case.records[sn].get('evidence_status')} differs from WP-K-01 ({status})")
  m = re.search(r"\*\*Available ([0-9]+), Partial ([0-9]+), Missing ([0-9]+)\*\* \(([0-9]+) evidence items\)", text)
  if m:
    counts = {s: sum(1 for e in case.of_kind("evidence") if e.get("evidence_status") == s) for s in ("available", "partial", "missing")}
    stated = dict(zip(("available", "partial", "missing", "total"), map(int, m.groups()), strict=True))
    if [counts["available"], counts["partial"], counts["missing"], len(rec_sn)] != [stated["available"], stated["partial"], stated["missing"], stated["total"]]:
      rep.err("X3", "WP-K-01 §6", f"summary line {stated} differs from records {counts} total {len(rec_sn)}")


def validate(case: Case) -> Report:
  _check_fields(case)
  _check_refs(case)
  _check_structure(case)
  _check_evidence_locations(case)
  _check_acceptance_rules(case)
  _check_against_safety_case(case)
  return case.report


# ---------------------------------------------------------------- summary



def records_digest() -> str:
  h = hashlib.sha256()
  # distribution.yaml records who got a copy, not what the case says, so issuing a copy does not change the digest
  paths = [SCHEMA_PATH] + sorted(p for p in CASE_DIR.rglob("*.yaml") if p.name != "distribution.yaml")
  for p in paths:
    h.update(rel(p).encode())
    h.update(b"\0")
    h.update(p.read_bytes())
  return h.hexdigest()[:12]


GATE_RECORD_RE = re.compile(r"^(G[0-6])-([0-9]{4}-[0-9]{2}-[0-9]{2})\.md$")
OUTCOME_RE = re.compile(r"-\s*\[[xX]\]\s*(Pass with conditions|Pass|Fail)")


def gate_records() -> list[dict]:
  """Gate review records G<n>-<date>.md (WP-K gates README), with the ticked outcome, if any."""
  out = []
  for path in sorted(GATES_DIR.glob("G*-*.md")) if GATES_DIR.exists() else []:
    m = GATE_RECORD_RE.match(path.name)
    if not m:
      continue
    ticked = OUTCOME_RE.findall(path.read_text(encoding="utf-8"))
    outcome = ticked[0].lower() if len(ticked) == 1 else "not decided"
    out.append({"gate": m.group(1), "date": m.group(2), "record": rel(path), "outcome": outcome})
  return out


def release_status(s: dict) -> dict:
  """The one status line every generated view uses. Approved only with a passed gate and a frozen, tagged baseline."""
  passed = sorted({g["gate"] for g in s["gates"]["records"] if g["outcome"].startswith("pass")})
  bl = s["baseline"] or {}
  approved = bool(passed) and bl.get("lifecycle_status") == "frozen" and bool(bl.get("tag"))
  if approved:
    return {"approved": True, "label": "APPROVED", "detail": f"{passed[-1]} passed", "color": "2e9e6a"}
  return {"approved": False, "label": "DRAFT", "detail": f"{passed[-1]} passed, baseline not frozen" if passed else "no gate passed",
          "color": "c2410c"}


def area_status(items: list[dict], claims: list[dict]) -> str:
  if any(c.get("lifecycle_status") == "blocked" and set(c.get("evidence_refs") or []) & {e["id"] for e in items} for c in claims):
    return "Blocked"
  if not items or all(e["evidence_status"] == "missing" for e in items):
    return "Not Started"
  if all(e["evidence_status"] == "available" and e["review_state"] == "accepted" for e in items):
    return "Accepted for Defined Baseline"
  if all(e["evidence_status"] != "missing" and e["review_state"] in ("in-review", "accepted") for e in items):
    return "Review Required"
  return "In Progress"


def summarize(case: Case) -> dict:
  claims = case.of_kind("claim")
  evidence = case.of_kind("evidence")
  configs = case.of_kind("configuration")
  baselines = sorted(case.of_kind("baseline"), key=lambda b: b["id"])
  supported = [c for c in configs if c["classification"] == "assurance-supported"]
  evaluated = [c for c in configs if c["classification"] in ("fork-evaluated", "assurance-supported")]
  in_review = any(r.get("review_state") == "in-review" for r in case.records.values())
  if supported:
    state = "Evidence Supported"
  elif in_review or case.of_kind("review"):
    state = "Under Review"
  else:
    state = "Development"
  child_parents = {c.get("parent") for c in claims}
  areas = []
  for key, title in AREA_TITLES.items():
    items = [e for e in evidence if e["lifecycle_area"] == key]
    areas.append({
      "id": key,
      "title": title,
      "status": area_status(items, claims),
      "evidence": len(items),
      "available": sum(1 for e in items if e["evidence_status"] == "available"),
      "partial": sum(1 for e in items if e["evidence_status"] == "partial"),
      "missing": sum(1 for e in items if e["evidence_status"] == "missing"),
      "accepted": sum(1 for e in items if e["review_state"] == "accepted"),
    })
  current = baselines[-1] if baselines else None
  return {
    "assurance_state": state,
    "baseline": {"id": current["id"], "source_revision": current["source_revision"], "lifecycle_status": current["lifecycle_status"],
                 "tag": current.get("tag")} if current else None,
    "gates": {"records": gate_records()},
    "records_digest": records_digest(),
    "claims": {
      "registered": len(claims),
      "accepted": sum(1 for c in claims if c["lifecycle_status"] == "accepted"),
      "with_accepted_evidence": sum(1 for c in claims if c.get("evidence_refs") and all(
        case.records[e]["review_state"] == "accepted" for e in c["evidence_refs"])),
      "undeveloped": sum(1 for c in claims if not c.get("evidence_refs") and c["id"] not in child_parents),
    },
    "evidence": {
      "registered": len(evidence),
      "available": sum(1 for e in evidence if e["evidence_status"] == "available"),
      "partial": sum(1 for e in evidence if e["evidence_status"] == "partial"),
      "missing": sum(1 for e in evidence if e["evidence_status"] == "missing"),
      "accepted": sum(1 for e in evidence if e["review_state"] == "accepted"),
      "awaiting_review": sum(1 for e in evidence if e["evidence_status"] != "missing" and e["review_state"] != "accepted"),
    },
    "defeaters_open": sum(1 for d in case.of_kind("defeater") if d["lifecycle_status"] == "open"),
    "actions_open": sum(1 for a in case.of_kind("action") if a["lifecycle_status"] == "open"),
    "reviews": len(case.of_kind("review")),
    "configurations": {
      "evaluated": len(evaluated),
      "assurance_supported": len(supported),
    },
    "lifecycle_areas": areas,
  }
