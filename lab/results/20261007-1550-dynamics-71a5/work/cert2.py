#!/usr/bin/env python3
"""Run 2: restructured decisive suite (lab run 20261007-1550-dynamics-71a5).

Fixes and design after run 1:
- coprec control uses ABSOLUTE equal Omega on both bodies (0.05 rad/time); run 1's '0.3 per
  orbit' gave unequal rates (different periods) — a malformed control, not a broken symmetry.
- Active-section aging measured as an ENSEMBLE over 12 conjunction phases (M0_j), because a
  single pair's first-miss time is conjunction-sampling luck (run 1: slope 0.45, nonmonotone).
- G6: near-tangential CROSSING pair (wide arcs, dense encounters). G4n: true 'None' pair
  (cone gap 0.0091 > eps_u(rho)), safety horizon t_cross = K/Om analytic.
- drift fit guarded (run 1 crashed on an empty selection).
"""
import json, os
import numpy as np
from cert import (TAU, body, frozen, pair_minima, run_case, first_below, fit_exp,
                  cone_gap, R_of, machine)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results2.json")


def main():
    T, N = 1500.0, 1 << 21
    RHO = 0.004
    nn = lambda a: a ** -1.5
    G2 = (body(1.0, 0.30, 0.3, nn(1.0)), body(0.85, 0.40, 1.2, nn(0.85)))
    G6 = (body(1.0, 0.30, 0.3, nn(1.0)), body(0.8, 0.30, 1.03, nn(0.8)))   # crossing (barely)
    G4n = (body(1.0, 0.30, 0.3, nn(1.0)), body(0.8, 0.30, 1.00, nn(0.8)))  # None pair
    results = dict(machine=machine(), params=dict(T=T, N=N, RHO=RHO), cases=[], fits={})

    for nm, gg in (("G2", G2), ("G6", G6), ("G4n", G4n)):
        print(f"{nm}: cone_gap={cone_gap(*gg):+.5f}", flush=True)

    # --- controls: kepler, and absolute-equal-rate precession (prediction 1) ---
    for g, gg in (("G6", G6), ("G4n", G4n)):
        froz = pair_minima(frozen(gg[0]), frozen(gg[1]), T, N, 0.05)
        for tag, om in (("kepler", 0.0), ("coprec", 0.05)):
            r = run_case(f"control-{g}-{tag}", dict(gg[0], Om=om), dict(gg[1], Om=om),
                         RHO, T, N, froz)
            results["cases"].append(r)
            print(f"control {g} {tag}: misses={r['misses']} waste={r['waste']} "
                  f"m0_true={r['m0_true']:.6f} vs frozen {r['m0_frozen']:.6f}", flush=True)

    # --- A2: active near-tangential crossing pair, ensemble over 12 conjunction phases ---
    K = 12
    phases = [k * TAU / K for k in range(K)]
    frozK = [pair_minima(frozen(G6[0]), frozen(dict(G6[1], M0=p)), T, N, 0.05) for p in phases]
    rates = np.logspace(-5.0, -3.0, 5)
    ens = []
    for om in rates:
        tot_m = tot_p = tot_w = tot_ev = 0
        earliest = None
        for p, fz in zip(phases, frozK):
            r = run_case(f"A2-G6-om{om:.3g}-ph{p:.3f}", dict(G6[0], Om=om),
                         dict(G6[1], M0=p), RHO, T, N, fz)
            tot_m += r["misses"]; tot_p += r["n_prop"]; tot_w += r["waste"]
            tot_ev += sum(1 for (t, d) in zip(r["drift_t"], r["drift_dd"]) if d < 0 and False)
            if r["first_miss"] is not None and (earliest is None or r["first_miss"] < earliest):
                earliest = r["first_miss"]
        ens.append(dict(om=float(om), misses=tot_m, props=tot_p, waste=tot_w, earliest=earliest))
        print(f"A2 G6 Om={om:.3g}: misses={tot_m}/{K}p props={tot_p} waste={tot_w} "
              f"earliest={earliest}", flush=True)
    okE = [(e["om"], e["earliest"]) for e in ens if e["earliest"] is not None]
    results["fits"]["A2_G6"] = dict(ensemble=ens,
                                    exp_earliest=fit_exp([o for o, _ in okE], [v for _, v in okE]))
    print("A2 earliest-vs-Om fit:", results["fits"]["A2_G6"]["exp_earliest"], flush=True)

    # --- B2: None pair; analytic t_cross vs first realized sub-rho event ---
    h = 1e-4
    R0 = R_of(G4n[0], G4n[1])
    Rp = R_of(G4n[0], dict(G4n[1], pom=G4n[1]["pom"] - h))
    dRdvar = (R0 - Rp) / h
    gap0 = cone_gap(*G4n)
    Kc = abs(gap0) / dRdvar
    frozB = pair_minima(frozen(G4n[0]), frozen(G4n[1]), T, N, 0.05)
    B = []
    for om in (5e-5, 1e-4, 2e-4, 5e-4):
        bj = dict(G4n[1], Om=-om)
        fb = first_below(pair_minima(G4n[0], bj, T, N, 0.05), RHO)
        r = run_case(f"B2-G4n-om{om:.3g}", G4n[0], bj, RHO, T, N, frozB)
        r["first_true_below"] = fb
        results["cases"].append(r)
        B.append(dict(om=om, t_cross=Kc / om, first_sub_rho=fb))
        print(f"B2 Om={om:.3g}: t_cross={Kc/om:.1f} first_sub_rho={fb}", flush=True)
    results["fits"]["B2_G4n"] = dict(cone_gap0=gap0, dR_d_var=dRdvar, K=Kc, rows=B)

    # --- drift linearity (prediction 2), guarded ---
    froz2 = pair_minima(frozen(G2[0]), frozen(G2[1]), T, N, 0.05)
    for om in (1e-4, 3e-4):
        r = run_case(f"drift-G2-om{om:.3g}", dict(G2[0], Om=om), G2[1], RHO, T, N, froz2)
        results["cases"].append(r)
        t = np.array(r["drift_t"]); dd = np.abs(np.array(r["drift_dd"]))
        sel = (t > 0.1 * T) & (dd > 0)
        if int(sel.sum()) >= 3:
            f = fit_exp(t[sel], dd[sel], floor=1e-13)
            amp = float(np.median(dd[sel] / t[sel]))
            results["fits"][f"drift_om{om:.3g}"] = dict(exp=f, amp_per_t=amp, n=int(sel.sum()))
            print(f"drift Om={om:.3g}: |dd|~t^{f['slope']} amp/t={amp:.3e} n={sel.sum()}", flush=True)
        else:
            print(f"drift Om={om:.3g}: too few matched minima ({int(sel.sum())})", flush=True)

    # --- mechanism constant: m0 vs rigid relative rotation ---
    for nm, gg in (("G2", G2), ("G6", G6)):
        md = {}
        for dlt in (0.0, +0.02, -0.02):
            bj = dict(gg[1], pom=gg[1]["pom"] + dlt)
            md[f"{dlt:+.2f}"] = min(d for (_, d) in pair_minima(frozen(gg[0]), frozen(bj), T, N, 0.05))
        md["dm0_dpom"] = (md["+0.02"] - md["-0.02"]) / 0.04
        results["fits"][f"m_of_dpom_{nm}"] = md
        print(f"{nm} m0(dpom): {md}", flush=True)

    with open(OUT, "w") as f:
        json.dump(results, f, indent=1)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
