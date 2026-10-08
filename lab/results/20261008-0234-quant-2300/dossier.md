# Dossier — 20261008-0234-quant-2300 (Quant lens)

**Claim.** The shipped kick resolver is O(1) in universe size (no capacity cliff from 4 to 400 members), but its constant is ~90 µs per kick on this box, and 79–88% of every kick is the Kepler tube refit (`rebind`), while the force evaluation the design argues about is 1–2% — so the next 10× in "fewer/cheaper kicks" lives entirely in when tubes are refit, not in the force law.

**Bottleneck.** Board focus #1: "fewer kicks per orbit at the same behaviour (correctors, higher-order splits): kicks dominate the engine's cost." Nobody had measured where inside one kick the time goes. Budget arithmetic: 10⁹ bodies × 32 kicks/orbit (H0190) ÷ a ~year orbit (3.15×10⁷ s) ≈ 10³ kicks per game-second; at RTF 100 that is 10⁵ kicks per wall-second, which fully occupies one P-core at 10 µs/kick. Measured median 89–99 µs (leavers, the population that scales) ⇒ ~10× over a one-core budget at RTF 100, before the tail (p99 = 4.1× median) that the allocator must absorb. What it deletes: the argument space around kick *cadence and force cost* — both are <2% of the bill.

**Evidence** (Linux x86, i7-4790 @3.6 GHz shared, loadavg 1.4, 02:36–02:45 UTC; orders of magnitude only, M1 re-measure pending):

1. Capacity curve — median µs/kick, resolver-only replays (uninstrumented binary, `cap-m*.json`):
   | members | made median/p99 (n) | leavers median/p99 (n) |
   |---|---|---|
   | 4 | 38.4 / 70.0 (86) | 89.7 / 432.5 (54) |
   | 48 | 38.7 / 60.0 (86) | 95.1 / 413.0 (527) |
   | 400 | 39.0 / 66.2 (86) | 99.1 / 411.3 (4878) |
   Flat medians across a 100× member range: the resolver touches O(1) other bodies (its doll's sources are structural). No pre-registered kill (cliff = median growing >4×). The *mean* per kick grows 65→101 µs (m4→m400, stage counters over all resolved kicks): the tail lengthens with N, the median does not.
2. Stage attribution — instrumented `step.rs` (stage ns accumulators; replay digest unchanged: `8ee18ba4…` before and after instrumentation, `refused` 0), stable across members (`stages.txt`):
   - v1 split path (fleet members, planets; n = 284–9,843 kicks): **rebind (tube fit) 79.3–88.3%**, readout 3.8–6.4%, ctx reads (secondaries+tide) 6.7–12.5%, **force 1.0–1.9%**, sigma-delta 0.1–0.3%, ramp 0.1%.
   - v2 clock path (motion law v2, the player; n = 12 only): quantize+rebind+project 60.0–60.9%, ctx reads+surface ~25%, readout ~8%, force+time ~5%, planning 1.4%. Weak on sample count; shares consistent across runs.
3. Cache lines per event (counted via `size_of`, `sizes/`): Scalar 16 B, Secondary 96 B (fits one 128 B M1 line), Item 16 B, IntegerState 40 B, Binding 176 B, Trajectory 176 B, BodyRec 448 B (7 lines @64 B), Update 496 B. One kick touches its BodyRec + Arc<Entry> heap entry + a fresh `Vec<Secondary>` ⇒ ~8–15 lines/event, and one heap allocation per kick (`Ctx::secondaries`) — but memory is not the bill: the fit is ALU-bound exact dyadic arithmetic.

Reproduce (each ≤60 s, from the repo root with this run's patch applied):
```
cargo build --release -p xtask
for m in 4 48 400; do $CARGO_TARGET_DIR/release/xtask universe --kick-bench --seconds 6 --seed 7 --rtf 100 --members $m; done
(cd lab/results/20261008-0234-quant-2300/sizes && cargo run --release)
```
`perf` hardware counters were unavailable here (`perf_event_paranoid=4`); prediction P4 is withdrawn as unmeasured, not as confirmed.

**Predictions** (`predictions.md`, written before the decisive runs): P1 held (fit+readout >50%; the fit alone is 79–88%). P2 held (ctx reads incl. the Vec allocation 6.7–12.5%). P3 half-held: medians flat ✓, p99/median ≈ 4.2–5.3× at *every* member count — the tail is structural (some kicks refit passages/deeper work), not cache growth with N; the growing mean says the far tail (p99.9+) does lengthen with N. P4 unmeasured (no PMU access). P5 held: median ≥10 µs ⇒ one-core budget at RTF 100 already exceeded ~10×.

**What would make it wrong.** Shares measured on Haswell with `Instant`+relaxed-atomic instrumentation (≈0.5% overhead, digest-neutral); an M1 could reorder stages only if the fit were memory-bound — unlikely (exact ALU arithmetic, ~15 lines touched). The v2 split merges quantize+rebind+project into one stage, so the v2 "fit share" is not isolated. The tail's cause (passage fits vs. coarser-word re-binds vs. deep levels) is inferred, not split. A kick that skipped the refit would change *when readouts are exact* — that is a law change, judged by B13/B17, not by this latency number alone.

**Cost of adoption, fit with PRINCIPLES.** Measurement only: nothing to adopt, one design lever named. The lever (accumulate dv exactly across kicks; refit the tube at boundaries or certificate breaks, not per kick) is "the cheapest compute is compute not done" (§1) and targets "minimize spike compute" (§12) — but it must not spend exactness: the refit *is* what keeps errors from compounding (§13), so the design question is which certificate guards the deferred refit. Not in conflict with the 6 Oct gold `components-4643` (that killed deferring *encounter window setup*, a different 92%), nor with `q-secular-v2` (zero-kick phasors die at belt scale — cadence has a floor, cost per kick is the other half of the product).

**The lens.** Quant reads latency and misses representation: I measured the shipped resolver as-is and did not ask whether the per-kick refit is the *right representation* of a kick (a B12-style question). The v2 clock path — the law everything is converging on — got only 12 samples because one player ship in 6 s of RTF 100 kicks rarely; a fleet of clock-stepped ships is the measurement the next run should make.
