#!/usr/bin/env python3
"""Stream statistics of exact encounter events (lab run 20261008-0148-dynamics-0a3d).

Input: belt_*.tsv from examples/stream (header lines '# body i a e', '# events N',
rows 'i j t d'). Outputs per-belt metrics + Poisson controls.
"""
import glob
import json
import sys

import numpy as np

TAU = 2 * np.pi


def load(path):
    bodies = {}
    ev = []
    with open(path) as f:
        for line in f:
            if line.startswith("# body"):
                _, _, i, a, e = line.split()
                bodies[int(i)] = (float(a), float(e))
            elif line.startswith("# events"):
                continue
            elif line.strip():
                i, j, t, d = line.split()
                ev.append((float(t), int(i), int(j), float(d)))
    ev.sort()
    return bodies, np.array([e[0] for e in ev]), ev


def window_stats(t, t_end, w, n_boot=120, rng=None):
    """Fano factor of counts in windows of width w; Poisson control by resampling."""
    rng = rng or np.random.default_rng(7)
    n_win = int(t_end / w)
    if n_win < 8:
        return None
    counts, _ = np.histogram(t, bins=np.linspace(0, t_end, n_win + 1))
    mean = counts.mean()
    fano = counts.var(ddof=1) / mean if mean > 0 else float("nan")
    # Poisson control: same number of events, uniform times
    fanos = []
    p99s = []
    for _ in range(n_boot):
        c, _ = np.histogram(rng.uniform(0, t_end, size=len(t)), bins=np.linspace(0, t_end, n_win + 1))
        fanos.append(c.var(ddof=1) / c.mean())
        p99s.append(np.quantile(c, 0.99))
    return dict(
        w=w, n_win=n_win, mean=mean, fano=fano,
        poisson_fano_mean=float(np.mean(fanos)),
        poisson_fano_p99=float(np.quantile(fanos, 0.99)),
        p99=float(np.quantile(counts, 0.99)),
        poisson_p99_of_counts=float(np.mean(p99s)),
    )


def analyze(path):
    bodies, t, ev = load(path)
    t_end = t[-1] * 1.0 if len(t) else 0.0
    t_orbits = t_end / TAU
    n_bodies = len(bodies)
    out = {"file": path.split("/")[-1], "events": len(t), "bodies": n_bodies,
           "orbits": t_orbits, "lambda_per_body_orbit": len(t) / n_bodies / t_orbits}
    # per-pair trains
    from collections import Counter
    per_pair = Counter((i, j) for _, i, j, _ in ev)
    counts = np.array(list(per_pair.values()))
    out["pairs_with_events"] = len(counts)
    out["pairs_ge2"] = int((counts >= 2).sum())
    out["frac_events_from_repeat_pairs"] = float(counts[counts >= 2].sum() / counts.sum())
    out["events_per_pair_median"] = float(np.median(counts))
    out["events_per_pair_max"] = int(counts.max())
    # median synodic period of encountering pairs, and gap/T_syn for trains
    tsyn_med = []
    gap_ratio = []
    by_pair = {}
    for tt, i, j, _ in ev:
        by_pair.setdefault((i, j), []).append(tt)
    for (i, j), ts in by_pair.items():
        ai, _ = bodies[i]
        aj, _ = bodies[j]
        dn = abs(ai ** -1.5 - aj ** -1.5)
        tsyn = TAU / dn if dn > 0 else np.inf  # equal integer periods: frozen synodic phase
        if np.isfinite(tsyn):
            tsyn_med.append(tsyn)
        if len(ts) >= 3 and np.isfinite(tsyn):
            gaps = np.diff(ts)
            gap_ratio.append(np.median(gaps) / tsyn)
    out["tsyn_med_orbits"] = float(np.median(tsyn_med) / TAU) if tsyn_med else None
    out["gap_over_tsyn_median"] = float(np.median(gap_ratio)) if gap_ratio else None
    # inter-arrival CV (aggregate stream)
    if len(t) > 10:
        ia = np.diff(t)
        cv = ia.std(ddof=1) / ia.mean()
        out["interarrival_cv"] = float(cv)
        out["burstiness"] = float((cv - 1) / (cv + 1))
    # windows in orbits
    rng = np.random.default_rng(11)
    ws = []
    for w_orb in (0.5, 1, 2, 5, 10, 20, 50):
        r = window_stats(t, t_end, w_orb * TAU, rng=rng)
        if r:
            r["w_orbits"] = w_orb
            ws.append(r)
    out["windows"] = ws
    # count autocorrelation at 1-orbit windows
    for w_orb in (1.0,):
        n_win = int(t_orbits / w_orb)
        if n_win >= 20:
            counts, _ = np.histogram(t, bins=np.linspace(0, t_end, n_win + 1))
            c = counts - counts.mean()
            ac1 = float((c[:-1] * c[1:]).sum() / (c * c).sum())
            out[f"ac1_{w_orb}orb"] = ac1
    return out


if __name__ == "__main__":
    results = [analyze(p) for p in sorted(sys.argv[1:])]
    for r in results:
        print("=" * 72)
        print(f"{r['file']}: {r['events']} events, {r['bodies']} bodies, {r['orbits']:.0f} orbits, "
              f"lambda={r['lambda_per_body_orbit']:.4f}/body/orbit")
        print(f"  pairs w/ events {r['pairs_with_events']}, >=2: {r['pairs_ge2']} "
              f"({100*r['frac_events_from_repeat_pairs']:.1f}% of events from repeat pairs), "
              f"median {r['events_per_pair_median']:.0f}, max {r['events_per_pair_max']}")
        print(f"  median T_syn of encountering pairs: {r['tsyn_med_orbits']} orbits; "
              f"per-pair gap/T_syn median: {r['gap_over_tsyn_median']}")
        print(f"  interarrival CV {r.get('interarrival_cv'):.3f}, burstiness {r.get('burstiness'):.3f}, "
              f"ac1(1 orb) {r.get('ac1_1.0orb')}")
        print("  w_orb  fano   poisson_fano(mean,p99)   p99    poisson_p99")
        for w in r["windows"]:
            print(f"  {w['w_orbits']:5.1f}  {w['fano']:6.2f}   ({w['poisson_fano_mean']:.2f}, {w['poisson_fano_p99']:.2f})"
                  f"        {w['p99']:6.0f}   {w['poisson_p99_of_counts']:6.1f}")
    json.dump(results, open("stream_stats.json", "w"), indent=1)
