#!/usr/bin/env python3
"""Validate the Living Safety Case records in assurance/case (format: assurance/case/README.md).

Checks:
  V1  records parse, sit in the directory of their kind, carry every schema field and no others
  V2  identifiers match their pattern and are unique; field types and enumerations are valid
  V3  every reference resolves to a record (or trace item) of the right kind
  V4  links are consistent in both directions (claim <-> evidence, claim <-> defeater,
      claim <-> argument)
  V5  every evidence location exists in the repository
  V6  acceptance rules: accepted objects need an accepted review record that lists them;
      accepted claims need available, accepted evidence, accepted sub-claims and no open
      defeater; assurance-supported configurations need an accepted claim
  V8  the claims form one tree under a single top-level claim
  X3  evidence, defeater and open-item tables in WP-K-01 match the records

Usage: python3 assurance/case/tools/validate.py
Exit code 0 when the records are valid, 1 otherwise. Standard library only.
"""
from __future__ import annotations

import sys

from caselib import load_case, summarize, validate


def main() -> int:
  case = load_case()
  rep = validate(case)
  if rep.errors:
    for e in rep.errors:
      print(f"ERROR {e}")
    print(f"FAIL: {len(rep.errors)} error(s) in assurance/case records")
    return 1
  s = summarize(case)
  kinds: dict[str, int] = {}
  for r in case.records.values():
    kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
  print("case: " + ", ".join(f"{k}={v}" for k, v in sorted(kinds.items())))
  claims, evidence = s["claims"], s["evidence"]
  print(f"state: {s['assurance_state']}; claims accepted {claims['accepted']}/{claims['registered']}; " +
        f"evidence accepted {evidence['accepted']}/{evidence['registered']}")
  print("OK: assurance case records are valid")
  return 0


if __name__ == "__main__":
  sys.exit(main())
