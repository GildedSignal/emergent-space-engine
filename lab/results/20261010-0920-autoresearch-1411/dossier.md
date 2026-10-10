# Dossier — run 20261010-0920-autoresearch-1411 (lens: autoresearch)

**Claim.** The contacts engine's per-op cost (`crates/lattice-event`, `EventCore`) is cut 15% on class-frame-heavy worlds and ~5% on dense-contact worlds by replacing two i128 software divisions per tracked frame (`entry_time`) and per prediction (`law::first_wall`) with a bounds-guarded i64 hardware division — bit-identical world/log digests everywhere, all tests green — while the obvious suspect (i128 arithmetic in the exact pair predicates `hit`/`first_hit`) measurably carries **nothing** (a checked i64 fast path was a wash and was reverted).

**Bottleneck.** Board #4/#12 territory (cost per event must not grow; smoothness): `ops/fired` is the engine's cost-per-event contract. Profiling (temporary rdtsc instrumentation, reverted): predict upkeep 55–59% + gather/scan 27–30% of wall time; within a prediction, the 3×3-cell scan (`around`+visits+predicates) is 82–84%; the calendar is 3–9%. The 10×-class lever (per-pair "cannot hit before T" certificates deleting most of the ~20 neighbour visits per prediction) is named below but was out of reach in one hour; this run takes the measured local win.

**Evidence** (Linux x86, 8 vCPU shared runner — orders of magnitude only; the integrator re-measures on the M1):
- Baseline vs final, interleaved A/B (pinned core, 3–5 alternations, median-of-3 reps each; ns/op):
  - `crowded_axes` 20k (8 co-moving class frames, zero events): 42.7 → 36.2 (**−15.3%**, min-of-alternations; every kept run beat every baseline run)
  - `gas` 20k fill 0.02: 43.6 → 40.7 (−6.5%)
  - `random` 20k Pass: 52.4 → 50.9 (−2.9%)
  - `gas` 20k fill 0.10: 45.6 → 45.3 (0%, inside noise)
- Held-out (see `predictions.md`, never tuned on): `h-crowded` 8k: 39.0 → 33.2 (−15%, all 4 alternations); `h-mixed` 8192: 42.6 → 40.7 (−4.6%); `h-gas-mid`/`h-gas-hot`: inside noise.
- **Digests:** all 4 tuning and all 4 held-out world+log digests bit-identical to baseline.
- Tests: `cargo test --release -p emergent-lattice -p emergent-lattice-event` — 38 passed, 0 failed (includes EventCore≡Chronon bit-equality).

Reproduce (≤ 60 s each):
```
cargo build --release -p emergent-lattice-event --example bench
$CARGO_TARGET_DIR/release/examples/bench            # tuning worlds, digests + ns/op
$CARGO_TARGET_DIR/release/examples/bench --heldout  # held-out set
```
Patch: `work/patch.diff` (law.rs `floor_div`+`first_wall`, lattice-event `floor_div`+`entry_time`), bench harness `work/bench.rs` (new `examples/bench.rs`).

**Predictions** (`predictions.md`, written before the decisive runs): "upkeep+scan ≥ 80%, rebuild ≤ 5%" **held** (83–86%, 2–3%). "i64 fast path for `hit`/`first_hit` gains ≥ 15%" **failed** (0–2%, wash; reverted) — the mechanism was plausible (7.6M predicate calls in gas-dense) but LLVM already compiles small-operand i128 multiplies to a few i64 ops; the miss cost is cache lines, not arithmetic. Held-out expectations (crowded ≥ tuning crowded's gain; mixed smaller; digests identical) all held.

**What would make it wrong.** A world where `entry_time`'s operands overflow i64: the guard (`i64::try_from` both operands, else exact i128) keeps exactness, only the speed reverts to today's. Nothing else can change behaviour: division results are identical by construction, verified by digests and the mode-equality tests. Cost of adopting: ~20 lines, no new state, no contract change.

**Fit with PRINCIPLES.** #1 "the cheapest compute is compute not done … make compute cheap"; #16 "what's cheapest to compute"; #26 "keep doing those smarter math and old tricks" — hardware `div` over software `__divti3`, the same fix `cross_time`'s comment already records ("an i128 division was a hot spot"): this run finished that sweep.

**The one idea that carried most of the gain.** One cheap measurement (rdtsc around `predict`'s inner loops) beat a day of plausible guesses: the exact predicates looked guilty and were innocent; a helper nobody profiles (`entry_time`, off the pair path) held 15%.

**The lens made me miss (blind spot).** A local search finds local optima: the structural change that beats this patch is deleting neighbour visits outright — per-pair "no hit before T" certificates (miss distance + closing speed bound the re-evaluation time), stored with the consumed-pair arena, so a re-prediction walks its 3×3 cells but skips most `first_hit` calls (98.4% return `None` in gas-dense). That is a law-adjacent change (it must preserve wake-up times exactly) and a rung of its own. Second miss: ns/op weights `random-pass`'s 44M ops most, hiding that event-heavy worlds gain least — a cost-model-driven report (`ops` mix per stage) would have shown the division fix's true audience (class frames, i.e. fleets) sooner.
