#!/usr/bin/env python3
"""Draw the integrated process model (WP-P-11) as SVG figures for the wiki and the docs.

Nine figures, all computed from the same records `process_model.py` checks, so they cannot disagree with
the Mermaid maps, the register or the safety plan:

  lifecycle-swimlanes.svg   L0: the seven phases across, the discipline lanes down, how many activities
                            each lane performs in each phase, the confirmation measures and the open
                            interfaces per gate, the feedback routes from operation back into the concept
  g0.svg … g6.svg           L1: one vertical swimlane per phase; one column per discipline present in the
                            phase, activities in dependency order from top to bottom, arrows for
                            work-product inputs, dotted links for the cross-domain interfaces, the
                            confirmation measures of the gate and the gate's exit criterion
  interfaces.svg            every cross-domain interface: which lanes it joins, through which work
                            products, its pattern, its status and the gate it is due at

Nothing is typed by hand: lane names, roles, activity names, inputs, work-product status and gate exit
criteria are read from the model, WP-M-00 and WP-M-02 at generation time. CI checks that the committed
copies match (`--check`).

Usage: python3 assurance/process/tools/process_figures.py [--out DIR | --check]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).resolve().parent))
import process_model as pm  # noqa: E402

ROOT = pm.ASSURANCE_DIR.parent
OUT_DIR = ROOT / "docs" / "assets" / "asimov" / "process"
NAMES = ("lifecycle-swimlanes.svg", "g0.svg", "g1.svg", "g2.svg", "g3.svg", "g4.svg", "g5.svg", "g6.svg", "interfaces.svg")

FONT = "Inter, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, monospace"
C = {
  # light theme, the same palette as make_assets.py
  "bg1": "#FFFFFF", "bg2": "#F3F7F8", "panel": "#EDF2F4", "panel2": "#F7FAFB", "stroke": "#D3DDE2",
  "amber": "#D4821A", "amber_hi": "#F2A33A", "amber_lo": "#A8650F", "cyan": "#0E8C83", "cyan_lo": "#8FD8D1",
  "text": "#122026", "muted": "#4E6A73", "dim": "#7E949B", "red": "#D64535", "green": "#2C9A58", "white": "#FFFFFF",
  "ink": "#122026",
}
# one tint per discipline lane; the joint lane is the green of the Mermaid maps, confirmation the yellow
LANE_COLOR = {"joint": "#2C9A58", "risk": "#D4821A", "srpcs": "#0E8C83", "hw": "#2F6FD6", "sw": "#7A4BD6",
              "cs": "#D64535", "ml": "#C2399A", "assess": "#A88A00"}
LANE_SHORT = {"joint": "Joint", "risk": "Risk assessment", "srpcs": "Safety-related control", "hw": "Electrical & mechanical",
              "sw": "Software", "cs": "Cybersecurity", "ml": "Machine learning", "assess": "Independent confirmation"}
STATUS_COLOR = {"S": "#C9D4D9", "D": C["amber_hi"], "R": C["cyan_lo"], "A": "#7FD8A4", "B": C["cyan_lo"], "N/A": "#C9D4D9"}
WIDTH = 1000


# ------------------------------------------------------------------ svg helpers

def text(x, y, s, size, fill=C["text"], weight=400, anchor="start", family=FONT, extra=""):
  return (f'<text x="{x:g}" y="{y:g}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
          f'fill="{fill}" text-anchor="{anchor}"{extra}>{escape(str(s))}</text>')


def rect(x, y, w, h, fill, r=0, stroke="", sw=1, opacity=None, dash=""):
  st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
  op = f' fill-opacity="{opacity}"' if opacity is not None else ""
  da = f' stroke-dasharray="{dash}"' if dash else ""
  return f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{r:g}" fill="{fill}"{st}{op}{da}/>'


def path(d, stroke, sw=1.4, dash="", marker=""):
  da = f' stroke-dasharray="{dash}"' if dash else ""
  mk = f' marker-end="url(#{marker})"' if marker else ""
  return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}"{da}{mk}/>'


def wrap(s, width, size, max_lines=3):
  per = max(int(width / (size * 0.54)), 8)
  lines, cur = [], ""
  for w in str(s).split():
    cand = f"{cur} {w}".strip()
    if len(cand) > per and cur:
      lines.append(cur)
      cur = w
    else:
      cur = cand
  if cur:
    lines.append(cur)
  if len(lines) > max_lines:
    lines = lines[:max_lines]
    lines[-1] = lines[-1][: max(per - 1, 1)].rstrip() + "…"
  return lines


def frame(w, h, gid):
  defs = "\n".join([
    f'<linearGradient id="{gid}-bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{C["bg1"]}"/><stop offset="1" stop-color="{C["bg2"]}"/></linearGradient>',
    f'<linearGradient id="{gid}-amber" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C["amber_lo"]}"/><stop offset="0.5" stop-color="{C["amber_hi"]}"/><stop offset="1" stop-color="{C["amber_lo"]}"/></linearGradient>',
    f'<marker id="{gid}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{C["muted"]}"/></marker>',
    f'<marker id="{gid}-arrow-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{C["amber"]}"/></marker>',
  ])
  body = "\n".join([
    f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="22" fill="url(#{gid}-bg)" stroke="{C["stroke"]}"/>',
    f'<rect x="40" y="0" width="{w - 80}" height="3" fill="url(#{gid}-amber)"/>',
  ])
  return defs, body


def svg(w, h, gid, title, desc, defs, body):
  return "\n".join([
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="{gid}-t {gid}-d">',
    f'  <title id="{gid}-t">{escape(title)}</title>',
    f'  <desc id="{gid}-d">{escape(desc)}</desc>',
    "  <defs>", defs, "  </defs>", body, "</svg>", ""])


def heading(label, title, right=""):
  out = [text(40, 56, label, 15, C["amber"], 700, extra=' letter-spacing="3"'), text(40, 94, title, 28, C["text"], 700)]
  if right:
    out.append(text(WIDTH - 40, 56, right, 12, C["muted"], anchor="end"))
  return out


def pill(x, y, label, color, size=10.5, h=18, fill_bg=None, mono=True):
  w = len(label) * size * 0.62 + 16
  fill = fill_bg or color
  out = [rect(x, y, w, h, fill, r=h / 2, opacity=None if fill_bg else 0.18),
         text(x + w / 2, y + h / 2 + size * 0.36, label, size, color if not fill_bg else C["ink"], 700, anchor="middle", family=MONO if mono else FONT)]
  return out, w


# ------------------------------------------------------------------ model views

class View:
  """The checked model plus the derived data every figure needs."""

  def __init__(self) -> None:
    self.model = pm.load_model()
    self.ctx = pm.load_context()
    self.orders = pm.check(self.model, self.ctx)
    if self.model.errors:
      raise SystemExit("\n".join(self.model.errors) + f"\nFAIL: {len(self.model.errors)} process model error(s); fix the model before drawing it")
    self.lane_of_wp = {wp: a["lane"] for a in self.model.activities.values() for wp in pm.outputs(a)}
    self.producer = {wp: a["id"] for a in self.model.activities.values() for wp in pm.outputs(a)}

  def lanes(self) -> list[str]:
    return list(self.model.lanes)

  def role_holder(self, lane: str) -> str:
    role = self.model.lanes[lane]["role"]
    holder = self.ctx.roles.get(role, ("TBD", ""))[0]
    return holder

  def phase_layout(self, gid: str):
    """Activities of a phase with their dependency depth and the direct input edges."""
    order = self.orders[gid]
    acts = {a: self.model.activities[a] for a in order}
    producer = {wp: ids[-1] for wp, ids in pm.phase_suppliers(acts).items()}
    deps = pm.direct_deps(acts, producer)
    depth: dict[str, int] = {}

    def d(a: str) -> int:
      if a not in depth:
        depth[a] = 0 if not deps[a] else 1 + max(d(x) for x in deps[a])
      return depth[a]

    for a in order:
      d(a)
    return acts, deps, depth

  def status_of(self, wp: str) -> str:
    row = self.ctx.register.get(wp)
    return row.status if row else "?"


# ------------------------------------------------------------------ L0 overview

def lifecycle_svg(v: View) -> str:
  lanes = v.lanes()
  label_w, cell_w, cell_h = 236, 100, 46
  top = 150
  grid_h = len(lanes) * cell_h
  h = top + grid_h + 212
  gid = "l0"
  defs, body_frame = frame(WIDTH, h, gid)
  body = [body_frame]
  body += heading("INTEGRATED LIFECYCLE · L0", "One lifecycle, seven gates, every discipline in the same phase",
                  f"{len(v.model.activities)} activities · {len(v.model.reviews)} confirmation measures · {len(v.model.interfaces)} interfaces")
  # phase columns
  x0 = 40 + label_w
  per_phase = {g: [a for a in v.model.activities.values() if a["phase"] == g] for g in pm.GATES}
  for i, g in enumerate(pm.GATES):
    x = x0 + i * cell_w
    name = v.ctx.gates[g][0]
    body.append(rect(x + 3, top - 44, cell_w - 6, 40, C["panel"], r=8, stroke=C["stroke"]))
    body.append(text(x + cell_w / 2, top - 27, f"P{i} · {g}", 11, C["amber"], 700, anchor="middle", family=MONO))
    body.append(text(x + cell_w / 2, top - 12, wrap(name, cell_w - 14, 10, 1)[0], 10, C["text"], 600, anchor="middle"))
  # lane rows
  for j, lane in enumerate(lanes):
    y = top + j * cell_h
    col = LANE_COLOR[lane]
    body.append(rect(40, y, WIDTH - 80, cell_h - 4, C["panel2"] if j % 2 else C["panel"], r=6, opacity=0.6))
    body.append(rect(40, y, 5, cell_h - 4, col, r=2))
    body.append(text(56, y + 19, LANE_SHORT[lane], 12, C["text"], 700))
    body.append(text(56, y + 34, wrap(v.role_holder(lane), label_w - 30, 9.5, 1)[0], 9.5, C["muted"]))
    for i, g in enumerate(pm.GATES):
      n = sum(1 for a in per_phase[g] if a["lane"] == lane)
      x = x0 + i * cell_w
      if n:
        for k in range(min(n, 8)):
          body.append(rect(x + 12 + (k % 4) * 17, y + 9 + (k // 4) * 13, 12, 9, col, r=2, opacity=0.85 if k < 4 else 0.5))
        body.append(text(x + cell_w - 10, y + 27, str(n), 15, col, 800, anchor="end", family=MONO))
      else:
        body.append(text(x + cell_w / 2, y + 27, "·", 14, C["dim"], anchor="middle"))
  # gate markers and bottom rows: measures, interfaces
  yb = top + grid_h + 14
  body.append(text(40, yb + 14, "Confirmation measures at the gate", 11, C["muted"], 600))
  body.append(text(40, yb + 40, "Cross-domain interfaces (open)", 11, C["muted"], 600))
  body.append(text(40, yb + 82, "Gates", 11, C["muted"], 600))
  for i, g in enumerate(pm.GATES):
    x = x0 + i * cell_w
    reviews = [r for r in v.model.reviews.values() if r["phase"] == g]
    ixs = [ix for ix in v.model.interfaces.values() if ix["phase"] == g]
    openn = sum(1 for ix in ixs if ix["status"] == "open")
    body.append(text(x + cell_w / 2, yb + 14, str(len(reviews)) if reviews else "·", 12, LANE_COLOR["assess"] if reviews else C["dim"], 700, anchor="middle", family=MONO))
    ix_label = f"{len(ixs)} ({openn})" if ixs else "·"
    body.append(text(x + cell_w / 2, yb + 40, ix_label, 12, C["red"] if openn else (C["cyan"] if ixs else C["dim"]), 700, anchor="middle", family=MONO))
    # gate diamond
    cx, cy = x + cell_w / 2, yb + 78
    body.append(f'<polygon points="{cx},{cy - 9} {cx + 9},{cy} {cx},{cy + 9} {cx - 9},{cy}" fill="{C["cyan_lo"]}" stroke="{C["cyan"]}" stroke-width="1.2"/>')
    body.append(text(cx, cy + 22, g, 10, C["cyan"], 700, anchor="middle", family=MONO))
    if i < len(pm.GATES) - 1:
      body.append(path(f"M{cx + 12},{cy} L{x + cell_w + cell_w / 2 - 12},{cy}", C["cyan_lo"], 1.2))
  # feedback arc from G6 back to G1
  gx6 = x0 + 6 * cell_w + cell_w / 2
  gx1 = x0 + 1 * cell_w + cell_w / 2
  ya = yb + 78
  body.append(path(f"M{gx6},{ya + 12} C{gx6},{ya + 66} {gx1},{ya + 66} {gx1},{ya + 14}", C["amber"], 1.4, dash="4 3", marker=f"{gid}-arrow-amber"))
  fbs = sorted(v.model.feedback)
  body.append(text((gx6 + gx1) / 2, ya + 76, f"{len(fbs)} feedback routes ({fbs[0]}…{fbs[-1]}): findings from operation re-open the concept phase", 10.5, C["amber"], 600, anchor="middle"))
  # exit criteria line (short) under the gate row
  body.append(text(40, h - 16, "Each cell is the number of activities the lane performs in the phase. Gates, roles and exit criteria are read from WP-M-00 and WP-M-02; nothing here is typed by hand.", 10.5, C["dim"]))
  desc = ("The integrated lifecycle as a lane-by-phase grid. " + "; ".join(
    f"{LANE_SHORT[lane]}: " + ", ".join(f"{g} {sum(1 for a in per_phase[g] if a['lane'] == lane)}" for g in pm.GATES) for lane in lanes) + ".")
  return svg(WIDTH, h, gid, "The integrated lifecycle: disciplines by phase", desc, defs, "\n".join(body))


# ------------------------------------------------------------------ L1 swimlanes

CARD_H = 80
ROW_PITCH = 108


def phase_svg(v: View, gid: str) -> str:
  acts, deps, depth = v.phase_layout(gid)
  order = list(acts)
  name, exit_ = v.ctx.gates[gid]
  lanes = [ln for ln in v.lanes() if ln != "assess" and any(a["lane"] == ln for a in acts.values())]
  reviews = [r for r in v.model.reviews.values() if r["phase"] == gid]
  assess_acts = [a for a in acts.values() if a["lane"] == "assess"]
  if assess_acts:
    lanes.append("assess")
  ixs = [ix for ix in v.model.interfaces.values() if ix["phase"] == gid]
  fbs = [f for f in v.model.feedback.values() if f["phase"] == gid]

  # geometry: lane columns across, dependency depth down; several activities at one (lane, depth) stack
  margin = 40
  col_w = (WIDTH - 2 * margin) / len(lanes)
  card_w = col_w - 22
  max_depth = max(depth.values())
  stack = {}
  for a in order:
    key = (acts[a]["lane"], depth[a])
    stack[key] = stack.get(key, 0) + 1
  rows_at = [max([n for (ln, dp), n in stack.items() if dp == d] + [1]) for d in range(max_depth + 1)]
  row_y = []
  y = 184
  for n in rows_at:
    row_y.append(y)
    y += n * ROW_PITCH
  lanes_bottom = y + 6
  review_h = 70 if (reviews or assess_acts) else 0
  fb_h = 24 + 20 * len(fbs) if fbs else 0
  gate_h = 74
  h = lanes_bottom + review_h + fb_h + gate_h + 72
  fid = f"p{gid[1]}"
  defs, body_frame = frame(WIDTH, h, fid)
  body = [body_frame]
  body += heading(f"PROCESS MAP · {gid} · L1", f"P{gid[1]} {name}: who does what, in what order",
                  f"{len(acts)} activities · {len(reviews)} confirmation measures · {len(ixs)} interfaces")

  # lane columns
  lane_x = {}
  for i, ln in enumerate(lanes):
    x = margin + i * col_w
    lane_x[ln] = x
    col = LANE_COLOR[ln]
    body.append(rect(x + 3, 118, col_w - 6, lanes_bottom - 118, C["panel2"] if i % 2 else C["panel"], r=10, opacity=0.55))
    body.append(rect(x + 3, 118, col_w - 6, 4, col, r=2))
    lines = wrap(LANE_SHORT[ln], col_w - 20, 12, 1)
    body.append(text(x + col_w / 2, 142, lines[0], 12, col, 700, anchor="middle"))
    holder = wrap(v.role_holder(ln), col_w - 20, 9.5, 1)[0]
    body.append(text(x + col_w / 2, 158, holder, 9.5, C["muted"], anchor="middle"))

  # place cards
  slot_used: dict[tuple[str, int], int] = {}
  pos: dict[str, tuple[float, float]] = {}
  for a in order:
    ln, dp = acts[a]["lane"], depth[a]
    k = slot_used.get((ln, dp), 0)
    slot_used[(ln, dp)] = k + 1
    x = lane_x[ln] + 11
    yy = row_y[dp] + k * ROW_PITCH
    pos[a] = (x, yy)

  # edges first, so cards sit on top
  for a in order:
    x1, y1 = pos[a]
    for src in sorted(deps[a]):
      x0_, y0_ = pos[src]
      sx, sy = x0_ + card_w / 2, y0_ + CARD_H
      tx, ty = x1 + card_w / 2, y1
      if abs(sx - tx) < 1:
        d = f"M{sx:.1f},{sy:.1f} L{tx:.1f},{ty - 2:.1f}"
      else:
        my = (sy + ty) / 2
        d = f"M{sx:.1f},{sy:.1f} C{sx:.1f},{my:.1f} {tx:.1f},{my:.1f} {tx:.1f},{ty - 2:.1f}"
      body.append(path(d, C["muted"], 1.3, marker=f"{fid}-arrow"))

  # cards
  for a in order:
    act = acts[a]
    x, yy = pos[a]
    col = LANE_COLOR[act["lane"]]
    body.append(rect(x, yy, card_w, CARD_H, C["white"], r=9, stroke=C["stroke"]))
    body.append(rect(x, yy + 8, 3, CARD_H - 16, col, r=1.5))
    body.append(text(x + 11, yy + 16, a, 9.5, col, 700, family=MONO))
    for li, line in enumerate(wrap(act["name"], card_w - 18, 10.5, 3)):
      body.append(text(x + 11, yy + 31 + li * 13, line, 10.5, C["text"], 500))
    # outputs as status chips
    cx = x + 11
    for wp in pm.outputs(act)[:3]:
      st = v.status_of(wp)
      lab = wp.replace("WP-", "")
      w = len(lab) * 6.3 + 10
      if cx + w > x + card_w - 4:
        break
      body.append(rect(cx, yy + CARD_H - 18, w, 13, STATUS_COLOR.get(st, C["dim"]), r=6.5, opacity=0.9))
      body.append(text(cx + w / 2, yy + CARD_H - 8.5, lab, 8.5, C["ink"], 700, anchor="middle", family=MONO))
      cx += w + 4

  # interface links, drawn last so the label sits on top: dotted between the producing activities;
  # two cards in the same row get a tent above them so the label is not hidden by either card
  for ix in ixs:
    ends = [v.producer.get(wp) for wp in ix["between"]]
    ends = [e for e in ends if e in pos]
    if len(ends) != 2:
      continue
    (xa, ya), (xb, yb) = pos[ends[0]], pos[ends[1]]
    col = C["red"] if ix["status"] == "open" else C["cyan"]
    if abs(ya - yb) < 1:
      ax, bx = xa + card_w / 2, xb + card_w / 2
      mx, my = (ax + bx) / 2, ya - 16
      body.append(path(f"M{ax:.1f},{ya:.1f} L{mx:.1f},{my:.1f} L{bx:.1f},{yb:.1f}", col, 1.2, dash="3 4"))
    else:
      ax, ay = xa + card_w / 2, ya + CARD_H / 2
      bx, by = xb + card_w / 2, yb + CARD_H / 2
      body.append(path(f"M{ax:.1f},{ay:.1f} L{bx:.1f},{by:.1f}", col, 1.2, dash="3 4"))
      mx, my = (ax + bx) / 2, (ay + by) / 2
    label = ix["id"] + (" OPEN" if ix["status"] == "open" else "")
    lw = len(label) * 6.2 + 10
    body.append(rect(mx - lw / 2, my - 9, lw, 16, C["white"], r=8, stroke=col, sw=1))
    body.append(text(mx, my + 3, label, 9.5, col, 700, anchor="middle", family=MONO))

  # confirmation measures band
  yv = lanes_bottom
  if review_h:
    body.append(rect(margin, yv, WIDTH - 2 * margin, review_h - 8, C["panel"], r=10, stroke=C["stroke"]))
    body.append(rect(margin, yv, 5, review_h - 8, LANE_COLOR["assess"], r=2))
    body.append(text(margin + 16, yv + 20, "INDEPENDENT CONFIRMATION AT THIS GATE", 10, LANE_COLOR["assess"], 700, extra=' letter-spacing="1.5"'))
    body.append(text(WIDTH - margin - 12, yv + 20, v.role_holder("assess"), 9.5, C["muted"], anchor="end"))
    px = margin + 16
    for r in reviews:
      done = pm.record_present(r, v.ctx.register)
      lab = f"{pm.measure_id(r['id'])} · {r['independence']}" + (" · done" if done else "")
      chips, w = pill(px, yv + 32, lab, C["green"] if done else LANE_COLOR["assess"], size=10)
      body += chips
      px += w + 8
    for a in assess_acts:
      chips, w = pill(px, yv + 32, a["id"], LANE_COLOR["assess"], size=10)
      body += chips
      px += w + 8
    if not reviews and not assess_acts:
      body.append(text(margin + 16, yv + 44, "No confirmation measure is planned at this gate.", 10.5, C["muted"]))
    yv += review_h

  # feedback routes
  if fbs:
    body.append(text(margin, yv + 14, "FEEDBACK INTO EARLIER PHASES", 10, C["amber"], 700, extra=' letter-spacing="1.5"'))
    for i, f in enumerate(sorted(fbs, key=lambda f: f["id"])):
      body.append(text(margin, yv + 32 + i * 20, f"{f['id']}  {f['finding']}  →  {', '.join(f['targets'])}", 10.5, C["text"]))
    yv += fb_h

  # gate bar
  gy = yv + 8
  body.append(rect(margin, gy, WIDTH - 2 * margin, gate_h - 10, C["cyan_lo"], r=12, opacity=0.3))
  body.append(rect(margin, gy, WIDTH - 2 * margin, gate_h - 10, "none", r=12, stroke=C["cyan"]))
  body.append(text(margin + 18, gy + 24, f"{gid} · {name} gate", 14, C["cyan"], 800))
  for i, line in enumerate(wrap("Exit: " + exit_, WIDTH - 2 * margin - 36, 10.5, 2)):
    body.append(text(margin + 18, gy + 42 + i * 13, line, 10.5, C["text"]))
  for i, line in enumerate(wrap("Arrows are work-product inputs: an activity cannot finish before the one above it. Chips name the work products produced, coloured by register status (grey skeleton, amber draft, green approved). Dotted links are cross-domain interfaces; red means a recorded open item still has to settle it.", WIDTH - 2 * margin, 9.5, 2)):
    body.append(text(margin, h - 28 + i * 13, line, 9.5, C["dim"]))
  desc = (f"Process map of phase {gid} {name}: " + "; ".join(
    f"{a} {acts[a]['name']} ({LANE_SHORT[acts[a]['lane']]}, after {', '.join(sorted(deps[a])) or 'nothing'})" for a in order) + ".")
  return svg(WIDTH, h, fid, f"{gid} {name}: integrated process map", desc, defs, "\n".join(body))


# ------------------------------------------------------------------ interfaces

def interfaces_svg(v: View) -> str:
  ixs = sorted(v.model.interfaces.values(), key=lambda x: x["id"])
  row_h = 46
  top = 150
  h = top + len(ixs) * row_h + 70
  gid = "ix"
  defs, body_frame = frame(WIDTH, h, gid)
  body = [body_frame]
  openn = sum(1 for x in ixs if x["status"] == "open")
  body += heading("CROSS-DOMAIN INTERFACES", "Where one discipline's analysis depends on another's",
                  f"{len(ixs)} interfaces · {openn} open · each anchored to text in both work products")
  cols = {"id": 40, "lanes": 110, "pattern": 640, "status": 840, "due": 935}
  for key, label in (("id", "ID · phase"), ("lanes", "Between (producing lane and work product)"), ("pattern", "Pattern"), ("status", "Status"), ("due", "Due")):
    body.append(text(cols[key], top - 14, label.upper(), 9.5, C["muted"], 700, extra=' letter-spacing="1"'))
  for i, ix in enumerate(ixs):
    y = top + i * row_h
    if i % 2:
      body.append(rect(32, y - 6, WIDTH - 64, row_h, C["panel"], r=8, opacity=0.5))
    body.append(text(cols["id"], y + 14, ix["id"], 11, C["text"], 700, family=MONO))
    body.append(text(cols["id"], y + 29, ix["phase"], 10, C["muted"], family=MONO))
    # two lane pills joined by a line
    x = cols["lanes"]
    wa, wb = ix["between"][0], ix["between"][1]
    for k, wp in enumerate((wa, wb)):
      ln = v.lane_of_wp.get(wp, "joint")
      chips, w = pill(x, y + 4, f"{LANE_SHORT[ln]} · {wp}", LANE_COLOR[ln], size=9.5, mono=False)
      body += chips
      if k == 0:
        col = C["red"] if ix["status"] == "open" else C["cyan"]
        body.append(path(f"M{x + w + 4},{y + 13} L{x + w + 26},{y + 13}", col, 1.6, dash="3 3" if ix["status"] == "open" else ""))
        x += w + 30
    body.append(text(cols["lanes"], y + 36, wrap(ix["topic"], cols["pattern"] - cols["lanes"] - 10, 9.5, 1)[0], 9.5, C["dim"]))
    body.append(text(cols["pattern"], y + 14, wrap(ix["pattern"], 190, 11, 1)[0], 11, C["text"], 600))
    st = ix["status"]
    chips, _ = pill(cols["status"], y + 4, st.upper() if st != "open" else "OPEN", C["red"] if st == "open" else C["cyan"], size=9.5)
    body += chips
    body.append(text(cols["due"], y + 16, ix["due"], 11, C["text"], 700, family=MONO))
  body.append(text(40, h - 16, "Documented: both work products reference each other, not yet reviewed. Open: a recorded open item still has to settle it; the checker fails if an anchor disappears from either work product.", 9.5, C["dim"]))
  desc = "Cross-domain interfaces: " + "; ".join(f"{x['id']} ({x['phase']}, {x['pattern']}, {x['status']}) between {x['between'][0]} and {x['between'][1]}" for x in ixs) + "."
  return svg(WIDTH, h, gid, "Cross-domain interfaces of the process model", desc, defs, "\n".join(body))


# ------------------------------------------------------------------ entry points

def render_all(v: View | None = None) -> dict[str, str]:
  v = v or View()
  figs = {"lifecycle-swimlanes.svg": lifecycle_svg(v)}
  for g in pm.GATES:
    figs[f"{g.lower()}.svg"] = phase_svg(v, g)
  figs["interfaces.svg"] = interfaces_svg(v)
  return figs


def check_dir(out: Path, figs: dict[str, str] | None = None) -> int:
  """0 when every committed figure in `out` matches its generator, 1 otherwise (prints the stale ones)."""
  figs = figs or render_all()
  stale = [n for n, s in figs.items() if not (out / n).exists() or (out / n).read_text(encoding="utf-8") != s]
  for n in stale:
    print(f"{out / n}: stale or missing; run process_figures.py")
  print(f"process figures: {len(figs) - len(stale)} of {len(figs)} current")
  return 1 if stale else 0


def main(argv: list[str]) -> int:
  ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
  ap.add_argument("--out", type=Path, default=None)
  ap.add_argument("--check", action="store_true")
  args = ap.parse_args(argv)
  out = args.out or OUT_DIR
  figs = render_all()
  if args.check:
    return check_dir(out, figs)
  out.mkdir(parents=True, exist_ok=True)
  for n, s in figs.items():
    (out / n).write_text(s, encoding="utf-8")
    print(f"wrote {out / n}")
  return 0


if __name__ == "__main__":
  sys.exit(main(sys.argv[1:]))
