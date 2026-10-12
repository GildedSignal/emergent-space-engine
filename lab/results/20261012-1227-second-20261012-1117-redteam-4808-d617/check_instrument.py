"""Instrument cross-check: quadrature vs the prior run's ODE, vs the checker's
independent numbers, and analytic limits. Part of the record."""
import numpy as np, sys
sys.path.insert(0, '.')
from cycle import *

print("== quadrature vs falsifier2's ODE path (verbatim) ==")
for (p, e) in [(10, .9), (13, .99), (8.3, .9), (8.05, .9), (8.01, .9), (7.3, .5), (8.28, .99)]:
    up, L = seed_from_pe(p, e)
    E = E_of(up, L)
    dq = float(dphi_quad(E, L)[0])
    do = dphi_cycle_ode(up, L)[0]
    print(f"  p={p:6} e={e}: quad={dq:12.7f}  ode={do:12.7f}  diff={dq-do:+.2e}  rel={(dq-do)/do:+.2e}")

print("\n== checker's independent quadrature values (check.md) ==")
for (p, e, ref) in [(10, .5, 10.0552), (8.2, .9, 14.7651), (8.05, .9, 16.5960), (8.01, .9, 17.5661)]:
    up, L = seed_from_pe(p, e)
    dq = float(dphi_quad(E_of(up, L), L)[0])
    print(f"  p={p:6} e={e}: quad={dq:10.4f}  check.md ref={ref}")

print("\n== analytic limit: near-circular epicyclic ratio 1/sqrt(1-6/r0) ==")
for r0 in [10.0, 20.0, 50.0]:
    up_, L = seed_from_pe(r0 * (1 + 1e-4), 1e-4)
    dq = float(dphi_quad(E_of(up_, L), L)[0])
    print(f"  r0={r0:5}: dphi/2pi = {dq/(2*np.pi):.6f}   1/sqrt(1-6/r0) = {1/np.sqrt(1-6/r0):.6f}")

print("\n== separatrix structure: mu -> 0 as p -> 6+2e ==")
for (p, e) in [(6 + 2*0.9 + 0.001, 0.9), (6 + 2*0.9, 0.9), (8.0, 0.99), (8.28, 0.99)]:
    up, L = seed_from_pe(p, e)
    E = E_of(up, L)
    ua, upr, u3 = bound_pair(E, L)
    mu, pp, ee = margin(ua, upr)
    print(f"  target (p={p:.3f}, e={e}): u_p={upr[0]:.6f} u3={u3[0]:.6f}"
          f" -> p={pp[0]:.4f} e={ee[0]:.4f} mu={mu[0]:+.5f}")

print("\n== margin > 0 whenever two turning points exist (sweep assert) ==")
Es = np.linspace(0.85, 0.9999, 300); Ls = np.linspace(2.5, 4.5, 300)
EE, LL = np.meshgrid(Es, Ls); EE, LL = EE.ravel(), LL.ravel()
ua, upr, u3 = bound_pair(EE, LL)
mu, pp, ee = margin(ua, upr)
sel = np.isfinite(ua) & (EE < 1.0)
print(f"  sweep {sel.sum()} bound orbits: min margin = {np.nanmin(mu[sel]):+.3e}  (must be > 0)")
