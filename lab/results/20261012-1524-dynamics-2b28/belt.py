#!/usr/bin/env python3
"""Event-driven conjunction-impulse belt (dynamics lens, run 20261012-1524).

Planar Kepler belt around one central mass (GM=1). Bodies interact ONLY
through impulsive two-body scattering at conjunctions (miss distance < b).
No ticks: conjunction times come from mean longitudes (exact circle
rotation, like law.md's Binet-cone circle rotation), miss distance refined
locally by parabolic fit. A kick on a body forces recomputation of the next
conjunction time of every partner pair -> that is the engine's "re-pay".

Measures: encounter-rate feedback vs a no-feedback control, stirring <e^2>(t),
re-pay ops, frame burstiness, N scaling. Deterministic by seed.

Usage: python3 belt.py --N 512 --T 1500 --mu 1e-6 --seed 3 --out run.json
"""
import numpy as np, heapq, argparse, json, math, time, sys

TWOPI = 2.0 * np.pi

def solve_kepler(M, e):
    M = M % TWOPI
    E = M + e * np.sin(M)
    for _ in range(12):
        f = E - e * np.sin(E) - M
        d = f / (1.0 - e * np.cos(E))
        E = E - d
        if np.max(np.abs(d)) < 1e-13:
            break
    return E

def states(a, e, M, w):
    """Positions/velocities for arrays of elements at common-ish epochs.
    a,e,w scalar-or-array broadcast with M array -> returns x,y,vx,vy."""
    E = solve_kepler(M, e)
    sa, ca = np.sin(w), np.cos(w)
    xo = a * (np.cos(E) - e)
    yo = a * np.sqrt(1.0 - e * e) * np.sin(E)
    f = a ** -0.5 / (1.0 - e * np.cos(E))
    vxo = -f * np.sin(E)
    vyo = f * np.sqrt(1.0 - e * e) * np.cos(E)
    x = ca * xo - sa * yo
    y = sa * xo + ca * yo
    vx = ca * vxo - sa * vyo
    vy = sa * vxo + ca * vyo
    return x, y, vx, vy

def state_to_elem(x, y, vx, vy, t_now):
    r = math.hypot(x, y)
    v2 = vx * vx + vy * vy
    rv = x * vx + y * vy
    energy = 0.5 * v2 - 1.0 / r
    a = -0.5 / energy
    evx = (v2 - 1.0 / r) * x - rv * vx
    evy = (v2 - 1.0 / r) * y - rv * vy
    e = math.hypot(evx, evy)
    if e < 1e-12:
        w = math.atan2(y, x)
        M0 = 0.0
    else:
        w = math.atan2(evy, evx)
        cw, sw = math.cos(w), math.sin(w)
        xo = cw * x + sw * y
        yo = -sw * x + cw * y
        E = math.atan2(yo / (a * math.sqrt(max(1.0 - e * e, 1e-18))), xo / a + e)
        M0 = E - e * math.sin(E)
    return a, e, M0 % TWOPI, w % TWOPI, a ** -1.5, t_now

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, default=512)
    ap.add_argument("--W", type=float, default=0.08)       # belt half-width in a
    ap.add_argument("--sig_e", type=float, default=0.02)
    ap.add_argument("--b", type=float, default=2e-3)       # encounter radius
    ap.add_argument("--mu", type=float, default=1e-7)      # body mass (GM central = 1)
    ap.add_argument("--T", type=float, default=1500.0)     # run length (orbits at a=1)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--nokick", action="store_true")       # control: zero impulses
    ap.add_argument("--formation", type=str, default="")   # "", "aligned", "random"
    ap.add_argument("--fda", type=float, default=3e-3)     # formation rank spacing in a
    ap.add_argument("--fsige", type=float, default=3e-3)
    ap.add_argument("--fb", type=float, default=1.5e-3)
    ap.add_argument("--out", type=str, required=True)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    t_start = time.time()

    # ---- init ----
    if args.formation:
        N = args.N
        a = 1.0 + (np.arange(N) - (N - 1) / 2.0) * args.fda
        e = rng.rayleigh(args.fsige, N)
        w = rng.uniform(0, TWOPI, N)
        if args.formation == "aligned":
            M0 = np.full(N, rng.uniform(0, TWOPI))
        else:
            M0 = rng.uniform(0, TWOPI, N)
        b = args.fb
    else:
        N = args.N
        a = 1.0 + rng.uniform(-args.W / 2, args.W / 2, N)
        e = rng.rayleigh(args.sig_e, N)
        w = rng.uniform(0, TWOPI, N)
        M0 = rng.uniform(0, TWOPI, N)
        b = args.b
    a = np.ascontiguousarray(a); e = np.ascontiguousarray(e)
    w = np.ascontiguousarray(w); M0 = np.ascontiguousarray(M0)
    t0 = np.zeros(N)
    n = a ** -1.5
    alive = np.ones(N, bool)
    mass = np.full(N, args.mu)

    # ---- pairs: orbit-overlap candidates with growth margin ----
    order = np.argsort(a)
    asort = a[order]
    margin = 1.3 * (e.max() + np.quantile(e, 0.98)) + 8.0 * b
    ia_l, ib_l = [], []
    for pos in range(N):
        i = order[pos]
        lo = np.searchsorted(asort, a[i] - margin, "left")
        hi = np.searchsorted(asort, a[i] + margin, "right")
        for q in range(lo, hi):
            j = order[q]
            if j > i and abs(a[i] - a[j]) <= 1.3 * (e[i] + e[j]) + 8.0 * b:
                ia_l.append(i); ib_l.append(j)
    ia = np.array(ia_l, dtype=np.int64); ib = np.array(ib_l, dtype=np.int64)
    P = len(ia)
    TSYN = TWOPI / np.maximum(np.abs(n[ia] - n[ib]), 1e-15)

    dn_eps = TWOPI / max(args.T, 1.0)   # pairs with synodic period > T never meet
    current = np.full(P, np.inf)

    def conj_time(pid, t_ref):
        i, j = ia[pid], ib[pid]
        if not (alive[i] and alive[j]):
            return np.inf
        dni = n[i] - n[j]
        if abs(dni) < dn_eps:
            return np.inf
        lam_i = w[i] + M0[i] + n[i] * (t_ref - t0[i])
        lam_j = w[j] + M0[j] + n[j] * (t_ref - t0[j])
        dl = (lam_i - lam_j) % TWOPI
        t = t_ref + ((TWOPI - dl) / dni if dni > 0 else dl / (-dni))
        return t if t > t_ref else t_ref + TWOPI / abs(dni)

    dn_all = n[ia] - n[ib]
    dl_all = ((w[ia] + M0[ia]) - (w[ib] + M0[ib])) % TWOPI
    with np.errstate(divide="ignore", invalid="ignore"):
        t_all = np.where(dn_all > 0, (TWOPI - dl_all) / dn_all,
                         np.where(dn_all < 0, dl_all / (-dn_all), np.inf))
    t_all = np.where(np.abs(dn_all) >= dn_eps, t_all, np.inf)
    t_all = np.where(t_all <= args.T, t_all, np.inf)
    current = t_all.copy()
    heap = [(float(t), int(p)) for p, t in enumerate(t_all) if np.isfinite(t)]
    heapq.heapify(heap)
    partners = [[] for _ in range(N)]
    for pid in range(P):
        partners[ia[pid]].append(pid)
        partners[ib[pid]].append(pid)
    degree = np.array([len(p) for p in partners], float)

    # ---- accounting ----
    n_orb = int(math.ceil(args.T)) + 2
    conj_hist = np.zeros(n_orb)          # conjunctions per orbit
    enc_hist = np.zeros(n_orb)           # encounters per orbit
    enc_fine = []                        # encounter times (for bursts)
    enc_de = []                          # kick sizes |delta e| per encounter body
    enc_R = []                           # board regime number U/sqrt(mu_p/b)
    repay_ops = 0
    kicks = 0
    deaths = 0
    e_curve_t, e_curve_v = [], []
    CH = 256

    def sample_e(t):
        e_curve_t.append(t)
        e_curve_v.append(float(np.mean(e[alive] ** 2)))

    def apply_encounter(pid, t):
        nonlocal repay_ops, kicks, deaths
        i, j = ia[pid], ib[pid]
        xi, yi, vxi, vyi = states(a[i], e[i], M0[i] + n[i] * (t - t0[i]), w[i])
        xj, yj, vxj, vyj = states(a[j], e[j], M0[j] + n[j] * (t - t0[j]), w[j])
        dx, dy = xi - xj, yi - yj
        d = math.hypot(dx, dy)
        dvx, dvy = vxi - vxj, vyi - vyj
        vrel = math.hypot(dvx, dvy)
        vrel = max(vrel, 1e-9)
        mu_p = mass[i] + mass[j]
        dv_rel = 2.0 * vrel / (1.0 + d * vrel * vrel / mu_p)  # exact hyperbolic
        sgn = 1.0 if (dvx * dy - dvy * dx) >= 0 else -1.0
        wx_, wy_ = -sgn * dvy / vrel, sgn * dvx / vrel        # perp to v_rel
        if not args.nokick and dv_rel > 0.0:
            fi = mass[j] / mu_p; fj = mass[i] / mu_p
            vxi += fi * dv_rel * wx_; vyi += fi * dv_rel * wy_
            vxj -= fj * dv_rel * wx_; vyj -= fj * dv_rel * wy_
        enc_R.append(vrel * math.sqrt(b / mu_p))
        if args.nokick:
            kicks += 1
            return
        for (xx, yy, vx, vy, idx) in ((xi, yi, vxi, vyi, i), (xj, yj, vxj, vyj, j)):
            e_old = e[idx]
            na, ne, nM0, nw, nn, nt0 = state_to_elem(xx, yy, vx, vy, t)
            if ne >= 0.99 or na <= 0 or na > 10.0:
                alive[idx] = False; deaths += 1
                a[idx], e[idx] = na, ne; M0[idx], w[idx] = nM0, nw
                n[idx], t0[idx] = nn, nt0
            else:
                a[idx], e[idx] = na, ne; M0[idx], w[idx] = nM0, nw
                n[idx], t0[idx] = nn, nt0
            enc_de.append(abs(ne - e_old))
        kicks += 1
        # re-pay: reschedule every pair of both bodies
        for body in (i, j):
            for q in partners[body]:
                if not alive[ia[q]] or not alive[ib[q]]:
                    if current[q] != np.inf:
                        current[q] = np.inf
                        heapq.heappush(heap, (np.inf, q))
                    continue
                tq = conj_time(q, t)
                current[q] = tq
                if tq <= args.T:
                    heapq.heappush(heap, (tq, q))
            repay_ops += len(partners[body])

    t_sim = 0.0
    next_sample = 0.0
    it_guard = 0
    while heap and t_sim < args.T:
        it_guard += 1
        if it_guard > 200_000_000:
            break
        chunk = []
        while heap and len(chunk) < CH and heap[0][0] <= args.T:
            t, pid = heapq.heappop(heap)
            if t != current[pid]:
                continue
            chunk.append((t, pid))
        if not chunk:
            break
        cts = np.array([c[0] for c in chunk])
        cia, cib = ia[[c[1] for c in chunk]], ib[[c[1] for c in chunk]]
        Ma = M0[cia] + n[cia] * (cts - t0[cia])
        Mb = M0[cib] + n[cib] * (cts - t0[cib])
        xa, ya, _, _ = states(a[cia], e[cia], Ma, w[cia])
        xb, yb, _, _ = states(a[cib], e[cib], Mb, w[cib])
        d0 = np.hypot(xa - xb, ya - yb)
        # parabolic refinement of separation^2 around t_c
        del_ = 0.75 * (e[cia] + e[cib]) / np.maximum(n[cia], n[cib])
        del_ = np.minimum(del_, 0.4)
        def sep2(tt):
            Ma2 = M0[cia] + n[cia] * (tt - t0[cia])
            Mb2 = M0[cib] + n[cib] * (tt - t0[cib])
            xa2, ya2, _, _ = states(a[cia], e[cia], Ma2, w[cia])
            xb2, yb2, _, _ = states(a[cib], e[cib], Mb2, w[cib])
            return (xa2 - xb2) ** 2 + (ya2 - yb2) ** 2
        s_m = sep2(cts - del_)
        s_0 = (xa - xb) ** 2 + (ya - yb) ** 2
        s_p = sep2(cts + del_)
        denom = s_m - 2.0 * s_0 + s_p
        shift = np.where(np.abs(denom) > 1e-30,
                         -0.5 * del_ * (s_p - s_m) / np.where(np.abs(denom) > 1e-30, denom, 1.0),
                         0.0)
        shift = np.clip(shift, -del_, del_)
        t_star = cts + shift
        Ma3 = M0[cia] + n[cia] * (t_star - t0[cia])
        Mb3 = M0[cib] + n[cib] * (t_star - t0[cib])
        xa3, ya3, _, _ = states(a[cia], e[cia], Ma3, w[cia])
        xb3, yb3, _, _ = states(a[cib], e[cib], Mb3, w[cib])
        dmin = np.hypot(xa3 - xb3, ya3 - yb3)
        enc_mask = dmin < b
        if not enc_mask.any():
            oi = (cts // 1).astype(int)
            np.add.at(conj_hist, oi, 1)
            t_sim = chunk[-1][0]
            # reschedule next conjunction: exactly one synodic period later
            for q in range(len(chunk)):
                pid2 = chunk[q][1]
                tn = chunk[q][0] + TSYN[pid2]
                if tn <= args.T:
                    current[pid2] = tn
                    heapq.heappush(heap, (tn, pid2))
        else:
            k = int(np.argmax(enc_mask))
            for q in range(k):
                oi = int(chunk[q][0] // 1)
                conj_hist[oi] += 1
                tn = chunk[q][0] + TSYN[chunk[q][1]]
                if tn <= args.T:
                    current[chunk[q][1]] = tn
                    heapq.heappush(heap, (tn, chunk[q][1]))
            oi = int(chunk[k][0] // 1)
            conj_hist[oi] += 1; enc_hist[oi] += 1
            enc_fine.append(chunk[k][0])
            t_enc, pid_enc = chunk[k]
            apply_encounter(pid_enc, t_enc)
            if args.nokick:
                tn = t_enc + TSYN[pid_enc]
                if tn <= args.T:
                    current[pid_enc] = tn
                    heapq.heappush(heap, (tn, pid_enc))
            t_sim = t_enc
            for q in range(k + 1, len(chunk)):
                t2, pid2 = chunk[q]
                if t2 != current[pid2]:
                    continue
                heapq.heappush(heap, (t2, pid2))
        while next_sample <= t_sim:
            sample_e(next_sample)
            next_sample += 25.0
    sample_e(args.T)

    et = np.array(enc_fine)
    live = alive.sum()
    out = {
        "cfg": {k: getattr(args, k) for k in
                ["N", "W", "sig_e", "b", "mu", "T", "seed", "nokick",
                 "formation", "fda", "fsige", "fb"]},
        "pairs": int(P), "alive": int(live), "deaths": int(deaths),
        "conjunctions": int(conj_hist.sum()), "encounters": int(enc_hist.sum()),
        "repay_ops": int(repay_ops), "kicks": int(kicks),
        "wall_s": round(time.time() - t_start, 2),
        "degree_mean": float(degree.mean()), "degree_max": int(degree.max()),
        "conj_hist": conj_hist[: int(args.T) + 1].tolist(),
        "enc_hist": enc_hist[: int(args.T) + 1].tolist(),
        "enc_times": et.tolist(),
        "e2_curve_t": e_curve_t, "e2_curve_v": e_curve_v,
        "enc_R": enc_R, "enc_de": enc_de,
    }
    with open(args.out, "w") as f:
        json.dump(out, f)
    print(f"[{args.out}] N={args.N} mu={args.mu:g} nokick={args.nokick} "
          f"form={args.formation or '-'} seed={args.seed} "
          f"conj={out['conjunctions']} enc={out['encounters']} "
          f"repay={repay_ops} e2: {e_curve_v[0]:.3e}->{e_curve_v[-1]:.3e} "
          f"deaths={deaths} wall={out['wall_s']}s")

if __name__ == "__main__":
    main()
