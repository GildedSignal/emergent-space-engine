#!/usr/bin/env python3
"""Tier 2: the observer scan's phase tier re-derived against the EXACT `law::hit` branch
structure (the approaching conjunct INCLUDED — scout-b083's replica dropped it, which its
checker named). Three parts:

  A. selector soundness: shipped-predicate hit (exact branch structure) ⊆ widened phase
     window, across e ≤ 0.5, σ_a ≤ 1e-3, both horizons, clustered phases;
  B. the answer on a rigid ring in the float replica (consistency with the flown result);
  C. the selector's cost grounded on the compact store: searchsorted on a δ-sorted
     class-major store (O(log K), not O(K)) and a packed unsorted sweep (the fallback).

Float replica (canonical outcomes are the integers' business; the flown probe in
crates/universe/examples/rigidring.rs grounds the shipped binary's side). Units r=1,v=1,n=1.
Outputs JSON to tier2.json.
"""
import json
import time

import numpy as np

K = 1_000_000
KB = 40_000
ENC = 2 ** 10
OUT = {}
rng = np.random.default_rng(20261018)


def kepler(M, e, a=1.0):
    n = a ** -1.5
    M = M * n
    E = M.copy()
    for _ in range(60):
        f = E - e * np.sin(E) - M
        E = E - f / (1 - e * np.cos(E))
    den = 1 - e * np.cos(E)
    x = a * (np.cos(E) - e)
    y = a * np.sqrt(1 - e * e) * np.sin(E)
    vx = -a * n * np.sin(E) / den
    vy = a * n * np.sqrt(1 - e * e) * np.cos(E) / den
    return x, y, vx, vy


def hit_exact(d0, d1, w0, w1, reach):
    """law::hit's branch structure, floats: approaching required in every branch."""
    dd = d0 * d0 + d1 * d1
    dw = d0 * w0 + d1 * w1
    ww = w0 * w0 + w1 * w1
    rr = reach * reach
    hit = np.zeros_like(dd, dtype=bool)
    in_now = dd <= rr
    hit[in_now] = dw[in_now] < 0
    rest = ~in_now & (ww != 0) & (dw < 0)
    end = rest & (-dw >= ww)
    e0, e1 = d0 + w0, d1 + w1
    hit[end] = (e0[end] * e0[end] + e1[end] * e1[end]) <= rr
    mid = rest & ~end
    cross = d0 * w1 - d1 * w0
    hit[mid] = (cross[mid] * cross[mid]) <= rr * ww[mid]
    return hit


def seg_only(d0, d1, w0, w1, reach):
    """The near set (the read list): min distance over the segment ≤ reach, no approaching."""
    dd = d0 * d0 + d1 * d1
    dw = d0 * w0 + d1 * w1
    ww = w0 * w0 + w1 * w1
    rr = reach * reach
    s = np.clip(-dw / np.where(ww == 0, 1.0, ww), 0.0, 1.0)
    r0, r1 = d0 + s * w0, d1 + s * w1
    return (r0 * r0 + r1 * r1) <= rr


def states(dM, e, M0, da=None):
    xj, yj, vxj, vyj = kepler(M0 + dM, e, a=1.0 + (da if da is not None else 0.0))
    xp, yp, vxp, vyp = kepler(np.array([M0]), e)
    return (xj - xp[0], yj - yp[0], vxj - vxp[0], vyj - vyp[0])


# ------------------------------------------------------------------ A: soundness sweep
A = {}
for e in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]:
    for sig in [0.0, 1e-5, 1e-4, 1e-3]:
        rho = 1e-6
        near = ENC * rho
        for h, hname in [(2 * np.pi / 10, "P/10"), (9.0, "9")]:
            dM = rng.normal(0.0, 0.02, KB)          # clustered: the hard class
            da = rng.normal(0.0, sig, KB) if sig > 0 else np.zeros(KB)
            d0, d1, v0, v1 = states(dM, e, 0.0, da=da)
            w0, w1 = v0 * h, v1 * h
            truth = hit_exact(d0, d1, w0, w1, near)
            drift = 1.5 * h * np.abs(da)
            if e == 0.0:
                sel = 2 * np.abs(np.sin(dM / 2)) <= near + drift
                sel_unw = 2 * np.abs(np.sin(dM / 2)) <= near
            else:
                # 2D capability curve C(offset, da; nu_p): the approaching-conjunct window
                # edge MOVES under the da-shear near apsides (d.w's same-orbit part is
                # O(delta^2) there), so the curve must be indexed by da too. 2^14 x 9
                # da-bins, widened one cell in delta and one bin in da (+ the drift span).
                gb = 14
                n = 2 ** gb
                grid = (np.arange(n) / n - 0.5) * 2 * np.pi
                da_bins = np.arange(-1e-3, 1.0001e-3, 2.5e-4)
                gw = np.zeros((len(da_bins), n), dtype=bool)
                g0 = np.zeros((len(da_bins), n), dtype=bool)
                for bi, db in enumerate(da_bins):
                    gg0, gg1, ggv0, ggv1 = states(grid, e, 0.0, da=np.full(n, db))
                    gb_ = hit_exact(gg0, gg1, ggv0 * h, ggv1 * h, near)
                    g0[bi] = gb_
                    gw[bi] = gb_
                    gw[bi, 1:] |= gb_[:-1]
                    gw[bi, :-1] |= gb_[1:]     # one-cell widening in delta
                gw[1:] |= gw[:-1]
                gw[:-1] |= gw[1:]              # one-bin widening in da
                idx = np.mod(np.floor((dM / (2 * np.pi) + 0.5) * n).astype(int), n)
                lo = np.mod(np.floor(((dM - drift) / (2 * np.pi) + 0.5) * n).astype(int) - 1, n)
                hi = np.mod(np.ceil(((dM + drift) / (2 * np.pi) + 0.5) * n).astype(int) + 1, n)
                bidx = np.clip(np.searchsorted(da_bins, da), 0, len(da_bins) - 1)
                sel = gw[bidx, idx] | gw[bidx, lo] | gw[bidx, hi]
                span = np.maximum(hi - lo, 0)
                wide = np.nonzero(span > 2)[0]
                for i in wide:
                    a_, b_ = lo[i], hi[i]
                    seg = gw[bidx[i], a_:b_ + 1] if b_ >= a_ else np.r_[gw[bidx[i], a_:], gw[bidx[i], :b_ + 1]]
                    sel[i] |= seg.any()
                sel_unw = g0[bidx, idx]
            misses = int(np.sum(truth & ~sel))
            reads = int(np.sum(sel))
            hits = int(np.sum(truth))
            unw_miss = float(np.sum(truth & ~sel_unw)) / max(hits, 1)
            key = f"e={e:g}_sa={sig:g}_h={hname}"
            A[key] = {"hits": hits, "selector_misses": misses, "reads": reads, "pop": KB,
                      "unwidened_miss_rate_among_hits": round(unw_miss, 4)}
OUT["A_soundness"] = A

# ------------------------------------------------------------ B: rigid ring, float replica
B = {}
dM = rng.uniform(0, 2 * np.pi, K)
rho = 1e-6
near = ENC * rho
for h in [2 * np.pi / 10, 9.0]:
    d0, d1, v0, v1 = states(dM, 0.0, 0.0)
    w0, w1 = v0 * h, v1 * h
    ans = hit_exact(d0, d1, w0, w1, near)
    ns = seg_only(d0, d1, w0, w1, near)
    # noise-decided: flip dw by one part in 1e12 -> answer set changes, near set does not
    eps = (w0 * w0 + w1 * w1) ** 0.5 * 1e-12
    ans2 = hit_exact(d0, d1, w0 + eps, w1, near)
    B[f"h={h:g}"] = {"near_set": int(ns.sum()), "answers": int(ans.sum()),
                     "answers_after_1e12_perturbation": int(ans2.sum()),
                     "membership_stability": float(np.mean(ans == ans2))}
OUT["B_rigid_ring"] = B

# ------------------------------------------------------------------- C: the store's costs
C = {}
dM_sorted = np.sort(rng.uniform(0, 2 * np.pi, K))
near_arc = ENC * 1e-6
t0 = time.perf_counter()
for _ in range(100):
    n_lo = np.searchsorted(dM_sorted, near_arc)
    n_hi = K - np.searchsorted(dM_sorted, 2 * np.pi - near_arc)
    n = n_lo + n_hi
t1 = time.perf_counter()
C["searchsorted_window_lookup_us"] = (t1 - t0) / 100 * 1e6
C["window_members_found"] = int(n)
# packed unsorted compact store: uint16 phase words, full sweep (the fallback layout)
words = (rng.uniform(0, 1, K) * 65536).astype(np.uint16)
t0 = time.perf_counter()
for _ in range(20):
    m = np.count_nonzero((words < 300) | (words > 65536 - 300))
t1 = time.perf_counter()
C["packed_uint16_sweep_ms_per_1e6"] = (t1 - t0) / 20 * 1e3
C["sweep_members_found"] = int(m)
# the exact tier's reads at the flown constants (this binary, rigidring probe): 1.9 us/cand
C["exact_read_us_per_member_flown"] = 1.9
C["shipped_per_candidate_us_flown"] = 1.9
lookup = C["searchsorted_window_lookup_us"] * 1e-6
C["tier_scan_s_at_1e6_rho1e-6_uniform"] = lookup + 353 * 1.9e-6
C["shipped_scan_s_at_1e6_flown_rate"] = K * 1.9e-6
C["tier_scan_s_at_1e6_rho1e-6_uniform_604c_rate"] = lookup + 353 * 4.4e-6
C["shipped_scan_s_at_1e6_604c_rate"] = K * 4.4e-6
OUT["C_store"] = C

print(json.dumps(OUT, indent=1, sort_keys=True))
with open(__file__.replace(".py", ".json"), "w") as f:
    json.dump(OUT, f, indent=1, sort_keys=True)
