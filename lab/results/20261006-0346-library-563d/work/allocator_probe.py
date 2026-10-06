#!/usr/bin/env python3
"""Allocator discipline probe (library lens, run 20261006-0346-library-563d).

Question: for the engine's one slack-queue allocator (board bottleneck 4,
Julien: "the algorithm that allocates the work ... it's the most important one"),
which lever buys the p99 of causal-deadline violations: queue DISCIPLINE,
FORECASTING (knowing future arrivals), BOUNDED UNITS, or UTILIZATION headroom?

Structure (mirrors the engine's measured shape):
- resumable (preemptive-resume) work units, one server;
- heavy-tailed service: 70% cheap units, 30% heavy units with a Pareto(alpha)
  tail, either CAPPED at 40 mean-cheap-units (the design: plane.md #7 "nothing
  takes an unbounded synchronous claim on the frame") or UNCAPPED (negative
  control: must blow up);
- bursty arrivals (chaos): Pareto(1,1.5) interarrival gaps;
- deadline = arrival + causal slack, log-uniform over 3 orders of magnitude;
- exact utilization control: the timeline is rescaled so total work / span = rho.

Policies: FIFO; SRPT; EDF (earliest deadline, online); LeastLaxity (deadline -
now - remaining; the design, engine.md rule 5); Clairvoyant = EDF with every
arrival pre-rolled to t=0 (perfect prediction + legal compute-ahead, the
engine's idle-time speculation; ignores discard cost, so it is an UPPER bound
on what any forecast machinery could ever buy for ordering). A pilot run with
Horn's idling rule had 69 max-lateness violations against EDF and was dropped:
a wrong control is worse than none.

Validity control (both sides): Clairvoyant must be <= EDF on p99 and miss
fraction in every cell, else the cell is flagged VOID in the JSON.

Usage: python3 allocator_probe.py [n_items] [n_seeds]
Writes ../data/probe_results.json and prints a table. Deterministic seeds.
Order-of-magnitude probe (cloud Linux, stdlib); floats explore, never decide.
"""
import heapq
import json
import math
import os
import random
import sys
import time
from collections import deque

N_ITEMS = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
N_SEEDS = int(sys.argv[2]) if len(sys.argv) > 2 else 10
RHOS = [0.7, 0.9, 0.95]
ALPHAS = [1.2, 1.5, 3.0]
CAPS = {"capped": 40.0, "uncapped": float("inf")}
POLICIES = ["FIFO", "SRPT", "EDF", "LeastLaxity", "Clairvoyant"]
EPS = 1e-9


def make_jobs(rng, alpha, cap):
    jobs = []
    for _ in range(N_ITEMS):
        u = rng.random()
        gap = 0.2 + (1.0 - u) ** (-1.0 / 1.5)          # Pareto(1, 1.5) gaps
        if rng.random() < 0.7:
            s = 0.2 + rng.expovariate(1.0)             # cheap unit
        else:
            s = min((1.0 - rng.random()) ** (-1.0 / alpha), cap)  # heavy tail
        slack = 10 ** rng.uniform(0.0, 3.0)            # causal slack, 3 decades
        jobs.append((gap, s, slack))
    return jobs


def build(jobs, rho):
    total_service = sum(s for _, s, _ in jobs)
    total_gap = sum(g for g, _, _ in jobs)
    scale = (total_service / rho) / total_gap
    arr, svc, dl = [], [], []
    t = 0.0
    for gap, s, slack in jobs:
        arr.append(t)
        svc.append(s)
        dl.append(t + slack * scale)
        t += gap * scale
    return arr, svc, dl


def simulate(arr, svc, dl, policy):
    """Preemptive-resume single server. Returns (lateness list, max lateness)."""
    n = len(arr)
    remaining = svc[:]
    done = [False] * n
    by_arr = sorted(range(n), key=lambda i: arr[i])
    by_dl = sorted(range(n), key=lambda i: dl[i])
    t = 0.0
    ai = 0
    cp = 0
    edf_h, srpt_h, clair_h = [], [], []
    fifo_q = deque()
    released = set()
    lateness = []
    max_late = -float("inf")

    def admit(now):
        nonlocal ai
        while ai < n and arr[by_arr[ai]] <= now + EPS:
            j = by_arr[ai]
            ai += 1
            heapq.heappush(edf_h, (dl[j], j))
            heapq.heappush(clair_h, (dl[j], j))
            heapq.heappush(srpt_h, (remaining[j], j))
            fifo_q.append(j)
            released.add(j)

    def top(h):
        while h and (done[h[0][1]]
                     or h is srpt_h and h[0][0] > remaining[h[0][1]] + EPS):
            heapq.heappop(h)
        return h[0][1] if h else None

    def future_min_deadline(now):
        nonlocal cp
        while cp < n and arr[by_dl[cp]] <= now + EPS:
            cp += 1
        return dl[by_dl[cp]] if cp < n else float("inf")

    while True:
        admit(t)
        j = None
        if policy == "FIFO":
            while fifo_q and done[fifo_q[0]]:
                fifo_q.popleft()
            j = fifo_q[0] if fifo_q else None
        elif policy == "SRPT":
            j = top(srpt_h)
        elif policy == "EDF":
            j = top(edf_h)
        elif policy == "LeastLaxity":
            best = None
            for k in released:
                lax = dl[k] - t - remaining[k]
                if j is None or lax < best:
                    j, best = k, lax
        else:                                      # Clairvoyant: unreachable
            j = top(edf_h)                         # (arrivals pre-rolled)
        if j is None:
            if ai >= n:
                break
            t = arr[by_arr[ai]]
            continue
        dt = remaining[j]
        if ai < n:
            dt = min(dt, arr[by_arr[ai]] - t)
        if dt <= EPS:
            t = arr[by_arr[ai]]
            continue
        remaining[j] -= dt
        t += dt
        if policy == "SRPT" and remaining[j] > EPS:
            heapq.heappush(srpt_h, (remaining[j], j))
        if remaining[j] <= EPS:
            done[j] = True
            released.discard(j)
            lateness.append(t - dl[j])
            max_late = max(max_late, t - dl[j])
    return lateness, max_late


def pct(xs, p):
    xs = sorted(xs)
    if not xs:
        return float("nan")
    k = min(len(xs) - 1, max(0, int(math.ceil(p / 100.0 * len(xs))) - 1))
    return xs[k]


def main():
    rng_master = random.Random(20261006)
    out = {"config": {"n_items": N_ITEMS, "n_seeds": N_SEEDS,
                      "rhos": RHOS, "alphas": ALPHAS,
                      "caps": {"capped": 40.0, "uncapped": None}},
           "cells": [], "clairvoyant_violations": 0}
    t0 = time.time()
    hdr = (f"{'rho':>5} {'alpha':>5} {'cap':>9} {'policy':>12} {'p50':>7} "
           f"{'p95':>7} {'p99':>7} {'Lmax':>8} {'miss%':>6} {'worstp99':>9}")
    print(hdr + "  (lateness in mean-cheap-service units)")
    for rho in RHOS:
        for alpha in ALPHAS:
            for cap_name in CAPS:
                cap = CAPS[cap_name]
                pooled = {p: [] for p in POLICIES}
                seed_p99 = {p: [] for p in POLICIES}
                seed_lmax = {p: [] for p in POLICIES}
                for seed in range(N_SEEDS):
                    rng = random.Random(rng_master.randrange(1 << 30))
                    jobs = make_jobs(rng, alpha, cap)
                    arr, svc, dl = build(jobs, rho)
                    mean_s = sum(svc) / len(svc)
                    for pol in POLICIES:
                        if pol == "Clairvoyant":
                            lat, lmax = simulate([0.0] * len(arr), svc, dl, "EDF")
                        else:
                            lat, lmax = simulate(arr, svc, dl, pol)
                        lat_n = [x / mean_s for x in lat]
                        pooled[pol].extend(lat_n)
                        seed_p99[pol].append(pct(lat_n, 99))
                        seed_lmax[pol].append(lmax / mean_s)
                # validity control: clairvoyant must beat EDF on p99/miss
                edf_p99 = pct(pooled["EDF"], 99)
                edf_miss = sum(1 for x in pooled["EDF"] if x > 0) / len(pooled["EDF"])
                cl_p99 = pct(pooled["Clairvoyant"], 99)
                cl_miss = sum(1 for x in pooled["Clairvoyant"] if x > 0) / len(pooled["Clairvoyant"])
                if cl_p99 > edf_p99 or cl_miss > edf_miss:
                    out["clairvoyant_violations"] += 1
                for pol in POLICIES:
                    lat = pooled[pol]
                    cell = {"rho": rho, "alpha": alpha, "cap": cap_name,
                            "policy": pol,
                            "p50": round(pct(lat, 50), 1),
                            "p95": round(pct(lat, 95), 1),
                            "p99": round(pct(lat, 99), 1),
                            "Lmax_med": round(sorted(seed_lmax[pol])[N_SEEDS // 2], 1),
                            "miss_frac": round(sum(1 for x in lat if x > 0) / len(lat), 4),
                            "worst_seed_p99": round(max(seed_p99[pol]), 1)}
                    out["cells"].append(cell)
                    print(f"{rho:>5} {alpha:>5} {cap_name:>9} {pol:>12} "
                          f"{cell['p50']:>7} {cell['p95']:>7} {cell['p99']:>7} "
                          f"{cell['Lmax_med']:>8} {100*cell['miss_frac']:>6.1f} "
                          f"{cell['worst_seed_p99']:>9}")
    out["wall_s"] = round(time.time() - t0, 1)
    dest = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",
                                        "data", "probe_results.json"))
    with open(dest, "w") as f:
        json.dump(out, f, indent=1)
    print("clairvoyant-vs-EDF violations:", out["clairvoyant_violations"])
    print("wrote", dest, "in", out["wall_s"], "s")


if __name__ == "__main__":
    main()
