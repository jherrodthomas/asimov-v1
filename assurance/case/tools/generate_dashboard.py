#!/usr/bin/env python3
"""Generate the Living Safety Case dashboard from the records in assurance/case.

Outputs (all deterministic, no timestamps):
  assurance/case/status.json                       machine-readable summary
  docs/assets/assurance/dashboard.svg   metrics card shown in the README
  docs/assets/assurance/lifecycle.svg   lifecycle-area status card
  assurance/README.md, between the assurance-summary markers   the same figures as text
  README.md, between the assurance-headline markers            one-line status strip
  assurance/case/badge.json                        shields.io endpoint for the snapshot button

Usage:
  python3 assurance/case/tools/generate_dashboard.py           # write the outputs
  python3 assurance/case/tools/generate_dashboard.py --check   # fail if any output is out of date

The records are validated first; invalid records produce no output.
"""
from __future__ import annotations

import json
import re
import sys
from html import escape
from pathlib import Path

from caselib import CASE_DIR, REPO_ROOT, load_case, release_status, summarize, validate

ASSET_DIR = REPO_ROOT / "docs" / "assets" / "assurance"
STATUS_JSON = CASE_DIR / "status.json"
BADGE_JSON = CASE_DIR / "badge.json"
REPO_SLUG = "jherrodthomas/asimov-v1"
SNAPSHOT_TAG = "snapshot-latest"
SNAPSHOT_PDF = "Asimov-v1-safety-case.pdf"
BADGE_URL = ("https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2F"
             + REPO_SLUG.replace("/", "%2F") + "%2Fmain%2Fassurance%2Fcase%2Fbadge.json")
SNAPSHOT_URL = f"https://github.com/{REPO_SLUG}/releases/download/{SNAPSHOT_TAG}/{SNAPSHOT_PDF}"
README = REPO_ROOT / "README.md"
ASSURANCE_README = REPO_ROOT / "assurance" / "README.md"
BEGIN = "<!-- BEGIN GENERATED: assurance-summary (assurance/case/tools/generate_dashboard.py) -->"
END = "<!-- END GENERATED: assurance-summary -->"
HEAD_BEGIN = "<!-- BEGIN GENERATED: assurance-headline (assurance/case/tools/generate_dashboard.py) -->"
HEAD_END = "<!-- END GENERATED: assurance-headline -->"

FONT = "Inter, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
C = {
  # light theme, the palette of the README figures
  "bg0": "#FFFFFF", "bg1": "#F3F7F8", "panel": "#EDF2F4", "line": "#D3DDE2",
  "gold": "#D4821A", "gold_hi": "#F2A33A", "gold_lo": "#A8650F",
  "blue": "#1F6FD0", "text": "#122026", "muted": "#4E6A73", "dim": "#8A9AA2",
  "green": "#2C9A58", "red": "#D64535",
}
STATUS_COLOR = {
  "Not Started": C["dim"], "In Progress": C["blue"], "Review Required": C["gold"],
  "Accepted for Defined Baseline": C["green"], "Blocked": C["red"],
}
STATE_COLOR = {"Development": C["blue"], "Under Review": C["gold"], "Evidence Supported": C["green"]}


def _defs(uid: str) -> str:
  return f"""<defs>
    <linearGradient id="{uid}-bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{C['bg0']}"/><stop offset="1" stop-color="{C['bg1']}"/>
    </linearGradient>
    <linearGradient id="{uid}-gold" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{C['gold_lo']}"/><stop offset="0.5" stop-color="{C['gold_hi']}"/><stop offset="1" stop-color="{C['gold_lo']}"/>
    </linearGradient>
  </defs>"""


def _frame(uid: str, w: int, h: int, title: str, desc: str, body: str) -> str:
  return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="{uid}-t {uid}-d">
  <title id="{uid}-t">{escape(title)}</title>
  <desc id="{uid}-d">{escape(desc)}</desc>
  {_defs(uid)}
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="22" fill="url(#{uid}-bg)" stroke="{C['line']}"/>
  <rect x="40" y="0" width="{w - 80}" height="3" fill="url(#{uid}-gold)"/>
  <g font-family="{FONT}">
{body}
  </g>
</svg>
"""


def _text(x: float, y: float, s: str, size: int, fill: str, weight: int = 400, anchor: str = "start", spacing: float = 0) -> str:
  ls = f' letter-spacing="{spacing}"' if spacing else ""
  return f'    <text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{ls}>{escape(s)}</text>'


def _pill(x: float, y: float, label: str, color: str, anchor_right: bool = False, size: int = 14) -> str:
  w = int(len(label) * size * 0.66) + 28
  x0 = x - w if anchor_right else x
  return (f'    <rect x="{x0}" y="{y}" width="{w}" height="{size + 16}" rx="{(size + 16) / 2}" fill="{color}" fill-opacity="0.12" stroke="{color}"/>\n'
          + _text(x0 + w / 2, y + size + 3, label.upper(), size, color, 600, "middle", 1.2))


def _bar(x: float, y: float, w: float, h: float, parts: list[tuple[int, str]], total: int) -> str:
  out = [f'    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="{C["bg0"]}" stroke="{C["line"]}"/>']
  cx = x
  for n, color in parts:
    if not n or not total:
      continue
    seg = w * n / total
    out.append(f'    <rect x="{cx:.1f}" y="{y}" width="{seg:.1f}" height="{h}" fill="{color}"/>')
    cx += seg
  clip = f'<clipPath id="bar{int(x)}{int(y)}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}"/></clipPath>'
  return f"    <defs>{clip}</defs>\n    <g clip-path=\"url(#bar{int(x)}{int(y)})\">\n" + "\n".join(out) + "\n    </g>"


def dashboard_svg(s: dict) -> str:
  w, h = 1000, 600
  state = s["assurance_state"]
  bl = s["baseline"]
  ev, cl, cf = s["evidence"], s["claims"], s["configurations"]
  body = [
    _text(40, 56, "LIVING SAFETY CASE", 15, C["gold"], 700, spacing=3),
    _text(40, 96, "Recorded assurance state", 30, C["text"], 700),
    _text(40, 126, "Every figure is counted from the structured records in assurance/case.", 16, C["muted"]),
    _pill(960, 38, state, STATE_COLOR[state], anchor_right=True, size=15),
    _text(960, 100, f"Baseline {bl['id']} · {bl['source_revision']} · {bl['lifecycle_status'].replace('-', ' ')}", 15, C["muted"], anchor="end"),
    _text(960, 124, f"Records digest {s['records_digest']}", 15, C["dim"], anchor="end"),
  ]
  tiles = [
    (cl["registered"], "Safety claims", "registered in the argument", C["text"]),
    (cl["with_accepted_evidence"], "Claims with accepted", "supporting evidence", C["text"]),
    (ev["registered"], "Evidence items", f"{ev['partial']} drafted · {ev['missing']} missing", C["text"]),
    (ev["awaiting_review"], "Evidence to review", "drafted, not yet accepted", C["text"]),
    (s["actions_open"], "Open actions", "safety-case open items", C["text"]),
    (s["defeaters_open"], "Open defeaters", "known counter-evidence", C["text"]),
    (cf["evaluated"], "Evaluated", "robot configurations", C["text"]),
    (cf["assurance_supported"], "Assurance-supported", "robot configurations", C["text"]),
  ]
  tw, th, gap = 218, 128, 16
  for i, (n, l1, l2, color) in enumerate(tiles):
    x = 40 + (i % 4) * (tw + gap)
    y = 160 + (i // 4) * (th + gap)
    accent = C["gold"] if n == 0 else C["blue"]
    body += [
      f'    <rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="14" fill="{C["panel"]}" stroke="{C["line"]}"/>',
      f'    <rect x="{x}" y="{y + 22}" width="3" height="38" rx="1.5" fill="{accent}"/>',
      _text(x + 22, y + 58, str(n), 44, color, 700),
      _text(x + 22, y + 90, l1, 16, C["text"], 600),
      _text(x + 22, y + 112, l2, 14, C["muted"]),
    ]
  y = 460
  total = ev["registered"]
  body += [
    _text(40, y, "Evidence status", 16, C["text"], 600),
    _text(960, y, f"{total} items", 15, C["muted"], anchor="end"),
    _bar(40, y + 16, 920, 14, [(ev["available"], C["green"]), (ev["partial"], C["blue"]), (ev["missing"], C["dim"])], total),
  ]
  lx = 40
  legend = (
    ("Available and accepted", ev["available"], C["green"]),
    ("Drafted (partial)", ev["partial"], C["blue"]),
    ("Not yet performed", ev["missing"], C["dim"]),
  )
  for label, n, color in legend:
    body += [f'    <rect x="{lx}" y="{y + 46}" width="12" height="12" rx="3" fill="{color}"/>', _text(lx + 20, y + 57, f"{label}  {n}", 15, C["muted"])]
    lx += 300
  disclaimer = "Represents recorded engineering evidence and review state. Not a certification or approval for unsupervised operation."
  body.append(_text(40, 568, disclaimer, 14, C["dim"]))
  desc = " ".join([
    f"Assurance state {state}. Baseline {bl['id']} at {bl['source_revision']}.",
    f"{cl['registered']} safety claims registered, {cl['with_accepted_evidence']} with accepted supporting evidence.",
    f"{ev['registered']} evidence items: {ev['available']} available, {ev['partial']} partial, {ev['missing']} missing;",
    f"{ev['awaiting_review']} require review.",
    f"{s['actions_open']} open assurance actions, {s['defeaters_open']} open defeaters.",
    f"{cf['evaluated']} evaluated configuration(s), {cf['assurance_supported']} assurance-supported.",
  ])
  return _frame("dash", w, h, "Asimov v1 assurance Living Safety Case dashboard", desc, "\n".join(body))


def lifecycle_svg(s: dict) -> str:
  w, h = 1000, 420
  body = [
    _text(40, 56, "LIFECYCLE AREAS", 15, C["gold"], 700, spacing=3),
    _text(40, 94, "Status by engineering area", 28, C["text"], 700),
    _text(960, 94, "Derived from evidence status and review state", 15, C["muted"], anchor="end"),
  ]
  cw, ch, gap = 296, 130, 16
  for i, a in enumerate(s["lifecycle_areas"]):
    x = 40 + (i % 3) * (cw + gap)
    y = 124 + (i // 3) * (ch + gap)
    color = STATUS_COLOR[a["status"]]
    body += [
      f'    <rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="14" fill="{C["panel"]}" stroke="{C["line"]}"/>',
      _text(x + 22, y + 36, f"{i + 1:02d}", 15, C["gold"], 700, spacing=1),
      _text(x + 56, y + 36, a["title"], 18, C["text"], 600),
      _pill(x + 22, y + 52, a["status"], color, size=12),
      _bar(x + 22, y + 94, cw - 44, 8, [(a["available"], C["green"]), (a["partial"], C["blue"]), (a["missing"], C["dim"])], a["evidence"]),
      _text(x + 22, y + 120, f"{a['partial']} drafted · {a['missing']} missing", 13, C["muted"]),
      _text(x + cw - 22, y + 120, f"{a['accepted']} of {a['evidence']} accepted", 13, C["muted"], anchor="end"),
    ]
  desc = "; ".join(f"{a['title']}: {a['status']} ({a['evidence']} evidence items, {a['partial']} drafted, {a['missing']} missing, {a['accepted']} accepted)"
                   for a in s["lifecycle_areas"])
  return _frame("life", w, h, "Asimov v1 assurance lifecycle areas", desc, "\n".join(body))


def readme_block(s: dict) -> str:
  ev, cl, cf = s["evidence"], s["claims"], s["configurations"]
  bl = s["baseline"]
  rows = [
    ("Assurance state", s["assurance_state"]),
    ("Engineering baseline", f"`{bl['id']}` at `{bl['source_revision']}` ({bl['lifecycle_status'].replace('-', ' ')})"),
    ("Registered safety claims", f"{cl['registered']}"),
    ("Claims with accepted supporting evidence", f"{cl['with_accepted_evidence']}"),
    ("Registered evidence items", f"{ev['registered']} ({ev['available']} available, {ev['partial']} drafted, {ev['missing']} not yet performed)"),
    ("Evidence requiring review", f"{ev['awaiting_review']}"),
    ("Open assurance actions", f"{s['actions_open']}"),
    ("Open defeaters (known counter-evidence)", f"{s['defeaters_open']}"),
    ("Evaluated configurations", f"{cf['evaluated']}"),
    ("Assurance-supported configurations", f"{cf['assurance_supported']}"),
    ("Records digest", f"`{s['records_digest']}`"),
  ]
  lines = [BEGIN, "", "| Indicator | Recorded value |", "|---|---|"] + [f"| {k} | {v} |" for k, v in rows] + [""]
  lines += ["| Lifecycle area | Status | Evidence (drafted / missing / accepted) |", "|---|---|---|"]
  lines += [f"| {a['title']} | {a['status']} | {a['evidence']} ({a['partial']} / {a['missing']} / {a['accepted']}) |" for a in s["lifecycle_areas"]]
  lines += ["", END]
  return "\n".join(lines)


def headline_block(s: dict) -> str:
  ev, cl = s["evidence"], s["claims"]
  bl = s["baseline"]
  line = (f"**{s['assurance_state']}** · baseline `{bl['id']}` at `{bl['source_revision']}` · "
          f"{cl['registered']} claims ({cl['with_accepted_evidence']} with accepted evidence) · "
          f"{ev['registered']} evidence items ({ev['accepted']} accepted) · "
          f"{s['defeaters_open']} open defeaters · records digest `{s['records_digest']}`")
  return "\n".join([HEAD_BEGIN, "", line, "", HEAD_END])


def badge_json(s: dict) -> str:
  rs = release_status(s)
  bl = s["baseline"]
  badge = {"schemaVersion": 1, "label": "⬇ safety case", "message": f"{rs['label']} · {rs['detail']} · {bl['id']}",
           "color": rs["color"], "labelColor": "334155"}
  return json.dumps(badge, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _replace(text: str, begin: str, end: str, block: str) -> str:
  if begin in text and end in text:
    pre, rest = text.split(begin, 1)
    text = pre + block + rest.split(end, 1)[1]
  return text


def outputs(s: dict) -> dict[Path, str]:
  readme = README.read_text(encoding="utf-8")
  readme = _replace(readme, HEAD_BEGIN, HEAD_END, headline_block(s))
  readme = _replace(readme, BEGIN, END, readme_block(s))
  assurance_readme = _replace(ASSURANCE_README.read_text(encoding="utf-8"), BEGIN, END, readme_block(s))
  return {
    STATUS_JSON: json.dumps(s, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
    BADGE_JSON: badge_json(s),
    ASSET_DIR / "dashboard.svg": dashboard_svg(s),
    ASSET_DIR / "lifecycle.svg": lifecycle_svg(s),
    README: readme,
    ASSURANCE_README: assurance_readme,
  }


def main(argv: list[str]) -> int:
  check = "--check" in argv
  case = load_case()
  rep = validate(case)
  if rep.errors:
    for e in rep.errors:
      print(f"ERROR {e}")
    print("FAIL: records are invalid; run assurance/case/tools/validate.py and fix them first")
    return 1
  stale = []
  for path, content in outputs(summarize(case)).items():
    current = path.read_text(encoding="utf-8") if path.exists() else None
    if current == content:
      continue
    if check:
      stale.append(path.relative_to(REPO_ROOT).as_posix())
    else:
      path.parent.mkdir(parents=True, exist_ok=True)
      path.write_text(content, encoding="utf-8")
      print(f"wrote {path.relative_to(REPO_ROOT).as_posix()}")
  if stale:
    print("FAIL: generated outputs are out of date: " + ", ".join(stale))
    print("Run: python3 assurance/case/tools/generate_dashboard.py, then commit the result")
    return 1
  print("OK: dashboard outputs match the records" if check else "OK: dashboard generated")
  return 0


if __name__ == "__main__":
  sys.exit(main(sys.argv[1:]))
