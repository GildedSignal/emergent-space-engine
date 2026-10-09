#!/usr/bin/env python3
"""Reabsorption ceiling: how fast can kicked-out bodies be re-banded into new programs?

Model of one reabsorption pass over the scar set (the operation shipmem must do to fold
scarred bodies back into programs): key each body by its quantized (E, L) band, sort,
group. We measure the sort+group rate for the payload sizes of the law (16-byte tube key
view: 8-byte far-time + 4+4-byte quantized E,L), at 10^7 and 5x10^7 bodies, single core,
plus a binary-heap event-key rate (the queue term).

Linux x86 shared runner: orders of magnitude only. The M1 re-measures.
"""
import json, time, os, resource

import numpy as np

rng = np.random.default_rng(20261009)


def reabsorb(n):
    # Quantized (E, L) of n scarred bodies: E ~ N(0,1) 32-bit scaled, L ~ N(0,1), plus
    # the 8-byte next-event far-time each body carries in the scar.
    e = rng.standard_normal(n)
    l = rng.standard_normal(n)
    t = rng.integers(0, 1 << 48, size=n, dtype=np.uint64)
    qe = (e * (1 << 24)).astype(np.int64)  # quantized E
    ql = (l * (1 << 24)).astype(np.int64)  # quantized L
    key = (qe.astype(np.uint64) << np.uint64(32)) | (ql.astype(np.uint64) & np.uint64((1 << 32) - 1))
    t0 = time.perf_counter()
    order = np.argsort(key, kind="stable")  # the re-band: sort by quantized invariants
    t_sort = time.perf_counter() - t0
    t0 = time.perf_counter()
    # group into families: contiguous equal-key runs are one program
    sk = key[order]
    starts = np.flatnonzero(np.concatenate(([True], sk[1:] != sk[:-1])))
    n_families = len(starts)
    t_group = time.perf_counter() - t0
    return t_sort, t_group, n_families


def heap_rate(n):
    import heapq

    h = []
    push = heapq.heappush
    pop = heapq.heappop
    keys = rng.integers(0, 1 << 62, size=n).tolist()
    t0 = time.perf_counter()
    for k in keys:
        push(h, (k, k & 0xFFFFFFFF))
    t_push = time.perf_counter() - t0
    t0 = time.perf_counter()
    while h:
        pop(h)
    t_pop = time.perf_counter() - t0
    return t_push, t_pop


def state():
    load = open("/proc/loadavg").read().split()
    mem = open("/proc/meminfo").readlines()
    d = {m.split(":")[0]: m.split()[1] for m in mem[:5]}
    return {
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "loadavg": " ".join(load[:3]),
        "meminfo_kb": d,
        "max_rss_kb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "nproc": os.cpu_count(),
    }


if __name__ == "__main__":
    out = {"state_before": state()}
    for n in (10_000_000, 50_000_000):
        ts, tg, nf = reabsorb(n)
        out[f"reabsorb_{n}"] = {
            "sort_s": round(ts, 3),
            "group_s": round(tg, 3),
            "families": int(nf),
            "bodies_per_s_per_core": round(n / (ts + tg)),
            "bytes_payload": n * 16,
        }
    tp, td = heap_rate(2_000_000)
    out["heap_2e6"] = {
        "push_s": round(tp, 3),
        "pop_s": round(td, 3),
        "keys_per_s": round(2_000_000 / (tp + td)),
        "bytes_if_10e9_12B": int(10**9 * 12),
    }
    out["state_after"] = state()
    print(json.dumps(out, indent=1))
