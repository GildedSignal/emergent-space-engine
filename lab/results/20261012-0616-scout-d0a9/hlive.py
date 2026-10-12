#!/usr/bin/env python3
"""H_live falsifier: rate and saturation of live distinguishing bits in a belt.

Shearing sheet (Hill), Omega=1, box 1x1, nearest-image forces, softened mutual
gravity. Split: exact linear drift (conserves the invariants (A, D)) + mutual
kicks -- the engine's drift+kick shape. Per orbit boundary: each body's (A, D).
A body's live distinction from its birth program is the offset series
state(t) - state(0); sigma-delta quantization of that offset at quantum Q
decides when a scar must be stored. Floats explore; nothing here is canonical.
"""
import json
import sys
import numpy as np

L = 1.0
OM = 1.0

def drift(x, y, vx, vy, dt):
    """Exact Hill drift over dt. Conserves C3 = vy + 2*OM*x (hence D), and A."""
    C3 = vy + 2.0 * OM * x
    D = 2.0 * C3 / OM
    xe = x - D
    A = np.sqrt(xe * xe + (vx / OM) ** 2)
    Asafe = np.where(A > 1e-300, A, 1.0)
    ph = np.arctan2(-vx / (OM * Asafe), xe / Asafe) + OM * dt
    x2 = D + A * np.cos(ph)
    vx2 = -A * OM * np.sin(ph)
    # y integrates y' = -1.5*OM*D - 2*OM*A*cos(ph(t))
    y2 = y + (-1.5 * OM * D) * dt + 2.0 * A * (np.sin(ph) - np.sin(ph - OM * dt))
    vy2 = -1.5 * OM * D - 2.0 * OM * A * np.cos(ph)
    y2 = y2 - L * np.floor(y2 / L + 0.5)   # wrap to [-L/2, L/2)
    return x2, y2, vx2, vy2

def accel(x, y, Gm, eps):
    dx = x[:, None] - x[None, :]
    dy = y[:, None] - y[None, :]
    dx -= L * np.round(dx / L)
    dy -= L * np.round(dy / L)
    r2 = dx * dx + dy * dy + eps * eps
    inv_r3 = r2 ** -1.5
    np.fill_diagonal(inv_r3, 0.0)
    ax = Gm * np.sum(dx * inv_r3, axis=1)
    ay = Gm * np.sum(dy * inv_r3, axis=1)
    return ax, ay

def min_dist(x, y, eps):
    dx = x[:, None] - x[None, :]
    dy = y[:, None] - y[None, :]
    dx -= L * np.round(dx / L)
    dy -= L * np.round(dy / L)
    r2 = dx * dx + dy * dy
    np.fill_diagonal(r2, np.inf)
    return np.sqrt(np.min(r2, axis=1))

def invariants(x, y, vx, vy):
    C3 = vy + 2.0 * OM * x
    D = 2.0 * C3 / OM
    return np.hypot(x - D, vx / OM), D

def init_cond(rng, N, vdisp):
    D = (rng.random(N) - 0.5) * 0.8 * L          # guiding centres across box
    A = rng.rayleigh(vdisp, N)                    # epicycle amplitudes
    ph = rng.uniform(0, 2 * np.pi, N)
    x = D + A * np.cos(ph)
    vx = -A * OM * np.sin(ph)
    vy = -1.5 * OM * D - 2.0 * OM * A * np.cos(ph)
    y = (rng.random(N) - 0.5) * L
    return x, y, vx, vy

def run(seed, N, orbits, Gm, eps, vdisp, gravity=True, steps_per_orbit=40):
    rng = np.random.default_rng(seed)
    x, y, vx, vy = init_cond(rng, N, vdisp)
    dt = 2 * np.pi / (OM * steps_per_orbit)
    AD = np.zeros((orbits + 1, N, 2))
    AD[0] = np.stack(invariants(x, y, vx, vy), axis=1)
    dmin_orb = np.zeros((orbits, N))
    for k in range(orbits):
        dmin = np.full(N, np.inf)
        for s in range(steps_per_orbit):
            if gravity:
                ax, ay = accel(x, y, Gm, eps)
                dmin = np.minimum(dmin, min_dist(x, y, eps))
                vx += 0.5 * dt * ax
                vy += 0.5 * dt * ay
            x, y, vx, vy = drift(x, y, vx, vy, dt)
            if gravity:
                ax, ay = accel(x, y, Gm, eps)
                vx += 0.5 * dt * ax
                vy += 0.5 * dt * ay
        AD[k + 1] = np.stack(invariants(x, y, vx, vy), axis=1)
        dmin_orb[k] = dmin if gravity else np.nan
    return AD, dmin_orb

def sigmadelta(off, Q):
    """off: (orbits+1, N) offset from birth program. Carry bounded to (-Q/2, Q/2].
    One scar event per orbit in which the offset's cell changes; d = quanta jumped.
    Returns per-body scar count, all deltas, first-scar orbit (-1 if none)."""
    n, T = off.shape[1], off.shape[0] - 1
    m = np.zeros(n, dtype=np.int64)      # offset in quanta (0 at birth)
    c = np.zeros(n)
    n_scar = np.zeros(n, dtype=np.int64)
    first = np.full(n, -1, dtype=np.int64)
    deltas = []
    frac_scarred = np.zeros(T)
    for k in range(T):
        v = m * Q + c + (off[k + 1] - off[k])    # kick lands on the carry
        m2 = np.floor(v / Q + 0.5).astype(np.int64)
        d = m2 - m
        changed = d != 0
        n_scar += changed
        newly = changed & (first < 0)
        first[newly] = k + 1
        frac_scarred[k] = changed.mean()
        dd = d[changed]
        deltas.extend(dd.tolist())
        m = m2
        c = v - m2 * Q
    return dict(n_scar=n_scar, deltas=deltas, first=first, frac_scarred=frac_scarred)

def delta_entropy(deltas):
    if not deltas:
        return 0.0, 0.0
    v, cnt = np.unique(deltas, return_counts=True)
    p = cnt / cnt.sum()
    return float(-(p * np.log2(p)).sum()), float(np.mean(np.abs(v) == 1))

def gauss_ent(sigma, Q):
    return 0.5 * np.log2(2 * np.pi * np.e * sigma ** 2 / Q ** 2)

def hist_entropy(samples, Q):
    lo, hi = samples.min() - Q, samples.max() + Q
    nb = int(np.clip(np.ceil((hi - lo) / Q), 1, 4096))
    h, _ = np.histogram(samples, bins=nb, range=(lo, hi))
    p = h / h.sum()
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum())

def main():
    N, ORBITS, Gm, eps, vdisp = 256, 40, 6e-7, 0.02, 0.04
    out = {"params": dict(N=N, orbits=ORBITS, Gm=Gm, eps=eps, vdisp=vdisp,
                          steps_per_orbit=40, model="hill sheet, softened")}
    results = {}
    for seed in (1, 2):
        AD, dmin = run(seed, N, ORBITS, Gm, eps, vdisp)
        dAD = np.diff(AD, axis=0)
        sig = {}
        for dim, name in ((0, "A"), (1, "D")):
            s = dAD[:, :, dim].ravel()
            ac1 = float(np.corrcoef(s[:-N], s[N:])[0, 1]) if len(s) > 2 * N else 0.0
            sig[name] = dict(rms=float(np.sqrt(np.mean(s ** 2))), mean=float(np.mean(s)),
                             lag1_autocorr=ac1,
                             p999=float(np.quantile(np.abs(s), 0.999)),
                             max=float(np.max(np.abs(s))))
        rms = {k: sig[k]["rms"] for k in ("A", "D")}
        sweep = []
        for qfac in (32, 16, 8, 5, 3, 2, 1, 0.5, 0.3, 0.15):
            row, tot_rate, tot_bits = {}, 0.0, 0.0
            for dim, name in ((0, "A"), (1, "D")):
                Q = rms[name] * qfac
                off = AD[:, :, dim] - AD[0, :, dim][None, :]
                sd = sigmadelta(off, Q)
                rate = float(sd["n_scar"].sum()) / (N * ORBITS)
                ent, frac_pm1 = delta_entropy(sd["deltas"])
                row[name] = dict(Q=Q, qfac=qfac, rate_per_body_orbit=rate,
                                 scar_bits=ent, frac_scarred_end=float((sd["n_scar"] > 0).mean()),
                                 delta_pm1_frac=frac_pm1)
                tot_rate += rate
                tot_bits += ent
            sweep.append(dict(qfac=qfac, A=row["A"], D=row["D"],
                              total_rate=tot_rate, bits_per_scar=tot_bits))
        # growth curve of scarred fraction at qfac 4 (first-scar process)
        curves = {}
        for dim, name in ((0, "A"), (1, "D")):
            Q = rms[name] * 4
            off = AD[:, :, dim] - AD[0, :, dim][None, :]
            sd = sigmadelta(off, Q)
            curves[name] = dict(Q=Q, frac_scarred_per_orbit=sd["frac_scarred"].tolist())
        # offset entropy at the end (saturation level) vs Gaussian formula
        Hsat = {}
        for qfac in (16, 4, 1):
            h = {}
            for dim, name in ((0, "A"), (1, "D")):
                Q = rms[name] * qfac
                off = AD[-1, :, dim] - AD[0, :, dim]
                h[name] = dict(Q=Q, measured=hist_entropy(off, Q),
                               gauss=gauss_ent(np.std(off), Q))
            Hsat[f"qfac{qfac}"] = h
        results[f"seed{seed}"] = dict(
            kick_stats=sig, sweep=sweep, growth=curves, H_sat=Hsat,
            enc_rate_b01=float(np.mean(dmin < 0.1)),
            enc_rate_b005=float(np.mean(dmin < 0.05)),
            disp=dict(A0=float(np.std(AD[0, :, 0])), Aend=float(np.std(AD[-1, :, 0])),
                      D0=float(np.std(AD[0, :, 1])), Dend=float(np.std(AD[-1, :, 1]))))
    # control: gravity off -> invariants drift only by float roundoff
    AD0, _ = run(1, N, 10, 0.0, eps, vdisp, gravity=False)
    dmax = float(np.max(np.abs(np.diff(AD0, axis=0))))
    n0 = sigmadelta(AD0[:, :, 0] - AD0[0, :, 0][None, :], 1e-14)["n_scar"].sum()
    results["control_no_gravity"] = dict(max_dAD_per_orbit=dmax,
                                         scars_at_Q1e_14=int(n0))
    out["results"] = results
    fn = sys.argv[1] if len(sys.argv) > 1 else "results.json"
    with open(fn, "w") as f:
        json.dump(out, f, indent=1)
    print("written", fn)

if __name__ == "__main__":
    main()
