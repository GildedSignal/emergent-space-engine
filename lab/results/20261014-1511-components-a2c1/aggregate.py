#!/usr/bin/env python3
"""Aggregate the scan census (ES_SCAN_CENSUS=1) into the dossier's table.
Usage: aggregate.py <census-file>...  — prints one row per file."""
import sys, re, collections
for path in sys.argv[1:]:
    rad, cap = {}, collections.defaultdict(dict)
    head = ""
    for line in open(path):
        if line.startswith("scan census:"):
            head = line.strip()
        if line.startswith("rad seq="):
            f = dict(t.split("=", 1) for t in line.split()[1:] if "=" in t)
            rad[int(f["seq"])] = f
        if line.startswith("cap seq="):
            f = dict(t.split("=", 1) for t in line.split()[1:] if "=" in t)
            cap[int(f["seq"])] = f
    walks = [int(c["walked"]) for c in cap.values()]
    keeps = [int(c["kept"]) for c in cap.values()]
    first = rad.get(1, {})
    last = rad.get(max(rad), {})
    why = collections.Counter(c["why"] for c in cap.values())
    n = len(walks)
    print(f"{path.split('/')[-1]:24s} calls={n} why={dict(why)} "
          f"walked/call={sum(walks)/max(n,1):.0f} kept/call={sum(keeps)/max(n,1):.0f} "
          f"| seq1: scap={first.get('scap','-')} hit={first.get('hit','-')} unb={first.get('unb','-')} reach={first.get('reach','-')} "
          f"| last: scap={last.get('scap','-')} hit={last.get('hit','-')} unb={last.get('unb','-')} reach={last.get('reach','-')} entries={last.get('entries','-')}")
    print(f"  {head}")
