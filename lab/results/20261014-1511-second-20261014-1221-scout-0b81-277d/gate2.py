#!/usr/bin/env python3
"""The quantum gate, re-derived with Kepler-true conjunction misses (second run on 0b81).

Per candidate pair, every close approach in the 10^3-orbit horizon is found as a local
minimum of |x1(t)-x2(t)| under EXACT Kepler propagation (no integration, no miss
model): Newton on d/dt(d^2) started at the mean-longitude conjunction times
t_k = (2 pi k - dL0)/dn (exact, linear clock) with a second start +0.35 orbit off.
The pair's strongest in-horizon impulse is charged against one Q48 of E (the shipped
`Key` quantum). The author's uniform miss model and the checker's pooled rescale are
both replaced by measurement.

Controls: brute-force sampled min + golden refine on a subsample; the checker's
per-da table; the author's two mass controls. Variants (quantum, belt mass) are
post-processing on the saved per-pair (wmin, vrel) arrays.
"""
import numpy as np
from multiprocessing import Pool

TWO_PI = 2 * np.pi
Q48 = 2.0**-48
MSUN = 1.989e30
H_TIME = 1000.0 * TWO_PI

# ---------------- exact Kepler ----------------

def kepler_state(a, e, w, M0, t):
    n = a**-1.5
    M = np.mod(M0 + n * t + np.pi, TWO_PI) - np.pi
    E = M + e * np.sin(M)
    for _ in range(5):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    cE, sE = np.cos(E), np.sin(E)
    b = a * np.sqrt(1 - e * e)
    ox, oy = a * (cE - e), b * sE
    dodE = n / (1 - e * cE)
    vox, voy = -a * sE * dodE, b * cE * dodE
    cw, sw = np.cos(w), np.sin(w)
    return cw * ox - sw * oy, sw * ox + cw * oy, cw * vox - sw * voy, sw * vox + cw * voy

def wrap(x):
    return np.mod(x + np.pi, TWO_PI) - np.pi

def true_lon(a, e, w, M0, t):
    """True longitude only (cheap: no rotation, no velocity)."""
    n = a**-1.5
    M = np.mod(M0 + n * t + np.pi, TWO_PI) - np.pi
    E = M + e * np.sin(M)
    for _ in range(5):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return w + np.arctan2(np.sqrt(1 - e * e) * np.sin(E), np.cos(E) - e)

def _dvw(a, e, w, M0, aj, ej, wj, Mj, t):
    """distance and |v_rel| at times t."""
    x1, y1, u1, v1 = kepler_state(a, e, w, M0, t)
    x2, y2, u2, v2 = kepler_state(aj, ej, wj, Mj, t)
    return np.hypot(x1 - x2, y1 - y2), np.hypot(u1 - u2, v1 - v2)

def _upd(wmin, dmin, vmin, idx, d, vr):
    z = d * vr
    better = z < wmin[idx]
    loc = idx[better]
    wmin[loc] = z[better]
    dmin[loc] = d[better]
    vmin[loc] = vr[better]

def _dth(ai, ei, wi, Mi, aj, ej, wj, Mj, t):
    return wrap(true_lon(ai, ei, wi, Mi, t) - true_lon(aj, ej, wj, Mj, t))

def _nu_off(e, M):
    """nu(M) - M for scalar e, array M (the equation of center)."""
    E = M.copy()
    for _ in range(6):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    nu = np.arctan2(np.sqrt(1 - e * e) * np.sin(E), np.cos(E) - e)
    return nu - M

DT_GRID = 0.35          # sample spacing inside bursts (bounds |wrap| at zeros <~ 0.7)
TBLOCK = 1024           # t-points per block (memory bound)

def _refine(G, ai, ei, wi, Mi, aj, ej, wj, Mj, t, p, ta, tb, fa, fb, mode):
    """Locate one event (crossing or graze of dtheta) inside [ta, tb], then
    Newton on d/dt(d^2) to the needle bottom. Returns event times."""
    if mode == "cross":
        tp, fp = ta.copy(), fa.copy()
        for _ in range(5):
            ft = _dth(ai[p], ei[p], wi[p], Mi[p], aj[p], ej[p], wj[p], Mj[p], t)
            dft = (ft - fp) / np.where(np.abs(t - tp) < 1e-13, np.full_like(t, 1e-13), t - tp)
            dft = np.where(dft >= 0, 1.0, -1.0) * np.maximum(np.abs(dft), 1e-12)
            tn = np.clip(t - ft / dft, ta, tb)
            tp, fp = t, ft
            t = tn
        clamp = 0.02
    else:
        tm = 0.5 * (ta + tb)
        fm = _dth(ai[p], ei[p], wi[p], Mi[p], aj[p], ej[p], wj[p], Mj[p], tm)
        den = fb - 2 * fm + fa
        safe = np.abs(den) > 1e-15
        tv = np.where(safe, tm - 0.5 * (tb - ta) * (fb - fa) / np.where(safe, den, 1.0), tm)
        t = np.clip(tv, ta, tb)
        clamp = 0.06
    for _ in range(3):
        x1, y1, u1, v1 = kepler_state(ai[p], ei[p], wi[p], Mi[p], t)
        x2, y2, u2, v2 = kepler_state(aj[p], ej[p], wj[p], Mj[p], t)
        g = (x1 - x2) * (u1 - u2) + (y1 - y2) * (v1 - v2)
        sl2 = np.maximum((u1 - u2)**2 + (v1 - v2)**2, 1e-12)
        t = t + np.clip(-g / sl2, -clamp, clamp)
        t = np.clip(t, ta - 0.1, tb + 0.1)
    return t


def _gate_chunk(job):
    """Every close approach in [0, H] per pair, under exact Kepler propagation.

    Conjunctions live where the mean-longitude difference sits inside the
    equation-of-center band (a linear-arithmetic mask); there the true-longitude
    difference oscillates and every crossing or graze near zero is an event.
    Deep minima of the distance are needles in time (width ~ d/v_rel), so events
    are located by root-finding on the smooth longitude difference and finished
    by Newton on d/dt(d^2); flagged intervals are re-gridded once because near
    needles the oscillation wiggles below the grid scale.
    """
    (ai, ei, wi, Mi, aj, ej, wj, Mj, dn, dL0, sgn, H) = job
    npair = len(ai)
    n1, n2 = ai**-1.5, aj**-1.5
    K = np.where(dn > 1e-12, np.floor(H * dn / TWO_PI) + 1.0, 0.0)
    K = np.minimum(K, 400)
    lev_rate = n1 - n2
    Mg = np.linspace(-np.pi, np.pi, 33)
    eoc_sup = np.array([np.abs(_nu_off(ee, Mg)).max() for ee in ei]) + \
              np.array([np.abs(_nu_off(ee, Mg)).max() for ee in ej]) + 0.02
    T = np.arange(0.0, H, DT_GRID)
    ev_p, ev_z, ev_d, ev_v = [], [], [], []
    for b0 in range(0, len(T), TBLOCK):
        Tb = T[b0:b0 + TBLOCK]
        lev = wrap(dL0[:, None] + lev_rate[:, None] * Tb[None, :])
        band2 = (eoc_sup + np.maximum(3.0 * np.abs(lev_rate) * DT_GRID, 0.05))[:, None]
        mask = np.abs(lev) < band2
        pm, tm_ = np.nonzero(mask)
        if len(pm) == 0:
            continue
        tt = Tb[tm_]
        dth = _dth(ai[pm], ei[pm], wi[pm], Mi[pm], aj[pm], ej[pm], wj[pm], Mj[pm], tt)
        same = pm[1:] == pm[:-1]
        gapok = np.abs(tt[1:] - tt[:-1]) < 2.0 * DT_GRID
        f1, f2 = dth[:-1], dth[1:]
        cross = same & gapok & (f1 * f2 < 0) & (np.abs(f1) < 1.5) & (np.abs(f2) < 1.5)
        graze = same & gapok & (f1 * f2 > 0) & (np.abs(f1) < 0.7) & (np.abs(f2) < 0.7)
        for sel, mode in ((cross, "cross"), (graze, "graze")):
            if not sel.any():
                continue
            p = pm[1:][sel]
            ta, tb = tt[:-1][sel], tt[1:][sel]
            fa, fb = f1[sel], f2[sel]
            t = _refine(None, ai, ei, wi, Mi, aj, ej, wj, Mj, 0.5 * (ta + tb), p, ta, tb, fa, fb, mode)
            d, vr = _dvw(ai[p], ei[p], wi[p], Mi[p], aj[p], ej[p], wj[p], Mj[p], t)
            ev_p.append(p); ev_z.append(d * vr); ev_d.append(d); ev_v.append(vr)
        # second pass: re-grid intervals that may hide sub-grid wiggles (needle nests)
        flag = same & gapok & (np.minimum(np.abs(f1), np.abs(f2)) < 0.05)
        if flag.any():
            p = pm[1:][flag]
            ta, tb = tt[:-1][flag], tt[1:][flag]
            sub = ta[:, None] + (tb - ta)[:, None] * (np.arange(13) / 12.0)[None, :]
            pex = np.repeat(p, 13)
            tex = sub.ravel()
            fex = _dth(ai[pex], ei[pex], wi[pex], Mi[pex], aj[pex], ej[pex], wj[pex], Mj[pex], tex)
            okc = (fex[:-1] * fex[1:] < 0) & (pex[1:] == pex[:-1]) & (np.abs(fex[:-1]) < 1.5) & (np.abs(fex[1:]) < 1.5)
            okg = (fex[:-1] * fex[1:] > 0) & (pex[1:] == pex[:-1]) & (np.minimum(np.abs(fex[:-1]), np.abs(fex[1:])) < 0.05)
            for sel2, mode2 in ((okc, "cross"), (okg, "graze")):
                if not sel2.any():
                    continue
                p2 = pex[1:][sel2]
                ta2, tb2 = tex[:-1][sel2], tex[1:][sel2]
                fa2, fb2 = fex[:-1][sel2], fex[1:][sel2]
                t = _refine(None, ai, ei, wi, Mi, aj, ej, wj, Mj, 0.5 * (ta2 + tb2), p2, ta2, tb2, fa2, fb2, mode2)
                d, vr = _dvw(ai[p2], ei[p2], wi[p2], Mi[p2], aj[p2], ej[p2], wj[p2], Mj[p2], t)
                ev_p.append(p2); ev_z.append(d * vr); ev_d.append(d); ev_v.append(vr)
    if ev_p:
        P = np.concatenate(ev_p); Z = np.concatenate(ev_z)
        D = np.concatenate(ev_d); V = np.concatenate(ev_v)
        ordv = np.lexsort((D, P))  # select by min miss distance d
        P, Z, D, V = P[ordv], Z[ordv], D[ordv], V[ordv]
        first = np.nonzero(np.r_[True, P[1:] != P[:-1]])[0]
        wmin = np.full(npair, np.inf)
        dmin = np.full(npair, np.inf)
        vmin = np.full(npair, np.inf)
        wmin[P[first]] = Z[first]
        dmin[P[first]] = D[first]
        vmin[P[first]] = V[first]
        pmin = P[first]
    else:
        wmin = np.full(npair, np.inf); dmin = wmin.copy(); vmin = wmin.copy(); pmin = np.arange(0)
    # pairs with no masked burst at all: mean separation never enters the eoc band;
    # probe a coarse sweep (their closest approach is far from any conjunction)
    seen = np.zeros(npair, bool)
    seen[pmin] = True
    miss = np.nonzero(~seen)[0]
    if len(miss):
        wm = np.full(len(miss), np.inf)
        dm = wm.copy()
        vm = wm.copy()
        for t in np.linspace(0, H, 17):
            tt2 = np.full(len(miss), t)
            d, vr = _dvw(ai[miss], ei[miss], wi[miss], Mi[miss], aj[miss], ej[miss], wj[miss], Mj[miss], tt2)
            z = d * vr
            b = z < wm
            wm[b] = z[b]
            dm[b] = d[b]
            vm[b] = vr[b]
        wmin[miss] = wm
        dmin[miss] = dm
        vmin[miss] = vm
    return wmin, dmin, vmin, K

def exact_gate(a, e, w, M0, i, j, H=H_TIME, nproc=6, chunk=1500):
    dn = np.abs(a[i]**-1.5 - a[j]**-1.5)
    dL0 = (M0[i] + w[i]) - (M0[j] + w[j])
    sgn = np.where(a[i]**-1.5 >= a[j]**-1.5, 1.0, -1.0)
    args = [(a[i][lo:lo + chunk], e[i][lo:lo + chunk], w[i][lo:lo + chunk], M0[i][lo:lo + chunk],
             a[j][lo:lo + chunk], e[j][lo:lo + chunk], w[j][lo:lo + chunk], M0[j][lo:lo + chunk],
             dn[lo:lo + chunk], dL0[lo:lo + chunk], sgn[lo:lo + chunk], H)
            for lo in range(0, len(i), chunk)]
    with Pool(nproc) as p:
        res = p.map(_gate_chunk, args)
    return (np.concatenate([r[0] for r in res]),
            np.concatenate([r[1] for r in res]),
            np.concatenate([r[2] for r in res]),
            np.concatenate([r[3] for r in res]))

def deleted_from(wmin, m, i, j, a, quant=Q48):
    vi, vj = a[i]**-0.5, a[j]**-0.5
    dEi = 4 * m[j] / (vi * wmin)
    dEj = 4 * m[i] / (vj * wmin)
    return (dEi < quant) & (dEj < quant), dEi, dEj

# ---------------- belt construction (author's, verbatim) ----------------

rng = np.random.default_rng(20261014)
rng_phase = np.random.default_rng(777)

def mass_of_D(D):
    return D**3 * np.pi / 6 * 2600.0 / MSUN

def dohnyani(n, dmin_, dmax_, slope=3.5):
    lo_, hi_ = dmin_**(-(slope - 1)), dmax_**(-(slope - 1))
    u = rng.random(n)
    return (lo_ + u * (hi_ - lo_))**(-1.0 / (slope - 1))

def candidate_pairs(a, e, npairs):
    peri_i, apo_i = a * (1 - e), a * (1 + e)
    ii = rng.integers(0, len(a), npairs * 3)
    jj = rng.integers(0, len(a), npairs * 3)
    ok = (ii != jj) & (peri_i[ii] < apo_i[jj]) & (peri_i[jj] < apo_i[ii])
    return ii[ok][:npairs], jj[ok][:npairs]

# ---------------- brute-force control ----------------

def brute_dmin(a1, e1, w1, M01, a2, e2, w2, M02, H=H_TIME, nsamp=1_000_000, rounds=4):
    t = np.linspace(0, H, nsamp)
    x1, y1, _, _ = kepler_state(np.full(nsamp, a1), np.full(nsamp, e1), np.full(nsamp, w1), np.full(nsamp, M01), t)
    x2, y2, _, _ = kepler_state(np.full(nsamp, a2), np.full(nsamp, e2), np.full(nsamp, w2), np.full(nsamp, M02), t)
    d = np.hypot(x1 - x2, y1 - y2)
    k = int(np.argmin(d))
    lo_, hi_ = t[max(k - 1, 0)], t[min(k + 1, nsamp - 1)]
    best = d[k]
    for _ in range(rounds):
        tt = np.linspace(lo_, hi_, 60)
        x1, y1, _, _ = kepler_state(np.full(60, a1), np.full(60, e1), np.full(60, w1), np.full(60, M01), tt)
        x2, y2, _, _ = kepler_state(np.full(60, a2), np.full(60, e2), np.full(60, w2), np.full(60, M02), tt)
        dd = np.hypot(x1 - x2, y1 - y2)
        kk = int(np.argmin(dd))
        lo_, hi_ = tt[max(kk - 1, 0)], tt[min(kk + 1, 59)]
        best = min(best, dd[kk])
    return best
