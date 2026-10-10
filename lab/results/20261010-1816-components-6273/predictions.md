# Predictions (written before the decisive run; the sweep below was Fermi-derived, not tuned)

Model: r8-like belt (a in [1, 1.5], sigma_e sweeps, rho = encounter radius), mutual
gravitational kicks applied with the impulse approximation at closest approach, elements
refit on the law's integer grid (period/periapsis in ticks = 2^-32 time units; e, pom at
2^24 fractional bits unless said). Distinction = any nonzero quantized element delta.

Fermi anchor (derived, not measured): U ~ 1e-3 (Kepler shear over neighbour spacing),
d <= rho = 1e-3, so dv/v ~ 2*mu_b/(U*d) ~ 2e9 * mu_b, and dP_ticks ~ 1.6e20 * mu_b.

## Tuned-on cases
- Main sweep: n=4000, sigma_e=1e-2, rho=1e-3, 100 orbits, mu_b in 1e-26..1e-12.

## Held-out predictions (not tuned on)

P1 (crossover): the mu_b at which 50% of encounters produce a nonzero deltaP (>= 1 tick)
lies in [1e-21, 1e-19]. (Anchor says ~6e-21 at d=rho, U=1e-3; the d and U spread moves it
down.)

P2 (volume): at mu_b = 1e-18, stored bits per belt body after 100 orbits (scar codec,
min(scar, fresh ~130-bit slot) rebind) lie in [8, 80] bits/body; therefore 10^9 belt bodies
land in [1, 10] GB — i.e. the answer to "do 10^9 fit in 8 GB" is decided by mu_b being
above or below ~1e-18, not by the body count.

P3 (coorbital): a narrow coorbital belt (a in [1, 1.0001], sigma_e=3e-4, same rho) has
encounter rate per body per orbit 5-50x the wide belt's.

P4 (fields): period and periapsis deltas carry > 70% of the event bits at mu_b <= 1e-16;
e/pom stay mostly zero below mu_b ~ 1e-16.

P5 (controls): mu_b = 1e-26 produces exactly 0 distinct bodies in 100 orbits (instrument
positive control); a float (unquantized) accounting marks every encounter distinct
(negative control: quantization is the whole lever).

P6 (conditional structure): conditioning deltas on the encounter distance d reduces the
order-0 entropy per event by at least 1 bit (the scar field is not conditionally flat);
if not, a d-conditioned codec is not worth building.

## What would falsify the framing
- If bits/body saturates far above 130 (residuals not rebindable), the population+scar
  store is dead and the belt must stay un-stirred or be chunked in time.
- If the encounter rate grows with kicks (feedback), saturation is faster than linear in
  orbits and the horizon matters more than the rate.
