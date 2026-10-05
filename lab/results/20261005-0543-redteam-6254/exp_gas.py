#!/usr/bin/env python3
"""Red-team falsifier, run 20261005-0543 (lab/results/20261005-0543-redteam-6254/).

Two measurements on a synchronous hard-disc gas (periodic box, one window = one
cell-update; a contact event = a pair closer than 2R at the window):

P2  At the design's own dense threshold (events per cell per light-crossing ~ 1),
    how often does a window contain same-epoch pairs sharing a body (the case where
    resolution order decides the outcome)?

P3  Flip the resolution order of same-epoch pairs in exactly ONE window (window
    FLIP), then resume the canonical order in both runs. How fast does the
    difference cascade through later contacts? (principle 13: errors never compound)

Deterministic: fixed seed, no wall-clock dependence. Newtonian impulses only; the
point (order non-commutativity of sequential contact resolution) is law-independent,
and the repo's own integer law shows the same thing (order-falsifier example).
"""
import numpy as np

R = 1.0
N = 1500
WINDOWS = 240
FLIP = 120  # the single window whose same-epoch pair order is reversed


def contacts(x, L):
    """Overlapping pairs at this window via a cell list of side 2R (vectorized).
    Returns sorted unique (i, j) with i < j."""
    nx = int(L // (2 * R))
    cell = (np.floor(x / (2 * R)).astype(np.int64) % nx)
    key = cell[:, 0] * nx + cell[:, 1]
    order = np.argsort(key, kind="stable")
    ks = key[order]
    xs = x[order]
    out_a, out_b = [], []
    # same cell + 4 neighbours (right, up, up-right, down-right) covers every pair once
    for dc in ((0, 0), (1, 0), (0, 1), (1, 1), (-1, 1)):
        target = ((cell[:, 0] + dc[0]) % nx) * nx + ((cell[:, 1] + dc[1]) % nx)
        lo = np.searchsorted(ks, target, side="left")
        hi = np.searchsorted(ks, target, side="right")
        cnt = hi - lo
        tot = int(cnt.sum())
        if tot == 0:
            continue
        a = np.repeat(np.arange(N), cnt)
        base = np.repeat(np.cumsum(cnt) - cnt, cnt)
        offs = np.arange(tot) - base + np.repeat(lo, cnt)
        b = order[offs]
        keep = a != b
        a, b = a[keep], b[keep]
        d = xs[offs[keep]] - x[a]
        d -= L * np.round(d / L)
        r2 = np.einsum("ij,ij->i", d, d)
        m = r2 < (2 * R) ** 2
        out_a.append(a[m])
        out_b.append(b[m])
    a = np.concatenate(out_a)
    b = np.concatenate(out_b)
    ia, ib = np.minimum(a, b), np.maximum(a, b)
    pairs = np.unique(ia * N + ib)
    return [(int(p // N), int(p % N)) for p in pairs]


def resolve(x, v, pairs, reverse=False):
    """Sequential elastic impulses in sorted (i, j) order (the repo law's batch rule:
    'each pair starts from the velocities earlier pairs left'); `reverse` feeds the
    same batch in the opposite order."""
    for a, b in sorted(pairs, reverse=reverse):
        d = x[b] - x[a]
        d -= 0.0  # contacts are within one cell neighbourhood, no wrap needed
        n = np.hypot(*d)
        if n >= 2 * R:
            continue
        u = d / n
        rel = float(np.dot(v[b] - v[a], u))
        if rel >= 0:
            continue  # separating
        v[a] += u * rel  # equal masses: exchange the normal components
        v[b] -= u * rel


def stats(pairs):
    touched = {}
    for a, b in pairs:
        touched[a] = touched.get(a, 0) + 1
        touched[b] = touched.get(b, 0) + 1
    sharing = sum(c - 1 for c in touched.values() if c > 1)
    multi = sum(1 for c in touched.values() if c > 1)
    return len(pairs), sharing, multi


def main():
    print("P2: same-epoch multi-contact rate (one window = one cell-update, cell = 2R)")
    print("     design's dense threshold: events per cell per light-crossing ~ 1")
    for L in (180.0, 150.0, 120.0, 100.0, 85.0):
        rng = np.random.default_rng(6254)
        x = rng.random((N, 2)) * L
        v = (rng.random((N, 2)) - 0.5) * 0.6
        v -= v.mean(0)
        ncells = int(L // (2 * R)) ** 2
        tp = ts = tm = 0
        for w in range(60):
            x = (x + v * 0.5) % L
            pairs = contacts(x, L)
            p, s, m = stats(pairs)
            tp, ts, tm = tp + p, ts + s, tm + m
            resolve(x, v, pairs)
        print(
            f"  L={L:6.1f} cells={ncells:5d} events/cell/window={tp/60/ncells:6.3f}"
            f" | pairs/window={tp/60:7.1f} sharing-a-body/window={ts/60:6.1f}"
            f" ({100*ts/max(tp,1):5.1f}% of pairs) bodies-in->=2-pairs/window={tm/60:6.1f}"
        )

    print("\nP3: cascade after flipping the order of same-epoch pairs in ONE window")
    L = 120.0
    rng = np.random.default_rng(6254)
    x0 = rng.random((N, 2)) * L
    v0 = (rng.random((N, 2)) - 0.5) * 0.6
    v0 -= v0.mean(0)

    def run(flip: bool, windows=WINDOWS):
        x, v = x0.copy(), v0.copy()
        for w in range(windows):
            x = (x + v * 0.5) % L
            pairs = contacts(x, L)
            resolve(x, v, pairs, reverse=(flip and w == FLIP))
        return v

    for end in (FLIP + 1, FLIP + 4, FLIP + 12, FLIP + 40, WINDOWS):
        va, vb = run(False, end), run(True, end)
        dv = np.linalg.norm(va - vb, axis=1)
        print(
            f"  windows after flip: {end-FLIP:3d} -> diverged bodies (|dv|>1e-9): "
            f"{(dv > 1e-9).sum():5d}/{N} ({100*(dv>1e-9).mean():5.1f}%)"
        )
    va, vb = run(False), run(True)
    dv = np.linalg.norm(va - vb, axis=1)
    print(
        f"  final: median |dv|/median |v| = "
        f"{np.median(dv)/np.median(np.linalg.norm(va,axis=1)):.3f}"
    )


if __name__ == "__main__":
    main()
