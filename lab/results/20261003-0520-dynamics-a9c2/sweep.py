#!/usr/bin/env python3
"""Dynamics-lens run: does the kick layer's own instability (finite-time Lyapunov
exponent, measured for free on its own state) predict (a) where no affordable kick
rate holds the behaviour gate (changeover trigger, board focus 2), (b) the required
kick budget (focus 1), better than the law's static resonance detection
(p*Om1 - q*Om2 ~ 0)?  And does a threshold rule thrash (lens blind spot)?

Planar elliptic restricted 3-body, heliocentric:
  truth : Yoshida-4 symplectic float oracle, dt = T2/1024, twin => lambda_ref
  layer : exact Kepler drift (GM = 1-mu) + tidal kick at K per particle orbit (WH split)
          K in {1,2,4,8,16,32,64}; twin at K=16 => lambda_layer
Gate (behaviour-level, B17 flavour): e-pump ratio in [0.8,1.25] (or |de|<=0.03 when
  e_max_ref <= 0.05) AND resonant-angle regime match (librate vs circulate).
All lambdas are per-orbit mean log-stretchings of a renormalised twin.
"""
import sys
import math
import numpy as np

TWOPI = 2.0 * np.pi
E2 = 0.05          # secondary eccentricity
N_ORB = 256        # samples (orbit boundaries) per config
WINDOW = 32        # orbits per finite-time-lambda window
KS = [1, 2, 4, 8, 16, 32, 64]


# ---------------- secondary (analytic exact two-body) ----------------
def kepler_E(M, e=E2):
    E = M.copy()
    for _ in range(10):
        E = E - (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    return E


def secondary(t):
    """Secondary heliocentric position at times t (a=1, e=E2, varpi=0, M0=0).  t: (N,)"""
    M = np.mod(t, TWOPI)
    E = kepler_E(M)
    x = np.cos(E) - E2
    y = np.sqrt(1.0 - E2 * E2) * np.sin(E)
    return np.stack([x, y], axis=1)          # (N,2)


def accel(pos, t, mu):
    """Heliocentric acceleration of the particle. pos (N,2), t (N,), mu (N,)."""
    x2 = secondary(t)                        # (N,2)
    d2 = np.sum(x2 * x2, axis=1)
    diff = pos - x2
    r = np.sqrt(np.sum(pos * pos, axis=1))
    d = np.sqrt(np.sum(diff * diff, axis=1))
    gm = 1.0 - mu
    a = (-gm[:, None] * pos / r[:, None] ** 3
         + mu[:, None] * (x2 - pos) / d[:, None] ** 3
         - mu[:, None] * x2 / d2[:, None] ** 1.5)
    return a


def accel_tide(pos, t, mu):
    """Tide-only acceleration (secondary + indirect): the layer's kick.
    The primary's monopole is carried exactly by the Kepler drift."""
    x2 = secondary(t)
    d2 = np.sum(x2 * x2, axis=1)
    diff = pos - x2
    d = np.sqrt(np.sum(diff * diff, axis=1))
    return mu[:, None] * ((x2 - pos) / d[:, None] ** 3 - x2 / d2[:, None] ** 1.5)


# ---------------- Stumpff + universal Kepler drift ----------------
_FAC_C = np.array([math.factorial(2 * k + 2) for k in range(26)], dtype=float)
_FAC_S = np.array([math.factorial(2 * k + 3) for k in range(26)], dtype=float)


def stumpff(z):
    t = np.ones_like(z)
    C = np.zeros_like(z)
    S = np.zeros_like(z)
    for k in range(26):
        C += t / _FAC_C[k]
        S += t / _FAC_S[k]
        t = t * (-z)
    return C, S


def kepler_drift(pos, vel, h, gm, chi0=None):
    """Exact two-body drift over h via eccentric anomaly (bound orbits, e<0.999).
    Newton from Danby's starting guess; warm start unused. Returns (pos, vel, M)."""
    r0 = np.sqrt(np.sum(pos * pos, axis=1))
    v2 = np.sum(vel * vel, axis=1)
    a = 1.0 / (2.0 / r0 - v2 / gm)
    hz = pos[:, 0] * vel[:, 1] - pos[:, 1] * vel[:, 0]
    ex = (v2 / gm - 1.0 / r0)[:, None] * pos - (np.sum(pos * vel, axis=1) / gm)[:, None] * vel
    ee = np.sqrt(np.sum(ex * ex, axis=1))
    ecc = np.sqrt(np.maximum(1.0 - hz * hz / (gm * np.maximum(a, 1e-12)), 0.0))
    ecc = np.minimum(np.maximum(ecc, ee), 0.999)
    varpi = np.arctan2(ex[:, 1], ex[:, 0])
    nu = np.mod(np.arctan2(pos[:, 1], pos[:, 0]) - varpi, TWOPI)
    E = np.arctan2(np.sqrt(np.maximum(1.0 - ecc * ecc, 1e-12)) * np.sin(nu), ecc + np.cos(nu))
    n = np.sqrt(gm / np.maximum(a, 1e-12) ** 3)
    M = np.mod(E - ecc * np.sin(E) + n * h, TWOPI)
    # Danby starter
    EE = M + 0.85 * ecc * np.sign(np.sin(M))
    for _ in range(20):
        f = EE - ecc * np.sin(EE) - M
        fp = 1.0 - ecc * np.cos(EE)
        fpp = ecc * np.sin(EE)
        d = -f / fp
        EE = EE + d + 0.5 * fpp * d * d / fp
        if np.max(np.abs(d)) < 1e-14:
            break
    cE, sE = np.cos(EE), np.sin(EE)
    r = a * (1.0 - ecc * cE)
    # rotate (varpi) from perifocal to heliocentric
    cv, sv = np.cos(varpi), np.sin(varpi)
    xp, yp = a * (cE - ecc), a * np.sqrt(np.maximum(1.0 - ecc * ecc, 1e-12)) * sE
    kk = np.sqrt(gm * a) / r
    vxp, vyp = -kk * sE, kk * np.sqrt(np.maximum(1.0 - ecc * ecc, 1e-12)) * cE
    return (np.stack([cv * xp - sv * yp, sv * xp + cv * yp], axis=1),
            np.stack([cv * vxp - sv * vyp, sv * vxp + cv * vyp], axis=1),
            M)
def elements(pos, vel, gm):
    r = np.sqrt(np.sum(pos * pos, axis=1))
    v2 = np.sum(vel * vel, axis=1)
    a = 1.0 / (2.0 / r - v2 / gm)
    hz = pos[:, 0] * vel[:, 1] - pos[:, 1] * vel[:, 0]
    p = hz * hz / gm
    e = np.sqrt(np.maximum(0.0, 1.0 - p / np.maximum(a, 1e-12)))
    ex = (v2 / gm - 1.0 / r)[:, None] * pos - (np.sum(pos * vel, axis=1) / gm)[:, None] * vel
    ee = np.sqrt(np.maximum(np.sum(ex * ex, axis=1), 0.0))
    varpi = np.arctan2(ex[:, 1], ex[:, 0])
    return a, ee, varpi


def longitudes(pos, vel, gm, t):
    """Mean longitude of particle and secondary at times t."""
    a, e, varpi = elements(pos, vel, gm)
    nu = np.arctan2(pos[:, 1], pos[:, 0]) - varpi
    E = np.arctan2(np.sqrt(np.maximum(1.0 - e * e, 0.0)) * np.sin(nu), e + np.cos(nu))
    lam = varpi + E - e * np.sin(E)
    E2v = kepler_E(np.mod(t, TWOPI))
    nu2 = np.arctan2(np.sqrt(1 - E2**2) * np.sin(E2v), np.cos(E2v) - E2)
    lam2 = nu2
    return lam, lam2, varpi


# ---------------- config grid ----------------
def build_grid():
    mus = [3e-5, 1e-4, 3e-4, 1e-3, 3e-3]
    a_res = 2.0 ** (-2.0 / 3.0)
    rows = []
    for mu in mus:
        W = 2.5 * mu ** (2.0 / 3.0)
        dets = [k / 3.0 for k in range(-6, 7)] + [min(20.0, 0.3 / W)]
        for dd in dets:
            for ph in [0.0, np.pi / 2]:
                rows.append((mu, a_res * (1.0 + dd * W), ph, dd))
    return np.array(rows)


def init_state(grid):
    mu = grid[:, 0]
    a0 = grid[:, 1]
    ph = grid[:, 2]
    e0 = 0.02
    gm = 1.0 - mu
    n0 = np.sqrt(gm / a0 ** 3)
    cE, sE = np.cos(ph), np.sin(ph)
    r = a0 * (1.0 - e0 * cE)
    x = a0 * (cE - e0)
    y = a0 * np.sqrt(1 - e0 * e0) * sE
    k = np.sqrt(gm * a0) / r
    vx = -k * sE
    vy = k * np.sqrt(1 - e0 * e0) * cE
    return np.stack([x, y], axis=1), np.stack([vx, vy], axis=1), n0
def sample_and_renorm(pos, vel, lpos, lvel, gm, t, d0,
                      e_s, phi_s, lam, idx, norb, twin=True):
    a, e, varpi = elements(pos[idx], vel[idx], gm[idx])
    lam_p, lam2, _ = longitudes(pos[idx], vel[idx], gm[idx], t[idx])
    phi = np.mod(2.0 * lam2 - lam_p - varpi, TWOPI)
    e_s[idx, norb[idx]] = e
    phi_s[idx, norb[idx]] = phi
    if twin:
        dd = np.sqrt(np.sum((lpos[idx] - pos[idx]) ** 2, axis=1)
                     + np.sum((lvel[idx] - vel[idx]) ** 2, axis=1))
        lam[idx, norb[idx]] = np.log(np.maximum(dd, 1e-300) / d0)
        sc = d0 / np.maximum(dd, 1e-300)
        lpos[idx] = pos[idx] + (lpos[idx] - pos[idx]) * sc[:, None]
        lvel[idx] = vel[idx] + (lvel[idx] - vel[idx]) * sc[:, None]


def handle_bad(pos, esc, col, t):
    r = np.sqrt(np.sum(pos * pos, axis=1))
    x2 = secondary(t)
    d = np.sqrt(np.sum((pos - x2) ** 2, axis=1))
    esc |= (~np.isfinite(r) | ~np.isfinite(d) | (r > 50.0)) & ~col
    col |= (d < 1e-3) & ~esc
    return esc | col


def fill_forward(e_s, phi_s):
    e_s[:, 0][e_s[:, 0] == 0.0] = 1.0
    for j in range(1, e_s.shape[1]):
        m = e_s[:, j] == 0.0
        e_s[m, j] = e_s[m, j - 1]
        phi_s[m, j] = phi_s[m, j - 1]

# ---------------- truth: Yoshida 4 ----------------
def run_truth(grid, pos, vel, dt_frac=1024.0):
    mu = grid[:, 0]
    gm = 1.0 - mu
    n0 = np.sqrt(gm / grid[:, 1] ** 3)
    T_end = N_ORB * TWOPI / n0[0]
    dt = TWOPI / dt_frac
    ns = int(np.ceil(T_end / dt))
    ncfg = len(grid)

    d0 = 1e-12
    # particle and its twin integrated as one array (rows 0..ncfg-1, ncfg..2ncfg-1)
    S = np.vstack([pos, pos])
    S[ncfg:, 0] += d0
    V = np.vstack([vel, vel])
    mu2 = np.concatenate([mu, mu])

    e_s = np.zeros((ncfg, N_ORB)); phi_s = np.zeros((ncfg, N_ORB))
    lam = np.zeros((ncfg, N_ORB))
    esc = np.zeros(ncfg, bool); col = np.zeros(ncfg, bool)
    norb = np.zeros(ncfg, int)
    tarr = np.zeros(ncfg)

    cr = 2.0 ** (1.0 / 3.0)
    c1 = 1.0 / (2.0 - 2.0 * cr)
    c2 = -2.0 * cr * c1

    def yoshida4(p, v, tt):
        # kick-drift triple jump: kicks sum to 1, drifts sum to dt
        v = v + (c1 * dt * 0.5) * accel(p, tt, mu2)
        p = p + (c1 * dt) * v
        v = v + ((c1 + c2) * dt * 0.5) * accel(p, tt + c1 * dt, mu2)
        p = p + (c2 * dt) * v
        v = v + ((c2 + c1) * dt * 0.5) * accel(p, tt + (c1 + c2) * dt, mu2)
        p = p + (c1 * dt) * v
        v = v + (c1 * dt * 0.5) * accel(p, tt + dt, mu2)
        return p, v

    for step in range(ns):
        tt = np.concatenate([tarr, tarr])
        S, V = yoshida4(S, V, tt)
        tarr += dt
        bad = handle_bad(S[:ncfg], esc, col, tarr)
        crossed = (norb < N_ORB) & (tarr >= (norb + 1) * TWOPI / n0) & ~bad
        while np.any(crossed):
            idx = np.where(crossed)[0]
            sample_and_renorm(S[:ncfg], V[:ncfg], S[ncfg:], V[ncfg:], gm, tarr, d0,
                              e_s, phi_s, lam, idx, norb)
            S[ncfg:][idx] = S[:ncfg][idx] + (S[ncfg:][idx] - S[:ncfg][idx])  # no-op, keep linter calm
            norb[idx] += 1
            crossed = (norb < N_ORB) & (tarr >= (norb + 1) * TWOPI / n0) & ~bad
    fill_forward(e_s, phi_s)
    return dict(e_s=e_s, phi_s=phi_s, lam=lam, esc=esc, col=col)


# ---------------- layer: exact drift + tidal kick ----------------
def run_layer(grid, pos, vel, K, twin=False):
    mu = grid[:, 0]
    gm = 1.0 - mu
    a0 = grid[:, 1]
    n0 = np.sqrt(gm / a0 ** 3)
    T_p0 = TWOPI / n0
    h = T_p0 / K
    ncfg = len(grid)
    T_end = N_ORB * TWOPI / n0[0]
    nsteps = int(np.ceil(T_end / h.min()))

    lpos, lvel = pos.copy(), vel.copy()
    chi = np.sqrt(gm) * h / a0
    d0 = 1e-9
    lpos2, lvel2 = None, None
    if twin:
        lpos2 = lpos.copy(); lpos2[:, 0] += d0
        lvel2 = lvel.copy()

    e_s = np.zeros((ncfg, N_ORB)); phi_s = np.zeros((ncfg, N_ORB))
    lam = np.zeros((ncfg, N_ORB))
    esc = np.zeros(ncfg, bool); col = np.zeros(ncfg, bool)
    norb = np.zeros(ncfg, int)
    tarr = np.zeros(ncfg)

    for step in range(nsteps):
        act = ~esc & ~col
        if not np.any(act):
            break
        idx = np.where(act)[0]
        tmid = tarr[idx] + h[idx] * 0.5
        p, v, chi[idx] = kepler_drift(lpos[idx], lvel[idx], h[idx] * 0.5, gm[idx], chi[idx])
        lpos[idx], lvel[idx] = p, v
        lvel[idx] += h[idx, None] * accel_tide(lpos[idx], tmid, mu[idx])
        p, v, chi[idx] = kepler_drift(lpos[idx], lvel[idx], h[idx] * 0.5, gm[idx], chi[idx])
        lpos[idx], lvel[idx] = p, v
        tarr[idx] += h[idx]
        if twin:
            chi2 = np.sqrt(gm[idx]) * h[idx] / a0[idx]
            p, v, _ = kepler_drift(lpos2[idx], lvel2[idx], h[idx] * 0.5, gm[idx], chi2)
            lpos2[idx], lvel2[idx] = p, v
            lvel2[idx] += h[idx, None] * accel_tide(lpos2[idx], tmid, mu[idx])
            p, v, _ = kepler_drift(lpos2[idx], lvel2[idx], h[idx] * 0.5, gm[idx], chi2)
            lpos2[idx], lvel2[idx] = p, v
        bad = handle_bad(lpos, esc, col, tarr)
        crossed = (norb < N_ORB) & (tarr >= (norb + 1) * TWOPI / n0) & ~bad
        while np.any(crossed):
            ii = np.where(crossed)[0]
            sample_and_renorm(lpos, lvel, lpos2, lvel2,
                              gm, tarr, d0,
                              e_s, phi_s, lam, ii, norb, twin=bool(twin))
            norb[ii] += 1
            crossed = (norb < N_ORB) & (tarr >= (norb + 1) * TWOPI / n0) & ~bad
    fill_forward(e_s, phi_s)
    return dict(e_s=e_s, phi_s=phi_s, lam=lam, esc=esc, col=col)


def unwrap_phi(phi_s):
    up = np.unwrap(phi_s, axis=1)
    wind = np.abs(up[:, -1] - up[:, 0])
    j = np.arange(up.shape[1])[None, :]
    slope = (up[:, -1] - up[:, 0]) / (up.shape[1] - 1)
    detr = up - up[:, :1] - slope * j
    amp = np.max(detr, axis=1) - np.min(detr, axis=1)
    return wind, amp


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    grid = build_grid()
    if mode == "smoke":
        global N_ORB
        N_ORB = 60
        grid = grid[:: max(1, len(grid) // 6)][:6]
    pos, vel, n0 = init_state(grid)
    out = {}
    out["truth"] = run_truth(grid, pos, vel)
    out["layer16"] = run_layer(grid, pos, vel, 16, twin=True)
    for K in KS:
        out[f"lay{K}"] = run_layer(grid, pos, vel, K)
    np.savez_compressed(
        "results.npz", grid=grid,
        **{f"{k}__{f}": v[f] for k, v in out.items() for f in ("e_s", "phi_s", "lam", "esc", "col")},
    )
    print("saved:", {k: tuple(v["e_s"].shape) for k, v in out.items()},
          "esc:", int(out["truth"]["esc"].sum()), "col:", int(out["truth"]["col"].sum()))


if __name__ == "__main__":
    main()
