"""Laws for run 20261005-2231-q-secular-008e: first-order Laplace-Lagrange and exact
double averaging (Gauss rings). Belt test particles driven by the planets' mutual LL
modes. Units and conventions identical to wh_run.py.

Sign convention (validated pre-run against quadrature coefficients and WH truth):
  dedt     = -sqrt(1-e^2)/(e sqrt(a)) d<R>/dvarpi
  dvarpidt = +sqrt(1-e^2)/(e sqrt(a)) d<R>/de
which reproduces zdot = i(A z + B z_P) with A = 2 c2/sqrt(a) prograde and B = B_R/sqrt(a).
"""
import json
import math

import numpy as np

from wh_run import (MU_J, A_J, E_J, MU_S, A_S, E_S, VARPI_J, VARPI_S, NB, SEED,
                    init_belt, modes)

NSTOR = 384

def planet_z(t, g, V, c):
    """z_P(t) from the two modes."""
    e = np.exp(1j * np.outer(t, g))          # (nt, 2)
    coef = V * c[None, :]                    # (2 planets, 2 modes) broadcast -> (2,2)
    # z_P(t) = sum_k V[P,k] c_k e^{i g_k t}
    return np.einsum('pk,tk->tp', (V * c), e)

def kepler_grid(a, e, varpi, NG):
    """Positions on a midpoint grid in M. a: (N,), e: (N,), varpi: (N,). -> (N, NG, 2)."""
    M = 2 * math.pi * (np.arange(NG) + 0.5) / NG
    E = np.broadcast_to(M, (len(a), NG)).copy()
    eN = np.broadcast_to(e[:, None], E.shape)
    for _ in range(8):
        E = E - (E - eN * np.sin(E) - np.broadcast_to(M, E.shape)) / (1 - eN * np.cos(E))
    cE, sE = np.cos(E), np.sin(E)
    x, y = a[:, None] * (cE - eN), a[:, None] * np.sqrt(1 - eN ** 2) * sE
    cf, sf = np.cos(varpi)[:, None], np.sin(varpi)[:, None]
    return np.stack([cf * x - sf * y, sf * x + cf * y], axis=-1)

def R_avg(rb, a_P, e_P, varpi_P, mu_P, NGP=10):
    """Double-averaged disturbing function per unit mass of one body pair.
    rb: (N, NG, 2) body grid; returns (N,)."""
    rp = kepler_grid(np.array([a_P]), np.array([e_P]), np.array([varpi_P]), NGP)[0]  # (NGP, 2)
    d = rb[:, :, None, :] - rp[None, None, :, :]
    direct = (1.0 / np.linalg.norm(d, axis=-1)).mean(axis=(1, 2))
    rbar = rb.mean(axis=1)                                    # (N, 2)
    rp3 = rp / np.linalg.norm(rp, axis=1)[:, None] ** 3
    indirect = rbar @ rp3.mean(axis=0)
    return mu_P * (direct - indirect)

NG_BODY, NGP = 24, 16
DE, DW = 1e-4, 1e-4

def rings_rhs(t, z, a, g, V, c):
    """dz/dt for the belt under exact double averaging, planets on LL ellipses."""
    e = np.maximum(np.abs(z), 1e-4)
    w = np.angle(z)
    sq = np.sqrt(np.maximum(1 - e * e, 1e-8))
    pref = sq / (e * np.sqrt(a))
    zP = planet_z(np.array([t]), g, V, c)[0]                  # (2,)
    # R at (e, w), (e+-de, w), (e, w+-dw): stack variants
    evar = np.stack([e, e + DE, e - DE, e, e], axis=0)        # (5, N)
    wvar = np.stack([w, w, w, w + DW, w - DW], axis=0)
    dRde = np.zeros(NB)
    dRdw = np.zeros(NB)
    for P in range(2):
        e_P, varpi_P = np.abs(zP[P]), np.angle(zP[P])
        mu_P, a_P = (MU_J, A_J) if P == 0 else (MU_S, A_S)
        # body grids for all 5 variants at once
        M = 2 * math.pi * (np.arange(NG_BODY) + 0.5) / NG_BODY
        E = np.broadcast_to(M, (5, NB, NG_BODY)).copy()
        eN = evar[:, :, None]
        for _ in range(8):
            E = E - (E - eN * np.sin(E) - M[None, None, :]) / (1 - eN * np.cos(E))
        cE, sE = np.cos(E), np.sin(E)
        x, y = a[None, :, None] * (cE - eN), a[None, :, None] * np.sqrt(1 - eN ** 2) * sE
        cf, sf = np.cos(wvar)[:, :, None], np.sin(wvar)[:, :, None]
        rb = np.stack([cf * x - sf * y, sf * x + cf * y], axis=-1)   # (5, N, NG, 2)
        rp = kepler_grid(np.array([a_P]), np.array([e_P]), np.array([varpi_P]), NGP)[0]
        d = rb[:, :, None, :, None, :] - rp[None, None, None, None, :, :]
        direct = (1.0 / np.linalg.norm(d, axis=-1)).mean(axis=(-1, -2, -3))  # (5, N)
        rbar = rb.mean(axis=2)
        rp3 = (rp / np.linalg.norm(rp, axis=1)[:, None] ** 3).mean(axis=0)
        indirect = rbar @ rp3
        R = mu_P * (direct - indirect)
        dRde += (R[1] - R[2]) / (2 * DE)
        dRdw += (R[3] - R[4]) / (2 * DW)
    dedt = -pref * dRdw
    dwdt = pref * dRde
    return (dedt + 1j * e * dwdt) * np.exp(1j * w)

def run_rings(driver="ll"):
    a, e_free, beta, M0, zf, A, z0 = init_belt()
    g, V, Vinv = modes()
    zpl0 = np.array([E_J * np.exp(1j * VARPI_J), E_S * np.exp(1j * VARPI_S)])
    c = Vinv @ zpl0
    zdrv_t = zdrv_ts = None
    if driver == "truth":
        d = np.load("truth_zbar.npz"); zdrv_ts = d["t"]; zdrv_t = d2 = np.load("truth_zp.npz")["z"].astype(complex)
        # planets: boxcar over one synodic is not needed; osculating z fine (smooth), decimate to stored times already
    T = 149022.4
    nsub = NSTOR
    dt = T / nsub
    z = z0.copy()
    out = np.zeros((NSTOR, NB), np.complex64)
    import time
    t0 = time.time()
    import scipy.interpolate as si
    if driver == "truth":
        itp = [(lambda P: (lambda tt: si.interp1d(zdrv_ts, zdrv_t[:, P].real, kind="cubic", fill_value="extrapolate")(tt) + 1j * si.interp1d(zdrv_ts, zdrv_t[:, P].imag, kind="cubic", fill_value="extrapolate")(tt)))(P) for P in range(2)]
        import sys
        _self = sys.modules["__main__"]
        _orig = _self.planet_z
        def _pz(tarr, g_, V_, c_):
            return np.array([[f(tarr[k]) for k in range(len(tarr))] for f in itp])
        _self.planet_z = _pz
    for s in range(nsub):
        t = s * dt
        k1 = rings_rhs(t, z, a, g, V, c)
        k2 = rings_rhs(t + dt / 2, z + dt / 2 * k1, a, g, V, c)
        k3 = rings_rhs(t + dt / 2, z + dt / 2 * k2, a, g, V, c)
        k4 = rings_rhs(t + dt, z + dt * k3, a, g, V, c)
        z = z + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        out[s] = z
        if s % 96 == 0:
            print(f"rings step {s}/{nsub} elapsed {time.time()-t0:.0f}s", flush=True)
    np.savez_compressed("rings_z.npz" if driver == "ll" else "rings_truec_z.npz", z=out)
    print(f"rings done in {time.time()-t0:.0f}s")

def run_ll():
    a, e_free, beta, M0, zf, A, z0 = init_belt()
    g, V, Vinv = modes()
    zpl0 = np.array([E_J * np.exp(1j * VARPI_J), E_S * np.exp(1j * VARPI_S)])
    c = Vinv @ zpl0
    T = 149022.4
    ts = np.linspace(0, T, NSTOR + 1)[1:]
    zP_t = planet_z(ts, g, V, c)                              # (nstor, 2)
    # forced term of the belt body at each t: sum_k BP_k(zP-mode) e^{i g_k t}/(A - g_k)
    from wh_run import laplace_b
    n = a ** -1.5
    BPk = np.zeros((2, NB))
    for P, (mup, ap) in enumerate([(MU_J, A_J), (MU_S, A_S)]):
        alpha = a / ap
        b2 = np.array([laplace_b(1.5, 2, al) for al in alpha])
        for k in range(2):
            BPk[k] += -n * mup / 4 * alpha * alpha * b2 * V[P, k]
    zf_t = np.zeros((NSTOR, NB), complex)
    for k in range(2):
        zf_t += np.outer(np.exp(1j * g[k] * ts), BPk[k] * c[k] / (A - g[k]))
    out = zf_t + (z0 - zf_t[0]) * np.exp(1j * np.outer(ts, A))
    np.savez_compressed("ll_z.npz", z=out.astype(np.complex64), ts=ts)
    print("ll done")

if __name__ == "__main__":
    import sys
    if sys.argv[1] == "rings":
        run_rings("ll")
    elif sys.argv[1] == "rings_tc":
        run_rings("truth")
    else:
        run_ll()
