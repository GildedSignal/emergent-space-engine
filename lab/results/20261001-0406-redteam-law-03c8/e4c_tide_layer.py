#!/usr/bin/env python3
"""E4c: premise-2 probe, faithful layer. Truth = full problem (DOP853, parent
rotating continuously). Law layer = the law's actual mechanism: per radial
period, integrate the FIRST-ORDER work/torque of the true instantaneous tide
along the unperturbed Kepler cycle (the orbit average), apply as a kick to
(E, L), re-derive the next cycle from (E, L) — i.e. kicks.rs `integrate_arc`
+ `apply`, in float.

Usage: python3 e4c_tide_layer.py [case-indices]
"""
import sys
import numpy as np
from scipy.integrate import solve_ivp

MU = 1e-3
RH = (MU / 3.0) ** (1.0 / 3.0)
TAU0 = 0.08

def accel(x, d):
    r = np.hypot(x[0], x[1])
    a = -MU * x / r**3
    xd = x + d
    rd = np.hypot(xd[0], xd[1])
    dd = np.hypot(d[0], d[1])
    return a - (xd / rd**3 - d / dd**3)

def rhs_truth(t, y):
    a = accel(y[:2], np.array([np.cos(t), np.sin(t)]))
    return np.array([y[2], y[3], a[0], a[1]])

def initial_state(a0, e0, E0=0.25):
    b0 = a0 * np.sqrt(1 - e0**2)
    n0 = np.sqrt(MU / a0**3)
    f = n0 / (1 - e0 * np.cos(E0))
    return np.array([a0 * (np.cos(E0) - e0), b0 * np.sin(E0),
                     -a0 * np.sin(E0) * f, b0 * np.cos(E0) * f])

def kepler_state(a, e, E):
    b = a * np.sqrt(1 - e * e)
    n = np.sqrt(MU / a**3)
    f = n / (1 - e * np.cos(E))
    return (np.array([a * (np.cos(E) - e), b * np.sin(E)]),
            np.array([-a * np.sin(E) * f, b * np.cos(E) * f]))

def orbit_average_kick(a, e, t_peri, panels=512):
    """First-order orbit-averaged (dE, dL) over one full radial period from
    periapsis t_peri, with the parent's TRUE rotating direction (midpoint
    panels in eccentric anomaly, as kicks.rs integrate_arc does in time)."""
    n = np.sqrt(MU / a**3)
    Es = (np.arange(panels) + 0.5) * (2 * np.pi / panels)
    dE_int = 0.0
    dL_int = 0.0
    for E in Es:
        x, v = kepler_state(a, e, E)
        t = t_peri + (E - e * np.sin(E)) / n
        d = np.array([np.cos(t), np.sin(t)])
        ac = accel(x, d) + MU * x / np.hypot(x[0], x[1])**3  # tide only
        dt = (1 - e * np.cos(E)) / n * (2 * np.pi / panels)
        dE_int += (v @ ac) * dt
        dL_int += (x[0] * ac[1] - x[1] * ac[0]) * dt
    return dE_int, dL_int

def run_case(name, apo_over_rh, e0, n_parent_orbits):
    a0 = apo_over_rh * RH / (1 + e0)
    y0 = initial_state(a0, e0)
    tend = 2 * np.pi * n_parent_orbits
    tau = (2.0 / 3.0) * apo_over_rh**3

    ev = lambda t, y, *u: (y[0] * y[2] + y[1] * y[3])
    ev.direction = 1.0
    sol = solve_ivp(rhs_truth, (0, tend), y0, method="DOP853", rtol=1e-12,
                    atol=1e-14, events=[ev], max_step=0.05)
    S = []
    for y in list(sol.y_events[0]) + [sol.y[:, -1]]:
        r = np.hypot(y[0], y[1]); v2 = y[2]**2 + y[3]**2
        eps = v2 / 2 - MU / r
        aa = -MU / (2 * eps)
        ee = np.sqrt(max(0.0, 1 + 2 * eps * (y[0]*y[3]-y[1]*y[2])**2 / MU**2))
        S.append((aa / RH, ee))
    S = np.array(S)
    rr = np.array([np.hypot(y[0], y[1]) for y in sol.y_events[0]])
    esc = sol.t_events[0][np.argmax(rr > 2 * RH)] / 2 / np.pi if (rr > 2 * RH).any() else None

    # law layer: (E, L) kicks once per radial period
    a, e = a0, e0
    t = 0.0
    M = [(a / RH, e)]
    while t < tend:
        E_k = -MU / (2 * a)
        L_k = np.sqrt(MU * a * (1 - e * e))
        dE, dL = orbit_average_kick(a, e, t)
        E_k += dE; L_k = abs(L_k + dL)
        if E_k >= 0 or L_k == 0:
            M.append((np.nan, np.nan)); break
        a = -MU / (2 * E_k)
        e = np.sqrt(max(0.0, 1 + 2 * E_k * L_k**2 / MU**2))
        if e >= 1:
            M.append((a / RH, e)); break
        t += 2 * np.pi * np.sqrt(a**3 / MU)
        M.append((a / RH, e))
    M = np.array(M)

    n = min(len(S), len(M))
    de = np.abs(S[:n, 1] - M[:n, 1])
    print(f"{name:22s} tau_apo={tau:.4f}{'>=' if tau >= TAU0 else '<'}tau0 "
          f"truth:{'ESCAPED t/t_p=' + f'{esc:.0f}' if esc else 'bound':>14s}"
          f"  layer:{'ESCAPED' if np.isnan(M[-1,1]) or M[-1,1] >= 1 or M[-1,0]*(1+M[-1,1]) > 2 else 'bound':>8s}"
          f"  peris T/L={len(S)-1}/{len(M)-1}")
    print(f"{'':22s} max|de|={np.nanmax(de):.4f}  e_end T/L={S[-1,1]:.4f}/{M[-1,1]:.4f}"
          f"  apo_end T/L={S[-1,0]*(1+S[-1,1]):.3f}/{np.nan_to_num(M[-1,0])*(1+np.nan_to_num(M[-1,1])):.3f} R_H")

CASES = [
    ("boundary .49 e.05", 0.49, 0.05, 250),
    ("in-regime .45 e.05", 0.45, 0.05, 250),
    ("held-out .42 e.10", 0.42, 0.10, 250),
    ("held-out .30 e.05", 0.30, 0.05, 250),
    ("context .60 e.10", 0.60, 0.10, 150),
]

if __name__ == "__main__":
    print(f"R_H = {RH:.6f} a;  tau0 = {TAU0} <-> r = {(3*TAU0/2)**(1/3):.4f} R_H")
    sel = [int(a) for a in sys.argv[1:]] or list(range(len(CASES)))
    for i in sel:
        run_case(*CASES[i])
