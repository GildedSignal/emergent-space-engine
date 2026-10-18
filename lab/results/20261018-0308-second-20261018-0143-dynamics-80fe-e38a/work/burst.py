#!/usr/bin/env python3
"""The mu=1e-2 burst, per cadence: the <=4 P plane kills against the truth's <=4 P disk entries,
per IC, for step 9 (finer), 7 (shipped), 5 and 3 (the negative control's coarser arms)."""
import json, sys

W = sys.argv[1] if len(sys.argv) > 1 else "."
load = lambda f: [json.loads(l.replace(":inf", ":0").replace(":NaN", ":0")) for l in open(f)]
key = lambda r: (round(r["du"], 3), round(r["phi_deg"], 1))
ev = load(f"{W}/ev-mu2.jsonl")
t4 = {key(r): round(r["entries"][0], 3) for r in ev if r["entries"] and r["entries"][0] <= 4.01}
lines = [f"truth <=4P entries: {len(t4)} (the fixed reference)"]
for s in (9, 7, 5, 3):
    pl = load(f"{W}/pl-mu2-4P-s{s}.jsonl")
    p4 = {key(r): (round(r["epoch_P"], 3), r["channel"]) for r in pl if r.get("dead") and r["epoch_P"] <= 4.01}
    beyond = {key(r): round(r["epoch_P"], 3) for r in pl if r.get("dead") and r["epoch_P"] > 4.01 and key(r) in t4}
    lines.append(f"--- step {s}: plane <=4P kills {len(p4)}   same IC set as truth: {set(t4) == set(p4)}   (kills of truth-burst ICs moved past 4 P: {len(beyond)})")
    worst = 0.0
    for k in sorted(t4):
        if k in p4:
            d = t4[k] - p4[k][0]
            worst = max(worst, abs(d))
            lines.append(f"  {k}  truth {t4[k]:7.3f} P  plane {p4[k][0]:7.3f} P ({p4[k][1]})  d = {d:+.3f} P")
        elif k in beyond:
            lines.append(f"  {k}  truth {t4[k]:7.3f} P  plane kill PAST 4 P at {beyond[k]:7.3f} P  (skipped the burst encounter)")
        else:
            lines.append(f"  {k}  truth {t4[k]:7.3f} P  plane: NO KILL by 4 P  (skipped)")
    extra = sorted(set(p4) - set(t4))
    if extra:
        lines.append(f"  plane-only <=4P kills (truth has no entry there): {[(k, p4[k]) for k in extra]}")
    lines.append(f"  step {s}: matched {len(set(t4) & set(p4))}/{len(t4)}  max |d_epoch| = {worst:.3f} P  (step-7 grid P/64 = {1/64:.3f} P)")
print("\n".join(lines))
open(f"{W}/burst.txt", "w").write("\n".join(lines) + "\n")
