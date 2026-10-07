#!/usr/bin/env python3
"""Measure the plane's ACTUAL belt (run ...-fa84, second author on 20261007-2155-fermi-ef1d).

The checker's named gold experiment: the decisive hot case of the H_live run rests on an
ASSUMED tau_L = 300 orbits for the whole belt. This script measures the real thing on the
shipped configuration and nothing else:

  - Perturbers (crates/universe/src/scenario.rs::PLANETS, the plane the game flies):
      Cinder  mass 2^-21 Msun, a = 0.3904 AU, e = 0.10   (periapsis 35_600_000 root units)
      Home    mass 2^-18 Msun, a = 1.0003 AU, e = 0.02   (periapsis  99_300_000)
      Giant   mass 2^-10 Msun, a = 5.1956 AU, e = 0.05   (periapsis 500_000_000)
    AU = 101_300_000 root units. These masses ARE the real perturber mass function.
  - Belt: B18b's frozen SPEC shape (xtask/src/behave/belt.rs): p uniform over a band with
    ratio 2560/2048 = 1.25, e Rayleigh sigma 0.07 capped at 0.6, angles uniform. Placed at
    the band the game's own scale implies, 2.0-2.5 AU (Home inside, Giant outside), which is
    also the toy's fiducial neighbourhood.
  - Dynamics: test particles (the belt is massless as shipped; peer self-scattering is the
    toy's layer, unchanged) under the four massive bodies integrated as a full Newtonian
    N-body system, DOP853 rtol 1e-12. Particles: symplectic KDK leapfrog dt = 0.02 yr
    (= P_belt/142 at 2 AU), planets read from a cubic spline of the DOP853 solution,
    precomputed on the kick grid.

Measured per body: osculating a(t), e(t) at log-spaced checkpoints over 10^4 yr (the toy's
horizon). tau_L from the growth of the a-residual after removing a per-body LINEAR drift
(the most any program re-fit could absorb for a secular body; the toy showed re-fit absorbs
drift, not spread). Regular bodies: slope ~ 0 (bounded residual). Chaotic: rms(w) e-folds.

Controls: (i) negative: no planets -> residual growth must sit at the integrator floor;
(ii) dt/2 on a subset (false chaos from the stepper would move tau_L);
(iii) massive-body energy drift reported.
Floats explore; the measured RATES are the output, integers decide downstream in hlive2.py.
"""
import json, math, os, sys, time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline

G  = 2.959122082855911e-4      # AU^3 / (Msun yr^2), Gaussian k^2
MU = {"Cinder": 2.0**-21, "Home": 2.0**-18, "Giant": 2.0**-10}
PLANETS = [  # name, mass, a (AU), e, angle0 (rad)  [scenario.rs::PLANETS, e_q48/(1<<48)]
    ("Cinder", MU["Cinder"], 35_600_000 / 101_300_000 / (1 - 0.10), 0.10, (0x3000_0000 / 2**32) * 2 * math.pi),
    ("Home",   MU["Home"],   99_300_000 / 101_300_000 / (1 - 0.02), 0.02, (0x9000_0000 / 2**32) * 2 * math.pi),
    ("Giant",  MU["Giant"], 500_000_000 / 101_300_000 / (1 - 0.05), 0.05, (0xC000_0000 / 2**32) * 2 * math.pi),
]
MS = 1.0 - sum(m for _, m, *_ in PLANETS)   # the star, in Msun
T_END = 1.0e4
CKPT = np.concatenate([[20.0, 50.0], np.geomspace(100.0, T_END, 40)])
def kepler_start(a, e, om, M):

    """Heliocentric Kepler state (AU, AU/yr) about the star only, at mean anomaly M."""
    mu = G * MS
    E = np.asarray(M, dtype=float).copy()
    for _ in range(64):                       # Newton, vectorized
        f, fp = E - e * np.sin(E) - M, 1.0 - e * np.cos(E)
        d = f / fp
        E -= d
        if np.max(np.abs(d)) < 1e-14:
            break
    cO, sO, cE, sE = np.cos(om), np.sin(om), np.cos(E), np.sin(E)
    r = a * (1.0 - e * cE)
    vg = np.sqrt(mu * a) / r
    x = a * (cO * (cE - e) - sO * sE * np.sqrt(1 - e * e))
    y = a * (sO * (cE - e) + cO * sE * np.sqrt(1 - e * e))
    vx = -vg * (cO * sE + sO * cE * np.sqrt(1 - e * e))
    vy = -vg * (sO * sE - cO * cE * np.sqrt(1 - e * e))
    return x, y, vx, vy

def massive_solution(t_grid):
    """Full Newtonian 4-body (star + 3 planets), barycentric, DOP853 rtol 1e-12."""
    masses = np.array([MS] + [p[1] for p in PLANETS])
    x0 = np.zeros((4, 4))                     # pos+vel per body, barycentric
    for j, (_, m, a, e, ang) in enumerate(PLANETS, start=1):
        hx, hy, hvx, hvy = kepler_start(np.array([a]), np.array([e]), np.array([ang]), np.array([0.0]))
        x0[j, :2], x0[j, 2:] = (hx[0], hy[0]), (hvx[0], hvy[0])
    _t0_m = time.time()
    x0[0, :2] = -(masses[1:, None] * x0[1:, :2]).sum(0) / MS
    x0[0, 2:] = -(masses[1:, None] * x0[1:, 2:]).sum(0) / MS
    def rhs(t, y):
        p = y.reshape(4, 4)
        d = p[None, :, :2] - p[:, None, :2]
        r3 = np.linalg.norm(d, axis=-1) ** 3
        np.fill_diagonal(r3, 1.0)
        acc = (G * masses[None, :, None] * d / r3[..., None]).sum(1)
        return np.concatenate([p[:, 2:], acc], axis=1).ravel()
    def energy(y):
        p = y.reshape(4, 4)
        ke = 0.5 * (masses * (p[:, 2:] ** 2).sum(1)).sum()
        d = p[None, :, :2] - p[:, None, :2]
        dist = np.linalg.norm(d, axis=-1)
        return ke - (G * (masses[:, None] * masses[None, :]) / np.where(dist > 0, dist, 1.0))[np.triu_indices(4, 1)].sum()
    sol = solve_ivp(rhs, (0.0, t_grid[-1]), x0.ravel(), method="DOP853", rtol=1e-10, atol=1e-12,
                    t_eval=t_grid, dense_output=False)
    assert sol.success, sol.message
    drift = abs(energy(sol.y[:, -1]) / energy(sol.y[:, 0]) - 1.0)
    print(f"  massive_solution: {len(sol.t)} grid pts, drift {drift:.1e}, {time.time()-_t0_m:.0f}s", file=sys.stderr)
    return sol.t, sol.y.reshape(4, 4, -1), masses, drift
def run(name, n, t_end, dt, planets_on=True, seed=0xFA84):
    t0 = time.time(); print(f"[{time.strftime('%H:%M:%S')}] start {name} (n={n}, dt={dt})", file=sys.stderr)
    rng = np.random.default_rng(seed)
    ckpt = np.unique(CKPT[CKPT <= t_end])
    # belt draws: B18b SPEC shape at 2.0-2.5 AU
    a0 = 2.0 + 0.5 * rng.random(n)
    e0 = np.minimum(rng.rayleigh(0.07, n), 0.6)
    om = rng.random(n) * 2 * math.pi
    M0 = rng.random(n) * 2 * math.pi
    steps = int(round(t_end / dt))
    half = dt / 2.0
    ngrid = 2 * steps + 3                    # one spare half-step against float rounding
    # massive bodies: DOP853 (or a fixed star for the negative), positions precomputed
    # on the half-step grid so the kick loop never evaluates a spline.
    if planets_on:
        grid = np.linspace(0.0, (ngrid - 1) * half, ngrid)
        ts, ys, masses, drift = massive_solution(grid)
        spl = [[CubicSpline(ts, ys[j][k]) for k in range(4)] for j in range(4)]
        MP = np.array([[spl[j][k](grid) for k in range(2)] for j in range(4)])   # (4, 2, T)
        MCHK = np.array([[spl[j][k](ckpt) for k in range(4)] for j in range(4)]) # (4, 4, C)
        GM = G * masses
    else:
        MP = np.zeros((4, 2, ngrid))
        GM = np.array([G * MS, 0.0, 0.0, 0.0])
        MCHK = np.zeros((4, 4, len(ckpt)))
        drift = 0.0
    # particles, barycentric start (heliocentric Kepler state + star's barycentric state)
    hx, hy, hvx, hvy = kepler_start(a0, e0, om, M0)
    x = np.stack([hx + MCHK[0, 0, 0], hy + MCHK[0, 1, 0]])
    v = np.stack([hvx + MCHK[0, 2, 0], hvy + MCHK[0, 3, 0]])
    if not planets_on:
        x, v = np.stack([hx, hy]), np.stack([hvx, hvy])
    def acc(x, k):
        d = MP[:, :, k][:, :, None] - x[None, :, :]
        r = np.linalg.norm(d, axis=1)
        return (GM[:, None, None] * d / r[:, None, :] ** 3).sum(0)
    rec_a, rec_e = np.zeros((len(ckpt), n)), np.zeros((len(ckpt), n))
    ci, t = 0, 0.0
    for k in range(steps):
        v += half * acc(x, 2 * k + 1)
        x += dt * v
        v += half * acc(x, 2 * k + 2)
        t += dt
        while ci < len(ckpt) and t >= ckpt[ci] - 1e-9:
            rx, ry = x[0] - MCHK[0, 0, ci], x[1] - MCHK[0, 1, ci]
            vx, vy = v[0] - MCHK[0, 2, ci], v[1] - MCHK[0, 3, ci]
            r = np.hypot(rx, ry)
            v2 = vx * vx + vy * vy
            rec_a[ci] = 1.0 / (2.0 / r - v2 / (G * MS))
            rv = rx * vx + ry * vy
            rec_e[ci] = np.hypot((v2 - G * MS / r) * rx - rv * vx, (v2 - G * MS / r) * ry - rv * vy) / (G * MS)
            ci += 1
    wall = time.time() - t0
    out = dict(cfg=name, n=n, t_end=t_end, dt=dt, wall_s=round(wall, 1),
               massive_energy_drift=float(drift))
    # ---- analysis: per-body tau_L from a-residual growth (linear drift removed) ----
    tmask = ckpt >= 100.0
    ta, ra = ckpt[tmask], rec_a[tmask]
    fit = np.polyfit(ta, ra, 1)
    res = ra - (fit[0][None, :] * ta[:, None] + fit[1][None, :])
    wins = [(100, 316), (316, 1000), (1000, 3162), (3162, 10000)]
    rms = np.array([np.sqrt((res[(ta >= w0) & (ta < w1)] ** 2).mean(0)) for w0, w1 in wins])
    tc = np.array([math.sqrt(w0 * w1) for w0, w1 in wins])
    ok = np.isfinite(rms).all(0) & (rms > 0).all(0)
    slope = np.full(n, np.nan)
    slope[ok] = np.polyfit(tc, np.log(rms[:, ok]), 1)[0]
    tau_yr = np.where(slope > 0, 1.0 / np.maximum(slope, 1e-12), np.inf)
    Porb = a0 ** 1.5
    tau_orb = tau_yr / Porb
    chaotic = tau_yr < 3.0e4                  # e-folds at least ~1.4x by 1e4 yr
    out.update(dict(
        a0=a0.tolist(), e0=e0.tolist(), tau_yr=tau_yr.tolist(), tau_orb=tau_orb.tolist(),
        chaotic=chaotic.tolist(), chaotic_frac=float(chaotic.mean()),
        bounded_rms_AU_regular=float(np.median(rms[-1][~chaotic & ok])) if (~chaotic & ok).any() else None,
        tau_yr_chaotic_median=float(np.median(tau_yr[chaotic])) if chaotic.any() else None,
        e_final=rec_e[-1].tolist(), a_final=rec_a[-1].tolist(),
        e_exceed_cap=float((rec_e[-1] > 0.6).mean()),
        a_out_of_band=float(((rec_a[-1] < 2.0) | (rec_a[-1] > 2.5)).mean()),
    ))
    return out

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    os.makedirs("out", exist_ok=True)
    if mode == "smoke":
        r = run("smoke", 512, 1000.0, 0.02)
        print(f"smoke: chaotic_frac={r['chaotic_frac']:.4f} wall={r['wall_s']}s "
              f"massive_drift={r['massive_energy_drift']:.2e}")
        return
    if mode == "negative":
        r = run("negative_no_planets", 2048, 3000.0, 0.02, planets_on=False)
        print(f"negative (no planets): chaotic_frac={r['chaotic_frac']:.5f} (must be ~0), "
              f"shortest tau_yr={np.nanmin(r['tau_yr']):.3g} (integrator floor)")
        json.dump({k: r[k] for k in ("cfg", "chaotic_frac", "n", "massive_energy_drift")},
                  open("out/negative.json", "w"))
        return
    runs = [
        run("measured", 8192, T_END, 0.02, seed=0xFA84),
        run("dt_half", 2048, T_END, 0.01, seed=0xFA84),
    ]
    json.dump(runs, open("out/taul.json", "w"))
    for r in runs:
        ch = np.array(r["chaotic"])
        tau = np.array(r["tau_orb"])
        print(f"{r['cfg']}: n={r['n']} chaotic_frac={r['chaotic_frac']:.4f} "
              f"tau_orb med={np.median(tau[ch]) if ch.any() else float('nan'):.1f} "
              f"p10={np.percentile(tau[ch], 10) if ch.any() else float('nan'):.1f} "
              f"p90={np.percentile(tau[ch], 90) if ch.any() else float('nan'):.1f} "
              f"e>cap={r['e_exceed_cap']:.5f} a_out={r['a_out_of_band']:.5f} "
              f"drift={r['massive_energy_drift']:.2e} wall={r['wall_s']}s")
    m = runs[0]
    ch = np.array(m["chaotic"]); a0 = np.array(m["a0"])
    print("chaotic fraction by 0.05-AU a-bin:",
          [f"{2.0 + 0.05 * i:.2f}:{(ch[(a0 >= 2.0 + 0.05 * i) & (a0 < 2.05 + 0.05 * i)]).mean():.3f}"
           for i in range(10)])

if __name__ == "__main__":
    main()
