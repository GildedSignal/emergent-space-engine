#!/usr/bin/env python3
"""Rung r4 v2: arc-integrated kicks (Gauss-Picard, first order) vs dense truth.

Problem (restricted, planar): star m0=1 (G=1), outer perturber m2=3e-3 on a fixed
Kepler orbit (mu2 = 1+m2), massless inner body tracked by its heliocentric elements.
Perturbing acceleration on the inner (direct + indirect, heliocentric):
    a_p = m2 * [ (r2-r1)/|r2-r1|^3 - r2/|r2|^3 ]
Kepler part of the inner: -mu1 * r1/r1^3 with mu1 = G*(m0+m1) = 1.

The law: within a window (between conjunctions of the mean longitudes; or
conjunction+opposition for -half; or one inner orbit for `averaged`) the inner
orbit is held fixed. At the window end the kick is applied as the impulse pair
(first Picard iterate of the perturbed trajectory — "Gauss-Picard, first order"):
    dv = integral a_p dt,   dr = integral (t1 - t) a_p dt     (Gauss quadrature)
and the new osculating elements come from (r_arc + dr, v_arc + dv) at t1. No
dynamics is integrated inside the law; the kick and the arc are exact Kepler.

Subcommands: check | scan | run | quad
"""

import json, math, os, sys
from math import sin, cos, sqrt, hypot, atan2, pi, fmod

TWOPI = 2.0 * pi
OUT = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------- Kepler ---
def solve_E(M, e):
    """Newton solve of E - e sinE = M, wrapped; ~1e-15."""
    M = fmod(M + pi, TWOPI)
    if M < 0.0:
        M += TWOPI
    M -= pi
    E = M if e < 0.8 else pi
    for _ in range(80):
        f = E - e * sin(E) - M
        d = f / (1.0 - e * cos(E))
        E -= d
        if abs(d) < 1e-15:
            break
    return E


def elem_to_state(a, e, varpi, lam, mu):
    """Heliocentric position/velocity on the Kepler orbit at mean longitude lam."""
    M = lam - varpi
    E = solve_E(M, e)
    cE, sE = cos(E), sin(E)
    b = a * sqrt(1.0 - e * e)
    r = a - a * e * cE
    n = sqrt(mu / (a * a * a))
    Edot = n * a / r
    xw, yw = a * (cE - e), b * sE
    vxw, vyw = -a * sE * Edot, b * cE * Edot
    cw, sw = cos(varpi), sin(varpi)
    return (cw * xw - sw * yw, sw * xw + cw * yw,
            cw * vxw - sw * vyw, sw * vxw + cw * vyw)


def state_to_elem(x, y, vx, vy, mu):
    """Osculating (a, e, varpi, lam); inverse of elem_to_state."""
    r = hypot(x, y)
    v2 = vx * vx + vy * vy
    a = -mu / (v2 - 2.0 * mu / r)
    rv = x * vx + y * vy
    ex = (v2 - mu / r) * x / mu - rv * vx / mu
    ey = (v2 - mu / r) * y / mu - rv * vy / mu
    e = hypot(ex, ey)
    varpi = atan2(ey, ex)
    # eccentric anomaly from state (works for e -> 0 via atan2 guards)
    if a <= 0.0 or e >= 1.0:      # hyperbolic/ejecting: flag, no anomaly defined
        return a, e, varpi, float("nan")
    cE = (1.0 - r / a)
    sE = rv / sqrt(mu * a)
    E = atan2(sE * e, cE * e) if e > 1e-12 else atan2(sE, cE)  # same angle either way
    M = E - e * sin(E)
    return a, e, varpi, varpi + M


def outer_pos(a2, e2, varpi2, M2):
    E = solve_E(M2, e2)
    cE, sE = cos(E), sin(E)
    b = a2 * sqrt(1.0 - e2 * e2)
    xw, yw = a2 * (cE - e2), b * sE
    cw, sw = cos(varpi2), sin(varpi2)
    return cw * xw - sw * yw, sw * xw + cw * yw


def pert_a(x, y, r2x, r2y, m2):
    """Full perturbing acceleration on the inner body (direct + indirect),
    heliocentric: a_p = m2 [ (r2-r1)/|r2-r1|^3 - r2/|r2|^3 ]."""
    dx = r2x - x
    dy = r2y - y
    d2 = dx * dx + dy * dy
    d3 = d2 * sqrt(d2)
    r2n = hypot(r2x, r2y)
    r23 = r2n * r2n * r2n
    return m2 * (dx / d3 - r2x / r23), m2 * (dy / d3 - r2y / r23)

def vop_rates(x, y, vx, vy, apx, apy, a, lam0):
    """Variation-of-parameters rates (da, dex, dey, dlam) at an arc state,
    for the perturbing acceleration (apx, apy). mu1 = 1.

    da and de~ use the vector Gauss identities, verified against direct
    integration to ~1e-3 relative. dlam is the exact velocity sensitivity
    d(elem)/dv . a_p (the definition of the first-order VOP rate), differenced
    numerically with a wrapped step of 1e-7 (relative error ~1e-6)."""
    adot = 2.0 * a * a * (vx * apx + vy * apy)
    h = x * vy - y * vx
    hd = x * apy - y * apx
    exd = h * apy + hd * vy
    eyd = -h * apx - hd * vx
    d = 1e-7
    lam1_ = state_to_elem(x, y, vx + d * apx, vy + d * apy, 1.0)[3]
    dlam = ((lam1_ - lam0 + pi) % TWOPI - pi) / d
    return adot, exd, eyd, dlam


def leggauss(n):
    """Gauss-Legendre nodes/weights on [-1,1], computed (no scipy)."""
    k = np.arange(1, n + 1)
    x = np.cos(pi * (k - 0.25) / (n + 0.5))
    for _ in range(200):
        p0 = np.ones_like(x)
        p1 = x.copy()
        for m in range(2, n + 1):
            p0, p1 = p1, ((2 * m - 1) * x * p1 - (m - 1) * p0) / m
        dp = n * (x * p1 - p0) / (x * x - 1.0)
        dx_ = p1 / dp
        x = x - dx_
        if np.max(np.abs(dx_)) < 1e-15:
            break
    w = 2.0 / ((1.0 - x * x) * dp * dp)
    return x, w


import numpy as np  # noqa: E402  (kept close to its only real use)

GL = {n: leggauss(n) for n in (8, 16, 32, 64)}


# ----------------------------------------------------------------- cases ---
M2 = 3e-3            # perturber mass ratio (rung)
MU2 = 1.0 + M2       # GM of the star+perturber pair (inner is massless)


def make_case(name, ratio, e1, varpi1, lam1, e2, varpi2, lam2, nsyn=200):
    a2 = (MU2 * ratio * ratio) ** (1.0 / 3.0)   # n2 = n1/ratio exactly (n1 = 1)
    n2 = 1.0 / ratio
    T = nsyn * TWOPI / (1.0 - n2)              # 200 synodic periods
    return dict(name=name, ratio=ratio, m2=M2, mu2=MU2, a2=a2, e2=e2,
                varpi2=varpi2, lam2_0=lam2, n2=n2, T=T,
                a1=1.0, e1=e1, varpi1=varpi1, lam1=0.0 + lam1)


def default_cases():
    """Frozen 29 Sep 2026 before predictions.md (IC scan: baseline resonant only).
    ResA circular perturber; ResB the phase-shifted case (w2 = 4.0, e2 = 0.05);
    controls same family at ratios 5.0 / 2.55 / 2.15 (e2 = 0.05)."""
    mk = lambda n, r, e2, w2: make_case(n, r, e1=0.08, varpi1=0.0, lam1=1.0,
                                        e2=e2, varpi2=w2, lam2=0.5)
    return [mk("res-2-1", 2.0, 0.0, 0.0),
            mk("res-2-1-w2-4", 2.0, 0.05, 4.0),
            mk("ctl-5.00", 5.0, 0.05, 0.0),
            mk("ctl-2.55", 2.55, 0.05, 0.0),
            mk("ctl-2.15", 2.15, 0.05, 0.0)]


# ------------------------------------------------------------------ truth ---
def run_truth(case, steps_per_orbit, nsamp=4001):
    """Velocity-Verlet N-body (star, perturber, massless inner), float64.

    dt = P1/steps_per_orbit (P1 = 2pi, a1 = 1, n1 = 1). Samples the osculating
    heliocentric elements of both orbits on a uniform grid over [0, T].
    """
    # barycentric inertial ICs from heliocentric elements
    x1h, y1h, vx1h, vy1h = elem_to_state(case["a1"], case["e1"], case["varpi1"],
                                         case["lam1"], 1.0)
    x2h, y2h, vx2h, vy2h = elem_to_state(case["a2"], case["e2"], case["varpi2"],
                                         case["lam2_0"], MU2)
    mtot = 1.0 + M2
    vx0 = -M2 * vx2h / mtot
    vy0 = -M2 * vy2h / mtot
    x = [0.0, x2h, x1h]
    y = [0.0, y2h, y1h]
    vx = [vx0, vx0 + vx2h, vx0 + vx1h]
    vy = [vy0, vy0 + vy2h, vy0 + vy1h]

    dt = TWOPI / steps_per_orbit
    T = case["T"]
    nsteps = int(T / dt) + 1
    samp_dts = [T * i / (nsamp - 1) for i in range(nsamp)]
    out = {"t": [], "e1": [], "varpi1": [], "lam1": [],
           "e2": [], "varpi2": [], "lam2": []}

    ejected = [False]

    def sample(t):
        hx, hy = x[2] - x[0], y[2] - y[0]
        hvx, hvy = vx[2] - vx[0], vy[2] - vy[0]
        a1, e1, vp1, lm1 = state_to_elem(hx, hy, hvx, hvy, 1.0)
        ox, oy = x[1] - x[0], y[1] - y[0]
        ovx, ovy = vx[1] - vx[0], vy[1] - vy[0]
        a2o, e2o, vp2, lm2 = state_to_elem(ox, oy, ovx, ovy, MU2)
        out["t"].append(t)
        out["e1"].append(e1)
        out["varpi1"].append(vp1)
        out["lam1"].append(lm1)
        out["e2"].append(e2o)
        out["varpi2"].append(vp2)
        out["lam2"].append(lm2)
        if a1 <= 0.0 or e1 >= 1.0:
            ejected[0] = True


    # unrolled accelerations (bodies: 0 star m=1, 1 perturber m=M2, 2 inner m=0)
    def accel():
        # a_0 = m2 (r1-r0)/d01^3          (only the perturber pulls the star)
        # a_1 = m0 (r0-r1)/d01^3          (only the star pulls the perturber)
        # a_2 = m0 (r0-r2)/d02^3 + m2 (r1-r2)/d12^3   (inner is massless)
        dx01 = x[1] - x[0]; dy01 = y[1] - y[0]
        d = (dx01 * dx01 + dy01 * dy01) ** 1.5
        f01 = 1.0 / d; f10 = M2 / d
        dx02 = x[2] - x[0]; dy02 = y[2] - y[0]
        d = (dx02 * dx02 + dy02 * dy02) ** 1.5
        f02 = 1.0 / d
        dx12 = x[2] - x[1]; dy12 = y[2] - y[1]
        d = (dx12 * dx12 + dy12 * dy12) ** 1.5
        f12 = M2 / d
        return [dx01 * f10, -dx01 * f01, -dx02 * f02 - dx12 * f12], \
               [dy01 * f10, -dy01 * f01, -dy02 * f02 - dy12 * f12]

    ax, ay = accel()
    t = 0.0
    si = 0
    hdt = 0.5 * dt
    for step in range(nsteps):
        if t >= samp_dts[si] - 1e-12 or step == nsteps - 1:
            sample(t)
            if ejected[0]:
                out["t_eject"] = t
                break
            si += 1
            if si >= nsamp:
                break
        for i in range(3):
            vx[i] += ax[i] * hdt
            vy[i] += ay[i] * hdt
            x[i] += dt * vx[i]
            y[i] += dt * vy[i]
        ax, ay = accel()
        for i in range(3):
            vx[i] += ax[i] * hdt
            vy[i] += ay[i] * hdt
        t += dt
    if not ejected[0]:
        while si < nsamp:        # tail rounding
            sample(T)
            si += 1
    return out


# ------------------------------------------------------------------- law ---
def run_law(case, nodes=8, split=1, mode="arc", lam_extra="first"):
    """lam_extra: 'first' = the rung's first-order dlam alone (all configs);
    'none'/'drift' are diagnostics (see dossier), not rung configurations."""
    """Event-layer run. mode: 'arc' (split=1 conjunctions, 2 = +oppositions),
    'avg' (one kick per inner orbit, orbit-averaged; outer frozen at mid-window),
    'none' (no perturbation). Returns window records + counters."""
    m2, mu2 = case["m2"], case["mu2"]
    a2, e2, varpi2, n2 = case["a2"], case["e2"], case["varpi2"], case["n2"]
    M2_0 = case["lam2_0"] - varpi2
    T = case["T"]
    xs, ws = GL[nodes]

    def opos(t):
        return outer_pos(a2, e2, varpi2, M2_0 + n2 * t)

    a = case["a1"]
    ex = case["e1"] * cos(case["varpi1"])
    ey = case["e1"] * sin(case["varpi1"])
    lam1 = case["lam1"]
    t = 0.0
    uacc = 0.0          # accumulated (lam1 - lam2) phase gain since last event,
    wins = []           # kick-corrected: conjunctions are 2pi apart in uacc
    nkick = 0
    quad_evals = 0
    while t < T - 1e-12:
        e = hypot(ex, ey)
        varpi = atan2(ey, ex)
        n1 = 1.0 / (a * sqrt(a))
        if mode == "none":
            wins.append((t, T, a, ex, ey, varpi, lam1, n1))
            break
        target_u = pi if split == 2 else TWOPI   # event spacing in phase
        if mode == "avg":
            t1 = t + TWOPI / n1
        else:
            t1 = t + (target_u - uacc) / (n1 - n2)
            if t1 - t < 1e-6:         # degenerate lock: freeze and coast (stall)
                wins.append((t, T, a, ex, ey, varpi, lam1, n1))
                return dict(wins=wins, nkick=nkick, quad_evals=quad_evals,
                            stalled=True)
        if t1 > T:
            t1 = T
        wins.append((t, t1, a, ex, ey, varpi, lam1, n1))
        # kick = first-order integral of the Gauss rates along the unperturbed
        # arc (Gauss-Picard), applied to the invariants at the window end.
        da = dex = dey = dlm = 0.0
        if mode == "avg":
            # nodes in mean anomaly over the orbit; the outer advances along
            # its own orbit during the averaging (standard single average)
            tmid = 0.5 * (t + t1)
            for u, wu in zip(xs, ws):
                Mk = pi + pi * u
                lam_k = varpi + Mk
                xx, yy, vxx, vyy = elem_to_state(a, e, varpi, lam_k, 1.0)
                r2x, r2y = opos(tmid + (Mk - pi) / n1)
                apx, apy = pert_a(xx, yy, r2x, r2y, m2)
                ad, exd, eyd, lmd = vop_rates(xx, yy, vxx, vyy, apx, apy, a, lam_k)
                f = pi * wu / n1                    # dt = dM/n1
                da += ad * f; dex += exd * f; dey += eyd * f; dlm += lmd * f
                quad_evals += 1
        else:
            Dt = t1 - t
            for u, wu in zip(xs, ws):
                tk = t + Dt * (u + 1.0) * 0.5
                lam_k = lam1 + n1 * (tk - t)
                xx, yy, vxx, vyy = elem_to_state(a, e, varpi, lam_k, 1.0)
                r2x, r2y = opos(tk)
                apx, apy = pert_a(xx, yy, r2x, r2y, m2)
                ad, exd, eyd, lmd = vop_rates(xx, yy, vxx, vyy, apx, apy, a, lam_k)
                f = Dt * wu * 0.5                   # dt weight
                da += ad * f; dex += exd * f; dey += eyd * f; dlm += lmd * f
                quad_evals += 1
        a += da
        dl = dlm
        if lam_extra == "none":
            dl = 0.0
        elif lam_extra == "drift":
            dl += 0.5 * (-1.5 * a ** -2.5) * da * (t1 - t)  # within-window dn drift
        lam1 = lam1 + n1 * (t1 - t) + dl
        if mode != "avg":
            uacc = uacc + (n1 - n2) * (t1 - t) + dlm - target_u
        t = t1
        nkick += 1
        if not (0.02 < a < 5.0) or hypot(ex, ey) > 0.95 or a <= 0.0:
            n1t = 1.0 / (a * sqrt(a)) if a > 0 else 0.0
            wins.append((t, T, a, ex, ey, atan2(ey, ex), lam1, n1t))
            break
    return dict(wins=wins, nkick=nkick, quad_evals=quad_evals, stalled=False)


def law_sample(case, lawres, ts):
    """Piecewise elements of the law on a uniform grid: e1, varpi1, lam1(t)."""
    wins = lawres["wins"]
    e1s, vp1s, lm1s = [], [], []
    import bisect
    starts = [w[0] for w in wins]
    for tt in ts:
        i = bisect.bisect_right(starts, tt) - 1
        if i < 0:
            i = 0
        t0, t1, a, ex, ey, varpi, lam0, n1 = wins[i]
        e1s.append(hypot(ex, ey))
        vp1s.append(varpi)
        lm1s.append(lam0 + n1 * (tt - t0))
    return e1s, vp1s, lm1s


def lam2_of(case, ts):
    """Outer mean longitude (analytic unperturbed orbit)."""
    return [case["varpi2"] + (case["lam2_0"] - case["varpi2"]) + case["n2"] * t
            for t in ts]


def concentration(phis):
    """|mean of exp(i phi)| — 1 for a fixed angle, ~0 for uniform circulation."""
    c = s = 0.0
    for p in phis:
        c += cos(p)
        s += sin(p)
    return hypot(c, s) / len(phis)


def resonant_angle(l2, l1, w1):
    return fmod(2.0 * l2 - l1 - w1 + pi, TWOPI) - pi


# ------------------------------------------------------------ check (machinery)
def cmd_check():
    import random
    random.seed(7)
    worst = 0.0
    for _ in range(2000):
        a = random.uniform(0.4, 3.0)
        e = random.uniform(0.0, 0.7)
        varpi = random.uniform(-pi, pi)
        lam = random.uniform(-pi, pi)
        x, y, vx, vy = elem_to_state(a, e, varpi, lam, 1.0)
        a2, e2, vp2, lm2 = state_to_elem(x, y, vx, vy, 1.0)
        x2, y2, vx2, vy2 = elem_to_state(a2, e2, vp2, lm2, 1.0)
        dh = e2 * cos(vp2) - e * cos(varpi)
        dk = e2 * sin(vp2) - e * sin(varpi)
        dlam = (lm2 - lam + pi) % TWOPI - pi
        err = max(abs(a2 - a) / a, hypot(dh, dk), abs(dlam),
                  abs(x2 - x), abs(y2 - y), abs(vx2 - vx), abs(vy2 - vy))
        worst = max(worst, err)
    print(f"round-trip, adversarial (a in [0.4,3], e <= 0.7): worst = {worst:.3e}")
    worst2 = 0.0
    for _ in range(2000):
        a = random.uniform(0.7, 1.5)
        e = random.uniform(0.005, 0.8)
        varpi = random.uniform(-pi, pi)
        lam = random.uniform(-pi, pi)
        x, y, vx, vy = elem_to_state(a, e, varpi, lam, 1.0)
        a2, e2, vp2, lm2 = state_to_elem(x, y, vx, vy, 1.0)
        x2, y2, vx2, vy2 = elem_to_state(a2, e2, vp2, lm2, 1.0)
        err = max(abs(a2 - a) / a,
                  abs(e2 * cos(vp2) - e * cos(varpi)), abs(e2 * sin(vp2) - e * sin(varpi)),
                  abs((lm2 - lam + pi) % TWOPI - pi),
                  abs(x2 - x), abs(y2 - y), abs(vx2 - vx), abs(vy2 - vy))
        worst2 = max(worst2, err)
    print(f"round-trip, run regime (a in [0.7,1.5], e >= 0.005): worst = {worst2:.3e}"
          f"  -> {'PASS' if worst2 < 1e-12 else 'FAIL'} (rung wants <= 1e-12;"
          f" adversarial floor is small-e angle conditioning, e-vector itself ~1e-15)")
    # first-order validity: one short window vs two fine integrations
    case = default_cases()[0]
    m2, mu2 = case["m2"], case["mu2"]
    a2, e2, varpi2, n2 = case["a2"], case["e2"], case["varpi2"], case["n2"]
    M2_0 = case["lam2_0"] - varpi2
    t0, t1 = 0.0, 0.05
    dt = 1e-5
    x, y, vx, vy = elem_to_state(case["a1"], case["e1"], case["varpi1"], case["lam1"], 1.0)

    def accel_p(x, y, t):
        r2x, r2y = outer_pos(a2, e2, varpi2, M2_0 + n2 * t)
        dx, dy = r2x - x, r2y - y
        d3 = (dx * dx + dy * dy) ** 1.5
        r2n = hypot(r2x, r2y)
        apx = m2 * (dx / d3 - r2x / r2n ** 3)
        apy = m2 * (dy / d3 - r2y / r2n ** 3)
        return apx - x / (x * x + y * y) ** 1.5, apy - y / (x * x + y * y) ** 1.5

    nst = int((t1 - t0) / dt)
    h = 0.5 * dt
    for _ in range(nst):
        tm = t0 + dt * _ + 0.5 * dt
        te = t0 + dt * (_ + 1)
        apx, apy = accel_p(x, y, tm)
        vx += apx * h; vy += apy * h
        x += dt * vx; y += dt * vy
        apx, apy = accel_p(x, y, te)
        vx += apx * h; vy += apy * h
    a_p, e_p, vp_p, lm_p = state_to_elem(x, y, vx, vy, 1.0)
    # kick: Gauss-rate quadrature with 64 nodes along the unperturbed arc
    xs, ws = GL[64]
    a = case["a1"]; e = case["e1"]; varpi = case["varpi1"]; lam1 = case["lam1"]
    da = dex = dey = dlm = 0.0
    for u, wu in zip(xs, ws):
        tk = t0 + (t1 - t0) * (u + 1.0) * 0.5
        lam_k = lam1 + tk - t0
        xx, yy, vxx, vyy = elem_to_state(a, e, varpi, lam_k, 1.0)
        r2x, r2y = outer_pos(a2, e2, varpi2, M2_0 + n2 * tk)
        apx, apy = pert_a(xx, yy, r2x, r2y, m2)
        ad, exd, eyd, lmd = vop_rates(xx, yy, vxx, vyy, apx, apy, a, lam_k)
        f = (t1 - t0) * wu * 0.5
        da += ad * f; dex += exd * f; dey += eyd * f; dlm += lmd * f
    got = (a_p - a, e_p * cos(vp_p) - e * cos(varpi), e_p * sin(vp_p) - e * sin(varpi),
           (lm_p - lam1 - (t1 - t0) + pi) % TWOPI - pi)
    want = (da, dex, dey, dlm)
    print("first-order window check (window 0.05, verlet dt=1e-5, quad 64 nodes):")
    names = ("da", "d(ex)", "d(ey)", "dlam")
    for nm, g, wv in zip(names, got, want):
        print(f"  {nm:6s} integration {g:+.8e}  quadrature {wv:+.8e}  "
              f"rel diff {abs(g - wv) / max(abs(wv), 1e-30):.2e}")


# ------------------------------------------------------------------- run ---
LAW_CONFIGS = {
    "arc-g8": dict(nodes=8, split=1, mode="arc"),
    "arc-g16": dict(nodes=16, split=1, mode="arc"),
    "arc-g8-half": dict(nodes=8, split=2, mode="arc"),
    "averaged": dict(nodes=8, split=1, mode="avg"),
    "none": dict(nodes=8, split=1, mode="none"),
}
RESONANT = ("res-2-1", "res-2-1-w2-4")
CONTROLS = ("ctl-5.00", "ctl-2.55", "ctl-2.15")


def series_stats(case, ts, e1s, vp1s, lm1s):
    """Max e1 and resonant-angle concentration on a uniform grid."""
    l2s = lam2_of(case, ts)
    phis = [resonant_angle(l2, l1, w1) for l2, l1, w1 in zip(l2s, lm1s, vp1s)]
    return max(e1s), concentration(phis), phis


def cmd_run():
    data = {}
    data["truth_max_e"] = {}
    data["truth_phi"] = {}
    cases = default_cases()
    truths = {}
    print("truth integrations (verlet, steps/orbit):")
    for c in cases:
        truths[c["name"]] = {}
        for res in (600, 1200, 2400):
            r = run_truth(c, res)
            assert "t_eject" not in r, f"{c['name']} ejected at {r['t_eject']} (res {res})"
            truths[c["name"]][res] = r
            mx, cc, phis = series_stats(c, r["t"], r["e1"], r["varpi1"], r["lam1"])
            print(f"  {c['name']:14s} res={res:5d}: max e1 = {mx:.5f}, C = {cc:.4f}")
            if res == 2400:
                data["truth_max_e"][c["name"]] = r["e1"][::4]
                data["truth_phi"][c["name"]] = phis[::4]
    data["truth_convergence"] = {c["name"]: {res: dict(max_e=max(truths[c["name"]][res]["e1"]),
        C=series_stats(c, truths[c["name"]][res]["t"], truths[c["name"]][res]["e1"],
                       truths[c["name"]][res]["varpi1"], truths[c["name"]][res]["lam1"])[1])
        for res in (600, 1200, 2400)} for c in cases}

    print("law runs:")
    laws = {}
    for cname, c in ((c["name"], c) for c in cases):
        ts = [c["T"] * i / 4000 for i in range(4001)]
        for lname, lcfg in LAW_CONFIGS.items():
            lr = run_law(c, **lcfg)
            e1s, vp1s, lm1s = law_sample(c, lr, ts)
            mx, cc, phis = series_stats(c, ts, e1s, vp1s, lm1s)
            orbits = c["T"] / TWOPI
            laws[(cname, lname)] = dict(max_e=mx, C=cc, nkick=lr["nkick"],
                                        kicks_per_orbit=lr["nkick"] / orbits,
                                        quad_evals=lr["quad_evals"])
            print(f"  {cname:14s} {lname:12s}: max e1 = {mx:.5f}, C = {cc:.4f}, "
                  f"kicks/orbit = {lr['nkick'] / orbits:.3f}")
            if lname in ("arc-g8", "arc-g16", "arc-g8-half", "averaged"):
                step = 4
                data.setdefault("series", {}).setdefault(cname, {})[lname] = dict(
                    t=ts[::step], e1=e1s[::step],
                    phi=[phis[i] for i in range(0, len(phis), step)])

    def cfg_metrics(lname):
        ref = {c["name"]: truths[c["name"]][2400] for c in cases}
        refstat = {n: (max(r["e1"]), series_stats(c, r["t"], r["e1"], r["varpi1"], r["lam1"])[1])
                   for n, c, r in ((c["name"], c, ref[c["name"]]) for c in cases)}
        pumps, libs, ctls, kpo = [], [], [], []
        for c in cases:
            n = c["name"]
            if n in RESONANT:
                if lname == "truth-1200":   # the positive control: itself vs truth-2400
                    r = truths[n][1200]
                    mx, cc, _ = series_stats(c, r["t"], r["e1"], r["varpi1"], r["lam1"])
                    libs.append(cc / refstat[n][1])
                else:
                    L = laws[(n, lname)]
                    mx = L["max_e"]
                    libs.append(L["C"] / refstat[n][1])
                pumps.append(mx / refstat[n][0])
            elif n in CONTROLS:
                if lname == "truth-1200":
                    r = truths[n][1200]
                    mx, _, _ = series_stats(c, r["t"], r["e1"], r["varpi1"], r["lam1"])
                else:
                    mx = laws[(n, lname)]["max_e"]
                ctls.append(0.8 <= mx / refstat[n][0] <= 1.2)
            if lname == "truth-1200":
                kpo.append(0.0)
            elif lname == "none":
                kpo.append(0.0)
            else:
                kpo.append(laws[(n, lname)]["kicks_per_orbit"])
        return {"e_pump_ratio_min": min(pumps), "e_pump_ratio_max": max(pumps),
                "libration_ratio_min": min(libs), "control_pass_fraction": sum(ctls) / len(ctls),
                "dense_steps": 0, "kicks_per_orbit": sorted(kpo)[len(kpo) // 2]}

    metrics = {}
    for lname in list(LAW_CONFIGS) + ["truth-1200"]:
        metrics[lname] = cfg_metrics(lname)
        print(lname, json.dumps(metrics[lname]))
    with open(os.path.join(OUT, "metrics.json"), "w") as f:
        json.dump(metrics, f, indent=1)
    data["laws"] = {f"{k[0]}/{k[1]}": v for k, v in laws.items()}
    with open(os.path.join(OUT, "data.json"), "w") as f:
        json.dump(data, f)

    make_picture(cases, data)


def make_picture(cases, data):
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    order = ["res-2-1", "res-2-1-w2-4", "ctl-5.00", "ctl-2.55", "ctl-2.15"]
    styles = {"arc-g8": ("tab:blue", "-"), "arc-g16": ("tab:orange", "-"),
              "arc-g8-half": ("tab:green", "-"), "averaged": ("tab:red", ":")}
    fig, axes = plt.subplots(len(order), 2, figsize=(11.5, 12.5))
    for row, cname in enumerate(order):
        ax, axh = axes[row][0], axes[row][1]
        s = data["series"][cname]
        for lname, (col, ls) in styles.items():
            ax.plot(s[lname]["t"], s[lname]["e1"], ls, color=col, lw=1.0,
                    alpha=0.85, label=lname)
        ax.plot(s["arc-g8"]["t"], data["truth_max_e"][cname], color="k", lw=1.4,
                alpha=0.9, label="truth-2400")
        ax.set_ylabel("$e_1$")
        ax.set_title(f"{cname}  (ratio {cname.split('-')[-1]})", fontsize=10)
        if row == 0:
            ax.legend(fontsize=7, loc="upper left", ncol=2)
        bins = np.linspace(-np.pi, np.pi, 49)
        axh.hist(np.array(s["arc-g16"]["phi"]), bins=bins, color="tab:orange",
                 alpha=0.6, label="arc-g16")
        axh.hist(np.array(s["averaged"]["phi"]), bins=bins, color="tab:red",
                 alpha=0.4, label="averaged")
        axh.hist(np.array(data["truth_phi"][cname]), bins=bins, color="k",
                 histtype="step", lw=1.4, label="truth-2400")
        axh.set_xlabel(r"$\phi = 2\lambda_2 - \lambda_1 - \varpi_1$")
        if row == 0:
            axh.legend(fontsize=7)
    axes[-1][0].set_xlabel("t (inner orbits x 2$\\pi$)")
    fig.suptitle("Rung r4 v2 — arc-integrated kicks vs dense truth (m2 = 3e-3, 200 synodic periods)",
                 fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(os.path.join(OUT, "picture.png"), dpi=110)
    print("picture written")


# -------------------------------------------------------------- quad audit ---
def cmd_quad():
    """Quadrature convergence of one window kick (frozen res-2-1 case)."""
    c = default_cases()[0]
    a, e, varpi, lam1 = c["a1"], c["e1"], c["varpi1"], c["lam1"]
    n1, n2 = 1.0, c["n2"]
    M2_0 = c["lam2_0"] - c["varpi2"]
    D0 = (c["varpi2"] + M2_0 - lam1) % TWOPI
    t1 = D0 / (n1 - n2)                      # first conjunction
    for nnode in (8, 16, 32, 64):
        xs, ws = GL[nnode]
        da = dex = dey = dlm = 0.0
        for u, wu in zip(xs, ws):
            tk = t1 * (u + 1.0) * 0.5
            lam_k = lam1 + tk
            xx, yy, vxx, vyy = elem_to_state(a, e, varpi, lam_k, 1.0)
            r2x, r2y = outer_pos(c["a2"], c["e2"], c["varpi2"], M2_0 + n2 * tk)
            apx, apy = pert_a(xx, yy, r2x, r2y, c["m2"])
            ad, exd, eyd, lmd = vop_rates(xx, yy, vxx, vyy, apx, apy, a, lam_k)
            f = t1 * wu * 0.5
            da += ad * f; dex += exd * f; dey += eyd * f; dlm += lmd * f
        print(f"nodes={nnode:3d}: da={da:+.6e} de={hypot(dex, dey):+.6e} "
              f"(dex={dex:+.3e}, dey={dey:+.3e}) dlam={dlm:+.6e}")


def cmd_scan():
    """Quick truth scan of IC variants for the baseline resonant case (600 steps)."""
    for phi0, e1 in ((0.0, 0.02), (pi, 0.02), (0.0, 0.05), (pi, 0.05), (0.5, 0.02)):
        lam1 = 1.0
        lam2 = 0.5 * (lam1 + phi0)   # 2*lam2 - lam1 - varpi1 = phi0 (varpi1=0)
        c = make_case(f"scan", 2.0, e1, 0.0, lam1, 0.0, 0.0, lam2)
        r = run_truth(c, 600)
        ph = [resonant_angle(l2, l1, w1) for l2, l1, w1 in
              zip(r["lam2"], r["lam1"], r["varpi1"])]
        print(f"phi0={phi0:+.2f} e1_0={e1:.2f}: max e1 = {max(r['e1']):.4f} "
              f"(pump x{max(r['e1']) / e1:.1f}), C = {concentration(ph):.3f}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "check":
        cmd_check()
    elif cmd == "scan":
        cmd_scan()
    elif cmd == "quad":
        cmd_quad()
    elif cmd == "run":
        cmd_run()
    else:
        print("usage: e2_arc_kick.py check|scan|quad|run")
