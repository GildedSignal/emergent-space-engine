#!/usr/bin/env python3
"""Gravity-as-news delivery cost at scale (run 20261010-0920-scout-e5f5).

Toy: 2D periodic patch, surface density sigma=1 body/unit^2, c=1. News events
(thrust/contact/rebind class, NOT free-fall kicks) arrive Poisson, lambda per
body per time unit, strengths log-uniform [s_min, s_max]. Field falloff 1/d^2.

Schemes:
  naive : every body processes every front at light-cone arrival (R5's cursor,
          taken literally). Cost per event = N; memory = fronts in flight
          (analytic) + N^2 cursors (reported).
  gated : an event direct-delivers inside its ring r_q = sqrt(s/q). Beyond the
          ring it is sub-quantum everywhere, so its strength accumulates in the
          smallest containing cell whose radius >= r_q. A cell flushes when its
          accumulator crosses theta = q * rho^2 (rho = cell radius); the flush
          is one aggregated news of that strength delivered outside the cell.
  drop  : negative control - sub-quantum news discarded instead of accumulated.

Instruments: deliveries + writes per body per time; deferral error
|a_gated - a_exact| at receivers over time; per-body delivery burst stats.
"""
import json
import numpy as np
from scipy.spatial import cKDTree

RNG = np.random.default_rng(20261010)


def make_patch(side_cells, k=16, lam=1.0, T=6.0, s_min=0.005, s_max=0.5, q=0.01):
    cell = np.sqrt(k)                       # cell side (area k, sigma=1)
    box = side_cells * cell
    n_body = side_cells * side_cells * k
    xy = RNG.random((n_body, 2)) * box
    tree = cKDTree(xy, boxsize=box)
    n_ev = RNG.poisson(lam * n_body * T)
    t0 = np.sort(RNG.random(n_ev) * T)
    src = RNG.integers(0, n_body, n_ev)
    s = np.exp(RNG.uniform(np.log(s_min), np.log(s_max), n_ev))
    return dict(box=box, cell=cell, side=side_cells, xy=xy, tree=tree,
                t0=t0, src=src, s=s, T=T, q=q, lam=lam, n_body=n_body)


def hierarchy(patch):
    """Nested cells: levels side, side/2, ..., 1."""
    levels = []
    side = patch["side"]
    cell = patch["cell"]
    lv = 0
    while True:
        c = cell * (2 ** lv)               # cell side at this level
        centers = (np.arange(side) + 0.5) * c
        gx, gy = np.meshgrid(centers, centers, indexing="ij")
        cen = np.stack([gx.ravel(), gy.ravel()], 1)
        rho = (c * np.sqrt(2) / 2) * np.ones(len(cen))   # circumscribed radius
        theta = patch["q"] * rho ** 2
        acc = np.zeros(len(cen))
        if lv == 0:                      # leaf: member-residue accumulator
            d_near, _ = patch["tree"].query(cen % patch["box"], k=1)
            m_theta = patch["q"] * np.maximum(d_near, 0.25) ** 2
        else:
            m_theta = None
        levels.append(dict(side=side, c=c, cen=cen, rho=rho,
                           theta=theta, acc=acc, m_acc=acc.copy(),
                           m_theta=m_theta))
        if side == 1:
            break
        side //= 2
        lv += 1
    return levels


def leaf_index(patch, x):
    i = np.floor(x / patch["cell"]).astype(int) % patch["side"]
    return i[..., 0] * patch["side"] + i[..., 1]


def parent_idx(levels, lv, idx):
    side = levels[lv]["side"]
    r, c = divmod(int(idx), side)
    ps = levels[lv + 1]["side"]
    return (r // 2) * ps + (c // 2)


def wrap_d(xy, x, box):
    return (xy - (x % box) + box / 2) % box - box / 2


def run_gated(patch, mode="gated", snap_times=None, n_recv=256, bin_w=1.0):
    q, T = patch["q"], patch["T"]
    tree, xy, box = patch["tree"], patch["xy"], patch["box"]
    lv0 = hierarchy(patch)
    L = len(lv0)
    n_body = patch["n_body"]
    recv = np.linspace(0, n_body - 1, n_recv).astype(int)
    counters = dict(direct=0, flush=0, writes=0, flush_emissions=0)
    flushes = []                            # (t, cx, cy, A, rho)
    n_bins = int(np.ceil((T + np.sqrt(0.5 / q)) / bin_w))
    bins = np.zeros((n_bins, n_body), dtype=np.int32)

    def deliver_ring(t_emit, x, strength, excl_sq=0.0, origin=None):
        """receivers within sqrt(strength/q), binned at ARRIVAL time (c=1).
        excl_sq>0: deliver only receivers OUTSIDE the cell square of that
        half-side, centred on origin (aggregates; exact complement of the
        direct rings when routing inscribes rings inside the square)."""
        r = np.sqrt(strength / q)
        if origin is None:
            origin = x
        idx = np.asarray(tree.query_ball_point(origin % box, r), dtype=int)
        if len(idx) == 0:
            return 0
        dvec = wrap_d(xy[idx], origin, box)
        d = np.linalg.norm(dvec, axis=1)
        if excl_sq > 0:
            keep = np.max(np.abs(dvec), axis=1) >= excl_sq
            idx, d = idx[keep], d[keep]
            if len(idx) == 0:
                return 0
        b = np.minimum(((t_emit + d) / bin_w).astype(int), n_bins - 1)
        np.add.at(bins, (b, idx), 1)
        return len(idx)

    for e in range(len(patch["t0"])):
        t, s = patch["t0"][e], patch["s"][e]
        x = xy[patch["src"][e]]
        r_q = np.sqrt(s / q)
        counters["direct"] += deliver_ring(t, x, s)
        counters["writes"] += 1
        if mode == "drop":
            continue
        # v3: member-residue accumulator at the event's own leaf, flushed at
        # the MEMBER quantum q*d_near^2 - serves receivers inside the leaf
        # square but outside the direct ring, which v2 left unserved.
        leaf = lv0[0]
        li = int(leaf_index(patch, x))
        leaf["m_acc"][li] += s
        if leaf["m_acc"][li] >= leaf["m_theta"][li]:
            A = leaf["m_acc"][li]
            lcen = leaf["cen"][li]
            flushes.append((t, lcen[0], lcen[1], A, 0.0))
            counters["flush"] += deliver_ring(t, lcen, A, origin=lcen)
            counters["flush_emissions"] += 1
            leaf["m_acc"][li] = 0.0
        # route the residue to the smallest containing cell whose INSCRIBED
        # disk contains the ring: the aggregate is then the exact complement
        # of the direct rings for outside-square receivers.
        lv, idx = 0, li
        while lv + 1 < L:
            cellv = lv0[lv]
            dc = np.linalg.norm(wrap_d(cellv["cen"][idx][None, :], x, box)[0])
            if dc + r_q <= cellv["c"] / 2:
                break
            idx = parent_idx(lv0, lv, idx)
            lv += 1
        # accumulate, flush upward while crossing theta
        while True:
            cellv = lv0[lv]
            cellv["acc"][idx] += s
            counters["writes"] += 1
            if cellv["acc"][idx] < cellv["theta"][idx]:
                break
            A = cellv["acc"][idx]
            cen = cellv["cen"][idx]
            flushes.append((t, cen[0], cen[1], A, cellv["c"] / 2))
            counters["flush"] += deliver_ring(t, cen, A,
                                              excl_sq=cellv["c"] / 2,
                                              origin=cen)
            counters["flush_emissions"] += 1
            cellv["acc"][idx] = 0.0
            s = A                                # carry to the parent
            if lv + 1 >= L:
                break
            idx = parent_idx(lv0, lv, idx)
            lv += 1

    # ---- error snapshots: |a_gated - a_exact| at receivers ----
    snaps = []
    if snap_times is not None:
        rx = xy[recv]
        ev_x = xy[patch["src"]]
        r_q_all = np.sqrt(patch["s"] / q)
        fl = np.array(flushes) if flushes else np.zeros((0, 5))
        for ts in snap_times:
            a_ex = np.zeros((n_recv, 2))
            a_gt = np.zeros((n_recv, 2))
            for i0 in range(0, n_recv, 128):
                sl = slice(i0, i0 + 128)
                d = wrap_d(rx[sl, None, :], ev_x[None, :, :], box)
                dist = np.linalg.norm(d, axis=2) + 1e-12
                arr = patch["t0"][None, :] + dist
                w_ex = np.where(arr <= ts, patch["s"][None, :] / dist ** 2, 0.0)
                a_ex[sl] = (w_ex[..., None] * (-d / dist[..., None])).sum(axis=1)
                m_dir = (dist <= r_q_all[None, :]) & (arr <= ts)
                w_dir = np.where(m_dir, patch["s"][None, :] / dist ** 2, 0.0)
                a_gt[sl] = (w_dir[..., None] * (-d / dist[..., None])).sum(axis=1)
                if len(fl):
                    df = wrap_d(rx[sl, None, :], fl[None, :, 0:2], box)
                    dfd = np.linalg.norm(df, axis=2) + 1e-12
                    arrf = fl[None, :, 0] + dfd
                    m_fl = (np.max(np.abs(df), axis=2) >= fl[None, :, 4]) & (arrf <= ts)
                    w_fl = np.where(m_fl, fl[None, :, 3] / dfd ** 2, 0.0)
                    a_gt[sl] += (w_fl[..., None] * (-df / dfd[..., None])).sum(axis=1)
            err = np.linalg.norm(a_gt - a_ex, axis=1)
            snaps.append(dict(t=float(ts), max=float(err.max()),
                              med=float(np.median(err))))
    in_horizon = bins[:int(T / bin_w)]           # bins fully inside [0, T]
    per_body_bins = in_horizon.sum(axis=0) / (T / bin_w)
    return counters, flushes, snaps, per_body_bins, L


def analytic(N, lam=1.0, q=0.01, k=16, s_bar=None, s_min=0.005, s_max=0.5):
    if s_bar is None:
        s_bar = (s_max - s_min) / (np.log(s_max) - np.log(s_min))
    R = np.sqrt(N / np.pi)
    A1 = k
    naive_per_body = lam * N
    E_tau = 5 * R / 3                     # mean front lifetime in the disk
    naive_inflight_per_body = lam * E_tau
    F = lam * 1.0 * s_bar                 # strength flux per unit area per time
    L = 1 + int(np.ceil(np.log(np.pi * R * R / A1) / np.log(4)))
    C = 3 * np.pi * lam * s_bar / (4 * q * k)   # emission-annulus constant
    # deliveries: direct rings dominate; emission annuluses add the log term
    gated_del_per_body = lam * np.pi * s_bar / q + C * L
    gated_writes_per_body = lam + F * np.pi / (q * A1) * (4.0 / 3.0)
    # in-flight pending state: an aggregated emission is pending only while
    # its front sweeps its own delivery ring (lifetime ~ ring radius / c),
    # NOT while crossing the disk (the first model, disproven by the MC's
    # emission rate x ring lifetime). The true light-cone residue is the
    # frontier: top-level emissions whose rings reach the disk edge.
    alive = 0.0
    for l in range(1, L + 1):
        A_l = A1 * 4 ** (l - 1)
        theta = q * A_l / np.pi
        rate_l = F * np.pi * R * R / theta          # emissions per disk per time
        ring_l = np.sqrt(theta / q)                 # delivery ring radius
        alive += rate_l * ring_l                    # pending while front in ring
    frontier = (F * np.pi * R * R / (q * np.pi * R * R / np.pi)) * (5 * R / 3)
    return dict(N=N, R=R, levels=L, s_bar=s_bar,
                naive_per_body=naive_per_body,
                naive_inflight_per_body=naive_inflight_per_body,
                naive_cursors=N * N,
                gated_del_per_body=gated_del_per_body,
                gated_writes_per_body=gated_writes_per_body,
                gated_accum_words_per_body=(4.0 / 3.0) / k,
                gated_inflight_per_body=alive / N,
                gated_frontier_total=frontier)


def fit_exp(x, y):
    return float(np.polyfit(np.log(x), np.log(y), 1)[0])


def main():
    out = {}
    q_main, q_fine = 0.01, 0.001
    Ns = [1e3, 1e4, 1e5, 1e6]
    A = [analytic(N, q=q_main) for N in Ns]
    out["analytic"] = A
    out["fits"] = dict(
        naive_del_exp=fit_exp(Ns, [a["naive_per_body"] for a in A]),
        naive_inflight_exp=fit_exp(Ns, [a["naive_inflight_per_body"] for a in A]),
        gated_del_exp=fit_exp(Ns, [a["gated_del_per_body"] for a in A]),
        gated_inflight_exp=fit_exp(Ns, [a["gated_inflight_per_body"] for a in A]),
        ratio_1e6=A[-1]["naive_per_body"] / A[-1]["gated_del_per_body"],
    )
    K, Nf = 1e4, 1e6
    s_bar = (0.5 - 0.005) / (np.log(0.5) - np.log(0.005))
    fleet_naive = K * Nf
    r_dir = np.sqrt(s_bar / q_main)
    fleet_gated = K * (np.pi * r_dir ** 2) + np.pi * (K * s_bar / q_main)
    out["fleet"] = dict(K=K, N=Nf, naive=fleet_naive, gated=fleet_gated,
                        ratio=fleet_naive / fleet_gated)
    mc = {}
    for tag, side, q in [("s32_q1", 32, q_main), ("s32_q1f", 32, q_fine)]:
        p = make_patch(side, q=q, T=6.0)
        snaps_t = [2.0, 4.0, 6.0]
        cnt, fl, sn, pbb, L = run_gated(p, mode="gated", snap_times=snaps_t)
        cnt_d, _, sn_d, pbb_d, _ = run_gated(p, mode="drop", snap_times=snaps_t)
        mc[tag] = dict(side=side, q=q, n_body=p["n_body"], n_ev=len(p["t0"]),
                       levels=L,
                       per_time=dict(
                           direct=cnt["direct"] / p["n_body"] / 6.0,
                           flush=cnt["flush"] / p["n_body"] / 6.0,
                           writes=cnt["writes"] / p["n_body"] / 6.0,
                           emissions=cnt["flush_emissions"] / p["n_body"] / 6.0),
                       bursts=dict(med=float(np.median(pbb)),
                                   p99=float(np.percentile(pbb, 99)),
                                   mx=float(pbb.max())),
                       err_gated=sn, err_drop=sn_d,
                       n_flushes=len(fl))
        print(tag, "done", flush=True)
    out["mc"] = mc
    with open("out/results.json", "w") as f:
        json.dump(out, f, indent=1, default=float)
    print("\n== analytic (q=%.3g) ==" % q_main)
    for a in A:
        print("N=%8.0f naive/body=%9.1f gated/body=%7.2f (%d lvls) "
              "inflight naive/body=%8.2f gated/body=%7.4f" %
              (a["N"], a["naive_per_body"], a["gated_del_per_body"], a["levels"],
               a["naive_inflight_per_body"], a["gated_inflight_per_body"]))
    print("fits:", {k: round(v, 4) for k, v in out["fits"].items()})
    print("fleet:", {k: round(v, 2) for k, v in out["fleet"].items()})
    for tag, m in mc.items():
        print("\n== MC %s: %d bodies, %d events, %d levels ==" %
              (tag, m["n_body"], m["n_ev"], m["levels"]))
        print(" per body/time: direct=%.2f flush=%.2f writes=%.2f emissions=%.3f"
              % (m["per_time"]["direct"], m["per_time"]["flush"],
                 m["per_time"]["writes"], m["per_time"]["emissions"]))
        print(" bursts: med=%.2f p99=%.2f max=%.2f (ratio %.1f)" %
              (m["bursts"]["med"], m["bursts"]["p99"], m["bursts"]["mx"],
               m["bursts"]["p99"] / max(m["bursts"]["med"], 1e-9)))
        for s in m["err_gated"]:
            print("  t=%.0f gated err: max=%.3g med=%.3g (q=%g)" %
                  (s["t"], s["max"], s["med"], m["q"]))
        for s in m["err_drop"]:
            print("  t=%.0f DROP err: max=%.3g med=%.3g" % (s["t"], s["max"], s["med"]))


if __name__ == "__main__":
    main()
