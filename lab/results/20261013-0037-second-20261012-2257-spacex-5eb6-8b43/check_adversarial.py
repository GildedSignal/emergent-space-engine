#!/usr/bin/env python3
"""Check the adversarial cases: each must print the same digest in both arms (the eager arm is
the shipped frame loop, so this is schedule-independence across the construction)."""
import json
import sys
from pathlib import Path

here = Path(__file__).resolve().parent


def row(name):
    for line in (here / name).read_text().splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                return json.loads(line)
            except ValueError:
                continue
    return {}


ok = True
for case, lazy, eager in [("storm", "storm-lazy.json", "storm-eager.json"), ("fast", "fast-lazy.json", "fast-eager.json"), ("replay", "replay-lazy.json", "replay-eager.json")]:
    a, b = row(lazy), row(eager)
    same = a.get("digest") == b.get("digest") and bool(a.get("digest"))
    ok &= same
    extra = f", events {a.get('events')}/{b.get('events')}" if case == "storm" else ""
    if case == "replay":
        extra += f", frames {a.get('frames')}/{b.get('frames')}, matches want: {a.get('digest') == a.get('want')}"
        ok &= a.get("digest") == a.get("want")
    print(f"{case}: lazy {str(a.get('digest'))[:16]}… eager {str(b.get('digest'))[:16]}…{extra} -> {'SAME' if same else 'DIFFER'}")
print("VERDICT:", "ADVERSARIAL HOLDS" if ok else "ADVERSARIAL FAILS")
sys.exit(0 if ok else 1)
