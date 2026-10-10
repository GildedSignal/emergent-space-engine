#!/usr/bin/env python3
"""Kick-cadence sufficiency in a belt, on the engine's own split.

Drift = exact Kepler (universal variables, the 'tube': zero work).
Kick  = Jupiter's full tide (direct + indirect), one impulse per step.
Question: per body, what is the minimum kicks per Jupiter orbit that
reproduces the body's BEHAVIOUR (mean/std/max of e(t)), and does the
resonance proximity zeta (computable from birth elements = the compiled
frequencies) predict it?

Usage: cadence.py <belt> <orbits> <k1,k2,...> [ftle] -> writes out_<belt>.npz
"""
import sys
import numpy as np

MU_S = 4.0 * np.pi ** 2          # AU^3 / yr^2 (Sun)
A_J = 5.204                       # AU
MUJ = 9.545937e-4                 # m_J / m_S
NJ = np.sqrt(MU_S * (1 + MUJ) / A_J ** 3)


def stumpff(z):
    """C(z), S(z), safe near 0."""
    z = np.asarray(z, dtype=float)
    C = np.empty_like(z); S = np.empty_like(z)
    small = np.abs(z) < 1e-6
    zs = z[small]
    # series for small z
    C[small] = 0.5 - zs / 24.0 + zs * zs / 720.0
    S[small] = 1.0 / 6.0 - zs / 120.0 + zs * zs / 5040.0
    big = ~small
    pos = z[big] > 0
    zp = z[big][pos]; zn = -z[big][~pos]
    Cb = np.empty_like(z[big]); Sb = np.empty_like(z[big])
    Cb[pos] = (1 - np.cos(np.sqrt(zp))) / zp
    Sb[pos] = (np.sqrt(zp) - np.sin(np.sqrt(zp))) / zp ** 1.5
    Cb[~pos] = (np.cosh(np.sqrt(zn)) - 1) / zn
    Sb[~pos] = (np.sinh(np.sqrt(zn)) - np.sqrt(zn)) / zn ** 1.5
    C[big] = Cb; S[big] = Sb
    return C, S


def kepler_drift(state, dt, mu=MU_S):
    """Exact Kepler drift dt, universal variables. state (..., 4)."""
    x, y, vx, vy = state[..., 0], state[..., 1], state[..., 2], state[..., 3]
    r0 = np.hypot(x, y)
    v2 = vx * vx + vy * vy
    vr = (x * vx + y * vy) / r0
    alpha = 2.0 / r0 - v2 / mu          # <0 bound
    sq = np.sqrt(mu)
    # starter: small-chi
    chi = np.sqrt(mu) * dt / r0 * np.ones_like(r0)
    for _ in range(6):
        z = alpha * chi * chi
        C, S = stumpff(z)
        F = (r0 * vr / sq) * chi * chi * C + (1 - alpha * r0) * chi ** 3 * S + r0 * chi - sq * dt
        dF = (r0 * vr / sq) * chi * (1 - z * S) + (1 - alpha * r0) * chi * chi * C + r0
        chi = chi - F / dF
    z = alpha * chi * chi
    C, S = stumpff(z)
    f = 1 - chi * chi / r0 * C
    g = dt - chi ** 3 / sq * S
    xn = f * x + g * vx
    yn = f * y + g * vy
    rn = np.hypot(xn, yn)
    fd = sq / (rn * r0) * chi * (z * S - 1)
    gd = 1 - chi * chi / rn * C
    out = np.empty_like(state)
    out[..., 0] = xn; out[..., 1] = yn
    out[..., 2] = fd * x + gd * vx; out[..., 3] = fd * y + gd * vy
    return out


def jupiter_kick(state, t, dt, muj=MUJ):
    x, y = state[..., 0], state[..., 1]
    xj, yj = A_J * np.cos(NJ * t), A_J * np.sin(NJ * t)
    dx, dy = xj - x, yj - y
    d3 = (dx * dx + dy * dy) ** 1.5
    state[..., 2] += muj * dt * (dx / d3 - xj / A_J ** 3)
    state[..., 3] += muj * dt * (dy / d3 - yj / A_J ** 3)


def ecc(state):
    x, y, vx, vy = state[..., 0], state[..., 1], state[..., 2], state[..., 3]
    r = np.hypot(x, y); v2 = vx * vx + vy * vy
    rv = x * vx + y * vy
    ex = ((v2 - MU_S / r) * x - rv * vx) / MU_S
    ey = ((v2 - MU_S / r) * y - rv * vy) / MU_S
    return np.hypot(ex, ey), (x * vy - y * vx)  # e, h


def make_belt(n, a_lo, a_hi, e_scale, seed, muj=MUJ):
    rng = np.random.default_rng(seed)
    a = rng.uniform(a_lo, a_hi, n)
    e = rng.rayleigh(e_scale, n)
    w = rng.uniform(0, 2 * np.pi, n)
    M = rng.uniform(0, 2 * np.pi, n)
    p = a * (1 - e * np.cos(M))          # rough r; use exact: solve not needed,
    # place at radius from true anomaly nu~M (e small): fine for a birth scene.
    nu = M  # small-e approximation of position angle
    r = a * (1 - e ** 2) / (1 + e * np.cos(nu))
    th = w + nu
    x, y = r * np.cos(th), r * np.sin(th)
    # velocity in plane (elliptic formula)
    mu = MU_S
    h = np.sqrt(mu * a * (1 - e ** 2))
    vr = mu / h * e * np.sin(nu)
    vt = h / r
    vx = vr * np.cos(th) - vt * np.sin(th)
    vy = vr * np.sin(th) + vt * np.cos(th)
    state = np.stack([x, y, vx, vy], axis=-1)
    return state, a, e


def run(state0, orbits, kicks_per_orbit, muj=MUJ, ftle=False, sample_every=4):
    P_J = 2 * np.pi / NJ
    T = orbits * P_J
    dt = P_J / kicks_per_orbit
    nsteps = int(round(T / dt))
    state = state0.copy()
    state = kepler_drift(state, dt / 2)
    if ftle:
        shadow = state + 1e-8 * np.ones_like(state)
        shadow[:, 0] += 1e-8
    nbody = state.shape[0]
    nsamp = nsteps // (kicks_per_orbit * sample_every)
    es = np.empty((nsamp, nbody), dtype=np.float32)
    lyap = np.zeros(nbody)
    si = 0
    step_per_sample = kicks_per_orbit * sample_every
    for i in range(nsteps):
        t = (i + 0.5) * dt
        jupiter_kick(state, t, dt, muj)
        if ftle:
            jupiter_kick(shadow, t, dt, muj)
        state = kepler_drift(state, dt)
        if ftle:
            shadow = kepler_drift(shadow, dt)
            d = shadow - state
            # measure + renormalize every half Jupiter orbit
            if (i + 1) % (kicks_per_orbit // 2 or 1) == 0:
                dist = np.sqrt((d * d).sum(axis=-1))
                lyap += np.log(dist / 1e-8)
                shadow = state + d * (1e-8 / np.maximum(dist, 1e-300))[..., None]
        if (i + 1) % step_per_sample == 0 and si < nsamp:
            es[si] = ecc(state)[0]
            si += 1
    return es, lyap / T


BELTS = {
    "A": dict(n=2048, a_lo=2.0, a_hi=3.6, e_scale=0.05, seed=11, muj=MUJ),
    "B": dict(n=1536, a_lo=3.6, a_hi=4.6, e_scale=0.12, seed=22, muj=MUJ),
    "C": dict(n=1536, a_lo=2.0, a_hi=3.6, e_scale=0.05, seed=33, muj=3 * MUJ),
}


def main():
    belt = sys.argv[1]
    orbits = int(sys.argv[2])
    cadences = [int(c) for c in sys.argv[3].split(",")]
    ftle = len(sys.argv) > 4 and sys.argv[4] == "ftle"
    tag = sys.argv[5] if len(sys.argv) > 5 else ""
    cfg = BELTS[belt]
    state0, a0, e0 = make_belt(cfg["n"], cfg["a_lo"], cfg["a_hi"], cfg["e_scale"], cfg["seed"])
    np.savez(f"out_{belt}_birth.npz", a=a0, e=e0)
    out = {}
    for K in cadences:
        es, lyap = run(state0, orbits, K, cfg["muj"], ftle=(ftle and K == max(cadences)))
        out[f"e{K}"] = es
        if ftle and K == max(cadences):
            out["lyap"] = lyap
        print(f"belt {belt} K={K} done", flush=True)
    np.savez(f"out_{belt}{tag}.npz", **out)


if __name__ == "__main__":
    main()
