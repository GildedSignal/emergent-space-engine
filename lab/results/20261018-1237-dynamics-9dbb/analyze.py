#!/usr/bin/env python3
"""20261018-1237-dynamics-9dbb: classify the seam map's walk from the per-crossing series.

Columns in each series file: n, k(Q48 ulps), p_sig, p_exp, w(Q32 turns), cw, r(quanta),
res_pos, res_vel. Reads index.tsv for the chain census (refusals, cycles).
"""
import glob
import os
import statistics as st
import sys
from collections import Counter

Q48 = 1 << 48
Q32 = 1 << 32
outdir = sys.argv[1] if len(sys.argv) > 1 else "series"
idx = {}
order = []
for line in open(os.path.join(outdir, "index.tsv")).read().splitlines()[1:]:
    f = line.split("\t")
    idx[f[0]] = dict(
        steps=int(f[1]), refused=f[2], col_at=f[3], col_len=f[4],
        key_at=f[5], key_len=f[6], dr=int(f[7]), file=f[8])
    order.append(f[0])

def load(cfg):
    p = os.path.join(outdir, idx[cfg]["file"])
    rows = [l.split("\t") for l in open(p).read().splitlines()]
    return dict(n=[int(x[0]) for x in rows], k=[int(x[1]) for x in rows],
                psig=[int(x[2]) for x in rows], pexp=[int(x[3]) for x in rows],
                w=[int(x[4]) for x in rows], cw=[int(x[5]) for x in rows],
                r=[int(x[6]) for x in rows], rp=[int(x[7]) for x in rows],
                rv=[int(x[8]) for x in rows])
def classify(d):
    k = d["k"]
    dk = [k[i + 1] - k[i] for i in range(len(k) - 1)]
    med = st.median(dk)
    sgn = sum(1 for x in dk if (x > 0) == (med > 0) and x != 0)
    trans = len(set(dk)) == 1
    q = len(dk) // 4
    rate_early = st.median(dk[16:512]) if len(dk) > 512 else med
    rate_late = st.median(dk[3 * q:]) if len(dk) > 1024 else None
    w = d["w"]
    dw = [w[i + 1] - w[i] for i in range(len(w) - 1)]
    bigjump = sum(1 for x in dw if abs(x) > Q32 // 256)
    r = d["r"]
    dr_rel = max(abs(x - r[0]) for x in r) / r[0]
    return dict(dk=dk, med=med, frac_sgn=sgn / len(dk), trans=trans,
                rate_early=rate_early, rate_late=rate_late,
                dk_min=min(dk), dk_max=max(dk),
                w_frozen=all(x == 0 for x in dw), w_bigjumps=bigjump,
                dw_max=max(map(abs, dw)), dr_rel=dr_rel,
                res_pos_med=st.median(d["rp"]), res_pos_spread=(max(d["rp"]) - min(d["rp"])) / max(1, st.median(d["rp"])),
                k0=k[0], kend=k[-1], steps=len(k))

print("== walk class per chain (grid, depth 1024) ==")
print(f"{'cfg':<58} {'class':<12} {'rate':>10} {'sign%':>6} {'dk min/max':>16} {'w':<9} {'dr_rel':<9} {'respos':<10} {'cyc':<5}")
grid = [c for c in order if "_d1024_grid" in c]
rows = []
for cfg in grid + [c for c in order if "_d1024_retro" in c]:
    meta = idx[cfg]
    if meta["steps"] < 64:
        print(f"{cfg:<58} REFUSED/SHORT at {meta['refused'][:40]}")
        continue
    c = classify(load(cfg))
    wtag = "frozen" if c["w_frozen"] else (f"jump{c['w_bigjumps']}" if c["w_bigjumps"] else "tiny")
    cls = "translation" if c["trans"] else ("ratchet" if c["frac_sgn"] >= 0.9 else "mixed")
    cyc = meta["key_at"] if meta["key_at"] != "null" else "-"
    print(f"{cfg:<58} {cls:<12} {c['med']:>10.0f} {100*c['frac_sgn']:>5.0f}% {c['dk_min']:>7}/{c['dk_max']:<7} {wtag:<9} {c['dr_rel']:<9.1e} {c['res_pos_med']:<10.3g} {cyc:<5}")
    rows.append((cfg, cls, c, meta))
deep = [c for c in order if "_d4096_deep" in c]
for cfg in deep:
    rows.append((cfg, "", classify(load(cfg)), idx[cfg]))

print("\n== P1: rate stability (early vs late window) ==")
for cfg, cls, c, meta in rows:
    if c["rate_late"] is not None and c["med"] != 0:
        drift = abs(c["rate_late"] - c["rate_early"]) / abs(c["rate_early"])
        print(f"{cfg[:56]:<58} rate {c['rate_early']:+.0f} -> {c['rate_late']:+.0f} ulps/crossing  change {100*drift:.1f}%")

print("\n== P2: cycle census ==")
print("key cycles among 48 grid chains:", sum(1 for c in grid if idx[c]["key_at"] != "null"))
print("column cycles anywhere:", sum(1 for c in order if idx[c]["col_at"] != "null"))
for c in order:
    if idx[c]["key_at"] != "null":
        print(f"  {c[:70]} key_cycle at {idx[c]['key_at']} len {idx[c]['key_len']}  col_cycle {idx[c]['col_at']}")

print("\n== deep arms (depth 4096) ==")
for cfg in [c for c in order if "_d4096_deep" in c]:
    meta = idx[cfg]
    c = classify(load(cfg))
    wtag = "frozen" if c["w_frozen"] else (f"jump{c['w_bigjumps']}" if c["w_bigjumps"] else "tiny")
    cls = "translation" if c["trans"] else ("ratchet" if c["frac_sgn"] >= 0.9 else "mixed")
    print(f"{cfg[:58]:<60} {cls:<12} med {c['med']:+.0f} sign {100*c['frac_sgn']:.0f}% "
          f"min/max {c['dk_min']}/{c['dk_max']} w {wtag} dr_rel {c['dr_rel']:.1e} "
          f"k: {c['k0']} -> {c['kend']} (net {c['kend']-c['k0']})")

print("\n== P4: twins (depth 8192) ==")
ta = [c for c in order if "twinA" in c][0]
tb = [c for c in order if "twinB" in c][0]
a, b = load(ta), load(tb)
ident = (a["k"] == b["k"]) and (a["w"] == b["w"]) and (a["r"] == b["r"])
print("series bit-identical:", ident)
print("\n== P4b: twin per-column divergence (depth 8192) ==")
for c in ["k", "psig", "pexp", "w", "cw", "r", "rp", "rv"]:
    diff = [i for i in range(len(a[c])) if a[c][i] != b[c][i]]
    if not diff:
        print(f"  {c}: identical over {len(a[c])} crossings")
    else:
        print(f"  {c}: diverges at {len(diff)} crossings, first {diff[0]}, "
              f"max gap {max(abs(a[c][i] - b[c][i]) for i in diff)}")

if not ident:
    first = next((i for i in range(len(a["k"])) if a["k"][i] != b["k"][i]), None)
    print("first k divergence at crossing:", first)
ca, cb = classify(a), classify(b)
print(f"rate A {ca['med']:+.0f} ({ca['dk_min']}/{ca['dk_max']}), rate B {cb['med']:+.0f} ({cb['dk_min']}/{cb['dk_max']})")
print(f"net k walk over 8192: A {a['k'][-1]-a['k'][0]:+d} ulps = {(a['k'][-1]-a['k'][0])/Q48:.3e} of range; "
      f"to reach 1% of k range: {abs(0.01*Q48/ca['med']):.2g} crossings")
print(f"w frozen over 8192: A {ca['w_frozen']} B {cb['w_frozen']}; dw max {ca['dw_max']} ({ca['dw_max']/Q32:.3f} turns)")
print(f"dr_rel A {ca['dr_rel']:.2e} vs 2^-20 = {2**-20:.2e}; res_pos median {ca['res_pos_med']:.4g}, spread {ca['res_pos_spread']:.2e}")

print("\n== P6: residual vs rate ==")
for cfg, cls, c, meta in rows:
    print(f"{cfg[:56]:<58} res_pos {c['res_pos_med']:>10.3g} res spread {c['res_pos_spread']:.1e} rate {c['med']:+.0f}")

print("\n== retro arms ==")
for cfg in [c for c in order if "_retro" in c]:
    meta = idx[cfg]
    if meta["steps"] < 64:
        print(f"{cfg[:70]} -> refused/short: {meta['refused']}")
    else:
        c = classify(load(cfg))
        cls = "translation" if c["trans"] else ("ratchet" if c["frac_sgn"] >= 0.9 else "mixed")
        wtag = "frozen" if c["w_frozen"] else (f"jump{c['w_bigjumps']}" if c["w_bigjumps"] else "tiny")
        print(f"{cfg[:70]} -> {cls} rate {c['med']:+.0f} sign {100*c['frac_sgn']:.0f}% w {wtag} dr_rel {c['dr_rel']:.1e} key_cyc {meta['key_at']}")

print("\n== class summary ==")
print(Counter(r[1] for r in rows))
