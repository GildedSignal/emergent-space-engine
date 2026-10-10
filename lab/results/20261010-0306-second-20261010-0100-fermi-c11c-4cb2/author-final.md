Refuted theThe named experiment is done, the record regenerates, and the verdict is a clean refutation of the silver's lever.

**What was done**
- **Record regeneration**: shipped `--kick-bench` at 20 s (seed 1) reproduces the original run's digests byte-for-byte; `budget.py` regenerates the table from today's inputs (39.1 machines low-orbit averaged @rtf 100; 1,516 ns/kick needed).
- **Attribution** (new `bench/`, shipped public APIs only; plane replay digest **equals the shipped bench's** at 20 s and 55 s, seeds 1–3; buckets cover 99–103% of `step::process`): the made-ship kick (52.9 µs) is bind 44%, of which the *shareable* compile is **10.6%** (5.6 µs); tau bookkeeping 17%, readout/secondaries ~10% each. The leaver tail is passage-compile-heavy (65% of 136.7 µs, min-vs-min).
- **Amortization**: N co-orbital ships provably share **one** quantized shape (400 kicks → 1 code; exact keys drift: 398 distinct), warm hit 0.8 µs — yet the gain is **1.14–1.17×** (made ships 1.09×; best tail population 6.3×) against the demanded **≥ 40×**. Even deleting the whole rebind leaves 28.4 µs/kick = 19× the bar.
- Checker's corrections folded in: 42× is an rtf-100 figure; quantized-memo 0% is window-dependent (16% at 55 s, exact 0%).

**Claim** (one sentence): sharing one compiled cycle across co-orbital bodies on the shipped law buys only 1.09–1.17× (best tail 6.3×), not the demanded ≥ 40×, because the compile is 8–17% of a distinct kick — so the first-breaker ranking stands (38–42 machines, low orbit averaged, rtf 100) with a new premise: dense populations need the per-kick rebind itself deleted (a formation generator or secular law; floor 28.4 µs = 19× the bar), not a compile memo.
