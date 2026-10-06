#!/usr/bin/env python3
"""Scar-store equilibrium of a belt under encounters (integer lattice, seed-driven).

Component under test: crates/shipmem Form P (program + sparse scars), whose reabsorption
rule is 'state returns exactly to its program'. Measures, per orbit:
  - one-tier exact scar bits (Elias-Fano ordinals + zigzag Elias-gamma delta values)
  - return-to-program reabsorptions
  - two-tier light-cone store: near bodies naive-exact, far bodies' delta requantized at q_far
  - coarse (a,e) occupancy entropy (the view/multipole-level information, identity-free)
plus the firewall margin for far reabsorption and the 10^9 extrapolation.

All arithmetic on int64 lattice indices; kicks are quantized to the law's grid (r2).
"""
import numpy as np

LA, LE, LW = 20, 16, 16                 # exact lattice widths (bits): a, e, varpi
NA, NE, NW = 1 << LA, 1 << LE, 1 << LW
NAIVE_BITS = LA + LE + LW               # 52
QFAR = 1 << 8                           # far reabsorption quantum (lattice units)
T_ORBITS = 100
LAMBDAS = [0.01, 0.1, 1.1]


def elias_gamma_bits(z):
    """Zigzag Elias-gamma code length for int64 deltas |z| < 2^52.
    Codes v = |z|+1 (gamma: 2*bl(v)-1 bits) plus one sign bit."""
    u = np.abs(z).astype(np.uint64) + np.uint64(1)
    n = u.astype(np.int64)
    bl = np.zeros(u.shape, dtype=np.int64)
    bl += (n >> 32 != 0) * 32; n = np.where(n >> 32 != 0, n >> 32, n)
    bl += (n >> 16 != 0) * 16; n = np.where(n >> 16 != 0, n >> 16, n)
    bl += (n >> 8 != 0) * 8;  n = np.where(n >> 8 != 0, n >> 8, n)
    bl += (n >> 4 != 0) * 4;  n = np.where(n >> 4 != 0, n >> 4, n)
    bl += (n >> 2 != 0) * 2;  n = np.where(n >> 2 != 0, n >> 2, n)
    bl += (n >> 1 != 0) * 1
    return 2 * bl


def splitmix(i, seed):
    x = (i.astype(np.uint64) + np.uint64(seed)) * np.uint64(0x9E3779B97F4A7C15)
    x = (x ^ (x >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
    x = (x ^ (x >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
    return ((x ^ (x >> np.uint64(31))) >> np.uint64(11)).astype(np.float64) / (1 << 53)


def birth(N, seed):
    """Bijective smooth program: Irwin-Hall (3 uniforms) in a, Rayleigh-ish e, uniform varpi."""
    idx = np.arange(N, dtype=np.uint64)
    u1, u2, u3 = splitmix(idx, seed + 1), splitmix(idx, seed + 2), splitmix(idx, seed + 3)
    a = ((u1 + u2 + u3) / 3 * NA).astype(np.int64).clip(0, NA - 1)   # smooth in a
    e = (np.sqrt(-np.log(1 - 0.999 * u1)) * 0.22 * NE).astype(np.int64).clip(0, NE - 1)
    w = (u2 * NW).astype(np.int64).clip(0, NW - 1)
    return a, e, w


def kick(rng, n):
    """Heavy-tailed quantized kick: bit-length geometric(p=1/2) truncated, one main column."""
    L = rng.geometric(0.5, n).clip(1, 20)                      # bit length 1..20
    mag = (np.int64(1) << (L - 1))
    sign = np.where(rng.random(n) < 0.5, -1, 1)
    col = rng.integers(0, 3, n)
    da = np.where(col == 0, sign * mag, rng.integers(-1, 2, n))
    de = np.where(col == 1, sign * mag, rng.integers(-1, 2, n))
    dw = np.where(col == 2, sign * mag, rng.integers(-1, 2, n))
    return da, de, dw


def clip_reflect(x, hi):
    return np.where(x < 0, -x, np.where(x >= hi, 2 * hi - x - 2, x))


def occupancy_bits(a, e, bins_a, bins_e):
    h, _, _ = np.histogram2d(a, e, bins=[bins_a, bins_e], range=[[0, NA], [0, NE]])
    p = h.flatten() / h.sum()
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum() * len(a))


def run(lam, N, seed, t_orbits=T_ORBITS, report_every=10):
    rng = np.random.default_rng(seed)
    a0, e0, w0 = birth(N, seed)
    a, e, w = a0.copy(), e0.copy(), w0.copy()
    a_player = NA // 2
    half_near = NA // 64
    ever_scarred = np.zeros(N, dtype=bool)
    rows = []
    reabs_total = 0
    enc_per_body = 0.0
    for t in range(1, t_orbits + 1):
        for _ in range(int(lam) + 1):                          # Poisson lam ~ passes x p
            p = lam if lam < 1 else lam / (int(lam) + 1)
            m = rng.random(N) < p
            n = int(m.sum())
            if n == 0:
                continue
            enc_per_body += n / N
            da, de, dw = kick(rng, n)
            a[m] = clip_reflect(a[m] + da, NA)
            e[m] = clip_reflect(e[m] + de, NE)
            w[m] = clip_reflect(w[m] + dw, NW)
        da_, de_, dw_ = a - a0, e - e0, w - w0
        scarred = (da_ != 0) | (de_ != 0) | (dw_ != 0)
        # return-to-program: ever-scarred body whose deltas hit exactly zero in all columns
        returned = int((ever_scarred & ~scarred).sum()) if t > 1 else 0
        ever_scarred |= scarred
        reabs_total += returned
        k = int(scarred.sum())
        # one-tier Form-P bits
        ef = k * (2 + np.log2(N / max(k, 1))) if k else 0.0
        val = (elias_gamma_bits(da_[scarred]).sum() + elias_gamma_bits(de_[scarred]).sum()
               + elias_gamma_bits(dw_[scarred]).sum())
        onetier = (ef + val) / N
        # two-tier: near naive-exact, far at q_far
        near = np.abs(a - a_player) <= half_near
        n_near = int(near.sum())
        far = ~near
        far_da = np.rint(da_[far] / QFAR).astype(np.int64)
        far_de = np.rint(de_[far] / QFAR).astype(np.int64)
        far_dw = np.rint(dw_[far] / QFAR).astype(np.int64)
        farbits = (elias_gamma_bits(far_da).sum() + elias_gamma_bits(far_de).sum()
                   + elias_gamma_bits(far_dw).sum() + 2.0 * far.sum()) / N  # +2 flag overhead
        twotier = n_near / N * NAIVE_BITS + farbits
        occ = occupancy_bits(a, e, 256, 128)
        if t % report_every == 0 or t == 1:
            rows.append((t, k / N, returned, reabs_total, onetier,
                         twotier, n_near, occ / N, enc_per_body))
    return rows


def firewall(mu=3.6e-9, n_far=int(1e9), eps_m=1e5, a_over_R=0.7,
             q_varpi=2 * np.pi / (1 << 16)):
    """Ring-quadrupole precession error induced on a near body by reabsorbing every far body
    at eps (metres of radial error). Belt at 3e11 m (2 AU); errors independent -> quadrature."""
    per_body = 0.75 * np.pi * (mu / n_far) * a_over_R ** 3 * 3 * (eps_m / 3e11)
    sigma = np.sqrt(n_far) * per_body
    return sigma, q_varpi, q_varpi / sigma


if __name__ == "__main__":
    import json, time, os
    t0 = time.time()
    out = {"machine": {"load": os.getloadavg(), "cores": os.cpu_count()}, "lambdas": {}}
    N = 1 << 18
    for lam in LAMBDAS:
        rows = run(lam, N, seed=20261006)
        out["lambdas"][str(lam)] = [
            {"t": r[0], "scarred_frac": round(r[1], 4), "returned_this_orbit": r[2],
             "returned_total": r[3], "onetier_bits_per_body": round(r[4], 2),
             "twotier_bits_per_body": round(r[5], 2), "n_near": r[6],
             "occupancy_bits_per_body": round(r[7], 3),
             "encounters_per_body": round(r[8], 2)} for r in rows]
    s, q, margin = firewall()
    out["firewall"] = {"sigma_dvarpi_rad": s, "q_varpi_rad": q, "margin": margin}
    # 10^9 extrapolation at t=100, lam=1.1, near fraction 1e-3
    last = out["lambdas"]["1.1"][-1]
    phi_run = (2 * (1 << (20 - 6)) / (1 << 20))       # near fraction in the run: 2/32
    far_sat = (last["twotier_bits_per_body"] - phi_run * NAIVE_BITS) / (1 - phi_run)
    out["extrapolation_1e9"] = {
        "naive_GB": NAIVE_BITS * 1e9 / 8e9,
        "onetier_t100_GB": last["onetier_bits_per_body"] * 1e9 / 8e9,
        "twotier_t100_GB": (1e-3 * NAIVE_BITS + (1 - 1e-3) * far_sat) * 1e9 / 8e9,
        "far_sat_bits": far_sat,
        "promotion_replay_encounters_mean": 1.1 * 100}
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "results.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(f"done in {time.time()-t0:.1f}s; naive={NAIVE_BITS} bits/body")
    for lam in LAMBDAS:
        r = out["lambdas"][str(lam)]
        print(f"\nlambda={lam}:  t scarred ret_tot  1tier  2tier  occ  (bits/body)")
        for x in r:
            print(f"  t={x['t']:3d} {x['scarred_frac']:.3f} {x['returned_total']:6d}"
                  f" {x['onetier_bits_per_body']:7.2f} {x['twotier_bits_per_body']:6.2f}"
                  f" {x['occupancy_bits_per_body']:7.3f}")
    print("\nfirewall margin (q_varpi/sigma):", f"{margin:.3g}")
    print("extrapolation:", json.dumps(out["extrapolation_1e9"], indent=1))
