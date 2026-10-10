#!/usr/bin/env python3
"""Analyze decisive.json: rho law, diffusion border, chaos inheritance."""
import json
import sys
import numpy as np

d = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "decisive.json"))
rows = d["rows"]
mus = sorted({r["mu"] for r in rows})
ns = sorted({r["n"] for r in rows})

def med(rs, key):
    v = [x[key] for x in rs if x.get(key) is not None]
    return float(np.median(v)) if v else None

print("=== per-config medians (6 seeds) ===")
print("mu      eps      n    rho_med  gz_end  gJ     dJ_end    e_err    d2_end   dtwin0   walk(gz>0.3)")
tab = {}
for r in rows:
    rs = r["seeds"]
    rho = med(rs, "rho"); gz = med(rs, "gz_end"); gJ = med(rs, "gJ")
    dJ = med(rs, "dJ_end"); ee = med(rs, "e_err"); d2 = med(rs, "d2_end")
    nw = sum(1 for x in rs if (x["gz"] or -1) > 0.3)
    tab[(r["mu"], r["n"])] = dict(rho=rho, gz_end=gz, gJ=gJ, dJ=dJ, e_err=ee,
                                  d2=d2, nw=nw)
    print("%.3g %8.2e %4d %8.4f %7.2f %6.2f %9.2e %8.2e %8.1e %8.1e %d/6"
          % (r["mu"], r["eps"], r["n"], rho if rho else -1, gz if gz is not None else -9,
             gJ if gJ is not None else -9, dJ, ee, d2 if d2 else -1,
             r.get("dtwin", {}).get("0", -1), nw))

# --- P1: rho ~ C mu^a n^-b (fit on medians, require rho data) ---
X, Y, W = [], [], []
for (mu, n), t in tab.items():
    if t["rho"] and t["rho"] > 0:
        X.append([np.log(mu), np.log(n)])
        Y.append(np.log(t["rho"]))
X = np.array(X); Y = np.array(Y)
c, res_, rank, sv = np.linalg.lstsq(np.column_stack([X, np.ones_like(Y)]), Y, rcond=None)
a, b, C = c[0], -c[1], np.exp(c[2])
resid = Y - (c[0] * X[:, 0] - c[1] * X[:, 1] + c[2])
print("\n=== P1 fit: rho = C * mu^%.2f * n^-%.2f, C=%.1f, max|resid|=%.2f (ln) ==="
      % (a, b, C, np.max(np.abs(resid))))
print("    per-n mu-exponents:",
      {n: round(float(np.polyfit([np.log(m) for m in mus if (m, n) in tab and tab[(m, n)]["rho"]],
                                 [np.log(tab[(m, n)]["rho"]) for m in mus if (m, n) in tab and tab[(m, n)]["rho"]], 1)[0]), 2)
       for n in ns if sum(1 for m in mus if (m, n) in tab and tab[(m, n)]["rho"]) >= 3})
print("    per-mu n-exponents:",
      {mu: round(float(np.polyfit([np.log(n) for n in ns if (mu, n) in tab and tab[(mu, n)]["rho"]],
                                  [np.log(tab[(mu, n)]["rho"]) for n in ns if (mu, n) in tab and tab[(mu, n)]["rho"]], 1)[0]), 2)
       for mu in mus if sum(1 for n in ns if (mu, n) in tab and tab[(mu, n)]["rho"]) >= 3})

# --- border n*(mu) at rho = 0.10 ---
print("\n=== rho=10% border n*(mu) ===")
bord = {}
for mu in mus:
    pts = sorted((n, tab[(mu, n)]["rho"]) for n in ns
                 if (mu, n) in tab and tab[(mu, n)]["rho"])
    lo = [p for p in pts if p[1] <= 0.10]
    hi = [p for p in pts if p[1] > 0.10]
    if lo and hi and lo[-1][0] < hi[0][0]:
        n1, r1 = lo[-1]; n2, r2 = hi[0]
        s = np.log(r2 / r1) / np.log(n2 / n1)
        nstar = n1 * (0.10 / r1) ** (1 / s)
        bord[mu] = nstar
        print("  mu=%.3g: n* = %.1f  (between n=%d rho=%.3f and n=%d rho=%.3f)"
              % (mu, nstar, n1, r1, n2, r2))
    else:
        print("  mu=%.3g: border outside grid (rho range %.2g..%.2g)"
              % (mu, pts[0][1] if pts else -1, pts[-1][1] if pts else -1))
if len(bord) >= 3:
    ls = np.polyfit(np.log(list(bord.keys())), np.log(list(bord.values())), 1)
    print("  n* ~ mu^%.2f  (P1 predicts 0.5)" % ls[0])

# --- P2: diffusion border (gz_end ~ 0.5 vs ~1) ---
print("\n=== P2: late-window exponent gz_end (1=drift, 0.5=walk) ===")
for mu in mus:
    line = " ".join("n%d:%.2f" % (n, tab[(mu, n)]["gz_end"])
                    for n in ns if (mu, n) in tab and tab[(mu, n)]["gz_end"] is not None)
    print("  mu=%.3g  %s" % (mu, line))

# --- P3: chaos inheritance ---
print("\n=== P3: d2_end(map twin) vs dtwin(truth twin) ===")
for r in rows:
    if r["n"] in (4, 32) or (r["mu"] == 0.2):
        dt0 = r.get("dtwin", {}).get("0", float("nan"))
        print("  mu=%.3g n=%4d d2_end=%.2e dtwin0=%.2e ratio=%.1f"
              % (r["mu"], r["n"], med(r["seeds"], "d2_end"), dt0,
                 med(r["seeds"], "d2_end") / dt0 if dt0 else float("nan")))

# --- P4: seed nonuniformity ---
print("\n=== P4: seed spread in rho (max/min) ===")
for r in rows:
    rh = sorted(x["rho"] for x in r["seeds"] if x.get("rho"))
    if len(rh) >= 4:
        print("  mu=%.3g n=%4d min=%.3f med=%.3f max=%.3f ratio=%.1f"
              % (r["mu"], r["n"], rh[0], rh[len(rh) // 2], rh[-1], rh[-1] / max(rh[0], 1e-9)))
