import numpy as np, sys, json
sys.path.insert(0, ".")
from replica import *

GM_S, GM_H = 1.0, 2.0 ** -18
aH, eH, varpiH, M0H = 9.93e7 / (1 - 0.02), 0.02, np.pi, 0.2 * TWOPI
nH = np.sqrt(GM_S / aH ** 3)
PH = TWOPI / nH
RH = aH * (GM_H / 3.0) ** (1.0 / 3.0)

def moon_accel(st, t):
    xp, _ = ellipse_xv(aH, eH, varpiH, np.array([M0H + nH * t]))
    xp = np.asarray(xp)[0]
    xabs = st[:, :2] + xp[None, :]
    r = np.linalg.norm(xabs, axis=1)
    return -GM_S * xabs / r[:, None] ** 3 + GM_S * xp / np.linalg.norm(xp) ** 3

heldout = "--heldout" in sys.argv
e0 = 0.3 if heldout else 0.05
fracs = [0.25, 0.4, 0.6, 0.8]
am = np.array([f * RH for f in fracs])
Pm0 = TWOPI * np.sqrt(am ** 3 / GM_H)
Norb = 50
schemes = ["dkd", "saba2", "saba3", "whc3", "whc3b"]
ks = [1, 2, 3, 4, 5, 6, 7]

def run_one(scheme, k, m):
    st0 = state_from_elements(GM_H, am[m], e0, TWOPI / 16, 0.4375 * TWOPI)[None]
    tau = Pm0[m] / 2 ** k
    it = Integrator(scheme, [GM_H], moon_accel)
    tr = it.run(st0, Norb * 2 ** k, tau, 2 ** k)     # sample each moon orbit
    a, e, vp, _ = elements(tr[:, 0, 0], tr[:, 0, 1], tr[:, 0, 2], tr[:, 0, 3], GM_H)
    S = len(a); sl = slice(S // 2, S)
    uu = np.unwrap(vp)
    rate = np.polyfit(np.arange(S)[sl], uu[sl], 1)[0] * Pm0[m] / PH  # rad per Home orbit
    return dict(rate=float(rate), emax=float(np.nanmax(e[2:])),
                esc=bool(e[-1] >= 1.0 or a[-1] > 3 * a[0])), tr

