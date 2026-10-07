#!/usr/bin/env python3
"""H_live for a plane-like belt: distinctions (scars) created per body per year.

Architecture = the plane's: bodies coast on exact Kepler generators around the
star; the planet's residual field is applied as slab-sampled kicks (midpoint).
No integration of the dominant field: the null control (m_p=0) must show zero
element change at the roundtrip floor.

Units: GM_star = 1, AU, yr. 2D.
Outputs: scars per body per year at swept quanta, secular-reabsorbed residuals,
resonance fingerprint, field coherence over (a0, lam0) cells.
"""
import argparse, json
import numpy as np

def kepler_E(M, e, iters=4):
    E = M + e * np.sin(M)
    for _ in range(iters):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E

def elements_to_state(a, e, varpi, M, GM=1.0):
    E = kepler_E(M, e)
    cE, sE = np.cos(E), np.sin(E)
    n = np.sqrt(GM / a**3)
    Edot = n / (1 - e * cE)
    xd = a * (cE - e); yd = a * np.sqrt(1 - e * e) * sE
    vxd = -a * sE * Edot; vyd = a * np.sqrt(1 - e * e) * cE * Edot
    cw, sw = np.cos(varpi), np.sin(varpi)
    return (xd * cw - yd * sw, xd * sw + yd * cw,
            vxd * cw - vyd * sw, vxd * sw + vyd * cw)

def state_to_elements(x, y, vx, vy, GM=1.0):
    r = np.hypot(x, y); v2 = vx * vx + vy * vy
    a = 1.0 / (2.0 / r - v2 / GM)
    h = x * vy - y * vx
    ex = (vy * h / GM) - x / r
    ey = (-vx * h / GM) - y / r
    e = np.hypot(ex, ey)
    varpi = np.arctan2(ey, ex)
    rdotv = x * vx + y * vy
    ee = np.maximum(e, 1e-12)
    cosE = np.clip((1.0 - r / a) / ee, -1.0, 1.0)
    sinE = np.clip(rdotv / (ee * np.sqrt(np.maximum(GM * a, 1e-18))), -1.0, 1.0)
    E = np.arctan2(sinE, cosE)
    M = E - e * np.sin(E)
    return a, e, varpi, M

def run(N, years, dt, m_p, a_p, e_p, seed, belt=(2.0, 3.3, 0.05),
        snap_years=(1, 2, 5, 10, 20, 50, 100, 200, 500, 1000), keep_sub=2000):
    rng = np.random.default_rng(seed)
    GM = 1.0
    a = rng.uniform(belt[0], belt[1], N)
    e = np.minimum(rng.rayleigh(belt[2], N), 0.25)
    varpi = rng.uniform(0, 2 * np.pi, N)
    M = rng.uniform(0, 2 * np.pi, N)
    lam_p0 = rng.uniform(0, 2 * np.pi)
    wp = 0.3
    n_p = np.sqrt(GM / a_p**3)
    a0, e0, w0, M0 = a.copy(), e.copy(), varpi.copy(), M.copy()
    dvx = np.zeros(N); dvy = np.zeros(N)
    n_slabs = int(round(years / dt))
    sub = rng.choice(N, size=min(keep_sub, N), replace=False)
    snaps_t, snaps_dvx, snaps_dvy, snaps_a, snaps_e, snaps_w = [], [], [], [], [], []
    for k in range(n_slabs):
        t_mid = (k + 0.5) * dt
        M_now = M + np.sqrt(GM / a**3) * t_mid
        x, y, vx, vy = elements_to_state(a, e, varpi, M_now)
        Mp = lam_p0 - wp + n_p * t_mid
        Ep = kepler_E(Mp, e_p)
        xp = a_p * (np.cos(Ep) - e_p); yp = a_p * np.sqrt(1 - e_p**2) * np.sin(Ep)
        cp, sp = np.cos(wp), np.sin(wp)
        xpp, ypp = xp * cp - yp * sp, xp * sp + yp * cp
        dx, dy = xpp - x, ypp - y
        d3 = (dx * dx + dy * dy) ** 1.5
        dvx_k = m_p * dx / d3 * dt; dvy_k = m_p * dy / d3 * dt
        dvx += dvx_k; dvy += dvy_k
        aN, eN, wN, Mnow = state_to_elements(x, y, vx + dvx_k, vy + dvy_k)
        M = Mnow - np.sqrt(GM / aN**3) * t_mid   # epoch-0 mean anomaly
        a, e, varpi = aN, eN, wN
        if np.any(np.abs((k + 1) * dt - np.array(snap_years)) < dt / 2):
            snaps_t.append(round((k + 1) * dt, 6))
            snaps_dvx.append(dvx[sub].copy()); snaps_dvy.append(dvy[sub].copy())
            snaps_a.append(a[sub].copy()); snaps_e.append(e[sub].copy()); snaps_w.append(varpi[sub].copy())
    return dict(t=np.array(snaps_t), a0=a0[sub], e0=e0[sub], w0=w0[sub], M0=M0[sub],
                sub=sub, a0_all=a0, e0_all=e0, w0_all=w0,
                dvx=np.array(snaps_dvx), dvy=np.array(snaps_dvy),
                a=np.array(snaps_a), e=np.array(snaps_e), w=np.array(snaps_w),
                a_final=a, e_final=e, w_final=varpi,
                dvx_all=dvx, dvy_all=dvy)

def analyze(res):
    out = {}
    v0 = 1.0 / np.sqrt(res['a0'])              # per-body Kepler speed (GM=1)
    T = res['t']
    dv = np.hypot(res['dvx'], res['dvy'])
    out['n_sub'] = int(dv.shape[1])
    out['snap_years'] = T.tolist()
    out['rms_dv_over_v'] = (dv / v0[None, :]).std(axis=1).tolist()
    out['p99_dv_over_v_final'] = float(np.percentile(dv[-1] / v0, 99))
    da = (res['a'] - res['a0'][None, :]) / res['a0'][None, :]
    de = res['e'] - res['e0'][None, :]
    out['rms_da_over_a'] = np.sqrt((da ** 2).mean(axis=1)).tolist()
    out['rms_de'] = np.sqrt((de ** 2).mean(axis=1)).tolist()
    # secular reabsorption: smooth (pooled polynomial) forced-e field F(a) and
    # free precession rate g(a); fit on half the subsample, evaluate out-of-sample
    # on the other half so fit noise shows up instead of hiding.
    ec = res['e'] * np.exp(1j * res['w'])      # (S, n_sub)
    fit_m = np.zeros(ec.shape[1], dtype=bool); fit_m[::2] = True
    a_fit = res['a0'][fit_m]
    deg = 5
    def smooth_fit(a_all, y_all, deg):
        # poly fit on the fit-mask subset only, evaluate everywhere
        c = np.polyfit(a_fit - 2.65, y_all[fit_m], deg)
        return np.polyval(c, a_all - 2.65)
    F_Re = smooth_fit(res['a0'], ec.mean(axis=0).real, deg)
    F_Im = smooth_fit(res['a0'], ec.mean(axis=0).imag, deg)
    F = F_Re + 1j * F_Im
    free0 = ec[0] - F
    # g(a): per-body rotation angle over full span, median-binned then smoothed
    with np.errstate(invalid='ignore'):
        rot = (ec[-1] - F) * np.conj(free0)
    g_raw = np.where(np.abs(free0) > 1e-4, np.angle(rot) / max(T[-1] - T[0], 1e-9), 0.0)
    g = smooth_fit(res['a0'], g_raw, deg)
    T0 = T[0]
    model = F + free0[None, :] * np.exp(1j * g[None, :] * (T[:, None] - T0))
    resid_ec = ec - model
    # a-drift field: smooth median trend removed (2nd-order secular, refittable)
    med_a = np.array([np.median(da[si]) for si in range(len(T))])
    da_res = da - med_a[:, None]
    resid_e = np.abs(resid_ec)
    out['rms_resid_e'] = np.sqrt((resid_e ** 2).mean(axis=1)).tolist()
    out['rms_da_resid'] = np.sqrt((da_res ** 2).mean(axis=1)).tolist()
    # first-scar crossing times at swept quanta (residual vs reabsorbed program)
    qs = [1e-5, 1e-4, 1e-3, 3e-3, 1e-2]
    xstats = {}
    for q in qs:
        crossed = (np.abs(da_res) > q) | (resid_e > q)
        first = np.full(crossed.shape[1], np.inf)
        for si in range(crossed.shape[0]):
            new = crossed[si] & np.isinf(first)
            first[new] = T[si]
        frac = float(np.mean(np.isfinite(first)))
        xstats[f'q={q:g}'] = dict(frac_crossed=frac,
                                  rate_per_body_per_yr=frac / max(T[-1], 1e-9),
                                  median_first_cross_yr=(None if frac == 0 else float(np.median(first[np.isfinite(first)]))))
    RES = np.array([2.50, 2.82, 2.96, 3.28])
    near = np.zeros(res['a0'].shape[0], dtype=bool)
    for rc in RES:
        near |= np.abs(res['a0'] - rc) < 0.05
    oos = ~fit_m
    for q in qs:
        crossed = (np.abs(da_res) > q) | (resid_e > q)
        first = np.full(crossed.shape[1], np.inf)
        for si in range(crossed.shape[0]):
            new = crossed[si] & np.isinf(first)
            first[new] = T[si]
        for tag, m in (('all', np.ones_like(oos)), ('near', near & oos), ('far', (~near) & oos), ('insample', fit_m)):
            mm = m & oos if tag == 'all' else m
            if mm.sum() == 0: continue
            xstats[f'q={q:g}_{tag}'] = dict(
                frac_crossed=float(np.mean(np.isfinite(first[mm]))),
                rate_per_body_per_yr=float(np.mean(np.isfinite(first[mm])) / max(T[-1], 1e-9)))
    xstats['frac_near_resonance'] = float(near.mean())
    out['crossing'] = xstats
    xraw = {}
    for q in qs:
        crossed = (np.abs(da) > q) | (np.abs(de) > q)
        first = np.full(crossed.shape[1], np.inf)
        for si in range(crossed.shape[0]):
            new = crossed[si] & np.isinf(first)
            first[new] = T[si]
        xraw[f'q={q:g}'] = float(np.mean(np.isfinite(first)))
    out['crossing_raw_frac'] = xraw
    # resonance fingerprint by initial a (full population)
    dv_all = np.hypot(res['dvx_all'], res['dvy_all'])
    ab = np.arange(2.0, 3.31, 0.05)
    prof = []
    for lo, hi in zip(ab[:-1], ab[1:]):
        m = (res['a0_all'] >= lo) & (res['a0_all'] < hi)
        if m.sum() > 10:
            prof.append(dict(a_lo=float(lo), a_hi=float(hi), n=int(m.sum()),
                             med_dv=float(np.median(dv_all[m])),
                             p99_dv=float(np.percentile(dv_all[m], 99))))
    out['dv_profile_by_a'] = prof
    # coherence: cell-mean of cumulative kick field over (a0, lam0) cells
    lam0 = (res['M0'] + res['w0']) % (2 * np.pi)
    Fx_f = res['dvx'][-1]; Fy_f = res['dvy'][-1]
    tot = np.sqrt(np.var(Fx_f) + np.var(Fy_f))
    coh = {}
    for (wa, wl) in [(0.10, np.deg2rad(10)), (0.05, np.deg2rad(5)), (0.02, np.deg2rad(2))]:
        ia = np.round(res['a0'] / wa).astype(np.int64)
        il = np.round(lam0 / wl).astype(np.int64)
        key = ia * 100003 + il
        uk, inv = np.unique(key, return_inverse=True)
        cnt = np.bincount(inv)
        good = np.isin(inv, np.where(cnt >= 10)[0])
        mx = np.bincount(inv, weights=Fx_f) / cnt
        my = np.bincount(inv, weights=Fy_f) / cnt
        rx = Fx_f[good] - mx[inv][good]; ry = Fy_f[good] - my[inv][good]
        coh[f'cell_{wa:g}AU_{np.rad2deg(wl):.0f}deg'] = dict(
            n_cells=int((cnt >= 10).sum()),
            frac_bodies_in_good_cells=float(good.mean()),
            resid_rms_over_field_rms=float(np.sqrt(np.var(rx) + np.var(ry)) / tot))
    out['coherence_cells'] = coh
    out['field_rms_dv'] = float(tot)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scene', default='belt', choices=['belt', 'null'])
    ap.add_argument('--N', type=int, default=30000)
    ap.add_argument('--years', type=float, default=1000.0)
    ap.add_argument('--dt', type=float, default=0.1)
    ap.add_argument('--seed', type=int, default=7)
    ap.add_argument('--out', default='out.json')
    ap.add_argument('--keep-sub', type=int, default=2000)
    args = ap.parse_args()
    m_p = 1e-3 if args.scene == 'belt' else 0.0
    res = run(args.N, args.years, args.dt, m_p, a_p=5.2, e_p=0.048, seed=args.seed, keep_sub=args.keep_sub)
    if args.scene == 'belt':
        ana = analyze(res)
    else:
        ana = dict(null_max_da_rel=float(np.abs(res['a_final'] - res['a0_all']).max()),
                   null_max_de=float(np.abs(res['e_final'] - res['e0_all']).max()),
                   null_max_dw_rad=float(np.abs(((res['w_final'] - res['w0_all'] + np.pi) % (2 * np.pi)) - np.pi).max()))
    with open(args.out, 'w') as f:
        json.dump(ana, f, indent=1)
    brief = {k: v for k, v in ana.items() if not isinstance(v, (list, dict))}
    print(json.dumps(brief, indent=1))

if __name__ == '__main__':
    main()
