#!/usr/bin/env python3
"""Decisive falsifier set (run: python3 falsifier2.py, ~10 s).
falsifier.py is kept as the documented broken instrument (its analytic band
stepper lands u exactly on shared edges and re-enters the band it just left,
turning spuriously; see dossier). This file uses raw ODE integration."""
import numpy as np
from scipy.integrate import solve_ivp

def seed_from_pa(rp, ra):
    """GR osculating orbit through periapsis rp, apoapsis ra -> (u_p, L)."""
    up_, ua_ = 1.0/rp, 1.0/ra
    L2 = ((1-2*ua_) - (1-2*up_)) / ((1-2*up_)*up_**2 - (1-2*ua_)*ua_**2)
    return up_, np.sqrt(L2)

def cycle_exact(u_p, L):
    """Exact GR radial cycle (periapsis->periapsis): returns (dphi, T, E)."""
    L2 = L*L
    E = np.sqrt((1-2*u_p)*(1+L2*u_p*u_p))
    u_pp = 1.0/L2 + 3*u_p*u_p - u_p
    eps0 = 1e-6
    y0 = [u_p + 0.5*u_pp*eps0*eps0, u_pp*eps0, 0.0]
    def rhs(phi, y):
        u, up, t = y
        return [up, 1.0/L2 + 3*u*u - u, E/(L*u*u*(1-2*u))]
    def peri(phi, y): return y[1]
    peri.direction = -1.0; peri.terminal = True
    s = solve_ivp(rhs, [eps0, 200*np.pi], y0, events=peri, method='DOP853',
                  rtol=1e-11, max_step=0.02, atol=[1e-13, 1e-13, 1e-8])
    assert len(s.t_events[0]), "no periapsis found (plunge?)"
    return s.t_events[0][0] - eps0, s.y[2,-1], E

def band_ode_cycle(u_p, L, m=16):
    """Binet band model as raw ODE: u'' = C_k - w_k^2 u, k = band(u)."""
    L2 = L*L
    def rhs(phi, y):
        k = int(np.floor(-np.log2(max(y[0], 1e-300))*m))
        uc = 2.0**(-(k+0.5)/m)
        return [y[1], (1.0/L2 - 3*uc*uc) - (1-6*uc)*y[0]]
    u_pp = 1.0/L2 + 3*u_p*u_p - u_p
    eps0 = 1e-6
    y0 = [u_p + 0.5*u_pp*eps0*eps0, u_pp*eps0]
    def peri(phi, y): return y[1]
    peri.direction = -1.0; peri.terminal = True
    s = solve_ivp(rhs, [eps0, 200*np.pi], y0, events=peri, method='DOP853',
                  rtol=1e-11, max_step=0.02, atol=[1e-13, 1e-13])
    return s.t_events[0][0] - eps0 if len(s.t_events[0]) else None

print("A. Binet band model (m=16) vs exact GR — r1 sampled e<=0.7 only")
for (p, e) in [(10,.5),(13,.7),(13,.8),(13,.9),(13,.95),(13,.98),(13,.99),
               (8.3,.9),(8.1,.9),(8.0,.9),(7.95,.9)]:
    u_p, L = seed_from_pa(p/(1+e), p/(1-e))
    dG, _, _ = cycle_exact(u_p, L)
    dB = band_ode_cycle(u_p, L)
    print(f"  p={p:6} e={e}: dphi_GR={dG:9.4f}  band={dB:9.4f}  relerr={abs(dB-dG)/dG:7.3%}")

print("\nB. kick multiply-add on the cycle: gain and one-signed truncation (delta L/L=1e-4)")
print("   (dG2 - [dG + dG'/dL * dL]); sign equal for +/-dL means systematic drift")
for p in [10, 8.5, 8.2, 8.1, 8.05, 8.02, 8.01]:
    e = 0.9   # critical p ~ 7.8: zoom-whirl separatrix
    u_p, L = seed_from_pa(p/(1+e), p/(1-e))
    dG, _, _ = cycle_exact(u_p, L)
    dG2, _, _ = cycle_exact(u_p, L*1.0001)
    dGm, _, _ = cycle_exact(u_p, L*0.9999)
    dd = (dG2 - dGm)/(2*0.0001*L)
    print(f"  p={p} (crit~7.8): dphi={dG:8.4f}  gainL={abs(dd)*L/dG:6.1f}  "
          f"err(+/-.deltaL)={dG2-(dG+dd*0.0001*L):+.3e} / {dGm-(dG-dd*0.0001*L):+.3e} rad/kick")

print("\nC. past-light-cone crossings of an orbiting emitter, observer at beta")
for beta in [0.9, 0.99, 0.995]:
    gam = 1/np.sqrt(1-beta*beta); R, Om = 1.0, 0.2
    roots = []
    for tobj in np.linspace(100, 100+gam*5, 40):
        te = np.linspace(tobj-120, tobj, 200001)[1:-1]
        xe = np.stack([R*np.cos(Om*te), R*np.sin(Om*te)], 0)
        xo = np.array([beta*tobj, 0.0]).reshape(2, 1)
        f = tobj - te - np.linalg.norm(xe - xo, axis=0)
        sgn = np.sign(f)
        roots.append(int(np.sum(sgn[:-1]*sgn[1:] < 0)))
    print(f"  beta={beta}: crossings per gather: {min(roots)}..{max(roots)} (f strictly decreasing => 1)")
