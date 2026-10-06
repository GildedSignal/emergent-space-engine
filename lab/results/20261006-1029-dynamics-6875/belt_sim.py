#!/usr/bin/env python3
"""Belt event dynamics with kick feedback (dynamics lens, run 20261006-1029).

First order in e, GM=1. Bodies: (a, eps=ex+i*ey, lam at tref). Conjunction when mean
longitudes cross; miss distance b from first-order positions; impulse rotates v_rel
(exact momentum+energy for the pair); Gauss-inverse updates elements. Pairs outside the
radial-overlap window are outside the certificate (two-tier premise) and enter/leave
incrementally on kicks of a member. No ticks: exact event times.
"""
import heapq, math, random, sys, json

TAU = 2.0 * math.pi

def make_belt(n, sigma_e, a_lo, a_hi, seed):
    rng = random.Random(seed)
    bodies = []
    for _ in range(n):
        a = a_lo + (a_hi - a_lo) * rng.random()
        u = rng.random()
        e = min(sigma_e * math.sqrt(-2.0 * math.log(1.0 - u)), 0.5)
        pom = TAU * rng.random()
        lam = TAU * rng.random()
        bodies.append([a, e * math.cos(pom), e * math.sin(pom), lam, 0.0, 0])
    return bodies

def n_of(a):
    return a ** -1.5

def lam_at(bd, t):
    return bd[3] + n_of(bd[0]) * (t - bd[4])

def elems(bd, t):
    """(a, e, pom, M) at time t."""
    a, ex, ey = bd[0], bd[1], bd[2]
    e = math.hypot(ex, ey)
    pom = math.atan2(ey, ex) if e > 1e-15 else 0.0
    M = lam_at(bd, t) % TAU
    return a, e, pom, M

def posvel(bd, t):
    a, e, pom, M = elems(bd, t)
    u = M - pom
    cu, su = math.cos(u), math.sin(u)
    r = a * (1.0 - e * cu)
    th = M + 2.0 * e * su
    x = r * math.cos(th); y = r * math.sin(th)
    na = n_of(a) * a
    vr = na * e * su
    vt = na * (1.0 + e * cu)
    return x, y, vr, vt

def apply_dv(bd, t, dvr, dvt):
    """Impulse (radial, along-track) at time t; first-order inverse Gauss."""
    a, e, pom, M = elems(bd, t)
    na = n_of(a) * a
    vr = na * e * math.sin(M - pom)
    vt = na * (1.0 + e * math.cos(M - pom))
    da = 2.0 * a * a * n_of(a) * dvt          # delta-a from energy (GM=1)
    a2 = max(a + da, 0.05)
    na2 = n_of(a2) * a2
    p = vt + dvt; p = p / na2 - 1.0           # e cos u
    q = (vr + dvr) / na2                      # e sin u
    # eps_bar * e^{iM} = p + i q  ->  eps = (p - i q) e^{iM}
    cM, sM = math.cos(M), math.sin(M)
    bd[1] = p * cM + q * sM
    bd[2] = p * sM - q * cM
    bd[0] = a2
    bd[3] = M; bd[4] = t; bd[5] += 1

def overlap(bi, bj):
    ai, ei = bi[0], math.hypot(bi[1], bi[2])
    aj, ej = bj[0], math.hypot(bj[1], bj[2])
    return abs(ai - aj) <= ai * ei + aj * ej + 4e-3   # +4 bodies' radii margin

def next_conj(bi, bj, t):
    """Next t2 > t when mean longitudes cross, or None if synodic ~ 0."""
    li, lj = lam_at(bi, t) % TAU, lam_at(bj, t) % TAU
    dn = n_of(bi[0]) - n_of(bj[0])
    if abs(dn) < 1e-12:
        return None
    d = (li - lj) % TAU                        # want d + dn*(t2-t) = 0 mod TAU
    if dn > 0:
        dt = ((TAU - d) % TAU) / dn
    else:
        dt = d / (-dn)
    if dt <= 1e-9:
        dt += TAU / abs(dn)
    return t + dt

def run(n=300, sigma_e=1e-2, a_lo=1.0, a_hi=1.5, gm=0.0, orbits=200, seed=0,
        rho=1e-3, inject=None, log_every=1):
    """inject: (orbit, dvt) tangential impulse on body 0. Returns (rows, stats)."""
    B = make_belt(n, sigma_e, a_lo, a_hi, seed)
    t_end = orbits * TAU / n_of(1.25)
    h = []
    resched = 0
    def sched_pair(i, j, t):
        nonlocal resched
        t2 = next_conj(B[i], B[j], t)
        if t2 is not None and t2 < t_end:
            heapq.heappush(h, (t2, i, j, B[i][5], B[j][5]))
            resched += 1
    for i in range(n):
        for j in range(i + 1, n):
            if overlap(B[i], B[j]):
                sched_pair(i, j, 0.0)
    orb_t = TAU / n_of(1.25)
    sum_inv_a0 = sum(1.0 / b[0] for b in B)
    rows = []
    ev_times = []
    counts = dict(conj=0, enc=0, strong=0)
    next_log = log_every
    inj_done = False
    while h:
        t, i, j, vi, vj = heapq.heappop(h)
        if t >= t_end:
            break
        if vi != B[i][5] or vj != B[j][5]:
            continue
        counts['conj'] += 1
        xi, yi, vri, vti = posvel(B[i], t)
        xj, yj, vrj, vtj = posvel(B[j], t)
        b = math.hypot(xi - xj, yi - yj)
        if b < rho:
            counts['enc'] += 1
        dvr, dvt = vri - vrj, vti - vtj
        v2 = dvr * dvr + dvt * dvt
        if gm > 0.0 and v2 > 0.0:
            alpha = 2.0 * gm / (max(b, 1e-4) * v2)
            alpha = min(alpha, 0.5)
            dv = 2.0 * math.sqrt(v2) * math.sin(alpha / 2.0)  # |delta v_rel|
            sgn = 1.0 if ((i * 2654435761 + j * 40503 + int(t * 1e6)) & 1) else -1.0
            # rotate v_rel by +-alpha: unit perpendicular to (dvr,dvt)
            v = math.sqrt(v2)
            ur, ut = dvr / v, dvt / v
            pr, pt = -ut * sgn, ur * sgn
            h_i = dv / 2.0
            apply_dv(B[i], t, h_i * pr, h_i * pt)
            apply_dv(B[j], t, -h_i * pr, -h_i * pt)
            if alpha > 0.1:
                counts['strong'] += 1
            # reschedule both bodies' overlap neighbourhoods (incremental certificate)
            for u_ in (i, j):
                bu = B[u_]
                for k in range(n):
                    if k == i or k == j:
                        continue
                    if overlap(bu, B[k]):
                        sched_pair(min(u_, k), max(u_, k), t)
        sched_pair(i, j, t)  # next synodic crossing of this pair, kicks or not
        # logging per orbit
        while t >= next_log * orb_t:
            es = [math.hypot(b[1], b[2]) for b in B]
            es.sort()
            med = es[n // 2]
            ovl = 0
            asorted = sorted(range(n), key=lambda k: B[k][0] * (1 - math.hypot(B[k][1], B[k][2])))
            ends = []
            for k in asorted:
                ek = math.hypot(B[k][1], B[k][2])
                lo = B[k][0] * (1 - ek); hi2 = B[k][0] * (1 + ek)
                while ends and ends[0][0] < lo:
                    heapq.heappop(ends)
                ovl += len(ends)
                heapq.heappush(ends, (hi2, k))
            rows.append(dict(orbit=next_log, sigma_e=med, overlap=ovl,
                             conj=counts['conj'], enc=counts['enc'],
                             strong=counts['strong'], resched=resched,
                             drift=sum(1.0 / b[0] for b in B) - sum_inv_a0,
                             emax=es[-1]))
            next_log += log_every
        if inject and not inj_done and t >= inject[0] * orb_t:
            inj_done = True
            apply_dv(B[0], t, 0.0, inject[1])
            for k in range(n):
                if k != 0 and overlap(B[k], B[0]):
                    sched_pair(0, k, t)
    stats = dict(conj=counts['conj'], enc=counts['enc'], strong=counts['strong'],
                 resched=resched, gm=gm, n=n, orbits=orbits, seed=seed,
                 drift=sum(1.0 / b[0] for b in B) - sum_inv_a0)
    return rows, stats

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--gm', type=float, default=0.0)
    ap.add_argument('--orbits', type=float, default=200)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--n', type=int, default=300)
    ap.add_argument('--out', default=None)
    ap.add_argument('--inject-orbit', type=float, default=None)
    ap.add_argument('--inject-dvt', type=float, default=None)
    a = ap.parse_args()
    inj = (a.inject_orbit, a.inject_dvt) if a.inject_orbit else None
    rows, stats = run(n=a.n, gm=a.gm, orbits=a.orbits, seed=a.seed, inject=inj)
    if a.out:
        with open(a.out, 'w') as f:
            json.dump(dict(rows=rows, stats=stats), f)
    print(json.dumps(stats))
