#!/usr/bin/env python3
"""Cadence analysis: k_req per bin, bimodality, T_div collapse, adaptive-rule saving.

Usage: python3 analyze_cadence.py backup.npz [T_run]
"""
import numpy as np, os, sys
OUT = os.path.dirname(os.path.abspath(__file__))
fn = sys.argv[1] if len(sys.argv) > 1 else "backup.npz"
T_run = float(sys.argv[2]) if len(sys.argv) > 2 else 150.0
TOLC = 1e-4  # B12's Jacobi threshold (frozen before the sweep, predictions.md)
z = np.load(os.path.join(OUT, fn))
za = np.load(os.path.join(OUT, "atlas.npz"))

a0 = z["a0"]
n = len(a0)
binid = np.round(a0 * 200).astype(int)  # 0.005 bins
bins = np.unique(binid)
ab = bins / 200.0

# T_div median per bin from the mu=1e-3 atlas (same grid)
td = za["mu_0.001"]
aa = za["mu_0.001_a"]
tdiv = {}
for b in np.unique(aa):
    v = td[aa == b]
    tdiv[np.round(b * 200)] = np.median(v) if np.any(np.isfinite(v)) else np.inf
Td = np.array([tdiv[b] for b in binid])

truth_dc = z["truth_maxdc"]
dmin = z["truth_dmin"]
print("truth: maxdc p50/p95/p99 = %.1e %.1e %.1e ; dmin<0.05: %d ; dmin<0.1: %d" %
      (np.nanpercentile(truth_dc, 50), np.nanpercentile(truth_dc, 95),
       np.nanpercentile(truth_dc, 99), (dmin < 0.05).sum(), (dmin < 0.1).sum()))

ks = [2, 4, 8, 16, 32, 64]
DC = {k: z[f"k{k}_maxdc"] for k in ks}

print("\n=== per-bin required cadence (75th pct of maxdc < 1e-4) ===")
kreq = {}
for b in bins:
    m = binid == b
    kr = None
    for k in ks:
        if np.nanquantile(DC[k][m], 0.75) < TOLC:
            kr = k
            break
    kreq[b] = kr if kr else 999
for i, b in enumerate(bins):
    if i % 4 == 0 or kreq[b] not in (4, None, 999):
        print(f"a={b/200:.3f} T_div={tdiv[b]:7.0f}  k_req={kreq[b]}")
kr_arr = np.array([kreq[b] for b in bins])

print("\n=== bimodality at k=8 ===")
d8 = DC[8]
q = np.nanquantile(d8, [0.25, 0.5, 0.75, 0.9])
print("k=8 maxdc quartiles:", np.round(q, 6))
lo = d8[d8 < 1e-5]
hi = d8[d8 > 1e-3]
print("bodies <1e-5: %d (%.0f%%)  bodies >1e-3: %d (%.0f%%)  between: %d" %
      (len(lo), 100*len(lo)/n, len(hi), 100*len(hi)/n, n-len(lo)-len(hi)))
quiet = Td > T_run
chao = Td <= T_run
print("among T_div>T_run (quiet, n=%d): frac>1e-3 = %.0f%%" % (quiet.sum(), 100*np.mean(d8[quiet] > 1e-3)))
print("among T_div<=T_run (chaotic, n=%d): frac>1e-3 = %.0f%%" % (chao.sum(), 100*np.mean(d8[chao] > 1e-3)))

print("\n=== collapse: ln(h_req) vs 11.5*T_run/T_div (transition bins) ===")
# h_req = P/k_req ; use bins with defined k_req in (4..64) and finite T_div<=2000
X, Y, TT = [], [], []
for i, b in enumerate(bins):
    if 4 <= kr_arr[i] <= 64 and np.isfinite(tdiv[b]) and tdiv[b] <= 2000:
        P = 2*np.pi*(b/200)**1.5
        X.append(11.5*T_run/tdiv[b])
        Y.append(np.log(P/kr_arr[i]))
        TT.append(tdiv[b])
X, Y = np.array(X), np.array(Y)
if len(X) >= 3:
    sl, ic = np.polyfit(X, Y, 1)
    print("n=%d bins  slope=%.3f (chaos-amplification predicts ~ -1/2)  R2=%.2f" %
          (len(X), sl, 1 - np.var(Y - (sl*X+ic))/np.var(Y)))
else:
    print("only %d transition bins with defined k_req" % len(X))

print("\n=== adaptive rule saving ===")
kmin, kmax = 4, 128
for C in [4, 8, 16, 32]:
    kv = np.clip(np.ceil(C * 2*np.pi*a0**1.5 / np.where(np.isfinite(Td), Td, 1e9)), kmin, kmax).astype(int)
    ok = np.zeros(n, bool)
    for i in range(n):
        cands = [k for k in ks if k >= kv[i]] or [64]
        for k in cands:
            if np.isfinite(DC[k][i]) and DC[k][i] < TOLC:
                ok[i] = True
                break
    tot_ad = kv.sum()
    # uniform cadence that holds bins where any k<=64 works
    uni = max((kreq[b] for b in bins if kreq[b] and kreq[b] <= 64), default=64)
    judged = np.array([kreq[b] not in (None, 999) or True for b in binid])
    print("C=%2d: total kicks adaptive=%d  uniform(%d)=%d  ratio=%.2f  "
          "bodies passing tol at own cadence=%d/%d" %
          (C, tot_ad, uni, uni*n, tot_ad/(uni*n), ok.sum(), n))
