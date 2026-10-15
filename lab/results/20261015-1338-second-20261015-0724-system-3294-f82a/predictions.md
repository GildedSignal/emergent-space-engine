# Predictions — 20261015-1338-second-20261015-0724-system-3294-f82a

Written before the decisive flights (the 10⁴ coast/burn × baseline/stagger arms). What I have seen
before writing this: two 5-second smoke flights at N=10³ to check the instrument prints (census
line, dim buckets present; ship/child dim peaked at 2⁻²⁷–2⁻²¹ of speed; ship/root not inspected),
and the prior run's published record (3294: fire rate 1.000, dv ≥ 2⁷ word units, wave-1 central
50% span 246 s on a 28,141.5 s interval). No 10⁴ flight of this build has run yet.

1. **Dimensionless impulse (belt, ship/root).** The fired impulse as a fraction of the body's own
   speed: median |dv|/|v| = 2⁻ʰ with h in [24, 34] (I predict h ≈ 29 ± 3). Derived claim that
   matters: at the behaviour floor (2–8 kicks/orbit, i.e. ~550–2,200× coarser than the grid) the
   per-kick impulse would still be ≥ 2⁷ word units (it grows ∝ Δs to first order), so the quantum
   fire-gate cannot bind before the behaviour gates do — the regime-split Δs is bounded by
   behaviour alone, now dimensionlessly, not just at 16×/64× (the checker's coarser-Δs arms).
2. **Staggered genesis flattens the train.** With the first clock begin of each body offset by
   hash(id) over one interval: belt wave-1 central-50% span goes from 246 s to ~0.5·I ≈ 14,000 s
   (uniform phase), and waves 2–3 lose their concentration too (spans grow toward the interval);
   the per-body fire interval median stays ≈ 28.1 k s; fire rate stays 1.000 (the gate is
   untouched); dv buckets unchanged.
3. **Stagger is behaviour-neutral on the counters that exist here.** dead = 0, refusals = 0,
   player alive, catalogue = bodies + 48 (no sharing change). The digest at a canonical cut
   (+80,000 game-s) differs from baseline (kick ticks moved — that is the change), and reproduces
   across re-runs of the same arm.
4. **Frame tail (soft, load-shared machine).** The wave crossing is a rebind storm; flattening it
   should cut the coast arm's worst-frame events and max_ms (direction: down; I do not predict a
   magnitude on this host — the integrator re-measures on the M1). held_max should drop in the
   burn arm (the train×burn interaction was the named tail there).

Kill criteria: if the staggered arm's belt fire rate leaves 1.000, or the wave-1 span stays
< 1,000 s (stagger did not reach the belt), or dead > 0 appears with the stagger on, the
corresponding claim dies and I report it as dead.
