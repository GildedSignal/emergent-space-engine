#!/usr/bin/env python3
"""Kick-cadence bifurcation in the law's own form.

Model: test particle about M=1 (G=1), outer perturber mu_p on a fixed circular
orbit R (analytic, exact). Engine form (law.md "Perturbed motion"): exact
Kepler drift about M + tidal kicks at fixed cadence n per inner radial period,
DKD leapfrog. Truth: DOP853 on the same equations. Circular restricted 3BP, so
the Jacobi constant is an exact invariant of truth.

Classifies the error dynamics per (eps, n, seed):
  - z-error exponent gamma vs truth (bounded ~0 / walk ~0.5 / drift ~1)
  - Jacobi-constant error exponent
  - twin divergence (map's own chaos, lambda_num)
"""
import json
import sys
import time
import numpy as np
from scipy.integrate import solve_ivp

# ---------------- universal-variable Kepler drift ----------------

def _stumpff(z):
    import warnings
    with np.errstate(invalid='ignore', divide='ignore', over='ignore'):
        return _stumpff_inner(z)


def _stumpff_inner(z):
    zp = np.maximum(z, 1e-300)
    zm = np.maximum(-z, 1e-300)
    rt = np.sqrt(zp)
    C = np.where(z > 1e-8, (1 - np.cos(rt)) / zp, 0.5 - z / 24 + z * z / 720)
    C = np.where(z < -1e-8, (np.cosh(np.sqrt(zm)) - 1) / zm, C)
    S = np.where(z > 1e-8, (rt - np.sin(rt)) / zp ** 1.5, 1 / 6 - z / 120 + z * z / 5040)
    S = np.where(z < -1e-8, (np.sinh(np.sqrt(zm)) - np.sqrt(zm)) / zm ** 1.5, S)
    return C, S


def kepler_drift(r, v, mu, dt):
    """Exact Kepler drift (r,v) by dt about mu. Vectorized over leading axis."""
    r0 = np.sqrt(np.sum(r * r, axis=-1))
    v2 = np.sum(v * v, axis=-1)
    rv = np.sum(r * v, axis=-1)
    alpha = 2.0 / r0 - v2 / mu            # 1/a
    sqmu = np.sqrt(mu)
    chi = sqmu * dt * np.maximum(np.abs(alpha), 1.0 / r0)
    for _ in range(60):
        z = alpha * chi * chi
        C, S = _stumpff(z)
        # F = sqrt(mu) * (t(chi) - dt)
        F = (rv / sqmu) * chi * chi * C + (1 - alpha * r0) * chi ** 3 * S \
            + r0 * chi - sqmu * dt
        f = 1 - chi * chi / r0 * C
        g = dt - chi ** 3 / sqmu * S
        rt2 = np.sum((f[..., None] * r + g[..., None] * v) ** 2, axis=-1)
        rtr = np.sqrt(np.maximum(rt2, 1e-300))
        dchi = -F / rtr          # dF/dchi = r(chi)  (Sundman)
        chi = chi + dchi
        if np.max(np.abs(dchi)) < 1e-13 * sqmu * abs(dt) + 1e-300:
            break
    z = alpha * chi * chi
    C, S = _stumpff(z)
    f = 1 - chi * chi / r0 * C
    g = dt - chi ** 3 / sqmu * S
    rn = f[..., None] * r + g[..., None] * v
    rn_abs = np.sqrt(np.sum(rn * rn, axis=-1))
    fdot = sqmu / (r0 * rn_abs) * chi * (z * S - 1)
    gdot = 1 - chi * chi / rn_abs * C
    vn = fdot[..., None] * r + gdot[..., None] * v
    return rn, vn


# ---------------- model ----------------

def accel_total(t, r, mu_p, R, n_out, M=1.0):
    """M-centered acceleration (indirect term included), shape (..., 2)."""
    ct, st = np.cos(n_out * t), np.sin(n_out * t)
    r3 = np.stack([R * ct, R * st], axis=-1)
    d = r - r3
    dn = np.sum(d * d, axis=-1)[..., None] ** 1.5
    return (-d / dn - r3 / R ** 3) * mu_p \
        + (-r / np.sum(r * r, axis=-1)[..., None] ** 1.5) * M


def kick_accel(t, r, mu_p, R, n_out, M=1.0):
    """Perturbation only (Kepler part is carried by the drift)."""
    ct, st = np.cos(n_out * t), np.sin(n_out * t)
    r3 = np.stack([R * ct, R * st], axis=-1)
    d = r - r3
    dn = np.sum(d * d, axis=-1)[..., None] ** 1.5
    return -mu_p * (d / dn + r3 / R ** 3)


def jacobi(t, r, v, mu_p, R, n_out, M=1.0):
    """CR3BP Jacobi constant (barycentric centrifugal, rotating velocity)."""
    ct, st = np.cos(n_out * t), np.sin(n_out * t)
    r3 = np.stack([R * ct, R * st], axis=-1)
    d = r - r3
    Rb = mu_p / (M + mu_p) * r3
    rb = r - Rb
    vrot = np.stack([v[..., 0] + n_out * r[..., 1],
                     v[..., 1] - n_out * r[..., 0]], axis=-1)
    return (n_out ** 2 * np.sum(rb * rb, axis=-1)
            + 2 * M / np.sqrt(np.sum(r * r, axis=-1))
            + 2 * mu_p / np.sqrt(np.sum(d * d, axis=-1))
            - np.sum(vrot * vrot, axis=-1))


def ecc_vec(r, v, M=1.0):
    """Complex eccentricity vector e*exp(i varpi), in-plane."""
    rn = np.sqrt(np.sum(r * r, axis=-1))
    rv = np.sum(r * v, axis=-1)
    v2 = np.sum(v * v, axis=-1)
    ex = (v2 / M - 1.0 / rn)[..., None] * (r / rn[..., None]) \
        - (rv / M)[..., None] * v
    return ex[..., 0] + 1j * ex[..., 1]


def state_from_elems(a, e, varpi, f0):
    """State at true anomaly f0 (polar form, mu=1)."""
    p = a * (1 - e * e)
    r0 = p / (1 + e * np.cos(f0)) * np.ones_like(np.asarray(f0, float) * np.asarray(varpi, float) + 1)
    ur = np.stack([np.cos(f0 + varpi), np.sin(f0 + varpi)], axis=-1)
    ut = np.stack([-np.sin(f0 + varpi), np.cos(f0 + varpi)], axis=-1)
    r = r0[..., None] * ur
    vr = np.sqrt(1.0 / p) * e * np.sin(f0)
    vt = np.sqrt(1.0 / p) * (1 + e * np.cos(f0))
    v = vr[..., None] * ur + vt[..., None] * ut
    return r, v


def run_map(n, n_orb, mu_p, R, n_out, seeds, twin=True):
    """DKD kick map at cadence n per inner radial period (a=1 => P=2pi)."""
    P = 2 * np.pi
    h = P / n
    N = len(seeds)
    f0 = np.array([s[0] for s in seeds])
    vp = np.array([s[1] for s in seeds])
    r, v = state_from_elems(1.0, 0.1, vp, f0)
    if twin:
        r2, v2 = r.copy(), v.copy()
        r2[..., 0] += 1e-12
    J0 = jacobi(0.0, r, v, mu_p, R, n_out)
    Z = [ecc_vec(r, v)]
    J = [np.zeros(N)]
    D2 = [np.zeros(N)]
    for k in range(n_orb):
        for i in range(n):
            t = (k * n + i + 0.5) * h
            r, v = kepler_drift(r, v, 1.0, h / 2)
            if twin:
                r2, v2 = kepler_drift(r2, v2, 1.0, h / 2)
            v = v + kick_accel(t, r, mu_p, R, n_out) * h
            if twin:
                v2 = v2 + kick_accel(t, r2, mu_p, R, n_out) * h
            r, v = kepler_drift(r, v, 1.0, h / 2)
            if twin:
                r2, v2 = kepler_drift(r2, v2, 1.0, h / 2)
        Z.append(ecc_vec(r, v))
        J.append(jacobi((k + 1) * P, r, v, mu_p, R, n_out) - J0)
        if twin:
            D2.append(np.sqrt(np.sum((r - r2) ** 2 + (v - v2) ** 2, axis=-1)))
    return np.array(Z), np.array(J), (np.array(D2) if twin else None)


def run_truth(n_orb, mu_p, R, n_out, seeds, rtol=1e-12):
    P = 2 * np.pi
    out = []
    for s in seeds:
        r0, v0 = state_from_elems(1.0, 0.1, s[1], s[0])
        r0 = np.asarray(r0).ravel(); v0 = np.asarray(v0).ravel()
        def f(t, y):
            a = accel_total(t, y[None, :2], mu_p, R, n_out)[0]
            return np.concatenate([y[2:], a])
        sol = solve_ivp(f, (0, n_orb * P), np.concatenate([r0, v0]),
                        method="DOP853", rtol=rtol, atol=1e-14,
                        dense_output=True)
        ts = np.arange(n_orb + 1) * P
        Y = sol.sol(ts)
        out.append((ts, ecc_vec(Y[:2].T, Y[2:].T),
                    jacobi(ts, Y[:2].T, Y[2:].T, mu_p, R, n_out)))
    return out


def exponent(k, d, kmin=20, floor=0.0):
    """log-log slope of d vs k on k>=kmin above floor."""
    m = (k >= kmin) & (d > 1.15 * floor) & np.isfinite(d) & (d > 0)
    if m.sum() < 8 or np.ptp(np.log(k[m])) < 1.0:
        return None
    return float(np.polyfit(np.log(k[m]), np.log(d[m]), 1)[0])


def twin_lambda(k, d):
    """linear-in-t slope of ln d on unsaturated window (per orbit)."""
    m = (d > 1e-9) & (d < 0.1)
    if m.sum() < 8:
        return None
    return float(np.polyfit(k[m], np.log(d[m]), 1)[0])


def machine_state():
    with open("/proc/loadavg") as f:
        la = f.read().strip()
    with open("/proc/meminfo") as f:
        mi = dict(l.split(":", 1) for l in f.read().splitlines() if ":" in l)
    return {"loadavg": la, "mem_available_kb": mi.get("MemAvailable", "?").strip()}


# ---------------- drivers ----------------

def do_instrument():
    """Controls: drift exactness; truth Jacobi constancy; noise floor."""
    P = 2 * np.pi
    # circular quarter/full-period roundtrip
    r = np.array([[1.0, 0.0]]); v = np.array([[0.0, 1.0]])
    rn, vn = kepler_drift(r, v, 1.0, P / 4)
    print("circular quarter: dr=%.2e dv=%.2e (expect [0,1],[-1,0])"
          % (np.linalg.norm(rn - [[0, 1]]), np.linalg.norm(vn - [[-1, 0]])))
    rn, vn = kepler_drift(r, v, 1.0, P)
    print("circular full   : dr=%.2e dv=%.2e"
          % (np.linalg.norm(rn - [[1, 0]]), np.linalg.norm(vn - [[0, 1]])))
    # eccentric: 512 sub-steps vs one drift
    re, ve = state_from_elems(1.0, 0.3, 0.7, 1.1)
    r1, v1 = kepler_drift(re, ve, 1.0, 0.37)
    rr, vv = re, ve
    for _ in range(512):
        rr, vv = kepler_drift(rr, vv, 1.0, 0.37 / 512)
    print("eccentric split : dr=%.2e dv=%.2e"
          % (np.linalg.norm(rr - r1), np.linalg.norm(vv - v1)))
    # truth: Jacobi constancy and tolerance floor
    mu_p, R = 0.02, 5.27
    n_out = np.sqrt((1 + mu_p) / R ** 3)
    seeds = [(0.3, 0.0), (2.1, 1.4)]
    tr = run_truth(200, mu_p, R, n_out, seeds)
    tr2 = run_truth(200, mu_p, R, n_out, seeds, rtol=1e-13)
    for i in range(len(seeds)):
        dJ = np.abs(tr[i][2] - tr[i][2][0])
        dz = np.abs(tr[i][1] - tr2[i][1])
        print("seed %d: truth |dJ|max=%.2e (rel %.1e)  |dz| between tols=%.2e"
              % (i, dJ.max(), dJ.max() / abs(tr[i][2][0]), dz.max()))
    return 0


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "instrument"
    if mode == "instrument":
        do_instrument()
        return
    R = float(sys.argv[2]) if len(sys.argv) > 2 else 5.27
    mu_list = [float(x) for x in sys.argv[3].split(",")]
    n_list = [int(x) for x in sys.argv[4].split(",")]
    n_orb = int(sys.argv[5]) if len(sys.argv) > 5 else 200
    n_seed = int(sys.argv[6]) if len(sys.argv) > 6 else 8
    out_path = sys.argv[7] if len(sys.argv) > 7 else "out.json"
    rng = np.random.default_rng(7)
    seeds = [(float(a), float(b)) for a, b in zip(
        rng.uniform(0, 2 * np.pi, n_seed), rng.uniform(0, 2 * np.pi, n_seed))]
    t_start = time.time()
    out = {"R": R, "f": R ** 1.5, "n_orb": n_orb, "machine": machine_state(),
           "rows": []}
    k = np.arange(n_orb + 1)
    for mu_p in mu_list:
        n_out = np.sqrt((1 + mu_p) / R ** 3)
        tr = run_truth(n_orb, mu_p, R, n_out, seeds)
        tr2 = run_truth(n_orb, mu_p, R, n_out, seeds, rtol=1e-13)
        floor_z = max(np.max(np.abs(a[1] - b[1])) for a, b in zip(tr, tr2))
        Zt = np.stack([t[1] for t in tr], axis=1)
        # physical-chaos control: twin truth runs, 1e-12 apart
        P2 = 2 * np.pi
        dtwin = {}
        for i in (0, 3):
            s = seeds[i]
            r0, v0 = state_from_elems(1.0, 0.1, s[1], s[0])
            r0 = np.asarray(r0).ravel(); v0 = np.asarray(v0).ravel()
            r0b = r0.copy(); r0b[0] += 1e-12

            def g(t, y):
                return np.concatenate([y[2:], accel_total(t, y[None, :2], mu_p, R, n_out)[0]])

            tb = solve_ivp(g, (0, n_orb * P2), np.concatenate([r0b, v0]),
                           method="DOP853", rtol=1e-12, atol=1e-14)
            ta = solve_ivp(g, (0, n_orb * P2), np.concatenate([r0, v0]),
                           method="DOP853", rtol=1e-12, atol=1e-14)
            dtwin[i] = float(np.linalg.norm(tb.y[:, -1] - ta.y[:, -1]))
        eps = mu_p / R ** 3
        for n in n_list:
            Z, J, D2 = run_map(n, n_orb, mu_p, R, n_out, seeds)
            rows = []
            for i in range(len(seeds)):
                dz = np.abs(Z[:, i] - Zt[:, i])
                gz = exponent(k, dz, 20, floor_z)
                gz_end = exponent(k, dz, max(20, n_orb // 2), floor_z)
                dJ = np.abs(J[:, i])
                gJ = exponent(k, dJ, 20, 1e-15)
                dw = np.unwrap(np.angle(Z[:, i] / Zt[:, i]))
                mw = k >= 20
                sl_d = np.polyfit(k[mw], dw[mw], 1)[0]
                wt = np.unwrap(np.angle(Zt[:, i]))
                sl_t = abs(np.polyfit(k[mw], wt[mw], 1)[0])
                rho = abs(sl_d) / sl_t if sl_t > 0 else None
                e_err = float(np.max(np.abs(np.abs(Z[mw, i]) - np.abs(Zt[mw, i]))))
                rows.append(dict(gz=gz, gz_end=gz_end, rho=rho, e_err=e_err,
                                 dz_end=float(dz[-1]), gJ=gJ,
                                 dJ_end=float(dJ[-1]),
                                 lam=twin_lambda(k, D2[:, i]),
                                 d2_end=float(D2[-1, i])))
            gzs = sorted(r["gz"] for r in rows if r["gz"] is not None)
            out["rows"].append(dict(
                mu=mu_p, eps=eps, n=n, floor_z=floor_z, dtwin=dtwin,
                seeds=rows,
                gz_med=gzs[len(gzs) // 2] if gzs else None,
                n_walk=sum(1 for r in rows if (r["gz"] or -1) > 0.3)))
            print("eps=%.2e n=%4d gz_med=%-6s walk=%d/%d dz_end_med=%.2e dJ_end_med=%.2e"
                  % (eps, n, out["rows"][-1]["gz_med"], out["rows"][-1]["n_walk"],
                     len(rows),
                     sorted(r["dz_end"] for r in rows)[len(rows) // 2],
                     sorted(r["dJ_end"] for r in rows)[len(rows) // 2]), flush=True)
    out["wall_s"] = time.time() - t_start
    with open(out_path, "w") as f:
        json.dump(out, f)


if __name__ == "__main__":
    main()
