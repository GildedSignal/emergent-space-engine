#!/usr/bin/env python3
"""H_live Fermi run 20261008-0743-fermi-fbf8.

Belt model = crates/encounters belt.rs: mu=1, a~U[1,1.5], Rayleigh e (sigma_e),
random angles. Encounters = min distance < rho at conjunctions. Kicks = impulse
approximation + Gauss equations (floats: this is an estimate; orders of magnitude).

Outputs h_live_result.json: anchor (direct belt propagation), walk (t_d vs m), budget.
"""
import json
import numpy as np

RNG = np.random.default_rng(20261008)
TAU = 2.0 * np.pi


def make_belt(n, sigma_e, a_lo, a_hi, seed):
    r = np.random.default_rng(seed)
    a = r.uniform(a_lo, a_hi, n)
    e = np.minimum(sigma_e * np.sqrt(-2.0 * np.log1p(-r.uniform(0, 1, n))), 0.5)
    pom = r.uniform(0, TAU, n)
    lam = r.uniform(0, TAU, n)  # mean longitude at t=0 (M0 = lam - pom)
    return a, e, pom, lam


def kepler_states(a, e, pom, M0, t):
    """Position/velocity arrays at times t (n = a^-3/2, mu = 1)."""
    n = a ** -1.5
    M = (M0 + n * t) % TAU
    E = M.copy()
    for _ in range(6):
        E = E - (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    cosE, sinE = np.cos(E), np.sin(E)
    sq = np.sqrt(1.0 - e * e)
    xo = a * (cosE - e)
    yo = a * sq * sinE
    denom = 1.0 - e * cosE
    vxo = -a * n * sinE / denom
    vyo = a * n * sq * cosE / denom
    cp, sp = np.cos(pom), np.sin(pom)
    return (xo * cp - yo * sp, xo * sp + yo * cp,
            vxo * cp - vyo * sp, vxo * sp + vyo * cp, E)


def true_anomaly(e, E):
    return 2.0 * np.arctan2(np.sqrt(1.0 + e) * np.sin(E / 2.0),
                            np.sqrt(1.0 - e) * np.cos(E / 2.0))


def gauss_deltas(a, e, f, E, dvx, dvy, x, y):
    """da, de from impulse (dvx, dvy) at true anomaly f (mu = 1)."""
    rn = np.hypot(x, y)
    urx, ury = x / rn, y / rn
    utx, uty = -ury, urx
    dvr = dvx * urx + dvy * ury
    dvt = dvx * utx + dvy * uty
    sq = np.sqrt(1.0 - e * e)
    da = 2.0 * a ** 1.5 / sq * (e * np.sin(f) * dvr + (1.0 + e * np.cos(f)) * dvt)
    de = sq * a ** 0.5 * (np.sin(f) * dvr + (np.cos(f) + np.cos(E)) * dvt)
    return da, de


# ---------------------------------------------------------------- anchor belt
def anchor(n=4000, sigma_e=1e-2, a_lo=1.0, a_hi=1.5, rho=1e-3, orbits=60,
           seed=20261001):
    a, e, pom, lam = make_belt(n, sigma_e, a_lo, a_hi, seed)
    nmot = a ** -1.5
    M0 = (lam - pom) % TAU
    t_end = orbits * TAU
    lo = a * (1.0 - e)
    hi = a * (1.0 + e)
    order = np.argsort(lo)
    lo_s, hi_s = lo[order], hi[order]
    # candidate radial-overlap pairs, chunked sweep (memory-safe)
    pi_list, pj_list = [], []
    for s in range(0, n, 512):
        idx = np.arange(s, min(s + 512, n))
        i_lo = lo[idx]
        i_hi = hi[idx] + rho
        end = np.searchsorted(lo_s, i_hi, side="right")
        start = np.searchsorted(lo_s, i_lo - rho, side="left")
        for k in range(len(idx)):
            if end[k] <= start[k]:
                continue
            seg = slice(start[k], end[k])
            cand = order[seg]
            msk = cand != idx[k]
            cand = cand[msk]
            ok = hi_s[seg][msk] >= i_lo[k] - rho
            c = cand[ok]
            pi_list.append(np.full(len(c), idx[k]))
            pj_list.append(c)
    pi = np.concatenate(pi_list)
    pj = np.concatenate(pj_list)
    keep = pi < pj  # each pair once
    pi, pj = pi[keep], pj[keep]
    cand_pairs = len(pi)

    # conjunction times per pair (mean-longitude crossings, exact: linear in t)
    dlam0 = ((M0[pi] + pom[pi]) - (M0[pj] + pom[pj])) % TAU
    dn = np.maximum(np.abs(nmot[pi] - nmot[pj]), 1e-15)
    t_first = dlam0 / dn
    t_syn = TAU / dn
    counts = np.maximum(np.floor((t_end - t_first) / t_syn).astype(np.int64) + 1, 0)
    total_conj = int(counts.sum())
    pair_idx = np.repeat(np.arange(cand_pairs), counts)
    kk = np.arange(total_conj) - np.repeat(np.cumsum(counts) - counts, counts)
    tcon = t_first[pair_idx] + kk * t_syn[pair_idx]

    # min distance over 3 samples around each conjunction
    dmin = None
    for frac in (0.0, 0.1, -0.1):
        t = tcon + frac * t_syn[pair_idx]
        xi, yi, _, _, _ = kepler_states(a[pi[pair_idx]], e[pi[pair_idx]],
                                        pom[pi[pair_idx]], M0[pi[pair_idx]], t)
        xj, yj, _, _, _ = kepler_states(a[pj[pair_idx]], e[pj[pair_idx]],
                                        pom[pj[pair_idx]], M0[pj[pair_idx]], t)
        d = np.hypot(xi - xj, yi - yj)
        dmin = d if dmin is None else np.minimum(dmin, d)
    hit = dmin < rho
    n_enc = int(hit.sum())

    enc_d = enc_de = enc_da = np.array([])
    if n_enc:
        h = np.where(hit)[0]
        ph = pair_idx[h]
        i, j = pi[ph], pj[ph]
        t = tcon[h]
        xi, yi, vxi, vyi, Ei = kepler_states(a[i], e[i], pom[i], M0[i], t)
        xj, yj, vxj, vyj, Ej = kepler_states(a[j], e[j], pom[j], M0[j], t)
        dvx, dvy = vxi - vxj, vyi - vyj
        vrel = np.hypot(dvx, dvy)
        d = dmin[h]
        kick = 2.0 / (vrel * d)          # |dv| per unit encounter mass (G=1)
        side = RNG.choice([-1.0, 1.0], len(h))
        dvxk, dvyk = -dvy / vrel * side * kick, dvx / vrel * side * kick
        fi = true_anomaly(e[i], Ei)
        da_i, de_i = gauss_deltas(a[i], e[i], fi, Ei, dvxk, dvyk, xi, yi)
        enc_d, enc_de, enc_da = d, np.abs(de_i), np.abs(da_i)
    return {
        "n": n, "sigma_e": sigma_e, "rho": rho, "orbits": orbits,
        "cand_pairs": cand_pairs,
        "cand_pairs_per_body": cand_pairs / n,
        "conjunctions_total": total_conj,
        "conjunctions_per_body_per_orbit": total_conj / n / orbits,
        "encounters": n_enc,
        "R_per_body_per_orbit": n_enc / n / orbits,
        "d_median": float(np.median(enc_d)) if n_enc else None,
        "vrel_median": None,
        "de_median_per_m": float(np.median(enc_de)) if n_enc else None,
        "de_rms_per_m": float(np.sqrt(np.mean(enc_de ** 2))) if n_enc else None,
        "da_median_per_m": float(np.median(enc_da)) if n_enc else None,
        "conj_per_encounter": total_conj / max(n_enc, 1),
    }


# ------------------------------------------------------- random walk to t_d
def walk(R, de_rms_unit, q_e=1e-3, n_bodies=200_000, orbits=2000, seed=7):
    out = {}
    for m in (1e-6, 1e-7, 1e-8, 1e-9, 1e-10, 1e-12):
        r = np.random.default_rng(seed)
        sig = de_rms_unit * m
        t_analytic = q_e ** 2 / (R * sig ** 2)
        blocks = 20
        per_block = orbits // blocks
        cum = np.zeros(n_bodies)
        crossed = np.full(n_bodies, np.inf)
        for b in range(blocks):
            draws = r.poisson(R * per_block, n_bodies)
            tot = int(draws.sum())
            if tot == 0:
                continue
            whom = r.integers(0, n_bodies, tot)
            cum += np.bincount(whom, weights=r.normal(0.0, sig, tot),
                               minlength=n_bodies)
            newly = (np.abs(cum) > q_e) & (crossed == np.inf)
            crossed[newly] = (b + 1) * per_block
        fin = crossed[np.isfinite(crossed)]
        out[f"{m:g}"] = {
            "t_d_analytic_orbits": t_analytic,
            "t_d_mc_median_orbits": float(np.median(fin)) if len(fin) else None,
            "frac_crossed": len(fin) / n_bodies,
        }
    return out


def main():
    res = {"anchor": anchor()}
    a_ = res["anchor"]
    R = a_["R_per_body_per_orbit"]
    de_rms = a_["de_rms_per_m"] or 0.0
    res["walk"] = walk(R, de_rms)
    for q in (1e-2, 1e-3, 1e-4):
        res[f"m_star_q{q:g}"] = float(np.sqrt(q ** 2 / (10.0 * R * de_rms ** 2)))
    print(json.dumps(res, indent=1))
    with open("h_live_result.json", "w") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    main()
