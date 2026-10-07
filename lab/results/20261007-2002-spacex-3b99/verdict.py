#!/usr/bin/env python3
"""Verdict: bits per body at N = 10^9 from the measured walk, and ruin horizons.

The conjunction flux per body is proportional to the local surface density, i.e. to N
at fixed belt width, so the measured per-body walk at N=4000 converts to the game's
belt by scaling kicks-per-orbit by N_game/N_meas. Scar bits per body at time t:
  H2(K/N) + (K/N) * H_fields(spread(t))
The fields' entropy is measured directly (walk spread); here we extrapolate the
measured bits_per_body curves with the log2-diffusion law between checkpoints and
report when 32 bits/body (4 GiB at 10^9 bodies) is crossed.
Also prints the measured values it works from.
"""
import json
import numpy as np

N_GAME = 1e9
N_MEAS = 4000
T_ORB = 2.1 ** 1.5  # years per belt orbit
BUDGET = 32.0       # bits per body (half of 8 GB at 1e9 bodies)


def bits_at(ref_bits_per_body_meas, kicks_meas, kicks_game):
    """Approximate the game-scale bits from the measured walk.

    A random walk's spread scales as sqrt(kicks): the fields' entropy shifts by
    0.5*log2(kicks_game/kicks_meas) per field; membership is exact (frac from the
    measured scarred fraction is a lower bound once the game rate is higher —
    at 10^9 the first-quantum spill happens proportionally earlier; we take frac=1
    for horizons, the optimistic bound).
    """
    shift = 0.5 * np.log2(kicks_game / kicks_meas)
    return ref_bits_per_body_meas + 3 * shift


def main():
    data = json.load(open("hlive_results.json"))
    for seeds in data:
        r0 = seeds[0]
        lam = r0["lam_conj_perbit"] if "lam_conj_perbit" in r0 else r0["lam_conj_per_body_orbit"]
        kicks_per_orbit_meas = lam * r0["n"] / N_MEAS * 0  # per body: lam already per body
        kicks_game = lam * (N_GAME / N_MEAS)
        print(f"\n== {r0['case']}: game kicks/body/orbit = {kicks_game:.4g} "
              f"(per game-second = {kicks_game / T_ORB / AU_SEC:.3g})")
        for q in (2 ** -16, 2 ** -20, 2 ** -24):
            rows = []
            for t in (1, 3, 10, 30, 100, 300):
                m = [s["checkpoints"][str(t)][f"q{q}"]["bits_per_body"] for s in seeds]
                rows.append((t, float(np.median(m))))
            # extrapolate in log-t (diffusion: bits ~ a + 0.5 log2 t)
            ts = np.array([r[0] for r in rows], float)
            bs = np.array([r[1] for r in rows])
            if bs[-1] < bs[0]:
                continue
            # fit slope on the last 3 points
            sl, ic = np.polyfit(np.log2(ts[-3:]), bs[-3:], 1)
            t_ruin = 2 ** ((BUDGET - ic) / sl) if sl > 0 else float("inf")
            # scale to game N: time to ruin shrinks by the rate ratio (walk: bits ~ 0.5 log2(rate*t))
            t_ruin_game = t_ruin * (N_MEAS / N_GAME) if np.isfinite(t_ruin) else float("inf")
            print(f"  q=2^{int(np.log2(q)):+d}: slope={sl:.3f} bits/doubling, "
                  f"bits@300orbits={bs[-1]:.2f}, ruin(meas N)={t_ruin:.3g} orbits, "
                  f"ruin(1e9)={t_ruin_game:.3g} orbits = {t_ruin_game * T_ORB:.3g} yr")


AU_SEC = 3.156e7
if __name__ == "__main__":
    main()
