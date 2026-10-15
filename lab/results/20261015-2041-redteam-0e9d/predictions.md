# Predictions — 20261015-2041-redteam-0e9d

Premise under attack (docs/representation.md §3, premise 3 of the lens): "A cycle's
derivatives are stored with it, so a kick updates the cycle by a multiply-add."
Attacked on the separatrix family (near-parabolic bound orbits, e → 1; and the GR
bound/plunge separatrix). Derived analytically before any run; the run's numbers are
the held-out confirmation.

## Pre-registered expectations (analytic, Newtonian Kepler cycle, q = μ = 1)

- Exact period T = 2πμ(−2E)^{−3/2}. For a kick with x = δE/|E|, exact cycle ratio
  T′/T = (1+x)^{−3/2}; multiply-add ratio = 1 − (3/2)x. So:
  **per-kick relative cycle error ε₁ = (15/8)x² − (35/16)x³ + …**
- Periapsis tangential kick of size δv (worst site, v maximal there):
  **x = 2√(1+e)·δv/(1−e)**, with δv in units of the circular speed at q (v_p = √(1+e)).
- 1%-behaviour bar (r-family style): x* = √(0.01·8/15) = 0.0730 ⇒ the multiply-add is
  over the bar for (1−e) ≤ 27.4·√(1+e)·δv, i.e.
  - belt quantum kick δv = 2⁻²³ ≈ 1.19e−7: breaks only at e ≳ 0.999995 (rarer than any
    shipped family);
  - encounter kick δv = 1e−3: breaks at **e ≥ 0.961**;
  - deep-passage kick δv = 1e−2 (B13's regime): breaks at **e ≥ 0.61** — half of r1's
    own sampler family;
  - slingshot δv = 0.3: everywhere.
- Stored second derivative (two more numbers per record) moves the bar to
  x* = (0.01·16/35)^{1/3} = 0.166 (≈ 2.3× wider band), still dead at slingshot x ~ 1.

## Held-out numeric arms (not derivable from the above; these decide)

- **H1 (confirmation of the reduction):** direct Kepler arithmetic at
  x ∈ {1e−3, 1e−2, 1e−1, 3e−1, 1} matches ε₁ = (15/8)x² + O(x³) to better than 1%
  relative for x ≤ 0.3.
- **H2 (control that must pass):** benign regime x = 1e−4 (circular orbit, belt kick):
  multiply-add ε < 2e−7. If this fails, the instrument is broken, not the premise.
- **H3 (chaining, error type):** 200 sequential kicks at δv = 1e−3 from e₀ = 0.95,
  periapsis-to-periapsis. Fresh-derivative-per-kick (re-anchor from true (E, L) each
  kick): mean-anomaly error grows ~linearly in kick count. Chained multiply-add
  (derivatives of the already-updated record): grows faster than linear (multiplicative
  drift), until e → 1 or unbinding. Prediction: chained/fresh error ratio > 3× by
  kick 100.
- **H4 (GR plunge separatrix, numeric Binet u″ = 1/L² + 3u² − u, L = 4, M = 1):**
  the radial period T(E) diverges as E → E_sep⁺. Pre-registered guess: logarithmically
  in (E − E_sep) (saddle dwell), which still makes ∂T/∂E diverge algebraically (≥ δ^−1/2).
  Either way: at fixed δE the multiply-add error diverges as the separatrix is
  approached; I will measure the divergence exponent and the multiply-add error at
  δ = 1e−2, 1e−3 above E_sep. Held-out: the exponent itself.
- **H5 (harness control):** with the 3u² GR term set to 0 the same integrator
  reproduces the Newtonian (1+x)^{−3/2} law to < 1e−6 at x = 0.1.

## Kill criterion (frozen before the run)

The premise sentence fails as a universal law if there is a (e, δv) pair **inside the
game's own families** (r1 sampler goes to e = 0.9; B13 deep passages δv/v ~ 1e−2;
comets e ≥ 0.99 in any stirred belt) where one kick's multiply-add cycle update errs
more than 1% on T against the exact recompile. Analytic says (e = 0.99, δv = 1e−3)
gives 14.9%; the run confirms or kills this.

A premise that survives would show ε₁ under the bar at every in-family (e, δv); that
would refute my attack and I will report it.
