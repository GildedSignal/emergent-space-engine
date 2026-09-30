#!/usr/bin/env python3
"""Rung r4 v2 — arc-integrated (Gauss-Picard) kicks vs mean-motion resonance.

Run id: 20260930-0732-rung-r4-resonance-v2-0a18  (author run)

Problem: restricted, coplanar. Central mass M=1 (G=1), massless particle on an
inner orbit (a1=1, e1_0, periapse w1_0, mean longitude l1_0), circular outer
perturber of mass m2=3e-3 with mean motion n2 = n1/q.

Truth: dense float64 N-body (central + perturber + massless particle), leapfrog
KDK, fixed step, converged over 600/1200/2400 steps per inner orbit.

Law (design's event layer): within each window the particle's Kepler arc is
held fixed (unperturbed, elements frozen at window start); at the window end
the first-order integral of the Gauss planetary equations along that arc is
applied as a jump in (a, e, w, M). Quadrature: Gauss-Legendre at 8 or 16 nodes
(arc-g8 / arc-g16). arc-g8-half uses two fixed windows per synodic period.
`averaged` replaces the arc integral by the double orbit-average over both mean
anomalies (H0190 K2 style). `none` applies no perturbation.

Subcommands: sanity | ics | truth | law | metrics | picture
"""

import json
import math
import os
import sys

TWO_PI = 2.0 * math.pi
HERE = os.path.dirname(os.path.abspath(__file__))

G = 1.0
MC = 1.0        # central mass
M2 = 3.0e-3     # perturber mass (mass ratio 3e-3, as the rung fixes)
A1 = 1.0
NSYN = 200      # synodic periods per run ("at least 200")
SPO = 50        # samples per inner orbit, identical for truth and law

MU1 = G * (MC + 0.0)          # particle-central Kepler parameter
MU2 = G * (MC + M2)           # perturber-central Kepler parameter
N1 = math.sqrt(MU1 / A1**3)   # = 1

# ---------------------------------------------------------------- cases
def make_case(q, l20, e1=0.05, w1=0.0, l1=0.0):
    n2 = N1 / q
    a2 = (MU2 / n2**2) ** (1.0 / 3.0)
    psyn = TWO_PI / abs(N1 - n2)
    return dict(q=q, l20=l20, e1=e1, w1=w1, l1=l1, n2=n2, a2=a2, psyn=psyn,
                tend=NSYN * psyn, orbits=NSYN * psyn / TWO_PI)

RESONANT = ["r2-base", "r2-shift"]
CONTROLS = ["c-5.00", "c-2.55", "c-2.15"]

def cases(ic):
    """ic: dict with the two resonant ICs chosen at setup (see ics step)."""
    return {
        "r2-base":  make_case(2.00, ic["l20_base"], e1=ic["e1"]),
        "r2-shift": make_case(2.00, 4.0,             e1=ic["e1"]),
        "c-5.00":   make_case(5.00, 0.0,             e1=ic["e1"]),
        "c-2.55":   make_case(2.55, 0.0,             e1=ic["e1"]),
        "c-2.15":   make_case(2.15, 0.0,             e1=ic["e1"]),
    }

def load_ic():
    with open(os.path.join(HERE, "ic.json")) as f:
        return json.load(f)

# ---------------------------------------------------------------- Kepler
def solve_kepler(M, e):
    M = M % TWO_PI
    E = M
    for _ in range(60):
        f = E - e * math.sin(E) - M
        d = f / (1.0 - e * math.cos(E))
        E -= d
        if abs(d) < 1e-15:
            break
    return E

def elem_to_state(a, e, w, M, mu):
    E = solve_kepler(M, e)
    cE, sE = math.cos(E), math.sin(E)
    sq = math.sqrt(1.0 - e * e)
    n = math.sqrt(mu / (a * a * a))
    den = 1.0 - e * cE
    xp = a * (cE - e)
    yp = a * sq * sE
    vxp = -a * n * sE / den
    vyp = a * sq * n * cE / den
    cw, sw = math.cos(w), math.sin(w)
    return (cw * xp - sw * yp, sw * xp + cw * yp,
            cw * vxp - sw * vyp, sw * vxp + cw * vyp)

def state_to_elem(x, y, vx, vy, mu):
    r = math.hypot(x, y)
    v2 = vx * vx + vy * vy
    a = 1.0 / (2.0 / r - v2 / mu)
    rv = x * vx + y * vy
    ex = (v2 / mu - 1.0 / r) * x - rv * vx / mu
    ey = (v2 / mu - 1.0 / r) * y - rv * vy / mu
    e = math.hypot(ex, ey)
    if e < 1e-12:
        w = 0.0
        M = math.atan2(y, x) % TWO_PI
        return a, e, w, M
    w = math.atan2(ey, ex) % TWO_PI
    cosf = (ex * x + ey * y) / (e * r)
    sinf = (ex * y - ey * x) / (e * r)      # (e x r)_z, prograde
    sq = math.sqrt(max(0.0, 1.0 - e * e))
    sinE = r * sinf / (a * sq)
    cosE = r * cosf / a + e
    E = math.atan2(sinE, cosE) % TWO_PI
    M = (E - e * math.sin(E)) % TWO_PI
    return a, e, w, M

def gauss_legendre(n):
    import numpy as np
    x, w = np.polynomial.legendre.leggauss(n)
    return list(map(float, x)), list(map(float, w))

_GL = {n: gauss_legendre(n) for n in (8, 16, 24)}

# ---------------------------------------------------------------- truth
def run_truth(cs, nsteps, out=None):
    """Dense N-body leapfrog (central, perturber, massless particle)."""
    n2, a2 = cs["n2"], cs["a2"]
    dt = TWO_PI / nsteps
    nstep = int(cs["tend"] / dt)
    x2r, y2r, vx2r, vy2r = elem_to_state(a2, 0.0, 0.0, cs["l20"], MU2)
    x1r, y1r, vx1r, vy1r = elem_to_state(A1, cs["e1"], cs["w1"],
                                         cs["l1"] - cs["w1"], MU1)
    mt = MC + M2
    rx = [-M2 * x2r / mt, x2r - M2 * x2r / mt, -M2 * x2r / mt + x1r]
    ry = [-M2 * y2r / mt, y2r - M2 * y2r / mt, -M2 * y2r / mt + y1r]
    vx = [-M2 * vx2r / mt, vx2r - M2 * vx2r / mt, -M2 * vx2r / mt + vx1r]
    vy = [-M2 * vy2r / mt, vy2r - M2 * vy2r / mt, -M2 * vy2r / mt + vy1r]

    def acc():
        dx = rx[1] - rx[0]; dy = ry[1] - ry[0]
        d = math.sqrt(dx * dx + dy * dy); inv = 1.0 / (d * d * d)
        f = G * inv  # common G/d^3
        # outer (1) pulled by central (0): G*MC*(r0-r1)/d^3
        a1x = -f * MC * dx; a1y = -f * MC * dy
        # central (0) pulled by outer (1): G*M2*(r1-r0)/d^3
        a0x = f * M2 * dx; a0y = f * M2 * dy
        dxp = rx[0] - rx[2]; dyp = ry[0] - ry[2]
        dp = math.sqrt(dxp * dxp + dyp * dyp); ip = G / (dp * dp * dp)
        dxq = rx[1] - rx[2]; dyq = ry[1] - ry[2]
        dq = math.sqrt(dxq * dxq + dyq * dyq); iq = G / (dq * dq * dq)
        a2x = ip * MC * dxp + iq * M2 * dxq
        a2y = ip * MC * dyp + iq * M2 * dyq
        return [a0x, a1x, a2x], [a0y, a1y, a2y]

    ax, ay = acc()
    every = max(1, nsteps // SPO)
    ts, es, phis = [], [], []
    emax = 0.0; emin = 10.0
    for k in range(nstep):
        # KDK
        for i in range(3):
            vx[i] += 0.5 * dt * ax[i]; vy[i] += 0.5 * dt * ay[i]
            rx[i] += dt * vx[i]; ry[i] += dt * vy[i]
        ax, ay = acc()
        for i in range(3):
            vx[i] += 0.5 * dt * ax[i]; vy[i] += 0.5 * dt * ay[i]
        if (k + 1) % every == 0 or k == nstep - 1:
            t = (k + 1) * dt
            # relative to central
            px, py = rx[2] - rx[0], ry[2] - ry[0]
            pvx, pvy = vx[2] - vx[0], vy[2] - vy[0]
            ox, oy = rx[1] - rx[0], ry[1] - ry[0]
            ovx, ovy = vx[1] - vx[0], vy[1] - vy[0]
            ap, e, w, M = state_to_elem(px, py, pvx, pvy, MU1)
            a2o, e2o, w2o, M2o = state_to_elem(ox, oy, ovx, ovy, MU2)
            lam1 = (w + M) % TWO_PI
            lam2 = (w2o + M2o) % TWO_PI
            phi = (2.0 * lam2 - lam1 - w) % TWO_PI
            ts.append(t); es.append(e); phis.append(phi)
            if e > emax: emax = e
            if e < emin: emin = e
    return dict(t=ts, e=es, phi=phis, emax=emax, emin=emin,
                R=concentration(phis), steps=nstep)

def concentration(phis):
    sr = si = 0.0
    for p in phis:
        sr += math.cos(p); si += math.sin(p)
    return math.hypot(sr, si) / len(phis)

# ---------------------------------------------------------------- the law
def gauss_rates(a, e, w, n, M1, lam2, a2, m2=G * M2):
    """Gauss planetary rates at particle mean anomaly M1, perturber longitude lam2."""
    E = solve_kepler(M1, e)
    cE, sE = math.cos(E), math.sin(E)
    sq = math.sqrt(1.0 - e * e)
    den = 1.0 - e * cE
    cf = (cE - e) / den
    sf = sq * sE / den
    r = a * den
    theta = w + math.atan2(sf, cf)
    cth, sth = math.cos(theta), math.sin(theta)
    x1 = r * cth; y1 = r * sth
    x2 = a2 * math.cos(lam2); y2 = a2 * math.sin(lam2)
    r2 = a2  # circular outer
    dx = x2 - x1; dy = y2 - y1
    d32 = (dx * dx + dy * dy) ** 1.5
    # direct + indirect perturbing acceleration (relative to free central mass)
    px = m2 * (dx / d32 - x2 / r2**3)
    py = m2 * (dy / d32 - y2 / r2**3)
    R = (px * x1 + py * y1) / r
    T = (-px * y1 + py * x1) / r
    p = a * (1.0 - e * e)
    na = n * a
    rate_a = 2.0 / (n * sq) * (e * sf * R + p / r * T)
    rate_e = sq / na * (sf * R + (cf + cE) * T)
    rate_w = sq / (na * e) * (-cf * R + (1.0 + r / p) * sf * T)
    rate_M = -(2.0 / na) * (r / a) * R - sq * rate_w
    return rate_a, rate_e, rate_w, rate_M

def run_law(cs, mode, out=None):
    """mode in {arc8, arc16, half8, avg, none}. Returns samples like run_truth."""
    n2, a2, l20 = cs["n2"], cs["a2"], cs["l20"]
    a, e, w, M = A1, cs["e1"], cs["w1"], cs["l1"] - cs["w1"]
    n = math.sqrt(MU1 / a**3)
    t = 0.0
    tend = cs["tend"]
    dt_s = TWO_PI / SPO
    ts, es, phis = [], [], []
    emax = 0.0; emin = 10.0
    windows = 0
    gm2 = G * M2
    while t < tend - 1e-9:
        # window end: next conjunction in mean longitude (or fixed half-synodic)
        lam1 = w + M  # at current t (M is at t)
        if mode == "half8":
            t1 = t + 0.5 * TWO_PI / abs(n - n2)
        else:
            c = (l20 + n2 * t - lam1) % TWO_PI
            if c < 1e-12:
                c = TWO_PI
            t1 = t + c / (n - n2)
        if t1 > tend:
            t1 = tend
        # kick: integral of Gauss rates along the frozen arc
        if mode == "none":
            da = de = dw = dM = 0.0
        elif mode == "avg":
            xs, ws = _GL[24]
            s = [0.0, 0.0, 0.0, 0.0]
            for xi, wi in zip(xs, ws):
                Mi = math.pi * (xi + 1.0)
                for xj, wj in zip(xs, ws):
                    Lj = math.pi * (xj + 1.0)
                    rr = gauss_rates(a, e, w, n, Mi, Lj, a2, gm2)
                    wt = 0.25 * wi * wj
                    s[0] += wt * rr[0]; s[1] += wt * rr[1]
                    s[2] += wt * rr[2]; s[3] += wt * rr[3]
            da, de, dw, dM = s[0] * (t1 - t), s[1] * (t1 - t), s[2] * (t1 - t), s[3] * (t1 - t)
        else:
            nn = 8 if mode in ("arc8", "half8") else 16
            xs, ws = _GL[nn]
            s = [0.0, 0.0, 0.0, 0.0]
            for xq, wq in zip(xs, ws):
                tk = t + (t1 - t) * xq
                Mk = M + n * (tk - t)
                Lk = l20 + n2 * tk
                rr = gauss_rates(a, e, w, n, Mk, Lk, a2, gm2)
                s[0] += wq * rr[0]; s[1] += wq * rr[1]
                s[2] += wq * rr[2]; s[3] += wq * rr[3]
            da, de, dw, dM = (s[0] * (t1 - t), s[1] * (t1 - t),
                              s[2] * (t1 - t), s[3] * (t1 - t))
        # sample the frozen arc inside the window at the standard cadence
        span = t1 - t
        ns = max(1, int(span / dt_s))
        for i in range(ns):
            tsk = t + span * (i + 0.5) / ns
            lam1s = w + M + n * (tsk - t)
            phi = (2.0 * (l20 + n2 * tsk) - lam1s - w) % TWO_PI
            ts.append(tsk); es.append(e); phis.append(phi)
            if e > emax: emax = e
            if e < emin: emin = e
        # apply the jump at the window end
        a += da
        e = abs(e + de)
        w = (w + dw) % TWO_PI
        M = (M + n * (t1 - t) + dM) % TWO_PI
        n = math.sqrt(MU1 / a**3)
        t = t1
        windows += 1
    return dict(t=ts, e=es, phi=phis, emax=emax, emin=emin,
                R=concentration(phis), windows=windows, orbits=tend / TWO_PI,
                n_samples=len(ts))

# ---------------------------------------------------------------- outputs
MODES = {"arc-g8": "arc8", "arc-g16": "arc16", "arc-g8-half": "half8",
         "averaged": "avg", "none": "none"}

def save_samples(tag, case, res):
    import numpy as np
    os.makedirs(os.path.join(HERE, "samples"), exist_ok=True)
    dec = max(1, len(res["t"]) // 4000)
    np.savez_compressed(
        os.path.join(HERE, "samples", f"{tag}-{case}.npz"),
        t=np.array(res["t"][::dec]), e=np.array(res["e"][::dec]),
        phi=np.array(res["phi"][::dec]))
    return dict(case=case, emax=res["emax"], emin=res["emin"], R=res["R"],
                windows=res.get("windows"), orbits=res.get("orbits",
                        res.get("steps", 0) and 0 or None),
                n_samples=len(res["t"]))

def cmd_truth():
    ic = load_ic()
    cs_all = cases(ic)
    for nsteps in (600, 1200, 2400):
        out = {}
        for name, cs in cs_all.items():
            res = run_truth(cs, nsteps)
            summ = save_samples(f"truth{nsteps}", name, res)
            summ["steps"] = res["steps"]
            out[name] = summ
            print(f"truth{nsteps} {name}: emax={res['emax']:.4f} "
                  f"R={res['R']:.3f} steps={res['steps']}", flush=True)
        with open(os.path.join(HERE, f"truth{nsteps}.json"), "w") as f:
            json.dump(out, f, indent=1)

def cmd_law(mode):
    ic = load_ic()
    cs_all = cases(ic)
    m = MODES[mode]
    out = {}
    for name, cs in cs_all.items():
        res = run_law(cs, m)
        summ = save_samples(mode, name, res)
        summ["windows"] = res["windows"]
        out[name] = summ
        print(f"{mode} {name}: emax={res['emax']:.4f} R={res['R']:.3f} "
              f"windows={res['windows']}", flush=True)
    with open(os.path.join(HERE, f"law-{mode}.json"), "w") as f:
        json.dump(out, f, indent=1)

# ---------------------------------------------------------------- sanity
def cmd_sanity():
    import random
    random.seed(7)
    worst = 0.0
    for _ in range(300):
        a = random.uniform(0.3, 5.0)
        e = random.uniform(0.0, 0.6)
        w = random.uniform(0, TWO_PI)
        M = random.uniform(0, TWO_PI)
        mu = random.uniform(0.5, 2.0)
        s = elem_to_state(a, e, w, M, mu)
        a2, e2, w2, M2 = state_to_elem(*s, mu)
        w2 = (w2 - w + math.pi) % TWO_PI - math.pi  # allow 2pi slips
        M2 = (M2 - M + math.pi) % TWO_PI - math.pi
        err = max(abs(a2 - a) / a, abs(e2 - e), abs(w2), abs(M2))
        worst = max(worst, err)
    print(f"round-trip worst relative error: {worst:.3e}  (gate 1e-12)")
    # quadrature self-check: integrate sin over one period with 8 nodes
    xs, ws = _GL[8]
    s = sum(w * math.sin(math.pi * (x + 1)) for x, w in zip(xs, ws)) * math.pi
    print(f"GL8 integral of sin over [0,2pi]: {s:.3e} (exact 0)")
    # short control check: law (arc8) vs truth at q=5, 40 synodic periods
    cs = make_case(5.0, 0.0)
    cs["tend"] = 40 * cs["psyn"]
    tr = run_truth(cs, 1200)
    lw = run_law(cs, "arc8")
    print(f"q=5 control, 40 syn: truth emax={tr['emax']:.5f} emin={tr['emin']:.5f} | "
          f"law emax={lw['emax']:.5f} emin={lw['emin']:.5f}")
    cs = make_case(2.0, 0.0)
    cs["tend"] = 60 * cs["psyn"]
    tr = run_truth(cs, 1200)
    print(f"q=2 base, 60 syn: truth emax={tr['emax']:.5f} R={tr['R']:.3f}")

def cmd_ics():
    """Setup exploration: pick resonant ICs where the truth librates."""
    out = {}
    for l20 in (0.0, 1.0, 2.0, 3.0, 4.0):
        for e1 in (0.05, 0.10):
            cs = make_case(2.0, l20, e1=e1)
            cs["tend"] = 100 * cs["psyn"]
            tr = run_truth(cs, 600)
            print(f"l20={l20:.1f} e0={e1:.2f}: emax={tr['emax']:.4f} "
                  f"emin={tr['emin']:.4f} R={tr['R']:.3f}", flush=True)
            out[f"l{l20}-e{e1}"] = dict(emax=tr["emax"], R=tr["R"])
    with open(os.path.join(HERE, "ic-scan.json"), "w") as f:
        json.dump(out, f, indent=1)

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "sanity":
        cmd_sanity()
    elif cmd == "ics":
        cmd_ics()
    elif cmd == "truth":
        cmd_truth()
    elif cmd == "law":
        cmd_law(sys.argv[2])
    else:
        print(__doc__)
        sys.exit(2)

if __name__ == "__main__":
    main()
