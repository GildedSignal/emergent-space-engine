# Predictions (written before the decisive runs)

Instrument: a print-only census on `Ctx::state_of` (opt-in via `ES_CENSUS=1`), keyed by
(call site, source j, tick t), recording call counts, distinct keys, bit-conflicts per key,
and the per-source field drift (max |Δpos| and relative drift across reads, f64 for
magnitude only). Digest identity: `ladder_digest "N=3000 coast through"` with the census
off vs on must print identical digests (the census writes nothing into the universe).

Cases not tuned on (the arms are the first runs of this instrument):

- **P1 (no exact sharing):** among `secondaries`-driven reads (ctx.rs:85) in the belt wave
  at N=10⁴ coast, distinct (j,t) keys ≈ calls: collision fraction (calls−distinct)/calls
  < 5%. Reason: TICK_SECONDS = 4.925e-6 s, so a ~1.5k game-s first-kick window spans
  ~3×10⁸ ticks and 9,700 kicks are ~all at distinct ticks (expected birthday collisions
  ≈ 9700²/2 / 3e8 ≈ 0.16 per source). If instead collisions are > 20%, a free exact memo
  is live and this run under-prices it.
- **P2 (no bit-conflicts):** keys seen more than once never return two different states
  (conflict count = 0): bindings only change at the source's own events and items are
  resolved in tick order, so an exact (j,t) memo would be bit-safe wherever it hits.
- **P3 (the drift is small but nonzero):** the sources' positions drift across the wave
  window by a relative 1e-6..1e-3 (the planets move ~v·W over W ≈ 1.5e3 game-s): large in
  absolute quanta, small relative to orbit scale — i.e. the shared field is *smooth*, so a
  canonical-tick read per comb is a bounded quantization, not a discontinuity. If the
  relative drift is > 1e-2 the field is not smooth at comb scale and sharing is a
  coarser law change than BELT_SPLIT's step class.
- **P4 (site split):** `secondaries` (ctx.rs:85) carries ≥ 50% of all state_of calls in
  the coast flight (read-stream's 3.0/body/event structure reproduced from the inside);
  the rest is the scheduler's post-event read, the clock step and the fleet path.
- **P5 (digest):** census on/off digests identical on `ladder_digest "N=3000 coast through"`
  (4 schedules × 2 runs).

Held-out for the checker (not measured by me): the same census on a burn flight (the
player's scan and the fleet path change the site mix), and at N=3×10⁴ (crest wider, same
structure expected).
