#!/usr/bin/env python3
"""Scout falsifier: how fast does live distinguishing state (H_live) grow?

Event-driven belt toy. Rate-structure model, not trajectory dynamics:
- conjunction rate Gamma per body per orbit (anchored to r8's measured 1.1/orbit),
- impulse kick dv = 2 G m / (b v_rel), b uniform in [b_floor, b_max] (synodic shear
  sweeps azimuth linearly), v_rel from epicyclic + shear speeds,
- state = current (a, e); quantum cells of relative width eps on a and e;
  a body is DISTINGUISHED iff its current cell differs from its generator cell
  (lazy replay from the seed would reproduce the generator cell).
Accounting: R0 naive 88 B/body; R1 16 B/tube; R2 cell-delta with empirical entropy;
R3 shared references per occupied cell (CRAM/git-pack style). Cone variant keeps
only encounters whose light has arrived at the player.
Deterministic: seed everything. <2 GB, seconds.
"""
import json, math, os, sys
import numpy as np

G = 4.0 * math.pi ** 2          # AU^3 / (M_sun yr^2)
C = 63241.0                      # AU / yr
YR_S = 3.156e7
RTF = 100.0
GS_PER_YR = YR_S / RTF           # game-seconds (real seconds at the player) per sim-year

def run(N=200_000, gamma0=1.1, sigma_e=0.05, m=1e-10, eps=1e-3, feedback=False,
        pos="belt", steps=300, orbits=3.0, seed=7, contacts_only_note=False):
    rng = np.random.default_rng(seed)
    a0 = rng.uniform(2.0, 2.4, N)                 # AU
    e0 = rng.rayleigh(sigma_e, N)
    if pos == "belt":
        dist = a0.copy()                          # encounter distance ~ orbital radius
    else:                                         # wide nursery: same orbits, spread tags
        dist = rng.uniform(0.05, 1000.0, N)
    a, e = a0.copy(), e0.copy()
    a_mid = 2.2
    vK = 2.0 * math.pi * np.sqrt(a / G)           # AU/yr (circular speed at a)
    P = 2.0 * math.pi * np.sqrt(a ** 3 / G)       # yr
    # physical radius for contact test, rho=2.5 g/cc: R = (3m/4pi rho)^(1/3)
    rho = 2.5 / 1.989e33 * (1.496e13) ** 3        # M_sun / AU^3
    Rbody = (3.0 * m / (4 * math.pi * rho)) ** (1.0 / 3.0)
    cell_a = eps * a_mid                          # absolute quantum on a
    cell_e = eps                                  # absolute quantum on e
    ka0 = np.round(a0 / cell_a).astype(np.int64)
    ke0 = np.round(e0 / cell_e).astype(np.int64)
    dt = orbits * P.mean() / steps
    t = 0.0
    hist = []                                     # (t_yr, D, arrived_D, contacts, events)
    arr_time = np.full(N, np.inf)                  # earliest light-arrival at the player
    contacts = 0
    events = 0
    for step in range(steps):
        gam = gamma0 if not feedback else gamma0 * np.clip(
            (e + sigma_e) / (2 * sigma_e), 0.05, 20.0)
        lam = gam * dt / P
        nev = rng.poisson(lam)                    # encounters per body this step
        idx = np.repeat(np.arange(N), nev)
        if idx.size:
            events += idx.size
            bmax = a[idx] * np.maximum(e[idx] + sigma_e, 2e-3)
            b = bmax * rng.random(idx.size) + 2 * Rbody
            vrel = np.maximum(vK[idx] * (e[idx] + sigma_e) * 0.5, b * vK[idx] / (2 * a[idx]))
            dv = 2 * G * m / (b * vrel)           # AU/yr
            contacts += int(np.sum(b < 2 * Rbody * 1.5))
            dv = np.where(b < 2 * Rbody * 1.5, 0.0, dv)   # contacts are lattice events, not belt kicks
            da = a[idx] * 2 * (dv / vK[idx]) * rng.choice((-1.0, 1.0), idx.size)
            de = 2 * (dv / vK[idx]) * rng.choice((-1.0, 1.0), idx.size)
            np.add.at(a, idx, da)
            np.add.at(e, idx, de)
            np.clip(e, 0.0, 0.9, out=e)
            t_arr = t + dist[idx] / C              # when the light reaches the player
            np.minimum.at(arr_time, idx, t_arr)    # conservative: earliest arrival sticks
        t += dt
        ka = np.round(a / cell_a).astype(np.int64)
        ke = np.round(e / cell_e).astype(np.int64)
        D = int(np.sum((ka != ka0) | (ke != ke0)))
        D_arr = int(np.sum(((ka != ka0) | (ke != ke0)) & (arr_time <= t)))
        hist.append((t, D, D_arr, contacts, events))
    ka = np.round(a / cell_a).astype(np.int64)
    ke = np.round(e / cell_e).astype(np.int64)
    dis = (ka != ka0) | (ke != ke0)
    m_ = (ka != ka0); e_ = (ke != ke0)
    esc_a = int((m_ & ~e_).sum()); esc_e = int((e_ & ~m_).sum()); esc_both = int((m_ & e_).sum())
    def Hj(kax, kex):
        _, c = np.unique(kax.astype(np.int64) * (1 << 24) + kex, return_counts=True)
        p = c / c.sum()
        return float(-(p * np.log2(p)).sum())
    Hj0, Hj1 = Hj(ka0, ke0), Hj(ka, ke)
    # ---- accounting ----
    id_bits = math.log2(N / max(D, 1))
    dka = (ka[dis] - ka0[dis])
    dke = (ke[dis] - ke0[dis])
    def H(x):
        if x.size == 0: return 0.0
        _, c = np.unique(x, return_counts=True)
        p = c / c.sum()
        return float(-(p * np.log2(p)).sum())
    H_delta = H(dka) + H(dke)
    # R3: shared references per occupied (ka,ke) cell
    cells, cnt = np.unique(ka[dis].astype(np.int64) * (1 << 24) + ke[dis], return_counts=True)
    cell_bits = math.log2(1 / eps) + 8            # address of a reference cell
    shared = int((cnt >= 2).sum())
    R3_bits = float(np.sum(np.where(cnt >= 2, cell_bits + cnt * id_bits,
                                    cnt * (id_bits + H_delta / max(D, 1)))))
    out = dict(N=N, gamma0=gamma0, m=m, eps=eps, feedback=feedback, pos=pos,
               orbits=orbits, events=events, contacts=contacts, D=D,
               s_frac=D / max(2 * events, 1),
               R0_MB=N * 88 / 1e6, R1_MB=D * 16 / 1e6,
               R2_MB=D * (id_bits + H_delta) / 8 / 1e6, R3_MB=R3_bits / 8 / 1e6,
               shared_frac=shared / max(len(cells), 1),
               esc_a=esc_a, esc_e=esc_e, esc_both=esc_both, Hj0=Hj0, Hj1=Hj1,
               D_over_N=D / N,
               hist_t=[h[0] for h in hist], hist_D=[h[1] for h in hist],
               hist_Darr=[h[2] for h in hist])
    # inflow fits (game-seconds)
    tg = np.array(out["hist_t"]) * GS_PER_YR
    Dd = np.array(out["hist_D"], float)
    sel = (Dd > 0) & (Dd < 0.05 * N) & (tg > tg[0])
    if sel.sum() > 20:
        out["inflow_exp"] = float(np.polyfit(np.log(tg[sel]), np.log(np.maximum(Dd[sel], 1)), 1)[0])
    else:
        out["inflow_exp"] = None
    return out, dict(a=a, a0=a0, ka=ka, ka0=ka0, D=D, tg=tg, Dd=Dd, events=events,
                     hist=hist, dist=dist)

def fit_power(x, y):
    x, y = np.array(x, float), np.array(y, float)
    ok = (x > 0) & (y > 0) & (y < 1.0)
    if ok.sum() < 3:
        return None
    return float(np.polyfit(np.log(x[ok]), np.log(y[ok]), 1)[0])

if __name__ == "__main__":
    import subprocess
    load = subprocess.run(["cat", "/proc/loadavg"], capture_output=True, text=True).stdout.split()
    results = {}
    print(f"machine state: load1={load[0]} load5={load[1]} (8 vCPU, shared)")
    # S6 positive control: no encounters -> exactly zero live bits
    r, _ = run(gamma0=0.0)
    assert r["D"] == 0 and r["R2_MB"] == 0.0, "positive control failed"
    print("S6 positive control (Gamma=0): D=0, live bits=0  PASS")
    results["S6_control"] = {k: r[k] for k in ("D", "R2_MB")}
    # S1 baseline
    r, aux = run()
    results["S1_baseline"] = {k: r[k] for k in (
        "N", "gamma0", "m", "eps", "events", "contacts", "D", "s_frac", "inflow_exp",
        "R0_MB", "R1_MB", "R2_MB", "R3_MB", "shared_frac", "esc_a", "esc_e", "esc_both",
        "Hj0", "Hj1", "D_over_N")}
    print("S1 baseline:", json.dumps(results["S1_baseline"], indent=1))
    # S2 epsilon sweep (Ceres-scale and heavier masses)
    for m in (1e-10, 1e-8, 1e-6):
        rows = []
        for eps in (1e-2, 3e-3, 1e-3, 3e-4, 1e-4, 3e-5, 1e-5, 1e-6, 1e-7, 1e-8):
            rr, _ = run(N=100_000, m=m, eps=eps, steps=200)
            rows.append((eps, rr["s_frac"], rr["inflow_exp"]))
        alpha = fit_power([x[0] for x in rows], [x[1] for x in rows])
        results[f"S2_m{m:g}"] = dict(rows=[(f"{a:g}", round(b, 4), c) for a, b, c in rows],
                                     alpha_partial=alpha)
        print(f"S2 m={m:g}: alpha(partial regime)={alpha}", rows)
    # S3 stirring feedback
    r3, _ = run(feedback=True)
    results["S3_stirring"] = {k: r3[k] for k in ("D", "D_over_N", "events", "s_frac", "inflow_exp", "R2_MB")}
    print("S3 stirring:", results["S3_stirring"])
    # S3b stirring with a planetary scatterer (Jupiter class)
    r3b, _ = run(feedback=True, m=1e-4, N=100_000, steps=150)
    results["S3b_stirring_jupiter"] = {k: r3b[k] for k in ("D", "D_over_N", "events", "s_frac", "inflow_exp", "Hj1")}
    print("S3b stirring (m=1e-4):", results["S3b_stirring_jupiter"])
    # S4 cone: wide active nursery within R=1000 AU, run ~4x its light-crossing time
    # T_x = 1000/C yr ~ 5000 game-seconds (~1.4 play-hours at rtf 100)
    r4, _ = run(pos="wide", N=200_000, gamma0=5.0, orbits=0.02, steps=500)
    Tx_gs = 1000.0 / C * GS_PER_YR
    tg = np.array(r4["hist_t"]) * GS_PER_YR
    Da = np.array(r4["hist_Darr"], float)
    Dt = np.array(r4["hist_D"], float)
    early = (tg < 0.7 * Tx_gs) & (Da > 0)
    late = (tg > 2.0 * Tx_gs)
    e_early = float(np.polyfit(np.log(tg[early]), np.log(Da[early]), 1)[0]) if early.sum() > 10 else None
    inc_late = float(np.mean(np.diff(Da[late]) / np.mean(np.diff(tg[late])))) if late.sum() > 10 else None
    inc_tot = float(np.mean(np.diff(Dt[-int(len(Dt) * 0.4):]) / np.mean(np.diff(tg[-int(len(tg) * 0.4):]))))
    ratio_late = float(np.mean(inc_late / inc_tot)) if inc_late and inc_tot else None
    results["S4_cone"] = dict(Tx_game_seconds=Tx_gs, early_exponent=e_early,
                              late_over_total_inflow=ratio_late,
                              ram_equals_total_after_gs=float(tg[np.argmax(Da >= 0.98 * Dt[-1])])
                              if np.any(Da >= 0.98 * Dt[-1]) else None)
    print("S4 cone:", results["S4_cone"])
    # S5 N invariance
    infl = []
    for Nn in (50_000, 100_000, 200_000):
        rr, _ = run(N=Nn, steps=150)
        infl.append((Nn, rr["D"] / rr["events"], rr["inflow_exp"]))
    results["S5_N"] = infl
    print("S5 N-invariance (D/events should be ~constant):", infl)
    # extrapolation to 1e9 bodies, per play-hour, at the player floor eps=1e-3
    # events/game-second at belt scale: N * gamma/orbit / (P in game-seconds)
    P_gs = (2 * math.pi * math.sqrt(2.2 ** 3 / G)) * GS_PER_YR
    for m in (1e-10, 1e-8, 1e-6):
        for eps in (1e-3, 1e-4):
            rr, _ = run(N=100_000, m=m, eps=eps, steps=150)
            ev_gs = 1e9 * 1.1 / P_gs
            mb_h = ev_gs * 3600 * 2 * rr["s_frac"] * 16 / 1e6   # R1 upper bound
            results.setdefault("S7_extrap", {})[f"m{m:g}_eps{eps:g}"] = dict(
                ev_per_gs=ev_gs, s=rr["s_frac"], D_over_N=rr["D_over_N"],
                R1_MB_per_play_hour=mb_h, rebase_bits_per_body=rr["Hj1"])
    print("S7 extrapolation 1e9 bodies:", json.dumps(results["S7_extrap"], indent=1))
    json.dump(results, open(os.path.join(os.path.dirname(__file__), "metrics.json"), "w"), indent=1)
    print("wrote metrics.json")
