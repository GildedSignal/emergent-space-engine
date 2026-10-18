#!/usr/bin/env python3
"""The mu=1e-2 burst: the <=4 P plane kills against the truth's <=4 P disk entries, per IC."""
import json, sys

W = sys.argv[1] if len(sys.argv) > 1 else "."
load = lambda f: [json.loads(l.replace(":inf", ":0").replace(":NaN", ":0")) for l in open(f)]
key = lambda r: (round(r["du"], 3), round(r["phi_deg"], 1))
ev = load(f"{W}/ev-mu2.jsonl")
pl = load(f"{W}/pl-mu2-4P.jsonl")
t4 = {key(r): round(r["entries"][0], 3) for r in ev if r["entries"] and r["entries"][0] <= 4.01}
p4 = {key(r): (round(r["epoch_P"], 3), r["channel"]) for r in pl if r.get("dead") and r["epoch_P"] <= 4.01}
print(f"truth <=4P entries: {len(t4)}   plane <=4P kills: {len(p4)}   same IC sets: {set(t4) == set(p4)}")
worst = 0.0
for k in sorted(t4):
    d = t4[k] - p4[k][0]
    worst = max(worst, abs(d))
    print(f"  {k}  truth {t4[k]:7.3f} P  plane {p4[k][0]:7.3f} P ({p4[k][1]})  d = {d:+.3f} P")
msg = f"max |d_epoch| = {worst:.3f} P (the plane's epoch grid is P/64 = {1/64:.3f} P)"
print(msg)
lines = [f"truth <=4P entries: {len(t4)}   plane <=4P kills: {len(p4)}   same IC sets: {set(t4) == set(p4)}"]
for k in sorted(t4):
    lines.append(f"  {k}  truth {t4[k]:7.3f} P  plane {p4[k][0]:7.3f} P ({p4[k][1]})  d = {t4[k]-p4[k][0]:+.3f} P")
lines.append(msg)
open(f"{W}/burst.txt", "w").write("\n".join(lines) + "\n")

msg = f"max |d_epoch| = {worst:.3f} P (the plane's epoch grid is P/64 = {1/64:.3f} P)"
lines_out = [f"truth <=4P entries: {len(t4)}   plane <=4P kills: {len(p4)}   same IC sets: {set(t4) == set(p4)}"]
for k in sorted(t4):
    lines_out.append(f"  {k}  truth {t4[k]:7.3f} P  plane {p4[k][0]:7.3f} P ({p4[k][1]})  d = {t4[k]-p4[k][0]:+.3f} P")
lines_out.append(msg)
open(f"{W}/burst.txt", "w").write("\n".join(lines_out) + "\n")
