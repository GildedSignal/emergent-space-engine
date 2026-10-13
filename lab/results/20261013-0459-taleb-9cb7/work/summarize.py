#!/usr/bin/env python3
"""Summarize the nose-map grid: outcome per (level, rel_v), boundaries, silence, timing."""
import csv, math, sys

def load(path):
    rows = []
    with open(path) as f:
        for r in csv.DictReader(f):
            r["level"] = int(r["level"]); r["rel_v"] = float(r["rel_v"]); r["rel_rout"] = float(r["rel_rout"])
            r["refusals"] = int(r["refusals"]); r["t_end"] = int(r["t_end_ticks"]); r["events"] = int(r["events"])
            rows.append(r)
    return rows

rows = load("nose_map.csv") if len(sys.argv) < 2 else load(sys.argv[1])
levels = sorted({r["level"] for r in rows})
print(f"{'lvl':>3} {'crash':>5} {'esc':>4} {'bnd':>4} {'other':>5}  crash-arc(rel_v deg)          max fault/ref   dead t range")
summary = {}
for L in levels:
    rs = [r for r in rows if r["level"] == L]
    kinds = {}
    for r in rs:
        k = r["outcome"].split()[0].split("@")[0]
        kinds.setdefault(k, []).append(r)
    crash = sorted(kinds.get("CRASH", []), key=lambda r: r["rel_v"])
    other = {k: v for k, v in kinds.items() if k not in ("CRASH",)}
    arc = f"[{crash[0]['rel_v']:.0f},{crash[-1]['rel_v']:.0f}]" if crash else "-"
    tmin = min((r["t_end"] for r in crash), default=0); tmax = max((r["t_end"] for r in crash), default=0)
    ncrash = len(crash); nesc = len(kinds.get("ESCAPE", []) + kinds.get("CAP_passage", []))
    nbound = sum(1 for i in range(len(rs)) if True) # computed below
    # boundary count: neighbours in rel_v order (circular) with differing death
    srt = sorted(rs, key=lambda r: r["rel_v"])
    dead = [r["outcome"].startswith("CRASH") or r["outcome"].startswith("LEAVE") or r["outcome"].startswith("DEAD") for r in srt]
    b = sum(1 for i in range(len(srt)) if dead[i] != dead[i - 1])
    faults = sum(1 for r in rs if r["fault"] != "-"); refs = sum(r["refusals"] for r in rs)
    oth = " ".join(f"{k}:{len(v)}" for k, v in sorted(other.items()) if not k.startswith("ESCAPE"))
    print(f"{L:>3} {ncrash:>5} {nesc:>4} {b:>4} {len(rs)-ncrash-nesc:>5}  {arc:<28} {faults}/{refs:<8} {tmin:.2e}-{tmax:.2e}  {oth}")
    summary[L] = (ncrash, nesc, b, crash, rs)

print()
print("silence: rows with fault!=None:", sum(1 for r in rows if r["fault"] != "-"),
      "| rows with refusals>0:", sum(1 for r in rows if r["refusals"] > 0))
print("crash gamma_max range:", min((float(r["gamma_max"]) for r in rows if r["outcome"].startswith("CRASH")), default=0),
      "-", max((float(r["gamma_max"]) for r in rows if r["outcome"].startswith("CRASH")), default=0))
print("wall total s:", round(sum(float(r["wall_s"]) for r in rows), 1))
# radial speed test: among crashes at each level, t_end vs inward component
print()
print("P3 radial: per level, crash t_end median for |rel_rout|>90 vs <=90")
for L in levels:
    cr = [r for r in rows if r["level"] == L and r["outcome"].startswith("CRASH")]
    if len(cr) < 3:
        continue
    inw = sorted(r["t_end"] for r in cr if abs(r["rel_rout"]) > 90)
    out = sorted(r["t_end"] for r in cr if abs(r["rel_rout"]) <= 90)
    if inw and out:
        m = lambda v: v[len(v) // 2]
        print(f"  L{L}: inward median {m(inw):.3e} ({len(inw)}) vs tangential/outward {m(out):.3e} ({len(out)})")
