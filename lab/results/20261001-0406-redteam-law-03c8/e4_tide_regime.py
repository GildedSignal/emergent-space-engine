#!/usr/bin/env python3
"""E4: premise-2 probe. Truth = full circular restricted three-body (parent's
direction rotates continuously). Law layer = the parent's direction frozen at
each periapsis for one full radial period ("orbit-averaged kick"; generous:
continuous full nonlinear tide, not an impulse). Axes inertial, origin at doll.

Doll on circular orbit a=1, GM_parent=1, mu_doll=1e-3, n_p=1.
tau(r_apo) = (2/3)(r_apo/R_H)^3, tau0 = 0.08 (kicks.rs: 2/25).
"""
import numpy as np
from scipy.integrate import solve_ivp

MU = 1e-3          # doll mass (parent mass = 1)
RH = (MU / 3.0) ** (1.0 / 3.0)
TAU0 = 0.08

def accel(x, d):
    """Full dynamics: doll point mass + exact differential parent force."""
    r = np.hypot(x[0], x[1])
    a = -MU * x / r**3
    xd = x + d                      # moon position relative to parent
    rd = np.hypot(xd[0], xd[1])
    dd = np.hypot(d[0], d[1])
    a = a - (xd / rd**3 - d / dd**3)  # parent pull minus origin pull (GM_p=1)
    return a

def peri_event(t, y, *unused):
    return y[0] * y[2] + y[1] * y[3]
peri_event.direction = 1.0   # inbound -> outbound crossing = periapsis
peri_event.terminal = True

def rhs_truth(t, y):
    d = np.array([np.cos(t), np.sin(t)])
    a = accel(y[:2], d)
    return np.array([y[2], y[3], a[0], a[1]])

def rhs_model(t, y, d):
    a = accel(y[:2], d)
    return np.array([y[2], y[3], a[0], a[1]])

def initial_state(a0, e0, E0=0.25):
    """State at eccentric anomaly E0 (off the turning points, so the periapsis
    event never fires at t0)."""
    b0 = a0 * np.sqrt(1 - e0**2)
    n0 = np.sqrt(MU / a0**3)
    f = n0 / (1 - e0 * np.cos(E0))
    x = np.array([a0 * (np.cos(E0) - e0), b0 * np.sin(E0)])
    v = np.array([-a0 * np.sin(E0) * f, b0 * np.cos(E0) * f])
    return np.array([x[0], x[1], v[0], v[1]])

def elements(y):
    r = np.hypot(y[0], y[1])
    v2 = y[2] ** 2 + y[3] ** 2
    eps = v2 / 2 - MU / r
    a = -MU / (2 * eps)
    e = np.sqrt(max(0.0, 1 + 2 * eps * (y[0] * y[3] - y[1] * y[2]) ** 2 / MU**2))
    return a / RH, e

def run_case(name, apo_over_rh, e0, n_parent_orbits):
    a0 = apo_over_rh * RH / (1 + e0)
    y0 = initial_state(a0, e0)
    tend = 2 * np.pi * n_parent_orbits
    tau = (2.0 / 3.0) * apo_over_rh**3

    # truth: non-terminal periapsis sampling
    ev = lambda t, y, *u: (y[0] * y[2] + y[1] * y[3])
    ev.direction = 1.0
    sol = solve_ivp(rhs_truth, (0, tend), y0, method="DOP853", rtol=1e-12,
                    atol=1e-14, events=[ev], max_step=0.05)
    pts = list(sol.y_events[0]) + [sol.y[:, -1]]

    # model: parent direction frozen at each periapsis, one radial period each
    y = y0.copy(); t = 0.0
    mpts = [y.copy()]
    guard = 0
    while t < tend and guard < 20000:
        guard += 1
        d = np.array([np.cos(t), np.sin(t)])
        seg = solve_ivp(rhs_model, (t, tend + 1.0), y, args=(d,), method="DOP853",
                        rtol=1e-12, atol=1e-14, events=[peri_event], max_step=0.05)
        hits = seg.t_events[0]
        if len(hits):
            y = seg.y_events[0][0]; t = hits[0]
        else:
            y = seg.y[:, -1]; t = tend + 1.0
        mpts.append(y.copy())
        if not np.all(np.isfinite(y)):
            break

    def series(pts):
        return np.array([elements(y) if np.all(np.isfinite(y)) else (np.nan, np.nan)
                         for y in pts])

    S, M = series(pts), series(mpts)
    n = min(len(S), len(M))
    de = np.abs(S[:n, 1] - M[:n, 1])
    da = np.abs(S[:n, 0] - M[:n, 0])
    print(f"{name:26s} tau_apo={tau:.4f}{'>=' if tau>=TAU0 else '<'}tau0 "
          f"orbits T/M={len(S)-1}/{len(mpts)-1}  max|de|={np.nanmax(de):.4f} "
          f"maxda={np.nanmax(da):.4f}/RH  e_end T/M={S[n-1,1]:.4f}/{M[n-1,1]:.4f}")
    return S, M

if __name__ == "__main__":
    print(f"R_H = {RH:.6f} a;  tau0 = {TAU0}  <->  r = {(3*TAU0/2)**(1/3):.4f} R_H")
    run_case("in-regime apo .49 e .05", 0.49, 0.05, 300)
    run_case("in-regime apo .45 e .05", 0.45, 0.05, 300)
    run_case("held-out  apo .42 e .10", 0.42, 0.10, 300)
    run_case("held-out  apo .30 e .05", 0.30, 0.05, 300)
    run_case("context  apo .60 e .10 (escalates)", 0.60, 0.10, 200)
