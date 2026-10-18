# Predictions (written before the decisive run)

Run: 20261018-0431-scout-b083. Instrument: `scan_replica.py` — a float replica of the
shipped observer scan (`crates/universe/src/encounter.rs::Scan` capture+compute,
`crates/universe/src/radial.rs::candidates`) on planar-Kepler co-orbital fleets, the
encounters page's own replica class (e ≤ 0.5). Units: r = 1 (orbit radius), circular
speed v = 1, n = 1, P = 2π. Dimensionless ship size ρ = (r_a+r_b)/r swept over
{1e-7, 1e-6, 1e-5}; encounter tier near = 2^10·ρ·r (shipped ENCOUNTER_LOG2 = 10);
coast window from 604c's measured constants (reach ≈ 9·r).

Cases I have NOT tuned on (held out until after the code runs):
- P1 (candidate tier): at the coast window (reach ≈ 9r) a co-orbital ring of K bodies
  returns candidates = K (the window ⊇ ring, and the radial representation cannot cut a
  ring at ANY horizon because co-orbital radial ranges ≡ the player's). A phase index
  cuts 0% of candidates at coast. At burn-class windows the radial filter ALSO returns
  all K for the fleet (only the non-fleet population shrinks).
- P2 (answer tier): on a shared circular orbit, d ⊥ w exactly for every member
  (verified algebraically: d·w = 0), so the shipped linear hit predicate reduces to the
  current separation: hit ⟺ 2r·sin(δ/2) ≤ near — horizon-independent. The
  encounter-tier near set is a phase window of ≈ 2·near/(2πr)·K members (uniform
  phases), and under taleb-class clustering (σ_φ = 0.02 rad) it grows ∝ 1/σ_φ.
- P3 (exactness control): the closed-form reduction reproduces the brute-force
  Kepler-solved shipped predicate on the circular fleet to ≤ 1e-12 (positive control);
  at e = 0.5 the closed-form circular reduction is WRONG for the answer (this is the
  known CW-first-order limit) — prediction: relative error of the near-set MEMBERSHIP
  exceeds 10% of members at e = 0.5, so the first-order form is an exclusion tier only,
  widened by the measured bound.
- P4 (shear failure mode): with radial spread σ_a > 0 the window widens by the shear
  term; the phase-only curve becomes UNSOUND (misses hits) once 1.5·n·(σ_a/a)·h·r ≳
  near·(the perpendicular term). Prediction: the σ_a where unsoundness starts follows
  that inequality to within 2× at h = P/10 (measured by brute force).
- P5 (price): per-member answer cost falls from the measured 3.3–4.4 µs
  (binding_at + cartesian, 604c/7343) to ~10–30 flops on a stored offset vector
  (δ, Δa/a, Δe) + O(window) exact reads; at K = 10^6 that is ~4.4 s → ~ms class
  (≥300×), closing 604c's ~500×-over extrapolation to ≈1×.
- Kill criterion: if the closed-form tier cannot decide ≥ 99% of members without a
  read at e ≤ 0.5, σ_a ≤ 1e-4·a (the tight keys-fleet class), the representation is
  dead as a scan tier.
- Negative control: a δ→answer table with shuffled keys must disagree with the true
  answers on ≥ 30% of members (the table carries the information, not the lookup).
