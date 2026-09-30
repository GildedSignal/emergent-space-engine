"""Scaling runs: sigma_e = 1e-2, rho = 1e-4*(1e4/N), N in {1e3,1e4,1e5,1e6},
T = 20 periods. Events per configuration:

- element-sort: exact phase-and-density-averaged aggregation,
  events = N^2/2 * E_pairs[2*(|dn|*T/2pi) * 1[co-listed]],
  co-listed ~ |da| <= a_i e_i + a_j e_j + 2*rho + 1.5*W (bin-index ranges
  intersect), estimated by 2e6-pair Monte Carlo on the population measure.
  Validated against the sampled-belt exact count at N=1e3/1e4.
- shear-grid: per-body cell-change rate (mean over 2e4 sampled bodies,
  exact per-body formula), events = N*(1 + 20*E_body). N-independent rate.
- ring-cells: N*(1+occ) + 20*(sum of per-body crossings)*(1+occ),
  occ = N/2048; per-body crossings = 128 + 2*levels(r-range) on the fixed
  16x128 grid.
- oracle: exact truth at N in {1e3, 3162, 1e4} (full reference machinery).
"""
import json, random, time
import numpy as np
from common import *

SIGMA_E = 1e-2
NS = [1000, 10000, 100000, 1000000]
NS_ORACLE = [1000, 3162, 10000]
T = T_TOTAL
ORBITS = T / TWOPI

def belt_at(N):
    rng = random.Random(20261008)
    rho = 1e-4 * (1e4 / N)
    a, e, varpi, lam0 = sample_belt(rng, N, SIGMA_E)
    return a, e, varpi, lam0, rho

def exact_belt(N):
    a, e, varpi, lam0, rho = belt_at(N)
    res = analyse_belt(a, e, varpi, lam0, rho, T=T)
    return res, a, e, rho

def es_events_mc(N, W):
    """N^2/2 * E[2*crossings * co-listed] by Monte Carlo on the population."""
    rho = 1e-4 * (1e4 / N)
    rng = np.random.default_rng(20260930 + int(np.log10(N)))
    M = 2_000_000
    ai = rng.uniform(1.0, 1.5, M); ei = SIGMA_E * rng.rayleigh(M)
    aj = rng.uniform(1.0, 1.5, M); ej = SIGMA_E * rng.rayleigh(M)
    da = np.abs(ai - aj)
    colist = da <= ai * ei + aj * ej + 2 * rho + 1.5 * W
    dn = np.abs(ai ** -1.5 - aj ** -1.5)
    return (N * N / 2.0) * float(np.mean(2.0 * dn * T / TWOPI * colist))

def shear_events_mc(N):
    rho = 1e-4 * (1e4 / N)
    rng = random.Random(4242)
    a, e, varpi, lam0 = sample_belt(rng, 20000, SIGMA_E)
    n = a ** -1.5
    base_r = float((a * (1 - e)).min() - rho - 1e-9)
    Eb = shear_events_per_body(a, e, varpi, lam0, n, rho, T, base_r)
    return N * (1.0 + ORBITS * Eb), Eb

def ring_events_mc(N):
    rho = 1e-4 * (1e4 / N)
    rng = np.random.default_rng(20260930)
    M = 200000
    a = rng.uniform(1.0, 1.5, M); e = SIGMA_E * rng.rayleigh(M)
    r0 = float((a * (1 - e)).min() - rho - 1e-9)
    r1 = float((a * (1 + e)).max() + rho + 1e-9)
    w_ring = (r1 - r0) / 16.0
    Nlev = np.maximum(np.floor((a * (1 + e) - r0) / w_ring) -
                      np.ceil((a * (1 - e) - r0) / w_ring) + 1.0, 0.0)
    cross = 128.0 + 2.0 * Nlev
    occ = N / 2048.0
    return N * (1.0 + occ) + ORBITS * float(np.sum(cross)) * (M and (1.0 + occ)) * (N / M)

def main():
    out = {"notes": "sigma_e=1e-2, rho=1e-4*(1e4/N), T=20 periods at a=1"}
    t0 = time.time()
    # ---- exact small-N belts: oracle truth + validation of aggregations
    ex = {}
    for N in NS_ORACLE:
        res, a, e, rho = exact_belt(N)
        ex[N] = res
        print(f"N={N}: ref={res['ref_encounters']} es_events={res['element-sort']['events']:.0f} "
              f"sh_events={res['shear-grid']['events']:.3e} rc_events={res['ring-cells']['events']:.3e} "
              f"[{time.time()-t0:.0f}s]")
    W_pop = 2 * 1.25 * SIGMA_E * np.sqrt(2 * np.log(2))  # population median of 2ae (+2rho below)
    # oracle scaling numbers
    oracle_events = {N: float(ex[N]['ref_encounters']) for N in NS_ORACLE}
    # element-sort aggregation + validation
    es_vals, es_val = {}, {}
    for N in NS:
        rho = 1e-4 * (1e4 / N)
        W = W_pop + 2 * rho
        if N in ex:   # validate against the sampled belt's exact count
            a, e, _, _, rho_b = belt_at(N)
            W_belt = max(rho_b, float(np.median(2 * a * e + 2 * rho_b)))
            mc = es_events_mc(N, W_belt)
            es_val[N] = dict(exact=ex[N]['element-sort']['events'], mc=mc,
                             rel=abs(mc - ex[N]['element-sort']['events']) / ex[N]['element-sort']['events'])
            print(f"element-sort validation N={N}: exact={es_val[N]['exact']:.0f} mc={mc:.0f} "
                  f"rel={es_val[N]['rel']:.3f}")
        es_vals[N] = es_events_mc(N, W)
    # shear + ring
    sh_vals, rc_vals, Ebys = {}, {}, {}
    for N in NS:
        sh_vals[N], Ebys[N] = shear_events_mc(N)
        rc_vals[N] = ring_events_mc(N)
    out['events'] = {"element-sort": es_vals, "shear-grid": sh_vals,
                     "ring-cells": rc_vals, "oracle": oracle_events}
    out['validation'] = {"element-sort": es_val}
    out['shear_Ebody'] = Ebys
    # exponents
    exps = {}
    for cfg, vals in out['events'].items():
        Ns = np.array(sorted(vals), float)
        ev = np.array([vals[int(n)] for n in Ns], float)
        exps[cfg] = float(np.polyfit(np.log10(Ns), np.log10(ev), 1)[0])
    out['scale_exponent'] = exps
    with open('scaling.json', 'w') as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out['scale_exponent'], indent=1))
    print(f"total {time.time()-t0:.0f}s")

if __name__ == '__main__':
    main()
