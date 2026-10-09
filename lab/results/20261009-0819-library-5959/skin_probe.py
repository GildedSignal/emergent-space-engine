#!/usr/bin/env python3
"""Skin-tier work-rate probe v2 (library lens, run 20261009-0819-library-5959).

v2 fixes vs v1 (disclosed in dossier.md): belt width now 1000 R (encounters rare),
window size saturates at N-1, and a composite policy is added. v1 output is kept
as skin-probe-out-v1-disclosed.txt.

Toy model of the encounter candidate tier with a slack skin:
- N bodies on a uniform belt of width W in a-space, spacing delta = W/N;
  candidate window = 2*(R+s) capped at N-1 pairs; R = encounter miss radius.
- Per body i, drift d_i (miss-distance units per orbit) accumulates; when it
  crosses the body's skin s_i the window is rebuilt (k(s_i) pair-evals) and the
  drift resets. Drift rate per orbit caps at 1 (discrete orbits).
- Stored pairs pay one clock-compare per orbit (c_keep); one pair-eval = 1.
- Policies: global s (swept); per-body sqrt law s_i = sqrt(R d_i / c_keep);
  composite: s_i = 0 (rebuild every orbit, element-sort behaviour for that body)
  when d_i >= R, else the sqrt law. Counters are integers; seed fixed.
Usage: python3 skin_probe.py
"""
import numpy as np

R = 1.0
BELT_W = 1000.0 * R
N = 20_000
ORBITS = 20
C_EVAL, C_KEEP = 1.0, 0.01
SEED = 20261009
DELTA = BELT_W / N


def draw_drift(case, rng):
    sigma = np.log(10) / 2.3263            # p99/median = 10
    d = np.exp(rng.normal(0.0, sigma, N))
    if case == "quiet":
        d = 0.02 * R * d                   # median 0.02 R
    elif case == "kicked":
        d = 0.10 * R * d
    elif case == "formation":
        d = 0.02 * R * d
        hot = rng.random(N) < 0.05         # 5% co-orbital concentrated tail
        d[hot] *= 100.0                    # median 2 R for hot bodies
    else:
        raise ValueError(case)
    return d


def k_of(s):
    return np.minimum(np.floor(2.0 * (R + s) / DELTA).astype(np.int64), N - 1) + 1


def run(d, s_policy):
    """s_policy: array of per-body skins. Returns work/orbit/body, evals, p99 body."""
    k = k_of(s_policy)
    drift = np.zeros(N)
    evals = np.zeros(N, dtype=np.int64)
    for _ in range(ORBITS):
        drift += d
        rebuild = drift > s_policy
        evals[rebuild] += k[rebuild]
        drift[rebuild] = 0.0
    work = C_EVAL * evals + C_KEEP * k * ORBITS
    return work.sum() / N / ORBITS, evals.sum() / ORBITS, float(np.percentile(work / ORBITS, 99))


def main():
    grid = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0]
    print(f"{'case':10s} {'s/R':>6s} {'work/orbit':>12s} {'evals/orbit':>12s} {'p99body':>10s}")
    for case in ["quiet", "kicked", "formation"]:
        rng = np.random.default_rng(SEED)
        d = draw_drift(case, rng)
        d_med = float(np.median(d))
        s_pred = np.sqrt(R * d_med / C_KEEP)
        rows = []
        for s in grid:
            w, ev, p99 = run(d, np.full(N, s))
            rows.append((s, w, ev, p99))
            print(f"{case:10s} {s:6.2f} {w:12.2f} {ev:12.1f} {p99:10.2f}")
        wmin = min(r[1] for r in rows)
        sbest = min(rows, key=lambda r: r[1])[0]
        print(f"  global: argmin s/R={sbest:.2f} work={wmin:.2f}; sqrt-law(median) s/R={s_pred:.2f};"
              f" thin x{rows[0][1]/wmin:.1f}, fat x{rows[-1][1]/wmin:.1f}")
        w_sqrt, _, p99_sqrt = run(d, np.sqrt(R * d / C_KEEP))
        comp = np.where(d >= R, 0.0, np.sqrt(R * d / C_KEEP))
        w_comp, _, p99_comp = run(d, comp)
        frac = float((d >= R).mean())
        print(f"  per-body sqrt law: work={w_sqrt:.2f} (x{wmin/w_sqrt:.2f} vs best global),"
              f" p99 body={p99_sqrt:.2f}")
        print(f"  composite (s=0 if d>=R, {frac:.1%} of bodies): work={w_comp:.2f}"
              f" (x{wmin/w_comp:.2f} vs best global, x{w_sqrt/w_comp:.2f} vs sqrt law),"
              f" p99 body={p99_comp:.2f}")
        print()


if __name__ == "__main__":
    main()
