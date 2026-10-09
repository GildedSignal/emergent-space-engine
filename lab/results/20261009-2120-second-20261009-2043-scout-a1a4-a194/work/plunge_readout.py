#!/usr/bin/env python3
"""Honest tube readout: bracket + Newton-in-psi (P4's predicted mechanism) vs the
shipped linear interpolation. The first run timed 3.08 us/sample on a linear readout
whose accuracy is ~1e-6; P4 predicted bracket+Newton < 20 us. This script measures
BOTH mechanisms: timing AND accuracy vs the independent backward-from-horizon DOP853
oracle, across a winding sweep |1-L/Lc| = 1e-3..1e-7 (the checker's named experiment)
plus the dossier's cases A-G.

Readout contract (massive): given proper time tau, return (u, Phi_total, V_total).
Bracket: bisect the Tau table. Newton in psi on the panel: T_j + GL4_[psi_j,psi]
(dtau/dpsi) - tau = 0, exact analytic derivative, safeguarded to the panel, 3 (or 4)
iterations from a linear start. u is then exact in psi; Phi, V from one local GL4
each. Photon: same with Phi as the clock.

The floor: the tube's own edge values vs the same oracle (what plunge_falsifier
measured: 1e-13..1.3e-10 away from critical). An honest readout should sit at that
floor, not above it; the linear readout should sit above it and degrade with winding.
"""
import json
import math
import time
from bisect import bisect_right

import numpy as np

from plunge_falsifier import make_tube, oracle_massive, oracle_photon, Lcrit, relerr

GX = (-0.8611363115940526, -0.3399810435848563, 0.3399810435848563, 0.8611363115940526)
GW = (0.3478548451374538, 0.6521451548625461, 0.6521451548625461, 0.3478548451374538)


def make_reader(tube, iters=3):
    """Return read(tau)->(u, phi_or_None, v) using bracket + Newton-in-psi."""
    psis = [float(x) for x in tube["psi"]]
    n_pan = len(psis) - 1
    u1 = tube["u1"]; rho = tube["rho"]; a = tube["a"]; bb = tube["bb"]
    L = tube["L"]; E = tube["E"]
    photon = tube["b"] is not None
    s2r = math.sqrt(2.0 * rho)
    gx0, gx1, gx2, gx3 = GX
    gw0, gw1, gw2, gw3 = GW

    def gl4(f, x0, x1):
        m = 0.5 * (x0 + x1); h = 0.5 * (x1 - x0)
        return h * (gw0 * f(m + h * gx0) + gw1 * f(m + h * gx1)
                    + gw2 * f(m + h * gx2) + gw3 * f(m + h * gx3))
    if photon:
        b = tube["b"]
        clock = [float(x) for x in tube["Phi"]]
        Vs = [float(x) for x in tube["V"]]

        def dclk(p):
            u = u1 + rho * math.sin(p) ** 2
            return s2r * math.cos(p) / math.sqrt((u - a) * (u - a) + bb * bb)

        def dv(p):
            s = math.sin(p); u = u1 + rho * s * s
            Q = (u - a) * (u - a) + bb * bb
            sqF = math.sqrt(2.0 * (u - u1) * Q)
            return b / (1.0 + b * sqF) * s2r * math.cos(p) / math.sqrt(Q)

    else:
        clock = [float(x) for x in tube["Tau"]]
        Phis = [float(x) for x in tube["Phi"]]
        Vs = [float(x) for x in tube["V"]]
        if L == 0.0:
            def dclk(p):
                u = u1 + rho * math.sin(p) ** 2
                return s2r * math.cos(p) / (u * u)

            def dphi(p):
                return 0.0

            def dv(p):
                u = u1 + rho * math.sin(p) ** 2
                return (1.0 / (E + math.sqrt(2.0 * (u - u1)))) * s2r * math.cos(p) / (u * u)
        else:
            def dclk(p):
                s = math.sin(p); u = u1 + rho * s * s
                return s2r / L * math.cos(p) / (u * u * math.sqrt((u - a) * (u - a) + bb * bb))

            def dphi(p):
                u = u1 + rho * math.sin(p) ** 2
                return s2r * math.cos(p) / math.sqrt((u - a) * (u - a) + bb * bb)

            def dv(p):
                s = math.sin(p); u = u1 + rho * s * s
                Q = (u - a) * (u - a) + bb * bb
                dt = s2r / L * math.cos(p) / (u * u * math.sqrt(Q))
                return (1.0 + L * L * u * u) / (E + L * math.sqrt(2.0 * (u - u1) * Q)) * dt

    def invert(t):
        j = bisect_right(clock, t) - 1
        if j < 0:
            j = 0
        elif j >= n_pan:
            j = n_pan - 1
        p0 = psis[j]; p1 = psis[j + 1]
        T0 = clock[j]; T1 = clock[j + 1]
        p = p0 + (t - T0) / (T1 - T0) * (p1 - p0)
        if not p0 < p < p1:
            p = 0.5 * (p0 + p1)
        for _ in range(iters):
            f = T0 + gl4(dclk, p0, p) - t
            p -= f / dclk(p)
            if p < p0:
                p = p0
            elif p > p1:
                p = p1
        return j, p

    def read(t):
        j, p = invert(t)
        u = u1 + rho * math.sin(p) * math.sin(p)
        phi = None if photon else Phis[j] + gl4(dphi, psis[j], p)
        v = Vs[j] + gl4(dv, psis[j], p)
        return u, phi, v

    return read


def make_linear(tube):
    """The shipped readout (plunge_cost.py): panel index + linear interp of u."""
    tau_np = tube["Tau"]; u_np = tube["u"]

    def read_linear(t):
        j = np.searchsorted(tau_np, t) - 1
        w = (t - tau_np[j]) / (tau_np[j + 1] - tau_np[j])
        return u_np[j] + w * (u_np[j + 1] - u_np[j])
    return read_linear


def time_us(fn, targets, reps=5):
    ts = []
    for _ in range(reps):
        t0 = time.perf_counter()
        for x in targets:
            fn(x)
        ts.append((time.perf_counter() - t0) / len(targets) * 1e6)
    return sorted(ts)[reps // 2]


def run_massive(name, E, L, n_targets=512):
    tube = make_tube(E, L, n_panels=512)
    Tau = tube["Tau"]
    rng = np.random.default_rng(0)
    targets = rng.uniform(Tau[1], Tau[-2], n_targets)
    u_o, phi_o, v_o, ok = oracle_massive(E, L, targets, tube)

    # floor: the tube's own edge values vs the same oracle (falsifier's measurement),
    # 128 edge targets so the floor's max is not undersampled
    idx = np.linspace(1, 511, 128).astype(int)
    tau_e = Tau[idx]
    ue, phie, ve, _ = oracle_massive(E, L, tau_e, tube)
    fl = dict(
        r=float(relerr(1.0 / tube["u"][idx], 1.0 / ue).max()),
        phi=float(relerr(tube["Phi"][idx], tube["Phi"][-1] + phie).max()),
        v=float(relerr(tube["V"][idx], tube["V"][-1] + ve).max()))

    lin = make_linear(tube)
    u_lin = np.array([lin(t) for t in targets])
    e_lin = float(relerr(1.0 / u_lin, 1.0 / u_o).max())

    read3 = make_reader(tube, iters=3)
    read4 = make_reader(tube, iters=4)
    read5 = make_reader(tube, iters=5)
    out3 = [read3(t) for t in targets]
    out4 = [read4(t) for t in targets]
    out5 = [read5(t) for t in targets]
    u3 = np.array([o[0] for o in out3])
    phi3 = np.array([o[1] for o in out3])
    v3 = np.array([o[2] for o in out3])
    e3 = dict(
        r=float(relerr(1.0 / u3, 1.0 / u_o).max()),
        phi=float(relerr(phi3, tube["Phi"][-1] + phi_o).max()),
        v=float(relerr(v3, tube["V"][-1] + v_o).max()))
    # convergence: does 3 iterations agree with 5 (and 4) to machine level?
    conv35 = float(np.max(np.abs(u3 - np.array([o[0] for o in out5]))))
    conv45 = float(np.max(np.abs(np.array([o[0] for o in out4]) - np.array([o[0] for o in out5]))))

    t_lin = time_us(lin, targets)
    t_new3 = time_us(read3, targets)
    t_new4 = time_us(read4, targets)

    res = dict(case=name, E=E, L=L, winding=float(tube["Phi"][-1]),
               floor=fl, lin=dict(u=e_lin, us=t_lin),
               newton3=dict(e3=e3, us=t_new3, conv35=conv35, conv45=conv45),
               newton4_us=t_new4)
    at_floor = (e3["r"] <= 5 * max(fl["r"], 1e-14) and e3["phi"] <= 5 * max(fl["phi"], 1e-14)
                and e3["v"] <= 5 * max(fl["v"], 1e-14))
    res["at_floor_5x"] = bool(at_floor)
    res["cost_under_20us"] = bool(t_new3 < 20.0)
    print(f"{name:16s} dPhi={res['winding']:8.3f} | floor r/phi/v {fl['r']:.1e}/{fl['phi']:.1e}/{fl['v']:.1e}"
          f" | lin_u {e_lin:.1e} | newton r/phi/v {e3['r']:.1e}/{e3['phi']:.1e}/{e3['v']:.1e}"
          f" | {t_lin:5.2f}/{t_new3:5.2f}/{t_new4:5.2f} us (lin/N3/N4)"
          f" | conv35 {conv35:.1e} | floor5x={at_floor} <20us={t_new3 < 20.0}")
    return res


def run_photon(name, b, n_targets=512):
    tube = make_tube(0, 0, photon_b=b)
    Phi = tube["Phi"]
    rng = np.random.default_rng(0)
    targets = rng.uniform(Phi[1], Phi[-2], n_targets)
    u_o, v_o = oracle_photon(b, targets, tube)

    idx = np.linspace(1, 511, 32).astype(int)
    phi_e = Phi[idx]
    ue, ve = oracle_photon(b, phi_e, tube)
    fl = dict(r=float(relerr(1.0 / tube["u"][idx], 1.0 / ue).max()),
              v=float(relerr(tube["V"][idx], ve).max()))

    read3 = make_reader(tube, iters=3)
    read5 = make_reader(tube, iters=5)
    out3 = [read3(t) for t in targets]
    u3 = np.array([o[0] for o in out3]); v3 = np.array([o[2] for o in out3])
    e3 = dict(r=float(relerr(1.0 / u3, 1.0 / u_o).max()),
              v=float(relerr(v3, v_o).max()))
    conv35 = float(np.max(np.abs(u3 - np.array([o[0] for o in [read5(t) for t in targets]]))))
    t_new3 = time_us(read3, targets)
    at_floor = e3["r"] <= 5 * max(fl["r"], 1e-14) and e3["v"] <= 5 * max(fl["v"], 1e-14)
    res = dict(case=name, b=b, winding=float(Phi[-1]), floor=fl,
               newton3=dict(e3=e3, us=t_new3, conv35=conv35),
               at_floor_5x=bool(at_floor), cost_under_20us=bool(t_new3 < 20.0))
    print(f"{name:16s} dPhi={res['winding']:8.3f} | floor r/v {fl['r']:.1e}/{fl['v']:.1e}"
          f" | newton r/v {e3['r']:.1e}/{e3['v']:.1e} | {t_new3:5.2f} us (N3)"
          f" | conv35 {conv35:.1e} | floor5x={at_floor} <20us={t_new3 < 20.0}")
    return res


def main():
    Lc97 = Lcrit(0.97); Lc12 = Lcrit(1.2); Lc2000 = Lcrit(2000.0); Lc1 = Lcrit(1.0)
    results = {}

    print("== honest readout vs oracle (floors are the tube's own edge errors) ==")
    print(f"{'case':16s} {'':8s}  {'':0s}   {'lin/N3/N4 = us per sample; conv35 = |u(3iter)-u(5iter)|'}")
    for nm, E, L in [("A apoapsis E0.8", 0.8, 3.8),
                     ("B apoapsis E0.97", 0.97, 0.9 * Lc97),
                     ("C direct E1", 1.0, 3.6),
                     ("D direct E1.2", 1.2, 0.99 * Lc12),
                     ("E gamma2000", 2000.0, 0.99 * Lc2000),
                     ("F radial L0", 1.0, 0.0)]:
        results[nm[0]] = run_massive(nm, E, L)
    results["G"] = run_photon("G photon 0.9bc", 0.9 * 3 * np.sqrt(3))

    print("\n== winding sweep, E=1, L = Lc*(1-10^-k) (checker's |1-L/Lc| >= 1e-3) ==")
    sweep = {}
    for k in range(3, 8):
        L = Lc1 * (1.0 - 10.0 ** (-k))
        sweep[k] = run_massive(f"sweep k={k}", 1.0, L)
    results["sweep"] = sweep

    sweep_costs = [r["newton3"]["us"] for r in sweep.values()]
    costs = [r["newton3"]["us"] for r in results.values() if "newton3" in r] + sweep_costs
    floors_ok = all(r["at_floor_5x"] for r in list(results.values()) + list(sweep.values())
                    if "at_floor_5x" in r)
    print(f"\ncost: min {min(costs):.2f}  max {max(costs):.2f} us over all cases"
          f" (incl. L=0 and photon special forms)")
    print(f"winding sweep k=3..7 cost: {min(sweep_costs):.2f}..{max(sweep_costs):.2f} us"
          f" (max/min = {max(sweep_costs)/min(sweep_costs):.3f})"
          f"   winding-independence: {'HOLDS' if max(sweep_costs)/min(sweep_costs) < 1.1 else 'FAILS'}")
    print(f"all cases at table floor (<=5x): {'YES' if floors_ok else 'NO'}")
    print(f"all pure-Python costs < 20 us: {'YES' if max(costs) < 20 else 'NO'}"
          f"   (compiled C form: see plunge_readout_c)")

    with open("readout-output.json", "w") as f:
        json.dump(results, f, indent=1)


if __name__ == "__main__":
    main()
