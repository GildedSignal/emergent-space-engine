"""Reference (truth) for one belt over [0, T].

Per the rung: exact Kepler positions (Kepler's equation solved by Newton to
~1e-14) for each pair whose radial ranges overlap within rho; pairwise
minimum distance found per synodic conjunction. Because the belt is cold
(the run is shorter than any wide synodic cycle), the minimum is taken over
the whole passage window around each conjunction (|ds| <= few a*e), where
the radial difference still beats; the best sample is then refined by Newton
on d/dt (d^2/2) = dr.dv to ~1e-12 relative.
"""
import numpy as np
from belt import TWOPI, kepler_states, rel_state


def candidate_pairs(B, chunk=512):
    """Unordered pairs whose radial ranges overlap within rho (i<j).

    Superset by a-window |da| <= a_i e_i + 1.5 e_max + rho, then exact
    interval test. Cost O(N log N + pairs)."""
def iter_candidate_pairs(B, chunk=512):
    """Yield unordered candidate pairs (i<j) chunk by chunk (each pair
    exactly once: generated from the smaller-index side)."""
    order = np.argsort(B.a, kind="stable")
    a_s = B.a[order]
    rlo = B.rlo[order]; rhi = B.rhi[order]
    emax = B.e.max()
    reach = B.a * B.e + 1.5 * emax + B.rho
    for s in range(0, B.N, chunk):
        rng = slice(s, min(s + chunk, B.N))
        lo = np.searchsorted(a_s, B.a[rng] - reach[rng], side="left")
        hi = np.searchsorted(a_s, B.a[rng] + reach[rng], side="right")
        cnt = hi - lo
        tot = int(cnt.sum())
        if tot == 0:
            continue
        gi = np.repeat(np.arange(rng.start, rng.stop), cnt)
        off = np.concatenate([[0], np.cumsum(cnt)[:-1]])
        pos = np.arange(tot) - np.repeat(off, cnt) + np.repeat(lo, cnt)
        gj = order[pos]
        keep = gi < gj
        gi = gi[keep]; gj = gj[keep]
        ok = (B.rlo[gi] <= B.rhi[gj] + B.rho) & (B.rlo[gj] <= B.rhi[gi] + B.rho)
        yield gi[ok].astype(np.int32), gj[ok].astype(np.int32)
def candidate_pairs(B, chunk=512):
    ii = []; jj = []
    for gi, gj in iter_candidate_pairs(B, chunk):
        ii.append(gi); jj.append(gj)
    if not ii:
        return np.empty(0, np.int32), np.empty(0, np.int32)
    return np.concatenate(ii), np.concatenate(jj)


def rlo_of(B, idx):
    return B.rlo[idx]


def conjunction_counts(B, pi, pj, T):
    """Closed-form number of mean-longitude conjunctions in [0,T] per pair."""
    dn = B.n[pi] - B.n[pj]
    dlam = np.mod(B.lam0[pi] - B.lam0[pj], TWOPI)   # in [0, 2pi)
    C = np.zeros(len(pi), np.int64)
    neg = dn < 0
    # dn<0: t_m = (dlam + 2 pi m)/(-dn), m>=0
    x = ((-dn[neg]) * T - dlam[neg]) / TWOPI
    C[neg] = np.floor(x) + 1
    pos = dn > 0
    x = (dn[pos] * T - (TWOPI - dlam[pos])) / TWOPI
    C[pos] = np.floor(x) + 1
    C[C < 0] = 0
    return C, dn, dlam


def reference_encounters(B, T, pi=None, pj=None, ev_chunk=60000):
    """Returns dict with the true encounter list and per-event detail.

    encounters: (ei, ej, t*, dmin) arrays, plus [t_in, t_out] (d<rho interval).
    Also returns the per-pair conjunction count (needed by element-sort).
    """
    if pi is None:
        pi, pj = candidate_pairs(B)
    C, dn, dlam = conjunction_counts(B, pi, pj, T)
    # expand events (pair, m)
    npair = len(pi)
    ev_pair = np.repeat(np.arange(npair, dtype=np.int64), C)
    if npair == 0:
        return dict(pi=pi, pj=pj, C=C, encounters=(np.empty(0),)*4,
                    t_in=np.empty(0), t_out=np.empty(0), n_events=0)
    m = np.arange(len(ev_pair), dtype=np.int64) - np.repeat(
        np.concatenate([[0], np.cumsum(C)[:-1]]), C)
    sgn = np.where(dn[ev_pair] < 0, 1.0, -1.0)
    tc = (dlam[ev_pair] + (sgn > 0) * 0.0)  # placeholder, computed below
    dnp = dn[ev_pair]; dlp = dlam[ev_pair]
    tc = np.where(dnp < 0, (dlp + TWOPI * m) / (-dnp),
                  (TWOPI - dlp + TWOPI * m) / dnp)
    inside = (tc >= 0) & (tc <= T)
    ev_pair = ev_pair[inside]; tc = tc[inside]
    ei = pi[ev_pair]; ej = pj[ev_pair]
    adn = np.abs(dn[ev_pair])
    # passage half-window: |ds| <= 2 a (e_i+e_j) + 3 rho, swept at ~ a|dn|
    abar = 0.5 * (B.a[ei] + B.a[ej])
    w = (2.0 * abar * (B.e[ei] + B.e[ej]) + 3.0 * B.rho) / (abar * adn + 1e-300)
    w = np.minimum(w, np.pi / (adn + 1e-300))
    w = np.minimum(w, T)
    # sample grid size: 8 points per radial beat, 3..257, bucketed to pow2
    nbar = np.maximum(B.n[ei], B.n[ej])
    msamp = np.ceil(1 + 8.0 * w * nbar / TWOPI).astype(np.int64)
    msamp = np.clip(msamp, 3, 257)
    bucket = np.maximum(4, np.power(2, np.ceil(np.log2(msamp)).astype(np.int64)))
    best_t = np.empty(len(tc)); best_d2 = np.empty(len(tc))
    for b in np.unique(bucket):
        sel = np.where(bucket == b)[0]
        for s in range(0, len(sel), ev_chunk):
            ix = sel[s:s + ev_chunk]
            grid = tc[ix, None] + np.linspace(-1.0, 1.0, int(b))[None, :] * w[ix, None]
            flat = grid.ravel()
            fi = np.repeat(ei[ix], int(b)); fj = np.repeat(ej[ix], int(b))
            dx, dy, _, _, _, _ = rel_state(flat, fi, fj, B)
            d2 = dx * dx + dy * dy
            d2 = d2.reshape(len(ix), int(b))
            k = np.argmin(d2, axis=1)
            best_d2[ix] = d2[np.arange(len(ix)), k]
            best_t[ix] = grid[np.arange(len(ix)), k]
    # Newton refinement of t* (clamped to the window and [0,T])
    t = best_t.copy()
    lo = np.maximum(tc - w, 0.0); hi = np.minimum(tc + w, T)
    for _ in range(4):
        dx, dy, vx, vy, ax, ay = rel_state(t, ei, ej, B)
        g = dx * vx + dy * vy
        gp = vx * vx + vy * vy + dx * ax + dy * ay
        step = g / np.where(np.abs(gp) > 1e-300, gp, 1e300)
        t = np.clip(t - step, lo, hi)
    dx, dy, _, _, _, _ = rel_state(t, ei, ej, B)
    d2 = dx * dx + dy * dy
    better = d2 < best_d2
    t = np.where(better, t, best_t)
    d2 = np.where(better, d2, best_d2)
    dmin = np.sqrt(d2)
    enc = dmin < B.rho
    out = dict(pi=pi, pj=pj, C=C,
               encounters=(ei[enc], ej[enc], t[enc], dmin[enc]),
               t_in=np.empty(0), t_out=np.empty(0), n_events=len(tc))
    out["t_in"], out["t_out"] = _intervals(B, out, T)
    return out


def _intervals(B, ref, T, steps=48):
    """Roots of d(t)=rho around each encounter (bracket + bisection)."""
    ei, ej, t, d = ref["encounters"]
    K = len(ei)
    t_in = np.full(K, np.nan); t_out = np.full(K, np.nan)
    for k in range(K):
        i = int(ei[k]); j = int(ej[k]); t0 = float(t[k])
        h = max(float(B.rho) / 1e-3, 1e-9)
        def dd(tt):
            dx, dy, _, _, _, _ = rel_state(np.array([tt]), np.array([i]), np.array([j]), B)
            return float(np.hypot(dx[0], dy[0]))
        a = t0; b = t0
        for _ in range(steps):
            if dd(a) < B.rho: a -= h
            if dd(b) < B.rho: b += h
            h *= 1.6
            if a < 0 and b > T: break
        lo_b, hi_b = max(a, 0.0), t0
        for _ in range(44):
            mid = 0.5 * (lo_b + hi_b)
            if dd(mid) < B.rho: lo_b = mid
            else: hi_b = mid
        t_in[k] = 0.5 * (lo_b + hi_b)
        lo_b, hi_b = t0, min(b, T)
        for _ in range(44):
            mid = 0.5 * (lo_b + hi_b)
            if dd(mid) < B.rho: lo_b = mid
            else: hi_b = mid
        t_out[k] = 0.5 * (lo_b + hi_b)
    return t_in, t_out
