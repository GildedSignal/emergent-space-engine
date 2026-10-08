#!/usr/bin/env python3
"""Losslessly shrink a kicks CSV: drop constant columns, delta-encode ticks per body."""
import csv, lzma, sys

run = sys.argv[1]
with lzma.open(f"{run}-kicks.csv.xz", "rt") as f:
    rows = list(csv.DictReader(f))

# how often oexp differs from nexp
diff = sum(1 for r in rows if r["oexp"] != r["nexp"])
nexp_of = {r["nexp"] for r in rows}
print(f"{run}: rows={len(rows)} oexp!=nexp in {diff}, nexp values {sorted(nexp_of)}")

last_t = {}
out = lzma.open(f"{run}-kicks2.csv.xz", "wt", preset=9 | lzma.PRESET_EXTREME)
out.write("body,dtick,dvx,dvy,nexp,oexp_diff,carry0,carry1\n")
for r in rows:
    b, t = int(r["body"]), int(r["tick"])
    dt = t - last_t.get(b, 0)
    last_t[b] = t
    od = "" if r["oexp"] == r["nexp"] else r["oexp"]
    out.write(f"{b},{dt},{r['dvx']},{r['dvy']},{r['nexp']},{od},{r['carry0']},{r['carry1']}\n")
out.close()
import os
print(f"{run}: kicks2 = {os.path.getsize(f'{run}-kicks2.csv.xz')} bytes")
