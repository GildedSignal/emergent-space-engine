#!/usr/bin/env python3
"""Falsifier for docs/representation.md §3: 'A cycle's derivatives are stored with it,
so a kick updates the cycle by a multiply-add.'  Float64, one process, < 60 s.

Parts:
  A  Newtonian doll cycles (closed form): multiply-add vs exact recompile, swept over
     (e, kick size); second-order row; ring-grid crossing contrast.
  B  Chaining: 200 periapsis kicks, fresh-derivative vs chained multiply-add.
  C  GR Binet (numeric, RK via solve_ivp): radial cycle T(L) as L -> L_sep+ at fixed E
     (compact orbit, pure homoclinic dwell), divergence exponent, multiply-add error.
     Harness control: GR term off -> Kepler to 1e-6.

All units: Newtonian q = mu = 1; GR M = 1, geometric.
"""
import json
import math
import sys

import numpy as np
from scipy.integrate import solve_ivp

OUT = {}

# ---------------------------------------------------------------- Part A: Newtonian
# T = 2*pi*mu*(-2E)^{-3/2},  x = dE/|E|,  exact ratio (1+x)^{-3/2}.
def partA():
    rows = []
    es = [0.3, 0.6, 0.9, 0.961, 0.99, 0.999]
    kicks = [  # (label, dv in units of v_p = sqrt(1+e))
        ("belt 2^-23", 2.0 ** -23),
        ("encounter 1e-3", 1e-3),
        ("deep passage 1e-2", 1e-2),
        ("slingshot 0.3", 0.3),
    ]
    for e in es:
        for lab, dv in kicks:
            x = 2.0 * math.sqrt(1 + e) * dv / (1 - e)  # dE/|E| at periapsis tangential
            exact = (1 + x) ** -1.5
            ma = 1 - 1.5 * x
            ma2 = 1 - 1.5 * x + 0.5 * (15 / 4) * x * x  # second derivative stored
            eps1 = abs(ma - exact) / exact
            eps2 = abs(ma2 - exact) / exact
            rows.append(dict(e=e, kick=lab, x=x, eps1=eps1, eps2=eps2,
                             bar1=eps1 > 0.01, bar_r2=eps1 > 2.0 ** -16))
    # H1 confirmation: eps1 matches (15/8)x^2 to <1% rel for x<=0.3
    h1 = []
    for x in [1e-3, 1e-2, 1e-1, 3e-1]:
        exact = (1 + x) ** -1.5
        law = (15 / 8) * x * x
        h1.append(dict(x=x, law=law, true=abs((1 - 1.5 * x) - exact) / exact,
                       relerr=abs(law - abs((1 - 1.5 * x) - exact) / exact) / law))
    # control H2: benign circular-scale kick
    x = 1e-4
    h2 = abs((1 - 1.5 * x) - (1 + x) ** -1.5) / (1 + x) ** -1.5
    # ring-grid crossings per cycle (analytic, log rings, m=16): 2*m*log2(a/q)
    cross = {e: 2 * 16 * math.log2(1 / (1 - e)) for e in es}
    # e* where the 1% bar breaks, per kick size: (1-e) = 2*sqrt(1+e)*dv/0.0730
    estar = {}
    def solve_e(dv, xbar):
        lo, hi = 0.0, 0.999999
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            if 2 * math.sqrt(1 + mid) * dv / (1 - mid) > xbar:
                hi = mid
            else:
                lo = mid
        return round(1 - lo, 6) if (1 - lo) < 0.5 else None
    for lab, dv in kicks:
        estar[lab] = solve_e(dv, 0.0730)
    estar2 = {lab: solve_e(dv, 0.166) for lab, dv in kicks}
    return dict(rows=rows, h1=h1, h2=h2, crossings=cross, estar=estar, estar2=estar2)

# ---------------------------------------------------------------- Part B: chaining
def partB(dv=1e-3, e0=0.95, nmax=200):
    def T_of_E(E):  # mu=1, q=1 fixed family: a = q/(1-e), E = -(1-e)/2
        return 2 * math.pi * (-2 * E) ** -1.5

    def run(chained, seed=None):
        rng = np.random.default_rng(seed)
        e = e0
        E = -(1 - e) / 2.0
        T_rec = T_of_E(E)          # the record's (wrong after kicks) cycle length
        err_t = 0.0                # accumulated schedule error in periapsis-return time
        hist = []
        kicks_done = 0
        for k in range(nmax):
            sgn = 1.0 if seed is None else rng.choice([-1.0, 1.0])
            dE = math.sqrt(1 + e) * (sgn * dv)  # kick at periapsis, v_p = sqrt(1+e)
            E_new = E + dE
            if E_new >= 0 or E_new <= -0.49999:  # unbound / e>=~1 territory reached
                break
            e_new = 1 + 2 * E_new
            # exact cycle after kick
            T_exact = T_of_E(E_new)
            # multiply-add from the current record
            if chained:
                dTdE = 1.5 * T_rec / abs(E)      # derivative of the (wrong) record
                T_ma = T_rec + dTdE * dE
            else:
                dTdE = 1.5 * T_of_E(E) / abs(E)  # derivative of the true current cycle
                T_ma = T_of_E(E) + dTdE * dE
            err_t += T_ma - T_exact
            T_rec = T_ma if chained else T_exact  # fresh re-anchors the record to truth
            E, e = E_new, e_new
            kicks_done = k + 1
            if kicks_done in (10, 50, 100, 200):
                hist.append(dict(kick=kicks_done, e=round(e, 6),
                                 mean_anom_err_turns=abs(err_t) / T_of_E(E)))
        return dict(chained=chained, kicks=kicks_done, e_final=round(e, 6),
                    hist=hist, seed=seed)
    return dict(one_sided=[run(False), run(True)],
                random_sign=[run(False, seed=7), run(True, seed=7)])

# ---------------------------------------------------------------- Part C: GR separatrix
def gr_cycle(E, L, g=1.0, phi_max=6000.0, rtol=1e-12):
    """One radial cycle (apo->apo) of u'' = g*(3u^2) + 1/L^2 - u via first-integral
    start at apoapsis; returns (phi_cycle, T_coord, tau_cycle) or None."""
    # roots of E^2 - (1-2u)(1+L^2 u^2) = 0  [g=1];  for g=0 Newtonian potential
    if g == 0:
        # Newtonian: u'' = 1/L^2 - u  => u = (1/L^2)(1 + e cos phi); roots from
        # turning points: (u')^2 = (2E_N/L^2) - u^2 + 2u/L^2 (with our Newtonian E)
        raise RuntimeError("use kepler_control instead")
    poly = [2 * L * L, -L * L, 2.0, E * E - 1.0]
    r = np.roots(poly)
    re = sorted([x.real for x in r if abs(x.imag) < 1e-11 and x.real > 0])
    if len(re) < 2:
        return None
    if len(re) < 3:
        return None  # no bound window at this (E, L)
    u_apo, u_peri = re[0], re[1]

    def V2(u):
        return (1 - 2 * u) * (1 + L * L * u * u)

    u0 = u_peri * (1 - 1e-9)
    p0 = -math.sqrt(max(E * E - V2(u0), 0)) / L  # du/dphi < 0 (outbound leg)

    def rhs(phi, y):
        u, p = y[0], y[1]
        return [p, 1 / L ** 2 + 3 * u * u - u,
                E / (L * u * u * (1 - 2 * u)), 1 / (L * u * u)]

    def apo(phi, y):
        return y[1]
    apo.direction = -1  # p: + -> - at NEXT periapsis = one FULL radial cycle
    apo.terminal = True

    sol = solve_ivp(rhs, (0, phi_max), [u0, p0, 0.0, 0.0], rtol=rtol, atol=1e-14,
                    events=apo, dense_output=False, max_step=0.05)
    if not sol.t_events[0].size:
        return None
    return dict(phi_cycle=float(sol.t_events[0][0]), T=float(sol.y_events[0][0][2]),
                tau=float(sol.y_events[0][0][3]), u_apo=u_apo, u_peri=u_peri)


def kepler_control(L=3.0, ecc=0.6):
    """Harness control: g=0 Newtonian Binet, same integrator machinery in tau.
    Analytic tau-cycle = 2*pi*a^{3/2}, a = L^2/(1-e^2) (mu=1)."""
    a = L * L / (1 - ecc * ecc)
    # Newtonian energy for start-at-apo initialisation: use u = (1+e cos)/L^2
    # integrate u'' = 1/L^2 - u with first-integral start
    u_peri = (1 + ecc) / L ** 2
    u0 = u_peri * (1 - 1e-9)
    # (u')^2 = (1/L^4)(e^2 - (1 - L^2 u)^2) for this family; outbound => p < 0
    p0 = -math.sqrt(max(ecc * ecc - (1 - L * L * u0) ** 2, 0)) / L ** 2

    def rhs(phi, y):
        u, p = y[0], y[1]
        return [p, 1 / L ** 2 - u, 1 / (L * u * u)]

    def apo(phi, y):
        return y[1]
    apo.direction = -1  # next periapsis = full cycle
    apo.terminal = True

    sol = solve_ivp(rhs, (0, 100.0), [u0, p0, 0.0], rtol=1e-12, atol=1e-14,
                    events=apo, max_step=0.05)
    tau_num = float(sol.y_events[0][0][2])
    tau_exact = 2 * math.pi * a ** 1.5
    phi_num = float(sol.t_events[0][0])
    return dict(tau_num=tau_num, tau_exact=tau_exact,
                relerr=abs(tau_num - tau_exact) / tau_exact,
                phi_cycle=phi_num, phi_err=abs(phi_num - 2 * math.pi))


def partC(E=0.95, g=1.0):
    # separatrix: unstable circular u_c solves (1-2u)^2 = E^2 (1-3u), larger root
    a, b, c = 4.0, 3 * E * E - 4.0, 1 - E * E
    disc = b * b - 4 * a * c
    u_c = (-b + math.sqrt(disc)) / (2 * a)  # larger root
    L_sep = math.sqrt(1.0 / (u_c - 3 * u_c * u_c))
    # upper edge of the bound window at fixed E: V2 at the stable circular u_-(L) == E^2
    def well(Lx):
        s = math.sqrt(max(1 - 12 / Lx ** 2, 0))
        um = (1 - s) / 6
        return (1 - 2 * um) * (1 + Lx * Lx * um * um)
    lo, hi = L_sep, L_sep * 1.10
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if well(mid) > E * E:
            hi = mid
        else:
            lo = mid
    L_edge = lo
    rows = [{"d": (L_edge - L_sep) / L_sep, "L": L_edge, "T": None, "note": "window edge"}]
    ds = [1e-2, 3e-3, 1e-3, 3e-4, 1e-4]
    for d in ds:
        L = L_sep * (1 + d)
        cy = gr_cycle(E, L, g=g)
        if cy is None:
            rows.append(dict(d=d, L=L, T=None))
            continue
        rows.append(dict(d=d, L=L, T=cy["T"], phi=cy["phi_cycle"],
                         u_apo=cy["u_apo"], u_peri=cy["u_peri"]))
    # divergence exponent: local dlnT/dln(1/d)  (test power vs log)
    fit = []
    for i in range(len(rows) - 1):
        if rows[i]["T"] and rows[i + 1]["T"]:
            fit.append(dict(d1=rows[i]["d"], d2=rows[i + 1]["d"],
                            exponent=math.log(rows[i + 1]["T"] / rows[i]["T"])
                            / math.log(rows[i]["d"] / rows[i + 1]["d"])))
    # log-divergence fit: T ~ a + b*ln(1/d)
    pts = [(math.log(1 / r["d"]), r["T"]) for r in rows if r["T"]]
    if len(pts) >= 3:
        xs, ys = zip(*pts)
        b_log, a_log = np.polyfit(xs, ys, 1)
        fit.append(dict(log_fit_slope=b_log, log_fit_a=a_log))
    # multiply-add rows: stored derivative via FD at L, kick dL, exact recompute
    ma = []
    for d in [1e-2, 3e-3, 1e-3]:
        for dl_rel in [1e-3, 1e-2]:
            L = L_sep * (1 + d)
            dL = dl_rel * L
            base = gr_cycle(E, L)
            up = gr_cycle(E, L + dL)
            dn = gr_cycle(E, L - dL * 0.5)  # derivative from below (stored deriv)
            if not (base and up and dn):
                continue
            dTdL = (base["T"] - dn["T"]) / (0.5 * dL)
            T_ma = base["T"] + dTdL * dL
            ma.append(dict(d=d, dl_rel=dl_rel,
                           eps=abs(T_ma - up["T"]) / up["T"],
                           crossed_sep=(L - dL * 0.5) < L_sep))
    # the boundary-crossing kick: d = 1e-3, kick DOWN by 1.5x the gap -> exact = plunge
    L = L_sep * (1 + 1e-3)
    dL = -1.5e-3 * L
    base = gr_cycle(E, L)
    crossed = gr_cycle(E, L + dL)  # None => plunge (no bound cycle exists)
    up = gr_cycle(E, L + 1e-3 * L)
    if base and up:
        dTdL = (up["T"] - base["T"]) / (1e-3 * L)
        T_ma = base["T"] + dTdL * dL
        ma.append(dict(d=1e-3, dl_rel=-1.5e-3, eps=None,
                       T_ma_bound=float(T_ma), exact="PLUNGE (no cycle)" if crossed is None
                       else float(crossed["T"]), crossed_sep=True))
    return dict(u_c=u_c, L_sep=L_sep, rows=rows, fit=fit, ma=ma)


if __name__ == "__main__":
    t0 = __import__("time").time()
    OUT["A"] = partA()
    OUT["B"] = partB()
    OUT["C_control"] = kepler_control()
    OUT["C"] = partC()
    OUT["wall_s"] = __import__("time").time() - t0
    with open(sys.argv[1] if len(sys.argv) > 1 else "falsifier_out.json", "w") as f:
        json.dump(OUT, f, indent=1)
    # ---- compact report
    print("== A: per-kick multiply-add error (Newtonian, closed form) ==")
    print(f"{'e':>7} {'kick':>18} {'x=dE/|E|':>10} {'eps1':>10} {'eps2':>10}  >1%  >r2floor")
    for r in OUT["A"]["rows"]:
        if r["kick"] == "belt 2^-23" and r["e"] not in (0.999,):
            continue
        print(f"{r['e']:>7} {r['kick']:>18} {r['x']:>10.3e} {r['eps1']:>10.3e} "
              f"{r['eps2']:>10.3e}  {str(r['bar1']):>5} {str(r['bar_r2']):>8}")
    print("H1 law check:", [(round(h['x'], 4), f"{h['relerr']:.2e}") for h in OUT["A"]["h1"]])
    print("H2 benign control eps:", f"{OUT['A']['h2']:.2e}")
    print("e* per kick (1% bar, 1st/2nd order):", OUT["A"]["estar"], OUT["A"]["estar2"])
    print("ring crossings/cycle:", {k: round(v) for k, v in OUT["A"]["crossings"].items()})
    print("\n== B: chaining (mean-anomaly error, turns) ==")
    for arm in ("one_sided", "random_sign"):
        for r in OUT["B"][arm]:
            print(arm, "chained" if r["chained"] else "fresh  ", "kicks", r["kicks"],
                  "e_final", r["e_final"], {h["kick"]: f"{h['mean_anom_err_turns']:.2e}" for h in r["hist"]})
    print("\n== C harness control (g=0): Kepler tau relerr, phi err ==")
    cc = OUT["C_control"]
    print(f"tau relerr {cc['relerr']:.2e}  phi_cycle err {cc['phi_err']:.2e}")
    print("\n== C: GR separatrix (E = 0.95, M = 1) ==")
    print("u_c", round(OUT["C"]["u_c"], 5), " L_sep", round(OUT["C"]["L_sep"], 6))
    for r in OUT["C"]["rows"]:
        if r["T"]:
            print(f"d={r['d']:.0e}  T={r['T']:.4e}  phi={r.get('phi', 0):.1f}")
        else:
            print(f"d={r['d']:.0e}  {r.get('note', 'cap')}")
    print("local exponents dlnT/dln(1/d):",
          [(f['d2'], round(f['exponent'], 3)) for f in OUT["C"]["fit"] if 'd2' in f])
    lf = [f for f in OUT["C"]["fit"] if 'log_fit_slope' in f]
    if lf:
        print("log fit T ~ a + b*ln(1/d): b=%.2f a=%.1f" % (lf[0]['log_fit_slope'], lf[0]['log_fit_a']))
    print("multiply-add rows:")
    for r in OUT["C"]["ma"]:
        if r["eps"] is not None:
            print(f"  d={r['d']:.0e} dL/L={r['dl_rel']:.0e} eps={r['eps']:.3e} crossed={r['crossed_sep']}")
        else:
            print(f"  d={r['d']:.0e} dL/L={r['dl_rel']:.0e} BOUNDARY KICK: MA predicts bound T="
                  f"{r['T_ma_bound']:.1f}, exact = {r['exact']}")
    print(f"\nwall {OUT['wall_s']:.1f} s")
