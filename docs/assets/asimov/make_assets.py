#!/usr/bin/env python3
"""Render the README and wiki figures of the Asimov v1 assurance record as SVG.

Eight figures, one style: hero.svg (banner), standards.svg (one question per standard), architecture.svg
(three layers and the assurance column), roadmap.svg (four phases, status from repository evidence),
lifecycle.svg (the seven gates and where the project stands), status.svg (the record-status card),
standards-map.svg (which standard shapes which phase, counted from the register) and repo-map.svg (how the
code, the record and what is generated from it fit together). The first five and the repository map are drawn
from the data at the top of this file; status.svg, the standards map and the README headline block between
the `record-headline` markers are computed from the records themselves (the work product register, the gap
assessment, the decision register, the process model, the gate and confirmation records). Nothing is typed by
hand, so a change to the data is a change to the figure and CI checks that the committed copies and the README
block match (`--check`).

Usage: python3 docs/assets/asimov/make_assets.py [--out DIR | --check]
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import math
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ASSURANCE = ROOT / "assurance"
README = ROOT / "README.md"
NAMES = ("hero.svg", "standards.svg", "architecture.svg", "roadmap.svg", "lifecycle.svg", "status.svg", "standards-map.svg", "repo-map.svg")
HEADLINE_BEGIN = "<!-- BEGIN GENERATED: record-headline (docs/assets/asimov/make_assets.py) -->"
HEADLINE_END = "<!-- END GENERATED: record-headline -->"

FONT = "Inter, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, monospace"
C = {
  # light theme: white card with a pale gradient, teal and amber accents dark enough to read on white
  "bg1": "#FFFFFF", "bg2": "#F3F7F8", "panel": "#EDF2F4", "panel2": "#F7FAFB", "stroke": "#D3DDE2",
  "amber": "#D4821A", "amber_hi": "#F2A33A", "amber_lo": "#A8650F", "cyan": "#0E8C83", "cyan_lo": "#8FD8D1",
  "text": "#122026", "muted": "#4E6A73", "dim": "#7E949B", "red": "#D64535", "green": "#2C9A58", "white": "#FFFFFF",
  "ink": "#122026",
}

# ------------------------------------------------------------------ data

TAGLINE = "An open humanoid. Engineered for safety."
CHIPS = ["ISO 12100", "ISO 10218", "ISO 13482", "ISO 13849-1", "IEC 62443", "Machinery Reg. (EU) 2023/1230"]

STANDARDS = [
  ("ISO 12100", "Risk assessment and reduction", "What could hurt someone, and how much risk reduction does it need?", "Machine limits, hazard identification, risk estimation, the three-step method"),
  ("ISO 10218-1 / -2 · TS 15066", "Industrial and collaborative robots", "Which safety functions must a robot have, and how hard may it touch?", "Emergency stop, protective stop, speed and separation, power and force limits, collaborative modes"),
  ("ISO 13482", "Personal care robots", "What does a robot that shares space with people have to show?", "Hazard catalogue for mobile servant robots, stability and falls, contact, verification and validation in §7"),
  ("ISO 13849-1 / -2", "Safety-related parts of control systems", "How reliable must the control system be, and how is that shown?", "Required Performance Level, categories, MTTFD, DCavg, CCF, validation"),
  ("IEC 60204-1 · ISO 13850 · IEC 62133-2", "Electrical equipment, emergency stop, battery", "Is the electrical installation safe, does the E-stop work, is the battery safe?", "Supply disconnection, overcurrent, stop categories, E-stop devices, lithium-ion cell and pack safety"),
  ("IEC 62443-4-1 / -4-2", "Cybersecurity", "What if someone attacks it over the tele-operation link?", "Secure development lifecycle, zones and conduits, security level target"),
  ("ISO/IEC TR 5469", "AI in safety functions", "How far can the learned locomotion policy be trusted?", "Technology classes, usage levels; here: whether balance may rest on a learned component is a decision"),
  ("UL 4600 · Machinery Reg.", "Safety case and conformity", "Is the whole argument convincing, and what does the law require?", "Claims, evidence, defeaters; Annex III requirements, Annex I Part A for learned safety behaviour, Annex IV technical file"),
]

LAYERS = [
  ("LAYER 1 · INHERITED FROM ASIMOV V1, HARDENED AS DEFENCE IN DEPTH", "Tele-operation stack and locomotion policy", "Raspberry Pi 5 · no Performance Level claim",
   [("WebRTC video and operator link", "inherited"), ("Asimov API (pre-1.0)", "inherited"), ("Learned locomotion policy, unreleased", "proposed"),
    ("Authenticated, bounded commands", "hardened"), ("Rate and range limits before the bus", "hardened"), ("Pinned builds, signed updates", "hardened")]),
  ("LAYER 2 · THE LAST SOFTWARE BEFORE THE MOTORS", "Deterministic safety layer on the motion control board", "Radxa CM5 · PL d target for the clamps, the watchdog and the controlled descent",
   [("Joint torque and velocity clamps (SF-03)", "chain"), ("IMU plausibility and cross-check (SF-23)", "chain"), ("Scheduler watchdog and deadline monitor (SF-24)", "chain"),
    ("Controlled descent on fault (SF-02)", "chain"), ("Mode machine DAMP · STAND · MOVE", "hardened"), ("Software joint limits inside the end-stops (SF-25)", "hardened")]),
  ("LAYER 3 · HARDWIRED STOP CHAIN, THE CHECKER OF LAST RESORT", "Safety-related control system", "PL d target · ISO 13849-1 · nothing in software can hold a contactor closed",
   [("Dual-channel wired E-stop pendant", "chain"), ("Safety relay with monitored reset", "chain"), ("Actuator-rail contactors", "chain"),
    ("E-stop link surveillance (SF-13)", "chain"), ("Fuse table and disconnect", "chain"), ("Tether and gantry in the laboratory", "proposed")]),
]
ASSURANCE_COLUMN = ["Item definition and risk assessment", "Safety functions and required PL", "SRP/CS architecture and PL calculation",
                    "Fall, descent, contact and E-stop validation", "Cybersecurity threat assessment", "Safety case and technical file",
                    "Decision register and gates"]
LEGEND = [("inherited", "Inherited, functional only"), ("hardened", "Hardened by the fork (proposed)"), ("chain", "To be built, PL d target"), ("proposed", "Proposed, not yet in any repository")]

# Standards map: a work product cites a standard when one of its WP-M-00 clause cells matches the pattern.
STANDARD_PATTERNS = [
  ("ISO 12100", "risk assessment", r"12100"),
  ("ISO 10218 · TS 15066", "robots, collaborative", r"10218|15066"),
  ("ISO 13482", "personal care robots", r"13482"),
  ("ISO 13849-1 / -2", "safety-related control", r"13849"),
  ("IEC 62061 · IEC 61508", "where 13849 runs out", r"62061|61508"),
  ("IEC 60204-1", "electrical equipment", r"60204"),
  ("ISO 13850 · ISO 13857", "E-stop, reach distances", r"13850|13857"),
  ("IEC 62133-2 · UN 38.3", "battery safety", r"62133|38\.3"),
  ("IEC 62443-4-1 / -4-2", "cybersecurity", r"62443"),
  ("ISO/IEC TR 5469", "AI in safety functions", r"5469"),
  ("ISO 21448 (method)", "performance limits", r"21448"),
  ("Machinery Regulation", "(EU) 2023/1230", r"Machinery Reg"),
  ("AI Act", "(EU) 2024/1689", r"AI Act"),
  ("UL 4600", "safety case", r"4600"),
  ("Automotive SPICE", "process capability", r"\b(SYS|SWE|SUP|MAN|ACQ|HWE|MLE|VAL)\.\d"),
]

# Repository map: the three columns of the figure and the arrows between them.
REPO_CODE = [("mechanical/", "CAD of the seven subassemblies, structure, end-stops", "SR-Q"),
             ("electrical/", "Motion control board (KiCad), harness, power and CAN", "SR-A"),
             ("sim-model/", "MuJoCo model: masses, joint ranges, control ranges", "SR-Q")]
REPO_RECORD = [("00", "assessment", "gaps, concept package"), ("01", "management", "strategy, plans, decisions"), ("02", "concept", "risk assessment, SF, PLr"),
               ("03", "system", "SRS, chain architecture"), ("04", "hardware", "chain, PL calculation"), ("05", "software", "safety layer, policy"),
               ("06", "validation", "tests, hold point"), ("07", "supporting", "CM, change, review"), ("08", "analyses", "FMEA, FTA, STPA"),
               ("09", "operation", "commissioning, field"), ("10", "safety-case", "case, tech file, gates"),
               ("process/", "model", "activities, lanes, gates"), ("trace/", "items", "hazards, SF, AoU"), ("case/", "records", "claims, evidence, defeaters")]
REPO_OUTPUTS = [("README figures and status card", "make_assets.py", "docs/assets/asimov/"),
                ("Living Safety Case dashboard", "generate_dashboard.py", "docs/assets/assurance/"),
                ("Process maps, swimlanes, gate skeletons", "process_model.py · process_figures.py", "process/maps/ · gates/skeletons/"),
                ("Folder indexes", "folder_index.py", "assurance/*/README.md"),
                ("Decision inbox page", "build_inbox.py", "a private page for the lead"),
                ("GitHub wiki", "build_wiki.py", "wiki/ mirrored on merge")]

ROADMAP = [
  ("01", "Foundation", "ACTIVE", ["Governance and safety plan", "Baseline gap assessment", "Work product register", "Integrated process model", "Decision register"]),
  ("02", "Safety Engineering", "ACTIVE", ["Item definition and risk assessment", "Safety functions and required PL", "Safe state and fall-arrest concept", "Cybersecurity threat assessment", "Test operations hold point"]),
  ("03", "Build and Verify", "PLANNED", ["Gantry, wired E-stop, bench supply", "Deterministic safety layer", "Chain design and PL calculation", "Fall, descent and contact tests", "Fault injection"]),
  ("04", "Validate and Release", "PLANNED", ["Validation on the robot", "Independent assessment", "Technical documentation", "Declaration of conformity draft", "Field monitoring"]),
]

GATES = [("G0", "Governance", "P0"), ("G1", "Concept", "P1"), ("G2", "System design", "P2"), ("G3", "HW/SW development", "P3"),
         ("G4", "Integration and verification", "P4"), ("G5", "Validation and release", "P5"), ("G6", "Operation", "P6")]
TODAY_PHASE = "P1"
HOLD_POINTS = {"G1": "no powered floor test before the gantry, the wired E-stop and WP-V-07", "G4": "no person within reach before WP-V-03 passes"}


# ------------------------------------------------------------------ helpers

def text(x, y, s, size, fill=C["text"], weight=400, anchor="start", family=FONT, extra=""):
  return (f'<text x="{x:g}" y="{y:g}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
          f'fill="{fill}" text-anchor="{anchor}"{extra}>{escape(s)}</text>')


def rect(x, y, w, h, fill, r=0, stroke="", sw=1, opacity=None, dash=""):
  st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
  op = f' fill-opacity="{opacity}"' if opacity is not None else ""
  da = f' stroke-dasharray="{dash}"' if dash else ""
  return f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{r:g}" fill="{fill}"{st}{op}{da}/>'


def wrap(s, width, size):
  per = width / (size * 0.52)
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


def card_bg(w, h, gid):
  return "\n".join([
    f'<linearGradient id="{gid}-bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{C["bg1"]}"/><stop offset="1" stop-color="{C["bg2"]}"/></linearGradient>',
    f'<linearGradient id="{gid}-amber" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C["amber_lo"]}"/><stop offset="0.5" stop-color="{C["amber_hi"]}"/><stop offset="1" stop-color="{C["amber_lo"]}"/></linearGradient>',
  ]), "\n".join([
    f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="22" fill="url(#{gid}-bg)" stroke="{C["stroke"]}"/>',
    f'<rect x="40" y="0" width="{w - 80}" height="3" fill="url(#{gid}-amber)"/>',
  ])


def svg(w, h, gid, title, desc, defs, body):
  return "\n".join([
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="{gid}-t {gid}-d">',
    f'  <title id="{gid}-t">{escape(title)}</title>',
    f'  <desc id="{gid}-d">{escape(desc)}</desc>',
    "  <defs>", defs, "  </defs>", body, "</svg>", ""])


def heading(x, label, title, right=""):
  out = [text(x, 56, label, 15, C["amber"], 700, extra=' letter-spacing="3"'), text(x, 94, title, 28, C["text"], 700)]
  if right:
    out.append(text(960, 56, right, 12, C["muted"], anchor="end"))
  return "\n".join(out)


# ------------------------------------------------------------------ hero

def robot_emblem(cx, cy, s=1.0):
  """A geometric biped on a tether: gantry beam and rope, head with camera, torso, two arms, two legs, a red E-stop pendant."""
  g = []
  # fall radius on the floor
  g.append(f'<ellipse cx="{cx:g}" cy="{cy + 150 * s:g}" rx="{200 * s:g}" ry="{44 * s:g}" fill="{C["cyan"]}" fill-opacity="0.06" stroke="{C["cyan"]}" stroke-opacity="0.55" stroke-width="1.6" stroke-dasharray="8 6"/>')
  g.append(f'<ellipse cx="{cx:g}" cy="{cy + 150 * s:g}" rx="{70 * s:g}" ry="{16 * s:g}" fill="{C["cyan"]}" fill-opacity="0.08" stroke="{C["cyan"]}" stroke-opacity="0.8" stroke-width="1.6"/>')
  # gantry beam and tether
  g.append(f'<rect x="{cx - 170 * s:g}" y="{cy - 232 * s:g}" width="{340 * s:g}" height="{12 * s:g}" rx="3" fill="#36515B" stroke="{C["stroke"]}"/>')
  g.append(f'<rect x="{cx - 14 * s:g}" y="{cy - 220 * s:g}" width="{28 * s:g}" height="{14 * s:g}" rx="3" fill="{C["amber"]}"/>')
  g.append(f'<line x1="{cx:g}" y1="{cy - 206 * s:g}" x2="{cx:g}" y2="{cy - 108 * s:g}" stroke="{C["cyan"]}" stroke-width="{3 * s:g}" stroke-dasharray="6 4"/>')
  g.append(f'<path d="M{cx - 22 * s:g},{cy - 92 * s:g} L{cx:g},{cy - 108 * s:g} L{cx + 22 * s:g},{cy - 92 * s:g}" fill="none" stroke="{C["cyan"]}" stroke-width="{3 * s:g}"/>')
  # head with camera
  g.append(f'<rect x="{cx - 26 * s:g}" y="{cy - 176 * s:g}" width="{52 * s:g}" height="{48 * s:g}" rx="{14 * s:g}" fill="#2B4A54" stroke="{C["cyan"]}"/>')
  g.append(f'<rect x="{cx - 16 * s:g}" y="{cy - 162 * s:g}" width="{32 * s:g}" height="{12 * s:g}" rx="6" fill="{C["cyan"]}" fill-opacity="0.9"/>')
  g.append(f'<rect x="{cx - 8 * s:g}" y="{cy - 128 * s:g}" width="{16 * s:g}" height="{14 * s:g}" fill="#A9C4CB"/>')
  # torso
  g.append(f'<rect x="{cx - 40 * s:g}" y="{cy - 114 * s:g}" width="{80 * s:g}" height="{120 * s:g}" rx="{18 * s:g}" fill="url(#hero-body)" stroke="{C["amber_lo"]}" stroke-width="1.5"/>')
  g.append(f'<rect x="{cx - 24 * s:g}" y="{cy - 90 * s:g}" width="{48 * s:g}" height="{8 * s:g}" rx="4" fill="{C["bg2"]}" fill-opacity="0.4"/>')
  g.append(f'<rect x="{cx - 24 * s:g}" y="{cy - 74 * s:g}" width="{48 * s:g}" height="{8 * s:g}" rx="4" fill="{C["bg2"]}" fill-opacity="0.4"/>')
  # waist
  g.append(f'<rect x="{cx - 30 * s:g}" y="{cy + 6 * s:g}" width="{60 * s:g}" height="{18 * s:g}" rx="6" fill="#36515B" stroke="{C["stroke"]}"/>')
  # arms
  for side in (-1, 1):
    sx = cx + side * 40 * s
    g.append(f'<path d="M{sx:g},{cy - 96 * s:g} L{sx + side * 34 * s:g},{cy - 36 * s:g} L{sx + side * 48 * s:g},{cy + 26 * s:g}" fill="none" stroke="#A9C4CB" stroke-width="{13 * s:g}" stroke-linecap="round" stroke-linejoin="round"/>')
    g.append(f'<path d="M{sx:g},{cy - 96 * s:g} L{sx + side * 34 * s:g},{cy - 36 * s:g} L{sx + side * 48 * s:g},{cy + 26 * s:g}" fill="none" stroke="{C["panel"]}" stroke-width="{6 * s:g}" stroke-linecap="round" stroke-linejoin="round"/>')
    g.append(f'<circle cx="{sx + side * 34 * s:g}" cy="{cy - 36 * s:g}" r="{7 * s:g}" fill="{C["amber"]}"/>')
    g.append(f'<rect x="{sx + side * 48 * s - 9 * s:g}" y="{cy + 22 * s:g}" width="{18 * s:g}" height="{22 * s:g}" rx="4" fill="#A9C4CB"/>')
  # legs
  for side in (-1, 1):
    hx = cx + side * 18 * s
    g.append(f'<path d="M{hx:g},{cy + 22 * s:g} L{hx + side * 6 * s:g},{cy + 84 * s:g} L{hx + side * 2 * s:g},{cy + 144 * s:g}" fill="none" stroke="#A9C4CB" stroke-width="{16 * s:g}" stroke-linecap="round" stroke-linejoin="round"/>')
    g.append(f'<path d="M{hx:g},{cy + 22 * s:g} L{hx + side * 6 * s:g},{cy + 84 * s:g} L{hx + side * 2 * s:g},{cy + 144 * s:g}" fill="none" stroke="{C["panel"]}" stroke-width="{8 * s:g}" stroke-linecap="round" stroke-linejoin="round"/>')
    g.append(f'<circle cx="{hx + side * 6 * s:g}" cy="{cy + 84 * s:g}" r="{7 * s:g}" fill="{C["amber"]}"/>')
    g.append(f'<rect x="{hx + side * 2 * s - 14 * s + (side * 6 * s):g}" y="{cy + 140 * s:g}" width="{34 * s:g}" height="{12 * s:g}" rx="4" fill="#36515B" stroke="{C["stroke"]}"/>')
  # the operator's E-stop pendant, on a lead to the right
  g.append(f'<path d="M{cx + 200 * s:g},{cy + 96 * s:g} C{cx + 150 * s:g},{cy + 60 * s:g} {cx + 110 * s:g},{cy + 50 * s:g} {cx + 40 * s:g},{cy - 30 * s:g}" fill="none" stroke="{C["red"]}" stroke-opacity="0.6" stroke-width="2"/>')
  g.append(f'<rect x="{cx + 178 * s:g}" y="{cy + 88 * s:g}" width="{44 * s:g}" height="{30 * s:g}" rx="8" fill="#2B4A54" stroke="{C["stroke"]}"/>')
  g.append(f'<circle cx="{cx + 200 * s:g}" cy="{cy + 103 * s:g}" r="{9 * s:g}" fill="{C["red"]}" stroke="#7A2A22" stroke-width="2"/>')
  g.append(f'<circle cx="{cx + 200 * s:g}" cy="{cy + 103 * s:g}" r="{14 * s:g}" fill="none" stroke="{C["amber_hi"]}" stroke-width="1.2"/>')
  return "\n".join(g)


def hero_svg():
  w, h = 1280, 520
  defs = "\n".join([
    f'<radialGradient id="hero-bg" cx="0.72" cy="0.45" r="0.95"><stop offset="0" stop-color="#D9EEF0"/><stop offset="0.55" stop-color="{C["bg1"]}"/><stop offset="1" stop-color="{C["bg2"]}"/></radialGradient>',
    f'<linearGradient id="hero-body" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["amber_hi"]}"/><stop offset="1" stop-color="{C["amber_lo"]}"/></linearGradient>',
    f'<linearGradient id="hero-amber" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C["amber_lo"]}"/><stop offset="0.5" stop-color="{C["amber_hi"]}"/><stop offset="1" stop-color="{C["amber_lo"]}"/></linearGradient>',
    f'<linearGradient id="hero-fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["cyan"]}" stop-opacity="0"/><stop offset="1" stop-color="{C["cyan"]}" stop-opacity="0.3"/></linearGradient>',
    '<clipPath id="hero-frame"><rect width="1280" height="520" rx="24"/></clipPath>',
  ])
  body = ['<g clip-path="url(#hero-frame)">', f'<rect width="{w}" height="{h}" fill="url(#hero-bg)"/>']
  # floor grid in perspective, vanishing point right of centre
  vx, vy = 980, 300
  for i in range(-9, 13):
    body.append(f'<line x1="{vx}" y1="{vy}" x2="{vx + i * 170}" y2="{h}" stroke="url(#hero-fade)" stroke-width="1"/>')
  for k in range(1, 9):
    y = vy + (h - vy) * (k / 8) ** 1.9
    half = (y - vy) * 7.5
    body.append(f'<line x1="{vx - half:g}" y1="{y:g}" x2="{vx + half:g}" y2="{y:g}" stroke="{C["cyan"]}" stroke-opacity="{0.05 + 0.03 * k:.2f}" stroke-width="1"/>')
  body.append(f'<line x1="660" y1="{vy}" x2="{w}" y2="{vy}" stroke="{C["cyan"]}" stroke-opacity="0.25"/>')
  # emblem
  body.append(robot_emblem(990, 270, 1.0))
  # title block
  body.append(text(72, 150, "ASIMOV V1 ASSURANCE", 18, C["amber"], 700, extra=' letter-spacing="6"'))
  body.append(text(72, 218, "An open humanoid.", 52, C["text"], 800, extra=' letter-spacing="-1"'))
  body.append(text(72, 278, "Engineered for safety.", 52, C["amber"], 800, extra=' letter-spacing="-1"'))
  lines = wrap("The engineering assurance record for a safety-assured fork of the Asimov v1 humanoid: robot risk assessment, a deterministic safety layer and a hardwired stop chain with a Performance Level target, and a safety case published as it is built.", 560, 17)
  for i, ln in enumerate(lines):
    body.append(text(72, 320 + i * 25, ln, 17, C["muted"]))
  x = 72
  for chip in CHIPS:
    cw = 11 + len(chip) * 8.2
    body.append(rect(x, 404, cw, 30, C["panel"], r=15, stroke=C["stroke"]))
    body.append(text(x + cw / 2, 424, chip, 13, C["text"], 600, anchor="middle", family=MONO))
    x += cw + 10
  body.append(text(72, 474, "Standards-informed engineering · no compliance claimed · nothing approved for operation around people", 13, C["dim"]))
  body.append("</g>")
  desc = ("Asimov v1 assurance banner: a geometric biped in amber hanging from a gantry on a cyan tether, with a camera head, a red emergency-stop pendant on a lead and a dashed fall radius on a "
          "perspective floor grid, beside the project name and the tagline " + TAGLINE + " Chips name the standards: " + ", ".join(CHIPS) + ".")
  return svg(w, h, "hero", "Asimov v1 assurance: " + TAGLINE, desc, defs, "\n".join(body))


# ------------------------------------------------------------------ standards

def standards_svg():
  w = 1000
  row_h, top = 70, 124
  h = top + len(STANDARDS) * (row_h + 10) + 36
  defs, frame = card_bg(w, h, "std")
  body = [frame, heading(40, "STANDARDS-INFORMED ENGINEERING", "One question per standard", "Aligned practices, not a compliance claim")]
  y = top
  for name, sub, question, scope in STANDARDS:
    body.append(rect(40, y, 920, row_h, C["panel"], r=14, stroke=C["stroke"]))
    body.append(rect(40, y + 18, 3, row_h - 36, C["amber"], r=1.5))
    body.append(text(64, y + 30, name, 18, C["amber"], 700))
    body.append(text(64, y + 52, sub, 13, C["muted"], 500))
    body.append(text(330, y + 30, question, 17, C["text"], 600))
    body.append(text(330, y + 52, scope, 13, C["muted"]))
    y += row_h + 10
  body.append(text(40, h - 14, "Every clause reference is marked to be checked against a licensed copy; how each standard is used is WP-M-01 §4.", 12, C["dim"]))
  desc = "Standards the engineering framework draws on. " + " ".join(f"{n} ({s}): {q}" for n, s, q, _ in STANDARDS) + " Aligned practices, not a claim of compliance."
  return svg(w, h, "std", "Standards-informed engineering framework", desc, defs, "\n".join(body))


# ------------------------------------------------------------------ architecture

STATE_STYLE = {
  "inherited": (C["cyan"], 0.12, C["cyan"], ""),
  "hardened": (C["amber"], 0.14, C["amber"], ""),
  "chain": (C["amber"], 0.28, C["amber_hi"], ""),
  "proposed": (C["muted"], 0.08, C["muted"], "5 4"),
}


def architecture_svg():
  w = 1000
  left_w, col_x, col_w = 640, 704, 256
  y = 124
  layer_boxes = []
  layer_tops = []
  for label, title, sub, items in LAYERS:
    cols = 3
    rows = math.ceil(len(items) / cols)
    lh = 96 + rows * 56
    layer_tops.append((y, lh))
    y += lh + 30
  h = y + 70
  defs, frame = card_bg(w, h, "arch")
  body = [frame, heading(40, "PLATFORM ARCHITECTURE", "Three layers, one checker of last resort")]
  for (label, title, sub, items), (ly, lh) in zip(LAYERS, layer_tops, strict=True):
    strong = title.startswith("Safety-related")
    body.append(rect(40, ly, left_w, lh, C["panel"], r=16, stroke=C["amber"] if strong else C["stroke"], sw=1.6 if strong else 1))
    body.append(text(60, ly + 26, label, 11, C["amber"], 700, extra=' letter-spacing="2"'))
    body.append(text(60, ly + 50, title, 19, C["text"], 700))
    body.append(text(60, ly + 70, sub, 12, C["muted"]))
    bw, bh, gap = 192, 46, 12
    for i, (name, state) in enumerate(items):
      bx = 60 + (i % 3) * (bw + gap)
      by = ly + 84 + (i // 3) * (bh + 10)
      fill, op, stroke, dash = STATE_STYLE[state]
      body.append(rect(bx, by, bw, bh, fill, r=9, stroke=stroke, opacity=op, dash=dash))
      lines = wrap(name, bw - 16, 12)
      for j, ln in enumerate(lines[:2]):
        body.append(text(bx + bw / 2, by + (29 if len(lines) == 1 else 21 + j * 15), ln, 12, C["text"], 500, anchor="middle"))
    layer_boxes.append((ly, lh))
  # arrows between layers
  for (ly, lh), (ny, _) in zip(layer_boxes, layer_boxes[1:], strict=False):
    mid = 40 + left_w / 2
    body.append(f'<line x1="{mid}" y1="{ly + lh}" x2="{mid}" y2="{ny - 2}" stroke="{C["muted"]}" stroke-width="1.6"/>')
    body.append(f'<polygon points="{mid - 6},{ny - 10} {mid + 6},{ny - 10} {mid},{ny - 2}" fill="{C["muted"]}"/>')
    body.append(text(mid + 14, ly + lh + 19, "requests, never authority", 11, C["dim"]))
  ly, lh = layer_boxes[-1]
  body.append(text(40 + left_w / 2, ly + lh + 26, "actuator power and brakes: removed by the chain, not by software", 12, C["amber_hi"], 600, anchor="middle"))
  # assurance column
  top, bottom = layer_boxes[0][0], layer_boxes[-1][0] + layer_boxes[-1][1]
  body.append(rect(col_x, top, col_w, bottom - top, C["panel2"], r=16, stroke=C["stroke"], dash="6 4"))
  body.append(text(col_x + 18, top + 26, "CROSS-CUTTING · ALL DRAFTS", 11, C["amber"], 700, extra=' letter-spacing="1.5"'))
  body.append(text(col_x + 18, top + 50, "Safety and assurance", 19, C["text"], 700))
  cy = top + 78
  for item in ASSURANCE_COLUMN:
    body.append(rect(col_x + 18, cy, col_w - 36, 40, C["amber"], r=8, stroke=C["amber"], opacity=0.08))
    lines = wrap(item, col_w - 52, 12)
    for j, ln in enumerate(lines[:2]):
      body.append(text(col_x + col_w / 2, cy + (25 if len(lines) == 1 else 18 + j * 14), ln, 12, C["text"], 500, anchor="middle"))
    cy += 50
  body.append(text(col_x + col_w / 2, bottom - 14, "applies to every layer", 11, C["dim"], anchor="middle"))
  # legend
  lx = 40
  for state, label in LEGEND:
    fill, op, stroke, dash = STATE_STYLE[state]
    body.append(rect(lx, h - 40, 16, 16, fill, r=4, stroke=stroke, opacity=op, dash=dash))
    body.append(text(lx + 24, h - 27, label, 12, C["muted"]))
    lx += 36 + len(label) * 6.6
  desc = ("Architecture diagram. " + " ".join(f"{t} ({s}): " + ", ".join(n for n, _ in it) + "." for _, t, s, it in LAYERS)
          + " A cross-cutting safety and assurance column of draft work products applies to every layer: " + ", ".join(ASSURANCE_COLUMN)
          + ". Legend: " + "; ".join(l for _, l in LEGEND) + ".")
  return svg(w, h, "arch", "Asimov v1 platform architecture", desc, defs, "\n".join(body))


# ------------------------------------------------------------------ roadmap

def roadmap_svg():
  w = 1000
  cw, gap = 218, 16
  wrapped = [[wrap(it, cw - 56, 13) for it in items] for _, _, _, items in ROADMAP]
  card_h = max(160 + sum(len(ls) for ls in col) * 17 + len(col) * 12 for col in wrapped)
  h = 180 + card_h + 50
  defs, frame = card_bg(w, h, "road")
  body = [frame, heading(40, "ROADMAP", "Four phases, status from repository evidence")]
  n = len(ROADMAP)
  x0 = 40
  cx = [x0 + i * (cw + gap) + cw / 2 for i in range(n)]
  body.append(f'<line x1="{cx[0]}" y1="150" x2="{cx[-1]}" y2="150" stroke="{C["stroke"]}" stroke-width="2"/>')
  for i, (num, name, status, items) in enumerate(ROADMAP):
    active = status == "ACTIVE"
    col = C["cyan"] if active else C["dim"]
    body.append(f'<circle cx="{cx[i]}" cy="150" r="11" fill="{C["bg2"]}" stroke="{col}" stroke-width="2.5"/>')
    body.append(f'<circle cx="{cx[i]}" cy="150" r="5" fill="{col}"/>')
    x = x0 + i * (cw + gap)
    body.append(rect(x, 180, cw, card_h, C["panel"], r=14, stroke=col, opacity=None if active else 0.7, sw=1.2))
    body.append(text(x + 20, 214, f"PHASE {num}", 13, C["amber"], 700, extra=' letter-spacing="2"'))
    for j, ln in enumerate(wrap(name, cw - 40, 19)):
      body.append(text(x + 20, 242 + j * 22, ln, 19, C["text"], 700))
    by = 290
    body.append(rect(x + 20, by, 84, 24, col, r=12, stroke=col, opacity=0.12))
    body.append(text(x + 62, by + 16.5, status, 12, col, 600, anchor="middle", extra=' letter-spacing="1.2"'))
    iy = 340
    for lines in wrapped[i]:
      body.append(rect(x + 20, iy - 8, 6, 6, col, r=1))
      for ln in lines:
        body.append(text(x + 36, iy, ln, 13, C["muted"]))
        iy += 17
      iy += 12
  body.append(text(40, h - 16, "\"Active\" means work products exist as drafts or skeletons; nothing is marked complete before its review. The gates are in WP-M-00 §2.", 12, C["dim"]))
  desc = "Roadmap. " + " ".join(f"Phase {n_}, {name} ({s.title()}): " + ", ".join(it) + "." for n_, name, s, it in ROADMAP)
  return svg(w, h, "road", "Asimov v1 assurance roadmap", desc, defs, "\n".join(body))


# ------------------------------------------------------------------ lifecycle

def lifecycle_svg():
  w, h = 1000, 300
  defs, frame = card_bg(w, h, "life")
  body = [frame, heading(40, "LIFECYCLE", "Seven phases, seven gates, none passed")]
  n = len(GATES)
  x0, x1 = 60, 940
  step = (x1 - x0) / (n - 1)
  body.append(f'<line x1="{x0}" y1="170" x2="{x1}" y2="170" stroke="{C["stroke"]}" stroke-width="3"/>')
  for i, (g, name, phase) in enumerate(GATES):
    x = x0 + i * step
    today = phase == TODAY_PHASE
    col = C["amber"] if today else C["dim"]
    body.append(f'<circle cx="{x:g}" cy="170" r="16" fill="{C["bg2"]}" stroke="{col}" stroke-width="2.5"/>')
    body.append(text(x, 175, g, 12, col, 700, anchor="middle", family=MONO))
    lines = wrap(name, 120, 12)
    for j, ln in enumerate(lines):
      body.append(text(x, 208 + j * 15, ln, 12, C["text"] if today else C["muted"], 600 if today else 400, anchor="middle"))
    if today:
      body.append(rect(x - 44, 118, 88, 22, C["amber"], r=11, stroke=C["amber"], opacity=0.15))
      body.append(text(x, 133, "TODAY · " + phase, 11, C["amber"], 700, anchor="middle", extra=' letter-spacing="1"'))
    if g in HOLD_POINTS:
      body.append(f'<path d="M{x - 9:g},150 L{x + 9:g},150 L{x:g},136 Z" fill="{C["red"]}"/>')
  body.append(text(40, h - 42, "Hold points: " + "; ".join(f"{g}: {t}" for g, t in HOLD_POINTS.items()) + ".", 12, C["red"]))
  body.append(text(40, h - 20, "A gate counts as passed only when its record in 10-safety-case/gates/ says Pass. Gate skeletons are generated by the process model.", 12, C["dim"]))
  desc = ("The seven phases P0 to P6, each closed by its gate: " + "; ".join(f"{g} {n_}" for g, n_, _ in GATES)
          + f". Today is {TODAY_PHASE}; the gates before it are passed by their records. Hold points at " + " and ".join(HOLD_POINTS) + ".")
  return svg(w, h, "life", "Asimov v1 assurance lifecycle", desc, defs, "\n".join(body))


# ------------------------------------------------------------------ the records

WP_STATUS = (("S", "Skeleton"), ("D", "Draft"), ("R", "In review"), ("A", "Approved"), ("B", "Baselined"))
WP_STATUS_COLOR = {"S": C["dim"], "D": C["amber"], "R": C["cyan_lo"], "A": C["green"], "B": C["cyan"]}
SEVERITY = (("High", C["red"]), ("Medium", C["amber"]), ("Low", C["muted"]))
DQ_STATUS = ("open", "queued", "answered", "assumed", "applied", "withdrawn")


def load_records(root: Path = ROOT) -> dict:
  """Every number the status card and the headline show, read from the records."""
  a = root / "assurance"
  files = {
    "register": a / "01-management" / "WP-M-00-work-product-register.md",
    "gaps": a / "00-assessment" / "gap-assessment.md",
    "decisions": a / "01-management" / "decisions" / "register.yaml",
    "interfaces": a / "process" / "model" / "interfaces.yaml",
    "confirmation_md": a / "01-management" / "WP-M-06-confirmation-measures-plan.md",
  }
  texts = {k: (f.read_text(encoding="utf-8") if f.exists() else "") for k, f in files.items()}
  wp = collections.Counter()
  wp_gate = collections.Counter()
  for line in texts["register"].splitlines():
    m = re.match(r"^\| \[(WP-[A-Z]-\d\d)\]\([^)]+\) \|", line)
    if m:
      c = [x.strip() for x in line.strip().strip("|").split("|")]
      wp[c[8]] += 1
      g = re.match(r"G\d", c[7])
      wp_gate[g.group(0) if g else "?"] += 1
  std_matrix: dict[str, dict[str, int]] = collections.OrderedDict((name, collections.Counter()) for name, _, _ in STANDARD_PATTERNS)
  for line in texts["register"].splitlines():
    m = re.match(r"^\| \[(WP-[A-Z]-\d\d)\]\([^)]+\) \|", line)
    if m:
      c = [x.strip() for x in line.strip().strip("|").split("|")]
      g = re.match(r"G\d", c[7])
      gate = g.group(0) if g else "?"
      cells = " ".join(c[2:7])
      for name, _, pat in STANDARD_PATTERNS:
        if re.search(pat, cells):
          std_matrix[name][gate] += 1
  gaps = collections.Counter()
  gap_areas: dict[str, int] = collections.OrderedDict()
  area = ""
  for line in texts["gaps"].splitlines():
    m = re.match(r"^## \d+\. (.+)$", line)
    if m:
      area = re.sub(r"\s*\(.*\)$", "", m.group(1))
    m = re.match(r"^\| GAP-\d\d", line)
    if m:
      sev = [x.strip() for x in line.strip().strip("|").split("|")][-1]
      gaps[sev] += 1
      gap_areas[area] = gap_areas.get(area, 0) + 1
  dq = collections.Counter(re.findall(r"^  status: (\w+)", texts["decisions"], re.M))
  ix_total = len(re.findall(r"^- id: IX-", texts["interfaces"], re.M))
  ix_open = len(re.findall(r"^  status: open", texts["interfaces"], re.M))
  measures = set()
  for line in texts["confirmation_md"].splitlines():
    m = re.match(r"^\| (G\d) \| ([^|]+) \|$", line)
    if m:
      measures.update(re.findall(r"\b(CR-\d\d|FSA-[A-Z0-9]+|AUD-\d|CS-[AI]\d|ML-R\d|NB-\d)\b", m.group(2)))
  gates_dir = a / "10-safety-case" / "gates"
  gate_records = sorted(p.name for p in gates_dir.glob("G[0-6]-[0-9]*.md")) if gates_dir.exists() else []
  conf_dir = a / "10-safety-case" / "confirmation"
  conf_records = sorted(p.name for p in conf_dir.glob("*.md") if p.name != "README.md") if conf_dir.exists() else []
  h = hashlib.sha256()
  for k in sorted(texts):
    h.update(k.encode()); h.update(texts[k].encode("utf-8"))
  for name in gate_records + conf_records:
    h.update(name.encode())
  return {
    "wp_total": sum(wp.values()), "wp": dict(wp), "wp_gate": dict(wp_gate),
    "std_matrix": {k: dict(v) for k, v in std_matrix.items()},
    "gaps_total": sum(gaps.values()), "gaps": dict(gaps), "gap_areas": dict(gap_areas),
    "dq": dict(dq), "dq_total": sum(dq.values()),
    "ix_total": ix_total, "ix_open": ix_open,
    "measures_planned": len(measures), "measures_performed": len(conf_records),
    "gates_passed": len(gate_records), "phase": "P1 Concept",
    "digest": h.hexdigest()[:12],
  }


def headline(r: dict) -> str:
  wp = r["wp"]
  parts = [f"**{r['phase']}**",
           ("no gate passed" if r["gates_passed"] == 0 else f"{r['gates_passed']} gate(s) passed"),
           f"{r['wp_total']} work products ({wp.get('D', 0)} draft, {wp.get('S', 0)} skeleton, {wp.get('A', 0) + wp.get('B', 0)} approved)",
           f"{r['gaps_total']} gap findings ({r['gaps'].get('High', 0)} high)",
           f"{r['dq'].get('open', 0)} decisions open",
           f"{r['ix_open']} of {r['ix_total']} cross-domain interfaces open",
           f"{r['measures_performed']} of {r['measures_planned']} confirmation measures performed",
           f"records digest `{r['digest']}`"]
  return " · ".join(parts)


def headline_block(r: dict) -> str:
  return f"{HEADLINE_BEGIN}\n\n{headline(r)}\n\n{HEADLINE_END}"


def with_headline(readme: str, r: dict) -> str:
  i, j = readme.find(HEADLINE_BEGIN), readme.find(HEADLINE_END)
  if i < 0 or j < 0:
    return readme
  return readme[:i] + headline_block(r) + readme[j + len(HEADLINE_END):]


def status_svg(r: dict) -> str:
  w, h = 1000, 600
  defs, frame = card_bg(w, h, "stat")
  body = [frame, heading(40, "RECORD STATUS", "Where the record stands, from the records", "generated · nothing typed by hand")]
  # three hero tiles
  tiles = [(str(r["gates_passed"]), "gates passed", "of 7; today is " + r["phase"].split(" ")[0], C["amber"]),
           (str(r["wp_total"]), "work products", f"{r['wp'].get('A', 0) + r['wp'].get('B', 0)} approved, {r['wp'].get('D', 0)} draft", C["text"]),
           (str(r["gaps_total"]), "gap findings open", f"{r['gaps'].get('High', 0)} high severity, published", C["red"])]
  for i, (num, label, sub, col) in enumerate(tiles):
    x = 40 + i * 206
    body.append(rect(x, 124, 190, 112, C["panel"], r=14, stroke=C["stroke"]))
    body.append(text(x + 18, 182, num, 44, col, 800, extra=' letter-spacing="-1"'))
    body.append(text(x + 18, 206, label, 14, C["text"], 600))
    body.append(text(x + 18, 226, sub, 11, C["muted"]))
  # register by status (stacked bar)
  bx, bw = 40, 580
  body.append(text(bx, 272, "Work products by status", 14, C["text"], 700))
  x = bx
  total = max(r["wp_total"], 1)
  for code, name in WP_STATUS:
    n = r["wp"].get(code, 0)
    if not n:
      continue
    seg = bw * n / total
    body.append(rect(x, 284, max(seg - 2, 2), 22, WP_STATUS_COLOR[code], r=4))
    if seg > 40:
      body.append(text(x + seg / 2 - 1, 300, f"{n} {name.lower()}", 12, C["ink"], 600, anchor="middle"))
    x += seg
  body.append(text(bx, 328, "Approval needs a verification review by someone other than the author; nothing has had one.", 11, C["dim"]))
  # per gate
  body.append(text(bx, 358, "Needed by each gate", 14, C["text"], 700))
  gmax = max(list(r["wp_gate"].values()) + [1])
  for i, g in enumerate(GATES):
    gx = bx + i * 83
    n = r["wp_gate"].get(g[0], 0)
    hgt = 58 * n / gmax
    body.append(rect(gx, 392 + 58 - hgt, 64, hgt, C["cyan"], r=3, opacity=0.35))
    body.append(text(gx + 32, 386 + 58 - hgt, str(n), 11, C["text"], 600, anchor="middle"))
    body.append(text(gx + 32, 466, g[0], 11, C["muted"], 600, anchor="middle", family=MONO))
  # right column: gaps by severity and area
  rx = 660
  body.append(rect(rx, 124, 300, 342, C["panel2"], r=14, stroke=C["stroke"]))
  body.append(text(rx + 18, 150, "KNOWN GAPS · COUNTER-EVIDENCE", 11, C["amber"], 700, extra=' letter-spacing="1.5"'))
  body.append(text(rx + 18, 174, "Findings against the inherited robot", 14, C["text"], 700))
  y = 194
  smax = max(list(r["gaps"].values()) + [1])
  for sev, col in SEVERITY:
    n = r["gaps"].get(sev, 0)
    body.append(rect(rx + 18, y, 170 * n / smax, 14, col, r=3))
    body.append(text(rx + 18 + 170 * n / smax + 8, y + 12, f"{n} {sev.lower()}", 12, C["text"]))
    y += 24
  y += 10
  body.append(text(rx + 18, y, "By area", 12, C["muted"], 600))
  y += 8
  for area, n in list(r["gap_areas"].items())[:6]:
    y += 20
    body.append(text(rx + 18, y, area if len(area) <= 40 else area[:39] + "…", 11, C["text"]))
    body.append(text(rx + 282, y, str(n), 11, C["muted"], 600, anchor="end", family=MONO))
  body.append(text(rx + 18, 452, "Each becomes a defeater in the safety case.", 11, C["dim"]))
  # bottom strip
  by = 496
  strip = [(f"{r['dq'].get('open', 0)} open · {r['dq'].get('queued', 0)} queued · {r['dq'].get('answered', 0) + r['dq'].get('applied', 0)} answered", "Decisions for the lead"),
           (f"{r['ix_open']} of {r['ix_total']} open", "Cross-domain interfaces"),
           (f"{r['measures_performed']} of {r['measures_planned']} performed", "Confirmation measures"),
           ("not yet met", "Hold point: powered floor test")]
  for i, (val, label) in enumerate(strip):
    x = 40 + i * 232
    body.append(rect(x, by, 216, 56, C["panel"], r=10, stroke=C["stroke"]))
    body.append(text(x + 14, by + 24, val, 13, C["text"], 700))
    body.append(text(x + 14, by + 43, label, 11, C["muted"]))
  body.append(text(40, h - 14, f"Records digest {r['digest']} identifies the exact state these figures describe. A gate counts as passed only by its record; a measure only by its record.", 11, C["dim"]))
  desc = ("Record status generated from the records: " + headline(r).replace("**", "").replace("`", "") + ". Gap findings by severity: "
          + ", ".join(f"{r['gaps'].get(s, 0)} {s.lower()}" for s, _ in SEVERITY) + ".")
  return svg(w, h, "stat", "Asimov v1 assurance record status", desc, defs, "\n".join(body))


# ------------------------------------------------------------------ standards map (from the register)

def standards_map_svg(r: dict) -> str:
  rows = [(name, sub) for name, sub, _ in STANDARD_PATTERNS]
  label_w, cell_w, row_h, top = 300, 84, 34, 160
  w, h = 1000, top + len(rows) * row_h + 92
  defs, frame = card_bg(w, h, "smap")
  body = [frame, heading(40, "STANDARDS MAP · FROM THE REGISTER", "Which standard shapes which phase",
                         f"{r['wp_total']} work products · counted from the clause columns of WP-M-00")]
  x0 = 40 + label_w
  gates = [g for g, _, _ in GATES]
  for i, (g, name, _) in enumerate(GATES):
    x = x0 + i * cell_w
    body.append(text(x + cell_w / 2, top - 40, g, 12, C["amber"], 700, anchor="middle", family=MONO))
    for li, line in enumerate(wrap(name, cell_w - 6, 9)[:2]):
      body.append(text(x + cell_w / 2, top - 27 + li * 11, line, 9, C["muted"], anchor="middle"))
    body.append(text(x + cell_w / 2, top - 3, f"{r['wp_gate'].get(g, 0)} WPs", 9, C["dim"], anchor="middle", family=MONO))
  body.append(text(x0 + 7 * cell_w + 28, top - 27, "total", 9.5, C["muted"], anchor="middle"))
  vmax = max([n for m in r["std_matrix"].values() for n in m.values()] + [1])
  for j, (name, sub) in enumerate(rows):
    y = top + j * row_h
    if j % 2:
      body.append(rect(32, y, w - 64, row_h, C["panel"], r=6, opacity=0.45))
    body.append(text(40, y + 15, name, 12, C["text"], 700))
    body.append(text(40, y + 28, sub, 9.5, C["muted"]))
    counts = r["std_matrix"].get(name, {})
    for i, g in enumerate(gates):
      n = counts.get(g, 0)
      x = x0 + i * cell_w
      if n:
        body.append(rect(x + 4, y + 4, cell_w - 8, row_h - 8, C["cyan"], r=6, opacity=0.12 + 0.78 * n / vmax))
        body.append(text(x + cell_w / 2, y + 22, str(n), 13, C["ink"], 800, anchor="middle", family=MONO))
      else:
        body.append(text(x + cell_w / 2, y + 22, "·", 13, C["dim"], anchor="middle"))
    body.append(text(x0 + 7 * cell_w + 28, y + 22, str(sum(counts.values())), 13, C["amber"], 800, anchor="middle", family=MONO))
  fy = top + len(rows) * row_h + 20
  body.append(text(40, fy, "A cell is the number of work products needed by that gate whose register row cites the standard; one work product can answer several standards, which is the point of an integrated lifecycle.", 10.5, C["dim"]))
  body.append(text(40, fy + 16, "Structured after the standards, cited by clause; no compliance is claimed, and every clause reference is marked to be checked against a licensed copy.", 10.5, C["dim"]))
  body.append(text(40, h - 16, f"Records digest {r['digest']} · regenerated whenever the register changes; CI fails if this figure is stale.", 10.5, C["dim"]))
  desc = "Standards by phase, counted from the work product register: " + "; ".join(
    f"{name}: " + ", ".join(f"{g} {r['std_matrix'].get(name, {}).get(g, 0)}" for g in gates) for name, _ in rows) + "."
  return svg(w, h, "smap", "Which standard shapes which phase", desc, defs, "\n".join(body))


# ------------------------------------------------------------------ repository map

def repo_map_svg() -> str:
  w, h = 1000, 640
  defs, frame = card_bg(w, h, "repo")
  defs += f'\n<marker id="repo-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{C["amber"]}"/></marker>'
  body = [frame, heading(40, "REPOSITORY MAP", "The code, the record, and what is generated from it", "one repository: the robot's sources and its record")]
  # column 1: code
  cx, cy, cw = 40, 124, 230
  body.append(rect(cx, cy, cw, 400, C["panel2"], r=14, stroke=C["stroke"]))
  body.append(text(cx + 16, cy + 26, "ROBOT SOURCES · UPSTREAM'S", 10.5, C["amber"], 700, extra=' letter-spacing="1.5"'))
  body.append(text(cx + 16, cy + 46, "Upstream's sources, changed by pull request", 10.5, C["muted"]))
  for i, (name, what, cls) in enumerate(REPO_CODE):
    y = cy + 64 + i * 84
    body.append(rect(cx + 14, y, cw - 28, 70, C["bg2"], r=10, stroke=C["stroke"]))
    body.append(text(cx + 26, y + 20, name, 11.5, C["text"], 700, family=MONO))
    for li, line in enumerate(wrap(what, cw - 60, 10)[:2]):
      body.append(text(cx + 26, y + 37 + li * 13, line, 10, C["muted"]))
    body.append(rect(cx + cw - 70, y + 8, 46, 16, C["red"] if cls == "SR-A" else C["amber"], r=8, opacity=0.9))
    body.append(text(cx + cw - 47, y + 19.5, cls, 9, C["ink"], 700, anchor="middle", family=MONO))
  body.append(text(cx + 16, cy + 332, "Classes from the safety-relevant file list:", 9.5, C["dim"]))
  body.append(text(cx + 16, cy + 346, "SR-A stop chain, boards, firmware safety layer,", 9.5, C["dim"]))
  body.append(text(cx + 16, cy + 360, "SR-Q structure, model, policy and API, SR-T tooling.", 9.5, C["dim"]))
  body.append(text(cx + 16, cy + 384, "A change on one needs an impact record.", 9.5, C["amber"], 600))
  # arrow 1
  body.append(f'<path d="M{cx + cw + 6},{cy + 200} L{cx + cw + 44},{cy + 200}" stroke="{C["amber"]}" stroke-width="1.6" fill="none" marker-end="url(#repo-arrow)"/>')
  body.append(text(cx + cw + 25, cy + 188, "impact", 9, C["amber"], 600, anchor="middle"))
  # column 2: the record
  rx, rw = cx + cw + 50, 356
  body.append(rect(rx, cy, rw, 400, C["panel"], r=14, stroke=C["cyan_lo"]))
  body.append(text(rx + 16, cy + 26, "ASSURANCE/ · THE RECORD", 10.5, C["cyan"], 700, extra=' letter-spacing="1.5"'))
  body.append(text(rx + 16, cy + 46, "assurance/ in lifecycle order; every file has a register row", 10.5, C["muted"]))
  for i, (num, folder, what) in enumerate(REPO_RECORD):
    col_i, row_i = i % 2, i // 2
    x = rx + 12 + col_i * 168
    y = cy + 60 + row_i * 44
    body.append(rect(x, y, 158, 38, C["bg2"], r=8, stroke=C["stroke"]))
    body.append(text(x + 10, y + 16, f"{num}", 10, C["cyan"], 700, family=MONO))
    body.append(text(x + 38 if len(num) <= 2 else x + 10 + len(num) * 6.5 + 6, y + 16, folder, 10.5, C["text"], 700))
    body.append(text(x + 10, y + 30, what, 9, C["muted"]))
  body.append(text(rx + 16, cy + 388, "Plus the decision register, the process model and the checks that CI runs.", 9.5, C["dim"]))
  # arrow 2
  body.append(f'<path d="M{rx + rw + 6},{cy + 200} L{rx + rw + 44},{cy + 200}" stroke="{C["amber"]}" stroke-width="1.6" fill="none" marker-end="url(#repo-arrow)"/>')
  body.append(text(rx + rw + 25, cy + 188, "generate", 9, C["amber"], 600, anchor="middle"))
  # column 3: outputs
  ox, ow = rx + rw + 50, w - 40 - (rx + rw + 50)
  body.append(rect(ox, cy, ow, 400, C["panel2"], r=14, stroke=C["stroke"]))
  body.append(text(ox + 16, cy + 26, "GENERATED · PUBLISHED", 10.5, C["amber"], 700, extra=' letter-spacing="1.5"'))
  body.append(text(ox + 16, cy + 46, "Never edited by hand", 10.5, C["muted"]))
  for i, (what, tool, where) in enumerate(REPO_OUTPUTS):
    y = cy + 62 + i * 54
    body.append(rect(ox + 12, y, ow - 24, 46, C["bg2"], r=8, stroke=C["stroke"]))
    body.append(text(ox + 22, y + 17, wrap(what, ow - 50, 10.5)[0], 10.5, C["text"], 700))
    body.append(text(ox + 22, y + 31, wrap(tool, ow - 50, 9)[0], 9, C["cyan"], family=MONO))
    body.append(text(ox + 22, y + 42, wrap(where, ow - 50, 8.5)[0], 8.5, C["dim"]))
  # bottom: CI strip
  by = cy + 416
  body.append(rect(40, by, w - 80, 56, C["bg2"], r=12, stroke=C["stroke"]))
  body.append(text(58, by + 23, "CI on every pull request", 12, C["text"], 700))
  body.append(text(58, by + 40, "case validator and dashboard · decision register · folder indexes · process model, maps and swimlanes · README figures · links and tables · wiki build.", 9.5, C["muted"]))
  body.append(text(w - 58, by + 23, "A passing run accepts nothing on its own: a claim is accepted only by a recorded review.", 9.5, C["dim"], anchor="end"))
  body.append(text(40, h - 16, "Source changes land under the change process; the record changes in the same pull request; every figure, map and page is regenerated from it.", 10.5, C["dim"]))
  desc = ("Repository map. Code: " + ", ".join(n for n, _, _ in REPO_CODE) + ". Record folders: " + ", ".join(f"{n} {f}" for n, f, _ in REPO_RECORD)
          + ". Generated: " + ", ".join(w_ for w_, _, _ in REPO_OUTPUTS) + ".")
  return svg(w, h, "repo", "Repository map: sources, record, generated outputs", desc, defs, "\n".join(body))


# ------------------------------------------------------------------ entry points

def render_all(root: Path = ROOT) -> dict[str, str]:
  r = load_records(root)
  return {"hero.svg": hero_svg(), "standards.svg": standards_svg(), "architecture.svg": architecture_svg(),
          "roadmap.svg": roadmap_svg(), "lifecycle.svg": lifecycle_svg(), "status.svg": status_svg(r),
          "standards-map.svg": standards_map_svg(r), "repo-map.svg": repo_map_svg()}


def main(argv: list[str]) -> int:
  ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
  g = ap.add_mutually_exclusive_group()
  g.add_argument("--out", type=Path, default=None)
  g.add_argument("--check", action="store_true")
  args = ap.parse_args(argv)
  out = args.out or HERE
  figs = render_all()
  records = load_records()
  readme = README.read_text(encoding="utf-8") if README.exists() else ""
  if args.check:
    stale = [n for n, s in figs.items() if not (out / n).exists() or (out / n).read_text(encoding="utf-8") != s]
    for n in stale:
      print(f"{out / n}: stale or missing; run make_assets.py")
    headline_stale = readme and with_headline(readme, records) != readme
    if headline_stale:
      print(f"{README}: record-headline block is stale; run make_assets.py")
    print(f"README figures: {len(figs) - len(stale)} of {len(figs)} current; headline {'stale' if headline_stale else 'current'}")
    return 1 if stale or headline_stale else 0
  out.mkdir(parents=True, exist_ok=True)
  for n, s in figs.items():
    (out / n).write_text(s, encoding="utf-8")
    print(f"wrote {out / n}")
  if readme and args.out is None:
    new = with_headline(readme, records)
    if new != readme:
      README.write_text(new, encoding="utf-8")
      print(f"updated the record-headline block in {README}")
  return 0


if __name__ == "__main__":
  sys.exit(main(sys.argv[1:]))
