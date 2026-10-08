#!/usr/bin/env python3
"""Decisive runs: (A) surprise-time atlas for several mu, (B) kick-cadence sweep.

Usage: python3 runs.py atlas | cadence | heldout
Saves npz + json into this folder.
"""
import numpy as np, json, time, sys, os
import surprise as S

OUT = os.path.dirname(os.path.abspath(__file__))
TWOPI = 2 * np.pi


def belt_bins(a_lo, a_hi, da, phases, seed):
    a = np.arange(a_lo, a_hi + 1e-9, da)
    return a, phases, seed


# ---------------- A: atlas ----------------
def do_atlas():
    res = {}
    for mu in [1e-5, 1e-4, 3e-4, 1e-3]:
        a, ph, seed = belt_bins(0.60, 0.98, 0.005, 4, 20261008)
        r = S.atlas(a, ph, mu, T_orb=2000, sample_every=4, hdiv=64, seed=seed)
        res[f"mu_{mu:g}"] = r
        print(f"mu={mu:g} wall={r['wall']:.0f}s finite={np.isfinite(r['tdiv']).mean():.0%}")
    # instrument check: hdiv=96 vs 64 at mu=1e-4
    a, ph, seed = belt_bins(0.80, 0.95, 0.005, 4, 20261008)
    r64 = S.atlas(a, ph, 1e-4, 2000, 4, hdiv=64, seed=99)
    r96 = S.atlas(a, ph, 1e-4, 2000, 4, hdiv=96, seed=99)
    res["hchk_64"] = r64
    res["hchk_96"] = r96
    np.savez_compressed(os.path.join(OUT, "atlas.npz"),
                        **{k: v["tdiv"] for k, v in res.items()},
                        **{f"{k}_a": v["a"] for k, v in res.items()})
    meta = {k: {kk: vv for kk, vv in v.items() if kk != "tdiv"} for k, v in res.items()}
    json.dump(meta, open(os.path.join(OUT, "atlas_meta.json"), "w"), indent=1, default=float)
    d64, d96 = np.log10(r64["tdiv"][np.isfinite(r64["tdiv"]) & np.isfinite(r96["tdiv"])]), \
               np.log10(r96["tdiv"][np.isfinite(r64["tdiv"]) & np.isfinite(r96["tdiv"])])
    print("hdiv instrument check: median |dlog10 T_div| = %.3f (n=%d)" %
          (np.median(np.abs(d64 - d96)), len(d64)))


# ---------------- B: cadence ----------------
def make_scene(mu, e0_sigma, seed, a_hi=0.95):
    rng = np.random.default_rng(seed)
    a = np.repeat(np.arange(0.60, a_hi + 1e-9, 0.005), 4)
    n = a.size
    e0 = rng.rayleigh(e0_sigma, n)
    # reject planet-crossing births (apoapsis >= 0.99)
    bad = a * (1 + e0) >= 0.99
    while bad.any():
        e0[bad] = rng.rayleigh(e0_sigma, bad.sum())
        bad = a * (1 + e0) >= 0.99
    w0 = rng.uniform(0, TWOPI, n)
    M0 = rng.uniform(0, TWOPI, n)
    return a, e0, w0, M0


def truth_with_series(a0, e0, w0, M0, mu, T_orb, hdiv):
    """Per-body adaptive-h leapfrog truth: h shrinks near the planet so
    encounter arcs are resolved; elements sampled ~per body orbit."""
    r, v = S.init_belt(a0, e0, w0, M0)
    n = a0.size
    npp = S.n_pl(mu)
    t = np.zeros(n)
    act = np.ones(n, bool)
    Cj0 = S.jacobi(r, v, 0.0, mu)
    maxdc = np.zeros(n)
    dmin = np.full(n, 9.9)
    ai, ei, wi = S.elems(r, v)
    w_tot = np.zeros(n); w_last = wi.copy()
    a_fin = ai.copy(); e_fin = ei.copy()
    samp_last = np.zeros(n)
    t0 = time.time()
    while act.any():
        idx = np.nonzero(act)[0]
        ri, vi, ti = r[idx], v[idx], t[idx]
        dx = np.cos(npp * ti) - ri[:, 0]
        dy = np.sin(npp * ti) - ri[:, 1]
        d = np.sqrt(dx * dx + dy * dy)
        dmin[idx] = np.minimum(dmin[idx], d)
        s = np.clip((d - 0.01) / 0.10, 0.02, 1.0)
        h = (TWOPI / hdiv) * s
        v_i = vi + 0.5 * h[:, None] * S.a_full(ri, ti, mu)
        ri = ri + h[:, None] * v_i
        ti = ti + h
        v_i = v_i + 0.5 * h[:, None] * S.a_full(ri, ti, mu)
        r[idx], v[idx], t[idx] = ri, v_i, ti
        done = ti >= T_orb * TWOPI
        act[idx[done]] = False
        maxdc[idx] = np.maximum(maxdc[idx], np.abs(S.jacobi(ri, v_i, ti, mu) - Cj0[idx]))
        asamp = S.elems(ri, v_i)[0] ** 1.5
        asamp = np.where(np.isfinite(asamp), asamp, 0.25)
        due = (ti - samp_last[idx]) > 0.25 * TWOPI * asamp
        take = idx[due]
        if take.size:
            aa, ee, ww = S.elems(r[take], v[take])
            dw = ww - w_last[take]
            dw = (dw + np.pi) % TWOPI - np.pi
            w_tot[take] += dw
            w_last[take] = ww
            a_fin[take] = aa
            e_fin[take] = ee
            samp_last[take] = t[take]
    return dict(a=a_fin, e=e_fin, w_tot=w_tot, maxdc=maxdc, Cj0=Cj0, dmin=dmin,
                wall=time.time() - t0)
def cadence_with_series(a0, e0, w0, M0, mu, T_orb, kvec, samp_every_kicks=4):
    r, v = S.init_belt(a0, e0, w0, M0)
    n = a0.size
    P = TWOPI * a0 ** 1.5
    h = P / kvec
    Cj0 = S.jacobi(r, v, 0.0, mu)
    maxdc = np.zeros(n)
    ai, ei, wi = S.elems(r, v)
    w_tot = np.zeros(n); w_last = wi.copy()
    a_fin = ai.copy(); e_fin = ei.copy()
    stepk = np.zeros(n, dtype=int)
    t = np.zeros(n)
    act = np.ones(n, bool)
    t0 = time.time()
    while act.any():
        idx = np.nonzero(act)[0]
        ri, vi, hi, ti = r[idx], v[idx], h[idx], t[idx]
        vi = vi + 0.5 * hi[:, None] * S.a_pert(ri, ti, mu)
        ri, vi, _ = S.drift(ri, vi, hi)
        ti = ti + hi
        vi = vi + 0.5 * hi[:, None] * S.a_pert(ri, ti, mu)
        r[idx], v[idx], t[idx] = ri, vi, ti
        stepk[idx] += 1
        if True:
            take = (stepk[idx] % samp_every_kicks) == 0
            if take.any():
                aa, ee, ww = S.elems(ri[take], vi[take])
                dw = ww - w_last[idx][take]
                dw = (dw + np.pi) % TWOPI - np.pi
                w_tot[idx[take]] += dw
                w_last[idx[take]] = ww
                a_fin[idx[take]] = aa
                e_fin[idx[take]] = ee
        maxdc[idx] = np.maximum(maxdc[idx], np.abs(S.jacobi(ri, vi, ti, mu) - Cj0[idx]))
        done = ti >= T_orb * TWOPI
        act[idx[done]] = False
    return dict(a=a_fin, e=e_fin, w_tot=w_tot, maxdc=maxdc, nkicks=stepk, dmin=None,
                wall=time.time() - t0)


def do_cadence():
    mu = 1e-3
    T_orb = 200
    ks = [2, 4, 8, 16, 32, 64]
    out = {}
    for tag, esig, seed in [("belt02", 0.02, 7), ("belt10", 0.1, 11)]:
        a0, e0, w0, M0 = make_scene(mu, esig, seed)
        tr = truth_with_series(a0, e0, w0, M0, mu, T_orb, hdiv=1024)
        out[f"{tag}_truth"] = dict(a=tr["a"], e=tr["e"], w_tot=tr["w_tot"],
                                   maxdc=tr["maxdc"], dmin=tr["dmin"])
        # cross-check: DKD-Kepler family at k=512 on a subset vs LF truth
        sub = np.arange(0, a0.size, 5)
        c512 = cadence_with_series(a0[sub], e0[sub], w0[sub], M0[sub], mu, T_orb,
                                   np.full(sub.size, 512))
        dC = np.max(np.abs(c512["maxdc"] - tr["maxdc"][sub]))
        dW = np.max(np.abs(c512["w_tot"] - tr["w_tot"][sub]))
        print(f"{tag}: truth wall={tr['wall']:.0f}s xcheck DKD512 vs LF1024 dC={dC:.1e} dW={dW:.2e}",
              flush=True)
        for k in ks:
            c = cadence_with_series(a0, e0, w0, M0, mu, T_orb, np.full(a0.size, k))
            out[f"{tag}_k{k}"] = dict(a=c["a"], e=c["e"], w_tot=c["w_tot"], maxdc=c["maxdc"],
                                      nkicks=c["nkicks"])
            print(f"{tag} k={k}: wall={c['wall']:.0f}s med maxdc={np.median(c['maxdc']):.1e} "
                  f"p95={np.quantile(c['maxdc'],0.95):.1e}", flush=True)
        out[f"{tag}_scene"] = dict(a=a0, e0=e0, w0=w0, M0=M0)
    np.savez_compressed(os.path.join(OUT, "cadence.npz"),
                        **{k: np.asarray(v, dtype=float) for k, v in out.items()})
if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "atlas"
    if what == "atlas":
        do_atlas()
    elif what == "cadence":
        do_cadence()
    elif what == "heldout":
        pass
