# Predictions — 20261007-0341-scout-9abe

Written BEFORE running S2c, S2d, S2c2, S3, S4. Tuning happens on S1 only
(choice of kappa; nothing else). Truth = RK4 at 1024 steps/orbit, prescribed
circular/elliptic perturbers with the indirect term (K1's tide model).

Mechanism under test ("TRIG"): next kick when B(tau) = 0.5*J*tau^2*(1+tau/P)
reaches kappa*|a_tide|*P, J = local tidal jerk along the drift; tau in
[P/64, P/4]; wall flag when even P/64 cannot hold the bound.

## Anchors (sanity, not held out)

- A1: K1QUANTUM replica on S1 lands within ±20% of K1's 32.5 kicks/orbit
  (26–39 over 60 orbits).
- A2: FIXED-4 on S1 unbinds or badly mis-pumps (known: 8/orbit is the floor);
  FIXED-8 holds.

## Held-out predictions

- P1 (S1 itself, kappa sweep): TRIG at some kappa in {0.25, 0.5, 1} fires
  between 0.7 and 4 kicks/orbit on the quiet LEO scene, with da_rel <= FIXED-8's
  da_rel and de <= 1e-3. If TRIG needs > 8 kicks/orbit on S1 to hold, the rule
  is dead (LEAD).
- P2 (S2c, 2:1 centre): AVG mis-pumps eccentricity (epump_ratio outside
  [0.5, 2], expected far off); TRIG densifies to >= 16 kicks/orbit (rate spread
  vs S1 >= 8x) with wall flags > 0 near conjunctions. I do NOT predict TRIG
  matches the librating truth (dynamics-a9c2 says no rate <= 64 does); the
  claim is detection, not accuracy.
- P3 (S2d, detuned 2/3 of half-width): weaker resonance; TRIG lands between
  2 and 16 kicks/orbit; epump_ratio strictly closer to 1 than AVG's.
- P4 (S3, e=0.3 moderate tide): TRIG kappa=0.5 lands in 4–20 kicks/orbit with
  de <= 2x FIXED-16's de and da_rel <= FIXED-16's.
- P5 (S4, adversarial e_p=0.6 conjunctions): TRIG's kick times cluster near
  conjunctions (>= 3x the uniform density within ±30° of conjunction); walls
  fire; TRIG's error at its own kick count <= FIXED's error at the same count.
- P6 (mixed total, the gold bar): on S1+S3+S4 with one kappa fixed on S1,
  total TRIG kicks <= 1/4 of total FIXED-16 kicks with behaviour no worse
  (da_rel, de) on every scene. S2 is reported separately as the detection case.

## What would make me wrong

- TRIG Pareto-dominated by FIXED at equal kick count on any scene (unsound
  bound) → LEAD.
- TRIG never densifies on S2c (stays <= 4/orbit while AVG fails) → the
  detection claim is dead; at best SILVER with the escalation redesigned.
- Total cut on the mixed scenes < 4x vs FIXED-16 (the lens's gold bar) →
  SILVER: real rule, gold bar missed.
