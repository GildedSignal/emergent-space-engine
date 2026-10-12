#!/usr/bin/env python3
"""H_live: the live distinction (scar-creation) rate of the engine's sparse scenes.

Law inputs used (docs/law.md): bodies are tubes stored as program + sparse scars
(shipmem, Form P); the allocator reads H_live as its memory budget; the tube's
periapsis angle is 32 bits, so the finest storable deflection is q32 = 2*pi/2^32.
A scar is created when a body's exact state departs from its program: distant
tide kicks are deterministic functions of stored programs (no scars in
principle); conjunction scatterings are the belt's gravitational channel.

Method: Monte-Carlo over iid pairs from the B18b-style belt program (a uniform
[2.1, 3.3] AU, Rayleigh e sigma=0.1, uniform angles, coplanar; D log-uniform
1-100 km, rho 2500 kg/m^3, host 1 Msun). Both members propagate as exact 2-D
Kepler orbits; local minima of the pair separation are conjunction approaches,
each recorded with its own (b, v_rel, mu_pair). Deflection q_max = 2*mu/(b*v^2).
Rates per body scale by (N-1) * <rate per sampled pair>. Thresholds below the
time grid's resolution (b ~ v*dt ~ 0.03 AU) are extrapolated on the measured
power law R(b) ~ b^alpha.
"""
import json, os, time
import numpy as np

AU = 1.495978707e11
YR = 3.156e7
G = 6.674e-11
MSUN = 1.98847e30
RHO = 2500.0
N_BELT = 2**20

rng = np.random.default_rng(20261012)

def sample_belt(n):
    a = rng.uniform(2.1, 3.3, n) * AU
    e = np.minimum(rng.rayleigh(0.1, n), 0.9)
    w = rng.uniform(0, 2 * np.pi, n)
    M0 = rng.uniform(0, 2 * np.pi, n)
    D = np.exp(rng.uniform(np.log(1e3), np.log(1e5), n))  # 1..100 km, log-uniform
    m = RHO * (np.pi / 6.0) * D**3
    return dict(a=a, e=e, w=w, M0=M0, m=m, n=np.sqrt(G * MSUN / a**3))

def kepler_pos_vel(body, t):
    """Positions and velocities of all bodies at times t (per-body t grid)."""
    M = body["M0"][:, None] + body["n"][:, None] * t[None, :]
    e = body["e"][:, None]
    E = M.copy()
    for _ in range(5):
        E = E - (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    cE, sE = np.cos(E), np.sin(E)
    r = body["a"][:, None]
    xo = r * (cE - e)
    yo = r * np.sqrt(1 - e**2) * sE
    f = body["n"][:, None] * body["a"][:, None] / (1.0 - e * cE)
    vxo = f * (-sE)
    vyo = f * np.sqrt(1 - e**2) * cE
    cw, sw = np.cos(body["w"])[:, None], np.sin(body["w"])[:, None]
    x = xo * cw - yo * sw
    y = xo * sw + yo * cw
    vx = vxo * cw - vyo * sw
    vy = vxo * sw + vyo * cw
    return np.stack([x, y], -1), np.stack([vx, vy], -1)

def belt_mc(P, T_yr, dt_days, chunk=128):
    T = T_yr * YR
    dt = dt_days * 86400.0
    steps = int(T / dt)
    b1 = sample_belt(P)
    b2 = sample_belt(P)
    body = {k: np.concatenate([b1[k], b2[k]]) for k in b1}
    mu_pair = G * (b1["m"] + b2["m"])
    B_MAX = 0.25 * AU
    ev_b, ev_v, ev_i = [], [], []
    tail = None
    t0 = time.time()
    for c0 in range(0, steps, chunk):
        t = (c0 + np.arange(chunk)) * dt
        pos, vel = kepler_pos_vel(body, t)
        p1, p2 = pos[:P], pos[P:]
        v1, v2 = vel[:P], vel[P:]
        d = p1 - p2
        sep = np.hypot(d[..., 0], d[..., 1])            # (P, chunk)
        s = sep if tail is None else np.concatenate([tail, sep], 1)
        inner = (s[:, 1:-1] < s[:, :-2]) & (s[:, 1:-1] <= s[:, 2:]) & (s[:, 1:-1] < B_MAX)
        pi, ci = np.nonzero(inner)
        if pi.size:
            gi = ci + 1 - (0 if tail is None else tail.shape[1])
            ev_b.append(s[pi, ci + 1])
            vv = np.hypot(v1[pi, gi, 0] - v2[pi, gi, 0], v1[pi, gi, 1] - v2[pi, gi, 1])
            ev_v.append(vv)
            ev_i.append(pi)
        tail = sep[:, -2:]
    b = np.concatenate(ev_b); v = np.concatenate(ev_v); idx = np.concatenate(ev_i)
    return b, v, idx, mu_pair, T, time.time() - t0

def main():
    out = {"machine": {
        "nproc": os.cpu_count(),
        "loadavg": list(os.getloadavg()),
        "mem_total_gb": round(os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 2**30, 1),
    }}
    P, T_yr, dt_d = 15000, 40.0, 3.0
    b, v, idx, mu_pair, T, wall = belt_mc(P, T_yr, dt_d)
    res_floor = float(np.median(v)) * 3.0 * 86400.0
    out["mc"] = {"pairs": P, "years": T_yr, "dt_days": dt_d, "wall_s": round(wall, 1),
                 "approaches_recorded": int(b.size),
                 "median_v_rel_kms": round(float(np.median(v)) / 1e3, 2),
                 "resolution_floor_b_AU": round(res_floor / AU, 4)}

    # R(B): measured approach rates at resolved thresholds + power-law fit
    Bs = np.array([0.05, 0.10, 0.15, 0.20, 0.25]) * AU
    rates = {}
    for B in Bs:
        cnt = np.count_nonzero(b < B)
        rates[f"{B/AU:.2f}AU"] = cnt / P / T_yr * (N_BELT - 1)
    lx = np.log(Bs); ly = np.log(list(rates.values()))
    alpha, lnc = np.polyfit(lx, ly, 1)
    out["approach_rate_per_body_per_yr"] = {k: float(x) for k, x in rates.items()}
    out["fit"] = {"exponent_alpha": round(float(alpha), 3),
                  "R_at_1AU_per_yr": float(np.exp(lnc))}

    # deflection-quantum sweep: every event carries its own mu_pair (exact)
    qs = {"q32": 2 * np.pi / 2**32, "q_1e-7": 1e-7, "q_1e-5": 1e-5, "q_1e-3": 1e-3}
    mu_ev = mu_pair[idx]
    v_med = float(np.median(v))
    R0, B0 = rates["0.05AU"], 0.05 * AU
    scar = {}
    for name, q in qs.items():
        qmax_ev = 2.0 * mu_ev / (b * v**2)
        meas = np.count_nonzero(qmax_ev > q) / P / T_yr * (N_BELT - 1)
        # unresolved part: approaches with b < res_floor; extrapolate R(b)=R0 (b/B0)^alpha
        # evaluated at the b threshold of a 100-km pair (the largest, binding scale)
        b_q100 = 2.0 * (G * 2 * RHO * (np.pi / 6.0) * 5e4**3) / (v_med**2 * q)
        extra = R0 * (b_q100 / B0)**alpha if b_q100 < B0 else 0.0
        scar[name] = {"measured": float(meas), "extrap_smallb": float(extra)}

    out["scar_rate_per_body_per_yr"] = scar
    out["memory_1e9_hour"] = {}
    for name in scar:
        r = (scar[name]["measured"] + scar[name]["extrap_smallb"]) / YR
        out["memory_1e9_hour"][name] = {
            "scars_per_body_per_game_second": r,
            "bytes_per_hour_rtf100_1e9_bodies": r * 1e9 * 3600 * 100 * 8}

    # contacts (real surprises): rate at b = 25 km, typical (D1+D2)/2
    rc = R0 * (25e3 / B0)**alpha
    out["contact_rate_per_body_per_yr"] = float(rc)
    out["memory_1e9_hour"]["contacts_25km"] = {
        "scars_per_body_per_game_second": rc / YR,
        "bytes_per_hour_rtf100_1e9_bodies": rc / YR * 1e9 * 3600 * 100 * 8}

    # cluster (dense order), kinetic 2-D, for contrast; radius per pre-registered scene
    out["cluster"] = {"bits_per_event_H0173": 4.0}
    for tag, r_disc in [("battle_10km", 1.0e4), ("dispersed_1e4km", 1.0e7)]:
        n_c, r_ship, v_c = 1e4, 10.0, 50.0
        r_ev = (n_c / (np.pi * r_disc**2)) * 2 * r_ship * v_c
        out["cluster"][tag] = {
            "events_per_body_per_game_second": r_ev,
            "bytes_per_hour_rtf100_1e6_ships": r_ev * 1e6 * 3600 * 100 * 8,
            "bytes_per_hour_rtf100_1e9_ships": r_ev * 1e9 * 3600 * 100 * 8}

    # drive stats: how fast conjunctions drive a body off its program. The
    # random-walk scar estimate is NOT reported: most steps exceed the finer
    # quanta, where the formula is invalid (it would exceed the event-count
    # upper bound). The correlation structure is the next run's measurement.
    qmax_all = 2.0 * mu_ev / (b * v**2)
    out["drive_rad_per_body_per_s"] = {
        "mean": float(np.mean(qmax_all)) * (N_BELT - 1) / YR,
        "median_event_qmax_rad": float(np.median(qmax_all)),
        "p90_event_qmax_rad": float(np.quantile(qmax_all, 0.9))}

    # budget crossover: the scar quantum where 10^9 belt bodies fit a bytes/hour
    # budget. Global power-law fit plus local interpolation between the two
    # bracketing measured quanta (the mixture of sizes bends the law in q).
    qv = np.array([2 * np.pi / 2**32, 1e-7, 1e-5, 1e-3])
    rv = np.array([(scar[k]["measured"] + scar[k]["extrap_smallb"]) / YR
                   for k in ["q32", "q_1e-7", "q_1e-5", "q_1e-3"]])
    beta, lnA = np.polyfit(np.log(qv), np.log(rv), 1)
    out["upper_bound_fit_beta"] = float(beta)
    out["budget_crossover_quantum"] = {}
    for tag, gby in [("4GiB_per_hour", 4 * 2**30), ("20GiB_per_hour", 20 * 2**30)]:
        rate_max = gby / (1e9 * 3600 * 100 * 8)
        qg = float(np.exp((np.log(rate_max) - lnA) / beta))
        lo = np.where(rv <= rate_max)[0]
        hi = lo[0] - 1 if lo.size and lo[0] > 0 else None
        ql = float(np.exp(np.log(qv[hi]) + (np.log(rate_max / rv[hi])) *
                          (np.log(qv[hi + 1] / qv[hi])) / (np.log(rv[hi + 1] / rv[hi]))
                   )) if hi is not None else qg
        out["budget_crossover_quantum"][tag] = {"global_fit": qg, "local_interp": ql}

    # resonant fraction of this belt under a Jupiter analog (P5 bound)
    aJ = 5.2 * AU
    muJ = 9.54e-4
    e_c = 0.21 * muJ**0.2
    a = rng.uniform(2.1, 3.3, 400000) * AU
    e = rng.rayleigh(0.1, 400000)
    frac = 0.0
    for p, qq in [(4, 1), (3, 1), (5, 2), (7, 3), (2, 1)]:
        a_r = aJ * (qq / p)**(2.0 / 3.0)
        halfw = 2.5 * muJ**(2.0 / 3.0) * a_r / 6.0   # conservative per-MMR share
        frac += float(np.mean((np.abs(a - a_r) < halfw) & (e > e_c)))
    out["belt_resonant_chaotic_fraction"] = float(frac)

    print(json.dumps(out, indent=1, default=float))

if __name__ == "__main__":
    main()
