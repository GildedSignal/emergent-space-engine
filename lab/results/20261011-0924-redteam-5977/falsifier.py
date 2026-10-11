#!/usr/bin/env python3
"""Red-team falsifier: the view gather's past light cone (premise 5) and the
1PN doll truncation (premise 1 proxy), against float64 Schwarzschild geodesics.

Truth: photon Binet u'' = 3u^2 - u (M=1), travel time dt/dphi along the null
geodesic. Design letter: flat past cone (coordinate chord) + memo deflection(b)
~ 4M/b for direction only.
"""
import json, math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

M = 1.0

def scan_arrival(r_s, r_o, Phi):
    """One stacked integration over 121 candidate initial slopes; returns
    (slopes, u_end, u_min, b) arrays."""
    us = 1.0 / r_s
    g = np.linspace(-6.0, 6.0, 121)
    up0 = us * g
    inv_b2 = up0 * up0 + us * us - 2 * us ** 3
    ok = inv_b2 > 0
    b = np.full_like(up0, np.nan)
    b[ok] = 1.0 / np.sqrt(inv_b2[ok])
    y0 = np.concatenate([np.full_like(up0, us), up0, np.zeros_like(up0),
                         np.zeros_like(up0)])  # u, u', t, capture-min-u
    n = len(up0)
    bb = np.where(ok, b, 1e9)
    def rhs(phi, y):
        u, up, t, _ = y[:n], y[n:2 * n], y[2 * n:3 * n], y[3 * n:]
        udd = np.where(u < 1e-9, -1.0, 3 * u * u - u)  # no fake bounce below 0
        f = np.where(ok, np.sqrt(np.maximum(1e-30, 1.0 / bb ** 2 - u * u + 2 * u ** 3))
                     / ((1 - 2 * u) * bb * u * u), 0.0)
        return np.concatenate([up, udd, f, np.zeros(n)])
    sol = solve_ivp(rhs, [0, Phi], y0, rtol=1e-10, atol=1e-12, max_step=0.1)
    u_end = sol.y[0:n, -1]
    u_min = sol.y[0:n, :].min(axis=1)
    t_end = sol.y[2 * n:3 * n, -1]
    return up0, u_end, u_min, b, t_end, sol

def trace_u(r_s, Phi, up0):
    """u-only integration with terminal events: returns (u_end, status)
    status: 'ok', 'escape' (u<1e-6), 'capture' (u>1/3)."""
    us = 1.0 / r_s
    inv_b2 = up0 * up0 + us * us - 2 * us ** 3
    if inv_b2 <= 0:
        return -1.0, "escape"
    def rhs(phi, y):
        u, up = y
        return [up, 3 * u * u - u]
    esc = lambda phi, y: y[0] - 1e-6
    cap = lambda phi, y: y[0] - 1.0 / 3.0
    esc.terminal = True
    cap.terminal = True
    sol = solve_ivp(rhs, [0, Phi], [us, up0], rtol=1e-11, atol=1e-13,
                    max_step=0.05, events=(esc, cap))
    if len(sol.t_events[0]):
        return -1.0, "escape"
    if len(sol.t_events[1]):
        return 2.0, "capture"
    return sol.y[0][-1], "ok"

def trace_time(r_s, r_o, Phi, up0):
    """Full integration with time, for a slope already known to land."""
    us = 1.0 / r_s
    b = 1.0 / math.sqrt(up0 * up0 + us * us - 2 * us ** 3)
    def rhs(phi, y):
        u, up, t = y
        return [up, 3 * u * u - u, 1.0 / ((1 - 2 * u) * b * u * u)]
    sol = solve_ivp(rhs, [0, Phi], [us, up0, 0.0], rtol=1e-11, atol=1e-13,
                    max_step=0.05)
    return sol.y[0][-1], sol.y[2][-1], sol.y[0].min(), b
def apparent(r_s, r_o, Phi):
    us, uo = 1.0 / r_s, 1.0 / r_o
    up0 = us * np.linspace(-6.0, 6.0, 121)
    f_end = np.array([trace_u(r_s, Phi, u)[0] - uo for u in up0])
    roots = []
    for i in np.where(np.isfinite(f_end[:-1]) & np.isfinite(f_end[1:])
                      & (f_end[:-1] * f_end[1:] < 0))[0]:
        try:
            g = lambda u: trace_u(r_s, Phi, u)[0] - uo
            root = brentq(g, up0[i], up0[i + 1], xtol=1e-13, rtol=8.9e-16)
            ue0, status = trace_u(r_s, Phi, root)
            if status != "ok" or abs(ue0 - uo) > 1e-6:
                continue
            ue, t, um, bb = trace_time(r_s, r_o, Phi, root)
            if um < 1.0 / 3.1:
                roots.append((root, ue, t, um, bb))
        except Exception:
            pass
    if not roots:
        return None
    _, ue, t_true, um, b_true = max(roots, key=lambda rr: rr[4])
    psi_true = math.asin(min(1.0, b_true * uo * math.sqrt(1 - 2 * uo)))
    chord = math.sqrt(r_s ** 2 + r_o ** 2 - 2 * r_s * r_o * math.cos(Phi))
    psi_flat = math.atan2(r_s * math.sin(Phi), r_o - r_s * math.cos(Phi))
    b_flat = r_s * r_o * math.sin(Phi) / chord
    psi_design = psi_flat + 4 * M / b_flat if b_flat > 1e-12 else psi_flat
    return dict(Phi=Phi, b=b_true, b_flat=b_flat, t_true=t_true, t_flat=chord,
                psi_true=psi_true, psi_design=psi_design, psi_flat=psi_flat)

def massive_advance(p, e):
    L2, u_peri = p, (1 + e) / p
    def rhs(phi, y):
        u, up = y
        return [up, 1.0 / L2 + 3 * u * u - u]
    sol = solve_ivp(rhs, [0, 4 * math.pi], [u_peri, 0.0], rtol=1e-12, atol=1e-14,
                    max_step=0.02)
    up = sol.y[1]
    zero = np.where(up[:-1] * up[1:] < 0)[0]
    if len(zero) < 2:
        return None
    def cross(i):
        ph, y = sol.t[i:i + 2], up[i:i + 2]
        return ph[0] - y[0] * (ph[1] - ph[0]) / (y[1] - y[0])
    # phi=0 is the starting periapsis (u'(0)=0); zero[0]=apoapsis, zero[1]=next periapsis
    return cross(zero[1]) - 2 * math.pi

def deflection_control():
    b, us = 100.0, 0.001
    up0 = math.sqrt(1 / b ** 2 - us ** 2 + 2 * us ** 3)
    def rhs(phi, y):
        u, up = y
        return [up, 3 * u * u - u]
    sol = solve_ivp(rhs, [0, math.pi + 0.05], [us, up0], rtol=1e-12, atol=1e-14,
                    max_step=0.02)
    u = sol.y[0]
    i2 = np.where((u <= us) & (np.arange(len(u)) > 10))[0][0]
    phi_land = brentq(lambda x: float(np.interp(x, sol.t[:i2 + 1], u[:i2 + 1])) - us,
                      sol.t[i2 - 1], sol.t[i2])
    return phi_land - (math.pi - 2 * math.asin(b * us)), 4 / b + 15 * math.pi / 4 / b ** 2

def main():
    out = {}
    defl, defl_pred = deflection_control()
    out["control_deflection"] = dict(measured=defl, predicted=defl_pred,
                                     rel_err=abs(defl - defl_pred) / defl_pred)
    print(f"[control] deflection b=100: {defl:.6f} vs {defl_pred:.6f} "
          f"(rel {out['control_deflection']['rel_err']:.3%})", flush=True)

    for tag, (rs, ro, Om) in dict(near=(12.0, 50.0, math.sqrt(1 / 12 ** 3)),
                                  far=(1000.0, 2000.0, math.sqrt(1 / 1000 ** 3))).items():
        rows = []
        for Phi in np.linspace(0.3, 2.7, 13):
            r = apparent(rs, ro, Phi)
            if r is None:
                continue
            r["dt"] = r["t_true"] - r["t_flat"]
            r["phase_err_deg"] = math.degrees(Om * r["dt"])
            r["dir_resid_deg"] = math.degrees(abs(r["psi_true"] - r["psi_design"]))
            r["dir_no_memo_deg"] = math.degrees(abs(r["psi_true"] - r["psi_flat"]))
            rows.append(r)
            print(f"  [{tag}] Phi={Phi:.2f} b={r['b']:.1f} dt={r['dt']:.2f}M "
                  f"phase_err={r['phase_err_deg']:.2f}deg dir_resid={r['dir_resid_deg']:.3f}deg",
                  flush=True)
        out[tag] = rows
        ph = [r["phase_err_deg"] for r in rows]
        dr = [r["dir_resid_deg"] for r in rows]
        print(f"[{tag}] n={len(rows)}: phase_err median {np.median(ph):.2f} max {np.max(ph):.2f} deg "
              f"| dir resid median {np.median(dr):.3f} max {np.max(dr):.3f} deg", flush=True)

    adv = {}
    for p in (12, 25, 50, 100, 300):
        circ = 2 * math.pi * (1 / math.sqrt(1 - 6.0 / p) - 1)
        adv[f"p{p}_circ"] = dict(exact=circ, pn1=6 * math.pi / p,
                                 gap=(circ - 6 * math.pi / p) / circ,
                                 b11_allow=0.01 + 16.0 / p)
        for e in (0.3, 0.6):
            a = massive_advance(p, e)
            if a is not None:
                adv[f"p{p}_e{e}"] = dict(exact=a, pn1=6 * math.pi / p,
                                         gap=(a - 6 * math.pi / p) / a,
                                         b11_allow=0.01 + 16.0 / p)
    out["advance"] = adv
    for k, v in adv.items():
        print(f"[advance] {k}: exact {v['exact']:.4f} 1PN {v['pn1']:.4f} "
              f"gap {v['gap']:.1%} B11 allowance {v['b11_allow']:.0%}")
    with open("falsifier-results.json", "w") as f:
        json.dump(out, f, indent=1)
    print("saved falsifier-results.json")

if __name__ == "__main__":
    main()
