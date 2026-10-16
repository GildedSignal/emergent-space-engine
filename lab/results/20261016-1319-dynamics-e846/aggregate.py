#!/usr/bin/env python3
"""Aggregate the dive arms into the dossier's verdict table (dossier evidence, one page)."""
import json, re, statistics, sys
from collections import Counter

R = __file__.rsplit("/", 1)[0]

def load(p):
    out = {}
    for l in open(f"{R}/{p}"):
        if not l.startswith("{"):
            continue
        l = re.sub(r":inf", ":-1", l)
        l = re.sub(r":NaN", ":-1", l)
        r = json.loads(l)
        out[(round(r["du"], 3), round(r["phi_deg"], 1))] = r
    return out

pl, orc, win = load("plane.jsonl"), load("oracle.jsonl"), load("oracle-win.jsonl")
an = load("analytic.jsonl")
dead = [k for k, r in pl.items() if r.get("dead")]
alive = [k for k, r in pl.items() if not r.get("dead")]
ch = Counter(pl[k]["channel"] for k in dead)
cd = sorted(orc[k]["closest_Rp"] for k in dead)
ca = sorted(orc[k]["closest_Rp"] for k in alive)
wc = sorted(win[k]["win_closest_Rp"] for k in win)
gmin = [min((s[3] for s in win[k]["win"]), default=-1) for k in win]

print(f"ensemble: {len(pl)} ships, dead {len(dead)} (channels: {dict(ch)})")
print(f"plane earliest deaths (P): {[round(pl[k]['epoch_P'],2) for k in sorted(dead, key=lambda k: pl[k]['epoch_P'])[:4]]}")
print(f"plane osculating q at death (S): min {min(pl[k]['q_last_over_S'] for k in dead):.0f} "
      f"median {statistics.median(pl[k]['q_last_over_S'] for k in dead):.0f}")
print(f"plane J walk to death (rel): [{min(pl[k]['j_min_rel'] for k in dead):.1e}, {min(pl[k]['j_max_rel'] for k in dead):.1e}]")
print(f"no confinement: J0 below J(L1) for {sum(1 for k in an if an[k]['dj1_rel'] < 0)}/{len(an)} ICs "
      f"(dj1_rel [{min(an[k]['dj1_rel'] for k in an):.4f}, {max(an[k]['dj1_rel'] for k in an):.4f}])")
print(f"resolved truth conjunction (Rp): dead-IC min {cd[0]:.3f} p10 {cd[len(cd)//10]:.2f} med {statistics.median(cd):.2f}; "
      f"alive-IC min {ca[0]:.3f} med {statistics.median(ca):.0f}")
print(f"truths crossing the disk (<1 Rp): dead {sum(1 for x in cd if x < 1)}/{len(dead)}, alive {sum(1 for x in ca if x < 1)}/{len(alive)}; "
      f"whole ensemble {sum(1 for x in cd + ca if x < 1)}/144")
print(f"truth crosses at the death conjunction (±2 P, resolved): {sum(1 for x in wc if x < 1)}/{len(wc)} "
      f"(<=2 Rp {sum(1 for x in wc if x <= 2)}, <=5 Rp {sum(1 for x in wc if x <= 5)}, >10 Rp {sum(1 for x in wc if x > 10)})")
print(f"P/64 grid catches of those crossings: {sum(1 for x in gmin if 0 <= x < 1)}/{len(wc)}")
print(f"oracle J drift max {max(orc[k]['j_dev_rel'] for k in orc):.1e}; oracle q_min/S dead {min(orc[k]['q_min_over_S'] for k in dead):.1f} alive {min(orc[k]['q_min_over_S'] for k in alive):.1f}")
