#!/usr/bin/env python3
"""Scout falsifier: when do orbit-averaged / epoch-kicked tides pump a doll member?

Model (1-D prototype of the phase-2 Fermi tide along an eccentric tube):
  member coordinate x (one tide eigen-channel), member binding Omega_m:
      x'' + [Omega_m^2 - alpha * lambda(tau)] x = 0
  lambda(tau) = u(tau)^3 * (3*gamma(tau)^2 - 1),  gamma = E/sqrt(1-2u)  (M=1)
  The closed form is that of lab run 20261006-0220-q-fermi2-tide-v2-26a7
  ("the radial tide -w(3 gamma^2 - 1)"), Newtonian limit 2/r^3.
  alpha=+1: the tide REDUCES stiffness (moon-like radial channel, Hill).
  alpha=-1: the tide ADDS stiffness (compressive channel).

Laws compared over one radial period T_r (lambda is periodic in tau with T_r):
  truth : full lambda(tau), RK4 (verified against scipy solve_ivp to 1e-6)
  avg   : constant lambda_bar (orbit-averaged tide; the 114x lever of H0190)
  holdK : lambda held piecewise-constant at K uniform epochs per period, each
          segment propagated EXACTLY (rotation/hyperbolic segment map)
  kickK : free drift + one velocity kick per epoch (lambda sampled at the
          epoch) -- the drift-kick reading of "exact integer kicks at epochs"

Certificate: Floquet. monodromy M over T_r; |tr M| <= 2 stable;
mu = acosh(|tr M|/2)/T_r, reported per orbit as mu*T_r.
Band prediction (first-order Floquet/Mathieu): bands where 2*omega_eff = k*Om_r
with omega_eff^2 = Om_m^2 - alpha*lam_bar; widths grow with |lam_hat_k|.
"""
import json
import sys
import numpy as np
from scipy.integrate import solve_ivp


def constants(rp, e):
    """E, L from turning points rp, ra of a bound equatorial Schwarzschild orbit."""
    if e < 1e-12:  # circular: L^2 = r^2/(r-3), E^2 = (1-2/r)^2/(1-3/r)
        L2 = rp**2 / (rp - 3.0)
        E2 = (1 - 2 / rp) ** 2 / (1 - 3 / rp)
        return np.sqrt(E2), np.sqrt(L2), rp
    ra = rp * (1 + e) / (1 - e)
    num = (1 - 2 / ra) - (1 - 2 / rp)
    den = (1 - 2 / rp) / rp**2 - (1 - 2 / ra) / ra**2
    L2 = num / den
    E2 = (1 - 2 / rp) * (1 + L2 / rp**2)
    return np.sqrt(E2), np.sqrt(L2), ra


def orbit_lambda(rp, e, n_tau=12001):
    """Exact eccentric geodesic via Darwin psi; lambda(tau) on a UNIFORM
    proper-time grid covering exactly one radial period."""
    E, L, ra = constants(rp, e)
    if e < 1e-12:
        u = 1.0 / rp
        T_r = 2 * np.pi * rp**2 / L
        tt = np.linspace(0.0, T_r, n_tau, endpoint=False)
        gamma = E / np.sqrt(1.0 - 2 * u)
        lam = np.full(n_tau, u**3 * (3 * gamma**2 - 1))
        return dict(tau=tt, lam=lam, T_r=T_r, dphi_r=2 * np.pi, E=E, L=L,
                    ra=rp, gamma_p=gamma, Om_r=2 * np.pi / T_r,
                    az_rate=2 * np.pi / T_r)

    up, ua = 1.0 / rp, 1.0 / ra
    roots = np.roots([2.0, -1.0, 2.0 / L**2, (E**2 - 1.0) / L**2])
    u3 = roots[(roots.real > up + 1e-12) & (np.abs(roots.imag) < 1e-9)].real[0]
    c, A = 0.5 * (up + ua), 0.5 * (up - ua)

    def rhs(psi, y):
        u = c + A * np.cos(psi)
        dphi = 1.0 / np.sqrt(2.0 * (u3 - u))
        return [dphi, dphi / (L * u**2)]

    sol = solve_ivp(rhs, (0.0, np.pi), [0.0, 0.0], rtol=1e-13, atol=1e-14,
                    dense_output=True, max_step=0.01)
    dphi_r = 2.0 * sol.y[0, -1]
    T_r = 2.0 * sol.y[1, -1]

    psi = np.linspace(0.0, np.pi, 8 * n_tau)[1:]
    yy = sol.sol(psi)
    tau_out, u_out = yy[1], c + A * np.cos(psi)
    g = np.linspace(0.0, T_r / 2, n_tau // 2 + 1)
    u_h = np.interp(g, tau_out, u_out)
    tt = np.linspace(0.0, T_r, n_tau, endpoint=False)
    u_full = np.where(tt <= T_r / 2, np.interp(tt, g, u_h),
                      np.interp(T_r - tt, g, u_h))
    gamma = E / np.sqrt(1.0 - 2.0 * u_full)
    lam = u_full**3 * (3.0 * gamma**2 - 1.0)
    return dict(tau=tt, lam=lam, T_r=T_r, dphi_r=dphi_r, E=E, L=L, ra=ra,
                gamma_p=E / np.sqrt(1 - 2 * up), Om_r=2 * np.pi / T_r,
                az_rate=dphi_r / T_r)


def floquet_truth(lam, T_r, Om_grid, alpha, sub=3):
    """RK4 monodromy, vectorized over Om; half-step lambda table precomputed."""
    n = len(lam)
    h = T_r / (n * sub)
    n_fine = 2 * n * sub
    fine = np.linspace(0.0, T_r, n, endpoint=False)
    grid = (np.arange(n_fine + 1) * (T_r / n_fine)) % T_r
    lam_seq = np.interp(grid, fine, lam)  # index i <-> time i*h/2
    Om2 = Om_grid**2

    def deriv(y, lam_t):
        w2 = Om2 - alpha * lam_t
        return np.stack((y[1], -w2 * y[0], y[3], -w2 * y[2]))

    y = np.zeros((4, len(Om_grid)))
    y[0] = 1.0  # basis 1: (x=1, v=0)
    y[3] = 1.0  # basis 2: (x=0, v=1)
    for k in range(n * sub):
        k1 = deriv(y, lam_seq[2 * k])
        k2 = deriv(y + h / 2 * k1, lam_seq[2 * k + 1])
        k3 = deriv(y + h / 2 * k2, lam_seq[2 * k + 1])
        k4 = deriv(y + h * k3, lam_seq[2 * k + 2])
        y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return y[0] + y[3]


def mu_from_tr(tr, T_r):
    tr = np.abs(np.real_if_close(np.asarray(tr, dtype=complex)).real)
    mu = np.zeros_like(tr, dtype=float)
    unst = tr > 2.0 + 1e-9
    mu[unst] = np.arccosh(np.clip(tr[unst] / 2.0, 1.0, 1e18)) / T_r
    return mu


def seg_map(w2, d):
    """Exact 2x2 map of x'' = -w2 x over duration d (vectorized over w2)."""
    w2 = np.asarray(w2, dtype=float)
    pos = w2 >= 0
    w = np.sqrt(np.abs(w2))
    c = np.where(pos, np.cos(w * d), np.cosh(w * d))
    s = np.where(pos, np.sin(w * d), np.sinh(w * d))
    return c, s / w, np.where(pos, -w * s, w * s), c


def floquet_hold(lam, T_r, Om_grid, alpha, K):
    """Piecewise-constant lambda at K uniform epochs; exact segment maps."""
    idx = np.arange(K) * len(lam) // K
    lams = lam[idx]
    d = T_r / K
    w2 = Om_grid[None, :]**2 - alpha * lams[:, None]
    a11, a12, a21, a22 = seg_map(w2, d)
    m11 = np.ones_like(a11[0]); m12 = np.zeros_like(a11[0])
    m21 = np.zeros_like(a11[0]); m22 = np.ones_like(a11[0])
    for k in range(K):
        n11 = m11 * a11[k] + m12 * a21[k]
        n12 = m11 * a12[k] + m12 * a22[k]
        n21 = m21 * a11[k] + m22 * a21[k]
        n22 = m21 * a12[k] + m22 * a22[k]
        m11, m12, m21, m22 = n11, n12, n21, n22
    return m11 + m22


def floquet_kick(lam, T_r, Om_grid, alpha, K):
    """Per epoch: tide as one velocity kick v += alpha*lam_k*x*d; between
    epochs the member drifts under its OWN binding Om_m exactly (the
    engine-faithful reading: kicks carry the tide, drift carries the rest)."""
    idx = np.arange(K) * len(lam) // K
    d = T_r / K
    b11, b12, b21, b22 = seg_map(np.asarray(Om_grid)**2, d)  # exact drift
    m11 = np.ones_like(Om_grid); m12 = np.zeros_like(Om_grid)
    m21 = np.zeros_like(Om_grid); m22 = np.ones_like(Om_grid)
    for k in range(K):
        lk = alpha * lam[idx[k]] * d
        n11, n12 = m11, m12
        n21, n22 = lk * m11 + m21, lk * m12 + m22   # kick
        m11 = b11 * n11 + b12 * n21                  # exact drift
        m12 = b11 * n12 + b12 * n22
        m21 = b21 * n11 + b22 * n21
        m22 = b21 * n12 + b22 * n22
    return m11 + m22


def fourier(lam, kmax=8):
    c = np.fft.rfft(lam - lam.mean()) / len(lam)
    return dict(mean=float(lam.mean()),
                amps={str(k): float(2 * np.abs(c[k])) for k in range(1, kmax + 1)})


def bands(Om_ratio, mu, thresh):
    """Contiguous regions with mu (per orbit) > thresh."""
    out = []
    m = np.asarray(mu) > thresh
    if not m.any():
        return out
    edges = np.diff(m.astype(int))
    starts = list(np.where(edges == 1)[0] + 1)
    ends = list(np.where(edges == -1)[0] + 1)
    if m[0]:
        starts = [0] + starts
    if m[-1]:
        ends = ends + [len(m)]
    for s, e in zip(starts, ends):
        out.append(dict(center=float(0.5 * (Om_ratio[s] + Om_ratio[e - 1])),
                        half_width=float(0.5 * (Om_ratio[e - 1] - Om_ratio[s])),
                        peak=float(np.max(np.asarray(mu)[s:e]))))
    return out


def run_case(rp, e, alpha, n_om=601, n_tau=12001, sub=3):
    o = orbit_lambda(rp, e, n_tau=n_tau)
    T_r, lam = o["T_r"], o["lam"]
    Om = np.geomspace(0.02, 16.0, n_om) * o["Om_r"]
    tr = np.asarray(floquet_truth(lam, T_r, Om, alpha, sub=sub))
    idx_chk = np.arange(0, n_om, 30)
    tr2 = np.asarray(floquet_truth(lam, T_r, Om[idx_chk], alpha, sub=2 * sub))
    dtr = float(np.max(np.abs(tr[idx_chk] - tr2)))
    lam_bar = float(lam.mean())
    w2 = Om**2 - alpha * lam_bar
    tr_avg = np.where(w2 >= 0, 2 * np.cos(np.sqrt(np.abs(w2)) * T_r),
                      2 * np.cosh(np.sqrt(np.abs(w2)) * T_r))
    laws = dict(avg=mu_from_tr(tr_avg, T_r),
                truth=mu_from_tr(tr, T_r))
    for K in (1, 4, 32):
        laws[f"hold{K}"] = mu_from_tr(floquet_hold(lam, T_r, Om, alpha, K), T_r)
    laws["kick32"] = mu_from_tr(floquet_kick(lam, T_r, Om, alpha, 32), T_r)
    Om_ratio = Om / o["Om_r"]
    mu_orbit = {k: (np.asarray(v) * T_r).tolist() for k, v in laws.items()}
    res = dict(rp=rp, e=e, alpha=alpha, gamma_p=o["gamma_p"], T_r=T_r,
               dphi_r=o["dphi_r"], Om_r=o["Om_r"],
               az_over_Om_r=o["az_rate"] / o["Om_r"], lam=fourier(lam),
               conv_max_dtr=dtr,
               static_edge=(float(np.sqrt(alpha * lam_bar)) / o["Om_r"]
                            if alpha * lam_bar > 0 else None))
    res["Om_over_Om_r"] = Om_ratio.tolist()
    res["laws"] = mu_orbit
    th = 0.02  # per-orbit growth
    res["bands"] = {k: bands(Om_ratio, v, th) for k, v in mu_orbit.items()}
    # predicted band centers from the tide's own moments (first-order Floquet)
    pred = []
    for k in range(1, 9):
        m2 = alpha * lam_bar + (k / 2.0) ** 2 * o["Om_r"] ** 2
        if 0 < m2:
            c = np.sqrt(m2) / o["Om_r"]
            if 0.02 <= c <= 16.0:
                pred.append(dict(k=k, center=float(c)))
    res["predicted_centers"] = pred
    return res


if __name__ == "__main__":
    cases = json.loads(sys.argv[1])
    out = []
    for c in cases:
        out.append(run_case(c["rp"], c["e"], c["alpha"]))
        r = out[-1]
        print(f"rp={r['rp']:>7} e={r['e']} a={r['alpha']:+d} "
              f"gamma_p={r['gamma_p']:.3f} dphi_r={r['dphi_r']:.4f} "
              f"conv={r['conv_max_dtr']:.1e} truth_bands={len(r['bands']['truth'])}",
              file=sys.stderr)
    tag = sys.argv[2] if len(sys.argv) > 2 else "out"
    with open(f"results-{tag}.json", "w") as f:
        json.dump(out, f)
