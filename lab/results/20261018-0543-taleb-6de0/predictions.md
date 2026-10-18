# Predictions — 20261018-0543-taleb-6de0 (written before the ensemble runs)

Question (wiki chaos-shadowing, open direction 3): the plane's μ = 1e-2 runaway tail —
a physical capture cascade (interval tracks a shrinking planetocentric orbital period,
cost bounded per local orbit) or an event storm (intervals collapse with no short period
behind them, cost per local orbit diverges)? The instrument: `crates/universe/src/bin/tail.rs`
(shipped plane through its public API, the behave scene, cap-bounded `advance`), per-kick
telemetry via `KICK_TRACE` (trace.rs, outcome-free). Ensemble: 144 ICs, circular
heliocentric orbits at a = sep + du·Hill, du ∈ [−1.5, +1.5] Hill (12), φ ∈ [60°, 180°]
(12). Screen: 4 P, cap 100k events. Deep trace: the worst grinders, 16 P, cap 1.5M.
Control: the same grid at μ = 1e-3, 64 P horizon (16× longer), cap 100k.

- **P1 (the grinders are captures).** Every capped IC's trace parks inside the planet's
  Hill sphere: min planetocentric distance < 0.3 R_H, and the kick interval during the
  grind scales with the planetocentric period P_sat(a_p) at the a_p the trace shows
  (dt/ds = f'(U_P + c) makes the interval a property of the state, ext.rs).
- **P2 (no event storm: cost per local orbit is bounded).** Kicks per planetocentric
  radial period stay within [0.25, 4]× 2^7 (the configured cadence, step_log2 = 7). No
  interval approaches MIN_STEP = 128 ticks unless the trace's own P_sat is comparably
  short. If instead intervals collapse while the planetocentric distance stays flat and
  long-period, the runaway is a law artifact and μ = 1e-2 is not flyable as built.
- **P3 (the tail is fat and μ-gated).** At μ = 1e-2, 4 P: at least one of 144 ICs is
  capped at 100k events, and the top IC holds ≥ 25% of all ensemble events. At μ = 1e-3,
  64 P (16× the horizon): zero caps, top IC ≤ 5% of events, median kicks/P ≈ 230-270
  (the wiki's 267/231 numbers — if this control fails, the instrument, not the law, is
  broken: VOID).
- **P4 (convexity then a rate jump, not divergence).** A grinder's cumulative events vs
  horizon accelerate up to its capture epoch, then grow linearly with slope
  ≈ 128·P/P_sat(a_p) kicks per planet period — a rate jump of 10²-10³× the belt rate,
  constant per local orbit. Cost per unit time is what the allocator cannot afford, not
  cost per orbit.
- **P5 (held-out cases, not tuned).** (a) Deaths inside 4 P exist at μ = 1e-2 (the wiki's
  8/144 burst: planet_kill at the first conjunctions) and they are the ICs with the
  smallest |du| (deepest co-orbital). (b) No μ = 1e-3 IC enters the Hill sphere at all in
  64 P (the layer is thin); any that does sits at |du| ≤ 0.5 R_H near the horseshoe
  turnaround (φ near 180°). (c) Traced captures do not escape within 16 P (temporary
  capture at μ = 1e-2 lasts far longer than our horizon) — so the capped cost is a
  permanent state of the ship, not a burst.

What would make each wrong, and why it matters, is in dossier.md's "what would make it
wrong". A P2 failure in the storm direction is the only outcome that kills a
configuration (μ = 1e-2 as a flyable plane mass); everything else prices the allocator.
