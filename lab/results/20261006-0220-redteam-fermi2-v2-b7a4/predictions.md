# predictions.md — run 20261006-0220-redteam-fermi2-v2-b7a4

Written BEFORE the decisive experiment (`kernel.py`). Already in hand from the
pre-predictions convention check (`sanity.py`, sign/rotation conventions only,
no kernel table, no epochs): the fixed-sign einsum equals diag(-(2+3lam)m, +m)
at tau=0 on circ 6M and 3.1M; omega = sqrt(M/r^3) exactly on circular orbits;
the prior run's "orbit" window 2*pi*r^1.5 is the coordinate period
(tau_end/T_p = 1/sqrt(g)).

## P1 — kernel table values (held-out numbers)
Closed-form in-plane eigenvalues {-(2+3lam)m, +m} and out-of-plane m(1+3lam),
with lam = L^2/r^2 = M/(r-3M) on circular orbits (L_circ^2 = M r^2/(r-3M)),
equivalently radial = -w(3*gamma^2-1) with gamma^2 = f/g (the two reductions
agree once lam is substituted correctly; the disputed sign R_{rFrF} does not
enter the boost derivation of the radial eigenvalue, so the closed form and
the independent boost derivation concur):
- circ 6M: lam = 1/3, radial = -3w (w = 4.6296e-3), transverse +w, C11 = 2w.
- circ 4M: lam = 1, radial = -5w = -2w*2.5 (gamma^2 = 2), C11 = w/g = 4w.
- circ 3.1M: lam = 10, radial = -32w = -2w*16.0, C11 = w/g = 31w.
Geodesic h->0 Richardson values match closed form within 1e-3 relative at every
scene and measurement point.

## P2 — window leakage (held-out)
At 3.1M, a full-proper-orbit window inflates |radial eigenvalue| by 1.25-1.55x
over the h->0 value (prior run's 23.6/16.0 anchor was a 5.57-orbit window);
the h-sequence converges monotonically (2nd order in h) to the closed form.

## P3 — rotation sign (held-out, falsifiable)
The geodesic-measured tensor at tau_0 > 0 matches R(Phi) C^B R(Phi)^T with
Phi(tau) = -int_0^tau omega dt, omega = E L M/(r^2 (r E^2 + 2M - r)) — the sign
as written in schwarztide.py. If instead the mirrored sign matches, the closed
form's omega convention is wrong and I report it.

## P4 — E-independence (held-out)
Two unbound orbits with the same L = 4.1 (E = 1.05 and E = 1.5), measured at the
same r = 6 outbound, share eigenvalues to <1e-12 in closed form and agree with
the geodesic measurement within 1e-3 (Xin-Mummery E-independence).

## P5 — epoch rule (held-out numbers; 2^-8 tolerance per kick)
- The eigenaxis sweep of the corrected kernel over the prior run's window
  (2*pi*r^1.5 of proper time) is exactly 2*pi at EVERY circular radius
  (omega = sqrt(M/r^3)): their epT column (3214/4017/4038) cannot be a physical
  rate — it is an unwrap artifact (values land on (1+k/2) full turns). Honest
  per-TRUE-orbit numbers: axis rule N = 512*pi*sqrt(g): 1606 (far), 1137 (6M),
  804 (4M), 289 (3.1M). The naive kernel's axis (co-rotating r-hat) sweeps the
  SAME 512*pi*sqrt(g) on circular orbits — same cadence, so the naive kernel
  costs accuracy, not kicks, on circular.
- Tensor rule N = 256*sqrt(2)*|a-b|/sqrt(a^2+b^2) * omega * T_p =
  512*pi*sqrt(2)*3f*sqrt(g)/sqrt((2-3x)^2+g^2): 3055 (far), 2035 (6M), 1337 (4M),
  421 (3.1M). The checker's corrected tensor counts, divided by their window in
  true orbits, land within ~5% of these (2877/1.4142 = 2034; 2395/5.5678 = 430).
- Phase-1's band (1600-3200/orbit) is set by the WEAK field; inside r ~ 4.6M the
  corrected kernel needs FEWER kicks per orbit than phase 1's band.

## P6 — eccentric and unbound epochs (held-out)
- ecc rp6.5 L3.5 (e ~ 0.88): tensor-rule N per radial period 2000-6000,
  dominated by periapsis; the naive axis (co-rotating r-hat) now rotates
  differently from the true eigenaxis (C23 != 0 inside the boosted frame).
- Unbound (parabolic rp6; hyperbolic): N per passage < 1500; peak kernel at
  periapsis equals the closed form within 1e-3.

## P7 — conditioning (held-out)
Richardson converges monotonically in h at 4M and 3.1M (no reconstruction
breakdown at kernel level, unlike the prior run's member-level r=3.1 exclusion).
