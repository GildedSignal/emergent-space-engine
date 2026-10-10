#!/usr/bin/env python3
"""Phase-neighbour certificate coverage for run 20261010-1407-inversion-5c2a.

Rank of partner j w.r.t. body i at time t0: number of bodies (in the chosen ordering
set: i's co-orbital group, or the merged population) whose wrapped angular distance to
i at t0 is smaller than j's. Coverage at k: min(rank_i->j, rank_j->i) <= k (the
favourable reading: either side monitoring the pair suffices).
"""
import json, math, sys
from collections import defaultdict

TAU = 2.0 * math.pi
TICKS = 4294967296.0

def load(path):
    meta, bodies, enc = None, [], []
    with open(path) as f:
        for line in f:
            o = json.loads(line)
            if o["ev"] == "meta":
                meta = o
            elif o["ev"] == "body":
                bodies.append(o)
            elif o["ev"] == "enc":
                enc.append(o)
    return meta, bodies, enc

def lam(b, t, true=True):
    x = (t * TICKS - b["tp"]) / b["period"]
    m = TAU * (x - math.floor(x))
    if not true:
        l = m + b["pom"]
    else:
        e = b["e"]
        ea = m
        for _ in range(12):
            d = (ea - e * math.sin(ea) - m) / (1.0 - e * math.cos(ea))
            ea -= d
            if abs(d) < 1e-14:
                break
        f = 2.0 * math.atan2(math.sqrt(1.0 + e) * math.sin(ea / 2.0),
                             math.sqrt(1.0 - e) * math.cos(ea / 2.0))
        l = b["pom"] + f
    if b["mirror"]:
        l = -l
    return l % TAU

def wrap(d):
    return abs(d) % TAU

class Order:
    """Sorted longitudes of a set at time t0, extended by +-TAU for circular ranks."""
    def __init__(self, bs, t0):
        self.ext = sorted(lam(b, t0) for b in bs)
        self.ext = [-x for x in reversed(self.ext)] + self.ext + [TAU + x for x in self.ext]
    def rank(self, li, lj):
        d = wrap(lj - li)
        if d == 0.0:
            return 0
        lo, hi = li - d, li + d
        # bisect on self.ext
        import bisect
        a = bisect.bisect_left(self.ext, lo)
        b = bisect.bisect_right(self.ext, hi)
        return max(0, b - a - 1)  # minus self


def coverage(bodies, enc, k, windows_orbits, t_end, group_of, merged):
    """Returns (covered, total) over events; orders rebuilt at each window open."""
    n = len(bodies)
    by_group = defaultdict(list)
    for idx, b in enumerate(bodies):
        by_group[b["g"]].append(idx)
    W = windows_orbits * TAU
    n_windows = max(1, math.ceil(t_end / W - 1e-12))
    # cache orders per window
    orders = {}
    def get_order(m, g_or_all, i):
        key = (m, g_or_all if g_or_all != "merged" else -1)
        if key not in orders:
            t0 = m * W
            if g_or_all == "merged":
                bs = bodies
            else:
                bs = [bodies[x] for x in by_group[g_or_all]]
            orders[key] = Order(bs, t0)
        return orders[key]
    cov = tot = 0
    for e in enc:
        i, j, t = e["i"], e["j"], e["t"]
        m = min(int(t / W), n_windows - 1)
        bi, bj = bodies[i], bodies[j]
        if merged:
            o = get_order(m, "merged", i)
            li, lj = lam(bi, m * W), lam(bj, m * W)
            r1 = o.rank(li, lj)
            r2 = o.rank(lj, li)
        else:
            if bi["g"] != bj["g"]:
                tot += 1
                continue  # partner not in the co-orbital group: rank infinite
            o = get_order(m, bi["g"], i)
            li, lj = lam(bi, m * W), lam(bj, m * W)
            r1 = o.rank(li, lj)
            r2 = o.rank(lj, li)
        tot += 1
        if min(r1, r2) <= k:
            cov += 1
    return cov, tot

def rank_at_event(bodies, enc, k, merged):
    by_group = defaultdict(list)
    for idx, b in enumerate(bodies):
        by_group[b["g"]].append(idx)
    cov = tot = 0
    o_cache = {}
    for e in enc:
        i, j, t = e["i"], e["j"], e["t"]
        bi, bj = bodies[i], bodies[j]
        if not merged and bi["g"] != bj["g"]:
            tot += 1
            continue
        key = "merged" if merged else bi["g"]
        if key not in o_cache:
            bs = bodies if merged else [bodies[x] for x in by_group[bi["g"]]]
            o_cache[key] = None  # order depends on t; build per event (cheap: 600 sorts)
        bs = bodies if merged else [bodies[x] for x in by_group[bi["g"]]]
        o = Order(bs, t)
        li, lj = lam(bi, t), lam(bj, t)
        r = min(o.rank(li, lj), o.rank(lj, li))
        tot += 1
        if r <= k:
            cov += 1
    return cov, tot

def main(path):
    meta, bodies, enc = load(path)
    n, t_end = meta["n"], meta["t_end"]
    # distinctness: duplicates by (i,j,t)
    seen = set()
    dup = 0
    for e in enc:
        key = (e["i"], e["j"], round(e["t"], 9))
        if key in seen:
            dup += 1
        seen.add(key)
    cross = sum(1 for e in enc if bodies[e["i"]]["g"] != bodies[e["j"]]["g"])
    pairs_per = defaultdict(int)
    for e in enc:
        pairs_per[(e["i"], e["j"])] += 1
    mult = sorted(pairs_per.values())
    print(f"== {meta['scene']}: enc={len(enc)} cross={cross} ({100*cross/len(enc):.1f}%) "
          f"intra={len(enc)-cross} dup={dup} distinct_pairs={len(pairs_per)} "
          f"max_events_per_pair={mult[-1] if mult else 0} pairs_quadratic_tier={meta['pairs']} "
          f"({meta['pairs']/len(enc):.1f}/enc) wall={meta['wall_s']}s")
    k = 4
    c, t = rank_at_event(bodies, enc, k, merged=True)
    print(f"  rank@event merged k={k}: {c}/{t} = {100*c/t:.2f}%")
    c, t = rank_at_event(bodies, enc, k, merged=False)
    if t:
        print(f"  rank@event per-group k={k}: {c}/{t} = {100*c/t:.2f}%")
    for W in [50.0, 10.0, 5.0, 1.0, 0.1, 0.05]:
        for merged in (False, True):
            c, t = coverage(bodies, enc, k, W, t_end, None, merged)
            nw = max(1, math.ceil(t_end / (W * TAU) - 1e-12))
            certs_per_enc = n * k * nw / len(enc)
            tag = "merged " if merged else "per-grp"
            print(f"  W={W:6.2f} orb {tag} k={k}: covered {c}/{t} = {100*c/t:7.2f}%   certs/enc={certs_per_enc:9.1f}")

if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
