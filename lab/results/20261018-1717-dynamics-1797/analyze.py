#!/usr/bin/env python3
"""Analyze the circle-ratchet deep run: deceleration law, collapse, w lottery, radius."""
import json, math, sys

UNIT = 1 << 48
rows = [json.loads(l) for l in open(sys.argv[1] if len(sys.argv) > 1 else "deep.jsonl")]
arms = {}
for r in rows:
    arms.setdefault(r["arm"], []).append(r)

def wrap_turns(dw_u32):
    x = dw_u32 / 2**32
    return x - 1.0 if x > 0.5 else x

def slope(xs, ys):
    n = len(xs); mx = sum(xs)/n; my = sum(ys)/n
    sxx = sum((x-mx)**2 for x in xs); sxy = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
    return sxy/sxx if sxx else float('nan')

print(f"{'arm':18s} {'n':>6s} {'neg%':>5s} {'D(n)':>10s} {'rate_last_dec':>13s} {'alpha':>6s} {'beta':>6s} {'maxlnr':>9s} {'residP_rel':>10s} {'lastsign'}")
summary = {}
for arm, a in arms.items():
    n = len(a)
    dk = [r["k2"] - r["k"] for r in a]
    neg = sum(1 for d in dk if d < 0) / n
    D = UNIT - a[-1]["k2"]  # total deficit
    # decade windows: mean one-signed rate
    wins = []
    j = 0
    while (1 << (j+1)) <= n:
        lo, hi = 1 << j, 1 << (j+1)
        w = [dk[i] for i in range(lo, min(hi, n))]
        if w: wins.append((lo, sum(w)/len(w)))
        j += 1
    # alpha: slope of log(-rate) vs log(n) over last 4 windows
    fit = wins[-4:] if len(wins) >= 4 else wins
    use = [(lo, r) for lo, r in fit if r < 0]
    alpha = slope([math.log(lo) for lo, _ in use], [math.log(-r) for _, r in use]) if len(use) >= 2 else float('nan')
    # beta: slope of log D(n) vs log n at decade points
    pts = []
    j = 0
    while (1 << j) < n:
        i = min(1 << j, n-1)
        pts.append((i+1, UNIT - a[i]["k2"]))
        j += 1
    fitd = pts[-4:] if len(pts) >= 4 else pts
    beta = slope([math.log(i) for i, _ in fitd], [math.log(max(d, 1)) for _, d in fitd]) if len(fitd) >= 2 else float('nan')
    sign = 'mixed' if any(r > 0 for _, r in wins[-4:]) else 'neg'
    r0 = a[0]["r"]; maxlr = max(abs(math.log(r / r0)) for r in (x["r"] for x in a))
    maxres = max(max(x["res_p"], 1) for x in a)
    word = 2.0**61  # position quanta relative
    print(f"{arm:18s} {n:6d} {neg*100:4.0f}% {D:10.3e} {abs(wins[-1][1]):13.1f} {alpha:6.3f} {beta:6.3f} {maxlr:9.2e} {maxres:10.3e} {sign}")
    summary[arm] = dict(n=n, neg=neg, D=D, wins=wins, alpha=alpha, beta=beta, a=a)

# collapse: rate vs D (binned), all e0 arms + em6/em3
print("\n== rate(D) collapse (mean |dk| in D-decade bins) ==")
print(f"{'Dbin':>10s} " + " ".join(f"{a[:9]:>9s}" for a in summary))
bins = [2**k for k in range(8, 42)]
for arm, s in summary.items():
    a = s["a"]
table = {}
for arm, s in summary.items():
    for i, r in enumerate(s["a"]):
        d = UNIT - r["k"]
        b = int(math.log2(max(d, 1)))
        dk = r["k2"] - r["k"]
        table.setdefault(b, {}).setdefault(arm, []).append(dk)
for b in sorted(table):
    line = []
    for arm in summary:
        v = table[b].get(arm)
        line.append(f"{-sum(v)/len(v):9.1f}" if v else f"{'—':>9s}")
    print(f"2^{b:<7d} " + " ".join(f"{x:>9s}" for x in line))

# sqrt-law constant C = D * rate at the last decade; price of 1% of k range
print("\n== price of D* = 1% of k range (0.01*2^48 = 2.8e12 ulps) ==")
for arm, s in summary.items():
    if "e0" not in arm: continue
    D = s["D"]; rate = -s["wins"][-1][1]; n = s["n"]
    C = D * rate
    Dstar = 0.01 * UNIT
    n_sqrt = Dstar**2 / (2 * C) if C > 0 else float('inf')
    n_lin = Dstar / rate if rate > 0 else float('inf')
    print(f"{arm:18s} C={C:.3e}  n*(sqrt)={n_sqrt:.2e}  n*(linear)={n_lin:.2e}  measured n={n}")

# w lottery: per-crossing increments, cumulative path vs sqrt envelope
print("\n== w column ==")
for arm, s in summary.items():
    a = s["a"]
    dw = [wrap_turns((r["w2"] - r["w"]) % 2**32) for r in a]
    m = len(dw); mu = sum(dw)/m; var = sum((x-mu)**2 for x in dw)/m
    cum = 0.0; maxdev = 0.0
    for k, x in enumerate(dw):
        cum += x
        maxdev = max(maxdev, abs(cum))
    env = 5 * math.sqrt(m * var)
    absmean = sum(abs(x) for x in dw)/m
    print(f"{arm:18s} mean_dw={mu:+.2e} sigma={math.sqrt(var):.3f} turns  mean|dw|={absmean:.3f}  max|cum|={maxdev:.2f}  5sqrt-envelope={env:.1f}  {'OK' if maxdev < env else 'RAILED'}")

# p (periapsis) column drift
print("\n== periapsis column ==")
for arm, s in summary.items():
    p0 = s["a"][0]["p"]; pn = s["a"][-1]["p2"]
    print(f"{arm:18s} p0={p0:.6e} pN={pn:.6e} rel={(pn/p0-1):+.2e}")
