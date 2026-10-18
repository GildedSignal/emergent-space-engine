#!/usr/bin/env python3
"""Tables and fits for the fill ladder. Usage: python3 analyze.py [fill.jsonl]"""
import json, sys, math
from collections import defaultdict

rows = [json.loads(l) for l in open(sys.argv[1] if len(sys.argv) > 1 else "fill.jsonl")]
arms = [r for r in rows if "tag" in r]
phi = defaultdict(list)
for r in arms:
    if r["tag"] in ("phi", "heldout") and r["n"] == 400 and r["vmax"] == 131072:
        phi[r["phi"]].append(r)

print("== phi ladder (n=400, vmax=2^17, all seeds; rate per body per chronon) ==")
print(f"{'phi':>5} {'seeds':>5} {'nu_meas':>8} {'nu_Hend':>8} {'g_eff/gH':>8} {'fano1':>6} {'fano64':>7} {'p99/p50':>7} {'maxcomp':>7} {'distinct':>8} {'maxbatch':>8} {'maxpairs':>8} {'maxwalls':>8} {'ops/fired':>9} {'meanops/n':>9}")
for p in sorted(phi):
    rs = phi[p]
    n = len(rs)
    mean = lambda k: sum(r[k] for r in rs) / n
    print(f"{p:>5} {n:>5} {mean('rate_per_body'):>8.4f} {mean('nu_enskog'):>8.4f} {mean('rate_per_body')/mean('nu_enskog'):>8.3f} {mean('fano1'):>6.3f} {mean('fano64'):>7.3f} {mean('spike_ratio'):>7.3f} {max(r['max_component'] for r in rs):>7} {mean('distinct_frac'):>8.4f} {max(r['max_batch'] for r in rs):>8} {max(r['max_pairs'] for r in rs):>8} {max(r['max_walls'] for r in rs):>8} {mean('ops_per_fired'):>9.1f} {mean('meanops')/400:>9.2f}")

print("\n== P1 control: dilute free-flight check (phi=0.05) ==")
for r in sorted(phi[0.05], key=lambda r: r["seed"]):
    print(f"seed {r['seed']}: measured {r['rate_per_body']:.6f}, Enskog-Henderson {r['nu_enskog']:.6f}, ratio {r['rate_per_body']/r['nu_enskog']:.4f}")

print("\n== P5: speed linearity at phi=0.3 ==")
sp = defaultdict(list)
for r in arms:
    if r["tag"] == "speed":
        sp[r["vmax"]].append(r)
for v in sorted(sp):
    for r in sp[v]:
        print(f"vmax 2^{int(math.log2(v))}: nu {r['rate_per_body']:.6f}, mean|w|/Q {r['mean_w']/1048576:.6f}, nu/(|w|/Q) {r['rate_per_body']/(r['mean_w']/1048576):.6f}, fano1 {r['fano1']:.3f}")
for r in phi[0.3]:
    print(f"vmax 2^17: nu {r['rate_per_body']:.6f}, mean|w|/Q {r['mean_w']/1048576:.6f}, nu/(|w|/Q) {r['rate_per_body']/(r['mean_w']/1048576):.6f}")

print("\n== P6: scale n=1600 vs n=400 ==")
for r in arms:
    if r["n"] == 1600:
        ref = [x for x in phi[r["phi"]] if x["seed"] == r["seed"]]
        b = ref[0] if ref else None
        if b:
            print(f"phi {r['phi']}: n1600 nu {r['rate_per_body']:.5f} vs n400 {b['rate_per_body']:.5f} (x{r['rate_per_body']/b['rate_per_body']:.3f}), fano1 {r['fano1']:.3f} vs {b['fano1']:.3f}, meanops/n {r['meanops']/1600:.2f} vs {b['meanops']/400:.2f}, maxcomp {r['max_component']} vs {b['max_component']}")

print("\n== cost law fit: meanops/n = a + b*nu (phi ladder, all seeds) ==")
xs = [r["rate_per_body"] for p in phi for r in phi[p]]
ys = [r["meanops"] / 400 for p in phi for r in phi[p]]
mx, my = sum(xs)/len(xs), sum(ys)/len(ys)
b = sum((x-mx)*(y-my) for x, y in zip(xs, ys)) / sum((x-mx)**2 for x in xs)
a = my - b*mx
pred = [a + b*x for x in xs]
worst = max(abs(y-p)/y for y, p in zip(ys, pred))
print(f"a={a:.2f}, b={b:.2f}, worst relative deviation {worst*100:.1f}%")

print("\n== predictions audit ==")
f1 = max(r["fano1"] for r in arms if r["n"] == 400)
spike = max(r["spike_ratio"] for r in arms)
print(f"max fano1 (n=400 arms): {f1:.3f} (P3 kill at 1.5; predict <1)")
print(f"max p99/p50: {spike:.3f} (P4 predict <1.15)")
print(f"max component: {max(r['max_component'] for r in arms if r['n']==400)} at n=400 (P4 line n/20=20)")
mc1600 = max((r['max_component'] for r in arms if r['n'] == 1600), default=0)
print(f"max component n=1600: {mc1600} (P4 line n/20=80)")
rh = [(r["phi"], r["rate_per_body"]/r["nu_enskog"]) for r in arms if r["n"]==400 and r["vmax"]==131072]
hi = [x for x in rh if x[0] >= 0.7]
print(f"measured/Henderson at phi>=0.7: max {max(x[1] for x in hi):.3f} (P2 predict <0.85), global max {max(x[1] for x in rh):.3f} (never >1.15)")
mb = [(r, r["max_batch"]) for r in arms if r["max_batch"] > 100]
for r, m in mb[:6]:
    print(f"maxbatch {m} at phi {r['phi']}: maxops/p50 {r['maxops']/r['p50ops']:.3f}, max_pairs {r['max_pairs']}, max_walls {r['max_walls']} (P7 wall-flash)")
