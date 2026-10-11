#!/usr/bin/env python3
"""Instrument checks for shapiro_gather.py's oracle.

1. flat closed forms at the SAME b (branch-aware): T = sqrt(ro^2-b^2)+sqrt(re^2-b^2),
   dphi_out = arcsin(b ue) - arcsin(b uo), dphi_in = arccos(b ue)+arccos(b uo).
2. curved: independent RK4 integration of the Binet ODE u'' = 3u^2 - u with
   dt/dphi = 1/(b u^2 (1-2u)) vs the quadrature's dphi, T.
3. textbook anchor where it is valid: grazing ray, both ends at r=1000,
   periapsis b=20 -> delay ~ 2M ln(4 ro re / b^2) + O(M/r).
"""
import math
import sys
sys.path.insert(0, ".")
from shapiro_gather import (simpson, path_phi_T, solve_b, turning_u1,
                            branch_int, g_curved, R_O, U_O)


def flat_closed(b, u_e, inbound):
    re = 1.0 / u_e
    if inbound:
        T = math.sqrt(R_O * R_O - b * b) + math.sqrt(re * re - b * b)
        phi = math.acos(b * u_e) + math.acos(b * U_O)
    else:
        T = math.sqrt(R_O * R_O - b * b) - math.sqrt(re * re - b * b)
        phi = math.asin(b * u_e) - math.asin(b * U_O)
    return phi, T


print("== flat closed-form check (same b) ==")
for re, frac in [(8.0, 0.93), (8.0, 0.5), (20.0, 0.68)]:
    u_e = 1.0 / re
    b = frac * (1.0 / u_e)  # inside tangential
    for inbound in (False, True):
        p_i, T_i = path_phi_T(b, u_e, inbound, curved=False, n=3000)
        p_c, T_c = flat_closed(b, u_e, inbound)
        print("re=%5.1f b=%7.4f in=%d  dphi: int %.9f closed %.9f rel %.2e | "
              "T: int %.6f closed %.6f rel %.2e"
              % (re, b, inbound, p_i, p_c, abs(p_i - p_c) / p_c,
                 T_i, T_c, abs(T_i - T_c) / T_c))


def rk4_photon(b, u_e, inbound, nsteps=4_000_000, dphi=2e-5):
    """integrate u'' = 3u^2 - u from emission to r_o; returns (dphi, T)."""
    u = u_e
    up = math.sqrt(g_curved(b, u_e)) * (1.0 if inbound else -1.0)
    phi = 0.0
    t = 0.0

    def f(u, up):
        return up, 3.0 * u * u - u

    # substeps in phi; stop when u <= u_o (arrived) on the outbound leg
    h = dphi
    while phi < 30.0:
        k1u, k1p = f(u, up)
        k2u, k2p = f(u + 0.5 * h * k1u, up + 0.5 * h * k1p)
        k3u, k3p = f(u + 0.5 * h * k2u, up + 0.5 * h * k2p)
        k4u, k4p = f(u + h * k3u, up + h * k3p)
        u_new = u + h / 6.0 * (k1u + 2 * k2u + 2 * k3u + k4u)
        up_new = up + h / 6.0 * (k1p + 2 * k2p + 2 * k3p + k4p)
        lap = 1.0 - 2.0 * u
        t += h / (b * u * u * lap)
        phi += h
        u, up = u_new, up_new
        if u <= U_O:
            break
    return phi, t


print("== curved: RK4 Binet ODE vs quadrature (same b) ==")
for re, b, inbound in [(8.0, 7.3, False), (8.0, 6.0, True), (20.0, 19.0, False),
                       (50.0, 10.0, False), (6.0, 5.4, True)]:
    u_e = 1.0 / re
    p_q, T_q = path_phi_T(b, u_e, inbound, curved=True, n=8000)
    p_r, T_r = rk4_photon(b, u_e, inbound)
    print("re=%5.1f b=%7.4f in=%d  dphi: quad %.8f rk4 %.8f rel %.2e | "
          "T: quad %.6f rk4 %.6f rel %.2e"
          % (re, b, inbound, p_q, p_r, abs(p_q - p_r) / p_r,
             T_q, T_r, abs(T_q - T_r) / T_r))

print("== exact radial anchor (b->0 limit, exact closed form) ==")
for r_e in (6.0, 20.0, 50.0):
    u_e = 1.0 / r_e
    T_q = branch_int(1e-4, U_O, u_e, 0.0, True, True, 20000)
    T_exact = (R_O - r_e) + 2.0 * math.log((R_O - 2.0) / (r_e - 2.0))
    print("r_e=%5.1f  T quad %.6f  exact %.6f  rel %.2e"
          % (r_e, T_q, T_exact, abs(T_q - T_exact) / T_exact))

print("== grazing reference (leading log; regime-limited, see dossier) ==")
u_ends = 1.0 / 1000.0
for b in (20.0, 100.0):
    T = 2.0 * branch_int(b, u_ends, turning_u1(b, True), turning_u1(b, True),
                         True, True, 8000)
    d_flat = 2.0 * math.sqrt(1000.0 ** 2 - b * b)
    ana = 2.0 * math.log(4.0 * 1000.0 * 1000.0 / (b * b))
    print("b=%6.1f periapsis=%6.3f  delay=%8.4f  leading-log=%8.4f  rel=%6.3f"
          % (b, 1.0 / turning_u1(b, True), T - d_flat, ana,
             abs((T - d_flat) - ana) / ana))
