# Predictions (written before the held-out runs)

Tuned on: 8 s flights, seed 1, arms ship/fine/off (the run's calibration above).
Held out below: 16 s flights (seed 1), seed 3 (8 s), and the f8 (1/256) interpolation arm.

The claim under test: the burn-cadence clamp (one rebind per 1/64 of |v|) is the engine paying
events to keep a readable state fresh because the state cannot express "a body under thrust
between events". Its two halves predict differently:

- **P1 (events):** the `off` arm collapses player items during held burns to ≈ the coast's own
  cadence and kills the burst frame and the lag, at every level, duration and seed. Predicted:
  pitems(off) < 100 on every held-burn flight (ship: ~800–2,900 at 8 s), pburst(off) = 1,
  lag(off) = the coast's 0.038 s at every level.
- **P2 (physics):** deleting the clamp without carrying the burn in the state breaks the burn:
  the canonical tube never absorbs it (end |v|/c ≈ the coast's), the view's owed dv grows to a
  ½aT² envelope between flushes, and the L12/L15 flush path refuses. Predicted: end |v|/c(off)
  within 2× of coast on forward L12/L15 at both durations and both seeds (ship: 0.032/0.25);
  refusals(off) > 0 on forward L15; max owed dv per read window ≥ 10⁻³ c at L15.
- **P3 (the shipped arm's own error):** the shipped 1/64 sampling is not exact either: its end
  velocity sits ~1.4–2.1% below the 1/1024 arm at L8–L15. The f8 (1/256) arm should land between
  them, monotone in the sampling fraction (predicting first-order-in-step error): predicted
  end |v|/c at L15 orders f8 ∈ (ship, fine), and |f8 − fine| ≈ |ship − f8|/2 within a factor 2.
- **P4 (duration):** at 16 s the ship arm's player items roughly double (burn time doubles), the
  off arm stays < 100, and the fine arm's worst frame grows past 20 ms (more items per burst).
- **P5 (seed):** seed 3 reproduces every ratio above within 3× (the counts are level-set, not
  seed-set).

Kill criteria for the claim: P1 failing (the waterfall is not the clamp's) kills the premise; P2
failing on the refusals/staleness (the deletion is actually safe) would make the deletion a
one-line adoptable fix instead of a carry contract — also a result, the other way.
