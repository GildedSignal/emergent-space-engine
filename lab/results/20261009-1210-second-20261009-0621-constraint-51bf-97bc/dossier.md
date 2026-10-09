# Dossier — the named lever built and measured: real, cheap, display-free — and not enough

**Claim.** The checker's gold experiment is done: the cheapest named lever (one shared read of a
doll's field sources per frame, `ES_SHARED_FIELD=1`, in `observe::partial` only) cuts the sources'
tube reads 11.9× (159.4 → 13.4 ms per 20 s unpaced, 92% of fetches reused) and the frame median
×1.16 (unpaced 0.972 → 0.840 ms), with the universe digest bit-identical at every setting, B16
passing and a measured display delta of 4.4 × 10⁻⁵ m — **and it does not meet the gold bar**: the
gather's share stays 0.62–0.63 against the engine's 0.21–0.30 at rtf 100, 1000 and seed 7, and the
frame median falls ×1.16, not ~3×. The original ranking survives its own lever: the constraint is
still the gather, now with the residual measured — 567 of 716 ms of the bodies loop is the crossing
search's own tube work outside `partial` (binding walks and per-level `cartesian` reads), a
representation term, not a scheduling one.

## Bottleneck

The board's #1 (fewer kicks) buys 21% of the frame; the gather holds ~63% *after* the cheapest
named fix. The lever's ceiling was readable before building it: the finer instrumentation shows the
sources' tube reads are 159.4 ms of an 890 ms bodies loop (the field block is 300.8 ms of partial
readouts: 53% sources' tubes, 10% field arithmetic, 37% the emitter's own reads). Deleting 92% of
the largest inner term cannot flip a 0.67-vs-0.21 ranking. What the experiment adds to the record:
the lever is validated (adoptable, display-free, digest-clean) **and insufficient** — the next term
is the per-readout chain walk itself, exactly the cell-held-field representation question
(PRINCIPLES 7) that the first run's lens named and no scheduler reaches.

## Evidence

Machine: GitHub Actions Linux runner, 8 vCPU, load 0.5–1.3 (co-tenant swings; paced p50 absolutes
moved 4.6 ↔ 1.5 ms between runs of the *same* binary — shares and unpaced walls are the robust
statistics, and every ns-level comparison is same-conditions back-to-back). Linux/x86: orders of
magnitude only. `X` = `$CARGO_TARGET_DIR/release/xtask` after `cargo build --release -p xtask`;
`R` = this folder. Patch: `work/lever.patch` = the first run's instrumentation plus the lever
(`git apply` on main).

1. **The record regenerates.** Stock main: digest `6ce636fa…`, cut 406050894, gather 0.669 /
   engine 0.201 (`stock-paced-r100.json`). Patched, lever off (`mode0-paced-r100.json`): digest
   identical; unpaced instrumented view digest `cb69811f…` = the author's bit for bit; bodies
   0.947–0.950 of the gather. Kick-bench (`kickbench-r100.json`): digest `c8ab26da…`, made median
   35.2 µs / leavers 91.6 µs, exact memo 0.0 with 926 fresh shapes, quantized 94.4924% — the
   author's numbers.
2. **Finer anatomy, lever off, unpaced** (`mode0-unpaced-r100-split.json`): bodies loop 890.1 ms;
   partial readouts 300.8 ms, of which sources' tubes 159.4 ms, field arithmetic 31.2 ms; 589 ms
   outside `partial`.
3. **The lever on** (`ES_SHARED_FIELD=1`): digest `6ce636fa…` identical, paced and unpaced, and at
   rtf 1000 (`99d27789` both modes) and seed 7 (`b338329d` both modes). Sources' tubes 159.4 →
   13.4 ms (11.9×), first touches 1199 ≈ one doll per frame (every partial step in the scene sits
   in one doll), reuses 13192 (92%). Bodies 890.1 → 716.4 ms (−19.5%); frame p50 (uninstrumented,
   unpaced, back-to-back) 0.972 → 0.840 ms, wall 1.42 → 1.26 s; gather share 0.674 → 0.634,
   engine 0.203 → 0.227. rtf 1000: gather 0.676 → 0.628 vs engine 0.26 → 0.298; seed 7: 0.652 →
   0.609 vs 0.224 → 0.251. **No inversion anywhere; the bar's "gather below engine" fails by ~2.5×.**
4. **Display safety.** Mode 2 (`ES_SHARED_FIELD=2`: the canonical per-step read drives the view,
   the shared one is only compared — fixed after the first version compared shared-with-shared)
   measures, per stepped readout, max Δposition 2.98 × 10⁻⁸ root units ≈ 44 µm and max Δvelocity
   1.2 × 10⁻¹⁶ doll units, against a read-tick spread of 1.53 × 10⁸ ticks (~754 s of retarded
   time): the partial step's τ² kills the source-motion error (`mode2-unpaced-r100-split.json`).
   B16 PASS, 256/256 seeds, worst 6.93 × 10⁻⁸ (`b16.txt`). View tests 5/5. The per-frame view
   digest is load-sensitive through the engine budget's presented ticks (the checker's own
   caveat), so the equality control is the cut digest plus the bit-level delta above.

Commands, each ≤ 60 s: `X universe --bench --rtf 100 --seconds 20 [--unpaced] [--seed 7]`,
prefixed with `ES_SHARED_FIELD=0|1|2` and optionally `ES_VIEW_SPLIT=1`; `X universe --kick-bench
--rtf 100 --seconds 20`; `X behave --gates B16`.

## Predictions

`predictions.md` was written after the reproduction runs and before the lever runs. All four held:
digests identical (1); ≥ 80% reuse, ≥ 80% sources-ns cut — 92% and 91.6% (2); the gold bar NOT met,
bodies −19.5%, frame ≤ 1.3× (measured ×1.16), gather share ≥ 0.58 (measured 0.63) (3); Δp ≤ 1 root
unit (measured 2 × 10⁻⁸), Δv ≤ 10⁻⁶ (measured 10⁻¹⁶), spread 10⁷–10⁸ ticks (measured 1.5 × 10⁸),
B16 pass (4).

## What would make it wrong

The lever shares across a 754 s retarded-time spread because the scene concentrates all partial
steps in one doll; a scene with emitters deep in several dolls would shrink the spread (more
first touches, less reuse) but also the win — the direction survives, the 12× would not. The frame
p50s carry the machine's co-tenant noise (±3× on paced absolutes); the refutation does not rest on
them but on the share ranking and the ns-level split, both load-robust. If `partial` ever fed an
outcome (it does not: the engine's kicks read their own sources in `step.rs`, and every digest
control says so), the digest equality would break — that control is the guard, and it held at
three settings.

## Cost of adopting, and fit

The lever itself is adoptable today: env-gated in this run, but the change is ~60 lines
(`shared_secondaries` in `view.rs`, the `sources` closure in `observe::partial`), view-path only,
no cache-semantics change, no budget machinery. It buys 12× on the term it targets and ×1.16 on
the frame. What the experiment really prices: **the gather's remaining 0.62 is not reachable by
read-sharing** — 567 ms of the 716 ms bodies loop is the chain walk and per-level tube evaluations
that exist to make reads second order. PRINCIPLES: "Nothing is evolved that can be derived when
looked at (clocks, redshift, views)" and 7 ("gravity compiled into geometry held by cells, not a
per-read recomputation") name the next move: the field as a cell-held quantity and the readout
chain amortised, before any stagger work.

## The lens

The second author's lens trusts the checker's bar and the digest controls, and it got one thing
wrong on the way (mode 2 comparing shared-with-shared, caught because a zero delta with a 10⁸-tick
spread is impossible). What it may miss: the "one doll per frame" concentration makes this scene
flatter-cheap; a fleet scene (many dolls, many partial steps) would both cost more and dedup less,
and I did not build one. The 44 µm delta is measured on stepped readouts, not on the final
crossing tick the player sees — the crossing could shift a tick where the root sits within the
delta of a boundary, unmeasured here.

