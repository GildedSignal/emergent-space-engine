#!/usr/bin/env python3
"""Checker's held-out series: w2 (1e5, 45-s wall, ~2x e3's duration), w1, e4/e5 (3e5),
s_on/d5 (3e3) — none analyzed in the dossier (only e3 was). delta_eff with each leg's
own lambda and gaps; verify the letter (max delta), the drift, and the decay trend."""
import re, sys
W = "/home/glmlab/actions-runner/_work/emergent-space-engine/lab-0/lab/results/20261020-2004-second-20261020-1815-library-a2c0-20f2/work/artifacts"
TICK = 4.925_490_947e-6

def series(tag):
    err = f"{W}/{tag}.err"; out = f"{W}/{tag}.out"
    rows = []
    for ln in open(err, errors="replace"):
        if ln.startswith("ANS "):
            d = dict(re.findall(r"(\w+)=(\d+)", ln))
            rows.append({k: int(v) for k, v in d.items()})
    bw = [r for r in rows if r.get("cand", 0) >= 50000]
    txt = open(out, errors="replace").read()
    lam = float(dict(re.findall(r"(\w+)=(\S+)", txt.splitlines()[-1]))["kicks_per_body_gs"])
    return bw, lam

for tag in ["23a6_w2_1e5_on", "23a6_w1_1e5_off", "23a6_e5_3e5_on", "23a6_e4_3e5_off",
            "23a6_s_on", "23a6_d5_3e3_verify"]:
    bw, lam = series(tag)
    if not bw:
        print(f"{tag}: no belt-wide answers"); continue
    print(f"\n== {tag}: {len(bw)} belt-wide, lambda={lam:.3e}")
    deffs, prev_t, misses, gaps = [], None, [], []
    for r in bw:
        t_gs = r["t"] * TICK
        gap = None if prev_t is None else (r["t"] - prev_t) * TICK
        prev_t = r["t"]
        miss = r["tests"] / r["cand"]
        if gap and gap > 1:
            deffs.append(miss / (lam * gap)); misses.append(miss); gaps.append(gap)
        else:
            print(f"  cold: tests {r['tests']:,}/{r['cand']:,} = {100*miss:.1f}%")
    if deffs:
        print(f"  warm n={len(deffs)} gaps {sorted(set(round(g,1) for g in gaps))}")
        print(f"  miss {100*min(misses):.3f}-{100*max(misses):.3f}%  delta_eff {min(deffs):.3f}-{max(deffs):.3f}"
              f"  letter<0.5: {max(deffs)<0.5}  delta=1 excluded (max ratio {max(deffs):.2f}<1): {max(deffs)<1}")
        run165 = [m for m, g in zip(misses, gaps) if abs(g-165.27) < 1]
        if len(run165) > 2:
            print(f"  165-gs legs: miss {100*run165[0]:.3f}% -> {100*run165[-1]:.3f}% ({run165[-1]/max(run165[0],1e-9):.1f}x over {len(run165)})")
        tail = misses[len(misses)//2:]
        head = misses[:len(misses)//2]
        print(f"  first-half mean miss {100*sum(head)/len(head):.3f}% vs second-half {100*sum(tail)/len(tail):.3f}%")
