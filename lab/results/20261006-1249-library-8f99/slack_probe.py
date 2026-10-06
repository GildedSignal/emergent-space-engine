#!/usr/bin/env python3
"""Slack-skin sizing law — run 20261006-1249-library-8f99.

Question (Taleb's redundancy lesson made quantitative): how must the encounter
skin's slack width be sized? Cheap model = the plane's: a Kepler generator
(osculating fit at setup) in the dominant field; the tide is the residual a
kick would correct. A pair's window is re-set when the generator's prediction
error crosses the slack width w. Measures setups per inner orbit, r(w), for a
non-resonant (nr), a detuned (det) and a resonant (res) test particle in a
restricted three-body field.

Restricted 3-body, heliocentric frame (direct + indirect term), e2 = 0.
Truth: DOP853 rtol 1e-12 (convergence checked at 1e-10).
Deterministic: fixed phases, no randomness. Order-of-magnitude claims only.
"""
import json
import sys
import time

import numpy as np
from scipy.integrate import solve_ivp

MU = 0.03          # perturber mass (primary = 1)
A2 = 5.0           # perturber semi-major axis
N2 = np.sqrt((1.0 + MU) / A2**3)  # perturber mean motion
PHI2 = np.pi       # perturber initial phase
E0 = 0.05          # belt free eccentricity (exactly represented by the fit)
ORBITS = 60
SAMP_PER_ORBIT = 1024
CASES = {"nr": 1.0, "det": 2.65, "res": 2.714}  # 5:2 interior resonance at 2.714


def rhs(t, y):
    """Heliocentric restricted: direct + indirect perturber acceleration."""
    x, y_, vx, vy = y
    r = np.hypot(x, y_)
    th = N2 * t + PHI2
    px, py = A2 * np.cos(th), A2 * np.sin(th)
    dx, dy = px - x, py - y_
    d = np.hypot(dx, dy)
    s = MU / d**3
    ax = -x / r**3 + s * dx - MU * px / A2**3
    ay = -y_ / r**3 + s * dy - MU * py / A2**3
    return (vx, vy, ax, ay)


def integrate(a, rtol=1e-12):
    """Truth trajectory of a test particle with e0=E0, started at apoapsis."""
    r0 = a * (1.0 + E0)
    v0 = np.sqrt(2.0 / r0 - 1.0 / a)
    T = ORBITS * 2.0 * np.pi * a**1.5
    dt = 2.0 * np.pi * a**1.5 / SAMP_PER_ORBIT
    t_eval = np.arange(dt, T, dt)
    sol = solve_ivp(rhs, (0.0, T), [r0, 0.0, 0.0, v0], method="DOP853",
                    rtol=rtol, atol=rtol * 1e-2, t_eval=t_eval, dense_output=False)
    assert sol.success, sol.message
    return sol.t, sol.y[0], sol.y[1], sol.y[2], sol.y[3]
def elements(x, y, vx, vy):
    """Osculating elements (a, e, omega, M0) about the primary, planar, mu_g=1."""
    r = np.hypot(x, y)
    v2 = vx * vx + vy * vy
    a = 1.0 / (2.0 / r - v2)
    rv = x * vx + y * vy
    ex = (v2 - 1.0 / r) * x - rv * vx
    ey = (v2 - 1.0 / r) * y - rv * vy
    e = np.hypot(ex, ey)
    omega = np.arctan2(ey, ex) if e > 1e-12 else 0.0
    if e > 1e-12:
        cosE = (1.0 - r / a) / e
        cosE = min(1.0, max(-1.0, cosE))
        sinE = rv / (e * np.sqrt(a)) if a > 0 else 0.0
        E = np.arctan2(sinE, cosE)
        M0 = E - e * sinE
    else:
        M0 = np.arctan2(y, x)
    return a, e, omega, M0

def kepler_xy(a, e, omega, M0, n, dt):
    """Vectorized Kepler propagation: position at dt after epoch."""
    M = (M0 + n * dt) % (2.0 * np.pi)
    E = M.copy()
    for _ in range(16):
        E -= (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    r = a * (1.0 - e * np.cos(E))
    nu = 2.0 * np.arctan2(np.sqrt(1.0 + e) * np.sin(E / 2.0),
                          np.sqrt(1.0 - e) * np.cos(E / 2.0))
    ang = nu + omega
    return r * np.cos(ang), r * np.sin(ang)



def make_rate_fn(t, x, y, vx, vy, horizon):
    """Skin semantics: the fit made at setup is KEPT until error crosses w."""
    N = len(t)

    def rate(w):
        setups = 0
        s = 0  # setup index (fit epoch)
        a, e, om, M0 = elements(x[s], y[s], vx[s], vy[s])
        n = np.sqrt(1.0 / a**3)
        i = 0  # scan frontier
        while i < N - 1:
            j_end = min(N, i + 1 + horizon)
            dt = t[i + 1:j_end] - t[s]
            px, py = kepler_xy(a, e, om, M0, n, dt)
            err = np.hypot(px - x[i + 1:j_end], py - y[i + 1:j_end])
            bad = np.nonzero(err > w)[0]
            if len(bad) == 0:
                i = j_end - 1  # window held; SAME fit, slide the frontier
                continue
            k = i + 1 + bad[0]  # crossing sample: re-setup here
            setups += 1
            s = k
            a, e, om, M0 = elements(x[s], y[s], vx[s], vy[s])
            n = np.sqrt(1.0 / a**3)
            i = k
        return setups, setups / ORBITS

    return rate


def free_error(t, x, y, vx, vy):
    """No-reset prediction error: fit once at t0, propagate, plus max |e| drift."""
    a, e, om, M0 = elements(x[0], y[0], vx[0], vy[0])
    px, py = kepler_xy(a, e, om, M0, np.sqrt(1.0 / a**3), t - t[0])
    err = np.hypot(px - x, py - y)
    es = np.array([elements(x[i], y[i], vx[i], vy[i])[1] for i in range(0, len(t), 64)])
    return err, es


def main():
    t0c = time.time()
    out = {"cases": {}}
    conv = None
    for name, a in CASES.items():
        t, x, y, vx, vy = integrate(a)
        if conv is None:
            t2, x2, y2, _, _ = integrate(a, rtol=1e-10)
            m = min(len(x), len(x2))
            conv = float(np.max(np.hypot(x[:m] - x2[:m], y[:m] - y2[:m])))
        err, es = free_error(t, x, y, vx, vy)
        A = float(err.max())
        # horizon: ~1.5 synodic periods of samples
        n = 1.0 / a**1.5
        syn = 2.0 * np.pi / abs(n - N2)
        horizon = int(1.5 * syn / (t[1] - t[0])) + 2
        rate = make_rate_fn(t, x, y, vx, vy, horizon)
        ws = A * np.logspace(np.log10(1.0 / 30.0), np.log10(1.0), 10)
        if name == "nr":
            ws = np.concatenate([ws, [2 * A, 4 * A]])  # look for the floor
        rows = []
        for w in ws:
            s, r = rate(float(w))
            rows.append((float(w), s, r))
        out["cases"][name] = {
            "a": a, "A_free": A, "e_max_drift": float(es.max()),
            "e0": E0, "samples": len(t),
            "synodic_period": float(syn),
            "curve": [{"w": w, "setups": s, "per_orbit": r} for w, s, r in rows],
        }
        print(f"[{name}] a={a}  A_free={A:.3e}  e_max={es.max():.4f} "
              f"(e0={E0})  samples={len(t)}  horizon={horizon}")
        for w, s, r in rows:
            print(f"    w={w:.3e}  setups={s:5d}  per_orbit={r:.3e}")
    out["convergence_max_pos_diff_rtol_1e10_vs_1e12"] = conv
    out["seconds"] = round(time.time() - t0c, 1)
    with open("probe-out.json", "w") as f:
        json.dump(out, f, indent=1)
    print(f"convergence (rtol 1e-10 vs 1e-12, nr): {conv:.3e}")
    print(f"total {out['seconds']} s")


if __name__ == "__main__":
    main()
