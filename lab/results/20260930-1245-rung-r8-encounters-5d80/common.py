"""Rung r8: finding encounters without work per orbit — common machinery.

One doll: single dominant mass (mu=1), 2D Newtonian Kepler.
Bodies: a in [1,1.5], e Rayleigh(sigma_e), random varpi, lambda0.
T = 20 orbital periods at a=1 (= 40*pi).

Reference ("truth"), all sound necessary conditions applied in order:
 1. rho-inflated radial ranges must overlap;
 2. timing: the mean-longitude difference sweeps [dlam0, dlam0+dn*T]; an
    encounter needs |delta-theta| <= eps(rho) at some t, and delta-theta =
    dlam + (nu-M)_i - (nu-M)_j with |nu-M| <= Qmax per body, so the sweep
    must pass within Qmax_i+Qmax_j+eps of a multiple of 2*pi;
 3. the two radial curves must be able to touch within rho at a common
    polar angle (exact min over theta, Newton-refined);
 4. windowed scans (~16 samples/orbit) around every conjunction catch all
    dtheta zeros and |dtheta| minima; each candidate is refined by Newton on
    d/dt (d^2) = 0 to machine precision. Sub-rho dips are the encounters.

All heavy loops are numpy-vectorised over pairs and times.
"""
import numpy as np

TWOPI = 2.0 * np.pi
T_TOTAL = 20.0 * TWOPI   # 20 orbital periods at a=1, mu=1

# ---------------------------------------------------------------- sampling

def draw_belt_params(rng):
    sigma_e = np.exp(rng.uniform(np.log(1e-3), np.log(3e-2)))
    rho = np.exp(rng.uniform(np.log(1e-5), np.log(3e-4)))
    return sigma_e, rho

def sample_belt(rng, N, sigma_e):
    """Draw order (frozen for this run): per body a, e, varpi, lambda0."""
    a = np.array([rng.uniform(1.0, 1.5) for _ in range(N)])
    u = np.array([rng.random() for _ in range(N)])
    e = sigma_e * np.sqrt(-2.0 * np.log(1.0 - u))       # Rayleigh
    varpi = np.array([rng.uniform(0.0, TWOPI) for _ in range(N)])
    lam0 = np.array([rng.uniform(0.0, TWOPI) for _ in range(N)])
    return a, e, varpi, lam0

# ---------------------------------------------------------------- Kepler

def kepler_E(M, e):
    M = np.mod(M, TWOPI)
    E = M + e * np.sin(M)
    for _ in range(14):
        dE = (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
        E = E - dE
        if np.max(np.abs(dE)) < 1e-14:
            break
    return E

def states(a, e, varpi, lam0, n, t):
    """Positions/velocities at times t. All args broadcast to a common shape.
    Returns x, y, vx, vy, theta, r."""
    M = lam0 - varpi + n * t
    E = kepler_E(M, e)
    cE, sE = np.cos(E), np.sin(E)
    denom = 1.0 - e * cE
    r = a * (1.0 - e * cE)
    nu = np.arctan2(np.sqrt(1.0 - e * e) * sE, cE - e)
    th = varpi + nu
    cw, sw = np.cos(varpi), np.sin(varpi)
    xo = a * (cE - e); yo = a * np.sqrt(1.0 - e * e) * sE
    vo = n * a / denom
    vxo = -vo * sE; vyo = vo * np.sqrt(1.0 - e * e) * cE
    x = xo * cw - yo * sw
    y = xo * sw + yo * cw
    vx = vxo * cw - vyo * sw
    vy = vxo * sw + vyo * cw
    return x, y, vx, vy, th, r

# ---------------------------------------------------------------- pairs

def overlap_pairs(a, e, rho, pad=0.0):
    """Pairs whose rho-inflated radial ranges (padded by `pad`) overlap.
    Returns i, j arrays (body indices), each pair once with i<j."""
    lo = a * (1.0 - e) - rho - pad
    hi = a * (1.0 + e) + rho + pad
    order = np.argsort(lo)
    los, his = lo[order], hi[order]
    N = len(a)
    right = np.searchsorted(los, his, side='right')
    ii, jj = [], []
    for k in range(N):
        m = right[k]
        if m == 0:
            continue
        om = order[:m]
        keep = his[:m] >= los[k]
        om = om[keep]
        ok = order[k]
        sel = om[om > ok]
        if sel.size:
            ii.append(np.full(sel.size, ok, dtype=np.int64))
            jj.append(sel.astype(np.int64))
    if not ii:
        return np.empty(0, np.int64), np.empty(0, np.int64)
    return np.concatenate(ii), np.concatenate(jj)

# ------------------------------------------------- timing filter (sound)

def qmax_body(e):
    """max_M |nu - M| (equation of centre), exact closed form, +2% safety."""
    e = np.asarray(e, float)
    cosE = np.where(e > 1e-8, (1.0 - (1.0 - e * e) ** 0.25) / np.maximum(e, 1e-12), 0.0)
    cosE = np.clip(cosE, -1.0, 1.0)
    Ea = np.arccos(cosE)
    out = np.zeros_like(e)
    for E in (Ea, TWOPI - Ea):
        nu = np.mod(np.arctan2(np.sqrt(1.0 - e * e) * np.sin(E), np.cos(E) - e), TWOPI)
        M = E - e * np.sin(E)
        out = np.maximum(out, np.abs(nu - M))
    return 1.02 * out + 1e-9

def eps_rho(a, e, i, j, rho):
    rmi = a[i] * (1.0 - e[i]); rmj = a[j] * (1.0 - e[j])
    return 2.0 * np.arcsin(np.minimum(1.0, rho / (2.0 * np.sqrt(rmi * rmj))))

def align_bound(a, e, i, j, rho):
    return qmax_body(e[i]) + qmax_body(e[j]) + eps_rho(a, e, i, j, rho)

def timing_filter(i, j, a, e, lam0, rho, T):
    """Keep pairs whose mean-longitude sweep passes near a multiple of 2pi
    within the alignment bound (necessary for delta-theta ~ 0)."""
    n = a ** -1.5
    dlam0 = np.mod(lam0[i] - lam0[j], TWOPI)
    dn = n[i] - n[j]
    A = dlam0; B = dlam0 + dn * T
    lo = np.minimum(A, B) / TWOPI
    hi = np.maximum(A, B) / TWOPI
    flo = np.floor(lo)
    dist = np.where(np.floor(hi) > flo, 0.0,
                    np.minimum(lo - flo, flo + 1.0 - hi) * TWOPI)
    return dist <= align_bound(a, e, i, j, rho)

# ------------------------------------------------- geometric pair pre-filter

def _Bmax(a, e):
    """max |dr/dtheta| on the orbit (exact at cos nu = -2e), with 5% safety."""
    e2 = e * e
    val = a * (1.0 - e2) * e * np.sqrt(np.maximum(0.0, 1.0 - 4.0 * e2)) / (1.0 - 2.0 * e2) ** 2
    return 1.05 * val + 1e-12

def radial_curve(a, e, varpi, theta):
    nu = theta - varpi
    c, s = np.cos(nu), np.sin(nu)
    p = a * (1.0 - e * e)
    den = 1.0 + e * c
    return p / den, p * e * s / (den * den)

def g_filter(i, j, a, e, varpi, rho, chunk=200000):
    """Sound filter: keep pair only if the two radial curves can come within
    rho at a common polar angle. g = min_theta |r_i(theta)-r_j(theta)|,
    computed exactly (grid + Newton on extrema of the difference).
    Encounter => |r_i - r_j| < rho at slightly different angles
    => g < rho + (B_i+B_j)*dtheta_max. Discard only above that."""
    ai, ei, wi = a[i], e[i], varpi[i]
    aj, ej, wj = a[j], e[j], varpi[j]
    rmi, rmj = ai * (1 - ei), aj * (1 - ej)
    dth_max = 2.0 * np.arcsin(np.minimum(1.0, rho / (2.0 * np.sqrt(rmi * rmj))))
    G = rho + (_Bmax(ai, ei) + _Bmax(aj, ej)) * dth_max
    K = 96
    tg = np.linspace(0.0, TWOPI, K, endpoint=False)
    P = len(i)
    keep = np.zeros(P, dtype=bool)
    gval = np.empty(P)
    for s in range(0, P, chunk):
        sl = slice(s, min(P, s + chunk))
        ii_, jj_ = i[sl], j[sl]
        ri_g, dri_g = radial_curve(a[ii_][:, None], e[ii_][:, None], varpi[ii_][:, None], tg[None, :])
        rj_g, drj_g = radial_curve(a[jj_][:, None], e[jj_][:, None], varpi[jj_][:, None], tg[None, :])
        h = ri_g - rj_g
        dh = dri_g - drj_g
        g = np.min(np.abs(h), axis=1)
        cross = np.any(h[:, :-1] * h[:, 1:] < 0.0, axis=1) | np.any(h == 0.0, axis=1)
        g = np.where(cross, 0.0, g)
        m = dh[:, :-1] * dh[:, 1:] < 0.0
        pi_, si_ = np.nonzero(m)
        if pi_.size:
            th0 = 0.5 * (tg[si_] + tg[si_ + 1])
            ai2 = a[ii_[pi_]]; ei2 = e[ii_[pi_]]; wi2 = varpi[ii_[pi_]]
            aj2 = a[jj_[pi_]]; ej2 = e[jj_[pi_]]; wj2 = varpi[jj_[pi_]]
            for _ in range(3):
                _, dhi = radial_curve(ai2, ei2, wi2, th0)
                _, dhj = radial_curve(aj2, ej2, wj2, th0)
                d2 = dhi - dhj
                eps = 1e-6
                _, dhi_p = radial_curve(ai2, ei2, wi2, th0 + eps)
                _, dhj_p = radial_curve(aj2, ej2, wj2, th0 + eps)
                slope = (dhi_p - dhj_p - d2) / eps
                step = d2 / np.where(np.abs(slope) > 1e-12, slope, 1e-12)
                th0 = th0 - np.sign(step) * np.minimum(np.abs(step), 0.3)
            _, ri0 = radial_curve(ai2, ei2, wi2, th0)
            _, rj0 = radial_curve(aj2, ej2, wj2, th0)
            hh = np.abs(ri0 - rj0)
            order = np.argsort(pi_, kind='stable')
            pi_s, hh_s = pi_[order], hh[order]
            uniq, start = np.unique(pi_s, return_index=True)
            mins = np.minimum.reduceat(hh_s, start)
            g[uniq] = np.minimum(g[uniq], mins)
        gval[sl] = g
        keep[sl] = g < G[sl]
    return keep, gval

# ------------------------------------------------- dip machinery (the truth)

def dth_wrap(x):
    return np.mod(x + np.pi, TWOPI) - np.pi

def _empty_dips():
    z6 = np.empty(0, np.int64); z = np.empty(0, float)
    return dict(pair=z6, t=z, d=z.copy(), t_in=z.copy(), t_out=z.copy())

def _scan_windows(i, j, a, e, lam0, rho, T):
    """Conjunction-centred windows that must contain every possible dip.
    Returns window arrays (pair index, t0, t1)."""
    n = a ** -1.5
    dlam0 = np.mod(lam0[i] - lam0[j], TWOPI)
    dn = n[i] - n[j]
    A = dlam0; B = dlam0 + dn * T
    lo = np.minimum(A, B) / TWOPI
    hi = np.maximum(A, B) / TWOPI
    flo = np.floor(lo); fhi = np.floor(hi)
    Qm = align_bound(a, e, i, j, rho)
    mlo = (flo.astype(int) - 1).astype(np.int64)
    mhi = (fhi.astype(int) + 1).astype(np.int64)
    cnt = np.maximum(mhi - mlo + 1, 1)
    csum = np.concatenate([[0], np.cumsum(cnt)[:-1]])
    pidx = np.repeat(np.arange(len(i)), cnt)
    mrep = np.repeat(mlo, cnt) + (np.arange(int(cnt.sum())) - np.repeat(csum, cnt))
    adn = np.abs(dn[pidx])
    tau0 = Qm[pidx] / np.maximum(adn, 1e-300)
    big = (adn < Qm[pidx] / T) | (tau0 >= T)
    tk = (TWOPI * mrep - dlam0[pidx]) / np.where(adn > 0, dn[pidx], 1.0)
    t0 = np.where(big, 0.0, np.clip(tk - tau0, 0.0, T))
    t1 = np.where(big, T, np.clip(tk + tau0, 0.0, T))
    okw = t1 > t0
    return pidx[okw], t0[okw], t1[okw]

def find_encounters(i, j, a, e, varpi, lam0, rho, T=T_TOTAL):
    """For surviving pairs, find every dip of the distance below rho
    (windowed scans around conjunctions; Newton refinement of each candidate
    local minimum to machine precision). Returns per-dip arrays."""
    if len(i) == 0:
        return _empty_dips()
    n = a ** -1.5
    ai, ei, wi, li, ni = a[i], e[i], varpi[i], lam0[i], n[i]
    aj, ej, wj, lj, nj = a[j], e[j], varpi[j], lam0[j], n[j]
    thr_dth = 4.0 * max(1e-3, 2.0 * np.arcsin(min(1.0, rho / 2.0)) + 1e-6)

    wp, wt0, wt1 = _scan_windows(i, j, a, e, lam0, rho, T)
    if wp.size == 0:
        return _empty_dips()
    wlen = wt1 - wt0
    Sw = np.clip(np.ceil(wlen * 2.5).astype(int) + 3, 6, 500)
    total = int(Sw.sum())
    widx = np.repeat(np.arange(len(wp)), Sw)
    starts = np.concatenate([[0], np.cumsum(Sw)[:-1]])
    offs = np.arange(total) - np.repeat(starts, Sw)
    u = offs / np.repeat(Sw - 1.0, Sw)
    ts = wt0[widx] + u * wlen[widx]
    same = widx[1:] == widx[:-1]           # adjacency within one window
    edge = (offs == 0) | (offs == np.repeat(Sw - 1, Sw))

    cand_p, cand_t = [], []
    CH = 1 << 21
    for s in range(0, total, CH):
        e_ = min(total, s + CH)
        c = slice(s, e_)
        ii2 = wp[widx[c]]
        t2 = ts[c]
        xi, yi, _, _, thi, _ = states(ai[ii2], ei[ii2], wi[ii2], li[ii2], ni[ii2], t2)
        xj, yj, _, _, thj, _ = states(aj[ii2], ej[ii2], wj[ii2], lj[ii2], nj[ii2], t2)
        d = np.hypot(xi - xj, yi - yj)
        dth = dth_wrap(thi - thj)
        adth = np.abs(dth)
        ddstep = np.abs(np.diff(dth))
        adjf = np.zeros(e_ - s, dtype=bool)
        adjf[:-1] = same[s:e_ - 1]
        # (a) dtheta sign changes within a window
        m = (dth[:-1] * dth[1:] < 0.0) & (ddstep < np.pi) & adjf[:-1]
        q = np.nonzero(m)[0]
        cand_p.append(ii2[q])
        cand_t.append(0.5 * (t2[q] + t2[q + 1]))
        # (b) local |dtheta| minima below threshold
        mm = (adth[1:-1] <= adth[:-2]) & (adth[1:-1] <= adth[2:]) & (adth[1:-1] < thr_dth) \
             & adjf[:-2] & adjf[1:-1]
        q = np.nonzero(mm)[0] + 1
        cand_p.append(ii2[q])
        cand_t.append(t2[q])
        # (c) window-boundary samples with small d
        q = np.nonzero(edge[c] & (d < 4.0 * rho))[0]
        cand_p.append(ii2[q])
        cand_t.append(t2[q])
        # (d) local d minima below 10*rho
        md = (d[1:-1] <= d[:-2]) & (d[1:-1] <= d[2:]) & (d[1:-1] < 10.0 * rho) \
             & adjf[:-2] & adjf[1:-1]
        q = np.nonzero(md)[0] + 1
        cand_p.append(ii2[q])
        cand_t.append(t2[q])
    if not cand_p:
        return _empty_dips()
    cand_p = np.concatenate(cand_p)
    cand_t = np.concatenate(cand_t)
    if cand_p.size == 0:
        return _empty_dips()
    key = cand_p.astype(np.int64) * 2000000 + np.round(cand_t * 1e4).astype(np.int64)
    _, first = np.unique(key, return_index=True)
    cand_p, cand_t = cand_p[first], cand_t[first]

    # Newton refine on F(t) = drel . vrel = 0
    t = cand_t.copy()
    A, E, W, L, NN = ai[cand_p], ei[cand_p], wi[cand_p], li[cand_p], ni[cand_p]
    B, E2, W2, L2, NN2 = aj[cand_p], ej[cand_p], wj[cand_p], lj[cand_p], nj[cand_p]
    for _ in range(9):
        xi, yi, vxi, vyi, _, ri_ = states(A, E, W, L, NN, t)
        xj, yj, vxj, vyj, _, rj_ = states(B, E2, W2, L2, NN2, t)
        dx, dy = xi - xj, yi - yj
        dvx, dvy = vxi - vxj, vyi - vyj
        F = dx * dvx + dy * dvy
        Fp = dvx * dvx + dvy * dvy + dx * (-xi / ri_ ** 3 + xj / rj_ ** 3) \
             + dy * (-yi / ri_ ** 3 + yj / rj_ ** 3)
        step = F / np.where(np.abs(Fp) > 1e-14, Fp, 1e-14)
        t = np.clip(t - step, 0.0, T)
        if np.max(np.abs(step)) < 1e-14:
            break
    xi, yi, vxi, vyi, _, _ = states(A, E, W, L, NN, t)
    xj, yj, vxj, vyj, _, _ = states(B, E2, W2, L2, NN2, t)
    d = np.hypot(xi - xj, yi - yj)
    vrel = np.hypot(vxi - vxj, vyi - vyj)

    hit = d < rho
    if not np.any(hit):
        return _empty_dips()
    hp = cand_p[hit]; ht = t[hit]; hd = d[hit]; hv = vrel[hit]
    hA, hE, hW, hL, hN = ai[hp], ei[hp], wi[hp], li[hp], ni[hp]
    hB, hE2, hW2, hL2, hN2 = aj[hp], ej[hp], wj[hp], lj[hp], nj[hp]

    def _d(tt):
        xi, yi, _, _, _, _ = states(hA, hE, hW, hL, hN, tt)
        xj, yj, _, _, _, _ = states(hB, hE2, hW2, hL2, hN2, tt)
        return np.hypot(xi - xj, yi - yj)

    step = 2.0 * rho / np.maximum(hv, 1e-12) + 1e-12
    tlo = np.maximum(ht - step, 0.0)
    thi_ = np.minimum(ht + step, T)
    for _ in range(40):
        grow = _d(tlo) < rho
        st = np.where(grow, np.maximum(ht - tlo, 1e-12) * 2.0, 0.0)
        tlo = np.maximum(tlo - st, 0.0)
        grow = _d(thi_) < rho
        st = np.where(grow, np.maximum(thi_ - ht, 1e-12) * 2.0, 0.0)
        thi_ = np.minimum(thi_ + st, T)
        if not (np.any(_d(tlo) < rho) or np.any(_d(thi_) < rho)):
            break
    for _ in range(26):   # bisection
        mid = 0.5 * (tlo + ht)
        tlo = np.where(_d(mid) < rho, mid, tlo)
        mid = 0.5 * (ht + thi_)
        thi_ = np.where(_d(mid) < rho, mid, thi_)
    return dict(pair=hp, t=ht, d=hd, t_in=tlo, t_out=thi_)

# ------------------------------------------------- element-sort crossing count

def crossing_count(dlam0, dn, T):
    """Number of mean-longitude conjunctions in [0,T] (exact integer count)."""
    lo = np.minimum(dlam0, dlam0 + dn * T) / TWOPI
    hi = np.maximum(dlam0, dlam0 + dn * T) / TWOPI
    c = np.floor(hi + 1e-12) - np.ceil(lo - 1e-12) + 1.0
    return np.maximum(c, 0.0)

# ------------------------------------------------- shear-grid helpers

def shear_events_per_body(a, e, varpi, lam0, n, rho, T, base_r, S=1024):
    """Mean cell-change events per body per orbit for the co-rotating grid
    (r-bins and phi-bins of width rho). Radial-bin events: r sweeps its range
    twice per orbit => 2*levels(r-range). The phi' smooth path per residence
    uses the bin rotation at the interval's left edge (jump-free increment)."""
    t0 = T / 2.0
    dt = (TWOPI / S) / n
    ts = t0 + np.cumsum(np.concatenate([np.zeros((len(a), 1)),
                                        np.tile(dt[:, None], (1, S - 1))], axis=1), axis=1)
    _, _, _, _, th, r = states(a[:, None], e[:, None], varpi[:, None],
                               lam0[:, None], n[:, None], ts)
    dth = np.mod(np.diff(th, axis=1) + np.pi, TWOPI) - np.pi
    dsm = dth - r[:, :-1] ** -1.5 * dt[:, None]
    var = np.sum(np.abs(dsm), axis=1)
    rmin = a * (1 - e); rmax = a * (1 + e)
    Nlev = np.maximum(np.floor((rmax - base_r) / rho) - np.ceil((rmin - base_r) / rho) + 1.0, 0.0)
    Ebody = 2.0 * Nlev + var / rho
    return float(np.mean(Ebody))

def window_cellmask(dips, i, j, a, e, varpi, lam0, n, rho, kind, grid, T, S=64):
    """For each sub-rho dip, sample both bodies' cells through the window.
    shear: found if either body's co-rotating cell index changes in-window
    (the check then sees the partner within rho, i.e. same-or-adjacent cell).
    ring: found iff at some in-window cell change the partner occupies the
    changer's new cell (the rung's ring-cells checks only the new cell)."""
    P = dips['pair'].size
    if P == 0:
        return np.zeros(0, dtype=bool)
    found = np.zeros(P, dtype=bool)
    CH = 4096
    for s in range(0, P, CH):
        c = slice(s, min(P, s + CH))
        pi_ = dips['pair'][c]
        tin = dips['t_in'][c][:, None]; tout = dips['t_out'][c][:, None]
        w = np.maximum(tout - tin, 1e-9)
        ts = np.clip(tin + np.linspace(0, 1, S)[None, :] * w, 0.0, T)
        ii = i[pi_]; jj = j[pi_]
        if kind == 'shear':
            base_r = grid
            chg_any = np.zeros(len(pi_), dtype=bool)
            for body in (ii, jj):
                x, y, _, _, th, r = states(a[body][:, None], e[body][:, None],
                                           varpi[body][:, None], lam0[body][:, None],
                                           n[body][:, None], ts)
                rb = np.clip(np.floor((r - base_r) / rho), 0, None)
                nb = (base_r + (rb + 0.5) * rho) ** -1.5
                pp = np.mod(th - nb * ts, TWOPI) / rho
                cell = np.stack([rb, pp], axis=-1)
                chg_any |= np.any(np.any(np.abs(np.diff(cell, axis=1)) > 0, axis=-1), axis=1)
            found[c] = chg_any
        else:
            r0, w_ring, w_spk = grid
            cellA = []; cellB = []
            for body, store in ((ii, cellA), (jj, cellB)):
                x, y, _, _, th, r = states(a[body][:, None], e[body][:, None],
                                           varpi[body][:, None], lam0[body][:, None],
                                           n[body][:, None], ts)
                rb = np.clip(np.floor((r - r0) / w_ring), 0, 15)
                sp = np.mod(th, TWOPI) / w_spk
                store.append(np.stack([rb, sp], axis=-1))
            eq = (np.floor(cellA[0]) == np.floor(cellB[0])).all(axis=-1)  # (P,S)
            chgA = np.any(np.abs(np.diff(cellA[0], axis=1)) > 0, axis=-1)
            chgB = np.any(np.abs(np.diff(cellB[0], axis=1)) > 0, axis=-1)
            okA = np.any(chgA & eq[:, 1:], axis=1)
            okB = np.any(chgB & eq[:, 1:], axis=1)
            found[c] = okA | okB
    return found

# ------------------------------------------------- run one belt end-to-end

def analyse_belt(a, e, varpi, lam0, rho, T=T_TOTAL, Ws=None, keep_dips=False):
    """Returns dict with reference encounters and per-configuration results."""
    N = len(a)
    n = a ** -1.5
    orbits = T / TWOPI
    # ---- reference: overlap -> timing -> geometric -> exact dips
    i, j = overlap_pairs(a, e, rho, pad=0.0)
    tkeep = timing_filter(i, j, a, e, lam0, rho, T)
    i, j = i[tkeep], j[tkeep]
    keep, _ = g_filter(i, j, a, e, varpi, rho)
    i, j = i[keep], j[keep]
    dips = find_encounters(i, j, a, e, varpi, lam0, rho, T=T)
    ref_pairs = np.unique(dips['pair']) if dips['pair'].size else np.empty(0, np.int64)
    ref_set = set(ref_pairs.tolist())
    E_ref = len(ref_set)

    out = dict(N=N, rho=rho, ref_encounters=E_ref, dip_count=int(dips['pair'].size))

    # ---- element-sort --------------------------------------------------
    reach = 2.0 * a * e + 2.0 * rho
    W0 = max(rho, float(np.median(reach)))
    if Ws is None:
        Ws = [W0]
    best = None
    for Wc in Ws:
        ci, cj = overlap_pairs(a, e, rho, pad=2.2 * Wc)
        if ci.size:
            lo_i = a[ci] * (1 - e[ci]) - rho; hi_i = a[ci] * (1 + e[ci]) + rho
            lo_j = a[cj] * (1 - e[cj]) - rho; hi_j = a[cj] * (1 + e[cj]) + rho
            base = min(lo_i.min(), lo_j.min()) - Wc
            ki0 = np.floor((lo_i - base) / Wc).astype(int); ki1 = np.floor((hi_i - base) / Wc).astype(int)
            kj0 = np.floor((lo_j - base) / Wc).astype(int); kj1 = np.floor((hi_j - base) / Wc).astype(int)
            co = (ki0 <= kj1) & (kj0 <= ki1)     # bin-index ranges intersect
            ci, cj = ci[co], cj[co]
            dlam0 = np.mod(lam0[ci] - lam0[cj], TWOPI)
            dn = n[ci] - n[cj]
            c_cnt = crossing_count(dlam0, dn, T)
            events = 2.0 * float(np.sum(c_cnt))     # swap + exact check per conjunction
        else:
            events = 0.0
        if best is None or events < best[0]:
            best = (events, Wc)
    events_es, W_used = best
    det = np.zeros(max(dips['pair'].size, 0), dtype=bool)
    if dips['pair'].size:
        dp = dips['pair']; dt_ = dips['t']
        dlam0 = np.mod(lam0[i[dp]] - lam0[j[dp]], TWOPI)
        dn = n[i[dp]] - n[j[dp]]
        ok = np.abs(dn) > 0
        mstar = np.round((dlam0 + dn * dt_) / TWOPI)
        tk = (TWOPI * mstar - dlam0) / np.where(ok, dn, 1.0)
        ee = e[i[dp]] + e[j[dp]]
        tau = (3.0 * ee + 8.0 * rho) / np.where(ok, np.abs(dn), 1.0)
        det = ok & (tk >= 0.0) & (tk <= T) & (np.abs(dt_ - tk) <= tau)
    es_found = np.unique(dips['pair'][det]) if det.any() else np.empty(0, np.int64)
    out['element-sort'] = dict(events=events_es, W=W_used,
                               found=len(es_found), missed=E_ref - len(es_found),
                               false=len(set(es_found.tolist()) - ref_set))

    # ---- shear-grid ------------------------------------------------------
    base_r = float((a * (1 - e)).min() - rho - 1e-9)
    E_body = shear_events_per_body(a, e, varpi, lam0, n, rho, T, base_r)
    events_sh = N * (1.0 + orbits * E_body)         # initial pass + cell changes
    found_sh = window_cellmask(dips, i, j, a, e, varpi, lam0, n, rho,
                               'shear', base_r, T)
    fsh = np.unique(dips['pair'][found_sh]) if found_sh.any() else np.empty(0, np.int64)
    out['shear-grid'] = dict(events=events_sh, found=len(fsh),
                             missed=E_ref - len(fsh),
                             false=len(set(fsh.tolist()) - ref_set))

    # ---- ring-cells (negative) -------------------------------------------
    r0 = base_r
    r1 = float((a * (1 + e)).max() + rho + 1e-9)
    w_ring = (r1 - r0) / 16.0
    w_spk = TWOPI / 128.0
    Nlev = np.maximum(np.floor((a * (1 + e) - r0) / w_ring) -
                      np.ceil((a * (1 - e) - r0) / w_ring) + 1.0, 0.0)
    cross = 128.0 + 2.0 * Nlev                    # spokes + ring crossings per orbit
    occ = N / 2048.0
    events_rc = N * (1.0 + occ) + orbits * (float(np.sum(cross)) * (1.0 + occ))
    found_rc = window_cellmask(dips, i, j, a, e, varpi, lam0, n, rho,
                               'ring', (r0, w_ring, w_spk), T)
    frc = np.unique(dips['pair'][found_rc]) if found_rc.any() else np.empty(0, np.int64)
    out['ring-cells'] = dict(events=events_rc, found=len(frc),
                             missed=E_ref - len(frc),
                             false=len(set(frc.tolist()) - ref_set))

    # ---- oracle -----------------------------------------------------------
    out['oracle'] = dict(events=float(E_ref), found=E_ref, missed=0, false=0)

    out['rate'] = E_ref / (N * orbits)
    if keep_dips:
        out['_dips'] = dips
        out['_pairs'] = (i, j)
    return out
