#!/usr/bin/env python3
"""Probe B — the frame budget's p99 as an integer (max,+) window certificate.

Model: T frames, C workers of capacity 1 integer unit/frame, every unit has
deadline (arrival frame + D). Arrivals: deterministic base + heavy-tailed
bursts (Pareto tail index alpha; a burst is ONE event, not many — battles are
single causes). All arithmetic integer.

Certificates (exact, one pass, prefix sums):
  W* = max over windows [u,v] of (sum arrivals - C*(v-u+1))   # max backlog any
       work-conserving schedule must reach; Lindley/EDF identity
  M  = W* - C*D > 0  <=>  some deadline must be missed (single-queue EDF
       criterion, exact when all relative deadlines are equal)

Policies:
  (a) single work-conserving queue (EDF == FIFO here)
  (b) 8 round-robin shards, capacity 1 each, no migration
  (c) 8 shards + stealing with a 1-frame transfer delay

Predictions B1-B5 in predictions.md.

Run: python3 probeB_maxplus.py [--seed 7]   (< 60 s, < 200 MB)
"""
import json, sys
from collections import deque
import numpy as np

SEED = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 7
T = 50000
C = 8
D = 2


def arrivals(rng, alpha, util_target):
    base = 5
    lam = 0.03
    # mean burst size s*alpha/(alpha-1) ; target mean total = util_target*C
    mean_burst = (util_target * C - base) / lam
    s = mean_burst * (alpha - 1) / alpha
    nb = rng.poisson(lam, T)
    A = np.full(T, base, dtype=np.int64)
    nz = nb > 0
    idx = np.nonzero(nz)[0]
    for i in idx:
        A[i] += int(np.ceil(rng.pareto(alpha) * s))
    return A


def certificates(A):
    P = np.concatenate([[0], np.cumsum(A)])
    g = P - C * np.arange(T + 1)          # g[u] = P[u] - C*u
    # W* = max_v (g[v+1]) - min_{u<=v} g[u]  (u <= v windows)
    W = 0
    m = g[0]
    for v in range(T):
        if g[v] < m:
            m = g[v]
        w = g[v + 1] - m
        if w > W:
            W = w
    return W, W - C * D


def single_queue(A):
    """Work-conserving FIFO; returns per-unit lateness (frames) and backlog."""
    B = 0
    backlog = np.zeros(T, dtype=np.int64)
    arr_total = np.concatenate([[0], np.cumsum(A)])
    serve = np.empty(T, dtype=np.int64)
    for f in range(T):
        serve[f] = min(B + A[f], C)
        B = B + A[f] - serve[f]
        backlog[f] = B
    cum = np.concatenate([[0], np.cumsum(serve)])
    n_units = int(arr_total[-1])
    # k-th unit (0-based) served in frame f where cum[f] > k
    k = np.arange(n_units)
    fserve = np.searchsorted(cum, k, side="right") - 1
    arr_frame = np.repeat(np.arange(T), A)
    lateness = fserve - (arr_frame + D)
    return lateness, backlog


def shard_lat(A, nsh=8, steal=False):
    """Round-robin shards; optional stealing with 1-frame delay."""
    if not steal:
        # rotating round-robin: the frame's units start at the running offset
        # arr_total[f] mod nsh (the non-rotating per-frame split is a strawman:
        # a deterministic base of 5 on 8 shards saturates shards 0-4 forever)
        lats = []
        Aj = np.zeros((nsh, T), dtype=np.int64)
        off = 0
        for f in range(T):
            a = A[f]
            full, rem = divmod(a, nsh)
            Aj[:, f] += full
            for u in range(rem):
                Aj[(off + u) % nsh, f] += 1
            off = (off + a) % nsh
        for j in range(nsh):
            lat, _ = single_queue_for(Aj[j], 1)
            lats.append(lat)
        return np.concatenate(lats)
    # batched shards: a unit is visible to its shard one frame after arrival
    # (handoff latency), deadlines unchanged
    if steal == 'batch':
        Aj = np.zeros((nsh, T), dtype=np.int64)
        off = 0
        for f in range(T):
            a = A[f]
            full, rem = divmod(a, nsh)
            Aj[:, f] += full
            for u in range(rem):
                Aj[(off + u) % nsh, f] += 1
            off = (off + a) % nsh
        lats = []
        for j in range(nsh):
            Ajd = np.concatenate([[0], Aj[j][:-1]])  # visible one frame later
            lat, _ = single_queue_for(Ajd, 1)
            lats.append(lat + 1)                     # deadline still arr+D
        return np.concatenate(lats)
    # stealing: sequential simulation with unit-level queues
    qs = [deque() for _ in range(nsh)]     # each entry: [arrival, units]
    glob = deque()
    rr = 0
    served = []                            # (arrival_frame, serve_frame)
    for f in range(T):
        a = A[f]
        for u in range(a):
            qs[rr % nsh].append(f)
            rr += 1
        # serve: local first, then steal from longest queue with 1-frame delay
        for j in range(nsh):
            cap = 1
            while cap > 0:
                if qs[j]:
                    arr = qs[j].popleft()
                    served.append((arr, f))
                    cap -= 1
                else:
                    # steal single unit from the longest other queue
                    longest = max(range(nsh), key=lambda i: len(qs[i]))
                    if longest != j and qs[longest]:
                        arr = qs[longest].popleft()
                        served.append((arr, f))     # 1-frame transfer folded in
                        cap -= 1
                    else:
                        break
    arr_f = np.array([s[0] for s in served])
    ser_f = np.array([s[1] for s in served])
    return ser_f - (arr_f + D)


def single_queue_for(A, cap):
    B = 0
    serve = np.empty(len(A), dtype=np.int64)
    for f in range(len(A)):
        serve[f] = min(B + A[f], cap)
        B = B + A[f] - serve[f]
    cum = np.concatenate([[0], np.cumsum(serve)])
    n_units = int(np.concatenate([[0], np.cumsum(A)])[-1])
    k = np.arange(n_units)
    fserve = np.searchsorted(cum, k, side="right") - 1
    arr_frame = np.repeat(np.arange(len(A)), A)
    return fserve - (arr_frame + D), None


def stats(lat):
    return {"p50": float(np.percentile(lat, 50)),
            "p99": float(np.percentile(lat, 99)),
            "max": float(lat.max()),
            "miss_frac": float((lat > 0).mean())}


def main():
    rng = np.random.default_rng(SEED)
    out = {"seed": SEED, "T": T, "C": C, "D": D, "configs": {}}
    for tag, alpha, util in (("alpha2.5", 2.5, 0.75), ("alpha1.5", 1.5, 0.70)):
        A = arrivals(rng, alpha, util)
        util_meas = A.sum() / (T * C)
        W, M = certificates(A)
        lat_a, backlog = single_queue(A)
        lat_b = shard_lat(A)
        lat_c = shard_lat(A, steal=True)
        lat_d = shard_lat(A, steal='batch')
        cfg = {"alpha": alpha, "util": float(util_meas),
               "W_star": int(W), "M": int(M),
               "max_backlog_sim": int(backlog.max()),
               "exact_W": bool(int(backlog.max()) == int(W)),
               "single": stats(lat_a), "shards": stats(lat_b),
               "steal": stats(lat_c), "batched": stats(lat_d)}
        # B1 soundness: single-queue misses only when forced
        miss_frames = int((lat_a > 0).sum())
        cfg["misses"] = miss_frames
        cfg["sound"] = bool(not (miss_frames > 0 and M <= 0))
        out["configs"][tag] = cfg
    json.dump(out, open("probeB_out.json", "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
