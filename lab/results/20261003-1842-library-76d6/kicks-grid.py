#!/usr/bin/env python3
"""lf2 with kicks on a palindromic E-uniform (pericenter-dense) grid vs
M-uniform grid, e=0.6. Drift = exact conic propagation in the window's own
osculating elements (e-vector carried, E advanced): zero new operators."""
import numpy as np

GM, R = 1.0, 0.05
J2 = 1e-3
e0, a = 0.6, 1.0
n = np.sqrt(GM / a**3)


def osc(s):
    x, y, u, v = s
    r = np.hypot(x, y)
    v2 = u * u + v * v
    ex = ((v2 - GM / r) * x - (x * u + y * v) * u) / GM
    ey = ((v2 - GM / r) * y - (x * u + y * v) * v) / GM
    ee = np.hypot(ex, ey)
    w = np.arctan2(ey, ex)
    # eccentric anomaly of current position (2pi-branch safe via atan2)
    xo = x * np.cos(w) + y * np.sin(w)
    yo = -x * np.sin(w) + y * np.cos(w)
    E = np.arctan2(yo / (a * np.sqrt(1 - ee * ee)),
                   (xo / a) + ee)
    return ee, w, E


def from_E(E, w, ee):
    xo = a * (np.cos(E) - ee)
    yo = a * np.sqrt(1 - ee * ee) * np.sin(E)
    fac = np.sqrt(GM / a) / (1 - ee * np.cos(E))
    vo_x = -fac * np.sin(E)
    vo_y = fac * np.sqrt(1 - ee * ee) * np.cos(E)
    cw, sw = np.cos(w), np.sin(w)
    return np.array([xo * cw - yo * sw, xo * sw + yo * cw,
                     vo_x * cw - vo_y * sw, vo_x * sw + vo_y * cw])


def elements(s):
    x, y, u, v = s
    r = np.hypot(x, y)
    v2 = u * u + v * v
    ex = ((v2 - GM / r) * x - (x * u + y * v) * u) / GM
    ey = ((v2 - GM / r) * y - (x * u + y * v) * v) / GM
    E = v2 / 2 - GM / r - 0.5 * GM * J2 * R * R / r**3
    return np.hypot(ex, ey), np.arctan2(ey, ex), E


def run(k, norb=200, grid="M"):
    s = np.array([1 - e0, 0.0, 0.0, np.sqrt(GM * (1 + e0) / (1 - e0))])
    _, _, E0 = elements(s)
    Em, evec, Emax = [], [], 0.0
    per = max(1, k // 8)
    step = 0
    edgesM = None
    for orb in range(norb):
        # window edges are phase offsets on the CURRENT osculating conic
        for i in range(k):
            ee, w, Ecur = osc(s)
            if grid == "E":
                de = 2 * np.pi / k
                Ea, Eb = Ecur, Ecur + de
            else:
                dm = 2 * np.pi / k
                Ma = Ecur - ee * np.sin(Ecur)
                Ea = Ecur
                Mb = Ma + dm
                Eb = Mb + ee * np.sin(Mb)  # Newton-lite, good enough (ee<=0.6)
                for _ in range(6):
                    Eb = Eb - (Eb - ee * np.sin(Eb) - Mb) / (1 - ee * np.cos(Eb))
            dt = ((Eb - ee * np.sin(Eb)) - (Ea - ee * np.sin(Ea))) / n
            # edge-kick scheme: at each edge apply a*dt/2 (half of each
            # adjacent window): symmetric, one force evaluation per window.
            sa = from_E(Ea, w, ee)
            x, y = sa[0], sa[1]
            r2, r = x * x + y * y, np.hypot(x, y)
            ar = -(3 / 2) * GM * J2 * R * R / r2**2
            sa = sa + (dt / 2) * np.array([0.0, 0.0, ar * x / r, ar * y / r])
            ee2, w2, Ea2 = osc(sa)          # new conic after the kick
            s = from_E(Eb, w2, ee2)         # exact Kepler drift to window end
            if step % per == 0:
                e, wi, En = elements(s)
                Em.append(wi)
                evec.append(e)
                Emax = max(Emax, abs(En - E0))
            step += 1
    wis = np.unwrap(np.array(Em))
    ts = np.arange(len(wis)) * per / k
    A = np.vstack([ts, np.ones_like(ts)]).T
    slope = np.linalg.lstsq(A, wis, rcond=None)[0][0]
    dth = 3 * np.pi * J2 * (R / (1 - e0 * e0))**2
    return dict(k=k, rel=abs(slope / dth - 1), de=abs(evec[-1] - evec[0]),
                dE=Emax)


print("e=0.6, J2=1e-3, 200 orbits; band rel<=1%, de<=1e-4")
for grid in ["M", "E"]:
    for k in [8, 12, 16, 24, 32]:
        r = run(k, grid=grid)
        ok = r["rel"] <= 1e-2 and r["de"] <= 1e-4
        print(f" grid-{grid} k={k:3d} {'PASS' if ok else 'fail'} "
              f"rel={r['rel']:.3f} de={r['de']:.1e} dE={r['dE']:.0e}")
