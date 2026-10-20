#!/usr/bin/env python3
"""The sky-cell one-shift readout on the observer's-own-gamma channel.

Premise under test (docs/representation.md L59, S6 view row): "Aggregates are one sample each,
and the screen caps the work at about one sample per pixel". Cold sky: every emitter at rest in
the sky frame (zero velocity dispersion). The observer's own aberration spreads k across a sky
cell; one shift per cell cannot represent k^4 brightness and k*T colour at the game's gamma.

Frames: sky frame S; observer moves at +beta along z. Emitter (at rest in S) at polar angle
theta_s (0 = dead ahead). Exact SR:  k = gamma*(1 + beta*cos(theta_s))  [blueshift ahead],
observed polar angle  cos(theta') = (cos(theta_s) + beta)/(1 + beta*cos(theta_s)).
k depends only on theta', so every cell in a ring of width theta_f shares one k-distribution
(for phi-uniform members); ring-level analysis is exact for the premise.

Readouts per ring (equal emitted luminosity per member):
  R1a mean k            (the record's lum-weighted shift, emitted-lum weighting)
  R1b seen-flux-weighted mean k = sum(k^5)/sum(k^4)   (lum-weighted by seen flux)
  R2   k at the ring's centre angle (analytic)
  R3   brightness-oracle k = <k^4>^(1/4)   (exact brightness; colour errs)
  R4   colour-oracle k = exp(<ln k>)       (exact colour; brightness errs)
Channels: brightness rel.err = |kbar^4*n - sum(k^4)| / sum(k^4); colour gap in octaves
log2(k3/k4). Cure arm: per-ring equal-ln-k histogram, B bins over the ring's [k_min,k_max].
"""
import json
import os
import platform
import numpy as np


def wquantile(v, q, w):
    order = np.argsort(v)
    cw = np.cumsum(w[order])
    cw = cw / cw[-1]
    return v[order][np.searchsorted(cw, q)]

GAMMAS = [1.0001, 1.33, 2.0, 5.0, 10.0, 22.0, 50.0, 125.0, 250.0, 500.0, 1000.0, 2000.0, 1.0e6]
FLOORS = {"stock_8e-3": 8e-3, "fine_1e-3": 1e-3}
NS = 2_000_000
BINS_CURE = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]


def rings(gamma, theta_f, seed=20261020):
    beta = np.sqrt(1.0 - 1.0 / gamma**2)
    rng = np.random.default_rng(seed)
    u = rng.uniform(-1.0, 1.0, NS)              # cos(theta_s), isotropic sky
    k = gamma * (1.0 + beta * u)                # exact Doppler, source at rest
    ctp = (u + beta) / (1.0 + beta * u)         # cos(theta')
    tp = np.arccos(np.clip(ctp, -1.0, 1.0))
    idx = np.minimum((tp / theta_f).astype(np.int64), int(np.pi / theta_f))
    n = np.bincount(idx)
    s1 = np.bincount(idx, weights=k)
    s4 = np.bincount(idx, weights=k**4)
    s5 = np.bincount(idx, weights=k**5)
    sl = np.bincount(idx, weights=np.log(k))
    # exact k-span per ring from the monotone k(theta') = 1/(gamma*(1-beta*cos theta'))
    edges = np.arange(len(n) + 1) * theta_f
    lo = np.minimum(edges[:-1], np.pi)
    hi = np.minimum(edges[1:], np.pi)
    # k at ring centre (analytic); for the last partial ring use the covered centre
    mid = np.minimum((lo + hi) / 2.0, np.pi)
    span = np.minimum((1.0 - beta * np.cos(hi)), np.inf) / (1.0 - beta * np.cos(lo))  # k(lo)/k(hi) >= 1
    kc = 1.0 / (gamma * (1.0 - beta * np.cos(mid)))
    return n, s1, s4, s5, sl, span, kc, tp, idx, k, beta, gamma


def readout_errors(n, s1, s4, s5, sl, kc):
    r1a = s1 / n
    r1b = s5 / s4
    r3 = (s4 / n) ** 0.25
    r4 = np.exp(sl / n)
    err = lambda kb: np.abs(kb**4 * n - s4) / np.maximum(s4, 1e-300)
    return {
        "R1a_mean": err(r1a),
        "R1b_seenw": err(r1b),
        "R2_centre": err(kc),
        "R3_bright_oracle": err(r3),
        "R4_colour_oracle": err(r4),
        "colour_gap_oct_R3": np.abs(np.log2(np.maximum(r3, 1e-300) / np.maximum(r4, 1e-300))),
    }


def main():
    state = {
        "nproc": os.cpu_count(),
        "load": os.getloadavg(),
        "machine": platform.platform(),
    }
    out = {"state": state, "floors": {}}
    for fname, theta_f in FLOORS.items():
        rows = []
        for g in GAMMAS:
            n, s1, s4, s5, sl, span, kc, tp, idx, k, beta, _ = rings(g, theta_f)
            with np.errstate(divide="ignore", invalid="ignore"):
                ro = readout_errors(n, s1, s4, s5, sl, kc)
            valid = n > 0
            flux = np.zeros_like(s4)
            flux[valid] = s4[valid] / s4.sum()
            fwd = 0  # forward ring index
            row_err = lambda key: float(ro[key][fwd]) if valid[fwd] else None
            # cure: histogram readout on the forward ring
            m = idx == fwd
            kf, kf4 = k[m], k[m] ** 4
            if kf.size >= 30:
                lmin, lmax = np.log(kf.min()), np.log(kf.max())
                cure = {"n": int(kf.size)}
                for B in BINS_CURE:
                    edges = np.linspace(lmin, lmax, B + 1)
                    which = np.clip(np.searchsorted(edges, np.log(kf), side="right") - 1, 0, B - 1)
                    w = np.bincount(which, minlength=B)
                    kc4 = np.exp(4.0 * (edges[:-1] + edges[1:]) / 2.0)
                    approx = float((w * kc4).sum())
                    cure[B] = abs(approx - kf4.sum()) / kf4.sum()
            else:
                cure = {"n": int(kf.size), "sparse": True}
            # error concentration: share of per-sample R1a brightness error beyond theta' > 2/gamma
            cut = min(2.0 / g, np.pi)
            per = np.abs(ro["R1a_mean"][idx] ** 4 - k**4)
            per = np.nan_to_num(per)
            share_beyond = float(per[tp > cut].sum() / per.sum())
            rows.append({
                "gamma": g,
                "beta": beta,
                "fwd_n": int(n[fwd]),
                "fwd_R1a": row_err("R1a_mean"),
                "fwd_R1b": row_err("R1b_seenw"),
                "fwd_R2": row_err("R2_centre"),
                "fwd_R4_colour_true": row_err("R4_colour_oracle"),
                "fwd_colour_gap_oct": row_err("colour_gap_oct_R3"),
                "fwd_k_span": float(span[fwd]),
                "fwd_flux_share": float(flux[fwd]),
                "p99_R1a_fluxw": float(wquantile(ro["R1a_mean"][valid], 0.99, (flux * n)[valid])),
                "mean_R1a_fluxw": float(np.average(ro["R1a_mean"][valid], weights=(flux * n)[valid])),
                "err_share_beyond_2overgamma": share_beyond,
                "fwd_hist_cure": cure,
            })
        out["floors"][fname] = rows
    # quadrature cross-check of the forward span law at a few gammas (exact formula),
    # and the exact gamma at which the forward ring's k-span crosses 2 (halving)
    chk = []
    for g in [50.0, 125.0, 250.0, 500.0, 1000.0, 2000.0]:
        beta = np.sqrt(1.0 - 1.0 / g**2)
        for fname, w in FLOORS.items():
            th = min(w, np.pi)
            span = (1.0 - beta * np.cos(th)) / (1.0 - beta)
            chk.append({"gamma": g, "floor": fname, "fwd_span_exact": span})
    for fname, w in FLOORS.items():
        lo_g, hi_g = 1.0, 1e8
        for _ in range(80):
            mid_g = np.sqrt(lo_g * hi_g)
            b = np.sqrt(1.0 - 1.0 / mid_g**2)
            sp = (1.0 - b * np.cos(w)) / (1.0 - b)
            if sp > 2.0:
                hi_g = mid_g
            else:
                lo_g = mid_g
        chk.append({"floor": fname, "halving_gamma_exact": float(np.sqrt(lo_g * hi_g))})
    out["span_check"] = chk
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json"), "w") as f:
        json.dump(out, f, indent=1)
    # console digest
    for fname, rows in out["floors"].items():
        print(f"== floor {fname} (theta_f={FLOORS[fname]}) ==")
        print("  gamma      fwd R1a    fwd R1b    fwd R4col   gap(oct)  k-span    fluxshare  p99R1a   errB>2/g")
        for r in rows:
            def pct(x):
                return f"{x:>9.4%}" if x is not None else "    sparse"
            print(f"  {r['gamma']:>8.4g}  {pct(r['fwd_R1a'])}  {pct(r['fwd_R1b'])}  "
                  f"{pct(r['fwd_R4_colour_true'])}  "
                  f"{r['fwd_colour_gap_oct'] if r['fwd_colour_gap_oct'] is not None else float('nan'):>8.4f}  "
                  f"{r['fwd_k_span']:>8.4g}  {r['fwd_flux_share']:>9.4%}  {r['p99_R1a_fluxw']:>9.4%}  "
                  f"{r['err_share_beyond_2overgamma']:>7.3f}")


if __name__ == "__main__":
    main()
