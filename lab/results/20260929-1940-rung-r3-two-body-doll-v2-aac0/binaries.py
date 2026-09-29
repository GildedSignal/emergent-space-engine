#!/usr/bin/env python3
"""Stage 2: full binary metrics for the three configurations + truncation sensitivity."""
import sys, json, random
import numpy as np
sys.path.insert(0, '.')
from r3lib import eih_EJ, damour_deruelle, doll_binaries

RNG = random.Random(20261002)   # rung sampler
N = 1024
seeds = []
for _ in range(N):
    p = np.exp(RNG.uniform(np.log(20.0), np.log(1000.0)))
    e = RNG.uniform(0.0, 0.6)
    nu = RNG.uniform(0.01, 0.25)
    seeds.append((p, e, nu))
P = np.array([s[0] for s in seeds]); E_ = np.array([s[1] for s in seeds])
NU = np.array([s[2] for s in seeds])
print("seeds:", len(seeds), "p range", P.min(), P.max())

TOL = {'prec': 0.01, 'period': 1e-3, 'nu': 0.10}

# oracle
Eor, Jor = eih_EJ(P, E_, NU)
DPHI_OR, T_OR = damour_deruelle(Eor, Jor, NU)

# truncation estimates (reading A: exact-vs-oracle gap at nu=0 = the oracle's own
# higher-PN truncation in the test-mass sector where exact geodesics are the truth)
# truncation estimates (reading A: exact-vs-oracle gap at nu=0 = the oracle's own
# higher-PN truncation in the test-mass sector, where exact geodesics are the truth)
Eor0, Jor0 = eih_EJ(P, E_, 0.0 * NU)
DPHI_OR0, T_OR0 = damour_deruelle(Eor0, Jor0, 0.0 * NU)
DPHI_D0, T_D0 = doll_binaries(P, E_, 0.0 * NU, 'eob')
EPS_PREC = np.abs((DPHI_D0 - 2 * np.pi) / DPHI_OR0 - 1.0) * (1.0 + NU)
EPS_PERIOD = np.abs(T_D0 / T_OR0 - 1.0) * (1.0 + NU)
R_OR = T_OR / T_OR0 - 1.0
# EOB nu-channel is from the oracle's nu-term (2PN content of the nu term)
_, T_Dn = doll_binaries(P, E_, NU, 'eob')
R_D = T_Dn / T_D0 - 1.0
EPS_NU = np.abs(R_D / R_OR - 1.0) + EPS_PERIOD
# reading B (oracle-internal next-PN term of the advance): 6pi/J^2 expansion
EPS_PREC_B = (4.0 + 2.0 * E_**2 - NU * E_**2) / P

out = {}
for mode in ('eob', 'test', 'newton'):
    dphi_d, T_d = doll_binaries(P, E_, NU, mode)
    adv = dphi_d - 2 * np.pi                      # doll's periastron advance
    if mode != 'newton':
        _, T_d0 = doll_binaries(P, E_, 0.0 * NU, mode)
        R_d = T_d / T_d0 - 1.0
    else:
        R_d = 0.0 * NU                            # Kepler period has no nu dependence

    judged = {'prec': EPS_PREC <= 0.5 * TOL['prec'],
              'period': EPS_PERIOD <= 0.5 * TOL['period'],
              'nu': (EPS_NU <= 0.5 * TOL['nu']) & (NU >= 0.05)}
    prec_pass = judged['prec'] & (np.abs(adv / DPHI_OR - 1.0) <= TOL['prec'])
    period_pass = judged['period'] & (np.abs(T_d / T_OR - 1.0) <= TOL['period'])
    nu_ok = judged['nu'] & (R_d * R_OR > 0) & (np.abs(R_d / R_OR - 1.0) <= TOL['nu'])

    res = {
        'precession_pass_fraction': float(prec_pass.sum() / max(judged['prec'].sum(), 1)),
        'period_pass_fraction': float(period_pass.sum() / max(judged['period'].sum(), 1)),
        'nu_effect_pass_fraction': float(nu_ok.sum() / max(judged['nu'].sum(), 1)),
        'min_judged_seeds': int(min(judged['prec'].sum(), judged['period'].sum(), judged['nu'].sum())),
        '_judged': {k: int(v.sum()) for k, v in judged.items()},
        '_excluded_A': {'prec': int((~judged['prec']).sum()), 'period': int((~judged['period']).sum()),
                        'nu': int((~judged['nu']).sum())},
        '_judgedB_prec': int((EPS_PREC_B <= 0.5 * TOL['prec']).sum()),
        '_passB_prec': int(((EPS_PREC_B <= 0.5 * TOL['prec']) &
                            (np.abs(adv / DPHI_OR - 1.0) <= TOL['prec'])).sum()),
    }
    out[mode] = res
    print(mode, json.dumps(res))

np.savez('binaries.npz', P=P, E=E_, NU=NU, DPHI_OR=DPHI_OR, T_OR=T_OR, R_OR=R_OR,
         EPS_PREC=EPS_PREC, EPS_PERIOD=EPS_PERIOD, EPS_PREC_B=EPS_PREC_B)
with open('binaries_summary.json', 'w') as f:
    json.dump(out, f, indent=1)
print("saved.")
