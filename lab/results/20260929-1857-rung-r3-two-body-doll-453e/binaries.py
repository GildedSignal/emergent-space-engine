"""Rung r3 binaries: 256 seeded cases x 3 configs -> prec/period/nu/events metrics.

Sampler (rung): random.Random(20261002); p log-uniform [20,1000] (units of M), e
uniform [0,0.6), nu uniform [0.01,0.25]; per binary draws (p, e, nu) in that order.

Configs:
  eob-doll  : exact Schwarzschild geodesic for the relative motion, invariants mapped
              from the case's 1PN harmonic invariants (E,J) via the EOB energy map
              x=((1+nu*eps)^2-1)/(2nu), L_eff=J; real period = F * T_geod with
              F = sqrt(1+2nu*x) = 1+nu*eps.
  test-mass : same geodesic law around m1 only (nu ignored), orbit (p,e) with
              Kepler/turning geometry around m1; no energy map.
  newton-doll: Kepler ellipse (advance = 0).

Oracle: damour_deruelle(eih_invariants(p,e,nu)) -- see oracle.py (verified vs Rust).
"""
import json
import math
import random

import numpy as np

from oracle import (eih_invariants, damour_deruelle,
                    schwarzschild_from_invariants, bound_constants,
                    geodesic_dphi_and_period)

N_BIN = 256
TRUNC_LIMIT = 5e-4   # oracle truncation estimate above which a period case is excluded


def eob_orbit(p, e, nu):
    """(advance, radial period) of the eob-doll for case (p,e,nu); nu=0 allowed."""
    rp, vt, eps, J = eih_invariants(p, e, nu)
    if nu > 1e-14:
        x = ((1.0 + nu*eps)**2 - 1.0)/(2.0*nu)
    else:
        x = eps
    ps, es = schwarzschild_from_invariants(x, J, p)
    adv, T = geodesic_dphi_and_period(ps, es)
    F = math.sqrt(1.0 + 2.0*nu*x)          # = 1 + nu*eps exactly
    return adv, F*T


def test_mass_orbit(p, e, nu):
    m1 = 0.5*(1.0 + math.sqrt(1.0 - 4.0*nu))
    E, L = bound_constants(p/m1, e)
    adv, T = geodesic_dphi_and_period(p/m1, e)
    return adv, m1*T                     # time scales with the central mass


def newton_orbit(p, e, nu):
    a = p/(1.0 - e*e)
    return 0.0, 2.0*np.pi*a**1.5


CONFIGS = {"eob-doll": eob_orbit, "test-mass": test_mass_orbit, "newton-doll": newton_orbit}


def main():
    rng = random.Random(20261002)
    cases = []
    for _ in range(N_BIN):
        p = math.exp(rng.uniform(math.log(20.0), math.log(1000.0)))
        e = rng.uniform(0.0, 0.6)
        nu = rng.uniform(0.01, 0.25)
        cases.append((p, e, nu))

    # oracle values and nu-baselines
    or_adv, or_P, or_P0 = [], [], []
    for (p, e, nu) in cases:
        _, _, eps, J = eih_invariants(p, e, nu)
        a, per = damour_deruelle(eps, J, nu)
        _, _, eps0, J0 = eih_invariants(p, e, 0.0)
        _, per0 = damour_deruelle(eps0, J0, 0.0)
        or_adv.append(a); or_P.append(per); or_P0.append(per0)
    or_adv = np.array(or_adv); or_P = np.array(or_P); or_P0 = np.array(or_P0)

    # doll orbits, all configs, both nu and nu=0 baseline
    doll = {}
    for name, fn in CONFIGS.items():
        doll[name] = [np.array([fn(p, e, nu) for (p, e, nu) in cases]),
                      np.array([fn(p, e, 0.0) for (p, e, nu) in cases])]

    # oracle truncation estimate (2PN size, nu=0): exact geodesic vs 1PN oracle
    excl = []
    for i, (p, e, nu) in enumerate(cases):
        adv0, T0 = eob_orbit(p, e, 0.0)
        excl.append(abs(T0 - or_P0[i])/or_P0[i] > TRUNC_LIMIT)
    excl = np.array(excl)

    metrics = {}
    detail = {}
    for name in CONFIGS:
        adv, P = doll[name][0][:, 0], doll[name][0][:, 1]
        P0 = doll[name][1][:, 1]
        prec_ok = np.abs(adv - or_adv) <= 0.01*or_adv
        keep = ~excl
        per_ok = (np.abs(P - or_P) <= 1e-3*or_P) & keep
        dP = P - P0
        dP_or = or_P - or_P0
        hi = np.array([nu >= 0.05 for (p, e, nu) in cases])
        nu_ok = hi & (np.sign(dP) == np.sign(dP_or)) & (np.abs(dP - dP_or) <= 0.1*np.abs(dP_or))
        metrics[name] = {
            "precession_pass_fraction": float(prec_ok.mean()),
            "period_pass_fraction": float(per_ok.sum()/keep.sum()),
            "nu_effect_pass_fraction": float(nu_ok[hi].mean()) if hi.any() else 0.0,
            "events_per_orbit": 0.0,
        }
        detail[name] = {
            "prec_min_p_passing": float(min([cases[i][0] for i in range(len(cases)) if prec_ok[i]], default=float('nan'))),
            "period_excluded_fraction": float(excl.mean()),
            "period_failures_included": int((~per_ok & keep).sum()),
            "nu_cases": int(hi.sum()),
            "nu_failures": int((hi & ~nu_ok).sum()),
            "worst_rel_period_err_included": float(np.max(np.abs(P - or_P)[keep]/or_P[keep])),
        }

    out = {"metrics": metrics, "detail": detail,
           "period_excluded_count": int(excl.sum()),
           "sampler_first_case": list(cases[0])}
    with open("binaries_out.json", "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
