#!/usr/bin/env python3
"""Second-author probe: the rotation certificate under real kicks (run 20261011-1102).

The checker's gold experiment for 20261011-0924-library-9834: measure the retrigger
rate of the (rotation number, window, return times) certificate under the plane's
kick workload with the slack-skin element-change quanta, and test whether amortized
certificate work per real encounter stays O(1) including window rebuilds.

Physics (matches crates/encounters + the q-skin gold harness):
  - kick: a <- a*(1+eps*sign), e and varpi unchanged, mean anomaly continuous.
  - rate kappa kicks per body per orbit, plane eps=1e-6, kappa=0.3.
  - slack-skin quantum (q-skin): retrigger when 2*(path_i + path_j) >= s,
    s = 4*eps_u, path = accumulated |dU| in Binet units (U = 1/(a(1-e^2))).
  - truth: piecewise-exact Kepler (elements frozen between kicks), per-interval
    minimum distance with conjunction refinement (the original probe's method).

Certificate variants measured:
  - as-stated: record (r, W, gaps) frozen between skin retriggers, hits predicted
    by the frozen rotation. -> phase-error retrigger quantum + miss audit.
  - repaired: exact phase/relative-longitude anchors updated per kick (O(1) arith),
    window W rebuilt at skin retriggers, padded by measured sensitivity.
Work is counted in Kepler-pair evaluations (one position solve for both bodies +
distance); arithmetic (phase updates, Diophantine jumps) counted separately and
converted at 1 arith = 0.01 eval for headline ratios (stated).

Outputs results2.json next to this file. Config ids as command-line args.
"""
import numpy as np, json, time, os, sys, zlib

TAU = 2 * np.pi
S = 48            # samples per interval for truth dmin
WPH = 64          # phases for the window scan at rebuild
SEED0 = 20261011
KAPPA = 0.3       # kicks per body per orbit (the plane's rate, q-skin harness)

# ---------------------------------------------------------------- Kepler

def kepler_pos(a, e, w, M):
    """Inertial position + true longitude from mean anomaly (vectorized).
    NOTE: the original probe returned perifocal x,y and never rotated by varpi,
    so its pair distances were computed across mismatched frames (it simulated
    aligned-pericenter pairs while claiming random varpi). Here positions are
    rotated into the inertial frame; u and D0 are consistent with them."""
    E = np.asarray(M, dtype=float).copy()
    for _ in range(6):
        E -= (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    xp = a * (np.cos(E) - e)
    yp = a * np.sqrt(1 - e * e) * np.sin(E)
    cw, sw = np.cos(w), np.sin(w)
    x = xp * cw - yp * sw
    y = xp * sw + yp * cw
    nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
    return x, y, w + nu

# ---------------------------------------------------------------- body timeline (kicks)
def at_longitude(a, e, w, lam):
    """State (x, y, vx, vy, r) of a Kepler body at true longitude lam (vectorized)."""
    nu = lam - w
    E = 2 * np.arctan2(np.sqrt(1 - e) * np.sin(nu / 2), np.sqrt(1 + e) * np.cos(nu / 2))
    n = TAU * a ** -1.5
    Edot = n / (1 - e * np.cos(E))
    xp = a * (np.cos(E) - e); yp = a * np.sqrt(1 - e * e) * np.sin(E)
    vxp = -a * np.sin(E) * Edot; vyp = a * np.sqrt(1 - e * e) * np.cos(E) * Edot
    cw, sw = np.cos(w), np.sin(w)
    x = xp * cw - yp * sw; y = xp * sw + yp * cw
    vx = vxp * cw - vyp * sw; vy = vxp * sw + vyp * cw
    return x, y, vx, vy, a * (1 - e * np.cos(E))

def psi_arcs(a1, e1, w1, a2, e2, w2, R_th, npsi=128):
    """Encounter arcs in conjunction-longitude space (phase units): psi where the
    conjunction's radial gap or impact parameter is below R_th. Edges one cell out.
    Returns (arcs_in_phase_units, evals)."""
    psis = (np.arange(npsi) + 0.5) / npsi * TAU
    x1, y1, vx1, vy1, r1 = at_longitude(a1, e1, w1, psis)
    x2, y2, vx2, vy2, r2 = at_longitude(a2, e2, w2, psis)
    dr = np.abs(r1 - r2)
    dvx, dvy = vx1 - vx2, vy1 - vy2
    dv = np.hypot(dvx, dvy)
    with np.errstate(divide='ignore', invalid='ignore'):
        b = np.abs((x1 - x2) * dvy - (y1 - y2) * dvx) / np.maximum(dv, 1e-300)
    inside = (dr < R_th) | (b < R_th)
    arcs = []
    i = 0
    while i < npsi:
        if inside[i]:
            j = i
            while j < npsi and inside[j]:
                j += 1
            arcs.append([(i - 1) / npsi, (j + 1) / npsi])
            i = j
        else:
            i += 1
    if len(arcs) > 1 and arcs[0][0] <= -0.5 / npsi and arcs[-1][1] >= 1 + 0.5 / npsi:
        arcs[0][0] = arcs[-1][0] - 1.0
        arcs.pop()
    return arcs, 2 * npsi

def make_kicks(rng, T, kappa, eps):
    """Kick schedule: Poisson(kappa*T) kicks, fractional a-change +-eps, uniform times.
    (Distribution-equivalent to the q-skin harness's per-orbit Bernoulli; vectorized.)"""
    n = rng.poisson(kappa * T)
    times = np.sort(rng.uniform(0.0, T, n))
    ks = eps * rng.choice([-1.0, 1.0], n)
    return times, ks

class Body:
    """Piecewise-exact Kepler body: a changes at kick times, M continuous."""
    def __init__(self, a0, e, w, M0, kick_t, kick_s):
        self.e, self.w = e, w
        kt = np.asarray(kick_t, float)
        ks = np.asarray(kick_s, float)
        a_seg = np.concatenate(([a0], a0 * np.cumprod(1.0 + ks))) if len(kt) else np.array([a0])
        n_seg = TAU * a_seg ** -1.5
        dt = np.diff(np.concatenate(([0.0], kt))) if len(kt) else np.array([])
        Mcum = M0 + np.concatenate(([0.0], np.cumsum(n_seg[:-1] * dt))) if len(kt) else np.array([M0])
        self.kt, self.a_seg, self.n_seg, self.Mcum = kt, a_seg, n_seg, Mcum

    def state(self, t):
        """(M, a, n) at times t (vectorized)."""
        if len(self.kt) == 0:
            return (self.Mcum[0] + self.n_seg[0] * np.asarray(t, float),
                    np.full(np.shape(t), self.a_seg[0]), np.full(np.shape(t), self.n_seg[0]))
        i = np.searchsorted(self.kt, t, side='right')
        left = np.where(i > 0, self.kt[np.maximum(i - 1, 0)], 0.0)
        M = self.Mcum[i] + self.n_seg[i] * (t - left)
        return M, self.a_seg[i], self.n_seg[i]


    def binet_path_after_kicks(self):
        """|dU| path after each kick (len = #kicks)."""
        U = 1.0 / (self.a_seg * (1 - self.e ** 2))
        return np.abs(np.diff(U)) if len(self.kt) else np.array([])


# ---------------------------------------------------------------- geometry helpers

def eps_u(a1, e1, a2, e2, rho):
    """Cone epsilon in Binet units (crates/encounters/src/pairs.rs)."""
    rmin = min(a1 * (1 - e1), a2 * (1 - e2))
    rmax = max(a1 * (1 + e1), a2 * (1 + e2))
    emax = max(e1, e2)
    pmin = min(a1 * (1 - e1 ** 2), a2 * (1 - e2 ** 2))
    kap = rmax * rmax * emax / (pmin * rmin)
    return 1.5 * rho * (1.0 + kap) / (rmin * rmin)

# ---------------------------------------------------------------- window (frozen model)

def dmin_frozen(th, a1, e1, w1, a2, e2, w2, D0, Ts, n1, n2, SS=24):
    """Per-interval minimum distance of the FROZEN pair at strobe phase(s) th:
    samples the interval, refines at true-longitude sign changes (the truth
    pass's method, on the frozen model). Vectorized over th. Returns (dmin, evals)."""
    th = np.atleast_1d(np.asarray(th, float))
    M1 = TAU * th
    M2 = (w1 - D0 - w2) + TAU * th          # so that L1-L2 = D0 at tau=0
    tt = (np.arange(SS) + 0.5) * (Ts / SS)
    M1t = M1[None, :] + n1 * tt[:, None]
    M2t = M2[None, :] + n2 * tt[:, None]
    x1, y1, l1 = kepler_pos(a1, e1, w1, M1t)
    x2, y2, l2 = kepler_pos(a2, e2, w2, M2t)
    dist = np.hypot(x1 - x2, y1 - y2)
    u = np.mod(l1 - l2 + np.pi, TAU) - np.pi
    d = dist.min(axis=0).astype(float)
    m = (u[:-1, :] * u[1:, :] <= 0) & (u[:-1, :] != u[1:, :])
    rr, cc = np.nonzero(m)          # rr: time-sample index, cc: phase index
    nref = 0
    if len(rr):
        u0, u1_ = u[rr, cc], u[rr + 1, cc]
        tc = tt[rr] + (u0 / (u0 - u1_)) * (Ts / SS)
        M1c = M1[cc] + n1 * tc; M2c = M2[cc] + n2 * tc
        xc1, yc1, _ = kepler_pos(a1, e1, w1, M1c)
        xc2, yc2, _ = kepler_pos(a2, e2, w2, M2c)
        np.minimum.at(d, cc, np.hypot(xc1 - xc2, yc1 - yc2))
        nref = len(rr)
    return d, 2 * SS * len(th) + 2 * nref

def window_scan(a1, e1, w1, a2, e2, w2, D0, R_th, nph=WPH):
    """Tight window arcs (strobed-phase units): phases whose frozen-model interval
    holds an encounter (< R_th), edges pushed outward by one grid cell. + eval count."""
    n1 = TAU * a1 ** -1.5; n2 = TAU * a2 ** -1.5
    if abs(n1 - n2) < 1e-14:
        return [], 0, (n1, n2, 1.0)
    Ts = TAU / abs(n1 - n2)
    thg = (np.arange(nph) + 0.5) / nph
    d, ev = dmin_frozen(thg, a1, e1, w1, a2, e2, w2, D0, Ts, n1, n2)
    inside = d < R_th
    arcs = []
    i = 0
    while i < nph:
        if inside[i]:
            j = i
            while j < nph and inside[j]:
                j += 1
            arcs.append([(i - 1) / nph, (j + 1) / nph])   # one cell outward each side
            i = j
        else:
            i += 1
    if len(arcs) > 1 and arcs[0][0] <= -0.5 / nph and arcs[-1][1] >= 1 + 0.5 / nph:
        arcs[0][0] = arcs[-1][0] - 1.0
        arcs.pop()
    return arcs, ev, (n1, n2, Ts)


def in_arcs(th, arcs):
    if not arcs:
        return np.zeros(len(th), bool)
    z = np.mod(th, 1.0)
    ins = np.zeros(len(z), bool)
    for lo, hi in arcs:
        if hi <= 1.0:
            ins |= (z >= lo) & (z <= hi)
        else:
            ins |= (z >= lo) | (z <= hi - 1.0)
    return ins

# ---------------------------------------------------------------- per-pair run

def run_pair(a1, e1, w1, M10, a2, e2, w2, M20, kicks1, kicks2, T, rho, R_th):
    b1 = Body(a1, e1, w1, M10, *kicks1)
    b2 = Body(a2, e2, w2, M20, *kicks2)

    # ---- skin-retrigger epochs: 2*(path1+path2) >= s (paths are nondecreasing step fns)
    p1t, p2t = b1.kt, b2.kt
    cum1 = np.concatenate(([0.0], np.cumsum(b1.binet_path_after_kicks())))
    cum2 = np.concatenate(([0.0], np.cumsum(b2.binet_path_after_kicks())))
    epochs = []
    t = 0.0
    guard = 0
    while t < T and guard < 100000:
        guard += 1
        M1, A1, n1 = b1.state(np.array([t])); M2, A2, n2 = b2.state(np.array([t]))
        A1, A2, n1, n2 = A1[0], A2[0], n1[0], n2[0]
        M1, M2 = M1[0], M2[0]
        s_skin = 4.0 * eps_u(A1, e1, A2, e2, rho)
        dn = n1 - n2
        if abs(dn) < 1e-13:
            break
        Ts = TAU / abs(dn)
        D0 = np.mod((w1 + M1) - (w2 + M2), TAU)
        # joint path (relative to this epoch's start) at each future kick time
        j1 = np.searchsorted(p1t, t, side='right'); j2 = np.searchsorted(p2t, t, side='right')
        base1 = cum1[j1] if j1 < len(cum1) else cum1[-1]
        base2 = cum2[j2] if j2 < len(cum2) else cum2[-1]
        all_t = np.concatenate((p1t[j1:], p2t[j2:]))
        if len(all_t):
            all_t.sort()
            i1 = np.searchsorted(p1t, all_t, side='right')
            i2 = np.searchsorted(p2t, all_t, side='right')
            path = (cum1[i1] - base1) + (cum2[i2] - base2)
            trig = np.nonzero(2.0 * path >= s_skin)[0]
            t_next = float(all_t[trig[0]]) if len(trig) else T
        else:
            t_next = T
        t_next = min(t_next, T)
        if t_next <= t + 1e-9:
            t_next = t + 1e-9
        epochs.append(dict(t0=t, t1=t_next, Ts=Ts, D0=D0, a1=A1, a2=A2, s=s_skin / 2.0))
        t = t_next
    if not epochs:
        return None

    # ---- interval grid: per-epoch strobe at that epoch's synodic period
    tb, ep_of, Ts_arr = [], [], []
    for ei, ep in enumerate(epochs):
        n_int = int(np.floor((ep['t1'] - ep['t0']) / ep['Ts'] + 1e-9))
        if n_int < 1:
            continue
        tj = ep['t0'] + ep['Ts'] * np.arange(n_int)
        tb.append(tj)
        ep_of.append(np.full(n_int, ei))
        Ts_arr.append(np.full(n_int, ep['Ts']))
    if not tb:
        return None
    tb = np.concatenate(tb); ep_of = np.concatenate(ep_of); Ts_arr = np.concatenate(Ts_arr)
    nint = len(tb)
    # ---- truth: per-interval dmin under the actual kicked dynamics
    tmid = tb[:, None] + (np.arange(S) + 0.5) * (Ts_arr / S)[:, None]
    ts = tmid.ravel()
    M1s, A1s, _ = b1.state(ts); M2s, A2s, _ = b2.state(ts)
    x1, y1, l1 = kepler_pos(A1s, e1, w1, M1s)
    x2, y2, l2 = kepler_pos(A2s, e2, w2, M2s)
    dist = np.hypot(x1 - x2, y1 - y2).reshape(nint, S)
    u = np.mod(l1 - l2 + np.pi, TAU).reshape(nint, S) - np.pi
    dmin = dist.min(axis=1).astype(float)
    m = (u[:, :-1] * u[:, 1:] <= 0) & (u[:, :-1] != u[:, 1:])
    rows, cols = np.nonzero(m)
    nref = 0
    if len(rows):
        u0, u1_ = u[rows, cols], u[rows, cols + 1]
        tj = tb[rows] + (cols + 0.5) * (Ts_arr[rows] / S)
        tc = tj + (u0 / (u0 - u1_)) * (Ts_arr[rows] / S)
        Mc1, Ac1, _ = b1.state(tc); Mc2, Ac2, _ = b2.state(tc)
        xc1, yc1, _ = kepler_pos(Ac1, e1, w1, Mc1)
        xc2, yc2, _ = kepler_pos(Ac2, e2, w2, Mc2)
        np.minimum.at(dmin, rows, np.hypot(xc1 - xc2, yc1 - yc2))
        nref = len(rows)
    hits = dmin < R_th
    scan_evals = nint * S + nref

    # ---- exact phases + per-interval rotation + relative longitudes
    M1b, A1b, n1j = b1.state(tb); M2b, A2b, n2j = b2.state(tb)
    M1e, _, _ = b1.state(tb + Ts_arr)
    th = np.mod(M1b / TAU, 1.0)
    r_j = np.mod(M1e - M1b, TAU) / TAU
    D_j = np.mod((w1 + M1b) - (w2 + M2b), TAU)
    dn_j = n1j - n2j
    dt_c = np.mod(-D_j * np.sign(dn_j), TAU) / np.maximum(np.abs(dn_j), 1e-300)
    psi = np.mod(w1 + M1b + n1j * dt_c, TAU) / TAU   # conjunction longitude (phase units)
    return dict(epochs=epochs, nint=nint, dmin=dmin, hits=hits, th=th, r_j=r_j, psi=psi,
                da_frac=abs(a1 - a2) / a1, n_kicks_tot=len(b1.kt) + len(b2.kt),
                D_j=D_j, ep_of=ep_of, scan_evals=scan_evals,
                b1=b1, b2=b2, tb=tb, Ts_arr=Ts_arr)

# ---------------------------------------------------------------- certificate accounting

def certify(res, e1, w1, e2, w2, rho, R_th):
    """Two certificates under real kicks, uniform work units (Kepler-pair evals;
    arithmetic converted at 1 arith = 0.01 eval, stated in the dossier).

    as-stated (the original claim's record): theta-space window W_theta built from
    the frozen model at each skin retrigger (the original probe's own construction,
    charged at its 64-phase scan cost), hits predicted by the frozen rotation
    (theta_0, r_0). Falsified by the phase-error quantum: the frozen rotation
    mispredicts phases after ~T_phase intervals.

    repaired (psi): exact anchors per kick (O(1) arith), closed-form encounter arcs
    in conjunction-longitude space (radial gap + impact parameter), rebuilt whenever
    the net Binet displacement crosses one arc cell. Valid where the relative
    longitude rate does not reverse (e_max <~ 0.75*da/a); the reversal regime is
    reported separately (the record must be 2D there)."""
    epochs = res['epochs']; ep_of = res['ep_of']; hits = res['hits']
    psi = res['psi']; th = res['th']; r_j = res['r_j']
    n_ep = len(epochs)
    comp = list(range(n_ep)) if n_ep <= 6 else sorted(set(np.linspace(0, n_ep - 1, 6).astype(int).tolist()))

    # ---------- as-stated: theta windows from the frozen model (charged) ----------
    as_miss = 0; as_pred_n = 0; phase_retrig = []; w_widths = []
    th_evals = 0
    for ei in comp:
        ep = epochs[ei]
        sel = np.nonzero(ep_of == ei)[0]
        if len(sel) == 0:
            continue
        n1 = TAU * ep['a1'] ** -1.5; n2 = TAU * ep['a2'] ** -1.5
        Ts = TAU / abs(n1 - n2)
        NPH = 256
        thg = (np.arange(NPH) + 0.5) / NPH
        d, ev = dmin_frozen(thg, ep['a1'], e1, w1, ep['a2'], e2, w2, ep['D0'], Ts, n1, n2, SS=24)
        th_evals += ev
        inside = d < R_th
        arcsT = []
        i = 0
        while i < NPH:
            if inside[i]:
                j = i
                while j < NPH and inside[j]:
                    j += 1
                arcsT.append([(i - 1) / NPH, (j + 1) / NPH]); i = j
            else:
                i += 1
        if len(arcsT) > 1 and arcsT[0][0] <= -0.5/NPH and arcsT[-1][1] >= 1 + 0.5/NPH:
            arcsT[0][0] = arcsT[-1][0] - 1.0; arcsT.pop()
        w_widths += [h - l for l, h in arcsT] or [0.0]
        if not arcsT:
            phase_retrig.append(len(sel)); continue
        th0 = th[sel[0]]; r0 = r_j[sel[0]]
        jj = sel - sel[0]
        pred = in_arcs(np.mod(th0 + r0 * jj, 1.0), arcsT)
        as_pred_n += int(pred.sum())
        as_miss += int((hits[sel] & ~pred).sum())
        err = np.abs(np.mod(th[sel] - (th0 + r0 * jj) + 0.5, 1.0) - 0.5)
        wslack = max(0.5 * max(h - l for l, h in arcsT), 0.01)
        beyond = np.nonzero(err > wslack)[0]
        phase_retrig.append(int(beyond[0]) if len(beyond) else len(sel))
    # extrapolate the charged rebuild cost to ALL epochs at the measured per-epoch cost
    per_epoch_evals = th_evals / max(len(comp), 1)
    T_phase = float(np.median(phase_retrig)) if phase_retrig else None
    as_rebuilds_total = res['nint'] / T_phase if T_phase else n_ep
    as_charged_eq = as_rebuilds_total * per_epoch_evals + 0.01 * 2 * (res['n_kicks_tot'])

    # ---------- repaired: psi arcs, closed form, cell-quantized rebuilds ----------
    cell = 1.0 / 128
    # count net-Binet-displacement cell crossings (rebuild trigger) per pair
    def cell_crossings(body):
        U = 1.0 / (body.a_seg * (1 - body.e ** 2))
        if len(U) <= 1:
            return 0, 0.0
        q = np.floor(U / (0.5 * cell)).astype(np.int64)
        changes = np.nonzero(np.diff(q) != 0)[0]
        return len(changes), float(np.max(U) - np.min(U))
    x1, rng1 = cell_crossings(res['b1']); x2, rng2 = cell_crossings(res['b2'])
    psi_rebuilds = max(x1 + x2, 1)
    arrivals = 0; arrivals_pad = 0; miss_cover = 0; false_alarm = 0
    miss_nonrev = 0; miss_rev = 0; n_rev = 0
    reversal = max(e1, e2) > 0.75 * abs(res['da_frac'])   # wobble > synodic rate
    for ei in range(n_ep):
        sel = ep_of == ei
        if not sel.any():
            continue
        ep = epochs[ei]
        arcs0, _ = psi_arcs(ep['a1'], e1, w1, ep['a2'], e2, w2, R_th)
        if not arcs0:
            continue
        pad = 1.5 * cell
        arcs = [(lo - pad, hi + pad) for lo, hi in arcs0]
        ins = in_arcs(psi[sel], arcs)
        arrivals += int(ins.sum())
        tight = [(l + pad, h - pad) for l, h in arcs]
        insT = in_arcs(psi[sel], tight) if all(h > l for l, h in tight) else np.zeros(int(sel.sum()), bool)
        arrivals_pad += int((ins & ~insT).sum())
        m = int((hits[sel] & ~ins).sum())
        miss_cover += m
        false_alarm += int((ins & ~hits[sel]).sum())
        if reversal:
            miss_rev += m; n_rev += 1
        else:
            miss_nonrev += m
    n_kicks = res['n_kicks_tot']
    # per-kick anchor updates (2 bodies) + per-interval jump re-derivation + arc rebuilds
    psi_arith = 2 * n_kicks + res['nint'] + 40 * psi_rebuilds
    psi_evals = arrivals_pad * (S + 3) + 0.01 * psi_arith

    out = dict(nint=res['nint'], nhits=int(hits.sum()), n_ep=n_ep,
               phase_retrig_med=T_phase,
               phase_retrig_min=float(np.min(phase_retrig)) if phase_retrig else None,
               as_miss=as_miss, as_pred_n=as_pred_n,
               as_charged_eq=as_charged_eq,
               miss_cover=miss_cover, miss_nonrev=miss_nonrev, miss_rev=miss_rev,
               reversal=bool(reversal),
               false_alarm=false_alarm, arrivals=arrivals, arrivals_pad=arrivals_pad,
               psi_rebuilds=psi_rebuilds, psi_evals=psi_evals,
               skin_retrig_intervals=res['nint'] / max(n_ep, 1),
               scan_evals=res['scan_evals'], n_kicks=n_kicks, gap_med=None,
               w_evals=th_evals)
    hk = np.nonzero(hits)[0]
    if len(hk) > 1:
        out['gap_med'] = float(np.median(np.diff(hk)))
    return out


# ---------------------------------------------------------------- configs

CONFIGS = {
    'A': dict(name='rho1e-4_plane',   rho=1e-4, R=1e-4, eps=1e-6, T=60000, npairs=300, da_lo=0.0008, da_hi=0.03),
    'B': dict(name='rho2e-3_plane',   rho=2e-3, R=2e-3, eps=1e-6, T=60000, npairs=300, da_lo=0.0008, da_hi=0.03),
    'C': dict(name='rho5e-3_plane',   rho=5e-3, R=5e-3, eps=1e-6, T=60000, npairs=300, da_lo=0.0008, da_hi=0.03),
    'D': dict(name='rho2e-3_eps1e-5', rho=2e-3, R=2e-3, eps=1e-5, T=6000,  npairs=300, da_lo=0.0008, da_hi=0.03),
    'E': dict(name='rho2e-3_eps1e-4', rho=2e-3, R=2e-3, eps=1e-4, T=600,   npairs=300, da_lo=0.0008, da_hi=0.03),
    'F': dict(name='coorbital',       rho=2e-3, R=2e-3, eps=1e-6, T=60000, npairs=100, da_lo=0.0005, da_hi=0.003),
    'G': dict(name='frozen_control',  rho=5e-3, R=5e-3, eps=0.0,  T=60000, npairs=300, da_lo=0.0008, da_hi=0.03),
}

def main():
    which = sys.argv[1:] or ['A']
    here = os.path.dirname(os.path.abspath(__file__))
    results = {}
    for cfg_id in which:
        cfg = CONFIGS[cfg_id]
        rng = np.random.default_rng(SEED0 + (zlib.crc32(cfg['name'].encode()) % 10000))
        t0 = time.time()
        recs = []
        for ip in range(cfg['npairs']):
            a1 = rng.uniform(0.97, 1.03)
            da = rng.uniform(cfg['da_lo'], cfg['da_hi']) * rng.choice([-1, 1])
            a2 = a1 + da
            if not (0.96 < a2 < 1.04):
                a2 = a1 - da
            e1, e2 = rng.uniform(0, 0.08), rng.uniform(0, 0.08)
            w1, w2 = rng.uniform(0, TAU), rng.uniform(0, TAU)
            M10, M20 = rng.uniform(0, TAU), rng.uniform(0, TAU)
            if cfg['eps'] == 0:
                k1 = k2 = (np.array([]), np.array([]))
            else:
                k1 = make_kicks(rng, cfg['T'], KAPPA, cfg['eps'])
                k2 = make_kicks(rng, cfg['T'], KAPPA, cfg['eps'])
            res = run_pair(a1, e1, w1, M10, a2, e2, w2, M20, k1, k2, cfg['T'], cfg['rho'], cfg['R'])
            if res is None:
                continue
            rec = certify(res, e1, w1, e2, w2, cfg['rho'], cfg['R'])
            rec['da'] = abs(da)
            recs.append(rec)
        tot = lambda k: float(sum(r[k] for r in recs))
        nrev = sum(1 for r in recs if r['reversal'])
        agg = dict(npairs=len(recs), nint=tot('nint'), nhits=tot('nhits'),
                   n_ep=tot('n_ep'), miss_cover=tot('miss_cover'),
                   miss_nonrev=tot('miss_nonrev'), miss_rev=tot('miss_rev'),
                   n_reversal_pairs=nrev,
                   false_alarm=tot('false_alarm'), as_miss=tot('as_miss'),
                   arrivals=tot('arrivals'), arrivals_pad=tot('arrivals_pad'),
                   psi_rebuilds=tot('psi_rebuilds'), psi_evals=tot('psi_evals'),
                   as_charged_eq=tot('as_charged_eq'),
                   scan_evals=tot('scan_evals'), n_kicks=tot('n_kicks'),
                   runtime_s=round(time.time() - t0, 1))
        for k in ('phase_retrig_med', 'phase_retrig_min', 'gap_med', 'skin_retrig_intervals'):
            vals = [r[k] for r in recs if r[k] is not None]
            agg[k] = float(np.median(vals)) if vals else None
            agg[k + '_min'] = float(np.min(vals)) if vals else None
        # uniform-unit ratios (scan baseline includes conjunction refinement)
        agg['scan_per_as_stated'] = agg['scan_evals'] / max(agg['as_charged_eq'], 1.0)
        agg['scan_per_psi'] = agg['scan_evals'] / max(agg['psi_evals'], 1.0)
        agg['as_per_encounter'] = agg['as_charged_eq'] / max(agg['nhits'], 1)
        agg['psi_per_encounter'] = agg['psi_evals'] / max(agg['nhits'], 1)
        agg['scan_per_encounter'] = agg['scan_evals'] / max(agg['nhits'], 1)
        results[cfg_id] = dict(cfg=cfg['name'], agg=agg, pairs=recs)
        print(json.dumps({cfg_id: {k: agg.get(k) for k in (
            'npairs', 'nint', 'nhits', 'n_ep', 'skin_retrig_intervals',
            'phase_retrig_med', 'phase_retrig_min', 'miss_cover', 'miss_nonrev',
            'miss_rev', 'n_reversal_pairs', 'false_alarm', 'as_miss',
            'scan_per_as_stated', 'scan_per_psi', 'as_per_encounter',
            'psi_per_encounter', 'scan_per_encounter', 'runtime_s')}},
            indent=1, default=float), flush=True)
    with open(os.path.join(here, 'results2.json'), 'w') as f:
        json.dump(results, f, indent=1, default=float)

if __name__ == '__main__':
    main()
