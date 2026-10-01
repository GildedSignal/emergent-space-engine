#!/usr/bin/env python3
"""E4 (fixed): premise-2 probe. Truth = full problem (parent direction rotates
continuously; doll on circular orbit; GM_p=1 fixed, mu_doll=1e-3 — the Hill
limit's finite-distance version). Law layer = parent direction frozen at each
periapsis for one radial period ("orbit-averaged kick"; generous: continuous
full nonlinear tide, not an impulse). Axes inertial, origin at the doll.

tau(r_apo) = (2/3)(r_apo/R_H)^3, tau0 = 0.08 (kicks.rs: 2/25).
Usage: python3 e4b_tide_regime.py <case-index>   (each case <= 60 s)
"""
import sys
import numpy as np
from scipy.integrate import solve_ivp

MU = 1e-3
RH = (MU / 3.0) ** (1.0 / 3.0)
TAU0 = 0.08
NUDGE = 1e-7

def accel(x, d):
    r = np.hypot(x[0], x[1])
    a = -MU * x / r**3
    xd = x + d
    rd = np.hypot(xd[0], xd[1])
    dd = np.hypot(d[0], d[1])
    return a - (xd / rd**3 - d / dd**3)

def peri_event(t, y, *unused):
    return y[0] * y[2] + y[1] * y[3]
peri_event.direction = 1.0
peri_event.terminal = True

def rhs_truth(t, y):
    a = accel(y[:2], np.array([np.cos(t), np.sin(t)]))
    return np.array([y[2], y[3], a[0], a[1]])

def rhs_model(t, y, d):
    a = accel(y[:2], d)
    return np.array([y[2], y[3], a[0], a[1]])

def initial_state(a0, e0, E0=0.25):
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

def jacobi_hill(t, y):
    """Conserved quantity of this exact setup, in the rotating frame."""
    c, s = np.cos(t), np.sin(t)
    xr = c * y[0] + s * y[1]; yr = -s * y[0] + c * y[1]
    vxr = c * y[2] + s * y[3]; vyr = -s * y[2] + c * y[3]
    q = np.hypot(xr, yr)
    qp = np.hypot(xr + 1.0, yr)
    return vxr**2 + vyr**2 + 2 * MU / q + 2.0 / qp - (xr**2 + yr**2)

def run_case(name, apo_over_rh, e0, n_parent_orbits):
    a0 = apo_over_rh * RH / (1 + e0)
    y0 = initial_state(a0, e0)
    tend = 2 * np.pi * n_parent_orbits
    tau = (2.0 / 3.0) * apo_over_rh**3

    # truth
    ev = lambda t, y, *u: (y[0] * y[2] + y[1] * y[3])
    ev.direction = 1.0
    sol = solve_ivp(rhs_truth, (0, tend), y0, method="DOP853", rtol=1e-12,
                    atol=1e-14, events=[ev], max_step=0.05)
    pts = list(sol.y_events[0]) + [sol.y[:, -1]]
    S = np.array([elements(y) for y in pts])
    rr = np.array([np.hypot(y[0], y[1]) for y in pts])
    esc_t = sol.t_events[0][np.argmax(rr[:-1] > 2 * RH)] if (rr[:-1] > 2 * RH).any() else None
    dJ = abs(jacobi_hill(tend, sol.y[:, -1]) - jacobi_hill(0, y0))

    # model: frozen parent direction per radial period (nudge past each root)
    y = y0.copy(); t = 0.0
    mpts = [y.copy()]
    guard = 0
    while t < tend and guard < 6000:
        guard += 1
        d = np.array([np.cos(t), np.sin(t)])
        seg = solve_ivp(rhs_model, (t, tend + 1.0), y, args=(d,), method="DOP853",
                        rtol=1e-12, atol=1e-14, events=[peri_event], max_step=0.05)
        hits = seg.t_events[0]
        if len(hits) and hits[0] > t + 1e-9:
            y = seg.y_events[0][0]; t = hits[0]
            mini = solve_ivp(rhs_model, (t, t + NUDGE), y, args=(d,), method="DOP853",
                             rtol=1e-12, atol=1e-14)
            y = mini.y[:, -1]; t = t + NUDGE
        else:
            y = seg.y[:, -1]; t = tend + 1.0
        mpts.append(y.copy())
        if not np.all(np.isfinite(y)):
            break
    M = np.array([elements(y) for y in mpts])
    mr = np.array([np.hypot(y[0], y[1]) for y in mpts])
    m_esc = (mr > 2 * RH).any()

    n = min(len(S), len(M))
    de = np.abs(S[:n, 1] - M[:n, 1])
    print(f"{name:24s} tau_apo={tau:.4f}{'>=' if tau >= TAU0 else '<'}tau0  "
          f"J-drift={dJ:.1e}  truth: {'ESCAPED doll' if esc_t else 'bound'}"
          f"{' t/t_p=' + f'{esc_t/2/np.pi:.0f}' if esc_t else ''}  "
          f"model: {'ESCAPED' if m_esc else 'bound'}")
    print(f"{'':24s} periapses T/M={len(S)-1}/{len(mpts)-1}  max|de|={np.nanmax(de[:min(n, max(len(S),1))]):.4f}"
          f"  e_end T/M={S[-1,1]:.4f}/{M[-1,1]:.4f}  apo_end T/M={S[-1,0]*(1+S[-1,1]):.3f}/{M[-1,0]*(1+M[-1,1]):.3f} R_H")

CASES = [
    ("boundary apo .49 e .05", 0.49, 0.05, 250),
    ("in-regime apo .45 e .05", 0.45, 0.05, 250),
    ("held-out apo .42 e .10", 0.42, 0.10, 250),
    ("held-out apo .30 e .05", 0.30, 0.05, 250),
    ("context apo .60 e .10", 0.60, 0.10, 150),
]

if __name__ == "__main__":
    print(f"R_H = {RH:.6f} a;  tau0 = {TAU0} <-> r = {(3*TAU0/2)**(1/3):.4f} R_H")
    sel = [int(a) for a in sys.argv[1:]] or range(len(CASES))
    for i in sel:
        run_case(*CASES[i])
