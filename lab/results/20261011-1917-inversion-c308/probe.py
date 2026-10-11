#!/usr/bin/env python3
"""Inversion probe: does the phase-neighbour certificate (gold 20261006-0346-taleb-09b5,
"every real encounter lies within partner rank 4 along the orbit", being built as
b-coorbital-cert at O(n*k), k~4) survive its own scene family as n, cadence H and
eccentricity spread scale?

Model: in-plane Kepler, a ~ U(1-W/2, 1+W/2), phases uniform, mean motion a^-3/2 rev/orbit.
Truth is exact:
  circular  - a close approach requires equal longitude; conjunction times are closed form
              (|dn|*win < 1 in every scene, so at most one per pair per window); conjunction
              distance == |da| exactly.
  eccentric - close approaches happen at track crossings (or quasi-crossings) whose longitudes
              solve a*D + e*(...) = 0, a linear equation in (cos th, sin th) (the Binet cone);
              each body's passage times through a crossing longitude are closed form via the
              inverse Kepler map; an encounter is a co-passage within (rho - s0)/|dv|.
Certificate model: partner rank in the sorted ring at the last derivation before the
encounter, derivations at cadence H (per-orbit is the most favorable reading of O(n*k) per
evaluation; q-candidate-degree's goal is lazier). Both sort coordinates are scored for
eccentric scenes: mean longitude (the cheap phase element) and true longitude (position).
Continuous variant is scored by its cost: expected conjunctions per real encounter.
"""
import json
import sys
import time

import numpy as np

SEED = 20261011
TWO_PI = 2.0 * np.pi


def kepler_E(M, e, iters=4):
    """Eccentric anomaly from mean anomaly (rad), vectorised Newton. e <= 0.1."""
    E = M.copy()
    for _ in range(iters):
        E = E - (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    return E


def positions(a, e, varpi, M0, nrev, t):
    """True radius and polar angle at time t (orbits). M0 is the mean anomaly."""
    if e == 0.0:
        th = (varpi + M0 + TWO_PI * nrev * t) % TWO_PI
        return np.full_like(np.asarray(th, float), 0.0) + a, th
    M = (M0 + TWO_PI * nrev * t) % TWO_PI
    E = kepler_E(M, e)
    nu = 2.0 * np.arctan2(np.sqrt(1.0 + e) * np.sin(E / 2.0),
                          np.sqrt(1.0 - e) * np.cos(E / 2.0))
    r = a * (1.0 - e * np.cos(E))
    return r, varpi + nu


def circ_events_circular(a, lam0, nrev, rho, win, chunk=2_000_000):
    """All conjunction events of pairs with |da| < rho, circular orbits.
    Returns (pi, pj, te). Every such event IS an encounter (distance == |da| < rho)."""
    n = len(a)
    order = np.argsort(a)
    a_s = a[order]
    hi = np.searchsorted(a_s, a_s + rho, side="right") - 1  # last partner within rho ahead
    cnt = np.maximum(hi - np.arange(n), 0)
    out_i, out_j, out_t = [], [], []
    s = 0
    while s < n:
        csum = np.cumsum(cnt[s:])
        e_rel = int(np.searchsorted(csum, chunk, side="right"))
        e_rel = max(1, min(e_rel, n - s))
        e_ = s + e_rel
        c = cnt[s:e_]
        if c.sum() > 0:
            ii = np.repeat(np.arange(s, e_, dtype=np.int64), c)
            base = np.cumsum(c) - c
            offs = np.arange(int(c.sum())) - np.repeat(base, c)
            jj = ii + 1 + offs
            ai, aj = a_s[ii], a_s[jj]
            dn = ai ** -1.5 - aj ** -1.5
            dl0 = (lam0[order[ii]] - lam0[order[jj]]) % 1.0
            # first mean-longitude crossing in (0, inf): dn>0 at k=1, dn<0 at k=0
            t = np.where(dn > 0, (1.0 - dl0) / dn, (-dl0) / dn)
            ok = (dn != 0) & (t > 0) & (t <= win)
            if ok.any():
                out_i.append(order[ii][ok])
                out_j.append(order[jj][ok])
                out_t.append(t[ok])
            del ii, jj, ai, aj, dn, dl0, t, ok, offs, base
        s = e_
    if not out_i:
        return (np.array([], np.int64),) * 2 + (np.array([]),)
    return np.concatenate(out_i), np.concatenate(out_j), np.concatenate(out_t)


def expected_conjunctions(a, win):
    """E[# conjunctions in window over ALL n(n-1)/2 pairs] = sum|dn| * win,
    exact for the sample: sum_{i<j}|b_i-b_j| via sorted prefix sums, b = a^-1.5."""
    b = np.sort(a ** -1.5)
    n = len(a)
    k = np.arange(n)
    return float(np.sum(b * (2.0 * k - n + 1.0)) * win)


def rank_report(n, lamfun, pi, pj, te, H, win):
    """Distribution of partner rank in the ring (sorted by lamfun(t), revolutions
    mod 1) at the last derivation before each encounter.
    Derivations at t = 0, H, 2H, ... <= win."""
    if len(te) == 0:
        return dict(events=0)
    nevals = int(np.floor(win / H)) + 1
    idx = np.minimum((te / H).astype(np.int64), nevals - 1)
    so = np.argsort(idx, kind="stable")
    idx_s = idx[so]
    pi_s, pj_s = pi[so], pj[so]
    ranks = np.empty(len(te), np.int64)
    lo = 0
    while lo < len(te):
        e = idx_s[lo]
        hi_ = np.searchsorted(idx_s, e, side="right")
        lam = lamfun(e * H)
        pos = np.empty(n, np.int64)
        pos[np.argsort(lam, kind="stable")] = np.arange(n)
        p0 = pos[pi_s[lo:hi_]]
        p1 = pos[pj_s[lo:hi_]]
        d = np.abs(p0 - p1)
        ranks[lo:hi_] = np.minimum(d, n - d)
        lo = hi_
    r = np.sort(ranks)
    miss4 = float(np.mean(r > 4))
    p99 = int(np.quantile(r, 0.99, method="higher"))
    k1 = int(r[max(0, len(r) - 1 - int(np.ceil(0.01 * len(r))))])  # smallest k with miss<=1%
    return dict(events=int(len(te)), miss4=miss4, rank_p99=p99, k_1pct=k1,
                rank_max=int(r[-1]))


def scene_circular(name, n, rho, W, H, win, fine=20, seed=SEED):
    rng = np.random.default_rng(seed)
    a = 1.0 + rng.uniform(-W / 2.0, W / 2.0, n)
    lam0 = rng.uniform(0.0, 1.0, n)
    nrev = a ** -1.5
    t0 = time.time()
    pi, pj, te = circ_events_circular(a, lam0, nrev, rho, win)
    enc = len(te)
    conj = expected_conjunctions(a, win)
    lamfun = lambda t: (lam0 + nrev * t) % 1.0
    res = dict(scene=name, kind="circular", n=n, rho=rho, W=W, e=0.0, H=H, win=win,
               events=enc, encounters=enc,
               kstar_law=1.5 * n * H * rho,
               conj_per_enc=conj / enc if enc else None)
    res["cadence_H"] = rank_report(n, lamfun, pi, pj, te, H, win)
    res["cadence_H_over_%d" % fine] = rank_report(n, lamfun, pi, pj, te, H / fine, win)
    res["seconds"] = round(time.time() - t0, 2)
    return res


# ---------------- eccentric scenes: crossing machinery ----------------

def ecc_events_for_pairs(i, j, a, e, varpi, M0, nrev, rho, win):
    """Encounter events for the given pair index arrays: (ev_i, ev_j, ev_t).
    Crossings (and quasi-crossings) are exact; co-passage times are closed form."""
    T = 1.0 / nrev
    ai, aj = a[i], a[j]
    wi, wj = varpi[i], varpi[j]
    D = ai - aj
    P = e * (ai * np.cos(wj) - aj * np.cos(wi))
    Q = e * (ai * np.sin(wj) - aj * np.sin(wi))
    R = np.hypot(P, Q)
    phi = np.arctan2(Q, P)
    cross = np.abs(D) <= R
    arg = np.clip(-D / np.where(R > 0, R, 1.0), -1.0, 1.0)
    ac = np.arccos(arg)
    th1 = phi + ac
    th2 = phi - ac
    thq = phi + np.where(D > 0, np.pi, 0.0)          # min-separation longitude, no crossing
    TH = np.where(cross[:, None], np.stack([th1, th2], axis=1), thq[:, None])
    keep_row = np.stack([np.ones(len(i), bool), cross], axis=1)
    I = np.repeat(i, 2)[keep_row.ravel()]
    J = np.repeat(j, 2)[keep_row.ravel()]
    THf = TH.ravel()[keep_row.ravel()]

    def E_at(ks, th):
        f = (th - varpi[ks] + np.pi) % TWO_PI - np.pi
        return 2.0 * np.arctan2(np.sqrt(1.0 - e) * np.sin(f / 2.0),
                                np.sqrt(1.0 + e) * np.cos(f / 2.0))

    Ei = E_at(I, THf)
    Ej = E_at(J, THf)
    ri = a[I] * (1.0 - e * np.cos(Ei))
    rj = a[J] * (1.0 - e * np.cos(Ej))
    s0 = np.abs(ri - rj)                              # exact separation at the longitude
    sel = s0 < rho
    if not sel.any():
        return (np.array([], np.int64),) * 2 + (np.array([]),)
    I, J, THf, Ei, Ej, s0 = I[sel], J[sel], THf[sel], Ei[sel], Ej[sel], s0[sel]
    Mi = Ei - e * np.sin(Ei)
    Mj = Ej - e * np.sin(Ej)
    ti0 = ((Mi - M0[I]) / (TWO_PI * nrev[I])) % T[I]   # first passage through THf
    tj0 = ((Mj - M0[J]) / (TWO_PI * nrev[J])) % T[J]
    eps = 1e-3

    def vel(ks, ts):
        r1, t1 = positions(a[ks], e, varpi[ks], M0[ks], nrev[ks], ts - eps)
        r2, t2 = positions(a[ks], e, varpi[ks], M0[ks], nrev[ks], ts + eps)
        return np.stack([r2 * np.cos(t2) - r1 * np.cos(t1),
                         r2 * np.sin(t2) - r1 * np.sin(t1)], axis=1) / (2 * eps)

    vi = vel(I, ti0)
    vj = vel(J, tj0)
    dv = np.linalg.norm(vi - vj, axis=1)
    crs = np.abs(vi[:, 0] * vj[:, 1] - vi[:, 1] * vj[:, 0])
    v_eff = crs / np.maximum(dv, 1e-12)   # flyby miss distance ~ |o| * v_eff (along-track)
    w_t = np.sqrt(np.maximum(rho * rho - s0 * s0, 0.0)) / np.maximum(v_eff, 1e-12)

    mmax = int(np.ceil(win)) + 2
    mm = np.arange(mmax + 1)
    tim = ti0[:, None] + mm[None, :] * T[I][:, None]
    lj = np.rint((tim - tj0[:, None]) / T[J][:, None])
    tj = tj0[:, None] + lj * T[J][:, None]
    o = tim - tj
    aom = np.abs(o)
    tev = 0.5 * (tim + tj)
    ok = (aom <= w_t[:, None]) & (tev > 0) & (tev <= win)
    big = np.full(aom.shape, np.inf)
    prev = np.concatenate([big[:, :1], aom[:, :-1]], axis=1)
    nxt = np.concatenate([aom[:, 1:], big[:, :1]], axis=1)
    ok &= (aom < prev) & (aom <= nxt)                  # one event per cluster
    rr, cc = np.nonzero(ok)
    if len(rr) == 0:
        return (np.array([], np.int64),) * 2 + (np.array([]),)
    return I[rr], J[rr], tev[rr, cc]


def brute_events_for_pairs(i, j, a, e, varpi, M0, nrev, rho, win,
                           coarse=0.005, fine=2e-4):
    """Independent truth on a small pair sample: coarse distance scan, refined locally."""
    out_i, out_j, out_t = [], [], []
    for k in range(len(i)):
        ii, jj = i[k], j[k]
        tc = np.arange(0.0, win, coarse)
        r1, t1 = positions(a[ii], e, varpi[ii], M0[ii], nrev[ii], tc)
        r2, t2 = positions(a[jj], e, varpi[jj], M0[jj], nrev[jj], tc)
        d = np.sqrt(r1 * r1 + r2 * r2 - 2 * r1 * r2 * np.cos(t1 - t2))
        cand = np.nonzero(d < 2 * rho)[0]
        if len(cand) == 0:
            continue
        breaks = np.nonzero(np.diff(cand) > 1)[0]
        starts = np.concatenate([[cand[0]], cand[breaks + 1]])
        ends = np.concatenate([cand[breaks], [cand[-1]]])
        for s_, e_ in zip(starts, ends):
            lo = max(0.0, tc[s_] - 2 * coarse)
            hi = min(win, tc[e_] + 2 * coarse)
            tf = np.arange(lo, hi, fine)
            if len(tf) < 3:
                continue
            r1, t1 = positions(a[ii], e, varpi[ii], M0[ii], nrev[ii], tf)
            r2, t2 = positions(a[jj], e, varpi[jj], M0[jj], nrev[jj], tf)
            df = np.sqrt(r1 * r1 + r2 * r2 - 2 * r1 * r2 * np.cos(t1 - t2))
            loc = np.nonzero((df[1:-1] < df[:-2]) & (df[1:-1] <= df[2:]) &
                             (df[1:-1] < rho))[0] + 1
            for L in loc:
                out_i.append(ii)
                out_j.append(jj)
                out_t.append(tf[L])
    return np.array(out_i, np.int64), np.array(out_j, np.int64), np.array(out_t)

def align_scan_events(i, j, a, e, varpi, M0, nrev, rho, win, step=0.05, block=500):
    """Independent event generator: roots of the true-longitude difference
    (alignments) by sign change + linear interp + Newton polish, kept when the
    pair distance at the alignment is below rho. Vectorised over pair blocks."""
    tg = np.arange(0.0, win + step, step)
    out_i, out_j, out_t = [], [], []
    for s in range(0, len(i), block):
        I = i[s:s + block]
        J = j[s:s + block]
        nb = len(I)
        th = np.empty((nb, len(tg)))
        for x, k in enumerate(I):
            _, t_ = positions(a[k], e, varpi[k], M0[k], nrev[k], tg)
            th[x] = t_
        for x, k in enumerate(J):
            _, t_ = positions(a[k], e, varpi[k], M0[k], nrev[k], tg)
            th[x] -= t_
        dth = (th + np.pi) % TWO_PI - np.pi
        sg = np.sign(dth)
        ch = sg[:, 1:] * sg[:, :-1] < 0
        pr, pt = np.nonzero(ch)
        if len(pr) == 0:
            continue
        t1 = tg[pt]
        t2 = tg[pt + 1]
        d1 = dth[:, :-1][pr, pt]
        d2 = dth[:, 1:][pr, pt]
        tr = t1 - d1 * (t2 - t1) / (d2 - d1)                      # linear interp root
        II, JJ = I[pr], J[pr]
        for _ in range(4):                                        # Newton polish
            _, ti = positions(a[II], e, varpi[II], M0[II], nrev[II], tr)
            _, tj = positions(a[JJ], e, varpi[JJ], M0[JJ], nrev[JJ], tr)
            f = (ti - tj + np.pi) % TWO_PI - np.pi
            _, tip = positions(a[II], e, varpi[II], M0[II], nrev[II], tr + 1e-4)
            _, tjp = positions(a[JJ], e, varpi[JJ], M0[JJ], nrev[JJ], tr + 1e-4)
            fp = (tip - tjp + np.pi) % TWO_PI - np.pi
            dfd = (fp - f) / 1e-4
            tr = tr - f / np.where(np.abs(dfd) > 1e-9, dfd, 1e-9)
        keep = (tr > 0) & (tr <= win)
        II, JJ, tr = II[keep], JJ[keep], tr[keep]
        if len(II) == 0:
            continue
        ri, ti = positions(a[II], e, varpi[II], M0[II], nrev[II], tr)
        rj, tj = positions(a[JJ], e, varpi[JJ], M0[JJ], nrev[JJ], tr)
        d = np.sqrt(ri * ri + rj * rj - 2 * ri * rj * np.cos(ti - tj))
        ok = d < rho
        if ok.any():
            out_i.append(II[ok]); out_j.append(JJ[ok]); out_t.append(tr[ok])
    if not out_i:
        return (np.array([], np.int64),) * 2 + (np.array([]),)
    return np.concatenate(out_i), np.concatenate(out_j), np.concatenate(out_t)


def scene_eccentric(name, n, rho, W, e, H, win, fine=20, seed=SEED,
                    npairs=2_000_000, chunk=150_000, nval=300):
    rng = np.random.default_rng(seed)
    a = 1.0 + rng.uniform(-W / 2.0, W / 2.0, n)
    varpi = rng.uniform(0.0, TWO_PI, n)
    M0 = rng.uniform(0.0, TWO_PI, n)
    nrev = a ** -1.5
    t0 = time.time()
    nsamp = int(npairs * 1.06)
    si = rng.integers(0, n, nsamp)
    sj = rng.integers(0, n, nsamp)
    m = si != sj
    si, sj = si[m][:npairs], sj[m][:npairs]
    ev_i, ev_j, ev_t = [], [], []
    for s in range(0, len(si), chunk):
        ev = ecc_events_for_pairs(si[s:s + chunk], sj[s:s + chunk],
                                  a, e, varpi, M0, nrev, rho, win)
        if len(ev[0]):
            ev_i.append(ev[0]); ev_j.append(ev[1]); ev_t.append(ev[2])
    pi = np.concatenate(ev_i) if ev_i else np.array([], np.int64)
    pj = np.concatenate(ev_j) if ev_j else np.array([], np.int64)
    te = np.concatenate(ev_t) if ev_t else np.array([])
    enc = len(te)
    # population extrapolation: sampled pairs -> whole ring
    scale = n * (n - 1) / (2.0 * len(si))
    enc_total = enc * scale
    per_body_orbit = 2.0 * enc_total / n / win
    # soundness spot-check at the real (thin) threshold: distance at t_e on a sample
    snd = None
    if enc > 0:
        sidx = rng.choice(enc, min(300, enc), replace=False)
        dmin = []
        for x in sidx:
            I, J, t = int(pi[x]), int(pj[x]), float(te[x])
            tf = t + np.array([0.0, 1e-4, -1e-4, 3e-4, -3e-4])
            r1, t1 = positions(a[I], e, varpi[I], M0[I], nrev[I], tf)
            r2, t2 = positions(a[J], e, varpi[J], M0[J], nrev[J], tf)
            dmin.append(float(np.min(np.sqrt(r1 * r1 + r2 * r2 - 2 * r1 * r2 * np.cos(t1 - t2)))))
        dmin = np.array(dmin)
        snd = dict(sample=len(dmin), frac_below_rho=float(np.mean(dmin < rho)),
                   d_p50=float(np.median(dmin)))
    # validation vs an independent generator: alignment roots (true-longitude
    # difference zero crossings, Newton polished) on a fresh pair sample, at the
    # real threshold; the scanner also catches wide-arc alignments of
    # near-concentric pairs that the vertex machinery does not claim
    nscan = 20000
    vi = rng.integers(0, n, nscan * 2)
    vj = rng.integers(0, n, nscan * 2)
    mm_ = vi != vj
    vi, vj = vi[mm_][:nscan], vj[mm_][:nscan]
    mech = ecc_events_for_pairs(vi, vj, a, e, varpi, M0, nrev, rho, win)
    scan = align_scan_events(vi, vj, a, e, varpi, M0, nrev, rho, win)

    def count_matched(A, B):
        c = 0
        if len(A[0]) == 0 or len(B[0]) == 0:
            return 0
        for x in range(len(A[0])):
            hit = np.nonzero((A[0][x] == B[0]) & (A[1][x] == B[1]) &
                             (np.abs(A[2][x] - B[2]) < 3e-3))[0]
            c += 1 if len(hit) else 0
        return c

    matched = count_matched(mech, scan)
    matched_rev = count_matched(scan, mech)
    lam_mean = lambda t: ((varpi + M0) / TWO_PI + nrev * t) % 1.0

    def lam_true(t):
        _, th = positions(a, e, varpi, M0, nrev, np.full(n, t))
        return (th / TWO_PI) % 1.0

    reach = min(W, 2.0 * e)
    res = dict(scene=name, kind="eccentric", n=n, rho=rho, W=W, e=e, H=H, win=win,
               pairs_sampled=int(len(si)), encounters=enc,
               enc_per_body_per_orbit=per_body_orbit,
               reach=reach, kstar_law=1.5 * n * H * reach)
    res["rank_mean_H"] = rank_report(n, lam_mean, pi, pj, te, H, win)
    res["rank_true_H"] = rank_report(n, lam_true, pi, pj, te, H, win)
    res["rank_mean_H_over_%d" % fine] = rank_report(n, lam_mean, pi, pj, te, H / fine, win)
    res["rank_true_H_over_%d" % fine] = rank_report(n, lam_true, pi, pj, te, H / fine, win)
    # mean-rank AT the encounter (sample): the sort-coordinate mismatch
    if enc > 0:
        idx = rng.choice(enc, min(400, enc), replace=False)
        ranks_at = []
        for x in idx:
            lamt = lam_mean(te[x])
            d = np.abs((lamt - lamt[pi[x]] + 0.5) % 1.0 - 0.5)
            ranks_at.append(int(np.sum(d <= d[pj[x]]) - 1))
        ranks_at = np.sort(np.array(ranks_at))
        res["mean_rank_at_encounter"] = dict(
            p50=int(ranks_at[len(ranks_at) // 2]), p99=int(ranks_at[int(.99 * len(ranks_at))]),
            max=int(ranks_at[-1]))
    if snd:
        res["soundness"] = snd
    # composite population (all alignment events, incl. near-concentric wide-arc)
    res["rank_true_H_scan"] = rank_report(n, lam_true, scan[0], scan[1], scan[2], H, win)
    res["rank_mean_H_scan"] = rank_report(n, lam_mean, scan[0], scan[1], scan[2], H, win)
    res["validation"] = dict(pairs=nscan,
                             machinery_events=int(len(mech[0])),
                             scan_events=int(len(scan[0])),
                             matched=matched, matched_rev=matched_rev)
    res["seconds"] = round(time.time() - t0, 2)
    return res


def run_part(part):
    out = []
    if part in ("1", "all"):
        out.append(scene_circular("S0-control", 10_000, 1e-4, 2e-4, 1.0, 100, seed=SEED + 1))
        out.append(scene_circular("A1", 3_000, 3e-4, 3e-2, 1.0, 300, seed=SEED + 2))
        out.append(scene_circular("A2", 10_000, 3e-4, 3e-2, 1.0, 100, seed=SEED + 3))
        out.append(scene_circular("A3", 30_000, 3e-4, 3e-2, 1.0, 30, seed=SEED + 4))
        out.append(scene_circular("A4", 100_000, 3e-4, 3e-2, 1.0, 10, seed=SEED + 5))
    if part in ("2", "all"):
        out.append(scene_circular("B1-dense-ring", 10_000, 5e-4, 1e-3, 1.0, 30, seed=SEED + 9))
        out.append(scene_circular("C1-H0.25", 30_000, 3e-4, 3e-2, 0.25, 30, seed=SEED + 6))
        out.append(scene_circular("C2-H4", 30_000, 3e-4, 3e-2, 4.0, 30, seed=SEED + 6))
        out.append(scene_circular("E0-twin-circ", 10_000, 3e-4, 1e-3, 1.0, 30, seed=SEED + 7))
        out.append(scene_eccentric("E1-ecc", 10_000, 3e-4, 1e-3, 0.05, 1.0, 30, seed=SEED + 8))
    return out


def main():
    part = sys.argv[1] if len(sys.argv) > 1 else "all"
    out = run_part(part)

    print(f"{'scene':<16}{'n':>8}{'rho':>8}{'W':>7}{'e':>5}{'H':>5}"
          f"{'enc':>9}{'miss4@H':>9}{'p99':>5}{'k1%':>5}{'rmax':>5}{'k*_law':>7}"
          f"{'miss4@H/20':>11}{'conj/enc':>9}{'sec':>6}")
    for r in out:
        if r["kind"] == "circular":
            c, f = r["cadence_H"], r["cadence_H_over_20"]
            print(f"{r['scene']:<16}{r['n']:>8}{r['rho']:>8.0e}{r['W']:>7.0e}{r.get('e', 0):>5}"
                  f"{r['H']:>5}{r['encounters']:>9}{c['miss4']:>9.3f}{c['rank_p99']:>5}"
                  f"{c['k_1pct']:>5}{c['rank_max']:>5}{r['kstar_law']:>7.1f}{f['miss4']:>11.3f}"
                  f"{r['conj_per_enc']:>9.1f}{r['seconds']:>6.1f}")
        else:
            print(f"\n{r['scene']}: n={r['n']} rho={r['rho']:.0e} W={r['W']:.0e} e={r['e']}"
                  f" H={r['H']} win={r['win']}")
            print(f"  encounters(sampled pairs)={r['encounters']} "
                  f"-> {r['enc_per_body_per_orbit']:.2f} per body per orbit over the ring; "
                  f"reach={r['reach']:.0e} k*_law={r['kstar_law']:.1f}")
            for key in ("rank_mean_H", "rank_true_H", "rank_mean_H_over_20", "rank_true_H_over_20",
                        "rank_mean_H_scan", "rank_true_H_scan"):
                c = r[key]
                print(f"  {key:<22} miss4={c['miss4']:.3f} p99={c['rank_p99']}"
                      f" k1%={c['k_1pct']} rmax={c['rank_max']}")
            if "mean_rank_at_encounter" in r:
                mre = r["mean_rank_at_encounter"]
                print(f"  mean-rank AT encounter: p50={mre['p50']} p99={mre['p99']} max={mre['max']}")
            if "soundness" in r:
                s = r["soundness"]
                print(f"  soundness at rho: {s['frac_below_rho']:.3f} of {s['sample']} sampled "
                      f"events below rho (median dist {s['d_p50']:.2e})")
            v = r["validation"]
            print(f"  validation vs alignment-root scanner on {v['pairs']} pairs: "
                  f"machinery={v['machinery_events']} scanner={v['scan_events']} "
                  f"matched={v['matched']}/{v['machinery_events']} "
                  f"rev={v['matched_rev']}/{v['scan_events']} ({r['seconds']} s)")

    ladder_names = ("A1", "A2", "A3", "A4")
    lad = [r for r in out if r["scene"] in ladder_names]
    slope = None
    if len(lad) == 4:
        ns = np.array([r["n"] for r in lad], float)
        ks = np.array([max(r["cadence_H"]["k_1pct"], 0.5) for r in lad], float)
        slope = float(np.polyfit(np.log(ns), np.log(ks), 1)[0])
        print(f"\nk_1% vs n exponent on A ladder: {slope:.2f} (drift law predicts 1.0)")
    print("rank = partner rank in the sorted ring at the last per-cadence derivation")

    fn = "results.json" if part == "all" else f"results-part{part}.json"
    with open(fn, "w") as fh:
        json.dump(dict(results=out, k_exponent_vs_n=slope), fh, indent=1)
    print("wrote", fn)


if __name__ == "__main__":
    main()
