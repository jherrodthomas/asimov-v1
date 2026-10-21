"""Parser for the restricted YAML subset of the assurance records (assurance/case/README.md, record format).

Standard library only; never PyYAML, so the result does not depend on what is installed.
"""
from __future__ import annotations

import re

def _scalar(v: str):
  v = v.strip()
  if v.startswith('"'):
    if not v.endswith('"') or len(v) < 2:
      raise ValueError(f"unterminated string: {v}")
    return v[1:-1].replace('\\"', '"').replace("\\\\", "\\")
  if v.startswith("["):
    if not v.endswith("]"):
      raise ValueError(f"unterminated list: {v}")
    inner = v[1:-1].strip()
    return [_scalar(x) for x in inner.split(",")] if inner else []
  if v in ("null", "~", ""):
    return None
  if v == "true":
    return True
  if v == "false":
    return False
  if re.fullmatch(r"-?[0-9]+", v):
    return int(v)
  return v


def _load_subset(text: str) -> list[dict]:
  """Parse a top-level list of flat mappings with scalar or flow-list values."""
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


