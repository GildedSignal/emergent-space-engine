#!/usr/bin/env python3
"""B12 statistic probe v2 — bounded vs compounding energy error, per-orbit sampling.

Regimes: (i) bounded oscillation + iid noise, (ii) random walk, (iii) leak.
Observable: per-orbit mean of the energy error (P = ticks per orbit).
Detector: two-sided CUSUM on orbit-to-orbit means, C+ = max(0, C+ + (m-k)),
C- = max(0, C- - (m-k)), alarm when max(C+, C-) > h.  On the plane m is an
integer orbit mean (one adder per kick), so the gate is integer and deterministic.

v1 (b12_cusum_v1.py, b12_v1-out.txt) differenced raw streams and is kept as the
record of the diagnosis: its "bounded" arms contained a random walk and CUSUM
correctly flagged them.
"""
import numpy as np

P = 1234          # ticks per orbit
NORB = 512        # orbits per stream
NSEED = 200

def stream(seed, A=1.0, sig=0.1, walk=0.0, leak=0.0, tail="n", pure_echo=False):
    rng = np.random.default_rng(seed)
    w = 2 * np.pi / P
    t = np.arange(P * NORB)
    e = A * np.sin(w * t + rng.uniform(0, 2 * np.pi))
    if not pure_echo:
        if tail == "t":
            e = e + sig * rng.standard_t(3, t.size)
        else:
            e = e + sig * rng.standard_normal(t.size)
    if walk:
        e = e + walk * np.cumsum(rng.standard_normal(t.size))
    if leak:
        e = e + leak * t / P          # leak is per-orbit
    m = e.reshape(NORB, P).mean(axis=1)          # per-orbit means
    return e, m

def cusum(m, k, h):
    Cp = Cm = 0.0; best = 0.0; alarm = NORB
    for j, x in enumerate(m):
        Cp = max(0.0, Cp + x - k)
        Cm = max(0.0, Cm - x - k)
        if max(Cp, Cm) > best: best = max(Cp, Cm)
        if max(Cp, Cm) > h and alarm == NORB: alarm = j
    return alarm, best

def expo(e):      # log-log slope of running max |e| over ticks
    t = np.arange(1, e.size + 1)
    rm = np.maximum.accumulate(np.abs(e))
    a, b = np.log(t), np.log(np.maximum(rm, 1e-12))
    n = e.size // 2
    return b[n:].mean() - b[:n].mean() and (b[n:].mean() - b[:n].mean()) / (a[n:].mean() - a[:n].mean())

def ratio(e):     # RMS last decile / first decile
    d = e.size // 10
    return e[-d:].std() / max(e[:d].std(), 1e-12)
ARMS = {  # name: (stream kwargs, class)  class: 'ok' must NOT alarm, 'bad' MUST alarm
    "c0_neg":  (dict(A=1.0),                       "ok"),
    "c1_pos":  (dict(A=1.0, leak=0.02),            "bad"),
    "P1_A2":   (dict(A=2.0),                       "ok"),
    "P1_A5":   (dict(A=5.0),                       "ok"),
    "P1_A20":  (dict(A=20.0),                      "ok"),
    "P2_c/2":  (dict(A=2.0, leak=0.01),            "bad"),
    "P2_c/4":  (dict(A=2.0, leak=0.005),           "bad"),
    "P3_walk": (dict(A=2.0, walk=0.005),           "bad"),
    "P4_t3":   (dict(A=2.0, tail="t"),             "ok"),
    "P4_echo": (dict(A=3.0, pure_echo=True),       "ok"),
}

# --- calibration (v3): h from the FULL acceptable-noise family {gauss, t3};
# --- threshold directions corrected (ratio/expo must exceed a value above the ok-family).
k = 0.01                                        # allowance: half the c1 leak
negfam = [stream(s, **ARMS["c0_neg"][0])[1] for s in range(30)] + \
         [stream(s, **ARMS["P4_t3"][0])[1] for s in range(30)]
h = 1.5 * max(cusum(m, k, np.inf)[1] for m in negfam)
pos = [stream(s, **ARMS["c1_pos"][0])[0] for s in range(30)]
neg0 = [stream(s, **ARMS["c0_neg"][0])[0] for s in range(30)] + \
       [stream(s, **ARMS["P4_t3"][0])[0] for s in range(30)]
r_lo = max(ratio(e) for e in pos)      # leak side must be ABOVE this to separate at all
r_hi = 1.2 * max(ratio(e) for e in neg0)
e_lo = max(expo(e) for e in pos)
e_hi = 1.2 * max(expo(e) for e in neg0)
thr_ratio = max(r_lo, r_hi)            # if no gap exists, unpassable by construction (r8 lesson)
thr_expo = max(e_lo, e_hi)
print(f"calibration v3: k={k} h={h:.4g} thr_ratio={thr_ratio:.3f} (pos max {r_lo:.3f} / ok max {r_hi:.3f}) thr_expo={thr_expo:.3f} (pos max {e_lo:.3f} / ok max {e_hi:.3f})")

print(f"{'arm':9s} {'class':5s} {'cusum':>12s} {'ratio':>12s} {'expo':>12s}  cusum_med_alarm")
tab = {}
for name, (cfg, cls) in ARMS.items():
    dc = dr = de = 0; alarms = []
    for s in range(NSEED):
        e, m = stream(s, **cfg)
        a, _ = cusum(m, k, h)
        if a < NORB: dc += 1; alarms.append(a)
        if ratio(e) > thr_ratio: dr += 1
        if expo(e) > thr_expo: de += 1
    med = int(np.median(alarms)) if alarms else -1
    tab[name] = (cls, dc, dr, de, med)
    print(f"{name:9s} {cls:5s} {dc:4d}/{NSEED}    {dr:4d}/{NSEED}    {de:4d}/{NSEED}   {med}")

print("\nverdicts vs predictions.md (v2):")
ok = lambda x: f"{100*x//NSEED}%"
for a in ["P1_A2", "P1_A5", "P1_A20"]:
    print(f"P1 {a}: cusum alarms {ok(tab[a][1])} (pred 0%), expo alarms {ok(tab[a][3])} (pred >=50% at A=20 only)")
d1 = tab["c1_pos"][4]; d2 = tab["P2_c/2"][4]; d4 = tab["P2_c/4"][4]
print(f"P2: cusum 100%? {ok(tab['P2_c/2'][1])}/{ok(tab['P2_c/4'][1])}; med alarm {d1}->{d2}->{d4} (linear in 1/c pred); ratio at c/4 {ok(tab['P2_c/4'][2])}")
print(f"P3 walk: cusum {ok(tab['P3_walk'][1])} (pred 100%), ratio {ok(tab['P3_walk'][2])} (pred ~0%), expo {ok(tab['P3_walk'][3])} (pred ~0%)")
print(f"P4: t3 false alarm {ok(tab['P4_t3'][1])} (pred <5%), echo false alarm {ok(tab['P4_echo'][1])} (pred ~0%)")
print(f"controls: pos cusum {ok(tab['c1_pos'][1])} (100 req), neg cusum {ok(tab['c0_neg'][1])} (0 req)")
