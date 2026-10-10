#!/usr/bin/env python3
"""Runs D1/D1b/D2/E: the accumulator link (principle 6) in the news chain — the
experiment the checker of 20261010-0814-system-fbc6 named between silver and gold.

Scene (real, geometrized G = c = 1, M_sun = 1): the B12 giant of
xtask/src/behave/restricted.rs JUPITER — mu = 1e-3 at sep = 5.27e8, planet radius
4.84e4 — its Hill doll R_sub = sep*(mu/3)^(1/3) = 3.65e7 inside a parent doll
R_p = 10*sep = 5.27e9.

D1 (real scene): 1000 fleet ships news at Poisson rate lam each; each event is a
delta-v. The doll FOLDS member news at its arrival (t_k + r_fold, r_fold = the
member's radius in the doll) into a running moment error; when |E - P| crosses the
parent's coarser quantum Dx, ONE aggregate news event is published to the parent
chain, whose ghosts die at min(r_q_agg, R_p), r_q_agg = sqrt(M_sub/Q_p) with
Q_p = M_sub*Dx/sep^3 (a reader at sep resolves the doll once offset Dx changes its
pull by Q_p; equivalently Dx = sep^3/r_q_agg^2). Plus the doll-less thrusting giant.

D1b (driven): the same scene with big impulses, chosen so the accumulator actually
surfaces and the parent chain is populated by aggregate events it produced.

D2 (scaling): Dx swept over decades, four process/fold laws; measures lam_agg(Dx)
exponents (predicted: coherent/impulse -1, coherent/drift -1/2, signed/impulse -2,
signed/drift -2/3) and lam_agg(t) stationarity — the wall test.

E (the ghost question): sub-quantum readers (r > r_q) either read member tubes
individually (the rule then misses: their dependency window is r, up to R) or the
published aggregate (zero misses, version error < one quantum).

Fold laws: impulse E = sum(delta); drift E(t) = S0*t - S1 (a thrust shifts the
doll's CoM linearly in time). Crossing detection at arrivals; E is linear between
arrivals, so detection is delayed by at most one inter-arrival gap (rates exact).
No dependencies; every metric lands in the run's JSON.
"""
import argparse, bisect, json, math, random

MU = 1e-3                 # giant's mass (solar)
SEP = 5.27e8              # 5.2 AU in gravitational radii
R_PLANET = 4.84e4
R_SUB = SEP * (MU / 3.0) ** (1.0 / 3.0)
R_P = 10.0 * SEP
M_SUB = MU


def poisson_events(rng, rate, t_end):
    ev, t = [], 0.0
    while True:
        t += rng.expovariate(rate)
        if t > t_end:
            return ev
        ev.append(t)


def live_ttl(events, ttl, ck):
    hi = bisect.bisect_right(events, ck)
    if ttl == float("inf"):
        return hi
    return hi - bisect.bisect_right(events, ck - ttl)


def chain_metrics(events, policies, readers, read_cadence, t_end, checkpoints):
    """Live counts per policy at checkpoints + unserved reads (misses) per policy.
    A read at t_j by a resolvable reader at r needs ghosts of events in
    (t_j - r, t_j]; a ghost is dead iff t_event + ttl < t_j."""
    misses = {n: 0 for n in policies}
    reads_needing = 0
    for r, resolvable in readers:
        if not resolvable:
            continue
        t_j = read_cadence
        while t_j <= t_end:
            lo = bisect.bisect_right(events, t_j - r)
            hi = bisect.bisect_right(events, t_j)
            if hi > lo:
                reads_needing += 1
                for name, ttl in policies.items():
                    if ttl == float("inf") or ttl < 0:
                        continue
                    mid = bisect.bisect_right(events, t_j - ttl)
                    if lo < min(mid, hi):
                        misses[name] += 1
            t_j += read_cadence
    rows = []
    for ck in checkpoints:
        row = {"t": ck}
        for name, ttl in policies.items():
            row[name] = live_ttl(events, ttl, ck)
        rows.append(row)
    return {"checkpoints": rows, "misses": misses, "ghost_reads": reads_needing}


def fold_events(rng, n_members, lam, sigma, process, fold, dx, t_end,
                radius_lo, radius_hi, pub_delay, order=1):
    """Member news + the accumulator. Deltas: coherent (+sigma) or signed (+-sigma).
    Impulse fold: E = sum(delta), a step function; publish at the arrival that
    crosses |E - P| >= dx (zeroth-order program; E has no slope to carry).
    Drift fold: E(t) = S0*t - S1 is piecewise linear; the crossing is solved
    EXACTLY between arrivals (possibly several publishes per gap), and the
    published program is order 0 (position) or order 1 (position + velocity,
    a doll's real state)."""
    radii = [rng.uniform(radius_lo, radius_hi) for _ in range(n_members)]
    arrivals = []
    for r in radii:
        for t_k in poisson_events(rng, lam, t_end):
            arrivals.append((t_k + r, t_k))
    arrivals.sort()
    creations = [t for _, t in arrivals]
    agg = []
    S0 = S1 = E = 0.0
    P0 = 0.0        # program position at its publish time t_x
    v0 = 0.0        # program velocity (order 1)
    t_x = 0.0

    def publish(t_pub, value):
        nonlocal P0, v0, t_x
        agg.append(t_pub + pub_delay)
        P0 = value
        v0 = S0 if (fold == "drift" and order == 1) else 0.0
        t_x = t_pub

    for idx, (arrival, t_k) in enumerate(arrivals):
        d = sigma if process == "coherent" else (sigma if rng.random() < 0.5 else -sigma)
        nxt = arrivals[idx + 1][0] if idx + 1 < len(arrivals) else float("inf")
        if fold == "impulse":
            E += d
            if abs(E - P0) >= dx:
                publish(arrival, E)
        else:
            S0 += d
            S1 += d * t_k
            # an arrival jumps e by d*(arrival - t_k); catch a boundary jumped over
            if abs((S0 - v0) * arrival + (-S1 - P0 + v0 * t_x)) >= dx:
                publish(arrival, S0 * arrival - S1)
            # on [arrival, nxt): E(t) = S0*t - S1; error e(t) = (S0-v0)*t + b
            while True:
                m = S0 - v0
                if m == 0:
                    break
                b = -S1 - P0 + v0 * t_x
                t_c = (dx - b) / m if m > 0 else (-dx - b) / m
                if not (arrival <= t_c < min(nxt, t_end)):
                    break
                publish(t_c, S0 * t_c - S1)
    return creations, [a for a, _ in arrivals], agg, radii

def member_chain(creations, arrivals, radii, checkpoints, half_window):
    """Member chain: a ghost dies when the fold consumes it (arrival t_k + r_k).
    live = created but not yet consumed. TTL-style policies starve folds whose
    ghost dies before arrival (r_k > window)."""
    rows = []
    starved_half = 0
    for ck in checkpoints:
        live_exact = bisect.bisect_right(creations, ck) - bisect.bisect_right(arrivals, ck)
        rows.append({"t": ck, "keep_forever": bisect.bisect_right(creations, ck),
                     "death_at_arrival": live_exact,
                     "ttl_Rsub": live_ttl(creations, R_SUB, ck),
                     "ttl_half": live_ttl(creations, half_window, ck)})
    starved_half = sum(1 for a, t in zip(arrivals, creations) if t + half_window < a)
    predicted_flatline = (len(creations) / (creations[-1] if creations else 1.0)) * \
        (sum(radii) / len(radii))
    return {"checkpoints": rows, "starved_folds_half": starved_half,
            "predicted_flatline_little": predicted_flatline}


def run_d1(seed, n_members, lam, sigma, process, rq_grid, t_end, checkpoint,
           lam_giant, driven):
    rng = random.Random(seed)
    readers_spec = sorted(set(SEP * f for f in (0.5, 0.8, 1.0, 1.2, 1.5, 2.0, 4.0, 6.0, 8.0, 9.5)) | {R_SUB * f for f in (0.3, 0.6, 0.95)})
    checkpoints = list(range(int(checkpoint), int(t_end) + 1, int(checkpoint)))
    out = {"driven": driven, "params": {"n_members": n_members, "lam": lam,
           "sigma": sigma, "process": process, "t_end": t_end}, "cells": [], "giant": {}}
    for rq in rq_grid:
        dx = SEP ** 3 / rq ** 2
        creations, arrivals, agg, radii = fold_events(
            rng, n_members, lam, sigma, process, "drift", dx, t_end,
            R_PLANET, R_SUB, R_SUB)
        mean_rfold = sum(radii) / len(radii)
        mem = member_chain(creations, arrivals, radii, checkpoints, R_SUB / 2.0)
        window = min(rq, R_P)
        r_max = max((r for r in readers_spec if r <= rq), default=0.0)
        policies = {"keep_forever": float("inf"), "ttl_R": R_P, "ttl_rule": window,
                    "ttl_half": window / 2.0, "exact": r_max if r_max > 0 else -1.0}
        readers = [(r, r <= rq) for r in readers_spec]
        cm = chain_metrics(agg, policies, readers, t_end / 200.0, t_end, checkpoints)
        out["cells"].append({"rq_agg": rq, "dx": dx, "q_p": M_SUB * dx / SEP ** 3,
                             "n_member_news": len(creations), "n_aggregate": len(agg),
                             "mean_rfold": mean_rfold, "member_chain": mem,
                             "parent_chain": cm,
                             "predicted_parent_flatline": len(agg) / t_end * window})
    giant_news = poisson_events(rng, lam_giant, t_end)
    for rq_g, tag in [(R_P, "rq_eq_Rp"), (R_P / 3.0, "rq_Rp_third")]:
        window = min(rq_g, R_P)
        policies = {"keep_forever": float("inf"), "ttl_R": R_P, "ttl_rule": window,
                    "ttl_half": window / 2.0}
        readers = [(r, r <= rq_g) for r in readers_spec]
        cm = chain_metrics(giant_news, policies, readers, t_end / 200.0, t_end, checkpoints)
        out["giant"][tag] = {"lam": lam_giant, "window": window,
                             "predicted_flatline": lam_giant * window, **cm}
    out["giant"]["news"] = len(giant_news)
    return out
def run_d2(seed, n_members, lam, sigma, dx_grid, t_end_cap, events_cap, only=None):
    rng = random.Random(seed)
    # (process, fold, program order, predicted dx-exponent, sizing)
    #   order 0 drift = the artifact (a position-only program re-published against a
    #   moving source): rate grows with t, exponent -1 in dx at fixed t_end.
    #   order 1 drift = a doll's real state (position + velocity): stationary.
    combos = [("coherent", "impulse", 0, -1.0, "auto"),
              ("signed", "impulse", 0, -2.0, "auto"),
              ("coherent", "drift", 0, -1.0, "fixed"),
              ("signed", "drift", 0, -1.0, "fixed"),
              ("coherent", "drift", 1, -0.5, "auto"),
              ("signed", "drift", 1, -2.0 / 3.0, "auto")]
    if only:
        p, f, o = only.split(",")
        combos = [c for c in combos if c[0] == p and c[1] == f and c[2] == int(o)]
    cells = []
    for process, fold, order, expo, sizing in combos:
        pts = []
        for dx in dx_grid:
            if sizing == "fixed":
                t_end = 3000.0
            else:
                rate0 = n_members * lam * dx ** expo
                t_end = min(t_end_cap, 300.0 / rate0 if rate0 > 0 else t_end_cap,
                            events_cap / (n_members * lam))
            pred = n_members * lam * t_end * dx ** expo
            if sizing == "fixed":
                pred = (n_members * lam * sigma * t_end ** 2 / (4.0 * dx)
                        if process == "coherent" else
                        (2.0 / 3.0) * sigma * math.sqrt(n_members * lam) *
                        t_end ** 1.5 / dx)
            if pred < 8 or n_members * lam * t_end > events_cap:
                pts.append({"dx": dx, "skipped": True,
                            "pred_crossings": round(pred, 1), "t_end": t_end})
                continue
            # zero fold delay for order-1 drift cells isolates the drift scaling
            # from the delay-jump term (d * r_k); the finite-delay case is D1b
            rlo, rhi = (1.0, 1.0) if (fold == "drift" and order == 1) else (1.0, 100.0)
            _, _, agg, _ = fold_events(rng, n_members, lam, sigma, process, fold, dx,
                                       t_end, rlo, rhi, 0.0, order)
            n1 = sum(1 for a in agg if a <= t_end / 2)
            n2 = len(agg) - n1
            z = (n2 - n1) / math.sqrt(n1 + n2) if (n1 + n2) > 0 else 0.0
            pts.append({"dx": dx, "t_end": t_end, "crossings": len(agg),
                        "events": int(n_members * lam * t_end),
                        "lam_agg": len(agg) / t_end,
                        "half1": n1, "half2": n2, "stationarity_z": round(z, 2)})
        ok = [p for p in pts if "lam_agg" in p and p["crossings"] >= 10]
        fit = None
        if len(ok) >= 3:
            xs = [math.log10(p["dx"]) for p in ok]
            ys = [math.log10(p["lam_agg"]) for p in ok]
            n = len(xs)
            sx = sum(xs)
            slope = (n * sum(x * y for x, y in zip(xs, ys)) - sx * sum(ys)) / \
                    (n * sum(x * x for x in xs) - sx * sx)
            fit = {"exponent": round(slope, 3), "predicted": expo, "n_points": n}
        cells.append({"process": process, "fold": fold, "order": order,
                      "points": pts, "fit": fit})
    return cells

def run_e(seed, R, rq, lam, n_readers, read_cadence, t_end, dx_agg):
    rng = random.Random(seed)
    news = poisson_events(rng, lam, t_end)
    radii = sorted(rng.uniform(1.0, R) for _ in range(n_readers))
    r_fold = 0.05 * R
    # ---- tubes mode: every reader extrapolates the source's tube itself
    pol = {"ttl_rule": min(rq, R), "ttl_R": R}
    misses = {n: 0 for n in pol}
    subquantum_misses_rule = 0
    for r in radii:
        t_j = read_cadence
        while t_j <= t_end:
            lo = bisect.bisect_right(news, t_j - r)
            hi = bisect.bisect_right(news, t_j)
            if hi > lo:
                for name, ttl in pol.items():
                    mid = bisect.bisect_right(news, t_j - ttl)
                    if lo < min(mid, hi):
                        misses[name] += 1
                        if name == "ttl_rule" and r > rq:
                            subquantum_misses_rule += 1
            t_j += read_cadence
    # ---- aggregate mode: the fold publishes at crossings (exact, first-order
    # program); sub-quantum readers read the published aggregate.
    arrivals = sorted(t + r_fold for t in news)
    rng2 = random.Random(seed + 1)
    deltas = [1.0 if rng2.random() < 0.5 else -1.0 for _ in arrivals]
    agg, P_hist, prefix = [], [], []
    s0 = s1 = 0.0
    P0 = v0 = t_x = 0.0
    for idx, (arrival, t_k) in enumerate(zip(arrivals, news)):
        d = deltas[idx]
        nxt = arrivals[idx + 1] if idx + 1 < len(arrivals) else float("inf")
        s0 += d
        s1 += d * t_k
        prefix.append((s0, s1))
        # an arrival jumps e by d*(arrival - t_k); catch a boundary jumped over
        if abs((s0 - v0) * arrival + (-s1 - P0 + v0 * t_x)) >= dx_agg:
            P0 = s0 * arrival - s1
            v0 = s0
            t_x = arrival
            agg.append(arrival)
            P_hist.append((t_x, P0, v0))
        while True:
            m = s0 - v0
            if m == 0:
                break
            b = -s1 - P0 + v0 * t_x
            t_c = (dx_agg - b) / m if m > 0 else (-dx_agg - b) / m
            if not (arrival <= t_c < nxt):
                break
            P0 = s0 * t_c - s1
            v0 = s0
            t_x = t_c
            agg.append(t_c)
            P_hist.append((t_x, P0, v0))

    def E_at(t):
        j = bisect.bisect_right(arrivals, t) - 1
        if j < 0:
            return 0.0
        s0j, s1j = prefix[j]
        return s0j * t - s1j

    agg_misses = agg_misses_half = agg_reads = err_violations = 0
    max_err = 0.0
    for r in radii:
        if r <= rq:
            continue  # resolvable readers stay on the member chain (run A's case)
        t_j = read_cadence
        while t_j <= t_end:
            t_ret = t_j - r
            # the reader reconstructs the aggregate as its cone saw it at t_ret: it
            # needs the ghost (pre-version) of every aggregate event in (t_ret, t_j];
            # a ghost dies at t_x + window.
            lo = bisect.bisect_right(agg, t_ret)
            hi = bisect.bisect_right(agg, t_j)
            if hi > lo:
                agg_reads += 1
                for x in agg[lo:hi]:
                    if x + R < t_j:
                        agg_misses += 1
                    if x + R / 2.0 < t_j:
                        agg_misses_half += 1
            i = bisect.bisect_right(agg, t_ret)
            if i > 0:
                t_v, P0_v, v0_v = P_hist[i - 1]
                err = abs(E_at(t_ret) - (P0_v + v0_v * (t_ret - t_v)))
                max_err = max(max_err, err)
                if err >= dx_agg * (1 + 1e-9):
                    err_violations += 1
            t_j += read_cadence
    return {"R": R, "rq": rq, "lam": lam, "n_news": len(news), "dx_agg": dx_agg,
            "n_subquantum_readers": sum(1 for r in radii if r > rq),
            "tubes_misses": misses,
            "subquantum_missed_at_rule": subquantum_misses_rule,
            "aggregate": {"n_publishes": len(agg), "window": R,
                          "reads_needing_ghosts": agg_reads, "misses": agg_misses,
                          "misses_half_window": agg_misses_half,
                          "max_version_error": max_err,
                          "quantum_violations": err_violations,
                          "live_at_end": live_ttl(agg, R, t_end),
                          "predicted_live": len(agg) / t_end * R}}

def fold_equivalence(seed, n_events):
    """Integer fold vs recompute-from-log in reverse arrival order: bit-identical."""
    rng = random.Random(seed)
    t, log = 0, []
    for _ in range(n_events):
        t += rng.randrange(1, 100)
        log.append((t, rng.choice([-3, -2, -1, 1, 2, 3])))
    S0 = S1 = 0
    for tk, d in log:
        S0 += d
        S1 += d * tk
    R0 = R1 = 0
    for tk, d in reversed(log):
        R0 += d
        R1 += d * tk
    return {"fold_S0_S1": [S0, S1], "recompute_S0_S1": [R0, R1],
            "bit_identical": (S0, S1) == (R0, R1)}


def main():
    import sys
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["d1", "d1b", "d2", "e", "equiv"])
    ap.add_argument("--json", default=None)
    ap.add_argument("--only", default=None,
                    help="d2: run one combo 'process,fold,order' in this process")
    a = ap.parse_args()
    if a.cmd == "d1":
        res = run_d1(seed=7, n_members=1000, lam=1e-7, sigma=3.3e-5, process="signed",
                     rq_grid=[R_SUB, SEP, R_P], t_end=2.5 * R_P,
                     checkpoint=0.25 * R_P, lam_giant=1e-8, driven=False)
    elif a.cmd == "d1b":
        res = run_d1(seed=17, n_members=1000, lam=3.3e-7, sigma=1e4, process="signed",
                     rq_grid=[R_SUB], t_end=10.0 * R_SUB,
                     checkpoint=1.0 * R_SUB, lam_giant=1e-8, driven=True)
    elif a.cmd == "d2":
        res = run_d2(seed=11, n_members=1000, lam=1e-3, sigma=1.0,
                     dx_grid=[10, 30, 100, 300, 1e3, 3e3, 1e4, 3e4, 1e5],
                     t_end_cap=1e7, events_cap=3e6, only=a.only)
    elif a.cmd == "e":
        res = run_e(seed=3, R=1000.0, rq=100.0, lam=0.05, n_readers=400,
                    read_cadence=8.0, t_end=4000.0, dx_agg=200.0)
    else:
        res = fold_equivalence(seed=5, n_events=100000)
    if a.json:
        mode = "w" if not a.only else "w"
        json.dump(res, open(a.json, "w"), indent=1)
    print("wrote", a.json, "ok" if a.json else "")


if __name__ == "__main__":
    main()
