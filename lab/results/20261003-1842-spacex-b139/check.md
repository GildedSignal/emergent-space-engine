Grade: silver

The plane's per-kick `Rebinding::from_state` recompiles the orbit quadrature although 99.8% of compiles rebuild one of 24 shapes; routing the Cycle branch through `crates/space`'s existing `ShapeMemo` deletes them at bit-identical digests and cuts the kick ~12–16% (my reproduction: 26.9→23.4 µs median, seed 7; seed 1 the same). The measured stage table (kick ≈ 98% bookkeeping, idiot index ≈ 40×) is the real product and names the next levers (incremental fit_key, one decode per bind, secondaries tube memo). Cost to adopt: ~15 lines plus dropping lab instrumentation; all space (50) and universe tests pass. My adversarial probe sharpened the found impurity: at exactly compactness 1/6 `ShapeMemo` does not refuse but silently returns a different orbit than `Orbit::compile` — the latent gap in `events/records.rs` is worse than reported.

## Reproduced (clean tree, `git apply work/patch.diff`)

- `kick_stages 10`: 13,801 `from_state` calls, all Cycle, 0 passages; **24 distinct shape keys, hit rate 0.998**; replay digest `8f353a2b…74f73bb` and universe digest `cb815b7e…d44d4ebb8` — exactly the baseline digests recorded in `predictions.md`. (This run is the control arm: without `ab`, `MEMO_ON` stays false.)
- `kick_stages 10 ab` (interleaved, one process): identical digests to the control-only run → **bit-identity across memo/control arms proven in-process**. Control 26.93 vs memo 23.65 µs median (−12%), p99 37.56 vs 32.40. Stage shares match the table: secondaries 33%, bind 53%, force+h·dv+quantize ≈ 0.6 µs ≈ 2% → idiot index ≈ 49× on this box.
- `kick_stages 10 ab 7` (held-out seed): hit rate 0.998, 24 distinct; control 26.69 vs memo 23.41 (−12%). Seed-7 digests (`4beed0e9…`, `33ae7f6b…`) appear nowhere in `predictions.md` — genuinely held out. I also ran seed 7 control-only: digests identical to its A/B run.
- `cargo test --release -p emergent-space`: all 50 tests pass, including `exact_parabolic_and_unstable_circle_ties_are_generators`. `cargo test --release -p emergent-universe`: all pass on three serial reruns. (One first-run background execution under full load reported 1 failed in one target; my grep had filtered test names, and three serial reruns are clean — unreproduced, attributed to shared-box load, consistent with the patch being a content-identical cache.)
- Absolute timings are higher than the author's (27 vs 22.5 µs median) — shared 2-vCPU box; orders of magnitude and the A/B ratio are what transfer, as the dossier itself says.

## Predictions

`predictions.md` mtime 18:50:56 vs dossier 19:01:48; the tuned-on section records only seed-1 numbers and baseline digests, and every held-out item (digests identical, seed-7 hit rate ≥ 0.95, ~19 µs not 10×, tests pass, passages unhelped — 0 bound here, tens of shapes) held. One promised held-out case, the **order** (prediction 2, "held-out order (not run yet)"), never ran and is not reported — quietly dropped, not failed.

## Attack

- **Adversarial probe (new test, deleted after):** `ShapeMemo::get` vs `Orbit::compile` on exactly circular keys (`k = 1<<48`): r=4 (q=0.25) and r=5 (q=0.20) — compile succeeds, memo refuses `NoBoundOrbit`, confirming the impurity. At **r=6, q=1/6 exactly, both succeed with different content**: compile's symbolic circle has `advance() = 0`, the memo's generic shape has `advance() ≠ 0`. So the memo is not equivalent even where it does not refuse; the patch's pass-through for all `k == UNIT` is necessary, not merely conservative. This also sharpens the integrator note: the same `ShapeMemo` in `events/records.rs` can silently bind a different orbit at the q=1/6 boundary, not just refuse.
- Cap (4096, clear-on-exceed): code-read, single thread-local, bounded; correct.
- Threads: memo is thread-local, `MEMO_ON` a global atomic; content equivalence plus the passing digest-across-budgets-and-threads test cover determinism. The perf claim is only measured single-threaded (the plane resolves single-threaded today — honest seam note in the dossier).

## Novelty

The cycle memo keyed by quantized (E, L) is the law's own design (`docs/law.md` line 14: "shared by every tube with the same key"), and `ShapeMemo` already exists (events store `records.rs`, tests `envelope.rs`). What is new: the measurement that the plane's kick path bypassed it (13,801 compiles → 24 shapes), the A/B proof, the stage table, and the impurity find. H0210 queues "kick cost (Sol)" as next with kicks at 29 µs; no prior entry memoizes the kick's compile. Not already done; the concept's pedigree makes adoption cheap.

## Goal fit

Board focus #1 ("kicks dominate the engine's cost"), H0210 limitation "kicks cost 29 µs". PRINCIPLES §6: "Store the generator, not the generated" — the generator was being regenerated per kick; §1: "Delete before optimizing." Respected: the deletion is content-identical, bounded, and reversible; gates are untouched.

## Why silver, not gold

Reproduced and honest, but it moves the kick ~1.2×, not 10×, and deletes no engine component (one stage of one operation). The impurity find is a wrong premise in `ShapeMemo`, but no downstream failure through `records.rs` is demonstrated — a flagged latent gap, not a killed configuration.

**The one experiment:** land levers 1–3 (incremental integer fit_key, one trajectory decode per bind, per-doll secondaries memo) in the same interleaved A/B and show ≥3× on the kick; or demonstrate a concrete wrong binding through the events store's unstable-circle path, which upgrades the impurity to a demonstrated wrong premise.

## What the author missed

1. The silent divergence at exactly q=1/6 (reported as refusal only) — the boundary case their own pass-through guards against, and the sharpest form of the records.rs warning.
2. The held-out order promised in predictions.md was never run or reported.
3. "space's own api test already asserts memo.get ≡ Orbit::compile" overstates: `envelope.rs` asserts it only on keys that avoid the circular boundary, as my probe shows.
4. The stage-table absolute numbers include the lab instrumentation itself (five `Instant::now` plus a HashMap insert per `from_state`, both arms); the A/B delta is clean, the absolutes are slightly inflated — the idiot index is if anything understated.
5. No multithreaded or Dense-order measurement; the thread-local seam is argued, not measured.
