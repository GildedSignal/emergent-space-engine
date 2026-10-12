#!/usr/bin/env python3
"""Second-author probe for run 20261011-2235-redteam-6164 (checker's named misses).

Part A (record regeneration, all from shipped code):
  - oracle precession ratios at p = 100/500/1000 (dossier cited 1.0481/1.0092/1.0046
    but the shipped probe.py only computed p = 100);
  - per-channel (dphi, T) jet errors for the P1 grid, against the parent's
    decomposition claim (precession phase 4*(alpha*a)^2 dominant, T-channel
    "r_apo-free, Kepler 15/4*alpha^2"; the checker said 15/8);
  - saturation measurement at r_apo = 2000 (p=20, e=0.99), alpha=1e-6: N_floor = 1
    (every kick recompiles; the dossier's unsaturated "2.8 compiles/kick" caps at 1);
  - L-channel errors against the oracle's own h-refinement noise;
  - doc-level findings regenerated from the tree (Minsky named the primary in-cell
    solution, r5/r6 named but absent, darwin16 replacement, no jet-domain criterion
    in B5-B19, re-anchor trigger drift-only).

Part B (the named experiment: Kerr, chi != 0):
  equatorial Kerr timelike geodesics (M=1, prograde) from the exact first-order
  form (du/dphi)^2 = u^4*D^2*R/Dphi^2, differentiated once: u'' = F'(u)/2 with F
  built symbolically (sympy) and lambdified. Same cycle/derivative/jet machinery as
  the parent's Schwarzschild probe. Control: a=0, r_c=5 must reproduce the parent's
  P3 separatrix sweep to < 1e-9 relative (it reduces to the same Binet RHS:
  at a=0, F'(u)/2 = 1/L^2 - u + 3u^2 and dt/dphi = E/(L u^2 (1-2u))).
"""
import json
import math
import os
import sys

import numpy as np
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from probe import FLOOR, EL_from_pe, cycle, derivatives, jet_err, walk_jet  # noqa: E402


# --------------------------------------------------------------------------
# Part A1: precession ratios the dossier cited but did not regenerate
# --------------------------------------------------------------------------
def precession_ratios():
    rows = []
    for p in (100.0, 500.0, 1000.0):
        E, L = EL_from_pe(p, 0.5)
        r = cycle(E, L)
        rows.append({"p": p, "e": 0.5,
                     "dphi_minus_2pi": r[0] - 2 * math.pi,
                     "6pi_over_p": 6 * math.pi / p,
                     "ratio": (r[0] - 2 * math.pi) / (6 * math.pi / p)})
    return rows


# --------------------------------------------------------------------------
# Part A2: per-channel jet errors (parent reported only the max of the two)
# --------------------------------------------------------------------------
def jet_channels(E, L, kick_E=0.0, kick_L=0.0):
    """(dphi_err, T_err) of the one-kick jet, per channel, plus 1-E."""
    base = cycle(E, L)
    der = derivatives(E, L)
    if base is None or der is None:
        return None
    new = cycle(E + kick_E, L + kick_L)
    if new is None:
        return "plunge-after-kick"
    jd = base[0] + der[0] * kick_E + der[2] * kick_L
    jT = base[1] + der[1] * kick_E + der[3] * kick_L
    return (abs(jd - new[0]) / new[0], abs(jT - new[1]) / new[1])


def per_channel_grid():
    rows = []
    for p in (20.0, 100.0):
        for e in (0.1, 0.5, 0.7, 0.9, 0.99):
            E, L = EL_from_pe(p, e)
            ch = jet_channels(E, L, kick_E=1e-6 * E)
            a_sem = p / (1 - e) / 2.0  # r_apo/2
            ke = {"p": p, "e": e, "r_apo": p / (1 - e), "one_minus_E": 1 - E,
                  "dphi_err": ch[0], "T_err": ch[1],
                  "kepler_T_est_15_8": (15 / 8) * (1e-6 * E / (1 - E)) ** 2,
                  "prec_est_4": (1e-6 * E * p / (1 - e)) ** 2}
            rows.append(ke)
    return rows


# --------------------------------------------------------------------------
# Part A3: saturation at r_apo = 2000 (compiles/kick caps at 1)
# --------------------------------------------------------------------------
def saturation():
    E, L = EL_from_pe(20.0, 0.99)  # r_apo = 2000
    pts, plunge_N = walk_jet(E, L, 1e-6, nmax=100000)
    n_floor = next((N for N, err in pts if err > FLOOR), None)
    one = jet_err(E, L, kick_E=1e-6 * E)
    formula = 1.4e3 * 2000.0 * 1e-6  # dossier's unsaturated figure: 2.8
    return {"p": 20, "e": 0.99, "r_apo": 2000.0, "alpha": 1e-6,
            "one_kick_err": one, "N_floor_measured": n_floor,
            "compiles_per_kick_measured": (1.0 / n_floor) if n_floor else None,
            "formula_1p4e3_rapo_alpha": formula,
            "formula_capped_at_1": min(1.0, formula)}


# --------------------------------------------------------------------------
# Part A4: L-channel vs the oracle's own h-refinement noise
# --------------------------------------------------------------------------
def l_channel_noise():
    E, L = EL_from_pe(100.0, 0.99)  # the largest L-channel error in the parent's grid
    h1 = cycle(E, L, h=1e-3)
    h2 = cycle(E, L, h=5e-4)
    noise = max(abs(h2[0] - h1[0]) / h1[0], abs(h2[1] - h1[1]) / h1[1])
    return {"case": "p=100, e=0.99", "oracle_h_noise_rel": noise,
            "L_channel_err_kickL_1e-6": jet_err(E, L, kick_L=1e-6 * L)}


# --------------------------------------------------------------------------
# Part A5: doc-level findings, regenerated from the tree
# --------------------------------------------------------------------------
def doc_check():
    root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "..", "..", ".."))
    rep = open(os.path.join(root, "docs", "representation.md")).read()
    law = open(os.path.join(root, "docs", "law.md")).read()
    rungs = os.listdir(os.path.join(root, "lab", "rungs"))
    gates = [ln for ln in law.splitlines() if ln.strip().startswith("| B")]
    return {
        "minsky_still_primary_in_representation":
            "Minsky" in rep and "primary in-cell solution" in rep,
        "jet_quote_in_representation_s3":
            "A cycle's derivatives are stored with it, so a kick updates the cycle by a multiply-add" in rep,
        "r5_r6_named_in_representation_ladder":
            "r5 dense order" in rep and "r6 view" in rep,
        "r5_r6_absent_from_lab_rungs":
            not any(r.startswith(("r5", "r6")) for r in rungs),
        "rungs_present": sorted(r.replace(".md", "") for r in rungs),
        "law_records_darwin16_replacement":
            "space-darwin16-v1" in law and "replaced the in-band area-preserving map" in law,
        "gate_count": len(gates),
        "gates_mentioning_recompile_or_jet_or_separatrix":
            [ln.split("|")[2].strip() for ln in gates
             if any(k in ln.lower() for k in ("recompile", "jet", "separatrix", "root-distance"))],
        "reanchor_trigger_drift_only":
            "accumulated offset reaches" in law and "sqrt(floor/C)" in law.replace("√(floor/C)", "sqrt(floor/C)"),
        "b19_gates_kerr_behaviours_not_jet_domain":
            "B19 rotating holes" in law and "recompile" not in
            [ln for ln in gates if "B19" in ln][0],
    }


# --------------------------------------------------------------------------
# Part B: equatorial Kerr geodesics (the named experiment)
# --------------------------------------------------------------------------
_u, _a, _E, _L = sp.symbols("u a E L", positive=False, real=True)
_D = 1 / _u**2 - 2 / _u + _a**2
_P = _E * (1 / _u**2 + _a**2) - _a * _L
_m = _L - _a * _E
_R = _P**2 - _D * (1 / _u**2 + _m**2)
_DPHI = _m * _D + _a * _P
_F = _u**4 * _D**2 * _R / _DPHI**2
_Fp = sp.cancel(sp.diff(_F, _u) / 2)
_G = sp.cancel((_a * _D * _m + (1 / _u**2 + _a**2) * _P) / _DPHI)
fp_fun = sp.lambdify((_u, _a, _E, _L), _Fp, "math")
g_fun = sp.lambdify((_u, _a, _E, _L), _G, "math")


def kerr_u_horizon(a):
    return 1.0 / (1.0 + math.sqrt(1.0 - a * a))


def kerr_roots(a, E, L):
    """Real roots of Q(u) = u^4 R(1/u) (cubic in u), ascending."""
    m = L - a * E
    b = a * a * E - a * L
    c = [E * E - 1.0, 2.0, 2 * E * b - a * a - m * m, 2 * m * m]  # c0..c3
    coeffs = [c[3], c[2], c[1], c[0]]
    while coeffs and abs(coeffs[0]) < 1e-300:
        coeffs.pop(0)
    r = np.roots(coeffs)
    return sorted(float(np.real(x)) for x in r if abs(np.imag(x)) < 1e-9)


def kerr_orbit(a, E, L, h=1e-3, cap_phi=300.0):
    """One radial cycle from periapsis, Kerr equatorial. (dphi, T) or None."""
    u_h = kerr_u_horizon(a)
    rs = kerr_roots(a, E, L)
    band = None
    for i in range(len(rs) - 1):
        lo, hi = rs[i], rs[i + 1]
        if lo <= 1e-12 or hi >= u_h - 1e-9:
            continue
        # Q > 0 strictly inside the band
        mid = 0.5 * (lo + hi)
        mm = L - a * E
        bb = a * a * E - a * L
        Qmid = (E * E - 1) + 2 * mid + (2 * E * bb - a * a - mm * mm) * mid**2 \
            + 2 * mm * mm * mid**3
        if Qmid > 0:
            band = (lo, hi)
            break
    if band is None:
        return None
    u_apo, u_per = band

    def f(u):
        return fp_fun(u, a, E, L)

    def g(u):
        return g_fun(u, a, E, L)

    u, up, up_prev, phi = u_per, 0.0, 0.0, 0.0
    passed_apo = False
    gs = [g(u)]
    while phi < cap_phi:
        k1u, k1v = up, f(u)
        k2u, k2v = up + 0.5 * h * k1v, f(u + 0.5 * h * k1u)
        k3u, k3v = up + 0.5 * h * k2v, f(u + 0.5 * h * k2u)
        k4u, k4v = up + h * k3v, f(u + h * k3u)
        u_new = u + (h / 6.0) * (k1u + 2 * k2u + 2 * k3u + k4u)
        up_new = up + (h / 6.0) * (k1v + 2 * k2v + 2 * k3v + k4v)
        phi_new = phi + h
        if not (u_apo * 0.5 < u_new < min(u_per * 1.5, u_h)):
            return None  # left the band: numerical failure or plunge
        if up_prev < 0.0 <= up_new:
            passed_apo = True
        gs.append(0.5 * (g(u) + g(u_new)))
        u, up_prev, phi = u_new, up, phi_new
        up = up_new
        if passed_apo and up_prev > 0.0 >= up:
            x = up_prev * h / (up_prev - up)
            phi_p = phi - h + x
            break
    else:
        return None
    if len(gs) % 2 == 0:
        gs = gs[:-1]
    T = (h / 3.0) * (gs[0] + gs[-1] + 4 * sum(gs[1:-1:2]) + 2 * sum(gs[2:-1:2]))
    T += g(u) * (phi_p - (len(gs) - 1) * h)
    return (phi_p, T)


def kerr_cycle(a, E, L, **kw):
    return kerr_orbit(a, E, L, **kw)


def kerr_derivatives(a, E, L, dh_rel=1e-7):
    dE, dL = dh_rel * abs(E), dh_rel * L
    pP, pM = kerr_cycle(a, E + dE, L), kerr_cycle(a, E - dE, L)
    qP, qM = kerr_cycle(a, E, L + dL), kerr_cycle(a, E, L - dL)
    if None in (pP, pM, qP, qM):
        return None
    return ((pP[0] - pM[0]) / (2 * dE), (pP[1] - pM[1]) / (2 * dE),
            (qP[0] - qM[0]) / (2 * dL), (qP[1] - qM[1]) / (2 * dL))


def kerr_jet_err(a, E, L, kick_E=0.0, kick_L=0.0):
    base = kerr_cycle(a, E, L)
    if base is None:
        return "base-plunge"
    der = kerr_derivatives(a, E, L)
    if der is None:
        return "div"
    new = kerr_cycle(a, E + kick_E, L + kick_L)
    if new is None:
        return "plunge-after-kick"
    jd = base[0] + der[0] * kick_E + der[2] * kick_L
    jT = base[1] + der[1] * kick_E + der[3] * kick_L
    return max(abs(jd - new[0]) / new[0], abs(jT - new[1]) / new[1])


def circular(a, r_c):
    """(E_c, L_c) of the circular orbit at r_c, prograde, from R = R' = 0."""
    r, E, L = sp.symbols("r E L", real=True)
    D = r**2 - 2 * r + a**2
    P = E * (r**2 + a**2) - a * L
    m = L - a * E
    R = P**2 - D * (r**2 + m**2)
    sols = sp.solve([sp.Eq(R.subs(r, r_c), 0), sp.Eq(sp.diff(R, r).subs(r, r_c), 0)],
                    [E, L], dict=True)
    out = []
    for s in sols:
        Ev, Lv = complex(s[E]), complex(s[L])
        if abs(Ev.imag) < 1e-12 and abs(Lv.imag) < 1e-12:
            Ev, Lv = Ev.real, Lv.real
            if 0 < Ev < 1 and Lv > 0:
                Rr = R.subs({r: r_c, E: Ev, L: Lv})
                dR = sp.diff(R, r).subs({r: r_c, E: Ev, L: Lv})
                out.append({"E": Ev, "L": Lv,
                            "R_residual": float(abs(Rr)), "dR_residual": float(abs(dR))})
    if not out:
        return None
    return min(out, key=lambda s: s["R_residual"] + s["dR_residual"])


def kerr_separatrix(a, r_c, eps_list=(1e-2, 1e-3, 1e-4, 1e-5, 1e-6)):
    cir = circular(a, r_c)
    if cir is None:
        return None
    Ec, Lc = cir["E"], cir["L"]
    rows = []
    for eps in eps_list:
        E = Ec * (1 - eps)
        c = kerr_cycle(a, E, Lc)
        der = kerr_derivatives(a, E, Lc)
        rows.append({
            "eps": eps, "dphi": c[0] if c else None, "T": c[1] if c else None,
            "jet_err_kickE_1e-6": (kerr_jet_err(a, E, Lc, kick_E=1e-6 * E)
                                   if c and der else None),
            "jet_err_kickL_1e-6": (kerr_jet_err(a, E, Lc, kick_L=1e-6 * Lc)
                                   if c and der else None),
            "abs_dT_dE": abs(der[1]) if der else None,
        })
    band = []
    E = Ec * (1 - 1e-3)
    for alpha in (1e-6, 1e-5, 1e-4, 1e-3, 3e-3, 1e-2):
        band.append({"alpha": alpha,
                     "kickE": kerr_jet_err(a, E, Lc, kick_E=alpha * abs(E)),
                     "kickL": kerr_jet_err(a, E, Lc, kick_L=alpha * Lc)})
    return {"a": a, "r_c": r_c, "E_c": Ec, "L_c": Lc,
            "R_residual": cir["R_residual"], "dR_residual": cir["dR_residual"],
            "sweep": rows, "kick_band_eps_1e-3": band}


def a0_control():
    """a=0, r_c=5 through the Kerr machinery vs the parent's P3 (same numbers)."""
    sw = kerr_separatrix(0.0, 5.0, eps_list=(1e-3, 1e-4, 1e-5, 1e-6))
    parent = {1e-3: {"dphi": 15.491419819550881, "T": 308.9257283370301,
                     "abs_dT_dE": 28045.195830530098},
              1e-4: {"dphi": 20.391851939189973, "T": 366.64255899922,
                     "abs_dT_dE": 259887.02794015897},
              1e-5: {"dphi": 25.489697633338654, "T": 423.7114072263334,
                     "abs_dT_dE": 2624779.562627014},
              1e-6: {"dphi": 30.630333912966215, "T": 481.1660230107202,
                     "abs_dT_dE": 26422848.16381022}}
    ctrl = []
    for row in sw["sweep"]:
        par = parent[row["eps"]]
        ctrl.append({
            "eps": row["eps"],
            "dphi_rel_diff": abs(row["dphi"] - par["dphi"]) / par["dphi"],
            "T_rel_diff": abs(row["T"] - par["T"]) / par["T"],
            "dTdE_rel_diff": abs(row["abs_dT_dE"] - par["abs_dT_dE"]) / par["abs_dT_dE"],
        })
    sw["control_vs_parent_P3"] = ctrl
    return sw


def machine():
    load = open("/proc/loadavg").read().split()
    mem = open("/proc/meminfo").read().split("\n")
    memav = next(x for x in mem if x.startswith("MemAvailable"))
    return {"cpus": os.cpu_count(), "loadavg_1min": float(load[0]),
            "mem_available_kb": int(memav.split()[1])}


SPINS = {"a0": (0.0, 5.0), "a09": (0.9, 2.0), "a05": (0.5, 3.5), "a0998": (0.998, 1.15)}


def h_check(a, r_c, eps=1e-4):
    """Kerr oracle self-check: h-refinement on one deep-whirl case."""
    cir = circular(a, r_c)
    E, L = cir["E"] * (1 - eps), cir["L"]
    c1 = kerr_cycle(a, E, L, h=1e-3)
    c2 = kerr_cycle(a, E, L, h=5e-4)
    if c1 is None or c2 is None:
        return None
    return {"a": a, "r_c": r_c, "eps": eps,
            "dphi_h_refine_rel": abs(c2[0] - c1[0]) / c1[0],
            "T_h_refine_rel": abs(c2[1] - c1[1]) / c1[1]}


def run_part(part):
    out = {"machine": machine()}
    if part == "A":
        print("A1: precession ratios...", file=sys.stderr)
        out["A1_precession_ratios"] = precession_ratios()
        print("A2: per-channel grid...", file=sys.stderr)
        out["A2_per_channel"] = per_channel_grid()
        print("A3: saturation at r_apo=2000...", file=sys.stderr)
        out["A3_saturation"] = saturation()
        print("A4: L-channel vs noise...", file=sys.stderr)
        out["A4_l_channel_noise"] = l_channel_noise()
        print("A5: doc check...", file=sys.stderr)
        out["A5_doc_check"] = doc_check()
    elif part == "a0":
        print("B: a=0 control...", file=sys.stderr)
        out["B_a0_control"] = a0_control()
    elif part in SPINS:
        a, r_c = SPINS[part]
        print(f"B: Kerr a={a}, r_c={r_c}...", file=sys.stderr)
        out[f"B_kerr_{part}"] = kerr_separatrix(a, r_c)
        if part == "a0998":
            print("B: a=0.998 h-refinement check...", file=sys.stderr)
            out["B_kerr_h_check"] = h_check(a, r_c)
    elif part == "merge":
        merged = {}
        for name in ("A", "a0", "a09", "a05", "a0998", "hcheck"):
            merged.update(json.load(open(f"probe2_part_{name}.json")))
        merged["machine"] = machine()
        with open("probe2_out.json", "w") as f:
            json.dump(merged, f, indent=1)
        print(json.dumps(merged, indent=1))
        return
    elif part == "hcheck":
        print("B: Kerr h-refinement checks (shallow whirls)...", file=sys.stderr)
        out["B_kerr_h_check"] = [h_check(0.9, 2.0, eps=1e-3),
                                 h_check(0.5, 3.5, eps=1e-3)]
    else:
        raise SystemExit(f"unknown part {part}")
    with open(f"probe2_part_{part}.json", "w") as f:
        json.dump(out, f, indent=1)


def run_a0998_trimmed():
    """a=0.998, full eps sweep, reduced kick band (E+kickL at the decisive alphas)."""
    a, r_c = 0.998, 1.15
    out = {"machine": machine()}
    sw = kerr_separatrix(a, r_c, eps_list=(1e-3, 1e-4, 1e-5, 1e-6))
    cir = circular(a, r_c)
    E, L = cir["E"] * (1 - 1e-3), cir["L"]
    band = []
    for alpha in (1e-6, 1e-3, 3e-3, 1e-2):
        band.append({"alpha": alpha,
                     "kickE": kerr_jet_err(a, E, L, kick_E=alpha * abs(E)),
                     "kickL": kerr_jet_err(a, E, L, kick_L=alpha * L)})
    sw["kick_band_eps_1e-3"] = band
    sw["h_check"] = h_check(a, r_c)
    out["B_kerr_a0998"] = sw
    with open("probe2_part_a0998.json", "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1))



def run_a0998_lite():
    """a=0.998 decisive minimum: full eps=1e-3 row, whirl at eps=1e-6, E-kick band."""
    a, r_c = 0.998, 1.15
    out = {"machine": machine()}
    cir = circular(a, r_c)
    Ec, Lc = cir["E"], cir["L"]
    sweep = []
    for eps in (1e-3, 1e-6):
        E = Ec * (1 - eps)
        c = kerr_cycle(a, E, Lc)
        row = {"eps": eps, "dphi": c[0] if c else None, "T": c[1] if c else None}
        if eps == 1e-3:
            der = kerr_derivatives(a, E, Lc)
            row["abs_dT_dE"] = abs(der[1]) if der else None
            row["jet_err_kickE_1e-6"] = (kerr_jet_err(a, E, Lc, kick_E=1e-6 * E)
                                         if der else None)
            row["jet_err_kickL_1e-6"] = (kerr_jet_err(a, E, Lc, kick_L=1e-6 * Lc)
                                         if der else None)
        sweep.append(row)
    band = []
    E = Ec * (1 - 1e-3)
    for alpha in (1e-3, 3e-3, 1e-2):
        band.append({"alpha": alpha,
                     "kickE": kerr_jet_err(a, E, Lc, kick_E=alpha * abs(E))})
    out["B_kerr_a0998"] = {"a": a, "r_c": r_c, "E_c": Ec, "L_c": Lc,
                           "R_residual": cir["R_residual"],
                           "dR_residual": cir["dR_residual"],
                           "sweep": sweep, "kick_band_eps_1e-3_E_only": band,
                           "note": "lite: full sweep only at eps=1e-3; whirl at 1e-6; "
                                   "the deep-eps rows and L-band exceeded the run budget"}
    with open("probe2_part_a0998.json", "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("a0998t", "a0998lite"):
        run_a0998_lite() if sys.argv[1] == "a0998lite" else run_a0998_trimmed()
    else:
        run_part(sys.argv[1] if len(sys.argv) > 1 else "A")
