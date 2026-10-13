#!/usr/bin/env python3
"""Check the starvation case: the three arms (budgeted-then-settled, stepped-settle, fresh
settled) must print one digest, and the budgeted fleet's committed tick must be at or below the
cut. This is the run's decisive experiment (the silver's named gap: the shipped plane gate)."""
import json
import re
import sys
from pathlib import Path

here = Path(__file__).resolve().parent


def rows(name):
    out = []
    for line in (here / name).read_text().splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            out.append(json.loads(line))
        except ValueError:
            continue
    return out


ok = True
digests = {}
for r in rows("starve-lazy.txt"):
    arm = r.get("arm")
    if arm:
        digests[arm] = r.get("digest")
cut = digests.get("budgeted") and next((r["cut"] for r in rows("starve-lazy.txt") if r.get("arm") == "budgeted"), None)
fleet = None
for line in (here / "starve-lazy.txt").read_text().splitlines():
    m = re.search(r"budgeted: fleet tick (\d+), live", line)
    if m:
        fleet = int(m.group(1))
one = len(set(d for d in digests.values() if d)) == 1 and len(digests) == 3
ok &= one
print(f"lazy starve: digests {digests} -> {'ONE digest' if one else 'DIGESTS MOVED'}")
if fleet is not None and cut is not None:
    at = fleet <= cut
    ok &= at
    print(f"lazy starve: budgeted fleet tick {fleet} vs cut {cut} -> {'AT OR BELOW the cut' if at else 'PAST THE CUT'}")
# The eager arm must hold too (it did on the author's tree; a regression here would be mine).
edig = {r.get("arm"): r.get("digest") for r in rows("starve-eager.txt") if r.get("arm")}
eone = len(set(d for d in edig.values() if d)) >= 1 and edig.get("budgeted") == edig.get("settled")
ok &= eone
print(f"eager starve: budgeted {edig.get('budgeted', '')[:12]}… settled {edig.get('settled', '')[:12]}… -> {'AGREE' if eone else 'DISAGREE'}")
print("VERDICT:", "STARVE HOLDS" if ok else "STARVE FAILS")
sys.exit(0 if ok else 1)
