# Predictions (held out before the decisive run)

Target premise (representation.md L37 / law.md L39 / `crates/space/src/events/binary.rs`):
"Two comparable masses form one doll with M = m1+m2; ν enters only through the
effective-one-body energy map at 1PN." Shipped: the effective orbit is the **exact
Schwarzschild geodesic** (A = 1−2u), so the doll's plunge boundary is ν-blind at
u_ISCO = 1/6 (r = 6M) for every ν.

Oracle (next term beyond the premise): the 2PN EOB radial potential
A(u) = 1 − 2u + 2ν·u³ (Buonanno–Damour 1999; the leading ν-in-the-potential term).
Circular orbits: j²(u) = −A′/(2uA + u²A′), W(u) = A(1+j²u²); ISCO solves W″(u) = 0.
Circular-adjacent periastron advance from the epicyclic ratio Ω_r/Ω_φ of the same
Hamiltonian (radial kinetic (p_u u^{−2})²/A, as Schwarzschild's g_rr = 1/A; the 2PN D̂
correction is omitted — stated oracle domain, it is same-order-but-smaller in νu²).

Cases not tuned on, and what I expect:

- P1 (ISCO shift, equal mass): u_ISCO(ν=1/4) exceeds 1/6 by **≥ 10%** (r_ISCO ≤ 5.4M).
  The doll calls every circular binary in (r_ISCO, 6M) stable; the oracle says plunge.
- P2 (ν scaling): the shift is monotone in ν and < 1% at ν = 0.01.
- P3 (precession at B11's inner edge): at u = 1/20 (p = 20M, circular), the relative
  difference between the doll's and the oracle's periastron advance at ν = 1/4 is
  **≥ 1%** (above B11's flat tolerance term), while at u = 1/1000 it is < 10⁻³.
- P4 (instrument controls): at ν = 10⁻⁶ both potentials agree: u_ISCO = 1/6 − 1e−9,
  Ω_r²/Ω_φ² = 1 − 6u to < 1e−9, doll-oracle precession difference < 1e−9.
- P5 (held-out, honest guess, not tuned): the epicyclic ν-shift at u = 0.05, ν = 0.25
  lies between 0.1% and 5% relative.

Kill criterion (frozen now): the premise **as a game claim for the merger scene is
breached** if the plunge boundary is ν-shifted by > 5% at ν = 1/4 AND no existing
rung/gate classifies binary plunge or stability (B4 is single-mass; B11/r3 judge
precession, period, ν-effect only, against a 1PN oracle). Survives if the shift is
< 2% or a gate covers it.
