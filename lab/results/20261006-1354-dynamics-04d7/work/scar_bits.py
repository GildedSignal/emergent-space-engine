#!/usr/bin/env python3
"""Scar growth under endogenous stirring (dynamics lens, run 20261006-1354).

Extends the checked belt_sim (20261006-1029-dynamics-6875) with the population store's
information accounting: the belt is born as a program (components-98bc; 0.126 bits/body at
2^20, ~0 at 1e9), and every kick writes an exact scar = the body's quantized difference
from its birth program. We measure bits/body(t) at two quanta:

  work : the dossier's draw precisions (p 27 bits over the band, e 12-bit table, t_p 44 bits)
  behav: the encounter scale (q = rho = 1e-3 in a, e, and phase in radians ~ rho/a)

Cost model mirrors crates/shipmem: Elias-Fano ordinal set (2 + log2(n/k) bits per scarred
ordinal, the crate's own documented rate) + zigzag-gamma value rows (gamma(m)=2*floor
(log2(m+1))+1, zero columns cost 1). A floor model (log2(m+1)+1) brackets codec overhead.
Sub-quantum deviations cost nothing and accumulate exactly (principle 6): we track the
exact float state and quantize only when costing.

Phase accounting: canonical phase-at-epoch-0 Lambda = lam - n(a)*tref is frozen between
kicks; the store holds (Da, Dex, Dey, DLambda) and the reader propagates with the true
n(a), so a scar's bits are fixed at write time. DLambda wraps mod 2pi.
"""
import heapq, math, random, sys, json
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import belt_sim as bs

TAU = 2.0 * math.pi

QUANTA = {
    "work":  dict(qa=0.5 / 2**27, qe=0.5 / 2**12, ql=TAU / 2**44),
    "behav": dict(qa=1e-3,        qe=1e-3,        ql=1e-3 / 1.25),
}

def gamma(m):   # zigzag+gamma cost in bits for nonnegative int m
    return 2 * int(math.floor(math.log2(m + 1))) + 1 if m > 0 else 1

def floorcode(m):
    return math.log2(m + 1) + 1.0 if m > 0 else 1.0

def canon(bd):
    """(a, ex, ey, Lambda-at-epoch-0)."""
    return bd[0], bd[1], bd[2], bd[3] - bs.n_of(bd[0]) * bd[4]

def dev_ints(birth, bd, q):
    a0, x0, y0, l0 = birth
    a, x, y, l = canon(bd)
    dl = (l - l0 + math.pi) % TAU - math.pi
    return (round((a - a0) / q["qa"]), round((x - x0) / q["qe"]),
            round((y - y0) / q["qe"]), round(dl / q["ql"]))

def cost_rows(births, B, q, codec=gamma):
    n = len(B)
    rows = [dev_ints(births[i], B[i], q) for i in range(n)]
    scarred = [r for r in rows if any(m != 0 for m in r)]
    k = len(scarred)
    if k == 0:
        return 0.0, 0.0, 0
    idx = k * (2.0 + math.log2(n / k))          # Elias-Fano ordinals
    val = sum(codec(abs(m)) for r in scarred for m in r)
    return (idx + val) / n, (idx / k + sum(codec(abs(m)) for r in scarred for m in r) / k), k

def run(n=300, sigma_e=1e-2, a_lo=1.0, a_hi=1.5, gm=0.0, orbits=200, seed=0,
        rho=1e-3, snap_every=20):
    B = bs.make_belt(n, sigma_e, a_lo, a_hi, seed)
    births = [canon(b) for b in B]
    t_end = orbits * TAU / bs.n_of(1.25)
    h = []
    def sched_pair(i, j, t):
        t2 = bs.next_conj(B[i], B[j], t)
        if t2 is not None and t2 < t_end:
            heapq.heappush(h, (t2, i, j, B[i][5], B[j][5]))
    for i in range(n):
        for j in range(i + 1, n):
            if bs.overlap(B[i], B[j]):
                sched_pair(i, j, 0.0)
    orb_t = TAU / bs.n_of(1.25)
    snaps = []
    counts = dict(conj=0, enc=0, kicks=0, rowwrites=0)
    next_snap = snap_every
    prev_rows = {name: [dev_ints(births[i], B[i], q) for i in range(n)] for name, q in QUANTA.items()}
    while h:
        t, i, j, vi, vj = heapq.heappop(h)
        if t >= t_end:
            break
        if vi != B[i][5] or vj != B[j][5]:
            continue
        counts['conj'] += 1
        xi, yi, vri, vti = bs.posvel(B[i], t)
        xj, yj, vrj, vtj = bs.posvel(B[j], t)
        b = math.hypot(xi - xj, yi - yj)
        if b < rho:
            counts['enc'] += 1
        dvr, dvt = vri - vrj, vti - vtj
        v2 = dvr * dvr + dvt * dvt
        if gm > 0.0 and v2 > 0.0:
            alpha = 2.0 * gm / (max(b, 1e-4) * v2)
            alpha = min(alpha, 0.5)
            dv = 2.0 * math.sqrt(v2) * math.sin(alpha / 2.0)
            sgn = 1.0 if ((i * 2654435761 + j * 40503 + int(t * 1e6)) & 1) else -1.0
            v = math.sqrt(v2)
            ur, ut = dvr / v, dvt / v
            pr, pt = -ut * sgn, ur * sgn
            h_i = dv / 2.0
            bs.apply_dv(B[i], t, h_i * pr, h_i * pt)
            bs.apply_dv(B[j], t, -h_i * pr, -h_i * pt)
            counts['kicks'] += 2
            for u_ in (i, j):
                for name, q in QUANTA.items():
                    new = dev_ints(births[u_], B[u_], q)
                    if new != prev_rows[name][u_]:
                        if name == "behav" and any(m != 0 for m in new):
                            counts['rowwrites'] += 1
                        prev_rows[name][u_] = new
                for k2 in range(n):
                    if k2 != i and k2 != j and bs.overlap(B[u_], B[k2]):
                        sched_pair(min(u_, k2), max(u_, k2), t)
        sched_pair(i, j, t)
        while t >= next_snap * orb_t:
            snap = dict(orbit=next_snap, conj=counts['conj'], enc=counts['enc'],
                        kicks=counts['kicks'], rowwrites=counts['rowwrites'])
            for name, q in QUANTA.items():
                rows = [dev_ints(births[i], B[i], q) for i in range(n)]
                scarred = [r for r in rows if any(m != 0 for m in r)]
                k = len(scarred)
                percol = [sum(gamma(abs(r[c])) for r in scarred) / n for c in range(4)]
                idx = k * (2.0 + math.log2(n / k)) if k else 0.0
                val = sum(percol)
                bpb = idx / n + val
                persb = (idx + val * n) / k if k else 0.0
                fl = (idx + sum(sum(floorcode(abs(m)) for m in r) for r in scarred)) / n if k else 0.0
                snap[name] = dict(bpb=bpb, persb=persb, floor=fl, k=k,
                                  percol=percol, idx=idx / n)
            # raw deviations for post-hoc quanta / spread analysis (compact)
            da = sorted(abs(B[i2][0] - births[i2][0]) for i2 in range(n))
            dl = sorted(abs((canon(B[i2])[3] - births[i2][3] + math.pi) % TAU - math.pi)
                        for i2 in range(n))
            snap["dev"] = dict(
                da_p50=da[n // 2], da_p90=da[(9 * n) // 10], da_max=da[-1],
                dl_p50=dl[n // 2], dl_p90=dl[(9 * n) // 10], dl_max=dl[-1])
            snaps.append(snap)
            next_snap += snap_every
    return snaps, dict(conj=counts['conj'], enc=counts['enc'], kicks=counts['kicks'],
                       rowwrites=counts['rowwrites'], gm=gm, n=n, orbits=orbits, seed=seed)

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--gm', type=float, default=0.0)
    ap.add_argument('--orbits', type=float, default=200)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--n', type=int, default=300)
    ap.add_argument('--snap-every', type=int, default=20)
    ap.add_argument('--out', default=None)
    a = ap.parse_args()
    snaps, stats = run(n=a.n, gm=a.gm, orbits=a.orbits, seed=a.seed, snap_every=a.snap_every)
    if a.out:
        with open(a.out, 'w') as f:
            json.dump(dict(snaps=snaps, stats=stats), f)
    print(json.dumps(stats))
