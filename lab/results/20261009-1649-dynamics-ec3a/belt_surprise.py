#!/usr/bin/env python3
"""Belt surprise-rate instrument (dynamics lens, run 20261009-1649-dynamics-ec3a).

Oracle: planar restricted 3-body in the DESIGN'S OWN SPLIT (law.md: "a
symmetric, symplectic split (Wisdom-Holman); the drift is exact along the
dominant body's compiled geodesic, the kicks carry everything else"):
 - drift: exact Kepler propagation about the primary (GM=1) via universal
   variables (Stumpff), so the epicycle carries zero numerical error;
 - kicks: the secondary's tide + the indirect term (+ optional J2), as
   impulses shared-step kick-drift-kick; the secondary rides an exact Kepler
   orbit.
Belt bodies are massless.

Measured: per body, the rate at which SECULAR elements cross quanta.
Secular = double averaging matching the design's orbit-averaged kicks:
boxcar over the body's own orbital period, then over the synodic period.
E-native quantum for a: q_a = QA * a0^2 (E = -1/2a => fixed q_E <=> q_a ~ a^2);
absolute quantum for e. A crossing of either key is one re-key of the law's
(E,L) memo: one distinction, one kick/recompile event. Uniform-tick policies
must pay the p99 rate for everyone; surprise-following pays the mean.

Multiple quanta (multipliers of QA/QE) are tracked in one run for scaling.

Outputs: <out>.json (summary + distributions), <out>.npz (per-body stats,
binned crossings, traces).
"""
import argparse, json, math, time
import numpy as np


def kepler_pos_secondary(M, e, a):
    E = M
    for _ in range(6):
        f = E - e * math.sin(E) - M
        fp = 1.0 - e * math.cos(E)
        E -= f / fp
    return a * (math.cos(E) - e), a * math.sqrt(1.0 - e * e) * math.sin(E)


def stumpff(z):
    az = np.abs(z)
    small = az < 1e-6
    safe = np.where(small, 1.0, z)
    sp = np.sqrt(np.abs(safe))
    pos = safe > 0
    zp = np.maximum(np.where(pos, safe, 1.0), 1e-12)
    zn = np.clip(np.where(~pos, -safe, 1.0), None, 1e4)
    Cp = (1.0 - np.cos(np.sqrt(zp))) / zp
    Cn = (np.cosh(np.sqrt(zn)) - 1.0) / zn
    Sp = (np.sqrt(zp) - np.sin(np.sqrt(zp))) / zp ** 1.5
    Sn = (np.sinh(np.sqrt(zn)) - np.sqrt(zn)) / zn ** 1.5
    C = np.where(pos, Cp, Cn)
    S = np.where(pos, Sp, Sn)
    Cs = 0.5 - safe / 24.0 + safe ** 2 / 720.0
    Ss = 1.0 / 6.0 - safe / 120.0 + safe ** 2 / 5040.0
    return np.where(small, Cs, C), np.where(small, Ss, S)


def kepler_drift(x, y, vx, vy, dt):
    """Exact Kepler advance (mu=1) by dt, universal variables."""
    r0 = np.sqrt(x * x + y * y)
    v2 = vx * vx + vy * vy
    alpha = 2.0 / r0 - v2            # 1/a
    vr0 = (x * vx + y * vy) / r0
    a = 1.0 / alpha
    chimax = 12.0 * dt * np.sqrt(np.maximum(alpha, 1e-12))
    chi = np.clip(dt / np.maximum(a, 1e-9), 0.0, chimax)
    for _ in range(7):
        z = alpha * chi * chi
        C, S = stumpff(z)
        F = (r0 * vr0) * chi * chi * C + (1.0 - alpha * r0) * chi ** 3 * S + r0 * chi - dt
        dF = (r0 * vr0) * chi * (1.0 - z * S) + (1.0 - alpha * r0) * chi * chi * C + r0
        chi = np.clip(chi - F / dF, 0.0, chimax)
    z = alpha * chi * chi
    C, S = stumpff(z)
    f = 1.0 - chi * chi * C / r0
    g = dt - chi ** 3 * S
    rx = f * x + g * vx
    ry = f * y + g * vy
    r = np.sqrt(rx * rx + ry * ry)
    fdot = chi * (z * S - 1.0) / (r * r0)
    gdot = 1.0 - chi * chi * C / r
    vxn = fdot * x + gdot * vx
    vyn = fdot * y + gdot * vy
    return rx, ry, vxn, vyn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--mprime", type=float, default=0.03)
    ap.add_argument("--eprime", type=float, default=0.05)
    ap.add_argument("--aprime", type=float, default=1.0)
    ap.add_argument("--j2", type=float, default=0.0)
    ap.add_argument("--rbody", type=float, default=0.1)
    ap.add_argument("--amin", type=float, default=0.28)
    ap.add_argument("--amax", type=float, default=0.40)
    ap.add_argument("--emax", type=float, default=0.15)
    ap.add_argument("--nbody", type=int, default=2048)
    ap.add_argument("--tmax", type=float, default=3000.0)
    ap.add_argument("--qa", type=float, default=1e-6)
    ap.add_argument("--qe", type=float, default=1e-4)
    ap.add_argument("--qmults", type=str, default="1,3.16,10")
    ap.add_argument("--dtper", type=float, default=45.0)
    ap.add_argument("--dsamp", type=float, default=0.04)
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()

    t0wall = time.time()
    rng = np.random.default_rng(args.seed)
    N = args.nbody
    mp, ep, ap_, J2, Rb = args.mprime, args.eprime, args.aprime, args.j2, args.rbody
    npert_orbit = math.sqrt((1.0 + mp) / ap_ ** 3)
    mults = [float(m) for m in args.qmults.split(",")]
    nm = len(mults)

    # --- initial belt (heliocentric, GM = 1) ---
    a0 = rng.uniform(args.amin, args.amax, N)
    e0 = rng.uniform(0.0, args.emax, N)
    varpi0 = rng.uniform(0, 2 * np.pi, N)
    M0 = rng.uniform(0, 2 * np.pi, N)
    Ean = M0.copy()
    for _ in range(6):
        Ean -= (Ean - e0 * np.sin(Ean) - M0) / (1.0 - e0 * np.cos(Ean))
    cE, sE = np.cos(Ean), np.sin(Ean)
    b = a0 * np.sqrt(1.0 - e0 * e0)
    n0 = a0 ** -1.5
    xf = a0 * (cE - e0)
    yf = b * sE
    vxf = (-a0 * sE / (1.0 - e0 * cE)) * n0
    vyf = (b * cE / (1.0 - e0 * cE)) * n0
    cv, sv = np.cos(varpi0), np.sin(varpi0)
    x = xf * cv - yf * sv
    y = xf * sv + yf * cv
    vx = vxf * cv - vyf * sv
    vy = vxf * sv + vyf * cv

    # --- stepping ---
    Pmin = 2 * math.pi * args.amin ** 1.5
    dt = Pmin / args.dtper
    nsteps = int(args.tmax / dt)
    nsamp_step = max(1, int(round(args.dsamp / dt)))

    # --- double averaging (own period -> synodic) + crossing counters ---
    n_i = a0 ** -1.5
    P_i = 2 * np.pi / n_i
    syn_i = 2 * np.pi / np.abs(n_i - npert_orbit)
    # scalar windows (outermost body's periods): exact-width rings, no bias,
    # inner bodies just get extra (harmless) smoothing of their epicycle
    W1 = max(3, int(np.rint(P_i.max() / args.dsamp)))
    W2 = max(3, int(np.rint(syn_i.max() / args.dsamp)))
    buf1_a = np.zeros((N, W1)); buf1_e = np.zeros((N, W1))
    buf2_a = np.zeros((N, W2)); buf2_e = np.zeros((N, W2))
    settle = W1 + 2 * W2 + 4  # samples before the cascade has fully settled
    b1 = np.zeros(N, int); b2 = np.zeros(N, int)
    s1_a = np.zeros(N); s1_e = np.zeros(N)
    s2_a = np.zeros(N); s2_e = np.zeros(N)
    f1 = np.zeros(N, int); f2 = np.zeros(N, int)
    ka = np.zeros((nm, N)); ke = np.zeros((nm, N))
    netA0 = np.zeros((nm, N)); netE0 = np.zeros((nm, N))
    kinit = np.zeros((nm, N), bool)
    qa_i = args.qa * a0 * a0
    qe_i = np.full(N, args.qe)
    cross_a = np.zeros((nm, N), np.int64)
    cross_e = np.zeros((nm, N), np.int64)
    kmin_a = np.full((nm, N), float(1 << 50)); kmax_a = np.zeros((nm, N))
    kmin_e = np.full((nm, N), float(1 << 50)); kmax_e = np.zeros((nm, N))
    alive = np.ones(N, bool)
    ejected = np.zeros(N, bool)
    nbin = 10
    bins_a = np.zeros((N, nbin), np.int32)
    bins_e = np.zeros((N, nbin), np.int32)
    ntr = min(256, N)
    tr_step = max(1, int(round(1.0 / args.dsamp)))
    tr_a = []; tr_e = []
    nsamples = 0
    ar = np.arange(N)
    qmult = np.array(mults)[:, None]

    def sample(t):
        nonlocal nsamples, alive, ejected, b1, b2, f1, f2
        nonlocal s1_a, s1_e, s2_a, s2_e
        nonlocal ka, ke, netA0, netE0, kinit, cross_a, cross_e
        nonlocal kmin_a, kmax_a, kmin_e, kmax_e, bins_a, bins_e
        r2 = x * x + y * y
        v2 = vx * vx + vy * vy
        r = np.sqrt(r2)
        eps = 0.5 * v2 - 1.0 / r
        hh = x * vy - y * vx
        with np.errstate(invalid="ignore", divide="ignore"):
            aa = -1.0 / (2.0 * eps)
            ee = np.sqrt(np.maximum(0.0, 1.0 + 2.0 * eps * hh * hh))
        ok = np.isfinite(aa) & (aa > 0) & (aa < 2.0 * ap_) & (ee < 0.95)
        alive &= ok
        ejected |= ~ok
        valid = alive & (aa > 0)
        av = np.where(valid, aa, 0.0)
        ev = np.where(valid, ee, 0.0)
        o1a = buf1_a[ar, b1]; o1e = buf1_e[ar, b1]
        buf1_a[ar, b1] = av; buf1_e[ar, b1] = ev
        g1 = f1 < W1
        s1_a += av - np.where(g1, 0.0, o1a)
        s1_e += ev - np.where(g1, 0.0, o1e)
        f1 = np.minimum(f1 + 1, W1)
        b1 = (b1 + 1) % W1
        rdy1 = valid & (f1 >= W1)
        v1a = np.where(rdy1, s1_a / W1, 0.0)
        v1e = np.where(rdy1, s1_e / W1, 0.0)
        o2a = buf2_a[ar, b2]; o2e = buf2_e[ar, b2]
        buf2_a[ar, b2] = v1a; buf2_e[ar, b2] = v1e
        g2 = f2 < W2
        s2_a += v1a - np.where(g2, 0.0, o2a)
        s2_e += v1e - np.where(g2, 0.0, o2e)
        f2 = np.minimum(f2 + 1, W2)
        b2 = (b2 + 1) % W2
        rdy2 = rdy1 & (f2 >= W2) & (nsamples + 1 >= settle)
        sec_a = np.where(rdy2, s2_a / W2, np.nan)
        sec_e = np.where(rdy2, s2_e / W2, np.nan)
        nsamples += 1
        kza = np.floor(sec_a[None, :] / (qa_i[None, :] * qmult))
        kze = np.floor(sec_e[None, :] / (qe_i[None, :] * qmult))
        kup = rdy2[None, :] & np.isfinite(kza)
        eup = rdy2[None, :] & np.isfinite(kze)
        initm = kup & ~kinit
        ka = np.where(initm, kza, ka)
        ke = np.where(initm, kze, ke)
        netA0 = np.where(initm, kza, netA0)
        netE0 = np.where(initm, kze, netE0)
        kinit |= initm
        act = kup & kinit
        da = np.where(act, np.abs(kza - ka), 0.0)
        de = np.where(eup & kinit, np.abs(kze - ke), 0.0)
        dai = np.nan_to_num(da).astype(np.int64)
        dei = np.nan_to_num(de).astype(np.int64)
        cross_a += dai
        cross_e += dei
        b = min(nbin - 1, int(t / args.tmax * nbin))
        bins_a[:, b] += dai[0].astype(np.int32)
        bins_e[:, b] += dei[0].astype(np.int32)
        kmin_a = np.where(kup, np.minimum(kmin_a, np.nan_to_num(kza, posinf=1 << 50)), kmin_a)
        kmax_a = np.where(kup, np.maximum(kmax_a, np.nan_to_num(kza, posinf=0.0)), kmax_a)
        kmin_e = np.where(eup, np.minimum(kmin_e, np.nan_to_num(kze, posinf=1 << 50)), kmin_e)
        kmax_e = np.where(eup, np.maximum(kmax_e, np.nan_to_num(kze, posinf=0.0)), kmax_e)
        ka = np.where(act, kza, ka)
        ke = np.where(eup & kinit, kze, ke)
        if nsamples % tr_step == 0:
            tr_a.append(ka[0][:ntr].astype(np.int32).copy())
            tr_e.append(ke[0][:ntr].astype(np.int32).copy())

    def tide_accel(t):
        Mp = kepler_pos_secondary(npert_orbit * t, ep, ap_)
        dx = Mp[0] - x
        dy = Mp[1] - y
        d2 = dx * dx + dy * dy + 1e-12
        d32 = d2 * np.sqrt(d2)
        r2 = x * x + y * y + 1e-12
        r32 = r2 * np.sqrt(r2)
        ax = mp * (dx / d32 - Mp[0] / ap_ ** 3)
        ay = mp * (dy / d32 - Mp[1] / ap_ ** 3)
        if J2 > 0:
            # planar J2 perturbation relative to the point-mass drift
            c = -1.5 * J2 * Rb * Rb / (r2 * r32)
            ax = ax + c * x
            ay = ay + c * y
        return ax, ay

    for s in range(nsteps):
        t = s * dt
        if mp > 0 or J2 > 0:
            ax, ay = tide_accel(t)
            vx = vx + 0.5 * dt * ax
            vy = vy + 0.5 * dt * ay
        x, y, vx, vy = kepler_drift(x, y, vx, vy, dt)
        if mp > 0 or J2 > 0:
            ax, ay = tide_accel(t + dt)
            vx = vx + 0.5 * dt * ax
            vy = vy + 0.5 * dt * ay
        if (s + 1) % nsamp_step == 0:
            sample((s + 1) * dt)

    # --- rates: crossings per belt orbit (own mean motion) ---
    T = args.tmax
    P0 = 2 * np.pi * a0 ** 1.5
    orb = T / P0

    def stats(r):
        rl = r[alive]
        return dict(mean=float(rl.mean()), median=float(np.median(rl)),
                    p90=float(np.percentile(rl, 90)), p99=float(np.percentile(rl, 99)),
                    p999=float(np.percentile(rl, 99.9)), max=float(rl.max()),
                    frac_zero=float((rl == 0).mean()))

    out_mults = []
    for j, m in enumerate(mults):
        r_a = cross_a[j] / orb
        r_e = cross_e[j] / orb
        sa, se = stats(r_a), stats(r_e)
        rl_key = (r_a + r_e)[alive]
        range_a = np.maximum(kmax_a[j] - kmin_a[j], 0.0)
        net_a = np.abs(ka[j] - netA0[j])
        frozen = (range_a <= 2) & alive
        walker = (net_a > 0.25 * np.maximum(range_a, 1.0)) & alive & ~frozen
        librarian = alive & ~frozen & ~walker
        out_mults.append(dict(
            mult=m, r_a=sa, r_e=se,
            r_key=dict(mean=float(rl_key.mean()), median=float(np.median(rl_key)),
                       p99=float(np.percentile(rl_key, 99)), max=float(rl_key.max())),
            S_a_p99_over_mean=sa["p99"] / max(sa["mean"], 1e-30),
            S_e_p99_over_mean=se["p99"] / max(se["mean"], 1e-30),
            S_key_p99_over_mean=float(np.percentile(rl_key, 99) / max(rl_key.mean(), 1e-30)),
            waste_uniform_key=float(1 - rl_key.mean() / max(np.percentile(rl_key, 99), 1e-30)),
            frac=dict(frozen=float(frozen.mean()), librarian=float(librarian.mean()),
                      walker=float(walker.mean())),
            hot_frac_10x_median=float(((r_a + r_e) > 10 * max(float(np.median(rl_key)), 1e-30)).mean()),
        ))
    tot_bin = bins_a.sum(axis=0) + bins_e.sum(axis=0)
    burst = float(tot_bin.max() / max(tot_bin.mean(), 1e-30))

    out = dict(
        config={k: getattr(args, k) for k in
                ["mprime", "eprime", "aprime", "j2", "rbody", "amin", "amax",
                 "emax", "nbody", "tmax", "qa", "qe", "qmults", "dtper", "dsamp", "seed"]},
        dt=dt, nsteps=nsteps, nsamples=nsamples,
        wall_s=time.time() - t0wall,
        live_frac=float(alive.mean()), ejected_frac=float(ejected.mean()),
        burst_bin_over_mean=burst, mults=out_mults,
    )
    with open(args.out + ".json", "w") as f:
        json.dump(out, f, indent=1)
    r_a = cross_a[0] / orb
    r_e = cross_e[0] / orb
    np.savez_compressed(
        args.out + ".npz", a0=a0, e0=e0, r_a=r_a, r_e=r_e, cross_a=cross_a,
        cross_e=cross_e, range_a=np.maximum(kmax_a[0] - kmin_a[0], 0.0),
        net_a=np.abs(ka[0] - netA0[0]), alive=alive, bins_a=bins_a, bins_e=bins_e,
        tr_a=np.array(tr_a) if tr_a else np.zeros((0, ntr), np.int32),
        tr_e=np.array(tr_e) if tr_e else np.zeros((0, ntr), np.int32))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
