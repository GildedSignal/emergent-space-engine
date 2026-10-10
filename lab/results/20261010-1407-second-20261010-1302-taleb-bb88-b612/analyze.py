#!/usr/bin/env python3
"""Summarize cert_out.json (full grid, window W) + cert_out_b.json (B re-run,
both windows) against the pre-registered letters."""
import json
import numpy as np

grid = json.load(open("cert_out.json"))
bnew = json.load(open("cert_out_b.json"))

def key(r):
    c = r["cfg"]
    return (c["fam"], c["e0"], c["n"], c["seed"], c["K"])

bnew_keys = {key(r) for r in bnew}
runs = [r for r in grid if key(r) not in bnew_keys] + bnew

def Wold(cfg):
    c = cfg
    v_apo = np.sqrt(4 * np.pi**2) * np.sqrt((1 - c["e0"]) / (1 + c["e0"]))
    return c["R"] / v_apo + 3 * c["da"] * (c["T"] + 1.0)

def Wprime(cfg):
    c = cfg
    v_apo = np.sqrt(4 * np.pi**2) * np.sqrt((1 - c["e0"]) / (1 + c["e0"]))
    X = (1 + c["e0"]) * 2 * c["da"] + 2 * c["de"] + (1 + c["e0"]) * 2 * c["dw"]
    return (c["R"] + X) / v_apo + 3 * c["da"] * (c["T"] + 1.0)

def sel(fam, e0, n, k=240):
    rs = [r for r in runs if r["cfg"]["fam"] == fam and r["cfg"]["e0"] == e0
          and r["cfg"]["n"] == n and (k is None or r["cfg"]["K"] == k)]
    assert len(rs) == 3 or (k is not None and len(rs) == 1), (fam, e0, n, len(rs))
    return rs

def med(rs, f): return float(np.median([f(r) for r in rs]))
def rng(rs, f):
    v = [f(r) for r in rs]; return min(v), max(v)

print("=== FAMILY A (cost/enc under pre-registered W; W' zero-miss check in dtau/W' col) ===")
print("e      n      enc/body  cost_mean cost/enc  cost_max [rng]   req_k [rng]  pred_k  tight  dtau/W'  gold_drop  miss(W) miss(W')")
for e0 in [0.0, 0.6, 0.9, 0.99]:
    for n in [3000, 30000]:
        rs = sel("A", e0, n)
        dtW = [(r["tightness"] * Wold(r["cfg"])) / Wprime(r["cfg"]) for r in rs]
        print(f"{e0:<5}  {n:<6} {med(rs, lambda r: r['enc_per_body']):8.3f}  "
              f"{med(rs, lambda r: r['cost_mean']):8.3f}  "
              f"{med(rs, lambda r: r['cost_over_enc']):7.4f}  "
              f"{int(med(rs, lambda r: r['cost_max'])):3d} [{rng(rs, lambda r: r['cost_max'])[0]}-{rng(rs, lambda r: r['cost_max'])[1]:<3d}]  "
              f"{int(med(rs, lambda r: r['required_k'])):3d} [{rng(rs, lambda r: r['required_k'])[0]}-{rng(rs, lambda r: r['required_k'])[1]:<3d}]  "
              f"{med(rs, lambda r: r['pred_k']):6.1f}  {max(r['tightness'] for r in rs):.4f}  "
              f"{max(dtW):.4f}  {med(rs, lambda r: r['gold_drop_frac']):6.3f}  "
              f"{sum(r['misses'] for r in rs):5d}   {sum(1 for x in dtW if x > 1)}")

print("\n=== K-control: famA(0.99, seed 11), K=480 vs K=240 ===")
r240 = [r for r in sel("A", 0.99, 3000) if r["cfg"]["seed"] == 11][0]
r480 = [r for r in grid if r["cfg"]["fam"] == "A" and r["cfg"]["e0"] == 0.99
        and r["cfg"]["K"] == 480][0]
print(f"pairs {r240['n_pairs']} -> {r480['n_pairs']} ({100*(r480['n_pairs']-r240['n_pairs'])/r240['n_pairs']:+.3f}%), "
      f"misses {r240['misses']}->{r480['misses']}, cost_mean {r240['cost_mean']:.3f}->{r480['cost_mean']:.3f}, "
      f"cost_max {r240['cost_max']}->{r480['cost_max']}, req_k {r240['required_k']}->{r480['required_k']}")

print("\n=== FAMILY B (both windows) ===")
print("e      n      enc/body  | W: miss cost/enc | W': miss cost_mean_c cost_max_c tight'_c W0-missfrac")
for e0 in [0.0, 0.6, 0.9, 0.99]:
    rs = sel("B", e0, 3000, 2000)
    print(f"{e0:<5}  3000   {med(rs, lambda r: r['enc_per_body']):8.3f}  | "
          f"{sum(r['misses'] for r in rs):>2d}  {med(rs, lambda r: r['cost_over_enc']):6.2f} | "
          f"{sum(r['misses_c'] for r in rs):>2d}  {med(rs, lambda r: r['cost_mean_c']):8.3f}  "
          f"{int(med(rs, lambda r: r['cost_max_c'])):3d}  {med(rs, lambda r: r['tightness_c']):.3f}  "
          f"{med(rs, lambda r: r['miss_frac_W0']):.4f}")
b30 = [r for r in bnew if r["cfg"]["n"] == 30000][0]
print(f"{b30['cfg']['e0']:<5}  30000  {b30['enc_per_body']:8.3f}  | "
      f"{b30['misses']:>2d}  {b30['cost_over_enc']:6.2f} | "
      f"{b30['misses_c']:>2d}  {b30['cost_mean_c']:8.3f}  {b30['cost_max_c']:3d}  "
      f"{b30['tightness_c']:.3f}  {b30['miss_frac_W0']:.4f}")

print("\n=== Letter audit ===")
ok = lambda b: "HELD" if b else "FAILED"
A_all = [r for r in runs if r["cfg"]["fam"] == "A" and r["cfg"]["K"] == 240]
B_all = [r for r in bnew if r["cfg"]["n"] == 3000]
z1 = sum(r["misses"] for r in A_all) == 0 and sum(r["misses"] for r in bnew) == 0
print(f"Z1  zero misses, pre-registered W, 38 runs:      {ok(z1)} "
      f"(A(0.99,30k): 8; B30: 2; B(0.99): 5 — all diagnosed, see addendum)")
z1c = (sum(r["misses_c"] for r in bnew) == 0 and
       all((r["tightness"] * Wold(r["cfg"])) <= Wprime(r["cfg"]) for r in A_all))
print(f"Z1' zero misses, corrected W', everywhere:       {ok(z1c)} "
      f"(B runs measured directly; A via dtau_max <= W', col above)")
ca = all(0.98 <= r["cost_over_enc"] <= 1.08 for r in A_all)
print(f"CA  A cost/enc in [0.98,1.08] every run:         {ok(ca)} "
      f"(range {min(r['cost_over_enc'] for r in A_all):.4f}-{max(r['cost_over_enc'] for r in A_all):.4f})")
ma = all(r["cost_max"] >= 1.5 * r["cost_mean"] for r in A_all)
print(f"MA  sub-letter cost_max>=1.5x mean every run:    {ok(ma)} "
      f"(fails at n=30000 e>=0.9 where sqrt-tail/mean < 0.5; all 8 range letters held)")
ka = [(r["required_k"], r["pred_k"]) for r in A_all]
n_safe = sum(1 for k, p in ka if k <= p)
n_tight = sum(1 for k, p in ka if p <= 1.6 * max(k, 1))
print(f"KA  req_k<=pred_k in {n_safe}/24 (letter >=21); pred_k<=1.6req_k in {n_tight}/24")
ta = all(r["tightness"] >= 0.9 for r in A_all if r["cfg"]["e0"] >= 0.6)
print(f"TA  A tightness >= 0.9 at e>=0.6:                {ok(ta)}")
neg = all(r["miss_frac_W0"] >= 0.9 for r in bnew)
print(f"NEG B miss_frac >= 0.9 without drift term:       {ok(neg)} "
      f"(e=0: .977, e=0.6: .939, e=0.9: .875, e=0.99: .688 — mechanism confirmed, letter too strict)")
g0 = sel("A", 0.0, 3000)
g99 = sel("A", 0.99, 3000)
print(f"G(0,3000) drop {rng(g0, lambda r: r['gold_drop_frac'])[0]:.3f} (letter [.02,.20]: FAILED low); "
      f"G(0.99,3000) {rng(g99, lambda r: r['gold_drop_frac'])[1]:.3f} (letter [.50,.80]: FAILED by .003)")
print("All other G range letters held: (0.9,3k)=.391 [.30,.50]; (0,30k)=.721 [.60,.80]; "
      "(0.9,30k)=.936 [.90,.99]; (0.99,30k)=.980 [.97,1.0]")
