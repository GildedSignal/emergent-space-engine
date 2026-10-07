#!/usr/bin/env python3
"""Battery 2: (a) workable-R reruns of empty/dilute scenes; (b) R-scan on a
broken scene (defense: does bigger R rescue rank?); (c) mechanism test: at the
encounter instant t*, is the pair's true-anomaly separation ~0 (aligned,
same-map co-location) or ~+/-Delta-omega (apsidal co-location), while their
mean-anomaly separation (the certificate's coordinate) is large?; (d) seed
robustness of k*."""
import json
import numpy as np
import coorb_probe as cp

TWO_PI = 2 * np.pi


def nu_of_E(E, e):
    e_ = e[:, None] if E.ndim == 2 else e
    return 2 * np.arctan2(np.sqrt(1 + e_) * np.sin(E / 2), np.sqrt(1 - e_) * np.cos(E / 2))


def run(name, spec, n, T, R, seed):
    bod = cp.make_scene(spec, n, seed)
    P = cp.positions(bod, T)
    mind = cp.truth_min_dist(P)
    enc = np.triu(mind < R, 1)
    n_enc = int(enc.sum())
    rank = cp.cert_phase(bod)
    out = dict(scene=name, R=R, n=n, seed=seed, n_enc=n_enc,
               setup_shell=cp.shell_setup_count(bod["e"], bod["a"], R))
    if n_enc:
        rr = rank[enc]
        out["k_star"] = int(rr.max())
        out["miss4"] = float((rr > 4).mean())
        out["miss_k_over_n"] = out["k_star"] / (n / 2)
    # mechanism: anomaly separations at the encounter instant
    if n_enc:
        M0 = bod["M0"]
        t = np.linspace(0, TWO_PI, T, endpoint=False)
        # recompute E(t) and nu(t)
        e = bod["e"][:, None]
        M = M0[:, None] + t[None, :]
        E = M.copy()
        for _ in range(10):
            E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
        nu = np.mod(nu_of_E(E, bod["e"]), TWO_PI)
        ii, jj = np.nonzero(enc)
        dnu_star, dM_star = [], []
        for i, j in zip(ii, jj):
            d = np.sqrt(((P[i] - P[j]) ** 2).sum(-1))
            ts = int(d.argmin())
            dnu_star.append(np.abs(nu[i, ts] - nu[j, ts]))
            dM_star.append(np.abs(np.mod(M[i, ts] - M[j, ts] + np.pi, TWO_PI) - np.pi))
        dnu_star = np.array(dnu_star); dM_star = np.array(dM_star)
        dom = cp.circ_diff(bod["om"])[ii, jj]
        wrap = lambda x: np.minimum(x, TWO_PI - x)
        out["med_dnu_star_deg"] = float(np.median(wrap(dnu_star)) / np.pi * 180)
        out["med_dM_star_deg"] = float(np.median(wrap(dM_star)) / np.pi * 180)
        out["med_domega_deg"] = float(np.median(dom) / np.pi * 180)
        out["frac_dnu_lt_2deg"] = float((wrap(dnu_star) < 2 * np.pi / 180).mean())
        out["med_rank_dM0"] = float(np.median(rank[ii, jj]))
    print(json.dumps(out), flush=True)
    return out


S = cp.SCENES
res = []
# (a) workable R
res.append(run("debris-ring", S["debris-ring"], 768, 8192, 0.02, 11))
res.append(run("Om180-e03-i15", S["Om180-e03-i15"], 384, 8192, 0.02, 12))
# (b) R scan on broken scenes
for R in (0.005, 0.02, 0.05):
    res.append(run(f"sw180-e03@R{R}", S["sw180-e03"], 384, 8192, R, 13))
res.append(run(f"se01-aligned@R0.02", S["se01-aligned"], 384, 8192, 0.02, 14))
# (c) mechanism focus
res.append(run("mech-se01", S["se01-aligned"], 384, 8192, 0.005, 15))
res.append(run("mech-sw180-e03", S["sw180-e03"], 384, 8192, 0.005, 16))
res.append(run("mech-ctl-e03", S["ctl-ring-e03-aligned"], 384, 8192, 0.005, 17))
# (d) seeds
for seed in (21, 22, 23):
    res.append(run(f"seed{seed}-sw180-e03", S["sw180-e03"], 384, 8192, 0.005, seed))
for seed in (21, 22):
    res.append(run(f"seed{seed}-se005", S["se005-aligned"], 384, 8192, 0.005, seed))
for seed in (21, 22):
    res.append(run(f"seed{seed}-ctl-arc", S["ctl-arc-circ-aligned"], 384, 8192, 0.005, seed))
json.dump(res, open("battery2.json", "w"), indent=1)
print("done")
