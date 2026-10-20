#!/bin/sh
# Regen for 20261020-0440-redteam-9c08 — every dossier number, from this folder, < 1 min.
set -e
cd "$(dirname "$0")"
python3 falsifier.py
python3 - <<'EOF'
import json
d = json.load(open("results.json"))
print("state:", d["state"])
print("halving (exact):", d["span_check"][-2:])
for floor in ["stock_8e-3", "fine_1e-3"]:
    tf = {"stock_8e-3": 8e-3, "fine_1e-3": 1e-3}[floor]
    for r in d["floors"][floor]:
        c = r["fwd_hist_cure"]
        if c.get("sparse"):
            continue
        b5 = min([int(b) for b, e in c.items() if b != "n" and e <= 0.05], default=None)
        print(floor, f"gamma={r['gamma']:>8g} gtf={r['gamma']*tf:6.1f} B5%={b5} "
                     f"B8={c['8']:.4f} B16={c['16']:.4f} B64={c['64']:.4f}")
EOF
