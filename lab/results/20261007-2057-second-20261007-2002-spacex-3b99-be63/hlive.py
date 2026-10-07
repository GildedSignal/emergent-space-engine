#!/usr/bin/env python3
"""H_live on the belt: rate of live distinguishing information, and bits per scar.

Impulse Monte Carlo (see predictions.md for the stated model). Per orbit, all of a
body's conjunction kicks are applied as linearized deltas on that orbit's base state
(kicks are quantum-sized; superposition error is second order), accumulated with
bincount. Entropy of quantized integer deltas = scar bits at that quantum.

Thinning: the hot case (lam ~ 2639/body/orbit) is Poisson-thinned 50x — the body-body
encounter rate is divided by `thin` and each kick's mass scaled by sqrt(thin), which
preserves the per-orbit kick variance (sigma) exactly. The thinned conjunction count
x thin is checked against the analytic expectation in `flux_check`.
"""
import json
import numpy as np

G = 4 * np.pi ** 2


def belt(n, sigma_e, w, a0, seed):
    rg = np.random.default_rng(seed)
    a = rg.uniform(a0 - w, a0 + w, n)
    e = rg.rayleigh(sigma_e, n)
    varpi = rg.uniform(-np.pi, np.pi, n)
    return a, e, varpi


def entropy_int(x):
    x = x - x.min()
    p = np.bincount(x) / x.size
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum())


def kick_deltas(idx, base, m_i, sigma_e, lam_i, a0, rg):
    """Per-event (dE, dL, dAx, dAy) against the orbit's base state (linearized)."""
    a, e, E, L, Ax, Ay = base
    n = a.size
    k = rg.poisson(lam_i, n)
    tot = int(k.sum())
    if tot == 0:
        return None, 0
    idx = np.repeat(np.arange(n), k)
    ej = rg.rayleigh(sigma_e, tot)
    bmax = (e[idx] + ej) * a0
    b = np.sqrt(rg.uniform(0, 1, tot)) * bmax
    b = np.maximum(b, 1e-9)
    vK = 2 * np.pi / np.sqrt(a[idx])
    vrel = vK * np.sqrt(e[idx] ** 2 + ej ** 2 + (0.75 * sigma_e) ** 2)
    dv = 2 * G * m_i / (b * vrel)
    ang = rg.uniform(-np.pi, np.pi, tot)
    dvx, dvy = dv * np.cos(ang), dv * np.sin(ang)
    M = rg.uniform(-np.pi, np.pi, tot)
    ei = e[idx]
    Ecc = M.copy()
    for _ in range(4):
        Ecc -= (Ecc - ei * np.sin(Ecc) - M) / (1 - ei * np.cos(Ecc))
    c, s = np.cos(Ecc), np.sin(Ecc)
    r = 1.0 - ei * c
    n_mot = 2 * np.pi / a[idx] ** 1.5
    vmag = n_mot * a[idx] / np.sqrt(1 - ei ** 2)
    rx = a[idx] * (c - ei)
    ry = a[idx] * np.sqrt(1 - ei ** 2) * s
    vpx = -n_mot * a[idx] * s / r
    vpy = n_mot * a[idx] * np.sqrt(1 - ei ** 2) * c / r
    dE = vpx * dvx + vpy * dvy
    dL = rx * dvy - ry * dvx
    Ln = L[idx] + dL
    # A = (v x Lz)/G - rhat; rhat cancels at fixed position:
    # dA = (v x dLz + dv x L'z)/G, both terms same order, both kept.
    dAx = (vpy * dL + dvy * Ln) / G
    dAy = (-vpx * dL - dvx * Ln) / G
    out = (
        np.bincount(idx, dE, minlength=n),
        np.bincount(idx, dL, minlength=n),
        np.bincount(idx, dAx, minlength=n),
        np.bincount(idx, dAy, minlength=n),
    )
    return out, tot


def run_case(name, n, sigma_e, w, a0, m_body, m_pert, orbits, checkpoints, seed, quanta, thin=1):
    a, e, varpi = belt(n, sigma_e, w, a0, seed)
    E = -G / (2 * a)
    L = np.sqrt(G * a * (1 - e ** 2))
    Ax = e * np.cos(varpi)
    Ay = e * np.sin(varpi)
    E0, L0, Ax0, Ay0 = E.copy(), L.copy(), Ax.copy(), Ay.copy()
    E_typ = G / (2 * a0)
    L_typ = np.sqrt(G * a0)
    rg = np.random.default_rng(seed + 777)
    e_bar = sigma_e * np.sqrt(np.pi / 2)
    n_mean = 2 * np.pi / a0 ** 1.5
    n_cross = n * (a0 * 2 * e_bar) / (2 * w)
    lam = n_cross * (1.5 * (a0 * 2 * e_bar * 2 / 3) / a0)
    lam_pert = 1.5 * n_mean * (2 * w) / a0 if m_pert > 0 else 0.0
    # Variance-preserving thinning of the body-body channel: rate/thin, mass*sqrt(thin).
    lam_body, m_body_eff = lam / thin, m_body * np.sqrt(thin)
    out = {"case": name, "lam_conj_per_body_orbit": lam,
           "lam_pert_per_body_orbit": lam_pert,
           "n": n, "sigma_e": sigma_e, "m_body": m_body, "m_pert": m_pert,
           "thin": thin,
           "checkpoints": {}, "sim_conjunctions": 0,
           "expected_conjunctions": int((lam + lam_pert) * n * orbits)}
    for t in range(1, orbits + 1):
        for lam_i, m_i in ((lam_body, m_body_eff), (lam_pert, m_pert)):
            if m_i <= 0:
                continue
            base = (a, e, E, L, Ax, Ay)
            d, tot = kick_deltas(None, base, m_i, sigma_e, lam_i, a0, rg)
            out["sim_conjunctions"] += tot
            if d is None:
                continue
            E = E + d[0]
            L = L + d[1]
            Ax = Ax + d[2]
            Ay = Ay + d[3]
        if t in checkpoints:
            dE, dL = E - E0, L - L0
            dvp = np.angle(Ax + 1j * Ay) - np.angle(Ax0 + 1j * Ay0)
            dvp = (dvp + np.pi) % (2 * np.pi) - np.pi
            rec = {"orbits": t, "years": t * a0 ** 1.5}
            for q in quanta:
                iE = np.round(dE / (q * E_typ)).astype(np.int64)
                iL = np.round(dL / (q * L_typ)).astype(np.int64)
                iW = np.round(dvp / (2 * np.pi * q)).astype(np.int64)
                scarred = (iE != 0) | (iL != 0) | (iW != 0)
                frac = float(scarred.mean())
                hE = entropy_int(iE) if frac > 0 else 0.0
                hL = entropy_int(iL) if frac > 0 else 0.0
                hW = entropy_int(iW) if frac > 0 else 0.0
                px = min(max(frac, 1e-12), 1 - 1e-12)
                memb = float(-(px * np.log2(px) + (1 - px) * np.log2(1 - px)))
                rec[f"q{q}"] = {"frac_scarred": frac, "bits_E": hE, "bits_L": hL,
                                "bits_W": hW,
                                "bits_per_body": memb + frac * (hE + hL + hW)}
            q = quanta[-1]
            rec["coherent_dE_quanta"] = float(abs(dE.mean()) / (q * E_typ))
            rec["spread_dE_quanta"] = float(dE.std() / (q * E_typ))
            out["checkpoints"][str(t)] = rec
    out["flux_check"] = out["sim_conjunctions"] * thin / out["expected_conjunctions"]
    return out


def main():
    quanta = [2 ** -16, 2 ** -20, 2 ** -24]
    cps = [1, 3, 10, 30, 100, 300]
    cases = [
        ("cold_m1e-10", 2000, 0.01, 0.05, 2.1, 1e-10, 0.0, 1),
        ("cold_m1e-12", 2000, 0.01, 0.05, 2.1, 1e-12, 0.0, 1),
        ("cold_m1e-8", 2000, 0.01, 0.05, 2.1, 1e-8, 0.0, 1),
        ("hot_m1e-10", 2000, 0.10, 0.05, 2.1, 1e-10, 0.0, 50),
        ("pert_m1e-7", 2000, 0.01, 0.05, 2.1, 1e-10, 1e-7, 1),
    ]
    all_out = []
    for name, n, se, w, a0, mb, mp, thin in cases:
        seeds = [run_case(name, n, se, w, a0, mb, mp, 300, cps, sd, quanta, thin)
                 for sd in (1, 2)]
        all_out.append(seeds)
        print(f"done {name}", flush=True)
    with open("hlive_results.json", "w") as f:
        json.dump(all_out, f, indent=1)
    for seeds in all_out:
        r0 = seeds[0]
        thin = r0["thin"]
        print(f"\n== {r0['case']} lam={r0['lam_conj_per_body_orbit']:.2f}+"
              f"{r0['lam_pert_per_body_orbit']:.3f}/orbit thin={thin} "
              f"(sim x thin {int(r0['sim_conjunctions'] * thin)} "
              f"exp {r0['expected_conjunctions']} flux_check {r0['flux_check']:.5f})")
        for t in cps:
            m = [s["checkpoints"][str(t)] for s in seeds]
            line = f"  t={t:4d}"
            for q in quanta:
                fr = np.median([x[f"q{q}"]["frac_scarred"] for x in m])
                bb = np.median([x[f"q{q}"]["bits_per_body"] for x in m])
                line += (f" | q2^{int(np.log2(q)):+d}: f={fr:7.4f} b={bb:7.2f}")
            print(line)


if __name__ == "__main__":
    main()
