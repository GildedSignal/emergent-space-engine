# Predictions (written before the decisive verification run finished)

The closed form (Legendre F/E/Π via Carlson RF/RD/RJ, squared pole by the sympy-solved Hermite
reduction) is tested against the shipped walk's dumped states on the 36-key grid (p in
{7,10,30,100,1e4,1e6} x e in {0.001,...,0.999}), 23 samples per key. Cases I did NOT tune on:

1. **Weak field (p=1e4, 1e6, q<=1e-4):** the n4 pole nearly vanishes (n4 ~ 2qe) and the 3x3
   partial-fraction solve approaches singularity. Prediction: psi agrees to <=1e-6 relative
   (Newton converges), tau/adv to <=1e-8; if the solve loses digits, the p=1e6 rows degrade
   gracefully (error grows with 1/n4), not catastrophically (the c4 coefficient -> 0 cancels).
2. **Near-separatrix rows (p=7, e=0.9/0.99/0.999):** m -> 1 (m = 4q(1-k)/A). Prediction: the
   closed form stays exact to its f64/mpmath arithmetic (the walk degrades there instead — de99's
   second checker measured the walk at 6.7e-7 near the separatrix); so at worst the two disagree
   at ~1e-6 relative on adv near p=7, e=0.999 — the mismatch would be the WALK's error, not the
   closed form's (checkable against mpmath.quad of the raw integrand).
3. **Newton inversion count:** starting from psi0 = pi*Tt/t(pi) (linear in time), prediction:
   <=5 iterations to |dpsi| < 1e-30 at 40 dps on every key including e=0.999 (the integrand's
   monotonicity is clean; near periapsis of high-e keys the curvature is high but Newton on a
   monotone convex function from below converges).
4. **The shipped read_ns distribution (not tuned):** prediction before looking: read_ns grows
   with e roughly like the knot count (5->176 per de99), from ~2-10 us at e<=0.3 to tens of us
   at e=0.999; build_us likewise (3->191 us class).
5. **R-call count per readout (composition input):** prediction: t(psi) = 4 RF + 3 RJ + 1 RD;
   full state = t + tau + adv + ~4 Newton steps ~ 18 RF + 13 RJ + 5 RD, constant in e.

If (1) or (2) fails at the stated level, the closed form is wrong somewhere and the run reports
the failure, not the theory.
