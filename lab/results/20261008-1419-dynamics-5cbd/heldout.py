#!/usr/bin/env python3
"""Held-out verification: mu=3e-4 scene, adaptive rule fitted on mu=1e-3 only."""
import numpy as np, os, time
import surprise as S
import runs
from runs import make_scene, truth_with_series, cadence_with_series, OUT, TWOPI


def tdiv_lookup(mu_tag, a_bins):
    """median T_div per a-bin from atlas (bin = 4 phases)."""
    z = np.load(os.path.join(OUT, "atlas.npz"))
    td = z[f"mu_{mu_tag:g}"]
    a = z[f"mu_{mu_tag:g}_a"]
    bins = np.unique(a)
    med = np.array([np.median(td[a == b]) if np.any(np.isfinite(td[a == b]))
                    else np.inf for b in bins])
    cens = np.array([np.all(~np.isfinite(td[a == b])) for b in bins])
    return bins, med, cens


def rule_kicks(T_div_med, a_bin, C, kmin=4, kmax=128):
    P = TWOPI * a_bin ** 1.5  # body period; T_div in same 2pi units
    k = np.ceil(C * P / np.where(np.isfinite(T_div_med), T_div_med, 1e9))
    return np.clip(k, kmin, kmax).astype(int)


if __name__ == "__main__":
    mu = 3e-4
    T_orb = 200
    a0, e0, w0, M0 = make_scene(mu, 0.02, 23)
    bins, med, cens = tdiv_lookup(3e-4, None)
    bidx = np.searchsorted(bins, a0)
    print("scene bins with censored T_div: %d/%d" % (cens[bidx].sum(), len(bidx)))
    tr = truth_with_series(a0, e0, w0, M0, mu, T_orb, hdiv=1024)
    print("truth wall %.0fs maxdc(q)=%s" % (tr["wall"], np.percentile(tr["maxdc"], [50, 95, 99])))
    out = dict(a0=a0, e0=e0, truth=dict(a=tr["a"], e=tr["e"], w_tot=tr["w_tot"],
                                        maxdc=tr["maxdc"], dmin=tr["dmin"]))
    for k in [2, 4, 8, 16, 32]:
        c = cadence_with_series(a0, e0, w0, M0, mu, T_orb, np.full(a0.size, k))
        out[f"k{k}"] = dict(maxdc=c["maxdc"], a=c["a"], e=c["e"], w_tot=c["w_tot"],
                            nkicks=c["nkicks"])
        print("k=%d med=%.1e p95=%.1e" % (k, np.median(c["maxdc"]), np.quantile(c["maxdc"], .95)))
    np.savez_compressed(os.path.join(OUT, "heldout.npz"),
                        **{k: np.asarray(v, dtype=float) for k, v in out.items()})
