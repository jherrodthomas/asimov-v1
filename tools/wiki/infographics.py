#!/usr/bin/env python3
"""Render the wiki's infographics as SVG from the records.

Three figures, every number read from the repository at build time so none is ever typed by hand:

  decision-register.svg  the decision register at a glance, from assurance/01-management/decisions/register.yaml:
                         questions by status, the batches of ten, how hard each is to undo, which gate it belongs
                         to, who decides, and how the answers arrived;
  change-path.svg        what a change goes through before it is merged, from the safety-relevant file list
                         (assurance/07-supporting/safety-relevant-paths.txt), the four things a safety-relevant pull
                         request must carry (CONTRIBUTING.md) and the workflows under .github/workflows/ that run on
                         pull requests;
  register-status.svg    the work product register at a glance, from WP-M-00 §3: work products per gate, coloured
                         by status.

build_wiki.py renders them into the built wiki next to the pages at each sync, so they are current by construction
and nothing is committed. `--out DIR` writes them anywhere; `--check DIR` fails when DIR's copies differ from what
the records give now.


Usage: python3 tools/wiki/infographics.py [--out DIR | --check DIR]
"""
from __future__ import annotations

import argparse
import collections
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REGISTER = ROOT / "assurance" / "01-management" / "decisions" / "register.yaml"
PATHS = ROOT / "assurance" / "07-supporting" / "safety-relevant-paths.txt"
WORKFLOWS = ROOT / ".github" / "workflows"
WP_REGISTER = ROOT / "assurance" / "01-management" / "WP-M-00-work-product-register.md"

NAMES = ("decision-register.svg", "change-path.svg", "register-status.svg")

FONT = "'Source Sans 3', 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'IBM Plex Mono', 'SFMono-Regular', Menlo, Consolas, monospace"
C = {
  "bg": "#FFFFFF", "navy": "#E8F0F2", "navy2": "#1E4752", "mid": "#5F8F99", "light": "#B9CFD4",
  "gold": "#F2A33A", "gold_text": "#8A5A0B", "cream": "#FBF3E3", "grey": "#E3E0D8", "panel": "#F4F3EF",
  "ink": "#122026", "muted": "#4E6A73", "line": "#D3DDE2", "white": "#FFFFFF", "on_navy": "#122026",
  "on_navy_muted": "#4E6A73", "gold_hi": "#F2A33A", "cyan": "#0E8C83",
}
W = 1280
H_REGISTER, H_CHANGE, H_STATUS = 640, 780, 520

STATUS_ORDER = ("queued", "open", "answered", "assumed", "applied", "withdrawn")
STATUS_COLOR = {"queued": C["light"], "open": C["gold"], "answered": C["mid"], "assumed": C["cream"],
                "applied": C["navy2"], "withdrawn": C["grey"]}
STATUS_NOTE = {"queued": "written ahead, not yet asked", "open": "asked", "answered": "change pending",
               "assumed": "recommended option taken", "applied": "change made and recorded",
               "withdrawn": "no longer apply"}

CLASS_TEXT = {
  "SR-A": "Safety-related parts of the control system: safety-chain design files, the firmware safety layer, safety parameter sets",
  "SR-Q": "Functional layers that feed hazards or configure limits: Nav2 chain, docking, drivers, scan filters, operator UI, firmware tuning",
  "SR-T": "Build, test, CI, toolchain or dependency configuration that changes evidence or binaries",
}
REQUIREMENTS = (
  ("Rationale.", "What it does and why."),
  ("Impact analysis.", "Which hazards, safety functions, requirements and assumptions it touches. \"None\" is a valid answer, with a reason."),
  ("Verification.", "The tests or analyses that show it is correct, and their results."),
  ("Record updates.", "The affected work products, every generator re-run."),
)
WORKFLOW_NOTE = {
  "assurance": "register, process model, figures, links, tables", "wiki": "pages, links, infographics",
}
WP_STATUS_ORDER = ("S", "D", "R", "A", "B")
WP_STATUS_NAME = {"S": "Skeleton", "D": "Draft", "R": "In review", "A": "Approved", "B": "Baselined"}
WP_STATUS_COLOR = {"S": C["light"], "D": C["gold"], "R": C["mid"], "A": "#5FD38F", "B": C["navy2"]}
GATES = ("G0", "G1", "G2", "G3", "G4", "G5", "G6")


# ================================================================ data

def load_register(path: Path = REGISTER) -> list[dict]:
  import yaml  # type: ignore
  data = yaml.safe_load(path.read_text(encoding="utf-8")) or []
  return [d for d in data if isinstance(d, dict)]


def load_classes(path: Path = PATHS) -> dict[str, int]:
  counts: dict[str, int] = collections.Counter()
  for line in path.read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(SR-[AQT])\s+\S", line)
    if m:
      counts[m.group(1)] += 1
  return dict(counts)


def load_workflows(folder: Path = WORKFLOWS) -> list[tuple[str, bool]]:
  import yaml  # type: ignore
  out = []
  for f in sorted(folder.glob("*.y*ml")):
    data = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
    name = str(data.get("name") or f.stem)
    on = data.get("on", data.get(True, {}))
    keys = set(on.keys()) if isinstance(on, dict) else set(on or [])
    out.append((name, bool(keys & {"pull_request", "pull_request_target"})))
  return out


def load_wp_register(path: Path = WP_REGISTER) -> list[tuple[str, str, str, str]]:
  """(id, folder section, first gate, status) for each row of WP-M-00 §3."""
  out = []
  section = ""
  for line in path.read_text(encoding="utf-8").splitlines():
    m = re.match(r"^### 3\.\d+ (.*?) \(`", line)
    if m:
      section = m.group(1)
    m = re.match(r"^\| \[(WP-[A-Z]-\d\d)\]\([^)]+\) \|", line)
    if m:
      c = [x.strip() for x in line.strip().strip("|").split("|")]
      g = re.match(r"G\d", c[7])
      out.append((m.group(1), section, g.group(0) if g else "", c[8]))
  return out


# ================================================================ drawing helpers

def text(x: float, y: float, s: str, size: int, fill: str = C["ink"], weight: int = 400, anchor: str = "start",
         family: str = FONT, extra: str = "") -> str:
  attrs = f'x="{x:g}" y="{y:g}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"'
  return f"<text {attrs}{extra}>{escape(s)}</text>"


def wrap(s: str, width: float, size: int) -> list[str]:
  per = width / (size * 0.5)
  lines, cur = [], ""
  for w in s.split():
    cand = f"{cur} {w}".strip()
    if len(cand) > per and cur:
      lines.append(cur)
      cur = w
    else:
      cur = cand
  if cur:
    lines.append(cur)
  return lines


def paragraph(x: float, y: float, s: str, size: int, width: float, fill: str = C["ink"], weight: int = 400,
              leading: float = 1.4) -> tuple[str, float]:
  out = []
  for i, line in enumerate(wrap(s, width, size)):
    out.append(text(x, y + i * size * leading, line, size, fill, weight))
  return "\n".join(out), y + len(out) * size * leading


def rect(x: float, y: float, w: float, h: float, fill: str, r: float = 0, stroke: str = "", sw: float = 1,
         dash: str = "") -> str:
  st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
  if dash:
    st += f' stroke-dasharray="{dash}"'
  return f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{r:g}" fill="{fill}"{st}/>'


def arrow(x: float, y: float) -> str:
  line = f'<line x1="{x:g}" y1="{y:g}" x2="{x + 12:g}" y2="{y:g}" stroke="{C["muted"]}" stroke-width="2"/>'
  head = f'<polygon points="{x + 12:g},{y - 5:g} {x + 20:g},{y:g} {x + 12:g},{y + 5:g}" fill="{C["muted"]}"/>'
  return line + head


def header(label: str, title: str, source: str) -> str:
  return "\n".join([
    rect(0, 0, W, 100, C["navy"]),
    text(40, 38, label, 13, C["gold"], 600, extra=' letter-spacing="1" style="text-transform:uppercase"'),
    text(40, 76, title, 30, C["on_navy"], 700),
    text(W - 40, 52, source, 14, C["on_navy_muted"], anchor="end"),
    text(W - 40, 72, "rendered at each wiki sync", 14, C["on_navy_muted"], anchor="end"),
  ])


def footer(left: str, right: str, h: int) -> str:
  return "\n".join([
    f'<line x1="0" y1="{h - 40}" x2="{W}" y2="{h - 40}" stroke="{C["line"]}"/>',
    text(40, h - 16, left, 13, C["muted"]),
    text(W - 40, h - 16, right, 13, C["muted"], anchor="end"),
  ])


def svg(title: str, desc: str, body: list[str], h: int) -> str:
  return "\n".join([
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img" aria-labelledby="t d">',
    f"<title id=\"t\">{escape(title)}</title>",
    f"<desc id=\"d\">{escape(desc)}</desc>",
    rect(0, 0, W, h, C["bg"]),
    *body,
    rect(0.5, 0.5, W - 1, h - 1, "none", stroke=C["line"]),
    "</svg>",
    "",
  ])


def bar_row(x: float, y: float, value: int, vmax: int, label: str, color: str, bar_w: float = 170,
            h: float = 14, size: int = 14, fill_text: str = C["ink"]) -> str:
  w = max(2.0, bar_w * value / vmax) if vmax else 2.0
  return "\n".join([
    rect(x, y, w, h, color, r=3),
    text(x + w + 8, y + h - 2, label, size, fill_text),
  ])


# ================================================================ figure 1: the decision register

def decision_register_svg(reg: list[dict]) -> str:
  total = len(reg)
  status = collections.Counter(str(d.get("status")) for d in reg)
  rev = collections.Counter(str(d.get("reversibility")) for d in reg)
  decider = collections.Counter(str(d.get("decider")) for d in reg)
  gate = collections.Counter(str(d.get("gate")) for d in reg)
  via = collections.Counter()
  for d in reg:
    if d.get("status") in ("answered", "applied"):
      a = d.get("answer")
      v = a.get("via") if isinstance(a, dict) else d.get("via")
      via[str(v or "unknown")] += 1
  batches: dict[int, collections.Counter] = collections.defaultdict(collections.Counter)
  for d in reg:
    b = d.get("batch")
    if isinstance(b, int):
      batches[b][str(d.get("status"))] += 1

  body = [header("Asimov v1 assurance · decision register", "Questions for the project lead, at a glance",
                 "Generated from register.yaml")]
  x0 = 40
  body.append(text(x0, 215, str(total), 88, C["ink"], 700, extra=' letter-spacing="-2"'))
  body.append(text(x0, 245, "questions recorded", 18, C["ink"], 600))
  p, y = paragraph(x0, 268, "one entry per question the lead alone can decide; tasks stay in their work products",
                   14, 290, C["muted"])
  body.append(p)
  tiles = (
    (status["open"], "open now", C["gold"]), (status["applied"], "answered and applied", C["navy2"]),
    (status["answered"], "answered, not yet applied", C["mid"]), (status["queued"], "queued, written ahead", C["light"]),
  )
  for i, (n, label, col) in enumerate(tiles):
    tx = x0 + (i % 2) * 160
    ty = 320 + (i // 2) * 80
    body.append(f'<line x1="{tx}" y1="{ty}" x2="{tx + 146}" y2="{ty}" stroke="{col}" stroke-width="3"/>')
    body.append(text(tx, ty + 40, str(n), 34, C["ink"], 700))
    body.append(text(tx, ty + 60, label, 12, C["muted"]))
  body.append(rect(x0, 490, 300, 96, C["panel"], r=8))
  body.append(text(x0 + 14, 512, "HOW ANSWERS ARRIVED", 12, C["muted"], 600, extra=' letter-spacing="0.6"'))
  vmax = max(via.values(), default=1)
  body.append(bar_row(x0 + 14, 526, via["inbox"], vmax, f"{via['inbox']} on the inbox page", C["navy2"], 110))
  body.append(bar_row(x0 + 14, 552, via["chat"], vmax, f"{via['chat']} in chat", C["mid"], 110))

  rx, rw = 380, W - 380 - 40
  body.append(text(rx, 150, "Where every question stands", 15, C["ink"], 700))
  present = [s for s in STATUS_ORDER if status[s]]
  gap = 2
  usable = rw - gap * (len(present) - 1)
  x = rx
  label_x = []
  for s in present:
    w = usable * status[s] / total if total else 0
    stroke = C["gold"] if s == "assumed" else ""
    body.append(rect(x, 162, w, 38, STATUS_COLOR[s], r=4, stroke=stroke))
    label_x.append((x, s))
    x += w + gap
  colw = rw / max(len(present), 1)
  for i, (_, s) in enumerate(label_x):
    lx = rx + i * colw
    body.append(rect(lx, 214, 10, 10, STATUS_COLOR[s], r=2, stroke=C["gold"] if s == "assumed" else ""))
    body.append(text(lx + 16, 223, f"{status[s]} {s}", 13, C["ink"], 700))
    body.append(text(lx + 16, 240, STATUS_NOTE[s], 12, C["muted"]))

  body.append(text(rx, 290, "Batches of ten", 15, C["ink"], 700))
  nums = sorted(batches)
  cells = len(nums) + 1
  cw = (rw - 6 * (cells - 1)) / (cells + 0.6)
  x = rx
  for n in nums:
    c = batches[n]
    open_n, done_n = c["open"], c["answered"] + c["applied"] + c["assumed"] + c["withdrawn"]
    if open_n and done_n == 0 and sum(c.values()) < 10:
      fill, ink, stroke = C["cream"], C["ink"], C["gold"]
    elif open_n:
      fill, ink, stroke = C["gold"], C["ink"], ""
    else:
      fill, ink, stroke = C["navy2"], C["on_navy"], ""
    body.append(rect(x, 302, cw, 66, fill, r=6, stroke=stroke, sw=2))
    body.append(text(x + cw / 2, 324, str(n), 16, ink, 700, anchor="middle"))
    lines = [f"{open_n} open"] * bool(open_n) + [f"{done_n} done"] * bool(done_n)
    for j, line in enumerate(lines):
      body.append(text(x + cw / 2, 342 + j * 15, line, 11, ink, anchor="middle"))
    x += cw + 6
  qw = cw * 1.6
  body.append(rect(x, 302, qw, 66, C["panel"], r=6, stroke=C["light"], dash="4 3"))
  body.append(text(x + qw / 2, 324, "queue", 16, C["muted"], 700, anchor="middle"))
  body.append(text(x + qw / 2, 346, f"{status['queued']} waiting", 11, C["muted"], anchor="middle"))

  py = 410
  colw = (rw - 40) / 3
  px = rx
  body.append(text(px, py, "How hard to undo", 15, C["ink"], 700))
  rows = (("easy", "easy"), ("revisit", "revisit at a gate"), ("hard", "hard, never assumed"))
  vmax = max((rev[k] for k, _ in rows), default=1) or 1
  for i, (k, label) in enumerate(rows):
    body.append(bar_row(px, py + 16 + i * 26, rev[k], vmax, f"{rev[k]} {label}", C["mid"], colw - 150))
  px = rx + colw + 20
  body.append(text(px, py, "Which gate it belongs to", 15, C["ink"], 700))
  gates = sorted((g for g in gate if g != "None"), key=lambda g: (len(g), g))
  vmax = max((gate[g] for g in gates), default=1) or 1
  for i, g in enumerate(gates):
    body.append(bar_row(px, py + 16 + i * 22, gate[g], vmax, f"{g} · {gate[g]}", C["mid"], colw - 120, h=10, size=13))
  if gate["None"]:
    body.append(bar_row(px, py + 16 + len(gates) * 22, gate["None"], vmax, f"no gate yet · {gate['None']}", C["grey"],
                        colw - 120, h=10, size=13, fill_text=C["muted"]))
  px = rx + 2 * (colw + 20)
  body.append(text(px, py, "Who decides", 15, C["ink"], 700))
  drows = (("lead", "the lead alone", C["gold"]), ("claude", "a reversible technical choice", C["mid"]),
           ("None", "not sorted yet", C["grey"]))
  vmax = max((decider[k] for k, _, _ in drows), default=1) or 1
  for i, (k, label, col) in enumerate(drows):
    body.append(bar_row(px, py + 16 + i * 26, decider[k], vmax, f"{decider[k]} {label}", col, colw - 190,
                        fill_text=C["muted"] if k == "None" else C["ink"]))
  p, _ = paragraph(px, py + 16 + 3 * 26 + 14, "Sorting happens when a question moves from queued to open.", 12,
                   colw, C["muted"])
  body.append(p)

  left = "Statuses, batches, gates, reversibility and decider are fields of each register entry; the lifecycle is in the register README and checked in CI."
  body.append(footer(left, "tools/wiki/infographics.py", H_REGISTER))
  return svg("The decision register at a glance",
             f"{total} questions recorded: " + ", ".join(f"{status[s]} {s}" for s in present) + ".", body, H_REGISTER)


# ================================================================ figure 2: what a change goes through

def change_path_svg(classes: dict[str, int], workflows: list[tuple[str, bool]]) -> str:
  on_pr = [n for n, pr in workflows if pr]
  manual = [n for n, pr in workflows if not pr]
  body = [header("Asimov v1 assurance · contributing", "What a change goes through before it is merged",
                 "Generated from safety-relevant-paths.txt and .github/workflows/")]
  top, bottom = 126, H_CHANGE - 56
  cols = ((40, 170), (238, 250), (516, 230), (774, 250), (1052, 188))
  caps = ("1 · A PULL REQUEST", "2 · CLASSIFIED BY PATHS", "3 · MUST CARRY, IF SAFETY-RELEVANT",
          f"4 · {len(on_pr)} WORKFLOWS CHECK IT", "5 · A PERSON REVIEWS")
  for (x, _w), cap in zip(cols, caps, strict=True):
    body.append(text(x, top + 12, cap, 11, C["muted"], 600, extra=' letter-spacing="0.6"'))
  for (x, w) in cols[:-1]:
    body.append(arrow(x + w + 4, (top + 30 + bottom) / 2))

  x, w = cols[0]
  body.append(rect(x, top + 24, w, bottom - top - 24, C["white"], r=8, stroke=C["line"]))
  body.append(text(x + 14, top + 56, "against", 17, C["ink"], 700))
  body.append(text(x + 14, top + 78, "main", 15, C["ink"], 500, family=MONO))
  p, y = paragraph(x + 14, top + 108, "Branch from it, open the pull request against it. Code changes go to the forked platform repositories; this one holds the record.",
                   14, w - 28, C["muted"])
  body.append(p)
  p, _ = paragraph(x + 14, bottom - 54, "Reviews of the analyses count as much as code.", 14, w - 28, C["muted"])
  body.append(p)

  x, w = cols[1]
  y = top + 24
  for cls in ("SR-A", "SR-Q", "SR-T"):
    hi = cls == "SR-A"
    lines = wrap(CLASS_TEXT[cls], w - 24, 14)
    h = 44 + len(lines) * 20
    body.append(rect(x, y, w, h, C["cream"] if hi else C["white"], r=8, stroke=C["gold"] if hi else C["mid"],
                     sw=2 if hi else 1))
    body.append(text(x + 12, y + 24, cls, 15, C["ink"], 500, family=MONO))
    body.append(text(x + w - 12, y + 24, f"{classes.get(cls, 0)} patterns", 13, C["muted"], anchor="end"))
    for i, line in enumerate(lines):
      body.append(text(x + 12, y + 46 + i * 20, line, 14, C["ink"]))
    y += h + 8
  body.append(rect(x, y, w, 64, C["panel"], r=8, stroke=C["light"], dash="4 3"))
  body.append(text(x + 12, y + 24, "NSR", 15, C["muted"], 500, family=MONO))
  body.append(text(x + 12, y + 46, "Everything else: the standard route", 14, C["muted"]))

  x, w = cols[2]
  y = top + 24
  for i, (head, rest) in enumerate(REQUIREMENTS, 1):
    lines = wrap(rest, w - 50, 14)
    h = 42 + len(lines) * 20
    body.append(rect(x, y, w, h, C["white"], r=8, stroke=C["line"]))
    body.append(text(x + 12, y + 28, str(i), 20, C["gold"], 700))
    body.append(text(x + 38, y + 24, head, 14, C["ink"], 700))
    for j, line in enumerate(lines):
      body.append(text(x + 38, y + 44 + j * 20, line, 14, C["ink"]))
    y += h + 8

  x, w = cols[3]
  body.append(rect(x, top + 24, w, bottom - top - 24, C["white"], r=8, stroke=C["line"]))
  y = top + 48
  for name in on_pr:
    body.append(text(x + 12, y, name, 13, C["ink"], 500, family=MONO))
    body.append(text(x + 12, y + 17, WORKFLOW_NOTE.get(name, "checks pull requests"), 12, C["muted"]))
    y += 26
    body.append(f'<line x1="{x + 12}" y1="{y}" x2="{x + w - 12}" y2="{y}" stroke="{C["grey"]}"/>')
    y += 22
  if manual:
    p, _ = paragraph(x + 12, bottom - 44, f"Started by hand, not on pull requests: {', '.join(manual)}.", 12,
                     w - 24, C["muted"])
    body.append(p)

  x, w = cols[4]
  body.append(rect(x, top + 24, w, bottom - top - 24, C["navy"], r=8))
  body.append(text(x + 14, top + 56, "Merged by the", 17, C["on_navy"], 700))
  body.append(text(x + 14, top + 78, "maintainer", 17, C["on_navy"], 700))
  p, _ = paragraph(x + 14, top + 108, "Never by the author of a work product. With one maintainer, I1 review needs an external reviewer.",
                   14, w - 28, C["on_navy_muted"])
  body.append(p)
  body.append(f'<line x1="{x + 14}" y1="{bottom - 150}" x2="{x + w - 14}" y2="{bottom - 150}" stroke="#2B4066"/>')
  body.append(text(x + 14, bottom - 128, "WHAT CI CANNOT DO", 12, C["gold_hi"], 600, extra=' letter-spacing="0.6"'))
  p, _ = paragraph(x + 14, bottom - 106, "Accept evidence. A green run can be evidence; only a review record by the named independent reviewer accepts it.",
                   14, w - 28, C["on_navy"])
  body.append(p)

  left = "Classes and pattern counts from WP-P-01; the four requirements from CONTRIBUTING.md; workflows from their files' names and triggers."
  body.append(footer(left, "tools/wiki/infographics.py", H_CHANGE))
  classes_text = ", ".join(f"{k} ({v} patterns)" for k, v in sorted(classes.items()))
  desc = (f"A pull request is classified into {classes_text} or not safety-relevant; a safety-relevant one carries rationale, "
          + f"impact analysis, verification and record updates; {len(on_pr)} workflows check it; a person reviews and merges.")
  return svg("What a change goes through before it is merged", desc, body, H_CHANGE)


# ================================================================ figure 3: the work product register

def register_status_svg(rows: list[tuple[str, str, str, str]]) -> str:
  total = len(rows)
  by_status = collections.Counter(s for _, _, _, s in rows)
  by_gate: dict[str, collections.Counter] = {g: collections.Counter() for g in GATES}
  for _, _, g, s in rows:
    if g in by_gate:
      by_gate[g][s] += 1
  body = [header("Asimov v1 assurance · work product register", "Every work product, by gate and status",
                 "Generated from WP-M-00 §3")]
  x0 = 40
  body.append(text(x0, 215, str(total), 88, C["ink"], 700, extra=' letter-spacing="-2"'))
  body.append(text(x0, 245, "work products registered", 18, C["ink"], 600))
  p, ty = paragraph(x0, 268, "each with its clauses, gate and status in the register; the folder READMEs and the process maps are generated from the same rows", 14, 290, C["muted"])
  body.append(p)
  ty += 18
  for s in WP_STATUS_ORDER:
    if by_status[s]:
      body.append(rect(x0, ty, 14, 14, WP_STATUS_COLOR[s], r=3))
      body.append(text(x0 + 24, ty + 12, f"{by_status[s]} {WP_STATUS_NAME[s]}", 15, C["ink"], 700))
      ty += 26
  body.append(text(x0, ty + 16, "Nothing is in review, approved or baselined.", 12, C["muted"]) if not (by_status["R"] or by_status["A"] or by_status["B"]) else "")

  rx, rw = 380, W - 380 - 40
  body.append(text(rx, 150, "Work products needed by each gate (first gate of a living work product)", 15, C["ink"], 700))
  vmax = max((sum(c.values()) for c in by_gate.values()), default=1) or 1
  bar_h = 34
  for i, g in enumerate(GATES):
    y = 172 + i * (bar_h + 10)
    c = by_gate[g]
    n = sum(c.values())
    body.append(text(rx, y + 23, g, 15, C["ink"], 700, family=MONO))
    x = rx + 50
    for s in WP_STATUS_ORDER:
      if c[s]:
        w = (rw - 120) * c[s] / vmax
        body.append(rect(x, y, w, bar_h, WP_STATUS_COLOR[s], r=3))
        if w > 26:
          body.append(text(x + w / 2, y + 22, str(c[s]), 13, C["ink"] if s in ("S", "D") else C["on_navy"], 600, anchor="middle"))
        x += w + 2
    body.append(text(x + 10, y + 23, f"{n}", 14, C["muted"], 600))
  left = "Status per the register's Status column: S skeleton, D draft, R in review, A approved, B baselined. A gate counts as passed only by its record."
  body.append(footer(left, "tools/wiki/infographics.py", H_STATUS))
  desc = f"{total} work products registered: " + ", ".join(f"{by_status[s]} {WP_STATUS_NAME[s]}" for s in WP_STATUS_ORDER if by_status[s]) + ". Per gate: " + "; ".join(f"{g} {sum(by_gate[g].values())}" for g in GATES) + "."
  return svg("The work product register at a glance", desc, body, H_STATUS)


# ================================================================ entry points

def render_all(root: Path = ROOT) -> dict[str, str]:
  reg = load_register(root / "assurance" / "01-management" / "decisions" / "register.yaml")
  classes = load_classes(root / "assurance" / "07-supporting" / "safety-relevant-paths.txt")
  workflows = load_workflows(root / ".github" / "workflows")
  rows = load_wp_register(root / "assurance" / "01-management" / "WP-M-00-work-product-register.md")
  return {"decision-register.svg": decision_register_svg(reg), "change-path.svg": change_path_svg(classes, workflows),
          "register-status.svg": register_status_svg(rows)}


def write_all(out: Path, root: Path = ROOT) -> list[str]:
  out.mkdir(parents=True, exist_ok=True)
  figs = render_all(root)
  for name, s in figs.items():
    (out / name).write_text(s, encoding="utf-8")
  return sorted(figs)


def check_all(folder: Path, root: Path = ROOT) -> list[str]:
  stale = []
  for name, s in render_all(root).items():
    f = folder / name
    if not f.exists() or f.read_text(encoding="utf-8") != s:
      stale.append(name)
  return stale


def main(argv: list[str]) -> int:
  ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
  g = ap.add_mutually_exclusive_group()
  g.add_argument("--out", type=Path, help="write the figures into this folder")
  g.add_argument("--check", type=Path, help="fail if this folder's copies are not what the records give now")
  args = ap.parse_args(argv)
  if args.check:
    stale = check_all(args.check)
    for name in stale:
      print(f"{args.check / name}: stale or missing; regenerate with --out")
    print(f"infographics: {len(NAMES) - len(stale)} of {len(NAMES)} current")
    return 1 if stale else 0
  if args.out:
    for name in write_all(args.out):
      print(f"wrote {args.out / name}")
    return 0
  for name, s in render_all().items():
    print(f"{name}: {len(s)} bytes")
  return 0


if __name__ == "__main__":
  sys.exit(main(sys.argv[1:]))
