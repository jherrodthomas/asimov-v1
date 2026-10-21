#!/usr/bin/env python3
"""Drawing kit shared by the generated assurance figures: palette, SVG helpers and Markdown table parsing.

Used by fig_m_management.py and fig_m_plans.py (01-management) and by 07-supporting/figures/fig_p_process.py
(through fig_m_management). Standard library only; every function is deterministic.
"""

from __future__ import annotations

import re
from xml.sax.saxutils import escape

# ---------------------------------------------------------------- palette (assurance figure style)

FONT = "Inter, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, monospace"
INK, MUTED, FAINT, LINE, HAIR = "#0F172A", "#475569", "#94A3B8", "#CBD5E1", "#E2E8F0"
CHIP = "#F8FAFC"
SAFETY, SAFETY_BG = "#C2410C", "#FFF7ED"
SW, SW_BG = "#0F766E", "#F0FDFA"
HW, HW_BG = "#4F46E5", "#EEF2FF"
GREEN, GREEN_BG = "#2E9E6A", "#ECFDF5"
AMBER, AMBER_BG = "#D97706", "#FFFBEB"
RED, RED_BG = "#D2553F", "#FEF2F2"
GREY_BG = "#F1F5F9"


class FigureError(Exception):
  pass


# ---------------------------------------------------------------- SVG helpers

def el(tag: str, text: str | None = None, **attrs) -> str:
  """One SVG element; attribute names use _ for - (stroke_width -> stroke-width), a trailing _ is dropped."""
  a = "".join(f' {k.rstrip("_").replace("_", "-")}="{v}"' for k, v in attrs.items() if v not in ("", None))
  return f"<{tag}{a}/>" if text is None else f"<{tag}{a}>{escape(text)}</{tag}>"


def fmt(v: float) -> str:
  return f"{v:.1f}".rstrip("0").rstrip(".")


def text(x, y, s, size=11, fill=INK, weight="", anchor="", family="", style="", deco="") -> str:
  return el("text", s, x=fmt(x), y=fmt(y), font_size=size, fill=fill, font_weight=weight, text_anchor=anchor,
            font_family=family, font_style=style, text_decoration=deco)


def rect(x, y, w, h, fill="#FFFFFF", stroke=LINE, sw=1.2, rx=8, dash="", opacity="") -> str:
  return el("rect", None, x=fmt(x), y=fmt(y), width=fmt(w), height=fmt(h), rx=rx, fill=fill, stroke=stroke,
            stroke_width=sw, stroke_dasharray=dash, opacity=opacity)


def line(x1, y1, x2, y2, stroke=MUTED, sw=1.4, dash="") -> str:
  return el("line", None, x1=fmt(x1), y1=fmt(y1), x2=fmt(x2), y2=fmt(y2), stroke=stroke, stroke_width=sw,
            stroke_dasharray=dash)


def path(d, stroke=MUTED, sw=1.4, fill="none", dash="") -> str:
  return el("path", None, d=d, stroke=stroke, stroke_width=sw, fill=fill, stroke_dasharray=dash,
            stroke_linejoin="round")


HATCH = ('<pattern id="hatch" patternUnits="userSpaceOnUse" width="6" height="6" patternTransform="rotate(45)">' +
         f'<rect width="6" height="6" fill="{GREY_BG}"/><line x1="0" y1="0" x2="0" y2="6" stroke="{LINE}" ' +
         'stroke-width="2"/></pattern>')


def svg(width: int, height: int, title: str, desc: str, body: list[str]) -> str:
  head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" ' +
          f'font-family="{FONT}" role="img">')
  return "\n".join([head, el("title", title), el("desc", desc), f"<defs>{HATCH}</defs>",
                    rect(0, 0, width, height, fill="#FFFFFF", stroke="none", rx=0, sw=0), *body, "</svg>"]) + "\n"


def header(width: int, number: str, title: str, subtitle: str, ref: str) -> list[str]:
  return [text(40, 44, f"Figure {number} · {title}", size=20, weight=700),
          text(40, 66, subtitle, size=12.5, fill=MUTED),
          text(width - 40, 44, ref, size=11, fill=MUTED, anchor="end"),
          line(40, 82, width - 40, 82, stroke=HAIR, sw=1)]


def legend(x: float, y: float, entries: list[tuple[str, str, str]]) -> tuple[list[str], float]:
  """entries: (fill, stroke, label); a stroke ending in ' dashed' is drawn dashed. Returns (svg, end x)."""
  out = []
  for fill, stroke, label in entries:
    dash = ""
    if stroke.endswith(" dashed"):
      stroke, dash = stroke[:-7], "3 2"
    out.append(rect(x, y - 10, 14, 12, fill=fill, stroke=stroke, rx=3, dash=dash))
    out.append(text(x + 20, y, label, size=11, fill=MUTED))
    x += 34 + text_w(label, 11)
  return out, x


def text_w(s: str, size: float, bold: bool = False) -> float:
  """Rough rendered width of s (Inter-like metrics)."""
  w = 0.0
  for ch in s:
    if ch in "il.,:;'|!·":
      w += 0.28
    elif ch in "fjrt() -/":
      w += 0.36
    elif ch.isupper() or ch in "mwMW≥≤–—…→×":
      w += 0.70
    elif ch.isdigit():
      w += 0.56
    else:
      w += 0.55
  return w * size * (1.06 if bold else 1.0)


def fit(s: str, width: float, size: float, bold: bool = False) -> str:
  """s, cut at a word boundary with an ellipsis when it is wider than width."""
  if text_w(s, size, bold) <= width:
    return s
  words, out = s.split(), ""
  for wd in words:
    cand = (out + " " + wd).strip()
    if text_w(cand + " …", size, bold) > width:
      break
    out = cand
  return out.rstrip(",;:(") + " …"


def pill(x, y, label, fill, color="#FFFFFF", h=16, size=9.5, stroke="none", dash="") -> tuple[list[str], float]:
  w = text_w(label, size, True) + 12
  return [rect(x, y, w, h, fill=fill, stroke=stroke, rx=h / 2, sw=1, dash=dash),
          text(x + w / 2, y + h / 2 + size * 0.36, label, size=size, fill=color, weight=700, anchor="middle")], w


# ---------------------------------------------------------------- Markdown parsing

def split_row(row: str) -> list[str]:
  """Cells of a Markdown table row (same rule as assurance/trace/tools/trace_map.split_row)."""
  cells = re.split(r"(?<!\\)\|", row.strip())
  return [c.strip() for c in cells[1:-1]]


def section(md: str, heading: str) -> str:
  """Body of the section whose heading line starts with heading, up to the next heading of the same or higher level."""
  level = len(heading) - len(heading.lstrip("#"))
  m = re.search(rf"^{re.escape(heading)}.*$", md, re.M)
  if not m:
    raise FigureError(f"heading not found: {heading}")
  rest = md[m.end():]
  end = re.search(rf"^#{{1,{level}}} ", rest, re.M)
  return rest[:end.start()] if end else rest


def table(body: str, first: str | None = None) -> tuple[list[str], list[list[str]]]:
  """(header cells, data rows) of the first Markdown table in body (whose header starts with `first`)."""
  lines = body.splitlines()
  for i, ln in enumerate(lines):
    if ln.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s\-:|]+\|$", lines[i + 1]):
      head = split_row(ln)
      if first and head[0] != first:
        continue
      rows = []
      for r in lines[i + 2:]:
        if not r.startswith("|"):
          break
        rows.append(split_row(r))
      return head, rows
  raise FigureError(f"no table{' ' + first if first else ''} found")


def col(head: list[str], name: str) -> int:
  if name not in head:
    raise FigureError(f"column {name!r} not in {head}")
  return head.index(name)


def plain(s: str) -> str:
  """Markdown cell text without links, emphasis and code ticks."""
  s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
  return re.sub(r"[*`]", "", s).strip()
