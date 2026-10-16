# Predictions (written before the decisive grid)

The run: checker 2's named gold experiment on 20261016-0213-system-d31c — "serve `plan_clock`'s two
own-state `readout` calls from one read, same instrument and digest bar; a further ≥ 1.5×
digest-identical cut crosses the bar." Built as one lever family: the pass's per-body recomputations
of quantities that are shared (`ES_STATE_ONCE`: one own-state read serves the register's word, the
projection and the tail, and the projection's Kepler energy is reused — the shipped path solves the
same `H_D` twice at the same state; `ES_CONSTANTS_ONCE`: every non-source body of a doll recomputes
the identical per-doll `(Δs, c, b)` Hill sum, now served from d31c's table). Plus d31c's checker's
latent catch: `PlanetsAt::build` now refuses to arm if any live read errs (the memo never converts an
error into a shorter answer). Arms: `off` (shipped verbatim), `on` (d31c's planets memo),
`state` (on + ES_STATE_ONCE), `full` (on + both), one `stateonly` cell (ES_STATE_ONCE without the
planets memo). Instrument: d31c's `ES_BIRTH_SPLIT` timers + two integer counters I add
(`readout_calls_per`, `const_hits_per`).

Cases tuned on: none beyond the shakeout cell N=10⁴ seed 1 (build-error check only; its numbers are
in the run log). Every number below is a prediction about cells not yet measured.

- **P1 (the full cut):** the `full` pass lands **10.0–13.0 µs/body** at every cell of the grid
  (10⁴/3×10⁴/10⁵ × seeds 1/7/11), i.e. ON→full ≥ 1.85× and shipped→full ~2.6–3.2×. Kill: if the
  full pass exceeds **15.1 µs/body at a majority of cells** (ON/full < 1.5×), the family misses
  checker 2's bar and the pass's floor is elsewhere.
- **P2 (the named lever alone):** the `state` arm lands **14.5–17.0 µs/body** — ON/state ≈
  **1.4–1.55×**, and I predict it does NOT clear 1.5× at most cells: the readout measures
  3.4–3.8 µs/call, only two duplicate calls and one Kepler solve are deletable, and the Fermi sum
  (~7 µs/body of ON's 18.5 replan) bounds the arm at ~15–16.
- **P3 (integers):** `readout_calls_per` = 2.85–2.95 on off/on (3 per clock body; ~3% of bodies are
  not clock bodies) and 0.95–0.98 on state/full; `const_hits_per` = 0.95–0.98 on full and 0.00
  everywhere else. Any deviation means a plan path I have not accounted for.
- **P4 (identity):** digests are **bit-identical across all arms at all seven flights**, equal to
  d31c's recorded per-(N, seed) digests; the universe crate's suite is green with every knob on
  and with each knob alone.
- **P5 (flat in N):** the full pass is flat in N (10⁴ → 10⁵ within ±15%), like the shipped pass.

Held out before the run: seed 11 at 10⁴ and 10⁵; 3×10⁴ seed 1 (d31c's held set); and the 10⁵ s7
full-arm cell.
