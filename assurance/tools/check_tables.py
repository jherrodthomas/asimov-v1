#!/usr/bin/env python3
"""Check that every row of every markdown table has as many cells as its header (WP-P-04).

GitHub renders a row with a missing `|` as merged cells and a row with an extra `|` as an extra column;
neither shows up in the link check, and an extra column silently moves a status out of the cell the
register parsers read. A `|` inside a code span still separates cells on GitHub unless it is escaped
(`\\|`), so only escaped pipes are ignored. Tables inside fenced code blocks are ignored.

Usage: python3 assurance/tools/check_tables.py [ROOT]
Checks ROOT/**/*.md (default: the repository). Exit code 0 when every table is consistent.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[2]
SKIP = {".git", "build", "node_modules", "__pycache__"}

FENCE = re.compile(r'^\s*```')
ESCAPED_PIPE = re.compile(r'\\\|')


def cells(line: str) -> int:
  row = ESCAPED_PIPE.sub('', line.strip())
  parts = row.split('|')
  if row.startswith('|'):
    parts = parts[1:]
  if row.endswith('|'):
    parts = parts[:-1]
  return len(parts)


def check_text(text: str, name: str) -> list[str]:
  errors = []
  in_code = False
  header: tuple[int, int] | None = None
  for number, line in enumerate(text.split('\n'), start=1):
    if FENCE.match(line):
      in_code = not in_code
      header = None
      continue
    if in_code or not line.startswith('|'):
      header = None
      continue
    count = cells(line)
    if header is None:
      header = (count, number)
    elif count != header[0]:
      errors.append(f"{name}:{number}: {count} cells, the table header (line {header[1]}) has {header[0]}")
  return errors


def check(root: Path) -> tuple[int, list[str]]:
  files = [p for p in sorted(root.rglob('*.md')) if not (SKIP & set(p.relative_to(root).parts[:-1]))]
  errors: list[str] = []
  for path in files:
    errors += check_text(path.read_text(encoding='utf-8'), str(path.relative_to(root)))
  return len(files), errors


def main(argv: list[str]) -> int:
  root = Path(argv[1]).resolve() if len(argv) > 1 else DEFAULT_ROOT
  count, errors = check(root)
  for e in errors:
    print(e)
  if errors:
    print(f"FAIL: {len(errors)} table row(s) with the wrong number of cells in {count} files")
    return 1
  print(f"{count} files checked, every table row matches its header")
  return 0


if __name__ == '__main__':
  sys.exit(main(sys.argv))
