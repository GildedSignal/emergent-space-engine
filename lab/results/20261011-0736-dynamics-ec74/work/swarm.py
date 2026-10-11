"""Conjunction-scattering swarm toy (dynamics lens, run 20261011-0736-dynamics-ec74).

One star (GM=1, units a=1, v_K=1, orbit=2pi). N bodies in a ring a in [1-w/2, 1+w/2],
Rayleigh e. Exact Kepler drift; at each closest-approach passage of a pair, one
Rutherford rotation of the relative velocity (the engine's own one-kick-per-conjunction
philosophy, law.md "kicks"). Equal masses m; coupling Psi = mu_g/(a*sigma_e)^3.

Events counted at thresholds (element change per kick >= q): the engine's per-body
event load. All impulses applied in float (floats explore).
"""
import numpy as np
import json, sys, time

TWO_PI = 2.0 * np.pi

# ---------- Kepler machinery ----------

def kepler_states(a, e, varpi, M0, t):
    n = a ** (-1.5)
    M = np.mod(M0 + n * t, TWO_PI)
    E = M.copy()
    for _ in range(10):
        E = E - (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    sa = np.sqrt(np.maximum(1.0 - e * e, 1e-12))
    cE, sE = np.cos(E), np.sin(E)
    x0 = a * (cE - e)
    y0 = a * sa * sE
    Edot = n / (1.0 - e * cE)
    vx0 = -a * sE * Edot
    vy0 = a * sa * cE * Edot
    c, s = np.cos(varpi), np.sin(varpi)
    return (x0 * c - y0 * s, x0 * s + y0 * c,
            vx0 * c - vy0 * s, vx0 * s + vy0 * c)


def elements_from_state(x, y, vx, vy, t):
    """(a, e, varpi, M0) from state at time t (GM=1)."""
    r = np.hypot(x, y)
    v2 = vx * vx + vy * vy
    a = 1.0 / (2.0 / r - v2)
    rv = x * vx + y * vy
    ex = (v2 - 1.0 / r) * x - rv * vx
    ey = (v2 - 1.0 / r) * y - rv * vy
    e = np.hypot(ex, ey)
    varpi = np.arctan2(ey, ex)
    # E from position: cosE=(1-r/a)/e ; sinE has sign of r.v (outbound positive)
    cosE = np.clip((1.0 - r / a) / np.maximum(e, 1e-15), -1.0, 1.0)
    sinE = np.clip(rv / (np.maximum(e, 1e-15) * np.sqrt(a)), -1.0, 1.0)
    E = np.arctan2(sinE, cosE)
    M = E - e * np.sin(E)
    n = a ** (-1.5)
    M0 = np.mod(M - n * t, TWO_PI)
    return a, e, varpi, M0


# ---------- swarm ----------

class Swarm:
    def __init__(self, N=400, w=0.02, sigma_e=0.02, m=1e-8, seed=0):
        rng = np.random.default_rng(seed)
        self.N = N
        self.a = rng.uniform(1.0 - w / 2, 1.0 + w / 2, N)
        self.e = rng.rayleigh(sigma_e, N)
        self.varpi = rng.uniform(0, TWO_PI, N)
        self.M0 = rng.uniform(0, TWO_PI, N)
        self.m = m                      # per-body GM (units GM_star=1)
        self.mu_g = 2.0 * m             # pair GM
        self.u_floor_sigma = sigma_e
        self.n_capture = 0
        self.log = []                   # (t, i, j, chi, da, de)
        self.orbit_counts = {}          # orbit index -> impulse count

    def perturb(self, ib=0, dM=1e-9):
        self.M0[ib] = np.mod(self.M0[ib] + dM, TWO_PI)

    def step_all(self, t, dt, K=6):
        """Advance one sample step: detect closest approaches between angle
        neighbours (rank<=K) and apply one Rutherford impulse per passage."""
        a, e, varpi, M0 = self.a, self.e, self.varpi, self.M0
        x1, y1, vx1, vy1 = kepler_states(a, e, varpi, M0, t - dt)
        x2, y2, vx2, vy2 = kepler_states(a, e, varpi, M0, t)
        lam = np.arctan2(y2, x2)
        order = np.argsort(lam)
        A = np.concatenate([order for _ in range(K)])
        B = np.concatenate([np.roll(order, -k) for k in range(1, K + 1)])
        # relative states at t-dt and t
        def rel(xs, ys, vxs, vys):
            return (xs[A] - xs[B], ys[A] - ys[B], vxs[A] - vxs[B], vys[A] - vys[B])
        px0, py0, ux0, uy0 = rel(x1, y1, vx1, vy1)
        px, py, ux, uy = rel(x2, y2, vx2, vy2)
        s_prev = px0 * ux0 + py0 * uy0          # <0 approaching
        s_now = px * ux + py * uy                # >0 separating
        cross = (s_prev < 0.0) & (s_now >= 0.0)
        if not np.any(cross):
            return 0
        iA, iB = A[cross], B[cross]
        px, py, ux, uy = px[cross], py[cross], ux[cross], uy[cross]
        u = np.hypot(ux, uy)
        b_signed = (px * uy - py * ux) / np.maximum(u, 1e-14)
        b = np.abs(b_signed)
        # Encounter tier: only inside the Hill sphere. Outside it the passage is
        # shear-shielded (RK4 control: Rutherford off by 2-5x there) and belongs
        # to the orbit-averaged kick layer, not to discrete encounter events.
        b_H = 3.0 * (self.mu_g / 3.0) ** (1.0 / 3.0)
        # co-orbital captures: near-zero relative speed at closest approach.
        # The Rutherford impulse is invalid there (chi -> pi for any b); count
        # them as capture events but do not apply an impulse.
        slow = u < 0.2 * self.u_floor_sigma
        strong = (b < b_H) & ~slow
        self.n_capture += int(((b < b_H) & slow).sum())
        iA, iB, b_signed = iA[strong], iB[strong], b_signed[strong]
        if len(iA) == 0:
            return 0
        px, py, ux, uy = px[strong], py[strong], ux[strong], uy[strong]
        u = u[strong]
        chi = 2.0 * np.arctan(self.mu_g / np.maximum(b[strong] * u * u, 1e-14))
        keep = chi > 1e-6
        iA, iB, b_signed, chi = iA[keep], iB[keep], b_signed[keep], chi[keep]
        if len(iA) == 0:
            return 0
        # Rutherford rotation of relative velocity, toward the other body
        # (attractive): rotate u by sign(b)*chi
        ang = np.sign(b_signed) * chi
        ca, sa = np.cos(ang), np.sin(ang)
        # per-body state at t
        xi, yi, vxi, vyi = kepler_states(self.a, self.e, self.varpi, self.M0, t)
        n_hit = 0
        for k in range(len(iA)):
            i, j = iA[k], iB[k]
            uxij = vxi[i] - vxi[j]
            uyij = vyi[i] - vyi[j]
            c, s = ca[k], sa[k]
            uxo = c * uxij - s * uyij
            uyo = s * uxij + c * uyij
            dux, duy = (uxo - uxij) / 2.0, (uyo - uyij) / 2.0  # equal masses
            # old elements for the delta log
            a_i, e_i = self.a[i], self.e[i]
            # apply
            vxi[i] += dux; vyi[i] += duy
            vxi[j] -= dux; vyi[j] -= duy
            self.a[i], self.e[i], self.varpi[i], self.M0[i] = elements_from_state(
                xi[i], yi[i], vxi[i], vyi[i], t)
            self.a[j], self.e[j], self.varpi[j], self.M0[j] = elements_from_state(
                xi[j], yi[j], vxi[j], vyi[j], t)
            d_a = abs(self.a[i] - a_i) / 1.0
            self.log.append((t, int(i), int(j), float(chi[k]),
                             float(abs(self.a[i] - a_i)), float(abs(self.e[i] - e_i))))
            n_hit += 1
            oi = int(t / TWO_PI)
            self.orbit_counts[oi] = self.orbit_counts.get(oi, 0) + 1
        return n_hit


def run_swarm(psi, N=400, w=0.02, sigma_e=0.02, T_orbits=200, S=128, seed=0,
              K=6, perturb=None, record_every=1):
    m = psi * sigma_e ** 3 / 2.0
    sw = Swarm(N=N, w=w, sigma_e=sigma_e, m=m, seed=seed)
    if perturb is not None:
        sw.perturb(ib=perturb[0], dM=perturb[1])
    dt = TWO_PI / S
    nsteps = int(T_orbits * S)
    sig_e_t = np.empty(T_orbits + 1)
    sig_a_t = np.empty(T_orbits + 1)
    lam_t = np.zeros(T_orbits + 1)      # angular positions snapshot (for divergence)
    tsnap = np.arange(0, T_orbits + 1) * TWO_PI
    x, y, _, _ = kepler_states(sw.a, sw.e, sw.varpi, sw.M0, 0.0)
    sig_e_t[0] = np.sqrt(np.mean(sw.e ** 2))
    sig_a_t[0] = np.std(sw.a)
    lam_snap = []
    t = 0.0
    per_orbit_hits = np.zeros(T_orbits + 1)
    for step in range(nsteps):
        t += dt
        hits = sw.step_all(t, dt, K=K)
        per_orbit_hits[int(t / TWO_PI)] += hits
    for oi, tt in enumerate(tsnap):
        if oi == 0:
            continue
        sig_e_t[oi] = np.sqrt(np.mean(sw.e ** 2))
        sig_a_t[oi] = np.std(sw.a)
    x, y, _, _ = kepler_states(sw.a, sw.e, sw.varpi, sw.M0, t)
    lam_final = np.arctan2(y, x)
    return sw, dict(psi=psi, m=m, N=N, w=w, sigma_e0=sigma_e, T_orbits=T_orbits,
                    S=S, seed=seed, sig_e=sig_e_t.tolist(), sig_a=sig_a_t.tolist(),
                    per_orbit_hits=per_orbit_hits.tolist(),
                    log=sw.log, lam_final=lam_final.tolist())

def run_pair(psi, N=300, w=0.04, sigma_e=0.04, T_orbits=200, S=128, seed=0,
             K=6, dM=1e-9):
    """Twin runs: identical except every M0 shifted by dM. Returns the RMS
    angular separation per orbit (divergence of the event-coupled flow)."""
    m = psi * sigma_e ** 3 / 2.0
    A = Swarm(N=N, w=w, sigma_e=sigma_e, m=m, seed=seed)
    B = Swarm(N=N, w=w, sigma_e=sigma_e, m=m, seed=seed)
    B.M0 = np.mod(B.M0 + dM, TWO_PI)
    dt = TWO_PI / S
    nsteps = int(T_orbits * S)
    D = np.empty(T_orbits + 1)
    x, y, _, _ = kepler_states(A.a, A.e, A.varpi, A.M0, 0.0)
    x2, y2, _, _ = kepler_states(B.a, B.e, B.varpi, B.M0, 0.0)
    dl = np.arctan2(y, x) - np.arctan2(y2, x2)
    D[0] = np.sqrt(np.mean(np.mod(dl + np.pi, TWO_PI) ** 2))
    t = 0.0
    for step in range(nsteps):
        t += dt
        A.step_all(t, dt, K=K)
        B.step_all(t, dt, K=K)
        oi = int(t / TWO_PI)
        if (step + 1) % S == 0:
            x, y, _, _ = kepler_states(A.a, A.e, A.varpi, A.M0, t)
            x2, y2, _, _ = kepler_states(B.a, B.e, B.varpi, B.M0, t)
            dl = np.arctan2(y, x) - np.arctan2(y2, x2)
            D[oi] = np.sqrt(np.mean(np.mod(dl + np.pi, TWO_PI) ** 2))
    return A, B, D


if __name__ == "__main__":
    t0 = time.time()
    psi = float(sys.argv[1]) if len(sys.argv) > 1 else 3e-3
    T = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    N = int(sys.argv[3]) if len(sys.argv) > 3 else 400
    S = int(sys.argv[4]) if len(sys.argv) > 4 else 128
    sw, res = run_swarm(psi, N=N, T_orbits=T, S=S)
    log = np.array([l[:1] + l[3:] for l in res["log"]])  # t, chi, da, de
    out = dict(psi=res["psi"], m=res["m"], N=N, T_orbits=T, S=S,
               wall_s=time.time() - t0,
               n_impulses=len(log),
               sig_e0=res["sig_e"][0], sig_e_final=res["sig_e"][-1],
               sig_a0=res["sig_a"][0], sig_a_final=res["sig_a"][-1])
    print(json.dumps(out, indent=1))
