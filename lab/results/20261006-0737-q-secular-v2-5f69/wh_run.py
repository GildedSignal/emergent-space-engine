"""WH runner for run 20261006-0737-q-secular-v2-5f69 (second author, v2 of 008e).

Fixes vs run 008e (checker's findings):
  1. accel(): pass j now contributes to every row except row j itself (run 008e's
     `out[j] = 0.0` wiped row j's accumulation from the previous pass, so Saturn
     never received Jupiter's kick).
  2. planet_matrix(): outer planet's LL row carries single alpha (quadrupole limit),
     inner row keeps alpha^2 (unchanged, matches the classic (3/4) n mu alpha^3).
  3. Initial velocities use n = sqrt(mu/a^3) with mu = 1+m, so the initial state is
     exactly the intended osculating (a, e, varpi, M) of each body's drift problem.

Heliocentric Wisdom-Holman: Sun + 2 massive planets + 1024 test belt bodies.
Drift: exact per-body Kepler (Gauss f/g). Kick: direct + indirect from both planets
(planets also kick each other). Same code for truth (small h), convergence run and
the plane's 64-kick law (h = P(2AU)/64) -- only h differs.

Outputs (each < 5 MB): reduced statistics at 384 stored times:
  <prefix>_meta.json, <prefix>_zbar.npz (synodic running mean of z, complex64),
  <prefix>_z.npz (raw osculating z), <prefix>_a.npz (osculating a, every 4th time),
  <prefix>_zp.npz (planets' z).
The synodic running mean is computed online: fine z samples every ~1 time unit are
kept in a rolling window, and each stored time evaluates per-body boxcar
windows w_i = round(syn_J(a_i)/dt_fine) via prefix sums.
"""
import json
import math
import sys
import time

import numpy as np

MU_J, A_J, E_J = 9.54e-4, 5.2026, 0.0484
MU_S, A_S, E_S = 2.858e-4, 9.5370, 0.0539
VARPI_J, VARPI_S = 0.8, 2.1
NB = 1024
NSTOR = 384
SEED = 20261005

def laplace_b(s, j, alpha):
    from scipy.integrate import quad
    f = lambda p: math.cos(j * p) / (1 - 2 * alpha * math.cos(p) + alpha * alpha) ** s
    return quad(f, 0, 2 * math.pi, epsabs=1e-14, limit=200)[0] / math.pi

def planet_matrix():
    n = [A_J ** -1.5, A_S ** -1.5]
    M = np.zeros((2, 2))
    alphas = [A_J / A_S, A_J / A_S]
    pairs = [(0, 1), (1, 0)]
    for i, j in pairs:
        alpha = alphas[0]
        m_j = MU_S if j == 1 else MU_J
        # LL row of body i perturbed by planet j. Quadrupole limit (doubly averaged
        # l=2 term, Lagrange eqs divide by n_i a_i^2): inner body's rates carry
        # alpha^2 b ~ 3 alpha^3, outer body's carry alpha b ~ 3 alpha^2. Row 0 is
        # inner (J), row 1 outer (S): only row 1's power changes vs run 008e.
        row_alpha = alpha ** 2 if i == 0 else alpha
        pref = n[i] * m_j / 4 * row_alpha
        M[i, i] += pref * laplace_b(1.5, 1, alpha)
        M[i, j] = -pref * laplace_b(1.5, 2, alpha)
    return M

def modes():
    M = planet_matrix()
    g, V = np.linalg.eig(M)
    assert np.allclose(g.imag, 0, atol=1e-12)
    g = g.real
    o = np.argsort(g)
    return g[o], V[:, o], np.linalg.inv(V[:, o])

def init_belt():
    g, V, Vinv = modes()
    zpl0 = np.array([E_J * np.exp(1j * VARPI_J), E_S * np.exp(1j * VARPI_S)])
    c = Vinv @ zpl0
    rng = np.random.default_rng(SEED)
    a = rng.uniform(2.0, 3.3, NB)
    e_free = rng.uniform(0.02, 0.23, NB)
    beta = rng.uniform(0, 2 * np.pi, NB)
    M0 = rng.uniform(0, 2 * np.pi, NB)
    n = a ** -1.5
    A = np.zeros(NB)
    for mup, ap in [(MU_J, A_J), (MU_S, A_S)]:
        alpha = a / ap
        b1 = np.array([laplace_b(1.5, 1, al) for al in alpha])
        A += n * mup / 4 * alpha * alpha * b1
    zf = np.zeros(NB, complex)
    for k in range(2):
        BPk = np.zeros(NB)
        for P, (mup, ap) in enumerate([(MU_J, A_J), (MU_S, A_S)]):
            alpha = a / ap
            b2 = np.array([laplace_b(1.5, 2, al) for al in alpha])
            BPk += -n * mup / 4 * alpha * alpha * b2 * V[P, k]
        zf += BPk * c[k] / (A - g[k])
    # redraw beta while |z0| > 0.25
    z0 = zf + e_free * np.exp(1j * beta)
    bad = np.abs(z0) > 0.25
    nbad = bad.sum()
    while nbad:
        beta[bad] = rng.uniform(0, 2 * np.pi, nbad)
        z0 = zf + e_free * np.exp(1j * beta)
        bad = np.abs(z0) > 0.25
        nbad = bad.sum()
    return a, e_free, beta, M0, zf, A, z0

def elements(r, v):
    rn = np.linalg.norm(r, axis=1)
    hz = r[:, 0] * v[:, 1] - r[:, 1] * v[:, 0]
    ex = v[:, 1] * hz - r[:, 0] / rn
    ey = -v[:, 0] * hz - r[:, 1] / rn
    a = 1 / (2 / rn - (v * v).sum(1))
    return ex + 1j * ey, a

def run(h, prefix, nsteps):
    t_wall = time.time()
    a, e_free, beta, M0, zf, A, z0 = init_belt()
    N = NB + 2
    m = np.zeros(N); m[0], m[1] = MU_J, MU_S
    # state
    ae = np.empty(N); ee = np.empty(N); we = np.empty(N); Me = np.empty(N)
    ae[0], ae[1] = A_J, A_S
    ee[0], ee[1] = E_J, E_S
    we[0], we[1] = VARPI_J, VARPI_S
    Me[0], Me[1] = 0.0, 0.0
    ae[2:], ee[2:], we[2:], Me[2:] = a, np.abs(z0), np.angle(z0), M0
    mu = 1.0 + m
    # Cartesian from (a, e, varpi, M)
    E = Me.copy()
    for _ in range(8):
        E = E - (E - ee * np.sin(E) - Me) / (1 - ee * np.cos(E))
    cE, sE = np.cos(E), np.sin(E)
    x, y = ae * (cE - ee), ae * np.sqrt(1 - ee * ee) * sE
    cf, sf = np.cos(we), np.sin(we)
    r = np.stack([cf * x - sf * y, sf * x + cf * y], 1)
    n_kep = np.sqrt(mu / ae ** 3)   # mu-consistent: initial state IS the osculating (a,e,varpi,M)
    Edot = n_kep / (1 - ee * cE)
    vx_p, vy_p = -ae * sE * Edot, ae * np.sqrt(1 - ee * ee) * cE * Edot
    v = np.stack([cf * vx_p - sf * vy_p, sf * vx_p + cf * vy_p], 1)

    def kepler_drift(r, v, h):
        rn = np.linalg.norm(r, axis=1)
        v2 = (v * v).sum(1)
        aa = 1 / (2 / rn - v2 / mu)
        nn = np.sqrt(mu / aa ** 3)
        sig = (r * v).sum(1) / np.sqrt(mu * aa)
        ec, es = 1 - rn / aa, sig
        dM = nn * h
        x = dM.copy()
        for _ in range(3):
            s, c = np.sin(x), np.cos(x)
            x -= (x - ec * s + es * (1 - c) - dM) / (1 - ec * c + es * s)
        s, c = np.sin(x), np.cos(x)
        f = aa / rn * (c - 1) + 1
        g = h + (s - x) / nn
        r2 = f[:, None] * r + g[:, None] * v
        r2n = np.linalg.norm(r2, axis=1)
        fd = -aa * aa * nn * s / (r2n * rn)
        gd = aa / r2n * (c - 1) + 1
        return r2, fd[:, None] * r + gd[:, None] * v

    def accel(r):
        # Heliocentric perturbation: pass j adds planet j's direct+indirect term to
        # every row EXCEPT row j itself. Run 008e had `out[j] = 0.0` after the +=,
        # which wiped row j's accumulation from the previous pass (Saturn never kicked).
        out = np.zeros_like(r)
        for j in (0, 1):
            d = r[j] - r
            dn = np.linalg.norm(d, axis=1)
            dn[j] = np.inf
            rjn = np.linalg.norm(r[j])
            contrib = m[j] * (d / dn[:, None] ** 3 - r[j] / rjn ** 3)
            contrib[j] = 0.0
            out += contrib
        return out

    # storage grid and rolling fine-sampling machinery
    T = nsteps * h
    stor_times = np.linspace(0, T, NSTOR + 1)[1:]
    stor_idx = 0
    fine_every = max(1, int(round(1.0 / h)))
    dt_fine = fine_every * h
    WMAX = int(math.ceil(80.0 / dt_fine)) + 2
    nJ = math.sqrt((1 + MU_J) / A_J ** 3)
    w_body = np.clip(np.round(2 * math.pi / np.abs(a ** -1.5 - nJ) / dt_fine), 4, WMAX - 2).astype(int)
    buf = np.zeros((WMAX, NB), np.complex64)
    buf_n = 0
    csum = np.zeros((WMAX + 1, NB), np.complex128)
    zbar_stor = np.zeros((NSTOR, NB), np.complex64)
    z_stor = np.zeros((NSTOR, NB), np.complex64)
    zp_stor = np.zeros((NSTOR, 2), np.complex64)
    a_stor = np.zeros((NSTOR // 4 + 1, NB), np.float32)
    a_stor[0] = a
    fine_count = 0
    t = 0.0
    next_fine = 0.0
    for step in range(nsteps):
        r, v = kepler_drift(r, v, h / 2)
        v = v + h * accel(r)
        r, v = kepler_drift(r, v, h / 2)
        t += h
        if step % fine_every == 0:
            z_b, _ = elements(r[2:], v[2:])
            buf[1:] = buf[:-1]
            buf[0] = z_b
            buf_n += 1
            fine_count += 1
        if stor_idx < NSTOR and t >= stor_times[stor_idx] - h / 2:
            z_b, a_b = elements(r[2:], v[2:])
            z_stor[stor_idx] = z_b
            zp_stor[stor_idx] = elements(r[:2], v[:2])[0]
            if (stor_idx + 1) % 4 == 0:
                a_stor[(stor_idx + 1) // 4] = a_b
            # boxcar over per-body synodic windows from the rolling buffer
            end = min(buf_n, WMAX)
            np.cumsum(buf[:end].astype(np.complex128), axis=0, out=csum[1:end + 1])
            starts = np.clip(end - w_body, 0, end)
            cols = np.arange(NB)
            zbar_stor[stor_idx] = ((csum[end, cols] - csum[starts, cols]) / np.maximum(end - starts, 1)).astype(np.complex64)
            stor_idx += 1
    assert stor_idx == NSTOR, (stor_idx, NSTOR)
    np.savez_compressed(prefix + "_zbar.npz", z=zbar_stor, t=stor_times)
    np.savez_compressed(prefix + "_z.npz", z=z_stor)
    np.savez_compressed(prefix + "_zp.npz", z=zp_stor)
    np.savez_compressed(prefix + "_a.npz", a=a_stor)
    meta = dict(h=h, nsteps=nsteps, T=T, dt_fine=dt_fine, w_body_median=int(np.median(w_body)),
                fine_count=fine_count, elapsed=time.time() - t_wall,
                a=a.tolist(), e_free=e_free.tolist(), beta=beta.tolist(), M0=M0.tolist(),
                zf_re=zf.real.tolist(), zf_im=zf.imag.tolist(), A=A.tolist())
    with open(prefix + "_meta.json", "w") as f:
        json.dump(meta, f)
    print(f"{prefix}: h={h} nsteps={nsteps} T={T:.0f} elapsed={time.time()-t_wall:.0f}s "
          f"fine={fine_count} w_med={int(np.median(w_body))}", flush=True)

if __name__ == "__main__":
    which = sys.argv[1]
    if which == "truth":
        run(0.125, "truth", 1192179)
    elif which == "conv":
        run(0.1875, "conv", 794786)
    elif which == "kick":
        h = 2 * math.pi * 2.0 ** 1.5 / 64
        run(h, "kick", int(149022.4 / h))
