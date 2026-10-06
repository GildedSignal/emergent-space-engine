#!/usr/bin/env python3
"""Belt chaos fraction vs planet mass ratio (circular restricted 3-body, 2D, float64).

Star (mass 1) + planet (mass mu) on a mutual circular orbit at a=1, plus N massless
test particles uniform in a in [a_min, a_max], e0 Rayleigh(sigma_e), random angles.
Leapfrog DKD, dt = 2*pi/n_dt. Chaos classifier: renormalized shadow particle
(d0 = 1e-9, renormalized every renorm_orbits planet periods). Resonance classifier:
circular variance of the resonant angle of the nearest k:j resonance.
Outputs JSON to stdout. Each run stays under ~40 s.
"""
import json
import sys
import numpy as np

def run(mu, sigma_e=0.1, N=800, T_orbits=1200, n_dt=150, a_min=0.38, a_max=0.75,
        d0=1e-9, renorm_orbits=50, tau_a=0.003, seed=7, tag=""):
    rng = np.random.default_rng(seed)
    G = 1.0
    Ms = 1.0
    Mp = mu
    mu_tot = G * (Ms + Mp)
    # planet & star: circular mutual orbit about the barycentre
    r_sep = 1.0
    v_c = np.sqrt(mu_tot / r_sep)
    star_x = np.array([-Mp / (Ms + Mp) * r_sep, 0.0])
    star_v = np.array([0.0, -Mp / (Ms + Mp) * v_c])
    pl_x = np.array([Ms / (Ms + Mp) * r_sep, 0.0])
    pl_v = np.array([0.0, Ms / (Ms + Mp) * v_c])
    # particles: uniform in a, Rayleigh e, random lambda, random omega (periapsis)
    a = rng.uniform(a_min, a_max, N)
    e = rng.rayleigh(sigma_e, N)
    e = np.clip(e, 0.0, 0.6)
    lam = rng.uniform(0, 2 * np.pi, N)
    om = rng.uniform(0, 2 * np.pi, N)
    # place at random true anomaly along the ellipse (Kepler via eccentric anomaly)
    M_an = rng.uniform(0, 2 * np.pi, N)
    E_an = M_an + e * np.sin(M_an)
    for _ in range(6):  # Newton for E
        E_an = E_an - (E_an - e * np.sin(E_an) - M_an) / (1 - e * np.cos(E_an))
    nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E_an / 2), np.sqrt(1 - e) * np.cos(E_an / 2))
    r = a * (1 - e * np.cos(E_an))
    th = om + nu
    x = np.stack([r * np.cos(th), r * np.sin(th)], axis=1) + star_x  # heliocentric-ish start (star nearly origin)
    h = np.sqrt(np.maximum(mu_tot * a * (1 - e**2), 1e-12))
    vr = mu_tot / h * e * np.sin(nu)
    vt = mu_tot / h * (1 + e * np.cos(nu))
    v = np.stack([vr * np.cos(th) - vt * np.sin(th), vr * np.sin(th) + vt * np.cos(th)], axis=1) + star_v
    # shadow particles
    xs = x.copy(); xs[:, 0] += d0
    vs = v.copy()

    dt = 2 * np.pi / n_dt
    n_steps = int(T_orbits * n_dt)
    renorm_every = renorm_orbits * n_dt
    log_sum = 0.0
    n_renorm = 0

    # resonance table k:j (particle:planet), coprime, k>=2
    res_list = []
    for k in range(2, 13):
        for j in range(1, k):
            if np.gcd(k, j) == 1:
                a_res = (j / k) ** (2.0 / 3.0)
                if a_min - 0.06 < a_res < a_max + 0.06:
                    res_list.append((k, j, a_res))
    a_res_arr = np.array([r[2] for r in res_list])
    k_arr = np.array([r[0] for r in res_list])
    j_arr = np.array([r[1] for r in res_list])

    # sample accumulators
    n_samples = T_orbits  # once per planet orbit
    ph_acc = []   # complex mean of e^{i phi} for nearest resonance
    ph2_acc = []  # for second-nearest
    conj_acc = np.zeros(N)
    lam_prev = None
    lamJ_prev = None
    a_samp = []

    def accel(pos):
        d_s = star_x - pos
        a_s = G * Ms * d_s / np.linalg.norm(d_s, axis=1, keepdims=True) ** 3
        d_p = pl_x - pos
        a_p = G * Mp * d_p / np.linalg.norm(d_p, axis=1, keepdims=True) ** 3
        return a_s + a_p

    # initial half kick (leapfrog: K-half, then per step D then full K)
    axp = accel(x); axs = accel(xs)
    v += 0.5 * dt * axp; vs += 0.5 * dt * axs
    d = pl_x - star_x
    r3 = np.linalg.norm(d) ** 3
    star_v += 0.5 * dt * (G * Mp * d / r3)
    pl_v += 0.5 * dt * (-G * Ms * d / r3)
    for step in range(n_steps):
        star_x += dt * star_v; pl_x += dt * pl_v
        x += dt * v; xs += dt * vs
        d = pl_x - star_x
        r3 = np.linalg.norm(d) ** 3
        star_v += dt * (G * Mp * d / r3)
        pl_v += dt * (-G * Ms * d / r3)
        axp = accel(x); axs = accel(xs)
        v += dt * axp; vs += dt * axs
        if (step + 1) % renorm_every == 0:
            dist = np.linalg.norm(xs - x, axis=1)
            log_sum += np.log(np.maximum(dist, 1e-300) / d0)
            n_renorm += 1
            xs = x + (xs - x) * (d0 / dist)[:, None]
            vs = v + (vs - v) * (d0 / dist)[:, None]

        if (step + 1) % n_dt == 0:
            rel = x - star_x
            vrel = v - star_v
            rn = np.linalg.norm(rel, axis=1)
            v2 = np.sum(vrel * vrel, axis=1)
            a_cur = 1.0 / (2.0 / rn - v2 / mu_tot)
            rv = np.sum(rel * vrel, axis=1)
            ev = ((v2 - mu_tot / rn)[:, None] * rel - rv[:, None] * vrel) / mu_tot
            ecc = np.linalg.norm(ev, axis=1)
            varpi = np.arctan2(ev[:, 1], ev[:, 0])
            lam_p = np.arctan2(rel[:, 1], rel[:, 0])
            lam_J = np.arctan2(pl_x[1] - star_x[1], pl_x[0] - star_x[0])
            # nearest resonance in mean a over samples so far
            a_samp.append(a_cur.copy())
            a_run = np.mean(a_samp, axis=0)
            idx = np.argmin(np.abs(a_run[:, None] - a_res_arr[None, :]), axis=1)
            kk = k_arr[idx]; jj = j_arr[idx]
            phi = kk * lam_p - jj * lam_J - (kk - jj) * varpi
            ph_acc.append(np.exp(1j * phi))
            order = np.argsort(np.abs(a_run[:, None] - a_res_arr[None, :]), axis=1)
            idx2 = order[:, 1]
            kk2 = k_arr[idx2]; jj2 = j_arr[idx2]
            phi2 = kk2 * lam_p - jj2 * lam_J - (kk2 - jj2) * varpi
            ph2_acc.append(np.exp(1j * phi2))

    T_time = T_orbits  # in planet periods
    lyap_per_orbit = log_sum / T_time
    A = np.array(a_samp)  # (T_orbits, N)
    W = T_orbits // 6
    win_means = np.array([A[i*W:(i+1)*W].mean(axis=0) for i in range(6)])
    drift = win_means.max(axis=0) - win_means.min(axis=0)
    chaotic = drift > tau_a
    ph_mean = np.mean(ph_acc, axis=0)
    ph2_mean = np.mean(ph2_acc, axis=0)
    circvar = 1.0 - np.abs(ph_mean)
    circvar2 = 1.0 - np.abs(ph2_mean)
    resonant = (~chaotic) & ((circvar < 0.5) | (circvar2 < 0.5))
    clean = ~(chaotic | resonant)
    a_run = np.mean(a_samp, axis=0)
    conj_rate = np.where(a_run > 0.05, np.maximum(a_run ** -1.5 - 1.0, 0.0), np.nan)

    out = {
        "tag": tag, "mu": mu, "sigma_e": sigma_e, "N": N, "T_orbits": T_orbits,
        "f_chaotic": float(chaotic.mean()), "f_resonant": float(resonant.mean()),
        "f_clean": float(clean.mean()),
        "n_chaotic": int(chaotic.sum()), "n_resonant": int(resonant.sum()),
        "median_drift_chaotic": float(np.median(drift[chaotic])) if chaotic.any() else None, "max_drift_all": float(drift.max()),
        "conj_rate_chaotic_per_Pj": float(np.median(conj_rate[chaotic])) if chaotic.any() else None,
        "conj_rate_clean_per_Pj": float(np.median(conj_rate[clean])) if clean.any() else None,
        "a_bins_chaotic": [float(x) for x in np.histogram(a_run[chaotic], bins=14, range=(a_min, a_max))[0]] if chaotic.any() else [],
        "a_bins_all": [float(x) for x in np.histogram(a_run, bins=14, range=(a_min, a_max))[0]],
    }
    print(json.dumps(out))

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--mu", type=float, required=True)
    p.add_argument("--sigma-e", type=float, default=0.1)
    p.add_argument("--T", type=int, default=1200)
    p.add_argument("--tag", default="")
    p.add_argument("--seed", type=int, default=7)
    args = p.parse_args()
    run(args.mu, sigma_e=args.sigma_e, T_orbits=args.T, tag=args.tag, seed=args.seed)
