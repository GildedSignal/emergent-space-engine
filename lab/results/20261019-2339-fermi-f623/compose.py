#!/usr/bin/env python3
"""Compose the mint stream's machine floors at 1e9 from the probe arms + the record's constants.
Every input digit is either read from a log in this folder or cited from lab/wiki/budget-1e9.md."""
import re

GB = 1e9
M1_BW_GB_S = 60.0        # derated LPDDR4X; the board's own number (bottleneck 0)
LAMBDA_LOW, LAMBDA_HIGH = 4e-5, 8.4e-5  # per body per game-s: 0659/3aec band; f80a's 8.397e-5 at 3e4
RTF = 100.0
N9 = 1e9
PAIR_NS = 11.6           # measured this box, bench_malloc: alloc+touch+free of 192-288 B

def parse(path):
    wins, tot, hist = [], None, {}
    for line in open(path):
        m = re.match(r"alloc: f=(\d+) gs=([\d.]+) kicks=(\d+) evs=(\d+) allocs=(\d+) frees=(\d+) reallocs=(\d+) ab=(\d+) fb=(\d+)", line)
        if m:
            wins.append(dict(f=int(m[1]), gs=float(m[2]), kicks=int(m[3]), evs=int(m[4]),
                             allocs=int(m[5]), frees=int(m[6]), reallocs=int(m[7]),
                             ab=int(m[8]), fb=int(m[9])))
        m = re.match(r"totals: frames (\d+) game_s ([\d.]+) kicks (\d+) .*? allocs (\d+) frees (\d+)", line)
        if m:
            tot = dict(frames=int(m[1]), gs=float(m[2]), kicks=int(m[3]), allocs=int(m[4]), frees=int(m[5]))
        if line.startswith("hist"):
            h = {k: int(v) for k, v in re.findall(r"(\d+|>2048):(\d+)", line)}
            hist = {(2049 if k == ">2048" else int(k)): v for k, v in h.items()}
    return wins, tot, hist

def ols(xs, ys, intercept=False):
    n = len(xs); mx = sum(xs)/n; my = sum(ys)/n
    sxx = sum((x-mx)**2 for x in xs); sxy = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
    b = sxy/sxx if sxx else 0.0
    return (b, my - b*mx) if intercept else b

rows = []
for name, path in [("1e4", "arm_1e4_coast.log"), ("3e4", "arm_3e4_coast.log")]:
    wins, tot, hist = parse(path)
    k = tot["kicks"]
    per = dict(arm=name, kicks=k, gs=tot["gs"], evs=sum(w["evs"] for w in wins))
    per["allocs_k"] = tot["allocs"]/k
    per["frees_k"] = tot["frees"]/k
    per["ab_k"] = sum(w["ab"] for w in wins)/k      # totals line's byte slots are shifted (disclosed bug); window sums are exact
    per["fb_k"] = sum(w["fb"] for w in wins)/k
    per["rl_k"] = sum(w["reallocs"] for w in wins)/k
    ks = [w["kicks"] for w in wins if w["kicks"] > 0]
    ab_w = [w["ab"] for w in wins if w["kicks"] > 0]
    al_w = [w["allocs"] for w in wins if w["kicks"] > 0]
    per["ab_ols"], per["ab_b0"] = ols(ks, ab_w, intercept=True)
    per["allocs_ols"] = ols(ks, al_w)
    gs_per_win = per["gs"]/len(ks)
    per["base_kb_gs"] = per["ab_b0"]/1024.0/gs_per_win
    fam = [88, 240, 304, 352, 384, 704, 832]
    per["fam_calls"] = sum(hist.get(s, 0) for s in fam)
    per["le2048_bytes"] = sum(s*c for s, c in hist.items() if s <= 2048)
    rows.append(per)
    print(f"[{name}] kicks {k} gs {per['gs']:.0f} evs {per['evs']} | allocs/kick {per['allocs_k']:.1f} frees/kick {per['frees_k']:.1f} "
          f"reallocs/kick {per['rl_k']:.1f} | naive ab/kick {per['ab_k']/1024:.2f} KB fb/kick {per['fb_k']/1024:.2f} KB | "
          f"OLS marginal ab/kick {per['ab_ols']/1024:.2f} KB allocs/kick {per['allocs_ols']:.1f} | "
          f"base churn {per['base_kb_gs']:.0f} KB/gs (N-flat if equal across arms) | "
          f"family calls/kick {per['fam_calls']/k:.2f}")

le = rows[0]["le2048_bytes"]; abw = rows[0]["ab_k"]*rows[0]["kicks"]
print(f"[1e4] hist bytes <=2048: {le/GB:.2f} GB of window ab {abw/GB:.2f} GB -> >2048 scratch {(abw-le)/GB:.2f} GB ({(abw-le)/abw*100:.0f}%), ~0.56 calls/kick at ~15 KB avg")

print("\n=== composition at 1e9, rtf 100 (marginal attribution; naive average in parens) ===")
marg_b = max(r["ab_ols"] for r in rows)
naive_b = max(r["ab_k"] for r in rows)
marg_c = max(r["allocs_ols"]*2 for r in rows)   # allocs + similar frees
naive_c = max(r["allocs_k"]+r["frees_k"] for r in rows)
for lam in (LAMBDA_LOW, LAMBDA_HIGH):
    rate = lam*N9*RTF
    print(f"lambda {lam:.1e}: kicks/s {rate:.2e} | alloc calls/s {rate*marg_c:.2e} -> {rate*marg_c*PAIR_NS/2*1e-9:.2f} cores "
          f"(naive {rate*naive_c*PAIR_NS/2*1e-9:.2f}) | bytes {rate*marg_b/GB:.1f} GB/s = {rate*marg_b/GB/M1_BW_GB_S*100:.0f}% of 60 "
          f"(naive {rate*naive_b/GB:.0f} GB/s = {rate*naive_b/GB/M1_BW_GB_S*100:.0f}%) | split8 marginal {rate*marg_b/8/GB:.1f} GB/s ({rate*marg_b/8/GB/M1_BW_GB_S*100:.0f}%)")

print("""
=== the ledger after every owned lever (1e9, rtf 100; cited rows unchanged) ===
row                      today                          with owned levers              closes?
kick stream CPU          193 c (82.5us x86) [3aec]      3.3 c (split8 + 4us Carlson)   yes
allocator CPU  (NEW)     0.6-1.7 c (marginal-naive)     0.05-0.2 c (split8)           yes
mint byte traffic (NEW)  13.6-28.5 GB/s marginal (23-48% of  1.7-3.6 GB/s (3-6%) split8    yes: material, not a wall;
                         60; naive 51-107 in waves)     (no lever touches bytes;      pooling the >2KB scratch
                                                         optional)                     cuts 2-3x)
live mint ratchet        4 GB/s fresh pages             0.5 GB/s (split8)              yes w/ fence+prune [f80a/b911]
state store              2.35 TB shipped                6 GB compact (<=48b)           wiring [097e]
player root item         ~2 h freeze/burn               unchanged by every lever      NO: law change [cc9d]
""")
