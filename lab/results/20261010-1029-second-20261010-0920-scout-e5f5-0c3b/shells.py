#!/usr/bin/env python3
"""Run 20261010-1029 (second author on 20261010-0920-scout-e5f5).

The checker's named experiment: replace the scalar accumulators with
per-(cell, shell) accumulators (FMM interaction shells, member quanta) and
measure the deferral error bounded and non-growing at O(1)-per-body cost,
MC-anchored at two sizes.

Scheme "shells" (same toy as the original run: 2D periodic patch, sigma=1,
c=1, Poisson news lambda=1/body/time, strengths log-uniform [0.005, 0.5],
1/d^2 falloff, receiver quantum q):

- DIRECT: an event broadcasts exactly (own s/d^2, arrival-timed) to the
  bodies of the 3x3 leaf neighbourhood of its leaf. No per-event rings, so
  there is no ring/square complement to mismatch.
- SHELLS: one accumulator per (source leaf D0, ring level l), l = 0..R-1,
  holding (A, dipole p about the leaf centre). The member set of (D0, l) is
  {receiver leaf R : l*(R, D0) = l} where l* is the tree-code separation
  level: the smallest l with the wrapped Chebyshev distance of the level-l
  ancestors in [2, 3] (an exact square-annulus tiling of everything outside
  the 3x3). Flush when A >= theta_l = q*(1.5*c_l)^2 (member quantum: nearest
  member body is at >= 1.5*c_l from the leaf centre). The flush delivers
  (A, p) from the leaf centre, arrival-timed, to member bodies only.

Exact partition (canonical, integer): every (receiver, event) pair goes
through exactly one channel -- DIRECT xor exactly one (D0, l) accumulator --
asserted over the full leaf x leaf l*-table for every configuration.

Accumulator crossing is checked at event-chunk boundaries (<= 0.125 time
units); the flush time is the chunk's last event time. Disclosed
approximation: adds <= one chunk-span of deferral, absorbed by the pending
bound (chunk arrivals into one accumulator << theta at every level).

Floats explore; the partition assert and the delivery counts are integers.
"""
import json
import numpy as np
from scipy.spatial import cKDTree

RNG = np.random.default_rng(20261010)


def make_patch(side_cells, k=16, lam=1.0, T=6.0, s_min=0.005, s_max=0.5,
               q=0.01, T_pre=0.0):
    """T_pre > 0: pre-history events with t0 in [-T_pre, 0) so the shell
    accumulators enter the measurement window [0, T] in steady state (the
    top ring's flush cycle is ~13 time units at q=0.01, longer than T)."""
    cell = np.sqrt(k)
    box = side_cells * cell
    n_body = side_cells * side_cells * k
    xy = RNG.random((n_body, 2)) * box
    tree = cKDTree(xy, boxsize=box)
    n_ev = RNG.poisson(lam * n_body * (T + T_pre))
    t0 = np.sort(RNG.random(n_ev) * (T + T_pre) - T_pre)
    src = RNG.integers(0, n_body, n_ev)
    s = np.exp(RNG.uniform(np.log(s_min), np.log(s_max), n_ev))
    return dict(box=box, cell=cell, side=side_cells, xy=xy, tree=tree,
                t0=t0, src=src, s=s, T=T, q=q, lam=lam, n_body=n_body, k=k,
                T_pre=T_pre)


def wrap_d(xy, x, box):
    return (xy - (x % box) + box / 2) % box - box / 2


def lstar_table(side):
    """l*[src_leaf, recv_leaf]: -1 direct (leaf-Cheb<=1), else smallest l
    with wrapped Chebyshev distance of the level-l ancestors in [2,3].
    -2 = uncovered (must not exist). Integer, canonical."""
    n = side * side
    si, sj = np.divmod(np.arange(n), side)
    ri, rj = np.divmod(np.arange(n), side)
    L = np.full((n, n), -2, dtype=np.int8)
    di = np.abs(si[:, None] - ri[None, :])
    di = np.minimum(di, side - di)
    dj = np.abs(sj[:, None] - rj[None, :])
    dj = np.minimum(dj, side - dj)
    cheb0 = np.maximum(di, dj)
    L[cheb0 <= 1] = -1
    open_mask = L == -2
    lv = 0
    while np.any(open_mask) and (side >> lv) >= 4:
        f = 1 << lv
        side_l = side // f
        ci = np.abs((si[:, None] // f) - (ri[None, :] // f))
        ci = np.minimum(ci, side_l - ci)
        cj = np.abs((sj[:, None] // f) - (rj[None, :] // f))
        cj = np.minimum(cj, side_l - cj)
        cl = np.maximum(ci, cj)
        in_ring = (cl >= 2) & (cl <= 3) & open_mask
        L[in_ring] = lv
        open_mask = L == -2
        lv += 1
    assert not np.any(open_mask), "uncovered (src,recv) leaf pairs exist"
    return L


def member_counts(L):
    n = L.shape[0]
    counts = np.zeros((n, int(L.max()) + 2), dtype=np.int64)
    for l in range(-1, int(L.max()) + 1):
        counts[:, l + 1] = (L == l).sum(axis=1)
    total = counts.sum(axis=1)
    assert np.all(total == n), "partition not exact"
    return counts


def dipole_field(dvec, A, p):
    """Field of aggregate (A, p about centre) at offsets dvec (...,2):
    F = -A*u/D^2 + (p - 3(p.u)u)/D^3.  A=0,p=0 -> 0."""
    D = np.linalg.norm(dvec, axis=-1) + 1e-12
    u = dvec / D[..., None]
    pu = (p * u).sum(-1)
    return (-(A / D**2)[..., None] * u
            + ((p - 3 * pu[..., None] * u) / D[..., None]**3))


def self_test_dipole():
    rng = np.random.default_rng(7)
    cen = np.array([50.0, 50.0])
    src = cen + rng.uniform(-2.8, 2.8, (200, 2))
    s = rng.uniform(0.005, 0.5, 200)
    recv = np.array([[50.0, 95.0], [15.0, 55.0], [58.0, 90.0]])  # D/rho ~ 14
    A, p = s.sum(), (s[:, None] * (src - cen)).sum(0)
    approx = dipole_field(recv - cen, A, p)
    mono = dipole_field(recv - cen, A, np.zeros(2))
    exact = np.zeros_like(approx)
    for i in range(len(recv)):
        d = recv[i] - src
        dist = np.linalg.norm(d, axis=1) + 1e-12
        exact[i] = (s[:, None] * (-d / dist[:, None] ** 3)).sum(0)
    rel = np.linalg.norm(approx - exact, axis=1) / np.linalg.norm(exact, axis=1)
    rel_m = np.linalg.norm(mono - exact, axis=1) / np.linalg.norm(exact, axis=1)
    assert rel.max() < 5e-3, "dipole formula wrong: %g" % rel.max()
    assert np.all(rel_m > 1.5 * rel), "dipole term not helping"
    return float(rel.max())


def run_shells(patch, agg="dipole", snap_times=None, n_recv=256, bin_w=1.0):
    q, T = patch["q"], patch["T"]
    xy, box, side, k = patch["xy"], patch["box"], patch["side"], patch["k"]
    n_body, cell = patch["n_body"], patch["cell"]
    n_leaf = side * side
    L = lstar_table(side)
    n_ring = int(L.max()) + 1
    mc = member_counts(L)

    # padded per-leaf body lists (variable occupancy -> -1 pad)
    leaf_of = (np.floor(xy / cell).astype(int) % side)
    leaf_of = leaf_of[:, 0] * side + leaf_of[:, 1]
    order = np.argsort(leaf_of, kind="stable")
    starts = np.searchsorted(leaf_of[order], np.arange(n_leaf + 1))
    k_max = int(np.diff(starts).max())
    bodies_pad = -np.ones((n_leaf, k_max), dtype=np.int64)
    for l in range(n_leaf):
        b = order[starts[l]:starts[l + 1]]
        bodies_pad[l, :len(b)] = b

    li_, lj_ = np.divmod(np.arange(n_leaf), side)
    cen = np.stack([(li_ + 0.5) * cell, (lj_ + 0.5) * cell], 1)

    theta = np.array([q * (1.5 * cell * 2**l) ** 2 for l in range(n_ring)])
    acc_A = [np.zeros(n_leaf) for _ in range(n_ring)]
    acc_p = [np.zeros((n_leaf, 2)) for _ in range(n_ring)]

    recv = np.linspace(0, n_body - 1, n_recv).astype(int)
    counters = dict(direct=0, flush=0, writes=0, emissions=0,
                    flush_by_level=[0] * n_ring, em_by_level=[0] * n_ring)
    flush_t, flush_leaf, flush_l, flush_A, flush_p = \
        [], [], [], [], []
    n_bins = int(np.ceil((T + box) / bin_w))
    bins = np.zeros((n_bins, n_body), dtype=np.int32)

    def deliver_bodies(bidx, t_emit, origin):
        """bidx: (m, k_max) padded body ids; count arrivals into bins."""
        valid = bidx >= 0
        bflat = bidx[valid]
        dvec = wrap_d(xy[bflat], origin, box)
        d = np.linalg.norm(dvec, axis=1)
        b = ((t_emit + d) / bin_w).astype(int)
        keep = (b >= 0) & (b < n_bins)
        np.add.at(bins, (b[keep], bflat[keep]), 1)
        return len(bflat)

    t0, src, s = patch["t0"], patch["src"], patch["s"]
    n_ev = len(t0)
    chunk = max(256, int(n_body * 0.125))
    off = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1)]

    for i0 in range(0, n_ev, chunk):
        i1 = min(i0 + chunk, n_ev)
        ev = np.arange(i0, i1)
        t_e, s_e = t0[ev], s[ev]
        x_e = xy[src[ev]]
        l_e = leaf_of[src[ev]]
        li, lj = np.divmod(l_e, side)
        t_chunk = t_e[-1]
        # ---- direct: 3x3 broadcast, exact arrival-timed
        for a, b in off:
            nb = ((li + a) % side) * side + ((lj + b) % side)
            bp = bodies_pad[nb]                       # (n_chunk, k_max)
            valid = bp >= 0
            bflat = bp[valid]
            reps = np.cumsum(np.concatenate([[0], valid.sum(axis=1)]))
            xy_b = xy[bflat]
            dvec = wrap_d(xy_b, np.repeat(x_e, valid.sum(axis=1), axis=0),
                          box)
            d = np.linalg.norm(dvec, axis=1)
            bb = ((np.repeat(t_e, valid.sum(axis=1)) + d)
                  / bin_w).astype(int)
            keep = (bb >= 0) & (bb < n_bins)
            np.add.at(bins, (bb[keep], bflat[keep]), 1)
            counters["direct"] += len(bflat)
        # ---- shell accumulators + flushes at chunk boundary
        delta = x_e - cen[l_e]
        for l in range(n_ring):
            np.add.at(acc_A[l], l_e, s_e)
            np.add.at(acc_p[l], l_e, s_e[:, None] * delta)
            counters["writes"] += len(ev)
            crossed = np.nonzero(acc_A[l] >= theta[l])[0]
            if len(crossed):
                A_c = acc_A[l][crossed].copy()
                p_c = acc_p[l][crossed].copy()
                if agg == "scalar":
                    p_c[:] = 0.0
                acc_A[l][crossed] = 0.0
                acc_p[l][crossed] = 0.0
                member_mask = (L[crossed] == l)          # (n_cross, n_leaf)
                for m_i, c_leaf in enumerate(crossed):
                    flush_t.append(t_chunk)
                    flush_leaf.append(int(c_leaf))
                    flush_l.append(l)
                    flush_A.append(float(A_c[m_i]))
                    flush_p.append((float(p_c[m_i, 0]), float(p_c[m_i, 1])))
                    m_leaves = np.nonzero(member_mask[m_i])[0]
                    nd = deliver_bodies(bodies_pad[m_leaves], t_chunk,
                                        cen[c_leaf])
                    counters["flush"] += nd
                    counters["flush_by_level"][l] += nd
                    counters["emissions"] += 1
                    counters["em_by_level"][l] += 1

    # ---- error snapshots (block-chunked over receivers and events)
    snaps = []
    if snap_times is not None:
        rx = xy[recv]
        rl = leaf_of[recv]
        ev_x = xy[src]
        src_leaf_ev = leaf_of[src]
        fl_t = np.array(flush_t)
        fl_leaf = np.array(flush_leaf, dtype=int)
        fl_l = np.array(flush_l, dtype=int)
        fl_A = np.array(flush_A)
        fl_p = np.array(flush_p) if flush_p else np.zeros((0, 2))
        n_fl = len(fl_t)
        EB, FB = 32768, 8192
        for ts in snap_times:
            a_ex = np.zeros((n_recv, 2))
            a_gt = np.zeros((n_recv, 2))
            for i0 in range(0, n_recv, 64):
                sl = slice(i0, i0 + 64)
                rxb = rx[sl]
                for e0 in range(0, n_ev, EB):
                    e1 = min(e0 + EB, n_ev)
                    d = wrap_d(rxb[:, None, :], ev_x[None, e0:e1, :], box)
                    dist = np.linalg.norm(d, axis=2) + 1e-12
                    arr = t0[None, e0:e1] + dist
                    w_ex = np.where(arr <= ts, s[None, e0:e1] / dist**2, 0.0)
                    a_ex[sl] += (w_ex[..., None]
                                 * (-d / dist[..., None])).sum(axis=1)
                    m_dir = (L[rl[sl, None],
                               src_leaf_ev[None, e0:e1]] == -1) & (arr <= ts)
                    w_dir = np.where(m_dir, s[None, e0:e1] / dist**2, 0.0)
                    a_gt[sl] += (w_dir[..., None]
                                 * (-d / dist[..., None])).sum(axis=1)
                for f0 in range(0, n_fl, FB):
                    f1 = min(f0 + FB, n_fl)
                    mem = (L[rl[sl, None], fl_leaf[None, f0:f1]]
                           == fl_l[None, f0:f1])
                    df = wrap_d(rxb[:, None, :], cen[fl_leaf][None, f0:f1, :],
                                box)
                    dfd = np.linalg.norm(df, axis=2) + 1e-12
                    arrf = fl_t[None, f0:f1] + dfd
                    m_fl = mem & (arrf <= ts)
                    A_w = np.where(m_fl, fl_A[None, f0:f1], 0.0)
                    p_w = np.where(m_fl[..., None],
                                   fl_p[None, f0:f1, :], 0.0)
                    a_gt[sl] += dipole_field(df, A_w, p_w).sum(axis=1)
            err = np.linalg.norm(a_gt - a_ex, axis=1)
            snaps.append(dict(t=float(ts), max=float(err.max()),
                              med=float(np.median(err))))
    in_horizon = bins[:int(T / bin_w)]
    per_body_bins = in_horizon.sum(axis=0) / (T / bin_w)
    acc_words = sum(int((acc_A[l] > 0).sum()) for l in range(n_ring)) * 3
    return dict(counters=counters, snaps=snaps, per_body_bins=per_body_bins,
                n_ring=n_ring, acc_words=acc_words, mcounts=mc,
                theta=theta.tolist(), n_flush=n_fl if snap_times else 0)


def main():
    print("dipole self-test rel err: %.2e" % self_test_dipole(), flush=True)
    out = {}
    import sys
    warm = "--cold" not in sys.argv
    if warm:
        # steady-state runs: pre-history so accumulators are warm at t=0
        cfgs = [
            ("s32_q1_T12_dip_pre", 32, 0.01, 12.0, "dipole", 30.0),
            ("s32_q1_T12_sca_pre", 32, 0.01, 12.0, "scalar", 30.0),
            ("s32_qf_T6_dip_pre", 32, 0.001, 6.0, "dipole", 30.0),
            ("s16_q1_T6_dip_pre", 16, 0.01, 6.0, "dipole", 30.0),
        ]
    else:
        # cold-start suite (transient exploration; explained in dossier)
        cfgs = [
            ("s16_q1_T6_dip", 16, 0.01, 6.0, "dipole", 0.0),
            ("s32_q1_T6_dip", 32, 0.01, 6.0, "dipole", 0.0),
            ("s32_q1_T12_dip", 32, 0.01, 12.0, "dipole", 0.0),
            ("s32_q1_T12_sca", 32, 0.01, 12.0, "scalar", 0.0),
            ("s32_qf_T6_dip", 32, 0.001, 6.0, "dipole", 0.0),
        ]
    import time
    for tag, side, q, T, agg, T_pre in cfgs:
        global RNG
        RNG = np.random.default_rng(20261010)
        p = make_patch(side, q=q, T=T, T_pre=T_pre)
        snaps_t = [2.0, 4.0, 6.0] + ([8.0, 10.0, 12.0] if T >= 12 else [])
        t_start = time.time()
        r = run_shells(p, agg=agg, snap_times=snaps_t)
        wall = time.time() - t_start
        n = p["n_body"]
        span = T + T_pre
        nrr = r["n_ring"]
        out[tag] = dict(
            side=side, q=q, T=T, T_pre=T_pre, agg=agg, n_body=n,
            n_ev=len(p["t0"]), n_ring=nrr, theta=r["theta"], wall_s=wall,
            per_time=dict(
                direct=r["counters"]["direct"] / n / span,
                flush=r["counters"]["flush"] / n / span,
                writes=r["counters"]["writes"] / n / span,
                emissions=r["counters"]["emissions"] / n / span),
            flush_by_level_per_time=[r["counters"]["flush_by_level"][l]
                                     / n / span for l in range(nrr)],
            em_by_level_per_time=[r["counters"]["em_by_level"][l]
                                  / n / span for l in range(nrr)],
            bursts=dict(med=float(np.median(r["per_body_bins"])),
                        p99=float(np.percentile(r["per_body_bins"], 99)),
                        mx=float(r["per_body_bins"].max())),
            err=[dict(t=s["t"], max_q=s["max"] / q, med_q=s["med"] / q)
                 for s in r["snaps"]],
            acc_words_per_body=r["acc_words"] / n,
            n_flush_total=r["counters"]["emissions"],
        )
        print(tag, "wall=%.0fs" % wall,
              {kk: round(vv, 2) for kk, vv in out[tag]["per_time"].items()},
              "flush/level:", [round(x, 1) for x in
                               out[tag]["flush_by_level_per_time"]],
              flush=True)
        print("  err(q):", [(e["t"], round(e["max_q"], 1),
                             round(e["med_q"], 2)) for e in out[tag]["err"]],
              flush=True)
    import os
    os.makedirs("out", exist_ok=True)
    fname = "out/shells-pre-results.json" if warm \
        else "out/shells-results.json"
    with open(fname, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print("wrote", fname)


if __name__ == "__main__":
    main()
