#!/usr/bin/env python3
"""Check relative markdown links in the repository's Markdown (WP-P-04 documentation management).

Reports every relative link in ROOT/**/*.md whose target file or directory does not exist. Anchors,
absolute URLs, and links inside code spans or fenced code blocks are ignored. Folders named in SKIP are
not walked (the wiki has its own link rules and checker).

Usage: python3 assurance/tools/check_links.py [ROOT]
Exit code 0 when no broken links, 1 otherwise.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[2]
SKIP = {".git", "wiki", "build", "node_modules", "__pycache__"}

LINK = re.compile(r'(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)|!\[[^\]]*\]\(([^)\s]+)\)')
HTML_SRC = re.compile(r'<img[^>]*\ssrc="([^"]+)"')
FENCE = re.compile(r'^\s*```')
CODE_SPAN = re.compile(r'`[^`]*`')
SCHEME = re.compile(r'^[a-z][a-z0-9+.-]*:', re.I)


def targets(line: str):
  for m in LINK.finditer(CODE_SPAN.sub('', line)):
    yield m.group(1) or m.group(2)
  for m in HTML_SRC.finditer(line):
    yield m.group(1)


def check(root: Path) -> tuple[int, list[str]]:
  total = 0
  broken = []
  for md in sorted(root.rglob('*.md')):
    if SKIP & set(md.relative_to(root).parts[:-1]):
      continue
    in_fence = False
    for n, line in enumerate(md.read_text(encoding='utf-8').splitlines(), 1):
      if FENCE.match(line):
        in_fence = not in_fence
        continue
      if in_fence:
        continue
      for target in targets(line):
        if SCHEME.match(target) or target.startswith('#'):
          continue
        path = target.split('#', 1)[0]
        if not path:
          continue
        total += 1
        if not (md.parent / path).resolve().exists():
          broken.append(f'{md.relative_to(root)}:{n}: {target}')
  return total, broken


def main(argv: list[str]) -> int:
  root = Path(argv[0]).resolve() if argv else DEFAULT_ROOT
  total, broken = check(root)
  for b in broken:
    print(b)
  print(f'{total} relative links checked, {len(broken)} broken')
  return 1 if broken else 0


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
