import numpy as np, sys
sys.path.insert(0, ".")
from replica import *

rng = np.random.default_rng(7)
# 1) drift round trip + invariants, elliptic and hyperbolic
for e, gm in [(0.05, 3.8e-6), (0.3, 3.8e-6), (1.3, 2 ** -10), (0.0, 1.0)]:
    a = 2.7e5
    st = state_from_elements(gm, a, e, 0.3, 1.1)
    for dt in [1e3, 2e5, 8.7e6]:
        st2 = kepler_drift(st, dt, gm)
        r = np.hypot(st[0], st[1])
        E0 = 0.5 * (st[2] ** 2 + st[3] ** 2) - gm / r
        r2 = np.hypot(st2[0], st2[1])
        E1 = 0.5 * (st2[2] ** 2 + st2[3] ** 2) - gm / r2
        h0 = st[0] * st[3] - st[1] * st[2]
        h1 = st2[0] * st2[3] - st2[1] * st2[2]
        back = kepler_drift(st2, -dt, gm)
        rt = np.max(np.abs(back - st) / np.maximum(np.abs(st), 1))
        print(f"e={e} dt={dt:.1e}: dE/E={abs(E1-E0)/abs(E0):.2e} dh/h={abs(h1-h0)/abs(h0):.2e} roundtrip={rt:.2e}")

# 2) saba sequences sum
for n in (2, 3, 4):
    seq = saba_sequence(n)
    ks = sum(c for op, c in seq if op == "K")
    ds = sum(c for op, c in seq if op == "D")
    print(f"saba{n}: kicks={sum(1 for op,c in seq if op=='K')} sumK={ks:.12f} sumD={ds:.12f}")

# 3) a moon around Home with star tide: dkd at two resolutions converges
GM_S, GM_H = 1.0, 2.0 ** -18
aH, eH, varpiH, M0H = 9.93e7 / (1 - 0.02), 0.02, np.pi, 0.2 * TWOPI
nH = np.sqrt(GM_S / aH ** 3)
PH = TWOPI / nH
am, em = 2.6e5 / (1 - 0.05), 0.05
Pm = TWOPI * np.sqrt(am ** 3 / GM_H)

def moon_accel(st, t):
    M = M0H + nH * t
    xp, _ = ellipse_xv(aH, eH, varpiH, np.array([M]))
    xp = np.asarray(xp)[0]          # Home position (2,)
    xabs = st[:, :2] + xp[None, :]
    r = np.linalg.norm(xabs, axis=1)
    return -GM_S * xabs / r[:, None] ** 3 + GM_S * xp / np.linalg.norm(xp) ** 3

st0 = state_from_elements(GM_H, am, em, 0.0625 * TWOPI, 0.4375 * TWOPI)[None]
for k in (6, 9):
    it = Integrator("dkd", [GM_H], moon_accel)
    tr = it.run(st0.copy(), 12 * 2 ** k, Pm / 2 ** k, 2 ** k)
    x, y = tr[-1, 0, 0], tr[-1, 0, 1]
    print(f"dkd k={k}: final=({x:.10e},{y:.10e}) nkicks={it.nkick}")
