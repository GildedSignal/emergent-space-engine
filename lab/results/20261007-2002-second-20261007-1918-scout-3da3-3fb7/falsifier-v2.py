#!/usr/bin/env python3
"""falsifier-v2: the scout traffic record, regenerated with the cap explicit.

Second-author run 20261007-2002-second. The checker of 20261007-1918-scout-3da3
found: (a) the code's granularity cap is 1 news per source orbit per consumer
(`min(s2/p_q**2, 1.0)`), not the dossier's stated nu=8, so the headline traffic
is 8x understated under the dossier's own model; (b) at eps=1e-6 the quantum
gate is 100% saturated — the uncapped requirement is ~1.4e12/unit ~= naive
pairwise — so the bound rests entirely on the cap; (c) "~1 event per game-hour
at 100x" is ~1e5x off (actual ~1e-5); (d) "~1e-4 per-body ratio at 1e9" is
actually ~1.5e-5. This script regenerates every number with the cap explicit
and reports both caps, the uncapped requirement, the saturation fraction, and
the eps at which the gate begins to bind. Traffic model identical to the
original (checker reproduced it bit for bit); at nu=1 this reproduces the
published falsifier-out.json values.
"""
import json
import numpy as np

G = v0 = 1.0
R0, R1 = 0.05, 1.0
NSTAR, MSTAR_TOT = 1024, 0.5
MSHIP_TOT = 0.01
NU_KICK = 8.0                   # engine kick cadence per orbit (cost reference)
C_LIGHT = 1000.0
NR = 14
THETA = 0.5
LN_TOTAL = np.log(R1 / R0)
edges = np.geomspace(R0, R1, NR + 1)
r_mid = np.sqrt(edges[:-1] * edges[1:])
wmass = np.diff(np.log(edges)) / LN_TOTAL
UNIT_MYR = 44.0                 # time unit = r_out/v0 ~ 44 Myr
UNIT_S = UNIT_MYR * 3.156e7 * 1e6
PLAYER_HOUR_S = 3600.0 * 100.0  # 1 player hour at 100x real time (sim seconds)


def diffusion(N_ship, r):
    A_star, A_ship = MSTAR_TOT / LN_TOTAL, MSHIP_TOT / LN_TOTAL
    Sig_star, Sig_ship = A_star / (2 * np.pi * r), A_ship / (2 * np.pi * r)
    m_star, m_ship = MSTAR_TOT / NSTAR, MSHIP_TOT / N_ship
    n_star, n_ship = Sig_star / m_star, Sig_ship / m_ship
    acc = 0.0
    for n_j, m_j in ((n_star, m_star), (n_ship, m_ship)):
        b_min = max(2.0 * G * m_j / v0**2, 1e-12)
        b_max = min(r, 1.0 / (2 * np.sqrt(n_j)))
        lnL = max(np.log(max(b_max / b_min, np.e)), 1.0)
        acc += n_j * m_j**2 * lnL
    return 8 * np.pi * r * G**2 * acc, n_star, n_ship, m_star, m_ship


def consumer_traffic(N_ship, eps, cap):
    """cap = max news per source orbit per consumer (None = uncapped requirement)."""
    Dmin = 3.0 * 0.2 * r_mid
    out = []
    for k, r_c in enumerate(r_mid):
        Var_dv, n_star, n_ship, m_star, m_ship = diffusion(N_ship, r_c)
        sig = np.sqrt(Var_dv)
        Ds = np.geomspace(Dmin[k], 2 * R1, 60)
        rate_orbit = 0.0
        sat = []
        for D in Ds:
            area = (THETA * D) ** 2
            n_s_cell = n_ship * area
            n_t_cell = n_star * area
            s2 = n_s_cell * (3 * m_ship * sig) ** 2 + n_t_cell * (3 * m_star * sig) ** 2
            p_q = (eps / r_c) * D**3
            req = s2 / p_q**2
            rate = req if cap is None else min(req, cap)
            step = Ds[1] / Ds[0]
            n_cells = 2 * np.pi * D * (D * (step - 1)) / area
            n_cells = min(n_cells, np.pi * (R1**2) / area)
            rate_orbit += n_cells * rate
            sat.append(req >= cap if cap else False)
        out.append(dict(r=r_c, w=wmass[k], rate_per_orbit=rate_orbit,
                        rate_per_time=rate_orbit / (2 * np.pi * r_c),
                        sat_frac=float(np.mean(sat)) if cap else 1.0))
    return out


def run(N_ship, eps, cap=1.0):
    rows = consumer_traffic(N_ship, eps, cap)
    cells_per_ring = [2 * np.pi * r / (0.2 * r) for r in r_mid]
    total = sum(row["rate_per_time"] * c for row, c in zip(rows, cells_per_ring))
    per_body = total / (N_ship + NSTAR)
    kick_ref = NU_KICK / (2 * np.pi * 0.5)
    window = 2 * R1 / C_LIGHT
    sat = float(np.average([row["sat_frac"] for row in rows],
                           weights=[row["rate_per_time"] for row in rows])) \
        if total > 0 else 0.0
    return dict(N=N_ship, eps=eps, cap=("none" if cap is None else cap),
                total_rate=total, per_body=per_body,
                ratio=per_body / kick_ref, sat_frac=sat,
                mem_sliding_events=total * window,
                naive_pairwise_per_body=(N_ship + NSTAR) * NU_KICK / (2 * np.pi * 0.5),
                events_per_player_hour_100x=total * PLAYER_HOUR_S / UNIT_S)


def main():
    out = {}
    Ns = [10**3, 10**4, 10**5, 10**6]
    # (a) the published record, cap=1 (reproduces falsifier-out.json)
    res1 = [run(N, 1e-6, 1.0) for N in Ns]
    out["C_eps1e-6_cap1"] = res1
    pb = np.array([r["per_body"] for r in res1])
    out["exponent_per_body_vs_N_cap1"] = float(np.polyfit(np.log(Ns), np.log(pb), 1)[0])
    # (b) the dossier's stated cap, nu=8
    out["C_eps1e-6_cap8"] = [run(N, 1e-6, 8.0) for N in Ns]
    # (c) the uncapped requirement at eps=1e-6 (the checker's attack, recomputed)
    out["C_eps1e-6_uncapped"] = [run(N, 1e-6, None) for N in Ns]
    # (d) where the quantum gate binds: saturation vs eps at N=1e6, cap=1
    sweep = [run(10**6, e, 1.0) for e in (1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-8)]
    out["eps_sweep_N1e6_cap1"] = sweep
    bind = [s["eps"] for s in sweep if s["sat_frac"] < 0.5]
    out["gate_binds_below_eps"] = max(bind) if bind else None
    # (e) goal scale, both caps, corrected derived numbers
    for cap, tag in ((1.0, "cap1"), (8.0, "cap8")):
        r6 = run(10**6, 1e-6, cap)
        r9 = run(10**9, 1e-6, cap)
        out[f"N1e6_and_N1e9_{tag}"] = dict(
            N1e6_ratio=r6["ratio"], N1e6_events_per_player_hour=r6["events_per_player_hour_100x"],
            N1e6_mem_events=r6["mem_sliding_events"],
            N1e9_ratio=r9["ratio"],
            N1e9_events_per_player_hour=r9["events_per_player_hour_100x"])
    out["naive_pairwise_N1e6_total_per_unit"] = run(10**6, 1e-6, 1.0)["naive_pairwise_per_body"] * (10**6 + NSTAR)
    out["notes"] = dict(
        unit="r_out/v0 ~ 44 Myr; c=1000 v0",
        cascade_caveat="the original's cascade peak was a histogram over a fixed "
                       "700-sample grid (14 rings x 50 shells), N-independent by "
                       "construction; dropped here as evidence",
        uncapped_meaning="if consumers truly need eps=1e-6 continuously, required "
                         "traffic = uncapped ~= naive pairwise: the wall returns")
    with open("falsifier2-out.json", "w") as f:
        json.dump(out, f, indent=1, default=float)
    slim = {k: v for k, v in out.items() if k != "notes"}
    print(json.dumps(slim, indent=1, default=float))


if __name__ == "__main__":
    main()
