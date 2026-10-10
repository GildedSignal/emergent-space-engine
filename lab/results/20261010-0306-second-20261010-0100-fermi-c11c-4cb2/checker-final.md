Working...
Check complete. `check.md` written to the run folder; nothing else touched.

**Grade: gold.**

What I verified:

**Reproduction** — clean tree (patch.diff empty; `bench/` targets shipped crates by path, public APIs only). All five `--kick-bench` digests and replay digests byte-identical to the stored records (20 s matches the silver's original too); rtf-100 bench digest identical (337.8 events/s); `budget.py` and `amort.py` regenerate byte-for-byte; derived rows recompute (1,516 ns/kick bar, 41.8→38.3 machines amortized). Timings shifted with box load (quiet now: 39.6–44.2 µs vs stored 38.4–59.2) — same spread the silver's checker saw; shares are what carry the verdict.

**The decisive experiment** — the plane replay's digest equals the shipped bench's (attribution provably covers the record's own kicks; distinct-kick dedup respects the 5 Oct re-timing lesson); coverage 98.7–103.3% on plane populations; the co-orbital sharing premise granted (400/400 kicks in one quantized shape, deterministic).

**Adversarial** — unseen seed 4: share 9.3%, gain 1.08×. N=1600 (4× the author's largest): still 1 quantized shape, gain 1.15×, no N blow-up. Independent radius: 1.14×. Fresh quiet-box verdict from scratch: gains 1.11–3.06×, floor 19 µs = 13× the bar. Arithmetic ceiling: 40× requires a compile share ≥ 97.5%; the worst measured anywhere is 84.3% → ≤ 6.4×. The refutation cannot be box noise or M1 variance.

**Predictions** — written 11 s before the first decisive output (mtime-only evidence again; run.log empty); P4 (the verdict) and P1 held; P3's exact-key half failed and is reported as failed, and the failure itself confirms dbd4add's committed split.

**Novelty** — dbd4add pinned the exact-key memo across kicks on one body; the compile share and cross-body amortization were never measured. This is exactly the checker-named gold experiment, delivered as a clean refutation: the compile-amortization lever dies; the next rung aims at the rebind remainder (28.4 µs floor, 19× the bar).

Misses noted in check.md: the "99–103% coverage on every population" overstates the co-orbital runs (95.5–98.2%), P5's seed 3 (7.7%) sits below the predicted band unreported, the share-ceiling argument is implicit but unstated, and the seed-3 tail row rests on 5 kicks.
