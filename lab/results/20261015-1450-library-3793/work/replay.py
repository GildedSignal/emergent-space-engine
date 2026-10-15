#!/usr/bin/env python3
"""Replay the engine's own key-read trace through bounded caches.

Policies: LRU (evict least-recently-used), 2Q (Johnson & Shasha: a key enters the
main LRU queue only on its SECOND reference; one-touch readers — scans — never
evict the hot set), and MRU-evict (a scan-friendly control that keeps the OLD
working set, evicting most-recently-used, the anti-LRU).
Trace: little-endian u32 catalogue keys, one per in-flight read of a standing
binding's compiled trajectory (keytrace.rs probe).
"""
import struct, sys, json
from collections import OrderedDict, Counter

def replay(keys, K, policy):
    if policy == "lru":
        cache = OrderedDict(); hits = 0
        for k in keys:
            if k in cache:
                hits += 1; cache.move_to_end(k)
            else:
                if len(cache) >= K: cache.popitem(last=False)
                cache[k] = 1
        return hits
    if policy == "2q":
        # A1in (FIFO, one-touch), A1out (ghost, keys only), Am (LRU main).
        a1in = OrderedDict(); a1out = OrderedDict(); am = OrderedDict()
        kin = kout = K // 4 or 1            # 25% / 75% split, as in the paper
        km = K - kin
        hits = 0
        for k in keys:
            if k in am:
                hits += 1; am.move_to_end(k)
            elif k in a1out:
                a1out.pop(k)                # second reference: promote to main
                if len(am) >= km: am.popitem(last=False)
                am[k] = 1
            elif k in a1in:
                pass                        # re-reference while still in A1in counts as hit
                hits += 1
            else:
                if len(a1in) >= kin:
                    old = a1in.popitem(last=False)[0]
                    if len(a1out) >= kout: a1out.popitem(last=False)
                    a1out[old] = 1
                a1in[k] = 1
        return hits
    if policy == "mru":                     # control: evict most-recently-used
        cache = OrderedDict(); hits = 0
        for k in keys:
            if k in cache:
                hits += 1
            else:
                if len(cache) >= K: cache.popitem(last=True)
                cache[k] = 1; cache.move_to_end(k)  # keep insertion order = recency for pop(last)
        return hits
    raise ValueError(policy)

def main():
    path = sys.argv[1]
    d = open(path, "rb").read()
    n = len(d) // 4
    ks = struct.unpack(f"<{n}I", d)
    out = {"trace": path, "reads": n, "distinct": len(set(ks))}
    burn = n // 10
    out["post_burn_reads"] = n - burn
    for tag, seq in (("full", ks), ("post_burn_in", ks[burn:]), ("middle_third", ks[n//3:2*n//3])):
        r = {"reads": len(seq)}
        for K in (64, 128, 256, 512, 1024, 2048, 4096):
            for pol in ("lru", "2q", "mru"):
                r[f"{pol}_{K}"] = replay(seq, K, pol) / len(seq)
        out[tag] = r
    json.dump(out, open(sys.argv[2], "w"), indent=1)
    print(json.dumps({k: (v if not isinstance(v, dict) else {kk: round(vv, 4) if isinstance(vv, float) else vv for kk, vv in list(v.items())[:8]}) for k, v in out.items()}, indent=1))

if __name__ == "__main__":
    main()
