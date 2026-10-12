#!/usr/bin/env python3
"""B12 statistic probe: bounded energy error vs slow leak.

Statistics compared on identical streams:
  expo   : log-log slope of max|e| vs t over the horizon (B12-current style)
  ratio  : RMS(last decile)/RMS(first decile) of e (redteam-b12-stat's recurrence ratio)
  cusum  : two-sided CUSUM on the error increments, C+ = max(0, C+ + (x-k)),
           C- = max(0, C- - (x-k)); alarm when max(C+,C-) > h.

Calibration (arm 0/1 only) fixes k, h, and every threshold; held-out arms P1-P4
are then run once. Seeds 0..199 per arm. All floats here; on the plane the same
CUSUM runs on the integer energy register in integers (deterministic).
"""
import numpy as np

T, NSEED = 20_000, 200
ARMS = {
    "c0_neg":   dict(bnd=1.0, leak=0.0,   tail="n"),   # negative control
    "c1_pos":   dict(bnd=1.0, leak=0.02,  tail="n"),   # positive control (large leak)
    "P1_match": dict(bnd=5.0, leak=0.001, tail="n"),   # bounded 5x leak drift; both present
    "P2_halfc": dict(bnd=2.0, leak=0.0005,tail="n"),   # leak halved vs c1 factor 40 below
    "P3_tail":  dict(bnd=2.0, leak=0.0,   tail="t"),   # heavy-tailed bounded noise
    "P4_echo":  dict(bnd=3.0, leak=0.0,   tail="z"),   # pure periodic, zero noise
}

def stream(seed, bnd, leak, tail):
    rng = np.random.default_rng(seed)
    w = 2 * np.pi / 1234.0                      # slow oscillation
    osc = bnd * np.sin(w * np.arange(T) + rng.uniform(0, 2 * np.pi))
    if tail == "z":
        inc = np.zeros(T)
    elif tail == "t":
        inc = rng.standard_t(3, T)
    else:
        inc = rng.standard_normal(T)
    rw = np.cumsum(0.05 * inc)                  # bounded-ish noise part, zero mean
    drift = leak * np.arange(T)                 # the leak
    e = osc + 0.1 * rw + drift
    return e

def cusum(e, k, h):
    x = np.diff(e, prepend=e[0])
    Cp = Cm = 0.0
    best = 0.0; alarm = T
    for t, xt in enumerate(x):
        Cp = max(0.0, Cp + xt - k)
        Cm = max(0.0, Cm - xt - k)
        m = max(Cp, Cm)
        if m > best: best = m
        if m > h and alarm == T: alarm = t
    return alarm, best

def expo(e):
    t = np.maximum(np.arange(1, T + 1), 1)
    runmax = np.maximum.accumulate(np.abs(e))
    a = np.log(t); b = np.log(np.maximum(runmax, 1e-12))
    n = T // 2
    return (b[n:].mean() - b[:n].mean()) / (a[n:].mean() - a[:n].mean())

def ratio(e):
    d = T // 10
    return e[-d:].std() / max(e[:d].std(), 1e-12)

# --- calibration on controls only ---
neg = [stream(s, **{k2: v for k2, v in ARMS["c0_neg"].items()}) for s in range(30)]
pos = [stream(s, **{k2: v for k2, v in ARMS["c1_pos"].items()}) for s in range(30)]
k = 0.5 * ARMS["c1_pos"]["leak"]                 # standard allowance = half the leak to catch
h = 1.5 * max(cusum(e, k, np.inf)[1] for e in neg)  # 1.5x worst negative-control peak
thr_ratio = 0.5 * min(ratio(e) for e in pos)     # below the weakest positive control
print(f"calibration: k={k:.5g} h={h:.4g} thr_ratio={thr_ratio:.4g}")

results = {}
for name, cfg in ARMS.items():
    det = {"cusum": 0, "ratio": 0, "expo": 0}
    cross = []
    for s in range(NSEED):
        e = stream(s, **cfg)
        a, _ = cusum(e, k, h)
        if a < T: det["cusum"] += 1
        if ratio(e) > thr_ratio: det["ratio"] += 1
        if expo(e) > 0.5: det["expo"] += 1
        cross.append(a)
    cross = np.array(cross)
    results[name] = (det, cross)
    print(f"{name:9s} detect cusum/ratio/expo = {det['cusum']:3d}/{det['ratio']:3d}/{det['expo']:3d}"
          f"  cusum median alarm = {np.median(cross[cross < T]) if (cross < T).any() else -1:.0f}")

# --- verdicts against predictions.md ---
def pct(x): return 100.0 * x / NSEED
print("\nverdicts:")
p1 = results["P1_match"][0]
print(f"P1: cusum catches leak {pct(p1['cusum']):.0f}% (pred >=95); expo flags {pct(p1['expo']):.0f}% at 5x-bounded amplitude")
d1, x1 = results["c1_pos"]; d2, x2 = results["P2_halfc"]
m1 = np.median(x1[x1 < T]) if (x1 < T).any() else -1
m2 = np.median(x2[x2 < T]) if (x2 < T).any() else -1
print(f"P2: leak halved -> cusum detect {pct(d2['cusum']):.0f}%, median alarm {m1:.0f} -> {m2:.0f} (pred ~2x = {2*m1:.0f}); ratio detect {pct(d2['ratio']):.0f}%")
print(f"P3: heavy-tailed bounded false alarm {pct(results['P3_tail'][0]['cusum']):.0f}% (pred <5)")
print(f"P4: pure echo false alarm {pct(results['P4_echo'][0]['cusum']):.0f}% (pred 0)")
print(f"controls: pos cusum {pct(results['c1_pos'][0]['cusum']):.0f}% (must be 100), neg cusum {pct(results['c0_neg'][0]['cusum']):.0f}% (must be 0)")
