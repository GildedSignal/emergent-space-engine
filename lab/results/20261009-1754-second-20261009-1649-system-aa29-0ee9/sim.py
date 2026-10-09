#!/usr/bin/env python3
"""One circle rotation, two gates: does the continued-fraction structure of a pair's
synodic rotation predict BOTH the conjunction lock pattern (encounters layer) AND
where orbit-averaged kicks fail (the kick layer's resonance gate)?

Float replica of the circular restricted three-body problem (the lab measures the
physics claim; integerisation is the crate's business). Sun GM=1 at origin; Jupiter
a fixed circular ring a_J=1, n_J=1; ship massless. Sweep alpha = n_ship/n_J across
first-order resonances (2:1, 3:2, 4:3) and higher-order ones (5:3, 7:4, 8:5).

Truth: velocity-Verlet, vectorised over seeds. Averaged layer: for a coplanar
circular external perturber the double-averaged field is axisymmetric, so e is
conserved (the layer is flat in e); its failure is the truth's secular e-pump.

Lock judge (second author, fixing run 1649's broken detrend metric): circular
statistics on the conjunction phases psi_n, with NO linear detrend. The detrended
RMS of run 1649 removed the circulation it should have exposed (62% of seeds
"locked"). Here: R_k = |mean exp(i k psi)| for k = 1, 2 (k=2 covers antipodal
bimodality: flips catch conjunction AND opposition, and odd-q resonances put
them on opposite sides), lockR = max(R_1, R_2); Rinc = R of the wrapped
successive increments (steady-drift diagnostic). LOCK iff lockR >= threshold,
threshold frozen in gate2.py from calibration only.

Trajectory loop unchanged from run 1649 (pump/a_drift/Rbar regenerate
bit-for-bit; verified against its calib.json).
"""
import argparse, json, math
import numpy as np

TWO_PI = 2.0 * math.pi


def kepler_state(a, e, varpi, M, GM=1.0):
    E = M.copy()
    for _ in range(8):
        E = E - (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    cE, sE = np.cos(E), np.sin(E)
    denom = 1.0 - e * cE
    xo = a * (cE - e)
    yo = a * np.sqrt(1.0 - e * e) * sE
    n = np.sqrt(GM / a**3)
    vx_o = -n * a * sE / denom
    vy_o = n * a * np.sqrt(1.0 - e * e) * cE / denom
    cv, sv = math.cos(varpi), math.sin(varpi)
    return (xo * cv - yo * sv, xo * sv + yo * cv,
            vx_o * cv - vy_o * sv, vx_o * sv + vy_o * cv)


def elements(x, y, vx, vy, GM=1.0):
    r = np.hypot(x, y)
    v2 = vx * vx + vy * vy
    a = -GM / (2.0 * (0.5 * v2 - GM / r))
    rv = x * vx + y * vy
    ex = ((v2 - GM / r) * x - rv * vx) / GM
    ey = ((v2 - GM / r) * y - rv * vy) / GM
    return a, np.hypot(ex, ey), np.arctan2(ey, ex)


def cf_convergents(x, qmax=8):
    res = []
    p_km2, q_km2, p_km1, q_km1 = 0, 1, 1, 0
    xrem = x
    for _ in range(14):
        ai = math.floor(xrem)
        p = ai * p_km1 + p_km2
        q = ai * q_km1 + q_km2
        res.append((p, q))
        p_km2, q_km2 = p_km1, q_km1
        p_km1, q_km1 = p, q
        if q > qmax:
            break
        frac = xrem - ai
        if frac < 1e-12:
            break
        xrem = 1.0 / frac
    return res


def delta_table(alpha, mu, e0):
    """Nearest CF convergent p/q (p>q, order<=4) with two width normalisations:
    N1 = mu^(2/3) (B17's W), N2 = sqrt(mu*e) (pendulum)."""
    best = None
    for (p, q) in cf_convergents(alpha, 12):
        if q < 1 or p <= q:
            continue  # 2/1 is a real resonance; only p<=q (the trivial floor) is skipped
        order = p - q
        if order > 4:
            continue
        d = abs(alpha - p / q)
        rec = dict(p=p, q=q, order=order, dist=d,
                   dN1=q * d / mu ** (2.0 / 3.0),
                   dN2=q * d / math.sqrt(mu * max(e0, 1e-6)))
        if best is None or rec["dN1"] < best["dN1"]:
            best = rec
    return best or dict(p=None, q=None, order=None, dist=None, dN1=None, dN2=None)


def run_sweep(mu, e0, alphas, M0_list, T_orbits=512, sub=384, sample=32, conj_every=8):
    dt = TWO_PI / sub
    nsteps = T_orbits * sub
    rows = []
    for M0v in M0_list:
        ns = len(alphas)
        a0 = alphas ** (-2.0 / 3.0)
        x, y, vx, vy = kepler_state(a0, np.full(ns, e0), 0.0, np.full(ns, M0v))

        def accel(x, y, t):
            cJ, sJ = math.cos(t), math.sin(t)
            r2 = x * x + y * y
            r = np.sqrt(r2)
            dx, dy = cJ - x, sJ - y
            d2 = dx * dx + dy * dy
            d = np.sqrt(d2)
            fd = mu / (d2 * d)
            return (-x / (r2 * r) + fd * dx - mu * cJ,
                    -y / (r2 * r) + fd * dy - mu * sJ)

        t = 0.0
        ax, ay = accel(x, y, t)
        nsamp = nsteps // sample + 1
        e_s = np.empty((nsamp, ns)); a_s = np.empty((nsamp, ns))
        nconj = nsteps // conj_every + 1
        sign_s = np.empty((nconj, ns), dtype=np.int8)
        psi_s = np.empty((nconj, ns), dtype=np.float32)
        isamp = iconj = 0
        for step in range(nsteps + 1):
            if step % sample == 0:
                aa, ee, _ = elements(x, y, vx, vy)
                e_s[isamp] = ee; a_s[isamp] = aa; isamp += 1
            if step % conj_every == 0:
                cJ, sJ = math.cos(t), math.sin(t)
                sign_s[iconj] = np.sign(x * sJ - y * cJ)
                _, _, w_now = elements(x, y, vx, vy)
                psi = np.arctan2(y, x) - w_now
                psi_s[iconj] = np.arctan2(np.sin(psi), np.cos(psi))
                iconj += 1
            if step == nsteps:
                break
            x = x + vx * dt + 0.5 * ax * dt * dt
            y = y + vy * dt + 0.5 * ay * dt * dt
            axn, ayn = accel(x, y, t + dt)
            vx = vx + 0.5 * (ax + axn) * dt
            vy = vy + 0.5 * (ay + ayn) * dt
            ax, ay = axn, ayn
            t += dt
        e_s, a_s = e_s[:isamp], a_s[:isamp]
        sign_s, psi_s = sign_s[:iconj], psi_s[:iconj]
        wlen = sub // sample  # one Jupiter orbit of samples
        csum = np.cumsum(np.vstack([np.zeros((1, ns)), e_s]), axis=0)
        sm = (csum[wlen:] - csum[:-wlen]) / wlen
        pump = np.max(np.abs(sm - e0), axis=0)
        a_drift = np.max(np.abs(a_s - a_s[0]), axis=0) / a_s[0]
        flip = np.zeros(sign_s.shape, dtype=bool)
        flip[1:] = sign_s[1:] * sign_s[:-1] < 0
        for i in range(ns):
            f = flip[:, i]
            nc = int(f.sum())
            if nc > 4:
                ang = psi_s[f, i].astype(np.float64)
                z = np.exp(1j * ang)
                Rbar = float(abs(z.mean()))
                R2 = float(abs(np.exp(2j * ang).mean()))
                d = np.diff(ang)
                d = np.arctan2(np.sin(d), np.cos(d))
                Rinc = float(abs(np.exp(1j * d).mean()))
                lockR = max(Rbar, R2)
            else:
                Rbar = R2 = Rinc = lockR = -1.0
            rows.append(dict(alpha=float(alphas[i]), M0=float(M0v),
                             pump=float(pump[i]), a_drift=float(a_drift[i]),
                             Rbar=Rbar, R2=R2, Rinc=Rinc, lockR=lockR, nconj=nc))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mu", type=float, required=True)
    ap.add_argument("--e0", type=float, required=True)
    ap.add_argument("--amin", type=float, default=1.27)
    ap.add_argument("--amax", type=float, default=2.09)
    ap.add_argument("--n", type=int, default=280)
    ap.add_argument("--T", type=int, default=512)
    ap.add_argument("--sub", type=int, default=384)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    alphas = np.linspace(args.amin, args.amax, args.n)
    rows = run_sweep(args.mu, args.e0, alphas, [0.0, math.pi / 2],
                     T_orbits=args.T, sub=args.sub)
    for r in rows:
        r.update(delta_table(r["alpha"], args.mu, args.e0))
    meta = dict(mu=args.mu, e0=args.e0, T=args.T, sub=args.sub, n=args.n,
                amin=args.amin, amax=args.amax)
    with open(args.out, "w") as f:
        json.dump(dict(meta=meta, rows=rows), f)
    print(f"wrote {args.out}: {len(rows)} rows")


if __name__ == "__main__":
    main()
