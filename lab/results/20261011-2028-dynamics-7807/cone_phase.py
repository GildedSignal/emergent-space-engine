#!/usr/bin/env python3
"""Phase diagram of the Binet-cone candidate tier on the belt's temperature axis.

Mirrors crates/encounters' candidate rule exactly (pairs.rs, r8 v3-verified):
    is_candidate(i, j):  |dU| - ||d(V,W)|| < eps_u(rho)
    eps_u = 1.5 * rho * (1 + k0) / rmin^2,  k0 = rmax^2 * emax / (pmin * rmin)
Belt ensembles follow belt.rs Spec: a ~ U[a_lo, a_hi], e ~ Rayleigh(sigma_e)
truncated at 0.5, uniform pom, uniform lam.  Newtonian, mu = 1, 2-D prograde.

Encounter rate per candidate pair (mean field over the section's circle
rotation, which equidistributes: the exact check times events, the rate is the
time average): at each of the pair's transversal crossings,
    rate = 2*rho / (v_rel * T_i * T_j),   T = 2*pi*a^1.5,
with v_rel from exact Kepler velocities at the crossing radius.  Gravitational
focusing is neglected (small bodies / ships).  Near-identical orbits (co-orbital
'Full' sections, R < eps_u) get the co-orbital rate
    rate_full = 2 * 2*rho / (v_orb*(e_i+e_j+0.02) * T_i * T_j)  (flagged approx).
"""
import json
import sys
import time
import numpy as np

TAU = 2.0 * np.pi
RUN = "/home/glmlab/actions-runner/_work/emergent-space-engine/lab-1/lab/results/20261011-2028-dynamics-7807"


def gen_belt(n, sigma_e, a_lo, a_hi, seed):
    rng = np.random.default_rng(seed)
    a = rng.uniform(a_lo, a_hi, n)
    e = np.minimum(sigma_e * np.sqrt(-2.0 * np.log1p(-rng.random(n))), 0.5)
    pom = TAU * rng.random(n)
    return a, e, pom


def binet(a, e, pom):
    p = a * (1.0 - e * e)
    u = 1.0 / p
    return u, e * np.cos(pom) * u, e * np.sin(pom) * u, p


def candidate_scan(a, e, pom, rho, chunk=384, cap=120_000, seed=7):
    """Exact cone test over j-chunks.  Returns (degree, total_pairs, n_full,
    (sampled_i, sampled_j))."""
    n = a.size
    U, V, W, p = binet(a, e, pom)
    rmin = a * (1.0 - e)
    rmax = a * (1.0 + e)
    deg = np.zeros(n, dtype=np.int64)
    total, n_full = 0, 0
    si, sj = [], []
    nch = (n + chunk - 1) // chunk
    per_chunk_cap = max(1500, cap // nch)
    rng = np.random.default_rng(seed)
    for lo in range(0, n, chunk):
        hi = min(lo + chunk, n)
        dU = np.abs(U[None, lo:hi] - U[:, None])
        dV = V[None, lo:hi] - V[:, None]
        dW = W[None, lo:hi] - W[:, None]
        R = np.hypot(dV, dW)
        rmin2 = np.minimum(rmin[None, lo:hi], rmin[:, None])
        rmax2 = np.maximum(rmax[None, lo:hi], rmax[:, None])
        emax2 = np.maximum(e[None, lo:hi], e[:, None])
        pmin2 = np.minimum(p[None, lo:hi], p[:, None])
        k0 = rmax2 * rmax2 * emax2 / (pmin2 * rmin2)
        eps = 1.5 * rho * (1.0 + k0) / (rmin2 * rmin2)
        cand = (dU - R) < eps
        cand &= np.arange(n)[:, None] < (lo + np.arange(hi - lo))[None, :]  # i < j once
        deg += cand.sum(1)
        deg[lo:hi] += cand.sum(0)
        cnt = int(cand.sum())
        total += cnt
        n_full += int(((R < eps) & cand).sum())
        if cnt:
            i_idx, c_idx = np.nonzero(cand)
            if i_idx.size > per_chunk_cap:
                keep = rng.choice(i_idx.size, per_chunk_cap, replace=False)
                i_idx, c_idx = i_idx[keep], c_idx[keep]
            si.append(i_idx)
            sj.append(c_idx + lo)
    if si:
        return deg, total, n_full, (np.concatenate(si), np.concatenate(sj))
    return deg, total, n_full, (np.zeros(0, np.int64), np.zeros(0, np.int64))


def pair_rates(a, e, pom, i_idx, j_idx, rho):
    """Mean-field close-approach rate per sampled pair (per time unit, mu=1).
    Transversal crossings: conjunctions once per synodic period, i's phase
    equidistributed over T_i, miss distance = offset * v_rel, so
        rate = 2*rho*|1/T_i - 1/T_j| / (v_rel * T_i)
    (the |n_i - n_j| factor kills the near-twin divergence: v_rel >= v*|da|/2a).
    Co-orbital 'Full' sections (equal periods, R < eps_u): epicyclic alignment,
        rate_full = (e_i+e_j+0.02) * min(1, 4*rho/(r*(e_i+e_j+0.02))) / T   (approx)
    Returns (rates, ncross, n_full, sum_transversal, sum_full)."""
    U, V, W, p = binet(a, e, pom)
    h = np.sqrt(p)
    T = TAU * a ** 1.5
    m = i_idx.size
    rates = np.zeros(m)
    ncross = np.zeros(m, dtype=int)
    if m == 0:
        return rates, ncross, 0, 0.0, 0.0
    dU0 = np.abs(U[i_idx] - U[j_idx])
    R0 = np.hypot(V[i_idx] - V[j_idx], W[i_idx] - W[j_idx])
    vmin2 = np.minimum(a[i_idx] * (1 - e[i_idx]), a[j_idx] * (1 - e[j_idx]))
    eps0 = 1.5 * rho * 1.4 / vmin2**2
    full = R0 < np.minimum(eps0, dU0 + 1e-18)
    nfull = int(full.sum())
    if nfull:
        ai, aj = a[i_idx[full]], a[j_idx[full]]
        ei, ej = e[i_idx[full]], e[j_idx[full]]
        r = 0.5 * (ai + aj)
        exc = ei + ej + 0.02
        rates[full] = exc * np.minimum(1.0, 4.0 * rho / (r * exc)) / (0.5 * (T[i_idx[full]] + T[j_idx[full]]))
        ncross[full] = 2
    sum_full = float(rates[full].sum())
    dn = np.abs(1.0 / T[i_idx] - 1.0 / T[j_idx])
    for s in (1, -1):
        dU = U[i_idx] - U[j_idx]
        dV = V[i_idx] - V[j_idx]
        dW = W[i_idx] - W[j_idx]
        R = np.hypot(dV, dW)
        ok = R > 1e-14
        x = np.clip(-dU[ok] / R[ok], -1.0, 1.0)
        th = np.arctan2(dW[ok], dV[ok]) + s * np.arccos(x)
        u_c = U[i_idx[ok]] + V[i_idx[ok]] * np.cos(th) + W[i_idx[ok]] * np.sin(th)
        with np.errstate(divide="ignore", invalid="ignore"):
            r = np.where(u_c > 0, 1.0 / np.maximum(u_c, 1e-300), np.inf)
        valid = (
            (u_c > 0)
            & (r >= a[i_idx[ok]] * (1 - e[i_idx[ok]]) * (1 - 1e-9))
            & (r <= a[i_idx[ok]] * (1 + e[i_idx[ok]]) * (1 + 1e-9))
            & (r >= a[j_idx[ok]] * (1 - e[j_idx[ok]]) * (1 - 1e-9))
            & (r <= a[j_idx[ok]] * (1 + e[j_idx[ok]]) * (1 + 1e-9))
        )
        if not valid.any():
            continue
        rows = np.where(ok)[0][valid]
        rv, thv = r[valid], th[valid]
        vt_i, vt_j = h[i_idx[rows]] / rv, h[j_idx[rows]] / rv
        v2 = 2.0 - 1.0 / rv
        vr_i = np.sqrt(np.maximum(0.0, v2 - vt_i * vt_i))
        vr_j = np.sqrt(np.maximum(0.0, v2 - vt_j * vt_j))
        si_ = -np.sign(-V[i_idx[rows]] * np.sin(thv) + W[i_idx[rows]] * np.cos(thv))
        sj_ = -np.sign(-V[j_idx[rows]] * np.sin(thv) + W[j_idx[rows]] * np.cos(thv))
        dot = si_ * sj_ * vr_i * vr_j + vt_i * vt_j
        vrel = np.sqrt(np.maximum(1e-12, 2.0 * v2 - 2.0 * dot))
        rates[rows] += 2.0 * rho * dn[rows] / (vrel * T[i_idx[rows]])
        ncross[rows] += 1
    sum_t = float(rates[~full].sum())
    return rates, ncross, nfull, sum_t, sum_full


def one_config(n, sigma_e, a_lo, a_hi, rho, seed, cap=120_000):
    t0 = time.time()
    a, e, pom = gen_belt(n, sigma_e, a_lo, a_hi, seed)
    deg, total, n_full, (ii, jj) = candidate_scan(a, e, pom, rho, cap=cap, seed=seed)
    kbar = 2.0 * total / n
    amed = 0.5 * (a_lo + a_hi)
    T_med = TAU * amed**1.5
    lam_o = 0.0
    lam_full = 0.0
    if ii.size:
        rates, ncross, nfull_s, st, sf = pair_rates(a, e, pom, ii, jj, rho)
        # per body: population mean pair-rate (unbiased sample) * pairs per body
        lam_o = rates.mean() * (total / n) * T_med
        lam_full = (sf / ii.size) * (total / n) * T_med
    kap = sigma_e * amed / (a_hi - a_lo)
    W = kbar / lam_o if lam_o > 0 else None
    return {
        "n": n, "sigma_e": round(sigma_e, 5), "rho": rho, "kappa": round(kap, 4),
        "pairs": total, "pairs_per_body": round(kbar, 1), "frac_pairs": round(kbar / n, 4),
        "deg_p50": float(np.median(deg)), "deg_p99": float(np.percentile(deg, 99)),
        "n_full_pairs": n_full,
        "enc_per_body_per_orbit": float(lam_o),
        "enc_full_share": round(lam_full / lam_o, 3) if lam_o > 0 else None,
        "W_setups_per_encounter": None if W is None else float(W),
        "sec": round(time.time() - t0, 1), "seed": seed,
    }


def phase(name, rows):
    with open(f"{RUN}/{name}.json", "w") as f:
        json.dump(rows, f, indent=1)
    print(f"[{name}] {len(rows)} configs")
    for r in rows:
        print(f"   kap={r['kappa']:<7} sig={r['sigma_e']:<7} N={r['n']:<6} rho={r['rho']:<6}"
              f" frac={r['frac_pairs']:<8.4f} enc/orb={r['enc_per_body_per_orbit']:<10.3e}"
              f" W={r['W_setups_per_encounter']}")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "sweep"
    if mode == "sweep":
        rows = []
        for rho in (0.01, 0.003):
            for sigma_e in np.geomspace(0.005, 0.5, 12):
                for seed in (11, 12, 13):
                    rows.append(one_config(4096, float(sigma_e), 2.0, 3.3, rho, seed))
        phase("sweep", rows)
    elif mode == "formation":
        rows = []
        for width in (0.39, 0.039, 0.0039):
            for sigma_e in (0.01, 0.07, 0.2):
                rows.append(one_config(2048, sigma_e, 2.65 - width / 2, 2.65 + width / 2, 0.01, 21))
        phase("formation", rows)
    elif mode == "nscal":
        rows = []
        for kap, n in ((0.10, 1024), (0.10, 4096), (0.10, 16384), (2.0, 1024), (2.0, 4096), (2.0, 16384)):
            sig = kap * 1.3 / 2.65
            rows.append(one_config(n, float(sig), 2.0, 3.3, 0.01, 31))
        phase("nscal", rows)
    elif mode == "analyze":
        agg = {}
        for name in ("sweep", "formation", "nscal"):
            try:
                with open(f"{RUN}/{name}.json") as f:
                    agg[name] = json.load(f)
            except FileNotFoundError:
                pass
        by = {}
        for r in agg.get("sweep", []):
            by.setdefault((r["rho"], round(r["sigma_e"], 5)), []).append(r)
        coll = []
        for (rho, sig), rs in sorted(by.items()):
            ws = [x["W_setups_per_encounter"] for x in rs if x["W_setups_per_encounter"]]
            coll.append({
                "rho": rho, "sigma_e": sig, "kappa": rs[0]["kappa"],
                "frac_pairs": float(np.mean([x["frac_pairs"] for x in rs])),
                "frac_sd": float(np.std([x["frac_pairs"] for x in rs])),
                "enc": float(np.mean([x["enc_per_body_per_orbit"] for x in rs])),
                "W": float(np.mean(ws)) if ws else None,
            })
        kap = np.array([c["kappa"] for c in coll if c["rho"] == 0.01])
        fr = np.array([c["frac_pairs"] for c in coll if c["rho"] == 0.01])
        below = fr < 0.5
        c_fit = float(np.mean(fr[below] / kap[below])) if below.sum() > 2 else None
        encs = [c for c in coll if c["rho"] == 0.01 and c["enc"] > 0]
        alpha = None
        if len(encs) > 3:
            lk = np.log([c["kappa"] for c in encs])
            le = np.log([c["enc"] for c in encs])
            alpha = float(np.polyfit(lk, le, 1)[0])
        import math
        kstar = {}
        for rho in (0.01, 0.003):
            cs = [c for c in coll if c["rho"] == rho and 0.05 < c["frac_pairs"] < 0.95]
            if len(cs) >= 2:
                lk = np.log([c["kappa"] for c in cs]); lf = np.log([c["frac_pairs"] for c in cs])
                sl, ic = np.polyfit(lk, lf, 1)
                kstar[str(rho)] = float(math.exp((math.log(0.5) - ic) / sl)) if abs(sl) > 0.2 else None
        out = {"collapsed_sweep": coll, "c_fit_frac_over_kappa": c_fit,
               "enc_alpha": alpha, "kappa_star_frac_half": kstar,
               "formation": agg.get("formation"), "nscal": agg.get("nscal")}
        with open(f"{RUN}/metrics.json", "w") as f:
            json.dump(out, f, indent=1)
        print(json.dumps({k: v for k, v in out.items()
                          if k not in ("collapsed_sweep", "formation", "nscal")}, indent=1))
        for c in coll:
            print(f"  rho={c['rho']:<6} sig={c['sigma_e']:.4f} kap={c['kappa']:.3f} "
                  f"frac={c['frac_pairs']:.4f}±{c['frac_sd']:.4f} enc/orb={c['enc']:.3e} W={c['W']}")


if __name__ == "__main__":
    main()
