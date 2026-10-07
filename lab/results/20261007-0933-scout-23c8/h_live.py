#!/usr/bin/env python3
"""H_live falsifier: scar-entropy production + finite-time Lyapunov per regime.

Restricted planar N-body: star GM=1, belt of massless bodies, one perturber on a
fixed Kepler orbit. Drift = exact Kepler in osculating elements; kicks carry the
perturber's pull + the indirect term (law.md's own split). All float64: floats
explore; this judges behaviours (growth laws, tails), not canonical outcomes.

Scar = (dE, dL) of each body vs its birth program, quantized at q. Entropy of
the scar distribution = bits/body the universe created that the program cannot
absorb (law.md: kicks change E and L; shipmem stores scars).

Usage: h_live.py S0|S1|S1b|S2|S3
"""
import json
import sys
import time

import numpy as np

TWO_PI = 2.0 * np.pi
EJECT_E = 0.97  # beyond this (or unbound) a body is frozen as a tracer, counted


def kepler_E(M, e, iters=12):
    E = M + e * np.sin(M)
    for _ in range(iters):
        f = E - e * np.sin(E) - M
        E = E - f / (1.0 - e * np.cos(E))
    return E


def elements_to_rv(a, e, w, M):
    E = kepler_E(M, e)
    cE, sE = np.cos(E), np.sin(E)
    n = a ** -1.5
    sq = np.sqrt(1.0 - e * e)
    xo = a * (cE - e)
    yo = a * sq * sE
    den = 1.0 - e * cE
    vxo = -a * n * sE / den
    vyo = a * n * sq * cE / den
    cw, sw = np.cos(w), np.sin(w)
    return (xo * cw - yo * sw, xo * sw + yo * cw,
            vxo * cw - vyo * sw, vxo * sw + vyo * cw)


def rv_to_elements(x, y, vx, vy):
    r = np.hypot(x, y)
    v2 = vx * vx + vy * vy
    a = 1.0 / (2.0 / r - v2)
    rv = x * vx + y * vy
    ex = (v2 - 1.0 / r) * x - rv * vx
    ey = (v2 - 1.0 / r) * y - rv * vy
    e = np.hypot(ex, ey)
    w = np.arctan2(ey, ex)
    ok = (a > 0.05) & np.isfinite(a) & np.isfinite(e)
    a = np.where(ok, a, 1.0)
    e = np.where(ok, np.clip(e, 0.0, EJECT_E), 1.0)
    cE = np.clip(1.0 - r / a, -1.0, 1.0)
    sE = np.clip(rv / np.sqrt(a), -1.0, 1.0)
    E = np.arctan2(sE, cE)
    return a, e, w, (E - e * np.sin(E)) % TWO_PI, ~ok


def perturber_xy(ap, ep, wp, Mp):
    E = kepler_E(Mp, ep)
    cE, sE = np.cos(E), np.sin(E)
    xo = ap * (cE - ep)
    yo = ap * np.sqrt(1.0 - ep * ep) * sE
    cw, sw = np.cos(wp), np.sin(wp)
    return xo * cw - yo * sw, xo * sw + yo * cw


def kick(a, e, w, M, xp, yp, mu, dt):
    x, y, vx, vy = elements_to_rv(a, e, w, M)
    dx, dy = xp - x, yp - y
    d3 = (dx * dx + dy * dy) ** 1.5
    rp3 = (xp * xp + yp * yp) ** 1.5
    vx += mu * (dx / d3 - xp / rp3) * dt
    vy += mu * (dy / d3 - yp / rp3) * dt
    a2, e2, w2, M2, unbound = rv_to_elements(x, y, vx, vy)
    bad = unbound | (e2 > EJECT_E)
    if bad.any():
        a2[bad] = a[bad]
        e2[bad] = e[bad]
        w2[bad] = w[bad]
        M2[bad] = M[bad]
    return a2, e2, w2, M2, int(bad.sum())


def scar_entropy_bits(dE, dL, q):
    """Plug-in entropy in bits of the 2-D quantized scar; range-free."""
    k1 = np.floor(dE / q).astype(np.int64)
    k2 = np.floor(dL / q).astype(np.int64)
    keys = np.stack([k1, k2], axis=1)
    _, counts = np.unique(keys, axis=0, return_counts=True)
    p = counts / counts.sum()
    return float(-(p * np.log2(p)).sum()), int(counts.size)


def run_scene(name, N=8192, orbits=16, steps_per_orbit=120, mu=1e-3,
              ap=5.2, ep=0.05, belt_a=1.0, belt_da=0.03, sig_e=0.02, seed=7):
    rng = np.random.default_rng(seed)
    t0 = time.time()
    a = belt_a + rng.uniform(-belt_da, belt_da, N)
    e = np.clip(np.abs(rng.normal(0.0, sig_e, N)) + 1e-3, 0.0, 0.6)
    w = rng.uniform(0, TWO_PI, N)
    M = rng.uniform(0, TWO_PI, N)
    n = a ** -1.5
    E0 = -1.0 / (2.0 * a)
    L0 = np.sqrt(a * (1.0 - e * e))

    wp = 0.0
    Mp0 = float(rng.uniform(0, TWO_PI))
    np_ = ap ** -1.5

    # Benettin shadow pairs (no renormalization; d0=1e-9)
    nsh = min(256, N)
    si = np.arange(0, N, N // nsh)[:nsh]
    ash, esh, wsh = a[si].copy(), e[si].copy(), w[si].copy()
    Msh = (M[si] + 1e-9 / (a[si] * (1.0 - e[si]))) % TWO_PI

    h = TWO_PI / steps_per_orbit
    t = 0.0
    clamped_total = 0
    frozen = np.zeros(N, dtype=bool)
    enc_min = np.full(N, np.inf)
    rhill = ap * (mu / 3.0) ** (1.0 / 3.0)
    qs = SCENES_QS[name]
    samples = sorted({1, 2, 4, orbits // 2, orbits})
    sample_steps = {int(round(s * steps_per_orbit)) for s in samples}
    out = {"scene": name, "N": N, "orbits": orbits, "mu": mu, "ap": ap, "ep": ep,
           "belt_a": belt_a, "steps_per_orbit": steps_per_orbit,
           "samples_t": [], "H_q": {f"{q:g}": [] for q in qs},
           "occupied": {f"{q:g}": [] for q in qs},
           "p99_absdE": [], "median_absdE": [], "clamped": [], "enc_frac": [],
           "frozen_frac": []}

    for step in range(orbits * steps_per_orbit):
        xp, yp = perturber_xy(ap, ep, wp, (Mp0 + np_ * t) % TWO_PI)
        a, e, w, M, ncl = kick(a, e, w, M, xp, yp, mu, h / 2)
        clamped_total += ncl
        M = (M + n * h) % TWO_PI
        xp, yp = perturber_xy(ap, ep, wp, (Mp0 + np_ * (t + h)) % TWO_PI)
        a, e, w, M, ncl = kick(a, e, w, M, xp, yp, mu, h / 2)
        clamped_total += ncl
        frozen |= e >= EJECT_E
        t += h
        # shadows: identical map, own state
        xps, yps = perturber_xy(ap, ep, wp, (Mp0 + np_ * t) % TWO_PI)
        ash, esh, wsh, Msh, _ = kick(ash, esh, wsh, Msh, xps, yps, mu, h / 2)
        Msh = (Msh + ash ** -1.5 * h) % TWO_PI
        ash, esh, wsh, Msh, _ = kick(ash, esh, wsh, Msh, xps, yps, mu, h / 2)
        if step % 10 == 0:
            x, y, _, _ = elements_to_rv(a, e, w, M)
            enc_min = np.minimum(enc_min, np.hypot(xp - x, yp - y))
        if (step + 1) in sample_steps:
            Et = -1.0 / (2.0 * a)
            Lt = np.sqrt(a * (1.0 - e * e))
            dE, dL = Et - E0, Lt - L0
            out["samples_t"].append((step + 1) / steps_per_orbit)
            for q in qs:
                H, occ = scar_entropy_bits(dE, dL, q)
                out["H_q"][f"{q:g}"].append(H)
                out["occupied"][f"{q:g}"].append(occ)
            out["p99_absdE"].append(float(np.percentile(np.abs(dE), 99)))
            out["median_absdE"].append(float(np.median(np.abs(dE))))
            out["clamped"].append(clamped_total)
            out["enc_frac"].append(float((enc_min < 3 * rhill).mean()))
            out["frozen_frac"].append(float(frozen.mean()))

    xb, yb, _, _ = elements_to_rv(a[si], e[si], w[si], M[si])
    xs, ys, _, _ = elements_to_rv(ash, esh, wsh, Msh)
    d_end = np.hypot(xs - xb, ys - yb)
    lam_T = np.log(np.maximum(d_end, 1e-300) / 1e-9)
    lam_T = np.where(np.isfinite(lam_T), lam_T, 40.0)  # unreadable -> saturated
    lam_per_orbit = lam_T / orbits
    sat = d_end > 1e-5
    out["shadow_d_end"] = d_end.tolist()
    out["lyap_median_per_orbit"] = float(np.median(lam_per_orbit))
    out["lyap_frac_Tlyap_lt1"] = float((lam_per_orbit > 1.0).mean())
    out["lyap_frac_sat"] = float(sat.mean())
    out["lyap_p99_per_orbit"] = float(np.percentile(lam_per_orbit, 99))
    out["lyap_pos_sum_bits_per_orbit"] = float(
        lam_per_orbit[lam_per_orbit > 0].sum() / np.log(2))
    out["wall_s"] = time.time() - t0
    out["qs"] = qs
    return out


SCENES = {
    "S0": dict(N=4096, orbits=6, steps_per_orbit=120, mu=0.0, ap=5.2, ep=0.05,
               belt_a=1.0, belt_da=0.03, sig_e=0.02),
    "S1": dict(N=8192, orbits=16, steps_per_orbit=120, mu=1e-3, ap=5.2, ep=0.05,
               belt_a=1.0, belt_da=0.03, sig_e=0.02),
    "S1b": dict(N=8192, orbits=16, steps_per_orbit=120, mu=1e-3, ap=4.75, ep=0.05,
                belt_a=1.0, belt_da=0.03, sig_e=0.02),
    "S2": dict(N=8192, orbits=16, steps_per_orbit=120, mu=1e-3, ap=2.08, ep=0.05,
               belt_a=2.08 * 2 ** (-2 / 3), belt_da=0.012, sig_e=0.02),
    "S3": dict(N=8192, orbits=10, steps_per_orbit=240, mu=1e-4, ap=1.35, ep=0.45,
               belt_a=1.0, belt_da=0.03, sig_e=0.05),
}

# per-scene quanta chosen to stay below the sampling cap log2(N)
SCENES_QS = {
    "S0": [1e-6, 1e-8],
    "S1": [1e-5, 1e-6, 1e-7],
    "S1b": [1e-5, 1e-6, 1e-7],
    "S2": [1e-4, 1e-5],
    "S3": [1e-3, 1e-4],
}

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "S1"
    res = run_scene(name, **SCENES[name])
    with open(f"h_live_{name}.json", "w") as f:
        json.dump(res, f, indent=1)
    print(f"=== {name} (mu={res['mu']:g}, ap={res['ap']}, ep={res['ep']}, "
          f"{res['orbits']} orbits, N={res['N']}, {res['wall_s']:.1f}s) ===")
    print("t(orbit)   [H(q)/occupied per quantum]                    p99|dE|    med|dE|   clamp enc3RH frozen")
    for i, t in enumerate(res["samples_t"]):
        cols = "".join(
            f"  H({q:g})={res['H_q'][f'{q:g}'][i]:7.3f}/{res['occupied'][f'{q:g}'][i]:5d}"
            for q in SCENES_QS[name])
        print(f"{t:8.2f}{cols}  {res['p99_absdE'][i]:.3e}  {res['median_absdE'][i]:.3e}"
              f"  {res['clamped'][i]:5d} {res['enc_frac'][i]:.3f} {res['frozen_frac'][i]:.3f}")
    print(f"FTLE/orbit: median {res['lyap_median_per_orbit']:.4g}  "
          f"frac(T_lyap<1 orbit) {res['lyap_frac_Tlyap_lt1']:.4f}  "
          f"sat {res['lyap_frac_sat']:.3f}  p99 {res['lyap_p99_per_orbit']:.4g}")
    nsh = len(res["shadow_d_end"])
    print(f"Pesin sum over {nsh} shadows: {res['lyap_pos_sum_bits_per_orbit']:.4g} "
          f"bits/orbit total = {res['lyap_pos_sum_bits_per_orbit'] / nsh:.4g} "
          f"bits/body/orbit")
