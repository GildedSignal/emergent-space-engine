"""Validation: drift exactness + classical solar-quadrupole apsidal precession."""
import numpy as np
import cad
from cad import TWOPI, elements, drift, Doll, run, fit_rate

rng = np.random.default_rng(7)
# --- drift round trip / energy conservation at e=0.3 and e=0.9 ---
gm = 1e-3
for e0 in (0.01, 0.3, 0.9, 0.99):
    a0 = 0.02
    w0 = 0.7
    M0 = 1.1
    E = cad.kepler_E(np.array([M0]), np.array([e0]))[0]
    x = np.array([a0 * (np.cos(E) - e0)]); y = np.array([a0 * np.sqrt(1 - e0 ** 2) * np.sin(E)])
    n = np.sqrt(gm / a0 ** 3)
    vx = np.array([-a0 * n * np.sin(E)]); vy = np.array([a0 * np.sqrt(1 - e0 ** 2) * n * np.cos(E)])
    x0, v0 = x.copy(), vx.copy()
    for _ in range(1000):
        x, y, vx, vy = drift(x, y, vx, vy, gm, 0.037)
    r0 = np.hypot(x0[0], y[0] if False else 0)
    # energy before/after
    _, e_after, _, _ = elements(x, y, vx, vy, gm)
    print(f"e0={e0}: e_after={e_after[0]:.15f}  (round trip dE/E ~ {(e_after[0]-e0)/max(e0,1e-9):.2e})")

# hyperbolic drift check
a0 = -0.05; e0 = 1.4; w0 = 0.3
Hh = 0.5
x = np.array([a0 * (e0 - np.cosh(Hh))]); y = np.array([a0 * np.sqrt(e0 ** 2 - 1) * np.sinh(Hh)])
n = np.sqrt(gm / 0.05 ** 3)
vx = np.array([-a0 * n * np.sinh(Hh) / (e0 * np.cosh(Hh) - 1)]); vy = np.array([a0 * np.sqrt(e0 ** 2 - 1) * n * np.cosh(Hh) / (e0 * np.cosh(Hh) - 1)])
for _ in range(500):
    x, y, vx, vy = drift(x, y, vx, vy, gm, 0.02)
_, e_after, _, _ = elements(x, y, vx, vy, gm)
print(f"hyp e0={e0}: e_after={e_after[0]:.15f}")

# --- classical apsidal precession: wdot = (3/4) n * tau, tau=(M/m_p)(a/D)^3 ---
mu = 1e-3          # planet mass fraction
D = 1.0
n2 = 1.0           # sun's mean motion (GM_tot=1)
GM_p = mu; GM_s = 1.0 - mu
sun = dict(gm=GM_s, D=D, n=n2, ph=0.0)
doll = Doll(GM_p, [sun])
RH = (mu / 3) ** (1 / 3)
for f in (0.1, 0.2, 0.3):
    a0 = f * RH
    n = np.sqrt(GM_p / a0 ** 3)
    e0 = 0.05
    ph = rng.uniform(0, TWOPI, 8)
    x = a0 * np.cos(ph); y = a0 * np.sin(ph)
    vx = -a0 * n * np.sin(ph); vy = a0 * n * np.cos(ph)
    s0 = dict(x=x * (1 - 0.0), y=y, vx=vx, vy=vy)  # circular birth
    T = 30 * TWOPI
    out, fin = run(doll, s0, T, 512, sample=np.arange(2, T, 2 * TWOPI / n))
    wd = fit_rate(out["t"], out["w"])
    tau = (GM_s / GM_p) * (a0 / D) ** 3
    wdot_cl = 0.75 * n * tau
    print(f"f={f}: wdot/n2  measured={np.median(wd):+.5f} classical={wdot_cl:+.5f} ratio={np.median(wd)/wdot_cl:.3f}  tau={tau:.4f}")
