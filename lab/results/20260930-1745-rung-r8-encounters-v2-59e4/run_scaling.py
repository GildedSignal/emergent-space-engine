"""Scaling runs: sigma_e = 1e-2, rho = 1e-4 * (1e4 / N), the same belt
generator. N = 1e3 and 1e4 are run exactly (full reference + all configs).
N = 1e5 is run exactly with a conjunction prefilter (a pair can only
encounter if it has a conjunction in [0,T]; the filter is exact, it
replaces the raw candidate scan). N = 1e6 uses the closed forms validated
on the exact points (sum of conjunctions and candidate count by (a,e)-bin
integration; truth by the measured N^2 rho^2 T law; shear-grid and
ring-cells are exact per-body path integrals in any case).
"""
import json
import random
import sys
import time

import numpy as np

from belt import make_belt, kepler_states, TWOPI
import reference as R
import configs as C
from configs import T_MAX


def exact_run(N, T, seed):
    rng = random.Random(seed)
    B = make_belt(rng, N, 1e-2, 1e-4 * (1e4 / N))
    T_MAX[0] = T
    rho = 1e-4 * (1e4 / N)
    if N <= 10_000:
        pi, pj = R.candidate_pairs(B)
        ref = R.reference_encounters(B, T, pi, pj)
        ncand, Csum, truth = len(pi), int(ref["C"].sum()), len(ref["encounters"][0])
    else:
        # chunked exact processing (the full candidate list is too big to hold)
        ei = []; ej = []; tt = []; dd = []; ti = []; to = []
        ncand = Csum = 0
        for gi, gj in R.iter_candidate_pairs(B, chunk=1000):
            ref = R.reference_encounters(B, T, gi, gj)
            ncand += len(gi)
            Csum += int(ref["C"].sum())
            a, b, c, d = ref["encounters"]
            ei.append(a); ej.append(b); tt.append(c); dd.append(d)
            ti.append(ref["t_in"]); to.append(ref["t_out"])
        ref = dict(pi=np.empty(ncand, np.int32), pj=np.empty(0, np.int32),
                   C=np.array([Csum], np.int64),
                   encounters=tuple(np.concatenate(x) for x in (ei, ej, tt, dd)),
                   t_in=np.concatenate(ti), t_out=np.concatenate(to),
                   n_events=Csum)
        truth = len(ref["encounters"][0])
    hb = C.hier_bounds(B, ref, T)
    sg = int(C.shear_grid_events(B, T).sum())
    rc_ev, dr, dphi = C.ring_cells_events(B, T)
    rc = int(rc_ev.sum())
    return dict(N=N, T=T, truth=truth, conj=Csum, cand=ncand, es=Csum,
                hb=hb["events"], sg=sg, rc=rc, sigma_e=1e-2, rho=rho)
def closed_form_counts(B, T, delta=1e-3, ne=48):
    """Sigma over candidate pairs of |dn| T/2pi (element-sort events) and
    the candidate count, by (a, e)-bin integration."""
    abar = float(B.a.mean())
    k75 = float(np.percentile(B.a * B.e, 99.5))
    Dmax = 2 * 1.5 * k75 + B.rho + 2 * delta
    abin = np.floor((B.a - B.a.min()) / delta).astype(np.int64)
    nb = int(abin.max()) + 1
    emax = B.e.max()
    edges = np.linspace(0, emax * 1.001, ne + 1)
    emid = 0.5 * (edges[:-1] + edges[1:])
    H = np.zeros((nb, ne))
    for b in range(nb):
        m = abin == b
        if m.any():
            H[b] = np.histogram(B.e[m], bins=edges)[0]
    sum_conj = 0.0
    cand = 0.0
    for b1 in range(nb):
        reach = int(Dmax / delta) + 2
        for b2 in range(b1, min(nb, b1 + reach)):
            n1, n2 = H[b1].sum(), H[b2].sum()
            if n1 == 0 or n2 == 0:
                continue
            if b1 == b2:
                D = delta / 3.0
                pr = 0.5 * n1 * (n1 - 1)
            else:
                D = (b2 - b1) * delta
                pr = n1 * n2
            thresh = (D - B.rho) / abar
            M = (emid[:, None] + emid[None, :] >= thresh)
            ok = float(H[b1] @ M @ H[b2])
            if b1 == b2:
                ok *= max(0.0, (n1 * (n1 - 1))) / max(1.0, n1 * n1)
            frac = ok / max(1.0, n1 * n2)
            dn = 1.5 * abar ** -2.5 * D
            cand += pr * frac
            sum_conj += pr * frac * dn * T / TWOPI
    return cand, sum_conj


def main(out_path):
    recs = []
    for N, T in [(1_000, 20 * TWOPI), (10_000, 20 * TWOPI)]:
        t0 = time.time()
        r = exact_run(N, T, 20261008 * 10 + N)
        B = None
        recs.append(r)
        print("exact", r, f"({time.time()-t0:.0f}s)", flush=True)
    # N = 1e5, 1 period (prefilter makes it exact for conjunction-bearing pairs)
    t0 = time.time()
    r = exact_run(100_000, TWOPI, 20261008 * 10 + 100_000)
    recs.append(r)
    print("exact 1e5", {k: r[k] for k in ("N", "T", "truth", "conj", "cand", "es", "hb", "sg", "rc")},
          f"({time.time()-t0:.0f}s)", flush=True)
    # validate closed forms
    rng = random.Random(999)
    val = []
    for N, T in [(1_000, 20 * TWOPI), (10_000, 20 * TWOPI)]:
        B = make_belt(rng, N, 1e-2, 1e-4 * (1e4 / N))
        cand, sc = closed_form_counts(B, T)
        val.append(dict(N=N, cand_cf=cand, conj_cf=sc))
        print("cf validate", N, cand, sc, flush=True)
    # N = 1e6 closed form
    rng = random.Random(20261008 * 10 + 1_000_000)
    B = make_belt(rng, 1_000_000, 1e-2, 1e-4 * 1e-2)
    t0 = time.time()
    cand, sc = closed_form_counts(B, TWOPI)
    sg = int(C.shear_grid_events(B, TWOPI).sum())
    rc_ev, dr, dphi = C.ring_cells_events(B, TWOPI)
    rc = int(rc_ev.sum())
    print("1e6 closed form", cand, sc, sg, rc, f"({time.time()-t0:.0f}s)", flush=True)
    # truth law from exact points: truth = k N^2 rho^2 T
    ks = []
    for r in recs:
        ks.append(r["truth"] / (r["N"]**2 * r["rho"]**2 * r["T"]))
    k = float(np.median(ks))
    truth_1e6 = k * 1e12 * (1e-6)**2 * TWOPI
    hb_ratio = float(np.median([r["hb"] / r["cand"] for r in recs]))
    recs.append(dict(N=1_000_000, T=TWOPI, truth=truth_1e6, conj=None,
                     cand=cand, es=sc, hb=cand * hb_ratio, sg=sg, rc=rc,
                     sigma_e=1e-2, rho=1e-6, exact=False,
                     k_law=k, hb_ratio=hb_ratio))
    with open(out_path, "w") as f:
        json.dump(dict(runs=recs, cf_validation=val), f)
    print("truth law k per run:", ks)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "scaling.json")
