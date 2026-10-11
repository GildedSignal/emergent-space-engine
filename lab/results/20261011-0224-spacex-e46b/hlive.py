#!/usr/bin/env python3
"""H_live of a belt: the rate at which per-body state departs from a population program.

Truth (the plane's kick path): heliocentric leapfrog, Jupiter direct + indirect
(law.md: "the indirect term of a heliocentric split").  Program (the design's
cheap path away from resonance): Laplace-Lagrange free precession of (k,h) =
(e cos varpi, e sin varpi), from birth mean elements.  Mean elements are
measured in per-body windows of exactly 8 synodic periods, so the synodic
short-period term integrates out (fixed-grid windows leave ~7e-4 leakage,
measured, which is above the quantum: a bad instrument).

Two programs: (a) 'noref': textbook rate A(a) = (3/4) n mu alpha b_{3/2}^{(1)};
(b) 'refit': per-body rate fit on the first half of the arc (what reabsorption
does), residual measured out-of-sample on the second half.
"""
import argparse, json, math
import numpy as np

GM = 4.0 * math.pi ** 2
AP = 5.2
PP = math.sqrt(AP ** 3 / GM)
KSYN = 8.0

def b_laplace(alpha):
    psi = np.linspace(0.0, 2.0 * math.pi, 8192, endpoint=False)
    out = []
    for al in np.atleast_1d(alpha):
        d = 1.0 - 2.0 * al * np.cos(psi) + al * al
        out.append(np.trapz(np.cos(psi) / d ** 1.5, psi) / math.pi)
    return np.array(out)

def osculating(x, y, vx, vy):
    rn = np.hypot(x, y)
    v2 = vx * vx + vy * vy
    a = 1.0 / (2.0 / rn - v2 / GM)
    rv = x * vx + y * vy
    k = ((v2 - GM / rn) * x - rv * vx) / GM
    h = ((v2 - GM / rn) * y - rv * vy) / GM
    return a, k, h

def initial_conditions(N, rng, amin=2.3, amax=3.4, esig=0.05, emax=0.2):
    a = rng.uniform(amin, amax, N)
    e = np.minimum(rng.rayleigh(esig, N), emax)
    pomega = rng.uniform(0.0, 2.0 * math.pi, N)
    M = rng.uniform(0.0, 2.0 * math.pi, N)
    E = M.copy()
    for _ in range(60):
        E -= (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    cE, sE = np.cos(E), np.sin(E)
    r = a * (1.0 - e * cE)
    xd, yd = -a * sE, a * np.sqrt(1.0 - e * e) * cE
    n = math.sqrt(GM) * a ** -1.5
    scale = a * n / r
    cp, sp = np.cos(pomega), np.sin(pomega)
    x = r * (cE * cp - sE * sp)
    y = r * (cE * sp + sE * cp)
    vx = scale * (xd * cp - yd * sp)
    vy = scale * (xd * sp + yd * cp)
    return a, x, y, vx, vy

def run(mu, N, pj_orbits, steps_per_inner, sample_every, seed=20261011,
        resonances=((2, 1), (3, 1), (5, 2), (7, 3))):
    rng = np.random.default_rng(seed)
    a_ic, x, y, vx, vy = initial_conditions(N, rng)
    nP = math.sqrt(GM / AP ** 3)

    def accel(x, y, lam):
        rn3 = (x * x + y * y) ** -1.5
        jx, jy = AP * np.cos(lam), AP * np.sin(lam)
        dx, dy = jx - x, jy - y
        dn3 = (dx * dx + dy * dy) ** -1.5
        return (-GM * x * rn3 + mu * GM * (dx * dn3 - jx * AP ** -3.0),
                -GM * y * rn3 + mu * GM * (dy * dn3 - jy * AP ** -3.0))

    n_in = math.sqrt(GM / 2.3 ** 3)
    hstep = (2.0 * math.pi / n_in) / steps_per_inner
    n_steps = int(pj_orbits * PP / hstep)
    dt_sample = sample_every * hstep
    nsyn = math.sqrt(GM) * a_ic ** -1.5 - nP          # synodic rate, conserved
    if (nsyn <= 0).any():
        raise SystemExit("belt beyond Jupiter")
    dphi = nsyn * dt_sample

    # per-body window accumulators
    ak = np.zeros(N); ah = np.zeros(N); aa = np.zeros(N); cnt = np.zeros(N)
    phi = np.zeros(N)
    Ts, Ks, Hs, As = [], [], [], []                   # per-body padded later
    t = 0.0
    for step in range(n_steps):
        ax, ay = accel(x, y, nP * t)
        vx += 0.5 * hstep * ax; vy += 0.5 * hstep * ay
        x += hstep * vx; y += hstep * vy; t += hstep
        ax, ay = accel(x, y, nP * t)
        vx += 0.5 * hstep * ax; vy += 0.5 * hstep * ay
        if step % sample_every == 0:
            a, k, hh = osculating(x, y, vx, vy)
            ak += k; ah += hh; aa += a; cnt += 1
            phi += dphi
            closed = phi >= 2.0 * math.pi * KSYN
            if closed.any():
                idx = np.where(closed)[0]
                for i in idx:
                    Ts.append((i, t, ak[i] / cnt[i], ah[i] / cnt[i], aa[i] / cnt[i]))
                ak[closed] = 0; ah[closed] = 0; aa[closed] = 0; cnt[closed] = 0
                phi[closed] -= 2.0 * math.pi * KSYN

    # ragged -> padded matrices [N, W]
    Wmax = 0
    counts = np.zeros(N, dtype=int)
    for (i, *_rest) in Ts:
        counts[i] += 1
    Wmax = counts.max()
    tw = np.full((N, Wmax), np.nan)
    kw = np.full((N, Wmax), np.nan)
    hw = np.full((N, Wmax), np.nan)
    aw = np.full((N, Wmax), np.nan)
    pos = np.zeros(N, dtype=int)
    for (i, t_, k_, h_, a_) in Ts:
        p = pos[i]; tw[i, p] = t_; kw[i, p] = k_; hw[i, p] = h_; aw[i, p] = a_
        pos[i] += 1

    # Jacobi-constant control (the rotating-frame invariant of this scene)
    def jacobi(x, y, vx, vy, lam):
        jx, jy = AP * np.cos(lam), AP * np.sin(lam)
        rn = np.hypot(x, y); dn = np.hypot(jx - x, jy - y)
        U = -GM / rn - mu * GM / dn + mu * GM * (x * jx + y * jy) / AP ** 3
        return 0.5 * (vx ** 2 + vy ** 2) + U - nP * (x * vy - y * vx)
    a0ic, x0, y0, vx0, vy0 = initial_conditions(N, np.random.default_rng(seed))
    C0 = jacobi(x0, y0, vx0, vy0, 0.0)
    C1 = jacobi(x, y, vx, vy, nP * t)
    dE = float(np.abs((C1 - C0) / C0).mean())

    # ---- program ----
    a_bar = aw[:, 0]
    alpha = np.clip(a_bar / AP, 0.0, 0.95)
    A = 0.75 * math.sqrt(GM) * a_bar ** -1.5 * mu * alpha * b_laplace(alpha)
    k0, h0 = kw[:, 0], hw[:, 0]
    z0 = k0 + 1j * h0
    tc = tw - tw[:, :1]

    # rate refit on first half of each body's windows (LS through the origin on
    # the angle increment: the birth angle is arbitrary and must not bias omega)
    ang = np.unwrap(np.arctan2(hw, kw), axis=1)
    half = np.maximum(counts // 2, 2)
    w_fit = np.arange(Wmax)[None, :] < half[:, None]
    valid = np.isfinite(tw) & w_fit
    tv = np.where(valid, tc, 0.0)
    dang = np.where(valid, ang - ang[:, :1], 0.0)
    denom = (tv * tv).sum(1); num = (tv * dang).sum(1)
    omega = np.where(denom > 0, num / np.maximum(denom, 1e-12), A)

    W2 = 2.5 * mu ** (2.0 / 3.0)
    dists = np.full(N, 1e9)
    res_list = []
    for (p, q) in resonances:
        ares = AP * (q / p) ** (2.0 / 3.0)
        res_list.append(round(ares, 4))
        dists = np.minimum(dists, np.abs(a_bar / ares - 1.0) / W2)
    bins = np.array([0.0, 1.0, 2.0, 3.0, 5.0, 10.0, 1e9])
    ib = np.digitize(dists, bins) - 1

    def prog_res(om):
        zp = z0[:, None] * np.exp(1j * om[:, None] * tc)
        return hw - zp.imag, kw - zp.real, (aw - a_bar[:, None]) / a_bar[:, None]

    rh, rk, ra = prog_res(A)                    # variant (a): textbook rate
    rh2, rk2, ra2 = prog_res(omega)             # variant (b): refit rate
    out_half = np.arange(Wmax)[None, :] >= half[:, None]   # out-of-sample mask

    def last_idx(mask):
        out = np.full(N, -1, dtype=int)
        mm = mask & np.isfinite(tw)
        any_ = mm.any(1)
        out[any_] = np.asarray(np.where(mm, np.arange(Wmax)[None, :], -1)).max(1)[any_]
        return out
    jlast_all = last_idx(np.ones((N, Wmax), dtype=bool))
    jlast_out = last_idx(out_half)

    def stats(rh, rk, ra, jlast):
        rows = {}
        ok = jlast >= 0
        jj = jlast[ok]
        rhf = rh[ok, jj]; rkf = rk[ok, jj]; raf = ra[ok, jj]
        sig = np.hypot(rhf, rkf)
        ibf = ib[ok]
        for b in range(6):
            m = ibf == b
            n = int(m.sum())
            if n < 5:
                continue
            rows[f"b{b}"] = {"n": n,
                             "sig_e": float(np.sqrt((rhf[m] ** 2 + rkf[m] ** 2).mean())),
                             "sig_da": float(np.sqrt((raf[m] ** 2).mean())),
                             "frac_e_gt1e-4": float((sig[m] > 1e-4).mean()),
                             "frac_e_gt1e-6": float((sig[m] > 1e-6).mean()),
                             "frac_da_gt1e-5": float((np.abs(raf[m]) > 1e-5).mean())}
        return rows

    result = {"params": dict(mu=mu, N=N, pj_orbits=pj_orbits,
                             steps_per_inner=steps_per_inner, sample_every=sample_every,
                             seed=seed, n_steps=n_steps, h_yr=hstep, W_frac=W2,
                             res_aus=res_list, dE_rel=dE, counts_med=int(np.median(counts)),
                             t_final_yr=round(t, 1)),
              "noref_final": stats(rh, rk, ra, jlast_all),
              "refit_out_of_sample_final": stats(rh2, rk2, ra2, jlast_out)}

    # growth vs prediction lead (time since the body's last in-fit window):
    # this is the number a reabsorption cadence trades against
    fitend = np.where(w_fit & np.isfinite(tw), tw, -np.inf).max(1)
    lead = tw - fitend[:, None]
    traj = []
    for lo, hi in ((0.0, 60.0), (60.0, 120.0), (120.0, 250.0), (250.0, 400.0)):
        m = out_half & np.isfinite(tw) & (lead >= lo) & (lead < hi)
        if m.sum() < 40:
            continue
        row = {"lead_yr": [lo, hi], "n_win": int(m.sum())}
        for b in range(6):
            mm = m & (ib[:, None] == b)
            if mm.sum() < 5:
                continue
            sig = np.hypot(rh2[mm], rk2[mm])
            row[f"b{b}"] = {"med_e": float(np.median(sig)),
                            "sig_e": float(np.sqrt((rh2[mm] ** 2 + rk2[mm] ** 2).mean())),
                            "f_gt1e-4": float((sig > 1e-4).mean())}
        traj.append(row)

    # scar bits at the horizon (refit variant, out-of-sample final windows)
    lastj = np.array([np.where(np.isfinite(tw[i]) & out_half[i])[0][-1] if (np.isfinite(tw[i]) & out_half[i]).any() else -1
                      for i in range(N)])
    mH = lastj >= 0
    def bits(vals, q):
        v = vals / q
        rmax = float(np.abs(v).max()) + 1e-12
        hist, _ = np.histogram(v, bins=np.linspace(-rmax, rmax, 4097))
        p = hist[hist > 0] / hist.sum()
        return {"H_bits": round(float(-(p * np.log2(p)).sum()), 2),
                "naive_bits": round(float(math.log2(rmax) + 1.0), 2),
                "rms_quanta": round(float(np.sqrt((vals ** 2).mean()) / q), 1)}
    scars = {}
    for b in range(6):
        mm = mH & (ib == b)
        if mm.sum() < 5:
            continue
        idx = lastj[mm]
        rrh = rh2[mm, idx]; rrk = rk2[mm, idx]; rra = ra2[mm, idx]
        scars[f"b{b}"] = {"n": int(mm.sum()),
                          "q1e-6": {"e_hk": bits(np.concatenate([rrh, rrk]), 1e-6),
                                    "da": bits(rra, 1e-6)},
                          "q1e-8": {"e_hk": bits(np.concatenate([rrh, rrk]), 1e-8)}}
    result["scar_bits"] = scars
    result["traj"] = traj
    return result

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mu", type=float, default=9.54e-4)
    ap.add_argument("--N", type=int, default=2048)
    ap.add_argument("--pj-orbits", type=int, default=300)
    ap.add_argument("--steps-per-orbit", type=int, default=350)
    ap.add_argument("--sample-every", type=int, default=16)
    ap.add_argument("--seed", type=int, default=20261011)
    ap.add_argument("--out", type=str, required=True)
    args = ap.parse_args()
    import time
    t0 = time.time()
    res = run(args.mu, args.N, args.pj_orbits, args.steps_per_orbit,
              args.sample_every, args.seed)
    res["wall_s"] = round(time.time() - t0, 1)
    json.dump(res, open(args.out, "w"), indent=1)
    print(json.dumps({k: res[k] for k in ("params", "noref_final",
                                          "refit_out_of_sample_final", "wall_s")}, indent=1))
