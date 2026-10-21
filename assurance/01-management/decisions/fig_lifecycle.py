#!/usr/bin/env python3
"""Draw the lifecycle of a decision-register entry (`figures/fig-dr-1-lifecycle.svg`) for README.md, at phone width.

The states, their meaning and who moves them come from the README "Lifecycle" table; the state list must equal
STATUS in check_decisions.py. The arrows between states exist only in prose, so each one in EDGES carries the README
text it is drawn from; `--check` fails when one of those texts is gone, when the table and STATUS differ, when the
README no longer embeds the figure, or when the committed SVG is stale. No counts from register.yaml are drawn, so the
figure changes only when the rules change.

    python3 fig_lifecycle.py            # write the SVG
    python3 fig_lifecycle.py --check    # fail if a source text changed or the SVG is stale

Standard library only. Output is deterministic.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
README = HERE / "README.md"
OUT = HERE / "figures" / "fig-dr-1-lifecycle.svg"
sys.path.insert(0, str(HERE.parents[0] / "figures"))
from figkit import FigureError, col, plain, section, table  # noqa: E402

sys.path.insert(0, str(HERE))
from check_decisions import STATUS  # noqa: E402

W = 640

# (from, to, label on the arrow, README text the arrow is drawn from)
EDGES = [
  ("queued", "open", "asked, in a batch of ten", "Ask in batches of ten."),
  ("open", "answered", "the lead picks an option", "The project lead picked an option"),
  ("open", "assumed", "no answer by proceed_after", "No answer by `proceed_after`"),
  ("answered", "applied", "change made", "The change is made"),
  ("assumed", "applied", "change made", "The change is made"),
]
# README rules printed on the figure (exact text)
RULES = ["A `hard` question is never assumed and never applied without an answer from the lead.",
         "Allowed only for `reversibility: easy`."]
WITHDRAWN = "The question no longer applies"

STYLE = """<style>
svg { --bg:#ffffff; --ink:#0b0b0b; --ink2:#52514e; --ink3:#8a8984; --grid:#e3e2de; --card:#f7f7f5;
      --blue:#2a78d6; --blue-bg:#e9f1fb; --amb:#c98500; --amb-bg:#fdf4dc; --ok:#2e9e6a; --ok-bg:#e6f5ec; }
@media (prefers-color-scheme: dark) {
  svg { --bg:#1a1a19; --ink:#f0efec; --ink2:#c3c2b7; --ink3:#8d8c85; --grid:#33322f; --card:#232321;
        --blue:#3987e5; --blue-bg:#16273c; --amb:#eda100; --amb-bg:#3a2f12; --ok:#3fb97d; --ok-bg:#15301f; }
}
.bg { fill:var(--bg); }
.h { font:600 21px -apple-system,'Segoe UI',Helvetica,Arial,sans-serif; fill:var(--ink); }
.tb { font:600 15px -apple-system,'Segoe UI',Helvetica,Arial,sans-serif; fill:var(--ink); }
.t2 { font:13px -apple-system,'Segoe UI',Helvetica,Arial,sans-serif; fill:var(--ink2); }
.ta { font:600 13px -apple-system,'Segoe UI',Helvetica,Arial,sans-serif; fill:var(--amb); }
.hair { stroke:var(--grid); stroke-width:1; }
.queued { fill:var(--bg); stroke:var(--ink3); stroke-width:1.4; stroke-dasharray:6 4; }
.open { fill:var(--amb-bg); stroke:var(--amb); stroke-width:2; }
.answered, .assumed { fill:var(--blue-bg); stroke:var(--blue); stroke-width:1.6; }
.applied { fill:var(--ok-bg); stroke:var(--ok); stroke-width:1.6; }
.withdrawn { fill:var(--card); stroke:var(--ink3); stroke-width:1.2; }
.rule { fill:var(--amb-bg); stroke:var(--amb); stroke-width:1.4; stroke-dasharray:6 4; }
.f-ink2 { fill:var(--ink2); }
.arr { stroke:var(--ink2); stroke-width:1.6; fill:none; }
.arrd { stroke:var(--ink3); stroke-width:1.6; fill:none; stroke-dasharray:5 4; }
</style>"""

MARKERS = ('<marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
           'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="f-ink2"/></marker>')
CHAR = {"tb": 0.6, "t2": 0.53, "ta": 0.56, "h": 0.56}
SIZE = {"tb": 15, "t2": 13, "ta": 13, "h": 21}


def fmt(v: float) -> str:
  return f"{v:.1f}".rstrip("0").rstrip(".")


def el(tag: str, content: str | None = None, **attrs) -> str:
  a = "".join(f' {k.rstrip("_").replace("_", "-")}="{v}"' for k, v in attrs.items() if v not in ("", None))
  return f"<{tag}{a}/>" if content is None else f"<{tag}{a}>{escape(content)}</{tag}>"


def T(x, y, s, cls="t2", anchor="") -> str:
  return el("text", s, x=fmt(x), y=fmt(y), class_=cls, text_anchor=anchor)


def R(x, y, w, h, cls, rx=8) -> str:
  return el("rect", None, x=fmt(x), y=fmt(y), width=fmt(w), height=fmt(h), rx=rx, class_=cls)


def P(d, cls="arr") -> str:
  return el("path", None, d=d, class_=cls, marker_end="url(#a)")


def wrap(s: str, w: float, cls="t2") -> list[str]:
  out, cur = [], ""
  for word in s.split():
    nxt = f"{cur} {word}".strip()
    if cur and len(nxt) * CHAR[cls] * SIZE[cls] > w:
      out.append(cur)
      cur = word
    else:
      cur = nxt
  return out + ([cur] if cur else [])


def norm(s: str) -> str:
  return re.sub(r"\s+", " ", s).strip()


# ---------------------------------------------------------------- source

def states(md: str | None = None) -> dict[str, tuple[str, str]]:
  """{status: (first sentence of the meaning, who moves it)} from the README Lifecycle table, in table order."""
  md = md if md is not None else README.read_text(encoding="utf-8")
  head, rows = table(section(md, "## Lifecycle"), "Status")
  i = [col(head, c) for c in ("Status", "Meaning", "Who moves it")]
  out = {}
  for r in rows:
    meaning = plain(r[i[1]])
    out[plain(r[i[0]])] = (re.split(r"(?<=[.;])\s", meaning)[0].rstrip(".;"), plain(r[i[2]]))
  return out


def problems(md: str | None = None) -> list[str]:
  md = md if md is not None else README.read_text(encoding="utf-8")
  out, text = [], norm(md)
  try:
    st = states(md)
  except FigureError as e:
    return [str(e)]
  if tuple(st) != STATUS:
    out.append(f"README Lifecycle table {tuple(st)} differs from check_decisions.STATUS {STATUS}")
  for a, b, _label, src in EDGES:
    if a not in st or b not in st:
      out.append(f"edge {a} -> {b}: state not in the Lifecycle table")
    if norm(src) not in text:
      out.append(f"edge {a} -> {b}: source text no longer in README: {src!r}")
  for s in RULES + [WITHDRAWN]:
    if norm(s) not in text:
      out.append(f"source text no longer in README: {s!r}")
  if f"({OUT.parent.name}/{OUT.name})" not in md:
    out.append(f"README does not embed {OUT.parent.name}/{OUT.name}")
  return out


# ---------------------------------------------------------------- figure

def card(x, y, w, name, st) -> tuple[list[str], float]:
  meaning, who = st[name]
  lines = [(ln, "t2") for ln in wrap(meaning, w - 24)]
  lines += [(ln, "ta" if name == "open" else "t2") for ln in wrap(f"Moved by: {who}", w - 24)]
  h = 38 + 17 * len(lines)
  body = [R(x, y, w, h, name), T(x + 12, y + 22, name, "tb")]
  body += [T(x + 12, y + 42 + 17 * k, ln, cls) for k, (ln, cls) in enumerate(lines)]
  return body, h


def build() -> str:
  st = states()
  body = [T(24, 34, "A question's path through the register", "h"),
          T(24, 56, "From the Lifecycle table of this page; who moves each state in the last line", "t2"),
          el("line", None, x1=24, y1=70, x2=W - 24, y2=70, class_="hair")]
  full, half = W - 48, (W - 48 - 24) / 2
  xl, xr = 24, 24 + half + 24
  y = 88
  c, h = card(24, y, full, "queued", st)
  body += c
  y += h
  edge = {(a, b): label for a, b, label, _s in EDGES}
  body += [P(f"M{W / 2} {y + 2} V{y + 38}"), T(W / 2 + 10, y + 24, edge[("queued", "open")])]
  y += 40
  c, h = card(24, y, full, "open", st)
  body += c
  y += h
  ya = y + 50
  body += [P(f"M{fmt(xl + half / 2)} {y + 2} V{ya - 2}"), T(xl + half / 2 - 10, y + 22, edge[("open", "answered")], anchor="end"),
           P(f"M{fmt(xr + half / 2)} {y + 2} V{ya - 2}"), T(xr + half / 2 - 10, y + 22, edge[("open", "assumed")], anchor="end"),
           T(xr + half / 2 - 10, y + 39, "easy questions only", "ta", "end")]
  c1, h1 = card(xl, ya, half, "answered", st)
  c2, h2 = card(xr, ya, half, "assumed", st)
  body += c1 + c2
  y = ya + max(h1, h2)
  yp = y + 46
  for x0 in (xl + half / 2, xr + half / 2):
    body.append(P(f"M{fmt(x0)} {y + 2} V{y + 20} H{fmt(W / 2 + (-12 if x0 < W / 2 else 12))} V{yp - 2}"))
  body.append(T(W / 2 + 22, y + 38, edge[("answered", "applied")]))
  c, h = card(24, yp, full, "applied", st)
  body += c
  y = yp + h + 16
  c, h = card(24, y, full, "withdrawn", st)
  body += c
  body.append(T(W - 36, y + 22, "from any state", "t2", "end"))
  y += h + 16
  rule = plain(RULES[0])
  lines = wrap(rule, full - 32, "tb")
  body.append(R(24, y, full, 20 + 20 * len(lines), "rule"))
  body += [T(40, y + 26 + 20 * k, ln, "tb") for k, ln in enumerate(lines)]
  y += 20 + 20 * len(lines) + 16
  desc = ("Lifecycle of a decision-register entry. " +
          "; ".join(f"{s}: {m} (moved by {w})" for s, (m, w) in st.items()) + ". Transitions: " +
          "; ".join(f"{a} to {b} when {label}" for a, b, label, _s in EDGES) +
          "; any state to withdrawn. Assumed is allowed only for easy questions. " + rule)
  head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{int(y)}" viewBox="0 0 {W} {int(y)}" '
          'role="img" aria-labelledby="t d">')
  return "\n".join([head, el("title", "Decision register: lifecycle of a question", id="t"), el("desc", desc, id="d"),
                    STYLE, f"<defs>{MARKERS}</defs>", f'<rect class="bg" width="{W}" height="{int(y)}"/>', *body,
                    "</svg>"]) + "\n"


def main(argv: list[str]) -> int:
  try:
    errs, out = problems(), build()
  except FigureError as e:
    print(f"fig_lifecycle: {e}", file=sys.stderr)
    return 1
  if "--check" in argv:
    if not OUT.exists() or OUT.read_text(encoding="utf-8") != out:
      errs.append(f"{OUT.name} is stale; run assurance/01-management/decisions/fig_lifecycle.py")
    for e in errs:
      print(f"fig_lifecycle: {e}", file=sys.stderr)
    if not errs:
      print("fig_lifecycle: figure current, source texts found")
    return 1 if errs else 0
  OUT.write_text(out, encoding="utf-8")
  print(f"fig_lifecycle: wrote {OUT.name}")
  for e in errs:
    print(f"fig_lifecycle: warning: {e}", file=sys.stderr)
  return 0


if __name__ == "__main__":
  sys.exit(main(sys.argv[1:]))
