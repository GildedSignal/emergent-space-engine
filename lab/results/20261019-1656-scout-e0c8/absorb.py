#!/usr/bin/env python3
"""Falsifier: does the compact belt row absorb the shipped cadence's clock-kick in place?

Float64 first-order replica on the shipped record's constants:
  - belt per shipmem's birth law (belt.rs): p uniform in [2.0, 2.5) (the [2048,2560) band),
    e Rayleigh(sigma=0.07) redrawn above 0.4, uniform angles; planar.
  - perturber per scenario.rs `restricted`: mu = 1/999 of the total, circular, two arms
    (inside the belt at sep=1.0, outside at sep=4.0), one shared phase.
  - one doll step dt = 27.4k game-s = 8.68e-4 yr (0659's measured wave spacing 14.3k/41.7k/69k gs).
  - grids per belt.rs: p 25-bit over the band, e 32-bit, omega 32-bit, t_p 44-bit over the period.
Departure bits per column = Rice-coded |quanta| residuals (codec.rs's uv-length measure),
before/after one step, on held-out members, with (a) the shipped codec's predictor class
(one shared slope: DFOR/CHORD shape), (b) a shared 10-coefficient variation-of-parameters
harmonic predictor (POST-HOC arm, disclosed), and (c) a scrambled-magnitude control.
Units: AU, yr, GM_star = 4*pi^2. Orders of magnitude (floats explore; integers decide).
"""
import numpy as np

GM = 4 * np.pi ** 2
MU = 1.0 / 999.0
DT = 27_400.0 / 31_557_600.0  # 27.4k game-s (SI s) -> yr
N = 4096
SEED = 20261019


def draw_belt(n, rng):
    a = 2.0 + 0.5 * rng.random(n)
    e = np.empty(n)
    keep = np.zeros(n, bool)
    while not keep.all():
        e[~keep] = rng.rayleigh(0.07, (~keep).sum())
        keep = e <= 0.4
    om = rng.uniform(0, 2 * np.pi, n)
    tp = rng.uniform(0.0, 1.0, n)
    return a, e, om, tp


def state(a, e, om, tp, t):
    n = np.sqrt(GM / a ** 3)
    P = 2 * np.pi / n
    M = ((t - tp * P) * n) % (2 * np.pi)
    E = M.copy()
    for _ in range(80):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    x = a * (np.cos(E) - e)
    y = a * np.sqrt(1 - e * e) * np.sin(E)
    edot = n / (1 - e * np.cos(E))
    vx = -a * np.sin(E) * edot
    vy = a * np.sqrt(1 - e * e) * np.cos(E) * edot
    c, s = np.cos(om), np.sin(om)
    return x * c - y * s, x * s + y * c, vx * c - vy * s, vx * s + vy * c


def elements(x, y, vx, vy, t):
    r = np.hypot(x, y)
    v2 = vx * vx + vy * vy
    a = 1.0 / (2.0 / r - v2 / GM)
    rv = x * vx + y * vy
    ex = ((v2 - GM / r) * x - rv * vx) / GM
    ey = ((v2 - GM / r) * y - rv * vy) / GM
    e = np.hypot(ex, ey)
    om = np.arctan2(ey, ex) % (2 * np.pi)
    n = np.sqrt(GM / a ** 3)
    P = 2 * np.pi / n
    E = np.arccos(np.clip((1 - r / a) / (e + 1e-300), -1, 1))
    E = np.where((x * ex + y * ey) < 0, -E, E)
    M = (E - e * np.sin(E)) % (2 * np.pi)
    tp = ((t - M / n) / P) % 1.0
    return a, e, om, tp


def accel(x, y, xp, yp):
    r3 = (x * x + y * y) ** 1.5
    dx, dy = x - xp, y - yp
    d3 = (dx * dx + dy * dy) ** 1.5
    rp3 = (xp * xp + yp * yp) ** 1.5
    ax = -GM * x / r3 - MU * GM * (dx / d3 + xp / rp3)
    ay = -GM * y / r3 - MU * GM * (dy / d3 + yp / rp3)
    return ax, ay


def fly(a, e, om, tp, sep, dt, k):
    x, y, vx, vy = state(a, e, om, tp, 0.0)
    n_p = np.sqrt(GM / sep ** 3)
    h = dt / k
    for i in range(k):
        t = (i + 0.5) * h
        xp, yp = sep * np.cos(n_p * t), sep * np.sin(n_p * t)
        ax, ay = accel(x, y, xp, yp)
        vx, vy = vx + ax * h / 2, vy + ay * h / 2
        x, y = x + vx * h, y + vy * h
        t = (i + 1) * h
        xp, yp = sep * np.cos(n_p * t), sep * np.sin(n_p * t)
        ax, ay = accel(x, y, xp, yp)
        vx, vy = vx + ax * h / 2, vy + ay * h / 2
    return x, y, vx, vy


def rice_bits(q):
    """codec.rs's uv-length stand-in: Rice code of |q| (+ sign) at the best width."""
    q = np.abs(q.astype(np.int64))
    best = None
    for w in range(0, 24):
        s = ((q >> w) + w + 1.5).sum()
        if best is None or s < best[0]:
            best = (s, w)
    return best[0], best[1]


def entropy(delta_quanta, keys, held):
    raw, _ = rice_bits(delta_quanta[held])
    raw /= held.sum()
    trn = ~held
    best_fit = raw
    for key in keys:
        A = np.c_[np.ones(trn.sum()), key[trn]]
        coef, *_ = np.linalg.lstsq(A, delta_quanta[trn], rcond=None)
        r = delta_quanta - np.c_[np.ones(len(key)), key] @ coef
        b, _ = rice_bits(r[held])
        best_fit = min(best_fit, b / held.sum())
    return raw, best_fit


def basis(a0, e0, om0, r0, sep):
    """Shared tide predictor (post-hoc arm, disclosed): the classical variation-of-
    parameters harmonic shape. 10 shared coefficients per column per step, block-wide."""
    lam_p = np.sqrt(GM / sep ** 3) * DT
    cosv = np.clip((a0 * (1 - e0 * e0) / r0 - 1) / (e0 + 1e-300), -1, 1)
    d = om0 + np.arccos(cosv) - lam_p
    g = 2.0 / a0
    return np.column_stack([
        g, g * np.sin(d), g * np.cos(d), g * np.sin(2 * d), g * np.cos(2 * d),
        g * np.sin(d) * e0, g * np.cos(d) * e0, g * e0, g * e0 * np.sin(2 * om0),
        np.ones_like(g),
    ])


def arm(name, sep):
    rng = np.random.default_rng(SEED)
    a, e, om, tp = draw_belt(N, rng)
    x0, y0, vx0, vy0 = state(a, e, om, tp, 0.0)
    a0, e0, om0, tp0 = elements(x0, y0, vx0, vy0, 0.0)
    rt = np.abs(a0 - a).max() / a.max()
    x, y, vx, vy = fly(a, e, om, tp, sep, DT, 256)
    a1, e1, om1, tp1 = elements(x, y, vx, vy, DT)
    xh, yh, vxh, vyh = fly(a, e, om, tp, sep, DT, 512)
    a2, _, _, _ = elements(xh, yh, vxh, vyh, DT)
    conv = np.median(np.abs(a1 - a2)) / np.median(np.abs(a1 - a0))

    P0 = 2 * np.pi / np.sqrt(GM / a0 ** 3)
    r0 = np.hypot(x0, y0)
    qp = 0.5 / 2 ** 25
    qe = 0.5 / 2 ** 32
    qom = 2 * np.pi / 2 ** 32
    qtp = P0 / 2 ** 44
    dom = (om1 - om0 + np.pi) % (2 * np.pi) - np.pi
    cols = {
        "p": ((a1 - a0) / qp, a0),
        "e": ((e1 - e0) / qe, e0),
        "omega": (dom / qom, om0),
        "t_p": (((tp1 - tp0 + 0.5) % 1.0 - 0.5) * P0 / qtp, tp0),
    }
    held = np.zeros(N, bool)
    held[N // 2:] = True
    print(f"\n== arm {name} (sep={sep}, mu=1/999, dt={DT:.3e} yr) ==")
    print(f"round-trip control: max|da|/a = {rt:.2e}   step-halving: median shift = {conv:.4f}")
    tot_raw = tot_fit = tot_harm = 0.0
    B = basis(a0, e0, om0, r0, sep)
    for cname, (dq, _key) in cols.items():
        raw, fit = entropy(dq, [a0, e0, om0, tp * P0], held)
        coef, *_ = np.linalg.lstsq(B[~held], dq[~held], rcond=None)
        hb, _ = rice_bits((dq - B @ coef)[held])
        harm = hb / held.sum()
        tot_raw += raw
        tot_fit += fit
        tot_harm += harm
        print(f"  {cname:5s} |delta| p50 = {np.median(np.abs(dq)):11.3e} quanta"
              f"   bits/body raw {raw:7.2f}  one-slope {fit:7.2f}  VoP-harm {harm:7.2f}")
    rng2 = np.random.default_rng(7)
    perm = rng2.permutation(N)
    scr = 0.0
    for cname, (dq, _k) in cols.items():
        b, _ = rice_bits(dq[perm][held])
        scr += b / held.sum()
    n = np.sqrt(GM / a0 ** 3)
    n_p = np.sqrt(GM / sep ** 3)
    best = None
    for J in range(2, 10):
        for K in range(1, J):
            if np.gcd(J, K) != 1 or J / K > 4.5:
                continue
            d = np.abs(n / n_p - K / J)
            best = d if best is None else np.minimum(best, d)
    print(f"  TOTAL bits/body: raw {tot_raw:.2f}  one-slope {tot_fit:.2f}"
          f"  VoP-harm {tot_harm:.2f}  scrambled {scr:.2f}")
    for w in (0.001, 0.005, 0.02):
        print(f"  resonance census: {(best < w).mean()*100:6.2f}% within |dn/n_p| {w} of a J:K (J<=9)")
    return tot_raw, tot_fit, tot_harm, scr


def mu0_control():
    """Negative control: with mu = 0 the flight is pure Kepler; the departure must be 0."""
    global MU
    rng = np.random.default_rng(SEED)
    a, e, om, tp = draw_belt(1024, rng)
    x0, y0, vx0, vy0 = state(a, e, om, tp, 0.0)
    a0, e0, om0, _tp0 = elements(x0, y0, vx0, vy0, 0.0)
    saved = MU
    MU = 0.0
    x, y, vx, vy = fly(a, e, om, tp, 1.0, DT, 256)
    MU = saved
    a1, e1, om1, _tp1 = elements(x, y, vx, vy, DT)
    dom = (om1 - om0 + np.pi) % (2 * np.pi) - np.pi
    print("mu=0 control: max|da| = %.2e AU  max|de| = %.2e  max|dom| = %.2e rad"
          % (np.abs(a1 - a0).max(), np.abs(e1 - e0).max(), np.abs(dom).max()))


if __name__ == "__main__":
    print("clock-kick absorbability falsifier (shipmem grids, one doll step)")
    mu0_control()
    for name, sep in (("inside", 1.0), ("outside", 4.0)):
        arm(name, sep)
