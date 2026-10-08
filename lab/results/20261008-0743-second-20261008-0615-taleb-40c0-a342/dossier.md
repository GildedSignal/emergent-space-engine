# Dossier — run 20261008-0743-second-20261008-0615-taleb-40c0-a342 (lens: second author on 20261008-0615-taleb-40c0)

## Claim

Check2's named experiment for gold is done and held: with the fix shipped — the live loop logs a
key change at its frame's *scheduled* game time quantized up to a decision quantum
(`Universe::input_frame`, 0.25 s wall; `session.rs` and `kick_bench.rs` call it) — the same
physical play writes **one digest per seed across play60/play30/play144/play60-starve at rtf 100
and at rtf 1** (logged ticks, encounters, contacts identical too), the load-only ruin form and the
thread axis are gone (`play60-starve` thr8 = thr1), the 54-run core matrix regenerates
byte-identical, and the equality is wired as a 12 s regression test
(`crates/universe/tests/decision_tick.rs`). The original claim (core schedule-independent; the
shipped loop leaked schedule into the canon at `session.rs:80`) stands, and its one-line fix
direction is now the shipped, tested behavior.

## Bottleneck

Not a compute lever: closing the one named ruin path (AGENTS.md Truth: "Canonical outcomes are
exact and independent of cache, partition, observation, schedule and hardware"). Check2 graded
the run silver solely because the fix was "a proposal": "the gold clause 'can be adopted within
one step' is unproven until the two-line change exists and holds." This run is that step. What it
deletes: the wall as a second wildcard on the played path, and the bench's wall-derived digests
(`kick_bench.rs` shared the seam, so its A/B comparisons across machines compared different
histories).

## Evidence

Machine: Linux x86, 8 vCPU, load 1.9–5.1 during the suite, 15 GB RAM (state.txt); every run
< 100 MB, ≤ 8 s. Everything below regenerates from `work/patch.diff` applied to a clean tree,
built `CARGO_TARGET_DIR=/tmp/x-target cargo build --release -p emergent-universe --bin
determinism`; the records are in `work/` (driver: `work/run-all.sh`, 229 s total).

**1. The named experiment (`work/play-rtf100.txt`, `work/play-rtf1.txt`; 24 runs).** Fixed key
timeline (wall 0.5 s, 1.7 s, 3.2 s), cut 80 M ticks, seeds 11/22/33:

| pace | seed 11 | seed 22 | seed 33 |
|---|---|---|---|
| rtf 100 (all four paths) | `e1da531e…` | `5b7583ba…` | `2e3fe224…` |
| rtf 1 (all four paths) | `8f0b9da5…` | `0dcdf641…` | `bff01384…` |

One digest per seed per pace; the logged ticks are identical across paths — `[10151272,
35529452, 65983268]` at rtf 100, `[101512, 355292, 659828]` at rtf 1 (the decision-quantum
multiples; ticks printed in every line) — and so are encounters/contacts/decisions/refused
(e.g. rtf 100 seed 11: 104/6/3/0 on all four; the raw seam spans 44–115 encounters and 0–14
contacts across its 12 runs).
Reproduce: `for seed in 11 22 33; do for case in play60 play30 play144 play60-starve; do
/tmp/x-target/release/determinism $case $seed 1 1024 80000000 100; …same with trailing arg 1…;
done; done`.

**2. The ruin form and the thread axis close (`work/thr8.txt`).** `play60-starve` thr8 = thr1
(seed 11 `e1da531e…`, seed 22 `5b7583ba…`): same fps, different load and thread count, one
history. Under the old path these split (`f7e17f7e…` vs the rich-path digest; check1's extra
axis).

**3. The core matrix is untouched (`work/matrix.txt` vs `work/matrix-orig.txt`).** All 54 lines
regenerate byte-identical modulo `wall_ms` and the thr8 tag's position (its digest/counters
match). The three `wall` lines diverged *while the suite ran under load 5*: this machine starved
the 0.2 ms budget to zero events, the probe's `events==0` break fired early, and `now` was forced
to the cut over unresolved state — a harness break-condition flaw, not the engine and not the
patch: rerun quiet (`work/wall-quiet.txt`), all three reproduce the original digests exactly
(`9dbf38e4…`, `9001b877…`, `ff0ff6d7…`, events 12082/11716/12141). Noted for future probes: a
wall-budget loop needs `advance`'s done-flag, not `events == 0`.

**4. The leak stays reproducible from this patch alone (`work/play-raw-rtf100.txt`).** The
`-raw` suffix keeps the old presented-tick log: 12/12 lines split per path, and the unfixed
digests match the original run's stored record (seed 11: `047817bb`/`53271800`/`7f84c5ac`/
`f7e17f7e`) — the before/after pair lives in one patch.

**5. Control and regression.** `fixed-input` = `direct` at 80 M for all seeds
(`49a1b20b…`/`264b1bee…`/`9fbcaa5f…`, `work/control.txt`) — the eager path is untouched.
`cargo test --release -p emergent-universe --test decision_tick`: 2 tests, pass in 12.4 s —
five paths (30/60/144 Hz, starved, starved-thr8) assert one digest + pinned ticks at rtf 100,
and the load-only pair at rtf 1 with pinned ticks. The workspace builds clean (xtask included).

**6. The honest boundary, measured (`work/play260.txt`).** A first key change at 0.26 s wall
(rtf 100) straddles a quantum boundary: 60 Hz and 30 Hz log tick 5 075 636, 144 Hz logs
10 151 272 — digests split, exactly as pre-registered. No function of a frame's sampling can
recover the continuum between two frame rates; the quantum is the declared price (≤ 0.25 s
timing ambiguity, under deliberate human timing; expected ambiguity ≈ sampling spread/quantum ≈
13 ms/250 ms ≈ 5% of key changes across frame *rates*). Same-cadence equality — load, budget,
threads, the ruin form — is exact.

## Predictions

`predictions.md` was written before the runs (one arithmetic correction inside it, made before
any run and marked). All seven held: P1 rtf-100 equality (one digest per seed, ticks equal), P2
rtf-1 equality, P3 matrix byte-identical (with the load-starved `wall` harness flaw diagnosed and
regenerated quiet), P4 control unchanged, P5 thr8 closes, P6 the 0.26 s straddle splits as
predicted, P7 the raw seam persists with the original digests.

## What would make it wrong

The probe idealizes frame cadence (exact `dt` per fps); the shipped page passes measured wall dt
(`http.rs:95`), so `sched` itself is wall-integrated there and frame jitter can move a decision
across a quantum boundary run-to-run on a real browser loop — unmeasured here (no browser), the
same order of ambiguity as the fps straddle, and removable the same way (derive `sched` from a
declared nominal cadence × frame count if the page ever needs it). The quantum constant (0.25 s)
is a judgement call, not derived; `rtf` changes mid-flight (`[` `]`) are still not logged, a
pre-existing replay seam. x86 only, one machine, 3 seeds, `Order::Sparse`, 1024 members. If the
integrator judges cross-frame-rate exactness required for *all* key timings, no finite quantum
gives it — that is an information bound, not a fixable bug, and the dossier says so with the
measurement.

## Cost of adoption, fit with PRINCIPLES

The patch: `sched` (one field, one line in `frame_to`), `DECISION_QUANTUM_SECONDS` +
`decision_quantum` + `input_frame` (~20 lines with docs) in `universe.rs`, the two glue
callsites, the probe, the test. No core path touched (the matrix proves it). The bench's
absolute numbers shift (its input ticks move to the quantum grid) — its comparisons become
same-history, which was the point. Fit: "Canonical outcomes are exact and independent of cache,
partition, observation, schedule and hardware" — restored at the played seam; law.md "Ties": "A
player's decision takes effect at the canonical tick written in the input log, never at a
wall-derived one" — the log is now written on the game's clock. #5 the player stays the only
wildcard; #13 a flipped contact no longer compounds from machine load; #21 the fix is the
two-line shape the original dossier drew, now measured.

## The lens

The second-author lens risked tuning to the checker's named cases and calling it done; the
pre-registered straddle case (P6) exists to keep the claim honest about what the fix cannot do.
What it may have missed: no run at other member counts or scenes (the seam is scene-independent
in mechanism, but only 1024/Sparse was run); no measurement of the real page's jitter (idealized
cadence); and it inherited the original probe's `wall`-case flaw silently until load exposed it —
worth a line in the harness, not the engine.
