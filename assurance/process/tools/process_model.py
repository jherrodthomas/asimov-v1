#!/usr/bin/env python3
"""Asimov v1 integrated process model (WP-P-11): checker and process-map generator.

Reads the process records in `assurance/process/model/` and checks them against the documents they
describe. It then writes the process maps (Mermaid) in `assurance/process/maps/` and the gate review
skeletons in `assurance/10-safety-case/gates/skeletons/`. Clause references, gate names, exit criteria,
work-product status and role assignments are never copied into the model. They are read from WP-M-00,
WP-M-02 and WP-M-06 at generation time, so a map cannot disagree with the register.

The standards columns and the confirmation-measure identifiers are the machinery set of WP-M-00 and WP-M-06.

Usage:
    python3 process_model.py           # check the model and write the maps
    python3 process_model.py --check   # check the model and fail if a committed map is stale
"""
# ruff: noqa: E501  (generated Markdown table rows)
from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
PROCESS_DIR = TOOLS_DIR.parent
ASSURANCE_DIR = PROCESS_DIR.parent
MODEL_DIR = PROCESS_DIR / "model"
MAPS_DIR = PROCESS_DIR / "maps"
SKELETON_DIR = ASSURANCE_DIR / "10-safety-case" / "gates" / "skeletons"
REGISTER_MD = ASSURANCE_DIR / "01-management" / "WP-M-00-work-product-register.md"
SAFETY_PLAN_MD = ASSURANCE_DIR / "01-management" / "WP-M-02-safety-plan.md"
CONFIRMATION_MD = ASSURANCE_DIR / "01-management" / "WP-M-06-confirmation-measures-plan.md"
CONFIRMATION_DIR = ASSURANCE_DIR / "10-safety-case" / "confirmation"

GATES = ["G0", "G1", "G2", "G3", "G4", "G5", "G6"]
STANDARDS = [("machinery", "Machinery"), ("srpcs", "SRP/CS"), ("iec62443", "IEC 62443"), ("other", "Other"), ("aspice", "ASPICE")]
STATUS_NAMES = {"S": "Skeleton", "D": "Draft", "R": "In review", "A": "Approved", "B": "Baselined", "N/A": "Tailored out"}
INTERFACE_STATUS = {"documented", "open"}
MEASURE_RE = r"\b(CR-\d\d|FSA-[A-Z0-9]+|AUD-\d|CS-[AI]\d|ML-R\d|NB-\d)\b"

REQUIRED = {
  "phase": ["id", "kind", "modelled"],
  "lane": ["id", "kind", "name", "role", "plan"],
  "activity": ["id", "kind", "phase", "lane", "name", "produces", "inputs"],
  "review": ["id", "kind", "phase", "name", "covers", "independence"],
  "interface": ["id", "kind", "phase", "between", "pattern", "topic", "anchors", "status", "open_item", "due"],
  "feedback": ["id", "kind", "phase", "source", "targets", "finding", "anchors"],
}
LIST_FIELDS = {"produces", "updates", "inputs", "covers", "between", "anchors", "targets"}


# ---------------------------------------------------------------- flat YAML subset

def _scalar(val: str):
  v = val.strip()
  if v.startswith("[") and v.endswith("]"):
    inner = v[1:-1].strip()
    return [_scalar(x) for x in inner.split(",")] if inner else []
  if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
    return v[1:-1]
  if v in ("true", "True"):
    return True
  if v in ("false", "False"):
    return False
  if v in ("null", "~", ""):
    return None
  if re.fullmatch(r"-?\d+", v):
    return int(v)
  return v


def load_subset(text: str) -> list[dict]:
  """Parse a top-level list of flat mappings with scalar or flow-list values (the `case/` record format)."""
  items: list[dict] = []
  cur: dict | None = None
  for n, raw in enumerate(text.splitlines(), 1):
    line = raw.rstrip()
    if not line or line.lstrip().startswith("#"):
      continue
    m = re.match(r"^(- |  )([A-Za-z_][A-Za-z0-9_]*):(?: (.*))?$", line)
    if not m:
      raise ValueError(f"line {n}: outside the supported YAML subset: {raw!r}")
    lead, key, val = m.group(1), m.group(2), m.group(3) or ""
    if lead == "- ":
      cur = {}
      items.append(cur)
    elif cur is None:
      raise ValueError(f"line {n}: key before first list item")
    cur[key] = _scalar(val)
  return items


# ---------------------------------------------------------------- sources

@dataclass
class RegisterRow:
  wp: str
  name: str
  path: Path
  clauses: dict[str, str]
  gate: str
  status: str

  @property
  def first_gate(self) -> str:
    m = re.match(r"G\d", self.gate)
    return m.group(0) if m else ""


def _cells(line: str) -> list[str]:
  return [c.strip() for c in line.strip().strip("|").split("|")]


def load_register(text: str) -> tuple[dict[str, RegisterRow], dict[str, tuple[str, str]]]:
  """Work-product rows of WP-M-00 §3 and the gate table of §2 (gate -> (name, exit criterion))."""
  rows: dict[str, RegisterRow] = {}
  gates: dict[str, tuple[str, str]] = {}
  for line in text.splitlines():
    m = re.match(r"^\| \[(WP-[A-Z]-\d\d)\]\(([^)]+)\) \|", line)
    if m:
      c = _cells(line)
      if len(c) != 9:
        raise ValueError(f"WP-M-00 row {m.group(1)}: expected 9 columns, found {len(c)}")
      clauses = dict(zip([k for k, _ in STANDARDS], c[2:7], strict=True))
      rows[m.group(1)] = RegisterRow(m.group(1), c[1], (REGISTER_MD.parent / m.group(2)).resolve(), clauses, c[7], c[8])
      continue
    g = re.match(r"^\| (G\d) \| ([^|]+) \| ([^|]+) \|$", line)
    if g:
      gates[g.group(1)] = (g.group(2).strip(), g.group(3).strip())
  return rows, gates


def load_roles(text: str) -> dict[str, tuple[str, str]]:
  """Role table of WP-M-02 §3.1: role -> (assigned to, needed by)."""
  roles: dict[str, tuple[str, str]] = {}
  in_table = False
  for line in text.splitlines():
    if line.startswith("| Role | Responsibilities | Assigned to | Needed by |"):
      in_table = True
      continue
    if in_table:
      if not line.startswith("|"):
        break
      c = _cells(line)
      if len(c) == 4 and not c[0].startswith("---"):
        roles[c[0]] = (c[2], c[3])
  return roles


def load_plan_roles(text: str) -> dict[str, str]:
  """Role table of a discipline plan (`| Role | Holder (today) | ...`): role -> holder."""
  roles: dict[str, str] = {}
  in_table = False
  for line in text.splitlines():
    if re.match(r"^\| Role \| Holder( \(today\)| today)? \|", line):
      in_table = True
      continue
    if in_table:
      if not line.startswith("|"):
        break
      c = _cells(line)
      if len(c) >= 2 and not c[0].startswith("---"):
        roles[c[0]] = c[1]
  return roles


def _role_key(role: str) -> str:
  return re.sub(r"\s+", " ", role.lower().replace("(acting)", "")).strip()


def _unassigned(holder: str) -> bool:
  h = holder.lower()
  return h.startswith(("tbd", "to be appointed", "external, tbd"))


def role_disagreements(ctx: Context, model: Model) -> list[str]:
  """Roles that WP-M-02 §3.1 and a lane's plan record differently (assigned in one, TBD in the other)."""
  safety_plan = {_role_key(r): (r, who) for r, (who, _) in ctx.roles.items()}
  out = []
  for plan in sorted({lane["plan"] for lane in model.lanes.values()} - {"WP-M-02"}):
    for role, holder in ctx.plan_roles.get(plan, {}).items():
      key = _role_key(role)
      if key in safety_plan:
        name, who = safety_plan[key]
        if _unassigned(who) != _unassigned(holder):
          out.append(f"{name}: WP-M-02 §3.1 says \"{who}\", {plan} says \"{holder}\"")
  return out


def load_gate_measures(text: str) -> dict[str, list[str]]:
  """Confirmation measures per gate from the WP-M-06 §9 summary table."""
  out: dict[str, list[str]] = {}
  for line in text.splitlines():
    m = re.match(r"^\| (G\d) \| ([^|]+) \|$", line)
    if m:
      out[m.group(1)] = re.findall(MEASURE_RE, m.group(2))
  return out


# ---------------------------------------------------------------- model

@dataclass
class Model:
  phases: dict[str, dict] = field(default_factory=dict)
  lanes: dict[str, dict] = field(default_factory=dict)
  activities: dict[str, dict] = field(default_factory=dict)
  reviews: dict[str, dict] = field(default_factory=dict)
  interfaces: dict[str, dict] = field(default_factory=dict)
  feedback: dict[str, dict] = field(default_factory=dict)
  errors: list[str] = field(default_factory=list)

  def err(self, check: str, where: str, msg: str) -> None:
    self.errors.append(f"[{check}] {where}: {msg}")


def load_model(model_dir: Path = MODEL_DIR) -> Model:
  model = Model()
  buckets = {"phase": model.phases, "lane": model.lanes, "activity": model.activities, "review": model.reviews, "interface": model.interfaces, "feedback": model.feedback}
  for path in sorted(model_dir.glob("*.yaml")):
    try:
      items = load_subset(path.read_text(encoding="utf-8"))
    except ValueError as e:
      model.err("P1", path.name, f"parse error: {e}")
      continue
    for it in items:
      kind = it.get("kind")
      where = f"{path.name}:{it.get('id')}"
      if kind not in REQUIRED:
        model.err("P1", where, f"unknown kind {kind!r}")
        continue
      missing = [k for k in REQUIRED[kind] if k not in it]
      if missing:
        model.err("P1", where, f"missing fields {missing}")
        continue
      bad = [k for k in LIST_FIELDS if k in it and not isinstance(it[k], list)]
      if bad:
        model.err("P1", where, f"fields must be lists: {bad}")
        continue
      if it["id"] in buckets[kind]:
        model.err("P1", where, "duplicate id")
        continue
      it["_file"] = path.name
      buckets[kind][it["id"]] = it
  return model


def measure_id(review_id: str) -> str:
  """WP-M-06 measure of a review record: `CR-06@G2` is measure CR-06 as performed at G2."""
  return review_id.split("@", 1)[0]


def record_pattern(review_id: str) -> str:
  """File-name pattern of a measure's record, per `10-safety-case/confirmation/README.md` and WP-M-06.

  Confirmation reviews are `CR-<nn>-<WP-ID>-v<version>.md`; a measure planned at one gate is `<measure>.md`;
  one planned at several gates is `<measure>-<gate>.md`. A confirmation review planned at several gates
  (CR-03, CR-06) cannot be told apart by file name: any record counts.
  """
  measure, _, gate = review_id.partition("@")
  if measure.startswith("CR-"):
    return f"{measure}-*.md"
  if gate:
    return f"{measure}-{gate}.md"
  return f"{measure}.md"


def record_present(review: dict, register: dict[str, RegisterRow] | None = None) -> bool:
  """A measure whose record is a work product (`record_wp`) counts once that work product is approved or baselined."""
  if review.get("record_wp"):
    row = (register or {}).get(review["record_wp"])
    return bool(row) and row.status in ("A", "B")
  return any(CONFIRMATION_DIR.glob(record_pattern(review["id"])))


def record_label(review: dict) -> str:
  return review["record_wp"] if review.get("record_wp") else f"confirmation/{record_pattern(review['id'])}"


def outputs(act: dict) -> list[str]:
  """Work products an activity produces or (for living work products) updates."""
  return act["produces"] + act.get("updates", [])


def phase_suppliers(acts: dict[str, dict]) -> dict[str, list[str]]:
  """Work product -> activities of the phase that produce or update it, in ID order."""
  out: dict[str, list[str]] = {}
  for aid in sorted(acts):
    for wp in outputs(acts[aid]):
      out.setdefault(wp, []).append(aid)
  return out


def direct_deps(acts: dict[str, dict], producer: dict[str, str]) -> dict[str, set[str]]:
  """Activity -> activities whose outputs it consumes, with transitive dependencies removed (map edges)."""
  deps = {a: {producer[w] for w in act["inputs"] if producer.get(w) in acts and producer[w] != a} for a, act in acts.items()}

  def reach(a: str, seen: set[str]) -> set[str]:
    for d in deps[a]:
      if d not in seen:
        seen.add(d)
        reach(d, seen)
    return seen

  return {a: {d for d in ds if not any(d in reach(o, set()) for o in ds - {d})} for a, ds in deps.items()}


@dataclass
class Context:
  register: dict[str, RegisterRow]
  gates: dict[str, tuple[str, str]]
  roles: dict[str, tuple[str, str]]
  gate_measures: dict[str, list[str]]
  plan_roles: dict[str, dict[str, str]] = field(default_factory=dict)


def load_context() -> Context:
  register, gates = load_register(REGISTER_MD.read_text(encoding="utf-8"))
  plan_roles = {wp: load_plan_roles(row.path.read_text(encoding="utf-8"))
                for wp, row in register.items() if wp.startswith("WP-M-") and row.path.exists()}
  return Context(register, gates, load_roles(SAFETY_PLAN_MD.read_text(encoding="utf-8")),
                 load_gate_measures(CONFIRMATION_MD.read_text(encoding="utf-8")), plan_roles)


def check(model: Model, ctx: Context) -> dict[str, list[str]]:
  """Run the checks; returns the activity order per modelled phase."""
  reg = ctx.register
  # P2 phases and lanes
  for g in GATES:
    if g not in model.phases:
      model.err("P2", g, "phase record missing")
    if g not in ctx.gates:
      model.err("P2", g, "gate missing from WP-M-00 §2")
  for lid, lane in model.lanes.items():
    if lane["role"] not in ctx.roles:
      model.err("P2", lid, f"role {lane['role']!r} not in WP-M-02 §3.1")
    if lane["plan"] not in reg:
      model.err("P2", lid, f"plan {lane['plan']} not in WP-M-00")

  producer: dict[str, str] = {}
  for aid, act in model.activities.items():
    # P3 activity references
    if act["phase"] not in model.phases:
      model.err("P3", aid, f"unknown phase {act['phase']}")
    if act["lane"] not in model.lanes:
      model.err("P3", aid, f"unknown lane {act['lane']!r}")
    for wp in act["produces"]:
      if wp not in reg:
        model.err("P3", aid, f"produces {wp}, which is not in WP-M-00")
        continue
      if wp in producer:
        model.err("P3", aid, f"{wp} is already produced by {producer[wp]}")
      producer[wp] = aid
      if reg[wp].first_gate != act["phase"]:
        model.err("P3", aid, f"{wp} is gated {reg[wp].gate} in WP-M-00, activity is in {act['phase']}")
      if not reg[wp].path.exists():
        model.err("P3", aid, f"{wp} file {reg[wp].path} does not exist")
    # living work products (gate "G1→G5"): produced once, then updated in a later phase of their range
    for wp in act.get("updates", []):
      gates = re.findall(r"G\d", reg[wp].gate) if wp in reg else []
      if len(gates) < 2:
        model.err("P3", aid, f"updates {wp}, which is not a living work product in WP-M-00")
      elif act["phase"] in GATES and not GATES.index(gates[0]) < GATES.index(act["phase"]) <= GATES.index(gates[-1]):
        model.err("P3", aid, f"updates {wp} in {act['phase']}, outside its gate range {reg[wp].gate}")

  orders: dict[str, list[str]] = {}
  for gid, phase in model.phases.items():
    if not phase["modelled"]:
      continue
    acts = {a: x for a, x in model.activities.items() if x["phase"] == gid}
    # P4 completeness: every work product the register gates here has a producing activity
    for wp, row in reg.items():
      if row.first_gate == gid and wp not in producer:
        model.err("P4", gid, f"{wp} ({row.name}) is gated {row.gate} but no activity produces it")
    # P5 inputs: produced by an activity with a lower ID in this phase (so the ID order is a valid
    # execution order and the inputs cannot form a cycle), or by a work product of an earlier gate
    suppliers = phase_suppliers(acts)
    for aid, act in acts.items():
      for wp in act["inputs"]:
        late = [s for s in suppliers.get(wp, []) if s >= aid and s != aid]
        if wp not in reg:
          model.err("P5", aid, f"input {wp} not in WP-M-00")
        elif late:
          model.err("P5", aid, f"input {wp} comes from {late[0]}, which is not earlier; renumber, or model the iteration as an interface")
        elif wp in suppliers:
          continue
        elif GATES.index(reg[wp].first_gate or "G6") >= GATES.index(gid):
          model.err("P5", aid, f"input {wp} is gated {reg[wp].gate} and not produced in {gid}")
    orders[gid] = sorted(acts)
    # P6 confirmation measures equal the WP-M-06 §9 row for the gate
    planned = set(ctx.gate_measures.get(gid, []))
    modelled = {measure_id(r) for r, x in model.reviews.items() if x["phase"] == gid}
    if planned != modelled:
      model.err("P6", gid, f"confirmation measures differ from WP-M-06 §9: missing {sorted(planned - modelled)}, extra {sorted(modelled - planned)}")

  conf_text = CONFIRMATION_MD.read_text(encoding="utf-8")
  for rid, rv in model.reviews.items():
    for wp in rv["covers"]:
      if wp not in reg:
        model.err("P6", rid, f"covers {wp}, which is not in WP-M-00")
    if not re.search(rf"\b{re.escape(measure_id(rid))}\b", conf_text):
      model.err("P6", rid, "not defined in WP-M-06")
    if rv.get("record_wp") and rv["record_wp"] not in reg:
      model.err("P6", rid, f"record_wp {rv['record_wp']} is not in WP-M-00")
    if "@" in rid and rid.split("@", 1)[1] != rv["phase"]:
      model.err("P6", rid, f"gate suffix does not match phase {rv['phase']}")

  # P7 interfaces: both ends produced by an activity, anchors present verbatim
  texts: dict[str, str] = {}
  for iid, ix in model.interfaces.items():
    if ix["status"] not in INTERFACE_STATUS:
      model.err("P7", iid, f"status must be one of {sorted(INTERFACE_STATUS)}")
    if (ix["status"] == "open") != bool(ix["open_item"]):
      model.err("P7", iid, "open_item is required exactly when status is open")
    if ix["due"] not in GATES:
      model.err("P7", iid, f"unknown gate {ix['due']}")
    elif ix["phase"] in GATES and GATES.index(ix["due"]) < GATES.index(ix["phase"]):
      model.err("P7", iid, f"due {ix['due']} is before its phase {ix['phase']}")
    if len(ix["between"]) != 2:
      model.err("P7", iid, "between must name two work products")
    for wp in ix["between"]:
      if wp not in producer:
        model.err("P7", iid, f"{wp} is not produced by any activity")
    check_anchors(model, "P7", iid, ix["anchors"], reg, texts)

  # P9 feedback: a finding of a later phase routed back to work products of earlier phases
  phase_of = {wp: a["phase"] for a in model.activities.values() for wp in a["produces"]}
  for fid, fb in model.feedback.items():
    if fb["source"] not in phase_of:
      model.err("P9", fid, f"source {fb['source']} is not produced by any activity")
    elif phase_of[fb["source"]] != fb["phase"]:
      model.err("P9", fid, f"source {fb['source']} is produced in {phase_of[fb['source']]}, not {fb['phase']}")
    for wp in fb["targets"]:
      if wp not in phase_of:
        model.err("P9", fid, f"target {wp} is not produced by any activity")
      elif fb["phase"] in GATES and GATES.index(phase_of[wp]) >= GATES.index(fb["phase"]):
        model.err("P9", fid, f"target {wp} is produced in {phase_of[wp]}, not in an earlier phase")
    check_anchors(model, "P9", fid, fb["anchors"], reg, texts)
  return orders


def check_anchors(model: Model, check: str, where: str, anchors: list[str], reg: dict[str, RegisterRow], texts: dict[str, str]) -> None:
  """Each anchor `WP-x-nn:text` must name a registered work product whose file contains the text."""
  for anchor in anchors:
    wp, sep, needle = anchor.partition(":")
    if not sep or wp not in reg:
      model.err(check, where, f"anchor {anchor!r} must be WP-x-nn:text with a registered work product")
      continue
    if wp not in texts:
      texts[wp] = reg[wp].path.read_text(encoding="utf-8") if reg[wp].path.exists() else ""
    if needle not in texts[wp]:
      model.err(check, where, f"anchor text {needle!r} not found in {wp}")


# ---------------------------------------------------------------- rendering

GENERATED_NOTE = "<!-- GENERATED by assurance/process/tools/process_model.py from assurance/process/model/. Do not edit; edit the model and re-run. -->"


def _q(text: str) -> str:
  """Mermaid node label: quoted, with characters Mermaid would misread replaced."""
  return '"' + text.replace('"', "'").replace("[", "(").replace("]", ")") + '"'


def _nid(item_id: str) -> str:
  """Mermaid node id: letters, digits and underscores only."""
  return re.sub(r"[^A-Za-z0-9_]", "_", item_id)


def _outputs_label(act: dict) -> str:
  return ", ".join(act["produces"] + [f"{w} (update)" for w in act.get("updates", [])])


def _link(wp: str, ctx: Context, up: int = 2) -> str:
  """Markdown link to a work product from a file `up` directories below `assurance/`."""
  row = ctx.register.get(wp)
  if not row:
    return wp
  return f"[{wp}]({Path(*(['..'] * up), row.path.relative_to(ASSURANCE_DIR)).as_posix()})"


def open_item_count(path: Path) -> int:
  """Rows of a work product's open-item table (`| OI-n |`) that are not marked closed."""
  if not path.exists():
    return 0
  return sum(1 for ln in path.read_text(encoding="utf-8").splitlines()
             if re.match(r"^\| OI-\d+ \|", ln) and "closed" not in ln.lower())


def render_lifecycle(model: Model, ctx: Context) -> str:
  lines = [GENERATED_NOTE, "", "# Integrated lifecycle (L0)", "",
           "One lifecycle with one gate per phase. All disciplines work inside each phase and decide at the same gate.",
           "Gate names and exit criteria come from [WP-M-00 §2](../../01-management/WP-M-00-work-product-register.md#2-gates).",
           "", "```mermaid", "flowchart LR"]
  for g in GATES:
    name = ctx.gates.get(g, ("?", ""))[0]
    n = len([a for a in model.activities.values() if a["phase"] == g])
    detail = f"{n} activities modelled" if model.phases.get(g, {}).get("modelled") else "not modelled yet"
    lines.append(f"  {g}[{_q(f'{g} {name}<br/>{detail}')}]")
  lines.append("  " + " --> ".join(GATES))
  phase_of = {wp: a["phase"] for a in model.activities.values() for wp in a["produces"]}
  back: dict[tuple[str, str], list[str]] = {}
  for fb in model.feedback.values():
    for g in sorted({phase_of[w] for w in fb["targets"] if w in phase_of}):
      back.setdefault((fb["phase"], g), []).append(fb["id"])
  lines.append("  classDef modelled fill:#0f6e63,stroke:#063f38,color:#ffffff")
  lines.append("  classDef pending fill:#f6f8fa,stroke:#8c959f,color:#57606a,stroke-dasharray: 4 3")
  mod = [g for g in GATES if model.phases.get(g, {}).get("modelled")]
  if mod:
    lines.append(f"  class {','.join(mod)} modelled")
  pend = [g for g in GATES if g not in mod]
  if pend:
    lines.append(f"  class {','.join(pend)} pending")
  lines.append("```")
  if back:
    lines += ["", "## Feedback into earlier phases", "",
              "Findings that a later phase routes back into work products of earlier phases (FB-nn, listed in the map of the phase that raises them). A finding that needs a change re-enters through problem resolution, change management and impact analysis.",
              "", "```mermaid", "flowchart LR"]
    targets = sorted({dst for _, dst in back}, key=GATES.index)
    for g in sorted({src for src, _ in back}, key=GATES.index):
      lines.append(f"  F_{g}[{_q(g + ' ' + ctx.gates[g][0])}]")
    for g in targets:
      lines.append(f"  T_{g}[{_q(g + ' ' + ctx.gates[g][0])}]")
    for (src, dst), ids in sorted(back.items(), key=lambda kv: (GATES.index(kv[0][0]), GATES.index(kv[0][1]))):
      lines.append(f"  F_{src} -. {_q(', '.join(ids))} .-> T_{dst}")
    lines.append("```")
  lines += ["", "## Phases", "", "| Gate | Phase | Exit criterion (WP-M-00 §2) | Process map |", "|---|---|---|---|"]
  for g in GATES:
    name, exit_ = ctx.gates.get(g, ("?", "?"))
    mp = f"[{g} map]({g.lower()}-{_slug(name)}.md)" if model.phases.get(g, {}).get("modelled") else "Not modelled yet"
    lines.append(f"| {g} | {name} | {exit_} | {mp} |")
  return "\n".join(lines) + "\n"


def _slug(name: str) -> str:
  return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def _clause_cell(wps: list[str], ctx: Context, std: str) -> str:
  vals = []
  for wp in wps:
    v = ctx.register[wp].clauses[std] if wp in ctx.register else ""
    if v and v != "—" and v not in vals:
      vals.append(v)
  return "; ".join(vals)


def render_phase(gid: str, order: list[str], model: Model, ctx: Context) -> str:
  name, exit_ = ctx.gates[gid]
  acts = [model.activities[a] for a in order]
  producer = {wp: ids[-1] for wp, ids in phase_suppliers({a["id"]: a for a in acts}).items()}
  lane_of = {wp: a["lane"] for a in model.activities.values() for wp in a["produces"]}
  reviews = [r for r in model.reviews.values() if r["phase"] == gid]
  ixs = [x for x in model.interfaces.values() if x["phase"] == gid]
  lane_ids = [lid for lid in model.lanes if lid != "assess" and any(a["lane"] == lid for a in acts)]

  out = [GENERATED_NOTE, "", f"# {gid} {name}: integrated process map (L1)", "",
         "Back to the [lifecycle map](lifecycle.md). Model: [`model/`](../model/), method: [process README](../README.md).", "",
         "## 1. Swimlane map", "",
         "One box per discipline; green activities are joint work of all disciplines and sit outside the boxes. Arrows are work-product inputs: an activity cannot finish before its inputs exist. An arrow implied by a longer path is left out; §2 lists every input. Iteration between disciplines is shown in the interface map (§1.1), not here.", "",
         "```mermaid", "flowchart LR"]
  for a in acts:
    if a["lane"] == "joint":
      out.append(f"  {_nid(a['id'])}[{_q(a['id'] + '<br/>' + a['name'] + '<br/>' + _outputs_label(a))}]")
  for lid in [x for x in lane_ids if x != "joint"]:
    out.append(f"  subgraph L_{lid}[{_q(model.lanes[lid]['name'])}]")
    out.append("    direction LR")
    for a in acts:
      if a["lane"] == lid:
        out.append(f"    {_nid(a['id'])}[{_q(a['id'] + '<br/>' + a['name'] + '<br/>' + _outputs_label(a))}]")
    out.append("  end")
  has_assess = bool(reviews) or any(a["lane"] == "assess" for a in acts)
  if has_assess:
    out.append(f"  subgraph L_assess[{_q(model.lanes['assess']['name'])}]")
    out.append("    direction LR")
    for a in acts:
      if a["lane"] == "assess":
        out.append(f"    {_nid(a['id'])}[{_q(a['id'] + '<br/>' + a['name'] + '<br/>' + _outputs_label(a))}]")
    for r in reviews:
      out.append(f"    {_nid(r['id'])}[{_q(r['id'] + '<br/>' + r['independence'])}]")
    out.append("  end")
  out.append(f"  GATE{{{{{_q(gid + ' ' + name + ' gate')}}}}}")
  edges = direct_deps({a["id"]: a for a in acts}, producer)
  for a in acts:
    for src in sorted(edges[a["id"]]):
      out.append(f"  {_nid(src)} --> {_nid(a['id'])}")
  consumed = {w for a in acts for w in a["inputs"]}
  for a in acts:
    if a["lane"] != "assess" and not any(w in consumed and producer.get(w) == a["id"] for w in outputs(a)):
      out.append(f"  {_nid(a['id'])} --> GATE")
  if has_assess:
    out.append("  L_assess --> GATE")
  joint = [_nid(a["id"]) for a in acts if a["lane"] == "joint"]
  if joint:
    out += ["  classDef joint fill:#dafbe1,stroke:#1a7f37,color:#0f3d1c", f"  class {','.join(joint)} joint"]
  if reviews:
    out += ["  classDef review fill:#fff8c5,stroke:#9a6700,color:#3d2c00", f"  class {','.join(_nid(r['id']) for r in reviews)} review"]
  out += ["  classDef gate fill:#0f6e63,stroke:#063f38,color:#ffffff", "  class GATE gate", "```", ""]

  out += ["### 1.1 Interface map", "",
          "Where one discipline's analysis depends on another's. Each edge lists the interfaces of §3 between two lanes; OPEN marks one that a recorded open item still has to settle.", "",
          "```mermaid", "flowchart LR"]
  pairs: dict[tuple[str, str], list[str]] = {}
  for x in ixs:
    la, lb = sorted(lane_of[w] for w in x["between"])
    pairs.setdefault((la, lb), []).append(x["id"] + (" OPEN" if x["status"] == "open" else ""))
  used = sorted({ln for p in pairs for ln in p}, key=list(model.lanes).index)
  for ln in used:
    out.append(f"  {ln}([{_q(model.lanes[ln]['name'])}])")
  for (la, lb), labels in pairs.items():
    out.append(f"  {la} -. {_q(', '.join(labels))} .- {lb}")
  if not pairs:
    out.append("  none([No cross-domain interface recorded in this phase])")
  out += ["```", ""]

  out += ["## 2. Activities", "",
          "Clause references and status are read from the [register (WP-M-00)](../../01-management/WP-M-00-work-product-register.md) row of each work product the activity produces or, for a living work product, updates (marked *update*).", "",
          "| Activity | Lane | Produces | Inputs | " + " | ".join(t for _, t in STANDARDS) + " | Status |",
          "|---|---|---|---|" + "---|" * len(STANDARDS) + "---|"]
  for a in acts:
    status = ", ".join(sorted({STATUS_NAMES.get(ctx.register[w].status, ctx.register[w].status) for w in outputs(a)}))
    made = [_link(w, ctx) for w in a["produces"]] + [f"{_link(w, ctx)} *update*" for w in a.get("updates", [])]
    out.append(f"| {a['id']} {a['name']} | {model.lanes[a['lane']]['name']} | {', '.join(made)} | {', '.join(a['inputs'])} | "
               + " | ".join(_clause_cell(outputs(a), ctx, k) for k, _ in STANDARDS) + f" | {status} |")
  out.append("")

  out += ["## 3. Cross-domain interfaces", "",
          "Each interface is anchored to text in the work products; the checker fails if an anchor disappears. *Documented* means the documents reference each other but nobody has reviewed the agreement yet.", "",
          "| ID | Pattern | Between | Topic | Status | Open item | Due |", "|---|---|---|---|---|---|---|"]
  for x in ixs:
    lanes = " / ".join(model.lanes[lane_of[w]]["name"].split(" (")[0] for w in x["between"])
    out.append(f"| {x['id']} | {x['pattern']} | {', '.join(_link(w, ctx) for w in x['between'])} ({lanes}) | {x['topic']} | {x['status'].capitalize()} | {x['open_item'] or '—'} | {x['due']} |")
  if not ixs:
    out.append("| — | — | — | No interface recorded in this phase | — | — | — |")
  out.append("")

  fbs = [f for f in model.feedback.values() if f["phase"] == gid]
  if fbs:
    phase_of = {wp: a["phase"] for a in model.activities.values() for wp in a["produces"]}
    out += ["### 3.1 Feedback into earlier phases", "",
            "Findings of this phase that re-open work products of earlier phases. Each row is anchored to the routing table of the source work product.", "",
            "| ID | Finding | From | Back into |", "|---|---|---|---|"]
    for f in fbs:
      into = ", ".join(f"{_link(w, ctx)} ({phase_of.get(w, '?')})" for w in f["targets"])
      out.append(f"| {f['id']} | {f['finding']} | {_link(f['source'], ctx)} | {into} |")
    out.append("")

  out += ["## 4. Clause coverage by standard", "",
          "Which activity answers each clause reference listed in the register. One activity can answer several standards; that is the point of the integrated lifecycle.", ""]
  for key, title in STANDARDS:
    by_clause: dict[str, list[str]] = {}
    for a in acts:
      for wp in outputs(a):
        c = ctx.register[wp].clauses[key]
        if c and c != "—" and a["id"] not in by_clause.setdefault(c, []):
          by_clause[c].append(a["id"])
    out.append(f"- **{title}:** " + ("; ".join(f"{c} → {', '.join(ids)}" for c, ids in by_clause.items()) if by_clause else "none"))
  out.append("")

  out += [f"## 5. {gid} readiness", "", f"**Exit criterion (WP-M-00 §2):** {exit_}", ""]
  wps = [w for a in acts for w in outputs(a)]
  counts: dict[str, int] = {}
  for w in wps:
    counts[ctx.register[w].status] = counts.get(ctx.register[w].status, 0) + 1
  out.append("**Work products:** " + ", ".join(f"{n} {STATUS_NAMES.get(s, s)}" for s, n in sorted(counts.items())) + f" of {len(wps)}. Approval needs the verification review of [WP-P-05](../../07-supporting/WP-P-05-verification-review-procedure.md).")
  out += ["", "**Roles the lanes need (WP-M-02 §3.1):**", "", "| Lane | Role | Assigned to | Needed by |", "|---|---|---|---|"]
  used_lanes = [*lane_ids, "assess"] if (reviews or any(a["lane"] == "assess" for a in acts)) else lane_ids
  for lid in used_lanes:
    role = model.lanes[lid]["role"]
    who, by = ctx.roles.get(role, ("?", "?"))
    out.append(f"| {model.lanes[lid]['name']} | {role} | {who} | {by} |")
  lane_roles = {model.lanes[lid]["role"] for lid in used_lanes}
  extra = []
  for role, (who, by) in ctx.roles.items():
    g = re.match(r"G\d", by)
    if role in lane_roles or not g or GATES.index(g.group(0)) > GATES.index(gid):
      continue
    if g.group(0) == gid:
      extra.append(f"{role} ({who})")
    elif who.startswith("TBD"):
      extra.append(f"{role} ({who}; needed by {g.group(0)}, still unassigned)")
  if extra:
    out += ["", f"**Other roles WP-M-02 §3.1 needs by {gid}:** " + "; ".join(extra) + "."]
  if gid == "G0":
    clash = role_disagreements(ctx, model)
    out += ["", "**Role records that disagree** (the readiness tables read WP-M-02 §3.1; a discipline plan records the same role differently): "
            + ("; ".join(clash) if clash else "none") + "."]
  out += ["", "**Confirmation measures (WP-M-06 §9):**" + ("" if reviews else " none planned at this gate."), ""]
  if reviews:
    out += ["| Measure | Covers | Independence | Record |", "|---|---|---|---|"]
  for r in reviews:
    out.append(f"| {r['id']} {r['name']} | {', '.join(r['covers'])} | {r['independence']} | {'Performed' if record_present(r, ctx.register) else 'Not performed'} |")
  assessments = [a for a in acts if a["lane"] == "assess"]
  covered = {w for r in reviews for w in r["covers"]} | {w for a in assessments for w in a["inputs"] + outputs(a)}
  uncovered = [w for w in wps if w not in covered]
  out += ["", "**Work products with no confirmation measure at this gate** (verification review only): " + (", ".join(uncovered) if uncovered else "none") + ".", ""]
  due = [x for x in model.interfaces.values() if x["status"] == "open" and GATES.index(x["due"]) <= GATES.index(gid)
         and GATES.index(x["phase"]) <= GATES.index(gid)]
  out.append("**Open interfaces due by this gate** (from this or an earlier phase): " + (", ".join(f"{x['id']} ({x['open_item']})" for x in due) if due else "none") + ".")
  return "\n".join(out) + "\n"


SKELETON_NOTE = "> [!IMPORTANT]\n> **Generated skeleton, not a gate review record.** No review has been held on the basis of this file. When the gate review is held, copy it to `../G{n}-<YYYY-MM-DD>.md`, re-check every pre-filled value at the review baseline, and complete it by hand. The pre-filled values are as recorded in the source documents when this file was generated by [`process_model.py`](../../../process/tools/process_model.py)."


def render_gate_skeleton(gid: str, order: list[str], model: Model, ctx: Context) -> str:
  """Gate review record skeleton (template of `10-safety-case/gates/README.md`) pre-filled from the model."""
  name, exit_ = ctx.gates[gid]
  acts = [model.activities[a] for a in order]
  reviews = [r for r in model.reviews.values() if r["phase"] == gid]
  wps = [w for a in acts for w in outputs(a)]
  lanes = [lid for lid in model.lanes if any(a["lane"] == lid for a in acts)]
  if reviews and "assess" not in lanes:
    lanes.append("assess")
  chair_who = ctx.roles.get("Safety manager", ("TBD", ""))[0]
  up = 3
  out = [GENERATED_NOTE, "", f"# {gid} gate review — {name}", "", SKELETON_NOTE.format(n=gid[1:]), "",
         "| Field | Value |", "|---|---|",
         f"| Gate | {gid} {name} |", "| Date | YYYY-MM-DD |", "| Baseline | <commit SHA or tag> |",
         f"| Chair | Safety manager ({chair_who}) |",
         "| Participants | " + "; ".join(f"{role} ({ctx.roles.get(role, ('?', ''))[0]})" for role in dict.fromkeys(model.lanes[ln]["role"] for ln in lanes)) + " |",
         "| Assessor informed | Yes / No (name) |", ""]

  counts: dict[str, int] = {}
  for w in wps:
    counts[ctx.register[w].status] = counts.get(ctx.register[w].status, 0) + 1
  status = ", ".join(f"{n} {STATUS_NAMES.get(s_, s_)}" for s_, n in sorted(counts.items())) + f" of {len(wps)} (table below)"
  performed = [r for r in reviews if record_present(r, ctx.register)]
  measures = (f"{len(performed)} of {len(reviews)} performed: " + ", ".join(r["id"] for r in reviews)) if reviews else "None planned at this gate"
  ois = sum(open_item_count(ctx.register[w].path) for w in wps)
  out += ["## Inputs (WP-M-02 §10)", "",
          "| Input | Status at this baseline | Link |", "|---|---|---|",
          f"| WP-M-00 status of the gate's work products | {status} | [WP-M-00](../../../01-management/WP-M-00-work-product-register.md) |",
          "| Open anomalies (`safety-anomaly`) | | GitHub issues labelled `safety-anomaly` |",
          "| Open risks (WP-M-07) | | [WP-M-07](../../../01-management/WP-M-07-risk-management.md) |",
          f"| Confirmation measures assigned to this gate (WP-M-06) and their results | {measures} | [WP-M-06](../../../01-management/WP-M-06-confirmation-measures-plan.md) |",
          "| QA findings (WP-M-05) | | [WP-M-05](../../../01-management/WP-M-05-quality-assurance-plan.md) |",
          f"| Open items of the phase's work products | {ois} open-item rows not marked closed, any due gate (table below) | |", ""]

  out += ["### Work products of this gate", "",
          "| Work product | Activity | Status in WP-M-00 | Open items | Verification review (WP-P-05) |", "|---|---|---|---|---|"]
  for a in acts:
    for w in outputs(a):
      row = ctx.register[w]
      kind = " (update)" if w in a.get("updates", []) else ""
      out.append(f"| {_link(w, ctx, up)} {row.name}{kind} | {a['id']} | {STATUS_NAMES.get(row.status, row.status)} | {open_item_count(row.path)} | |")
  out.append("")

  if reviews:
    out += ["### Confirmation measures", "",
            "A gate cannot pass if a confirmation review WP-M-06 assigns to it has not been performed, unless the safety manager and the assessor agree a documented deferral (WP-M-02 §10).", "",
            "| Measure | Covers | Independence | Record | Result |", "|---|---|---|---|---|"]
    for r in reviews:
      out.append(f"| {r['id']} {r['name']} | {', '.join(r['covers'])} | {r['independence']} | `{record_label(r)}` {('(approved)' if record_present(r, ctx.register) else '(not approved)') if r.get('record_wp') else ('(present)' if record_present(r, ctx.register) else '(not present)')} | |")
    out.append("")

  due = [x for x in model.interfaces.values() if x["status"] == "open" and GATES.index(x["due"]) <= GATES.index(gid)
         and GATES.index(x["phase"]) <= GATES.index(gid)]
  out += ["### Open cross-domain interfaces due by this gate", "",
          "From the [process model](../../../process/README.md). Each one is a condition on the gate unless it is closed before the review.", ""]
  if due:
    out += ["| Interface | Topic | Open item | Due | Closed? |", "|---|---|---|---|---|"]
    out += [f"| {x['id']} | {x['topic']} | {x['open_item']} | {x['due']} | |" for x in due]
  else:
    out.append("None.")
  out.append("")

  missing = []
  for role, (who, by) in ctx.roles.items():
    g = re.match(r"G\d", by)
    if g and GATES.index(g.group(0)) <= GATES.index(gid) and _unassigned(who):
      missing.append(f"| {role} | {who} | {g.group(0)} |")
  out += ["### Roles WP-M-02 §3.1 needs by this gate that are not assigned", ""]
  out += (["| Role | Assigned to | Needed by |", "|---|---|---|", *missing] if missing else ["None."]) + [""]

  criteria = [c.strip()[0].upper() + c.strip()[1:] for c in exit_.split(";") if c.strip()]
  out += ["## Exit criteria (WP-M-00 §2)", "", "| Criterion | Met? | Evidence |", "|---|---|---|"]
  out += [f"| {c} | | |" for c in criteria]
  if reviews:
    out.append("| Every confirmation measure assigned to this gate performed, or deferral documented (WP-M-02 §10) | | |")
  out += ["", "## Outcome", "", "- [ ] Pass  - [ ] Pass with conditions  - [ ] Fail", "",
          "| Condition | Owner | Due gate | Issue |", "|---|---|---|---|", "",
          "Deferrals of confirmation measures (agreed by safety manager and assessor), with rationale:", "",
          "Signature / approving GitHub review link:"]
  return "\n".join(out) + "\n"


def render_all(model: Model, ctx: Context, orders: dict[str, list[str]]) -> dict[Path, str]:
  files = {MAPS_DIR / "lifecycle.md": render_lifecycle(model, ctx)}
  for gid, order in orders.items():
    files[MAPS_DIR / f"{gid.lower()}-{_slug(ctx.gates[gid][0])}.md"] = render_phase(gid, order, model, ctx)
    files[SKELETON_DIR / f"{gid}-skeleton.md"] = render_gate_skeleton(gid, order, model, ctx)
  return files


def main(argv: list[str]) -> int:
  model = load_model()
  ctx = load_context()
  orders = check(model, ctx)
  if model.errors:
    print("\n".join(model.errors))
    print(f"FAIL: {len(model.errors)} process model error(s)")
    return 1
  files = render_all(model, ctx, orders)
  if "--check" in argv:
    stale = [p for p, text in files.items() if not p.exists() or p.read_text(encoding="utf-8") != text]
    extra = [p for d in (MAPS_DIR, SKELETON_DIR) for p in d.glob("*.md") if p not in files]
    for p in stale + extra:
      print(f"[P8] {p.relative_to(ASSURANCE_DIR)}: {'stale' if p in stale else 'not generated by the model'}; run process_model.py")
    if stale or extra:
      return 1
    print(f"OK: {len(model.activities)} activities, {len(model.reviews)} reviews, {len(model.interfaces)} interfaces; maps and gate skeletons current")
    return 0
  MAPS_DIR.mkdir(exist_ok=True)
  SKELETON_DIR.mkdir(parents=True, exist_ok=True)
  for p, text in files.items():
    p.write_text(text, encoding="utf-8")
    print(f"wrote {p.relative_to(ASSURANCE_DIR)}")
  return 0


if __name__ == "__main__":
  sys.exit(main(sys.argv))
