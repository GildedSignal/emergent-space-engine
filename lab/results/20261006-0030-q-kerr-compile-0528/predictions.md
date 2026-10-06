# predictions.md — written before the decisive verification grid

Held-out cases: I tuned nothing on them (the tuning used chi=0 reduction to
ENVELOPE.md, circular-orbit Omega/H closed forms, and one bound orbit at
chi in {0, 0.5}, k=3/4, q=1/8). The grid below is chosen by rule, not by
success.

## P1 — agreement with direct integration

For every vector in the grid (chi in {0, 0.5, 0.9, 0.998}, both senses,
e in {0, 0.1, 0.3, 0.6, 0.9}, q from weak field to near-separatrix,
unbound, photons near and far from critical b, an E<0 ergosphere plunge):

  |compiler - direct RK4 Hamiltonian| / |value| <= 1e-12

on all three increments where defined (dt is not defined at horizon arrival
or at infinity). I expect ~1e-14 typically; if any family exceeds 1e-12 I
expect it to be the near-separatrix whirl at chi=0.998 (long periods make
the RK4 error control the binding constraint, not the compiler).

## P2 — weak-field series structure in q

At fixed k and chi, fitting Delta phi - 2*pi in powers of q^(1/2):

- the chi=0 series has only integer powers (6*pi*k*q leading — Darwin);
- the odd-in-chi part first appears at q^(3/2) (Lense-Thirring), which I
  predict has coefficient C1(k) = -12*pi*k^(3/2) from the standard
  per-orbit LT apsidal rate (uncertain: sign and the exact k-power);
- the even-in-chi part first appears at q^2, same order as the chi=0
  second-order term, so one memo per (k, chi) carries the q-series exactly
  as the Schwarzschild memo does per k, with one extra sense bit.

## P3 — shape inverse and memo key

For fixed (k, q, chi) the two turning-point equations give a unique (E, L)
per sense on the bound domain (Newton from the Schwarzschild seed converges
without continuation except near the separatrix); the map degenerates only
as the separatrix is approached (u_3 - u_1 -> 0 double root). Predicted:
no solutions interior to q_sep(k, chi, sense) on either branch.

## P4 — nodes (which integrands lose smoothness, chi -> 1)

All three integrands share g = 1/sqrt(2(u_3 - u)); the only smoothness loss
is the integrable square-root degeneration at psi = pi as q -> q_sep (the
whirl: apoastron root u_1 merges with u_3·... merges toward the double
root). Predicted: the Gauss-Legendre order n needed for 1e-13 relative on
the half-cycle grows like (1 - q/q_sep)^(-1/2)·polylog, roughly n ~ 100 at
1 - q/q_sep = 1e-2 and n ~ 500-2000 at 1e-4; chi=0.998 prograde adds
conditioning (not smoothness) to dt (periapsis near the horizon, Delta
small in the denominator) but no new singular structure. If plain GL needs
> 4096 nodes anywhere on the grid, the compiler should panel-split at
psi = pi (as the crate already cuts at band edges).

## P5 — negative energy

At chi = 0.998: future-directed timelike orbits with E < 0 exist, all have
their outer turning point inside r = 2 (ergosphere), and none is bound
(no pair of positive turning points) — they plunge. Outside the ergosphere
no E < 0 solution of V(r) = -1 exists at any L (scan).

## P6 — photons

The null cubic's double root reproduces Bardeen's equatorial b± (verified
already in tuning: r_ph and b± match the closed forms to all digits); the
compiler's deflection for b -> b_crit+ diverges logarithmically·... grows
without bound (strong-field whirl), and for |b| >> |b_c| tends to
4/b + (15 pi/4)·(1/b²)·... the ENVELOPE weak-null form 4q + (15pi/4 - 4)q²
with q identified per the passage shape.
