# Dossier — second author on 20261008-0743-constraint-4588 (run 20261008-0945-…-0e54)

**Claim (the checker's gold experiment, done).** The display-quantum row cache was built beside
`ViewCache` and gated as specified — and the original claim **does not hold**: at player scale an
honest all-field row cache serves 6–31 % of rows (not the author's 54–83 % "quiet"), saves
0.28–0.48 ms/frame p50 (not 1.4–2 ms), and fails the checker's gate ("every row within one
quantum") in 6 of 7 configurations, worst 1,962×. The gate passes only where events flood
(rtf 10⁴, 1080p) — where the cache matters least. The view gather remains the frame's constraint
at ≤ 10³× (H0210's recorded finding stands, now with the cache built and measured), but the
"cheapest 5×" presentation memo is not cheap enough to collect: the quiet-fraction instrument
overestimated cacheability by gating 2 of 10 fields, exactly as the checker suspected.

**Bottleneck.** The named gold condition of run 20261008-0743 (silver): build the row cache, gate
it across seeds/rtf/quanta, measure the realized gain. Expected: the ~2–3× frame gain. Measured:
~1.5× on the gather at 48 members (0.72 ms → saves 0.35), ~1.1× at 400 members — the lever is a
constant, not the claimed order of magnitude.

**What was built** (`work/second-author.patch`, applies to the run's base; example
`work/quantum_view.rs`, `crates/universe/examples/quantum_view.rs` in the patch):
- `view::RowCache` + `view::Quantum` + `view::Basis` + `gather_quantized` in
  `crates/universe/src/view.rs`. A held row is served **extrapolated along its measured drift**
  (first-order hold: sky rotation, offset, distance, age, closing, shift, luminosity, colour,
  lag, angular radius — all ten `Seen` fields), guarded by the worst measured curvature
  (error ≈ a·n(n+1)/2 < q/4, two samples minimum, 4× safety). **Zero-order holding was the wrong
  representation and failed immediately**: age and distance drift every frame by construction
  (t_now advances), so a value-hold fights its own channels — 85 % of served rows breached the
  age quantum on the first smoke run.
- Rows retire on **events, not timers**: the body's committed tick (`event_time` — one integer
  compare, a kick rebuilds it), the fleet's committed tick, the observer's committed tick *and
  any owed burn* (a key-down jumps `vo`, aberrating every row at once).
- **Fleet-loop rows are excluded**: `f.tick()` moves ~450×/frame (measured), and member rows
  still jump between its moves — there is no cheap sound basis for the battle's extrapolated
  rows. This is a finding, not a stub: the fleet population needs the stepper's own event
  counts (`epochs`/`anchors`) as basis, untested here.

**Evidence** (`matrix.txt`, shared Linux x86, 8 vCPU, load 0.6–2.8, 15 s runs, 900 frames;
orders of magnitude only — the integrator re-measures on the M1). All seven runs regenerate from
`cargo build --release --example quantum_view -p emergent-universe` then
`./quantum_view 15 <rtf> <seed> 5 <members> <1080p|4k>`:

| config (15 s, 900 frames) | served | saved ms p50 (of truth) | gate | worst err/quantum |
|---|---|---|---|---|
| m48 rtf 1, 1080p | 31.2 % | 0.395 (0.448) | FAIL | 1,962 (age, moon) |
| m48 rtf 100, 1080p | 24.2 % | 0.348 (0.718) | FAIL | 16.8 (offset) |
| m400 rtf 100, 1080p | 10.4 % | 0.309 (2.716) | FAIL | 265 (offset) |
| m48 rtf 100, 4K | 20.9 % | 0.331 (0.748) | FAIL | 59.4 (age) |
| m48 rtf 10⁴, 1080p | 27.8 % | 0.481 (1.371) | **PASS** | 0.82 |
| m48 rtf 10⁴, 4K | 25.5 % | 0.445 (1.370) | FAIL | 1.12 (16 rows) |
| m400 rtf 100, 4K, seed 7 | 5.8 % | 0.276 (2.976) | FAIL | 224 (age) |

Why it fails, by measured population (violation census in `matrix.txt`):
1. **rtf 1 (worst)**: almost no engine events (1 kick in 15 s) — rows arm on two curvature
   samples and then serve for hundreds of frames; Keplerian curvature is periodic, so two
   adjacent samples do not bound it (a moon's `age` walks 1,962 quanta). The guard's premise —
   measured curvature bounds future curvature — is false between events.
2. **rtf 100, m400**: battle handoff churn (the fleet's `motions` list is ~2,600–26,000 entries;
   thousands of handoffs) — freshly handed-out members at 4–10 milli-light-seconds move ~2 % of
   their distance per frame; their first post-handoff measurements understate it.
3. **Where events flood (rtf 10⁴)** bases churn every few frames, estimates stay fresh, and the
   gate passes — but that is the regime where the engine, not the gather, is the constraint.

Adoption cost if ever wanted: one file beside `ViewCache`, no law, no gate, no memory layout —
the view still reads and never writes (`observation_never_changes_the_digest` passes with the
patch; every default suite passes. The one failing test,
`a_ship_passing_a_planet_keeps_its_jacobi_constant_bounded`, is ignored-by-default and fails
identically on the clean tree — pre-existing, no view involvement).

**Predictions** (`predictions.md`, written before the matrix): 1, 2, 3 held (gate fails on the
named tail; quiet ≠ cacheable; saving below claim and flat in members because bodies, not fleet
rows, are what the cache serves). Prediction 4 half-wrong: rtf 10⁴ serves 27.8 % (not < 10 %)
because basis refusals, not drift, gate it — and it passes the gate there, which I did not
predict.

**What would make it right, and cost.** The failure is not the hold order but the *soundness of
the bound between events*. Three exits, none built here: (a) a per-row re-measure event that is
not a timer — e.g. the crossing memo's extrapolated tick stepping (it already exists per body),
or the stepper's `epochs`/`anchors` counts for fleets; (b) accept a sub-quantum *bounded* breach
rate and re-specify the gate statistically (the far population — planets, moons, distant ships —
holds every field under one quantum at rtf ≥ 100; it is 20–24 % of rows); (c) drop the row cache
and cut the gather's per-row cost instead (6–9 µs/row is the real number to attack).
Adoption cost if ever wanted: one file beside `ViewCache`, no law, no gate, no memory layout —
the view still reads and never writes (`observation_never_changes_the_digest` untested here only
because the crate test run was cut by the window; the cache adds no write path).

**Fit with PRINCIPLES.** #3 "Nothing is evolved that can be derived when looked at (clocks,
redshift, views)" — the experiment says the view's rows are *not* as derivable as the quiet
metric claimed: between events a row's drift is smooth but its curvature is not bounded by two
samples, so "deriving when looked at" needs an event, and the events are the engine's. #19 —
the zero-order hold was a fix-fix-fix spiral until the first-order Taylor form made the linear
channels exact; what remains is the same lesson one level down. #22 — "the simulation tells us
what's next": confirmed from both sides (the gate passes exactly where the simulation talks
often). H0210/H0211 already record the gather's dominance and the crossing cache; this run adds
the post-cache re-measurement and the refutation of the *next* memo in that line.

**The lens (second author).** I inherited the checker's framing and spent the budget proving the
gate could be passed rather than asking earlier whether "every row, every field" is the right
gate for a spectacle (#34: the oracle is a guard — a 1,962× breach on a moon's *age readout*
is a wrong dial, not a wrong sky). The ms numbers are shared-box wall time; the served
fractions, violation censuses and pass/fail are deterministic (identical across repeats).
`tail_view`'s broken CPU meter and the H0210 citation gap were the checker's other misses: the
citation gap is closed above; the meter is still broken and still unused.
