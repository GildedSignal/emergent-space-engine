"""P2: can a stable belt body be a sum of uniformly rotating phasors (zero kicks) instead of 64 kicks per orbit?

Representation: z = e*exp(i*varpi) (the Binet cone's (V, W) up to the factor 1/p). Laplace-Lagrange (first order in
mass, second order in e) makes dz/dt = i(A z + B z_J): every body's eccentricity vector is a forced phasor plus a
free phasor rotating at A. With exact Laplace coefficients (quadrature, no expansion in alpha).

Scene: Sun + Jupiter on a fixed ellipse (a=5.2026, e=0.0484, mu=9.54e-4), test particles in the main belt.
Truth: Wisdom-Holman (heliocentric, direct + indirect kick, which is a gradient for a test particle) at two steps,
to show convergence. Compared: the synodic-period running mean of the osculating z against the phasor's z(t).
Controls that must fail: particles at the 3:1 (2.50 AU) and 5:2 (2.82 AU) mean-motion resonances.
Reported: the eccentricity-vector error relative to the free amplitude, the precession-rate error, and the
mean-longitude drift a naive osculating n would carry (the phasor law's phase error type).
"""
import math, time
import numpy as np
from scipy.integrate import quad

MU_J, A_J, E_J = 9.54e-4, 5.2026, 0.0484

def laplace_b(s, j, alpha):
    f = lambda p: math.cos(j * p) / (1 - 2 * alpha * math.cos(p) + alpha * alpha) ** s
    return quad(f, 0, 2 * math.pi, epsabs=1e-14, limit=200)[0] / math.pi

def kepler_drift(r, v, mu, h):
    """Vectorized elliptic Kepler drift by Gauss's f and g functions (bound orbits only)."""
    rn = np.linalg.norm(r, axis=1)
    v2 = (v * v).sum(1)
    a = 1 / (2 / rn - v2 / mu)
    n = np.sqrt(mu / a ** 3)
    sig = (r * v).sum(1) / np.sqrt(mu * a)
    ec, es = 1 - rn / a, sig  # e cos E0, e sin E0
    dM = n * h
    x = dM.copy()  # solve dE - ec sin dE + es (1 - cos dE) = dM
    for _ in range(5):
        s, c = np.sin(x), np.cos(x)
        f = x - ec * s + es * (1 - c) - dM
        x -= f / (1 - ec * c + es * s)
    s, c = np.sin(x), np.cos(x)
    f = a / rn * (c - 1) + 1
    g = h + (s - x) / n
    r2 = f[:, None] * r + g[:, None] * v
    r2n = np.linalg.norm(r2, axis=1)
    fd = -a * a * n * s / (r2n * rn)
    gd = a / r2n * (c - 1) + 1
    return r2, fd[:, None] * r + gd[:, None] * v

def jupiter(t):
    nJ = math.sqrt((1 + MU_J) / A_J ** 3)
    M = nJ * t
    E = M
    for _ in range(20):
        E -= (E - E_J * math.sin(E) - M) / (1 - E_J * math.cos(E))
    return np.array([A_J * (math.cos(E) - E_J), A_J * math.sqrt(1 - E_J ** 2) * math.sin(E)])

def accel(r, rj):
    d = rj[None, :] - r
    dn = np.linalg.norm(d, axis=1)
    return MU_J * (d / dn[:, None] ** 3 - rj[None, :] / np.linalg.norm(rj) ** 3)

def elements(r, v):
    rn = np.linalg.norm(r, axis=1)
    hz = r[:, 0] * v[:, 1] - r[:, 1] * v[:, 0]
    ex = v[:, 1] * hz - r[:, 0] / rn
    ey = -v[:, 0] * hz - r[:, 1] / rn
    a = 1 / (2 / rn - (v * v).sum(1))
    # mean longitude
    e = np.hypot(ex, ey)
    w = np.arctan2(ey, ex)
    nu = np.arctan2(r[:, 1], r[:, 0]) - w
    E = 2 * np.arctan(np.sqrt((1 - e) / (1 + e)) * np.tan(nu / 2))
    lam = w + E - e * np.sin(E)
    return ex + 1j * ey, a, lam

def run(a0, e0, w0, T, h):
    N = len(a0)
    r = np.zeros((N, 2)); v = np.zeros((N, 2))
    for i in range(N):  # start at periapsis
        rp = a0[i] * (1 - e0[i]); vp = math.sqrt((1 + e0[i]) / rp)
        r[i] = rp * np.array([math.cos(w0[i]), math.sin(w0[i])])
        v[i] = vp * np.array([-math.sin(w0[i]), math.cos(w0[i])])
    steps = int(T / h)
    every = max(1, steps // 4000)
    ts, zs, lams, as_ = [], [], [], []
    t = 0.0
    for s in range(steps):
        r, v = kepler_drift(r, v, 1.0, h / 2)
        v = v + h * accel(r, jupiter(t + h / 2))
        r, v = kepler_drift(r, v, 1.0, h / 2)
        t += h
        if s % every == 0:
            z, a, lam = elements(r, v)
            ts.append(t); zs.append(z); lams.append(lam); as_.append(a)
    return np.array(ts), np.array(zs), np.unwrap(np.array(lams), axis=0), np.array(as_)

def main():
    t0 = time.time()
    rng = np.random.default_rng(7)
    a_list = [2.20, 2.35, 2.62, 2.70, 3.05, 3.15, 2.502, 2.825]  # last two: 3:1 and 5:2 (controls)
    e_list = [0.02, 0.10, 0.20]
    a0 = np.array([a for a in a_list for _ in e_list])
    e0 = np.array([e for _ in a_list for e in e_list])
    w0 = rng.uniform(0, 2 * math.pi, len(a0))
    T = 12000.0
    res = {}
    for h in (0.25, 0.125):
        res[h] = run(a0, e0, w0, T, h)
    ts, zs, lams, as_ = res[0.125]
    zs_c = res[0.25][1]
    nJ = math.sqrt((1 + MU_J) / A_J ** 3)
    zJ = E_J
    print(f"(truth convergence) max |z(h=0.25) - z(h=0.125)| = {np.abs(zs_c - zs).max():.2e}")
    print(" a      e0    A_pred      A_meas     relerr  |  e-vector err / free amp (median, max)  |  forced e   |  naive phase drift (rad) over T  |  max phase error with n fitted over 3 synodic periods (rad)")
    for i in range(len(a0)):
        a = a0[i]; al = a / A_J; n = a ** -1.5
        b1, b2 = laplace_b(1.5, 1, al), laplace_b(1.5, 2, al)
        A = n * 0.25 * MU_J * al * al * b1
        B = -n * 0.25 * MU_J * al * al * b2
        zf = -B * zJ / A
        # synodic running mean of the osculating z
        syn = 2 * math.pi / abs(n - nJ)
        dt = ts[1] - ts[0]
        w = max(1, int(round(syn / dt)))
        k = np.ones(w) / w
        zbar = np.convolve(zs[:, i], k, mode="valid")
        tbar = np.convolve(ts, k, mode="valid")
        z0bar = zbar[0]
        # phasor law started from the first mean value
        zsec = zf + (z0bar - zf) * np.exp(1j * A * (tbar - tbar[0]))
        amp = abs(z0bar - zf)
        err = np.abs(zbar - zsec) / max(amp, 1e-12)
        ang = np.unwrap(np.angle(zbar - zf))
        A_meas = np.polyfit(tbar, ang, 1)[0]
        # naive phase: osculating n at t=0 against the run's mean longitude slope
        n_osc = as_[0, i] ** -1.5
        n_meas = np.polyfit(ts, lams[:, i], 1)[0]
        m3 = min(len(ts), 3 * w)
        n_fit = np.polyfit(ts[:m3], lams[:m3, i], 1)[0]
        resid = lams[:, i] - (lams[0, i] + n_fit * (ts - ts[0]))
        fit_drift = np.abs(resid).max()
        tag = " (3:1)" if abs(a - 2.502) < 1e-6 else (" (5:2)" if abs(a - 2.825) < 1e-6 else "")
        print(f" {a:<5.3f} {e0[i]:<5.2f} {A:10.3e} {A_meas:10.3e} {abs(A_meas / A - 1):8.3f}  |  {np.median(err):8.3f} {err.max():8.3f}"
              f"  |  {abs(zf):.4f}  |  {(n_meas - n_osc) * T:9.3f}  |  {fit_drift:7.3f}{tag}")
    print(f"elapsed {time.time() - t0:.1f} s; T = {T} (= {T / (2 * math.pi):.0f} yr, {T * nJ / (2 * math.pi):.0f} Jupiter orbits)")

main()
