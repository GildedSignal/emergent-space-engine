#!/usr/bin/env python3
"""Conjunction map of a coplanar belt (dynamics lens, run 20261006-0437).

Exact Kepler drift about one dominant mass (mu=1); interactions only at conjunctions
(mean-longitude alignment, closed form in time), where positions/velocities are evaluated
exactly via Kepler and an impulse |dv| = 2*m_other/(v_rel*d) is applied along the separation
(thin-lens hyperbolic deflection, momentum-conserving). This mirrors the law's own structure:
compiled drift plus kicks. Measures: kick-rate relaxation, element diffusion, log-u quantum
crossings (pair re-setup certificates), burstiness (Allan factor), branching proxy, and a
fragmentation (Kessler) mode.
"""
import argparse, json, math, heapq, random, sys, time
import numpy as np

TWOPI = 2.0 * math.pi

def kepler_E(M, e):
    M = (M + math.pi) % TWOPI - math.pi
    E = M
    for _ in range(10):
        f = E - e * math.sin(E) - M
        fp = 1.0 - e * math.cos(E)
        E -= f / fp
    return E

def state_at(t, p, e, w, lm0, n):
    """Position and velocity at time t (exact Kepler, planar)."""
    lm = lm0 + n * t
    E = kepler_E(lm - w, e)
    cE, sE = math.cos(E), math.sin(E)
    r = p / (1.0 + e * cE)
    # true anomaly and longitude
    xf = cE - e; yf = sE * math.sqrt(max(1e-18, 1.0 - e * e))
    f = math.atan2(yf, xf)
    lam = w + f
    h = math.sqrt(p)  # mu=1
    vr = h / p * e * math.sin(f)
    vt = h / p * (1.0 + e * math.cos(f))
    cl, sl = math.cos(lam), math.sin(lam)
    x = r * cl; y = r * sl
    vx = vr * cl - vt * sl; vy = vr * sl + vt * cl
    return x, y, vx, vy

def elements_from(x, y, vx, vy, t):
    r2 = x * x + y * y; r = math.sqrt(r2)
    v2 = vx * vx + vy * vy; rv = x * vx + y * vy
    h = x * vy - y * vx
    p = h * h
    ex = (v2 - 1.0 / r) * x - rv * vx
    ey = (v2 - 1.0 / r) * y - rv * vy
    e = math.hypot(ex, ey)
    w = math.atan2(ey, ex) if e > 1e-14 else 0.0
    one_m_e2 = 1.0 - e * e
    if one_m_e2 <= 1e-12:
        a = float('inf'); n = 0.0
    else:
        a = p / one_m_e2
        n = a ** -1.5
    # mean longitude at t (continue the same mean longitude)
    f = math.atan2(y, x) - w
    E = 2.0 * math.atan2(math.sqrt(max(1e-18, 1 - e)) * math.sin(f / 2),
                         math.sqrt(max(1e-18, 1 + e)) * math.cos(f / 2))
    M = E - e * math.sin(E)
    lm = w + M
    lm0 = lm - n * t
    return p, e, w, lm0, n, a
def next_synodic(t, i, j):
    dn = NN[i] - NN[j]
    if abs(dn) < 1e-14:
        return None
    return t + TWOPI / abs(dn)

def next_conj(t, i, j):
    dlm = (LM0[i] - LM0[j]) + (NN[i] - NN[j]) * t
    dn = NN[i] - NN[j]
    if abs(dn) < 1e-14:
        return None
    g = dlm % TWOPI
    if dn > 0:
        dt = ((TWOPI - g) if g > 1e-9 else TWOPI) / dn
    else:
        dt = (g if g > 1e-9 else TWOPI) / (-dn)
    if not (dt > 1e-9) or dt != dt or dt > 1e9:
        return None
    return t + dt

# globals per body (python lists for speed)
P = []; EE = []; W = []; LM0 = []; NN = []; AA = []; MASS = []; ALIVE = []; VER = []
last_done = {}

def add_body(m, p, e, w, lm0, n, a):
    P.append(p); EE.append(e); W.append(w); LM0.append(lm0); NN.append(n); AA.append(a)
    MASS.append(m); ALIVE.append(True); VER.append(0)
    return len(P) - 1

def pair_key(i, j):
    return (i, j) if i < j else (j, i)

def build_pairs(heap, t, margin_extra=0.0):
    idx = [i for i in range(len(P)) if ALIVE[i]]
    idx.sort(key=lambda i: AA[i])
    maxea = max((EE[i] * AA[i] for i in idx), default=0.0)
    R = maxea + BMAX + margin_extra
    added = 0
    lo = 0
    pairs = []
    for k, i in enumerate(idx):
        ai = AA[i]
        while lo < len(idx) and AA[idx[lo]] < ai - R:
            lo += 1
        for q in range(lo, len(idx)):
            j = idx[q]
            if j <= i or AA[j] > ai + R:
                if AA[j] > ai + R: break
                continue
            pairs.append((i, j))
    for (i, j) in pairs:
        tc = next_conj(t, i, j)
        if tc is not None:
            heapq.heappush(heap, (tc, i, j, VER[i], VER[j]))
            added += 1
    return len(pairs), added

def main():
    global BMAX, BC
    ap = argparse.ArgumentParser()
    ap.add_argument('--N', type=int, default=768)
    ap.add_argument('--orbits', type=float, default=240.0)
    ap.add_argument('--mass', type=float, default=1e-8)
    ap.add_argument('--sigma-e', type=float, default=0.02)
    ap.add_argument('--a-min', type=float, default=1.0)
    ap.add_argument('--a-max', type=float, default=1.4)
    ap.add_argument('--bmax', type=float, default=0.0, help='encounter radius; 0 = 2 mutual Hill at a-mean')
    ap.add_argument('--frag', type=int, default=-1, help='-1 elastic; K>=0: contact replaces pair by K fragments (0=annihilate)')
    ap.add_argument('--bc', type=float, default=0.0, help='contact radius for frag mode; 0 = bmax/6')
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--frag-dv', type=float, default=3e-3)
    ap.add_argument('--wall', type=float, default=150.0)
    ap.add_argument('--out', type=str, required=True)
    ap.add_argument('--dump', type=str, default='')
    args = ap.parse_args()
    rng = random.Random(args.seed)
    t0_wall = time.time()

    amin, amax = args.a_min, args.a_max
    if args.bmax <= 0:
        args.bmax = 2.0 * ((2.0 * args.mass / 3.0) ** (1.0 / 3.0)) * 0.5 * (amin + amax)
    BMAX = args.bmax
    BC = args.bc if args.bc > 0 else BMAX / 6.0

    # birth: banded uniform a, Rayleigh e, uniform angles (the B18b belt shape)
    for _ in range(args.N):
        a = rng.uniform(amin, amax)
        e = abs(rng.gauss(0.0, args.sigma_e / math.sqrt(2)))
        w = rng.uniform(0, TWOPI); lm0 = rng.uniform(0, TWOPI)
        p = a * (1 - e * e)
        add_body(args.mass, p, e, w, lm0, a ** -1.5, a)

    T_end = args.orbits * TWOPI  # time unit: inner orbit ~ 2pi
    heap = []
    npairs, _ = build_pairs(heap, 0.0)
    degree = 2.0 * npairs / args.N

    # quantum grids on ln u (u=1/p): band grid r_k=2^(k/m) -> dln u = ln2/m
    GRIDS = [4, 8, 16, 32, 64]
    ln2 = math.log(2.0)
    lnu = [math.log(1.0 / P[i]) for i in range(len(P))]
    cross = {m: 0 for m in GRIDS}
    cell = {m: [math.floor(x / (ln2 / m)) for x in lnu] for m in GRIDS}

    ev_t = []; ev_i = []; ev_j = []; ev_dv = []; ev_kind = []
    alive_count = args.N; pop_series = []
    E0 = sum(-MASS[i] / (2 * AA[i]) for i in range(len(P)) if ALIVE[i])
    nkick = ncontact = 0; ejected = 0; E_ej = 0.0
    pops = 0; rebuilds = 0
    t = 0.0
    maxea0 = max(EE[i] * AA[i] for i in range(len(P)))

    while heap and t < T_end and time.time() - t0_wall < args.wall:
        tc, i, j, vi, vj = heapq.heappop(heap)
        if tc > T_end: break
        if not (ALIVE[i] and ALIVE[j]):
            continue
        key = pair_key(i, j)
        if tc <= last_done.get(key, -1.0):
            continue
        if vi != VER[i] or vj != VER[j]:
            tn = next_conj(tc, i, j)
            if tn is not None and tn <= T_end:
                heapq.heappush(heap, (tn, i, j, VER[i], VER[j]))
            continue
        t = tc
        last_done[key] = tc
        pops += 1
        while len(pop_series) < int(t / TWOPI):
            pop_series.append(alive_count)
        xi, yi, vxi, vyi = state_at(t, P[i], EE[i], W[i], LM0[i], NN[i])
        xj, yj, vxj, vyj = state_at(t, P[j], EE[j], W[j], LM0[j], NN[j])
        dx, dy = xj - xi, yj - yi
        d = math.hypot(dx, dy)
        if d >= BMAX:
            tn = next_synodic(t, i, j)
            if tn is not None and tn <= T_end:
                heapq.heappush(heap, (tn, i, j, VER[i], VER[j]))
            continue
        # encounter
        dvx, dvy = vxi - vxj, vyi - vyj
        vrel = math.hypot(dvx, dvy)
        if vrel < 1e-12:
            tn = next_conj(t, i, j)
            if tn is not None and tn <= T_end:
                heapq.heappush(heap, (tn, i, j, VER[i], VER[j]))
            continue
        if args.frag >= 0 and d < BC:
            # contact: replace both by K fragments
            ncontact += 1
            ev_t.append(t); ev_i.append(i); ev_j.append(j)
            ev_dv.append(0.0); ev_kind.append(2)
            ALIVE[i] = False; ALIVE[j] = False
            alive_count -= 2
            mx, my = 0.5 * (xi + xj), 0.5 * (yi + yj)
            vmx, vmy = 0.5 * (vxi + vxj), 0.5 * (vyi + vyj)
            m_new = 2.0 * args.mass / max(1, args.frag)
            for _ in range(args.frag):
                ang = rng.uniform(0, TWOPI)
                dv = args.frag_dv * rng.uniform(0.2, 1.0)
                p2, e2, w2, l20, n2, a2 = elements_from(
                    mx + 1e-4 * math.cos(ang), my + 1e-4 * math.sin(ang),
                    vmx + dv * math.cos(ang), vmy + dv * math.sin(ang), t)
                if e2 < 0.95:
                    alive_count += 1
                    nid = add_body(m_new, p2, e2, w2, l20, n2, a2)
                    lnu.append(math.log(1.0 / p2))
                    for m in GRIDS:
                        cell[m].append(math.floor(lnu[-1] / (ln2 / m)))
                    # immediate pairs for the newborn
                    for k2 in range(len(P) - 1):
                        if not ALIVE[k2]: continue
                        if abs(AA[k2] - a2) < max(EE[k2] * AA[k2], EE[nid] * AA[nid]) + BMAX:
                            tn = next_conj(t, nid, k2)
                            if tn is not None and tn <= T_end:
                                heapq.heappush(heap, (tn, min(nid, k2), max(nid, k2), VER[nid], VER[k2]))
            alive_now = sum(ALIVE)
            if alive_now > 6000 or alive_now < 8:
                break
            continue
        # elastic impulse kick
        nkick += 1
        ev_t.append(t); ev_i.append(i); ev_j.append(j)
        ev_kind.append(1)
        ux, uy = dx / d, dy / d
        ki = 2.0 * MASS[j] / (vrel * d)
        kj = 2.0 * MASS[i] / (vrel * d)
        dv_mag = ki
        ev_dv.append(dv_mag)
        for (b, other, sgn) in ((i, j, 1.0), (j, i, -1.0)):
            k = 2.0 * MASS[other] / (vrel * d) * sgn
            xb, yb, vxb, vyb = (xi, yi, vxi, vyi) if b == i else (xj, yj, vxj, vyj)
            p2, e2, w2, l20, n2, a2 = elements_from(xb, yb, vxb + k * ux, vyb + k * uy, t)
            old_lnu = math.log(1.0 / P[b])
            P[b] = p2; EE[b] = e2; W[b] = w2; LM0[b] = l20; NN[b] = n2; AA[b] = a2
            VER[b] += 1
            new_lnu = math.log(1.0 / p2)
            for m in GRIDS:
                g = ln2 / m
                c_new = math.floor(new_lnu / g); c_old = cell[m][b]
                if c_new != c_old:
                    cross[m] += abs(c_new - c_old)
                    cell[m][b] = c_new
            if e2 >= 0.95 or not (0.4 < a2 < 3.0) or a2 != a2:
                E_ej += -MASS[b] / (2 * a2) if a2 == a2 and a2 > 0 else 0.0
                ALIVE[b] = False; ejected += 1; alive_count -= 1
        # reschedule this pair: next full synodic period (one impulse per conjunction)
        tn = next_synodic(t, i, j)
        if tn is not None and tn <= T_end:
            heapq.heappush(heap, (tn, i, j, VER[i], VER[j]))
        # occasional widening rebuild as stirring grows excursions
        if pops % 4000 == 0:
            maxea_now = max((EE[i2] * AA[i2] for i2 in range(len(P)) if ALIVE[i2]), default=0.0)
            if maxea_now > maxea0 * 1.25:
                maxea0 = maxea_now
                _, added = build_pairs(heap, t)
                rebuilds += 1

    wall = time.time() - t0_wall
    alive = [i for i in range(len(P)) if ALIVE[i]]
    E1 = sum(-MASS[i] / (2 * AA[i]) for i in alive)
    orbits_done = t / TWOPI

    ev_t = np.array(ev_t); ev_i = np.array(ev_i, dtype=int); ev_j = np.array(ev_j, dtype=int)
    ev_kind = np.array(ev_kind, dtype=int)

    # kick rate per body per orbit, binned per orbit
    res = {}
    res['params'] = dict(N=args.N, orbits_req=args.orbits, mass=args.mass, sigma_e=args.sigma_e,
                         bmax=BMAX, bc=BC, frag=args.frag, seed=args.seed,
                         amin=amin, amax=amax)
    res['wall_s'] = wall; res['pops'] = pops; res['rebuilds'] = rebuilds
    res['orbits_done'] = orbits_done
    res['nkick'] = int(nkick); res['ncontact'] = int(ncontact); res['ejected'] = ejected
    res['n_alive_end'] = len(alive); res['n_bodies_total'] = len(P)
    res['degree0'] = degree
    res['E_drift_rel'] = ((E1 + E_ej) - E0) / abs(E0) if E0 else 0.0
    nb0 = args.N
    if len(ev_t):
        bins = np.arange(0, t + TWOPI, TWOPI)
        kicks = ev_t[ev_kind == 1]
        denom = max(1, len(alive)) * 1.0
        cnt, _ = np.histogram(kicks, bins=bins)
        ccont, _ = np.histogram(ev_t[ev_kind == 2], bins=bins)
        res['contact_rate_series'] = (ccont / denom).tolist()
        res['pop_series'] = pop_series
        res['kick_rate_series'] = (cnt / denom).tolist()
        res['kick_rate_first10'] = float(np.mean(cnt[:10]) / denom)
        res['kick_rate_last20pct'] = float(np.mean(cnt[int(0.8 * len(cnt)):]) / denom)
        # Allan factor on kick series for several windows (in orbits)
        af = {}
        for w in (0.25, 0.5, 1.0, 2.0, 4.0, 8.0):
            bw = w * TWOPI
            nb2 = int(t // bw)
            if nb2 < 8: continue
            c2, _ = np.histogram(kicks, bins=np.arange(0, (nb2 + 1) * bw, bw))
            mu = c2.mean()
            af[f'{w}'] = float(c2.var() / mu) if mu > 0 else float('nan')
        res['allan'] = af
        # branching proxy: extra events touching i or j within W after an event, vs time-shifted baseline
        WIN = 0.4 * TWOPI
        touch = {}
        for tt, ii, jj in zip(ev_t, ev_i, ev_j):
            touch.setdefault(ii, []).append(tt); touch.setdefault(jj, []).append(tt)
        def count_after(tt, ii, jj):
            c = 0
            for b in (ii, jj):
                arr = touch.get(b)
                if arr is None: continue
                lo = np.searchsorted(arr, tt + 1e-9); hi = np.searchsorted(arr, tt + WIN)
                c += hi - lo
            return c
        idxs = np.arange(0, len(ev_t), max(1, len(ev_t) // 400))
        post = np.mean([count_after(ev_t[k], ev_i[k], ev_j[k]) for k in idxs]) if len(idxs) else 0.0
        base_counts = []
        for _ in range(300):
            k = rng.randrange(len(ev_t))
            sh = rng.uniform(0, t)
            base_counts.append(count_after(sh, ev_i[k], ev_j[k]))
        base = float(np.mean(base_counts)) if base_counts else 0.0
        res['branch_proxy_post'] = float(post); res['branch_proxy_base'] = base
        # element diffusion: needs kick dv series -> proxy via quantum crossings and kick stats
        res['dv_median'] = float(np.median([d for d in ev_dv if d > 0])) if np.any(np.array(ev_dv) > 0) else 0.0
    else:
        res['kick_rate_series'] = []; res['contact_rate_series'] = []; res['pop_series'] = pop_series
    # quantum crossing rates per body per orbit (setup-certificate churn)
    nbody_orbits = max(1.0, args.N) * max(orbits_done, 1e-9)
    res['cross_rate'] = {str(m): cross[m] / nbody_orbits for m in GRIDS}
    # work proxy: crossings x degree vs real encounter rate
    enc_rate = res.get('kick_rate_last20pct', 0.0)
    res['setup_work_vs_enc_m16'] = (cross[16] / nbody_orbits) * degree / max(enc_rate, 1e-12)
    res['setup_work_vs_enc_m8'] = (cross[8] / nbody_orbits) * degree / max(enc_rate, 1e-12)
    # final eccentricity stats (stirring check)
    if alive:
        res['e_rms_final'] = float(np.sqrt(np.mean([EE[i] ** 2 for i in alive])))
        res['e_rms_initial'] = float(args.sigma_e)
    while len(pop_series) < int(t / TWOPI):
        pop_series.append(alive_count)
    with open(args.out, 'w') as f:
        json.dump(res, f, indent=1)
    if args.dump:
        np.savez(args.dump, t=ev_t, i=ev_i, j=ev_j, kind=ev_kind,
                 p=np.array([P[k] for k in alive]), e=np.array([EE[k] for k in alive]),
                 w=np.array([W[k] for k in alive]), ids=np.array(alive))
    print(json.dumps({k: v for k, v in res.items() if k != 'kick_rate_series'}, indent=1))

if __name__ == '__main__':
    main()
