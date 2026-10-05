#!/usr/bin/env python3
"""Independent arbiter: geodesics of the covariant 1PN metric via analytic
Christoffel symbols (second-order form), vs the Hamiltonian flow in probe_mks.
Metric (covariant, diagonal, static):  g_tt = -(1-2U+2U^2),  g_ij = (1+2U) delta_ij.
"""
import numpy as np
from scipy.integrate import solve_ivp

M = 0.04

def dU(x, y):
    r = np.hypot(x, y)
    return np.array([-M * x / r**3, -M * y / r**3])

def rhs(lam, w):
    t, x, y, wt, wx, wy = w
    r = np.hypot(x, y)
    U = M / r
    gtt = -(1 - 2 * U + 2 * U * U)
    f = 1 + 2 * U                      # g_ij factor
    dgtt = (2 - 4 * U) * dU(x, y)      # d_i g_tt
    df = 2 * dU(x, y)
    # Gamma^i_tt = -1/2 g^ii d_i g_tt
    Gi_tt = -0.5 / f * dgtt
    # Gamma^t_ti = 1/2 g^tt d_i g_tt ; g^tt = 1/g_tt
    Gt_t = 0.5 / gtt * dgtt
    # Gamma^i_jk = 1/2 f^-1 (d_j f delta_ki + d_k f delta_ji - d_i f delta_jk)
    v = np.array([wx, wy])
    acc = np.empty(3)
    acc[0] = -2 * (Gt_t[0] * wt * wx + Gt_t[1] * wt * wy)
    ax = np.zeros(2)
    for i in range(2):
        for j in range(2):
            for k in range(2):
                G = 0.5 / f * ((df[j] if k == i else 0.0) + (df[k] if j == i else 0.0)
                               - (df[i] if j == k else 0.0))
                ax[i] -= G * v[j] * v[k]
    ax -= Gi_tt * wt * wt
    return [wt, wx, wy, acc[0], ax[0], ax[1]]

rp = 18.181818181818182
a_orb = 20.0 / 0.99
v = np.sqrt(M * (2 / rp - 1 / a_orb))
w = np.array([1.0, 0.0, v])
def gfull(x, y):
    r = np.hypot(x, y); U = M / r
    g = np.eye(3); g[0, 0] = -(1 - 2 * U + 2 * U * U); g[1, 1] = g[2, 2] = 1 + 2 * U
    return g
g0 = gfull(rp, 0.0)
s = np.sqrt(1.0 / (-g0 @ w @ w))
w = w * s
T = 8 * 2 * np.pi * np.sqrt(a_orb**3 / M)
sol = solve_ivp(rhs, (0, T), [0, rp, 0, *w], rtol=1e-12, atol=1e-14, method='DOP853',
                t_eval=np.linspace(0, T, 20000))
r = np.hypot(sol.y[1], sol.y[2]); phi = np.unwrap(np.arctan2(sol.y[2], sol.y[1]))
idx = [i for i in range(1, len(r) - 1) if r[i] < r[i - 1] and r[i] < r[i + 1]]
phis = [phi[i] for i in idx]
adv = np.median(np.diff(phis)) - 2 * np.pi
p_act = 2 * r.min() * r.max() / (r.min() + r.max())
print("christoffel flow: nmin", len(idx), "adv", adv, "p_act", p_act)
print("6piM/p_act =", 6 * np.pi * M / p_act, " rel:", adv / (6 * np.pi * M / p_act) - 1)
