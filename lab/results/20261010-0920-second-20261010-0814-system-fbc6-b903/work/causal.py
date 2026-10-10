#!/usr/bin/env python3
"""Causal-memory toy: does the news chain (ghosts) grow without bound?

One doll, radius R, c = 1 (distance unit per tick). A central source of mass m
emits news events (thrust/contact/rebind) at Poisson rate lambda. A reader at
radius r resolves the source individually only where the pull G*m/r^2 exceeds
one kick quantum Q  =>  r_q = sqrt(G*m/Q).

A read (kick) by reader i at time t_j extrapolates the source from its past-cone
crossing (t_j - r/c) to now: it needs the ghost (pre-news tube) of every news
event k with t_k in (t_j - r, t_j]. So ghost k is needed by reader i during
[t_k, t_k + r]. Its exact min-plus death is t_k + max{r_i : r_i resolvable}.

Policies: KEEP-FOREVER, TTL=R/c, TTL=min(r_q,R)/c, TTL=half, EXACT.
Metrics: live records at checkpoints, unserved reads (misses), totals.
"""
import argparse, bisect, json, math, random
from collections import defaultdict


def poisson_events(rng, rate, t_end):
    ev, t = [], 0.0
    while True:
        t += rng.expovariate(rate)
        if t > t_end:
            return ev
        ev.append(t)


def run_a(seed, R, lam, rq, n_readers, delta, t_end, checkpoint):
    rng = random.Random(seed)
    news = poisson_events(rng, lam, t_end)  # sorted by construction
    radii = sorted(rng.uniform(1.0, R) for _ in range(n_readers))
    resolvable = [r for r in radii if r <= rq]
    r_max = max(resolvable) if resolvable else 0.0
    window = min(rq, R) if resolvable else -1.0
    policies = {
        "keep_forever": float("inf"),
        "ttl_R": float(R),
        "ttl_rq": window,
        "ttl_half": window / 2.0 if window > 0 else -1.0,
        "exact": r_max if r_max > 0 else -1.0,
    }
    misses = defaultdict(int)
    reads_needing = 0
    for r in resolvable:
        t_j = delta
        while t_j <= t_end:
            lo = bisect.bisect_right(news, t_j - r)
            hi = bisect.bisect_right(news, t_j)
            if hi > lo:
                reads_needing += 1
                for name, ttl in policies.items():
                    if ttl < 0 or ttl == float("inf"):
                        continue
                    # a needed ghost is dead iff some news in window has t + ttl < t_j
                    mid = bisect.bisect_right(news, t_j - ttl)
                    if lo < min(mid, hi):
                        misses[name] += 1
            t_j += delta
    checkpoints = []
    for ck in range(checkpoint, t_end + 1, checkpoint):
        row = {"t": ck}
        hi = bisect.bisect_right(news, ck)
        for name, ttl in policies.items():
            if ttl == float("inf"):
                row[name] = hi
            elif ttl < 0:
                row[name] = 0
            else:
                lo = bisect.bisect_right(news, ck - ttl)
                row[name] = hi - lo
        checkpoints.append(row)
    return {"seed": seed, "R": R, "lambda": lam, "rq": rq, "n_news": len(news),
            "r_max_resolvable": round(r_max, 2),
            "readers_resolvable": len(resolvable),
            "flatline_predicted_lam_window": round(lam * max(window, 0.0), 3),
            "checkpoints": checkpoints, "misses": dict(misses),
            "ghost_reads": reads_needing}


def run_b(t_end, d_act, v, half_grid):
    """Frontier vs volume: a player moving at v (cells/tick, c=1) acts every
    d_act ticks at its current cell. A cell is causally touched at the min-plus
    arrival min_k (t_k + |x-x_k| + |y-y_k|) (diamond cone, integer L1).
    Per frame: DEDUP work = cells whose earliest arrival falls in the frame
    (the min-plus envelope); NAIVE work = sum over actions of the cells that
    action's own front newly reaches this frame (no dedup, double-counts)."""
    frames = []
    seen = set()
    actions = []
    for t in range(d_act, t_end + 1, d_act):
        actions.append((t, (t // d_act) * d_act * v))  # (time, x position), y=0
    for t in range(d_act, t_end + 1, d_act):
        newly = []
        for x in range(-half_grid, half_grid):
            for y in range(-half_grid, half_grid):
                best = None
                for (tk, xk) in actions:
                    arr = tk + abs(x - xk) + abs(y)
                    if arr <= t and (best is None or arr < best):
                        best = arr
                if best is not None and t - d_act < best <= t and (x, y) not in seen:
                    newly.append((x, y))
        naive = 0
        for (tk, xk) in actions:
            for x in range(-half_grid, half_grid):
                for y in range(-half_grid, half_grid):
                    arr = tk + abs(x - xk) + abs(y)
                    if t - d_act < arr <= t:
                        naive += 1
        seen.update(newly)
        frames.append({"t": t, "frontier_dedup_cells": len(newly),
                       "naive_ring_sum_cells": naive, "touched_total": len(seen)})
    return frames


def run_c(seed, R, r_sub, lam, t_end, member_rq, checkpoint):
    """Hierarchy/shadow: members in sub-dolls of radius r_sub inside a parent
    doll of radius R. A member's news enters the parent chain only if a
    parent-level reader (radii in [r_sub, R]) can resolve it: r_q > r_sub."""
    rng = random.Random(seed)
    per_member = []
    for rq in member_rq:
        news = poisson_events(rng, lam, t_end)
        enters = rq > r_sub
        window = min(rq, R) if enters else min(rq, r_sub)
        per_member.append({"rq": rq, "enters_parent": enters, "window": window,
                           "news": news})
    rows = []
    for ck in range(checkpoint, t_end + 1, checkpoint):
        parent_live = sub_live = 0
        for pm in per_member:
            hi = bisect.bisect_right(pm["news"], ck)
            lo = bisect.bisect_right(pm["news"], ck - pm["window"])
            live = hi - lo
            if pm["enters_parent"]:
                parent_live += live
            else:
                sub_live += live
        rows.append({"t": ck, "parent_chain_live": parent_live, "sub_chain_live": sub_live})
    return {"members": [{k: v for k, v in pm.items() if k != "news"} for pm in per_member],
            "checkpoints": rows,
            "predicted_parent_flatline": round(sum(lam * min(rq, R) for rq in member_rq if rq > r_sub), 2),
            "predicted_sub_flatline": round(sum(lam * min(rq, r_sub) for rq in member_rq if rq <= r_sub), 2)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["a", "b", "c"])
    ap.add_argument("--json", default="")
    a = ap.parse_args()
    if a.cmd == "a":
        results = [run_a(seed, R=1000.0, lam=lam, rq=rq, n_readers=2000, delta=8.0,
                         t_end=4000, checkpoint=500)
                   for lam in (0.01, 0.05, 0.2) for rq in (10.0, 100.0, 1000.0, 5000.0)
                   for seed in (1, 2, 3)]
        path = a.json or "run_a.json"
    elif a.cmd == "b":
        frames = run_b(t_end=80, d_act=10, v=0.5, half_grid=100)
        path = a.json or "run_b.json"
        results = frames
    else:
        results = run_c(seed=7, R=1000.0, r_sub=50.0, lam=0.05, t_end=4000,
                        member_rq=[8.0, 20.0, 40.0, 60.0, 200.0, 900.0, 3000.0],
                        checkpoint=500)
        path = a.json or "run_c.json"
    with open(path, "w") as f:
        json.dump(results, f, indent=1)
    print("wrote", path, len(results), "records")


if __name__ == "__main__":
    main()
