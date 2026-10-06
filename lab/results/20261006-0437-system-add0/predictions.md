# Predictions (written before the decisive run)

Run: 20261006-0437-system-add0. The decisive run is `python3 flyby.py rows.json` — the
full 75-seed sweep (v∞ ∈ {5,8,12,16,20} km/s × periapsis target ∈ {1.2,3,10,30,50} R_J ×
3 approach angles, one tuned per v∞ to land near-parabolic heliocentric e), six
configurations per seed: A (the plane's phase rule, hmax=0.5 yr), A2/A01/A002 (A with the
clamp at 2 / 0.1 / 0.02 yr), B (epochs = the tube's own event times), C (oracle cadence
inside Jupiter's doll). The instrument was debugged on 6 smoke seeds (disclosed in the
dossier); the code below this line is frozen for the decisive run.

Cases I have NOT tuned on, and what I expect there:

- **P1 (the plane's failure mode reproduces).** A fails B13's 1% band on a minority of
  in-band seeds (actual closest approach 1.2–50 R_J), concentrated at low v∞ (≤ 12 km/s)
  and bound-but-eccentric to unbound heliocentric e (e ≳ 0.7): the encounters whose
  star-doll approach leg outruns the engaged sub-cadences. Fast encounters (v∞ = 20) pass
  under A (their annulus crossing is quick and mostly radial, so the midpoint force is
  closer to the mean).
- **P2 (the clamp decides, not the phase fraction).** For every A failure, A2 (clamp 2 yr)
  is worse or equal — the clamp, not P/64, sets the step for unbound and near-parabolic
  orbits (P = ∞ or ≫ 64·hmax). A002 (clamp 0.02 yr ≈ 25× finer) passes nearly everything
  A fails, at ~25× the kicks: the same physics, bought with a free parameter.
- **P3 (events replace the parameter).** B passes ≥ 90% of in-band seeds with no clamp to
  tune (its only floors are numerical: HMIN and the 1.000000001 landing overshoot), cuts
  A's error by roughly an order of magnitude on A's failures, and costs ~2–3× A's kicks —
  against A002's ~25× for the same accuracy.
- **P4 (the residue is structural, and it sits where m-meso-motion said).** B's remaining
  failures concentrate on wide slow encounters (actual ca ≳ 25–30 R_J with v∞ ≤ 12 km/s)
  at 1–2%: the annulus [R_edge/4, R_edge] where the level shares W_l are evaluated at
  midpoints of ratio-2 shells whose step ratio is 4 — under-resolved by the changeover's
  own geometry, not by the epoch rule. That is the regime the lab's m-meso-motion pair
  event (one exact event for the whole encounter) exists to delete.
- **P5 (the control).** C is bit-comparable to A on nearly all seeds (its jup-doll oracle
  cadence changes nothing): the error does not live inside Jupiter's doll. A control that
  cannot fail (C ≡ A) and one that cannot pass (A2 on unbound seeds) both present.

If P1 fails (A passes everything), the plane's B13 starvation is not reproduced at float
level in this scene and the cadence explanation loses its only replica evidence — I would
report that and stop.
