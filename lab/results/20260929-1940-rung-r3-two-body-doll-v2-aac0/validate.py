#!/usr/bin/env python3
"""Stage 1: validate the doll-vs-oracle wiring on a few seeds, then full binaries."""
import sys, json
import numpy as np
sys.path.insert(0, '.')
from r3lib import (eih_EJ, damour_deruelle, doll_binaries, bound_constants,
                   schw_cycle, orbit_from_invariants)

# ---- validation anchors -------------------------------------------------
print("== anchor 1: exact Schwarzschild period vs repo series T_t/T_N = 1+3/a ==")
for (p, e) in [(20.0, 0.0), (100.0, 0.3), (1000.0, 0.6)]:
    dphi, Tt = schw_cycle(np.array(p), np.array(e))
    a = p / (1 - e * e)
    Tn = 2 * np.pi * a**1.5
    print(f"  p={p:7.1f} e={e:.1f}: T_t/T_N - (1+3/a) = {float(Tt/Tn) - (1 + 3/a):+.3e}   "
          f"dphi-2pi vs 6pi/p: {float(dphi) - 2*np.pi - 6*np.pi/p:+.3e}")

print("== anchor 2: eih port self-consistency (weak series: 6pi/p; T first order) ==")
# weak-series period from the repo's eih_weak_series formula
def weak_period(p, e, nu):
    rp = p/(1+e); ra = p/(1-e); j0 = np.sqrt(p)
    v0 = j0/rp
    def corr(r):
        return (-(1-3*nu)*j0**4/(8*r**4) - (3+nu)*j0**2/(2*r**3) + 1/(2*r*r))
    dj = -(corr(rp)-corr(ra))/(j0*(1/rp**2 - 1/ra**2))
    dv = dj/rp - v0*(0.5*(1-3*nu)*j0*j0/(rp*rp) + (3+nu)/rp)
    e0 = 0.5*v0*v0 - 1/rp
    e1 = v0*dv + 0.375*(1-3*nu)*v0**4 + 0.5/rp*((3+nu)*v0*v0 + 1/rp)
    q0 = -2*e0; q1 = -2*e1
    newton = 2*np.pi/q0**1.5
    return 6*np.pi/p, newton, newton*(1 - 1.5*q1/q0 + q0*(15-nu)/8)

for (p, e, nu) in [(50.0, 0.3, 0.2), (200.0, 0.1, 0.1)]:
    E, J = eih_EJ(np.array(p), np.array(e), np.array(nu))
    dphio, To = damour_deruelle(E, J, np.array(nu))
    _, _, Tws = weak_period(p, e, nu)
    print(f"  p={p} e={e} nu={nu}: oracle T={float(To):.6f} weak-series T={Tws:.6f} "
          f"ratio={float(To/Tws)-1:+.2e}; dphi_oracle={float(dphio):.6f}")

print("== anchor 3: eob doll vs oracle on a spread of seeds (should agree to ~2PN) ==")
for (p, e, nu) in [(1000.0, 0.0, 0.25), (1000.0, 0.6, 0.25), (500.0, 0.3, 0.1),
                   (1000.0, 0.3, 0.01), (100.0, 0.3, 0.2)]:
    E, J = eih_EJ(np.array(p), np.array(e), np.array(nu))
    dphio, To = damour_deruelle(E, J, np.array(nu))
    dphid, Td = doll_binaries(np.array(p), np.array(e), np.array(nu), 'eob')
    print(f"  p={p:7.1f} e={e:.1f} nu={nu:.2f}: prec rel err={float(dphid/dphio)-1:+.2e} "
          f"period rel err={float(Td/To)-1:+.2e}")

print("== anchor 4: nu-channel (c_nu doll vs oracle) ==")
for (p, e) in [(1000.0, 0.0), (500.0, 0.3), (200.0, 0.5)]:
    nu = 0.2
    E, J = eih_EJ(np.array(p), np.array(e), np.array(nu))
    _, To_nu = damour_deruelle(E, J, np.array(nu))
    E0, J0 = eih_EJ(np.array(p), np.array(e), np.array(0.0))
    _, To_0 = damour_deruelle(E0, J0, np.array(0.0))
    Ror = float(To_nu/To_0) - 1
    _, Td_nu = doll_binaries(np.array(p), np.array(e), np.array(nu), 'eob')
    _, Td_0 = doll_binaries(np.array(p), np.array(e), np.array(0.0), 'eob')
    Rd = float(Td_nu/Td_0) - 1
    print(f"  p={p:7.1f} e={e:.1f}: R_oracle={Ror:+.3e} R_doll={Rd:+.3e} "
          f"rel diff={Rd/Ror-1:+.2e}")
