#!/usr/bin/env python3
"""Kicks per orbit at the same behaviour: lf2 vs Forest-Ruth y4 vs Yoshida y6.

Wisdom-Holman style: exact Kepler drift + J2 impulse kicks, uniform step.
Equatorial orbit -> pure apsidal precession, analytic oracle
  Delta-wpi/orbit = 3*pi*J2*(R/p)^2,  p = a(1-e^2)
(epicyclic: kappa^2 = d2Phi/dr2 + 3Phi'/r with Phi = -GM/r - GM*J2*R^2/(2 r^3);
 Binet/GR-analog: r^-3 correction beta gives 6*pi*beta/p^2, beta = J2 R^2/2.)
Positive control: y6 at 896 kicks/orbit matches oracle to 0.2%.
Negative control: lf2 at 4 kicks/orbit fails the 1% band.
PASS: |rel precession error| <= 1% and |de| <= 1e-4 over 200 orbits.
"""
import numpy as np

GM = 1.0
R = 0.05
J2_CUR = [1e-3]


def kepler_drift(s, dt):
    x, y, u, v = s
    r = np.hypot(x, y)
    v2 = u * u + v * v
    E = v2 / 2 - GM / r
    a = -GM / (2 * E)
    ex = ((v2 - GM / r) * x - (x * u + y * v) * u) / GM
    ey = ((v2 - GM / r) * y - (x * u + y * v) * v) / GM
    e = np.hypot(ex, ey)
    n = np.sqrt(GM / a**3)
    cE = (1 - r / a) / e if e > 1e-12 else 0.0
    sE = (x * u + y * v) / (e * np.sqrt(GM * a)) if e > 1e-12 else 0.0
    Ean = np.arctan2(sE, cE)
    M0 = Ean - e * np.sin(Ean)
    M1 = M0 + n * dt
    Ean1 = M1 + e * np.sin(M1)
    for _ in range(60):
        f = Ean1 - e * np.sin(Ean1) - M1
        fp = 1 - e * np.cos(Ean1)
        d = f / fp
        Ean1 -= d
        if abs(d) < 1e-16:
            break
    w = np.arctan2(ey, ex)
    xo = a * (np.cos(Ean1) - e)
    yo = a * np.sqrt(1 - e * e) * np.sin(Ean1)
    fac = np.sqrt(GM / a) / (1 - e * np.cos(Ean1))
    vo_x = -fac * np.sin(Ean1)
    vo_y = fac * np.sqrt(1 - e * e) * np.cos(Ean1)
    cw, sw = np.cos(w), np.sin(w)
    return np.array([xo * cw - yo * sw, xo * sw + yo * cw,
                     vo_x * cw - vo_y * sw, vo_x * sw + vo_y * cw])


def kick(s, h, J2):
    x, y, u, v = s
    r2 = x * x + y * y
    r = np.sqrt(r2)
    ar = -(3 / 2) * GM * J2 * R * R / r2**2
    return s + h * np.array([0.0, 0.0, ar * x / r, ar * y / r])


def s2(s, h, J2, cost):
    cost[0] += 1
    s = kepler_drift(s, h / 2)
    s = kick(s, h, J2)
    return kepler_drift(s, h / 2)


X13 = 2 ** (1.0 / 3.0)
W1 = 1.0 / (2 - X13)
W2 = -X13 / (2 - X13)
Y6 = np.array([0.784513610477560, 0.235573213359357, -1.17767998417887,
               1.31518632068391, -1.17767998417887, 0.235573213359357,
               0.784513610477560])


def lf2(s, h, J2, cost):
    return s2(s, h, J2, cost)          # 1 kick


def y4(s, h, J2, cost):
    s = s2(s, W1 * h, J2, cost)
    s = s2(s, W2 * h, J2, cost)
    return s2(s, W1 * h, J2, cost)     # 3 kicks


def y6(s, h, J2, cost):
    for w in Y6:
        s = s2(s, w * h, J2, cost)
    return s                            # 7 kicks


def elements(s):
    x, y, u, v = s
    r = np.hypot(x, y)
    v2 = u * u + v * v
    ex = ((v2 - GM / r) * x - (x * u + y * v) * u) / GM
    ey = ((v2 - GM / r) * y - (x * u + y * v) * v) / GM
    E = v2 / 2 - GM / r - 0.5 * GM * J2_CUR[0] * R * R / r**3
    return np.hypot(ex, ey), np.arctan2(ey, ex), E


def run(method, k, norb, e0, J2, mulfac):
    J2_CUR[0] = J2
    h = 2 * np.pi / k
    s = np.array([1 - e0, 0.0, 0.0, np.sqrt(GM * (1 + e0) / (1 - e0))])
    cost = [0]
    per = max(1, k // 8)
    wis, es, Emax = [], [], 0.0
    _, _, E0 = elements(s)
    for it in range(norb * k):
        s = method(s, h, J2, cost)
        if it % per == 0:
            e, wi, E = elements(s)
            wis.append(wi)
            es.append(e)
            Emax = max(Emax, abs(E - E0))
    wis = np.unwrap(np.array(wis))
    ts = np.arange(len(wis)) * per / k
    A = np.vstack([ts, np.ones_like(ts)]).T
    slope = np.linalg.lstsq(A, wis, rcond=None)[0][0]
    dth = 3 * np.pi * J2 * (R / (1 - e0 * e0))**2
    return dict(kicks=cost[0] / norb, rel=abs(slope / dth - 1),
                de=abs(es[-1] - es[0]), Emax=Emax)


def probe(method, k, e0, J2):
    return run(method, k, 200, e0, J2, 1)


if __name__ == "__main__":
    print("oracle: d_wpi/orbit = 3*pi*J2*(R/p)^2; band: rel<=1%, |de|<=1e-4, 200 orbits")
    ctrl = probe(y6, 128, 0.1, 1e-3)   # 896 kicks/orbit
    print(f"positive control y6 k=128 (896 kicks/orbit): rel err = {ctrl['rel']:.4f}")
    ctrl2 = probe(lf2, 4, 0.1, 1e-3)
    print(f"negative control lf2 k=4  (4 kicks/orbit):   rel err = {ctrl2['rel']:.4f} (must fail)")
    GRIDS = {"lf2": ([8, 12, 16, 24, 32, 48, 64, 96, 128], 1),
             "y4":  ([3, 4, 6, 8, 12, 16, 24, 32, 42], 3),
             "y6":  ([2, 3, 4, 6, 8, 12, 16, 24, 36], 7)}
    FUN = {"lf2": lf2, "y4": y4, "y6": y6}
    for name, e0, J2 in [("base e=0.1 J2=1e-3", 0.1, 1e-3),
                         ("held-out e=0.6 J2=1e-3", 0.6, 1e-3),
                         ("held-out e=0.1 J2=1e-2", 0.1, 1e-2)]:
        print(f"\n== {name}: min kicks/orbit in band (per method)")
        for m, (ks, mul) in GRIDS.items():
            best = None
            for k in ks:
                r = probe(FUN[m], k, e0, J2)
                ok = r["rel"] <= 1e-2 and r["de"] <= 1e-4
                if ok and best is None:
                    best = r
                print(f"   {m} outer_k={k:3d} kicks/orbit={mul*k:3d} "
                      f"{'PASS' if ok else 'fail'} rel={r['rel']:.3f} "
                      f"de={r['de']:.1e} dE={r['Emax']:.0e}")
            print(f"  -> {m}: pass-band = "
                  f"{best['kicks'] if best else None} kicks/orbit")
