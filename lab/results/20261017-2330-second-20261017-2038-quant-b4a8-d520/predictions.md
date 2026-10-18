# Predictions (written before the decisive run)

Question (the checker's named experiment, calendar page open direction 4): on the shipped
chained clock, how long does the genesis fire train live as a function of the population's
step spread, and does a compact-store belt with quantized (shared exact) periods sit on the
combing side of that rule?

Instrument: one census (b4a8's, extended) per fire generation g = 0..8 on belt populations
whose orbit-draw width is swept ([2,3) AU down to [2.999,3) AU, σ_e as shipped) plus two
quantized-class arms (shared exact (a,e) per class: 32 and 1024 a-classes × 4 e-levels over
[2,3) AU). All seed 1, shipped law, `settle` to H_g = first_max + g·step_max·1.03.

Reading of the shipped law before any measurement: the belt's step is `ext.ticks(time(y, ds))`
with y = H_D + p_t + c ≈ U_P(planets' potential at the body's position) + c; the step spread
across a population therefore follows the draw's (a,e) spread through H_D, with a floor set
by the phase-dependent part of U_P and the clock's integer arithmetic. Genesis fires sit at
first ≈ step/2 per body, so the genesis train width ≈ half the step spread.

- **P1 (spread scaling, with a floor).** Step relative spread (p99−p1)/p50 tracks the draw
  width Δa/a with exponent ≈ 1.5 (Kepler) down to ~[2.95,3), then stops shrinking: the
  e-draw (σ_e = 0.07, unchanged in the sweep) plus the U_P phase term set a floor ≥ ~10⁻³.
  Held-out: the floor's size and which arm reaches it.
- **P2 (genesis train = half the spread).** Half-mass window of the g=0 dues ≈ 0.5 × step
  spread; at the shipped [2,3) draw the concentration (0.5·median_step / half-mass window)
  lands within a factor 2 of f82a/3294's 57× (their belt: same draw, interval 28,141.5 s,
  50% of fires in 0.9% of the interval). Held-out: the exact numbers.
- **P3 (the rule: lifetime ≈ train width / step spread).** The train's half-mass width grows
  ≈ W(g) = W0 + g·σ_step (shearing); the frame comb (dues max/mean over the step span) falls
  below 2× after L ≈ W0/σ_step fires. At the shipped draw L ≈ 3–5 (8ffc's "shearing past ~5
  intervals"); each 10× narrower draw multiplies L by ~10; the narrowest arm (σ at the P1
  floor) still decorrelates within the 8 measured generations. Held-out: the shear constant
  (does width grow as g·σ_step or g·σ_step/√12 etc.) and L per arm.
- **P4 (quantized classes sit on the combing side).** With shared exact (a,e), bodies of a
  class share y to within the U_P phase term (~10⁻⁵ relative), so their fires stay within
  ~sub-frame offsets of each other at genesis; the frame-level comb (max/mean over span)
  stays ≥ 5× at g = 8 (vs < 2× for every continuous arm), and exact-tick battalions of size
  ≈ N/(classes·e_levels) persist or re-form at adjacent-frame offsets. The alternative
  outcome — differential drift shearing classes apart within ≤ 2 generations — would refute
  the page's last comb premise instead (the chained clock would then self-heal even a
  quantized belt). Either way direction 4 closes.
- **P5 (controls).** The refactor control: plane_belt with the shipped ([2,3), σ70,
  continuous) options reproduces plane_extra's population bit-identically (same G0 census at
  N = 3,000). Planets/moon/locals stay exactly on the `aligned` grid in every arm, before
  and after settle. Dues per frame of the shipped arm at g = 3 match b4a8's record (mean
  1.64 over support; max ~17) up to the horizon difference.

Kill criteria: P5's refactor control failing kills the instrument (report as such). P3
failing with width(g) non-linear in g (e.g. stuck) or P4's classes shearing to Poisson in
≤ 2 generations each close direction 4 the other way — measured, not a failure of the run.
