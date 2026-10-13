#!/usr/bin/env python3
"""Compare the two arms of the lazy-rekey probe: per seed, every schedule and both arms must
print one digest; the quiet populations must agree per n."""
import json
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
            continue  # human summary lines are not data
    return out


ok = True
for arm in ["fly-lazy.json", "fly-legacy.json"]:
    by_seed = {}
    for r in rows(arm):
        if r.get("case") == "fly":
            by_seed.setdefault(r["seed"], set()).add(r["digest"])
    for seed, ds in sorted(by_seed.items()):
        one = len(ds) == 1
        ok &= one
        print(f"{arm} seed {seed}: {'ONE digest' if one else 'DIGESTS MOVED'} {sorted(ds)}")

lazy = {r["n"]: r["digest"] for r in rows("fly-lazy.json") if r.get("case") == "quiet"}
legacy = {r["n"]: r["digest"] for r in rows("fly-legacy.json") if r.get("case") == "quiet"}
cross = {r["n"]: r["digest"] for r in rows("quiet-lazy.json") if r.get("case") == "quiet"}
quiet_legacy = {r["n"]: r["digest"] for r in rows("quiet-legacy.json") if r.get("case") == "quiet"}
for n in sorted(cross):
    same = cross[n] == quiet_legacy[n]
    ok &= same
    print(f"quiet n={n}: lazy {cross[n]} legacy {quiet_legacy[n]} {'SAME' if same else 'DIFFER'}")

lazy_d = {r["seed"]: next(iter({x["digest"] for x in rows('fly-lazy.json') if x.get('case') == 'fly' and x['seed'] == r['seed']})) for r in rows("fly-lazy.json") if r.get("case") == "fly"}
for seed, d in sorted(lazy_d.items()):
    legacy_ds = {x["digest"] for x in rows("fly-legacy.json") if x.get("case") == "fly" and x["seed"] == seed}
    same = legacy_ds == {d}
    ok &= same
    print(f"cross-arm seed {seed}: lazy {d} legacy {sorted(legacy_ds)} {'SAME' if same else 'DIFFER'}")

print("VERDICT:", "ALL DIGESTS AGREE" if ok else "DIGESTS MOVED")
sys.exit(0 if ok else 1)
