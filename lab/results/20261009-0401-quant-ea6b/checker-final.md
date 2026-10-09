Working...
Check complete. `check.md` written: **Grade: silver**.

**What I did:**
- **Reproduced everything bit-exact** in a clean tree with `work/patch.diff` applied: replay digests, memo counts (0.970988…, 260 shapes, 8962 rebinds), medians 35.4/69.4 µs, cold/warm 1.379×. Completed the digest control the author claimed but never saved — the patched binary reproduces the clean baseline's `dac49af3…` exactly.
- **Killed the headline claim.** The author's "rebind 59.3% of all kicks" comes from stage timers in `kick_clock`, but counters I added show only **12 of 9192** benched kicks take that path — 7601 are doll-2 ships on the legacy split `fn kick`, never instrumented. The run's own JSON contradicts it (total_ns is 10³× below samples × median). The "(motion law v2)" label is likewise wrong; law v2 got 12 samples and remains unbenched.
- **Rescued the conclusion.** Instrumenting the real path myself: rebind is **84.8%** of plain-kick time — the "delete the recompile" lever stands, on evidence this run didn't produce.
- **Adversarial cases:** population-identity probe (ext/doll counters), load sensitivity (medians inflate 1.5× at loadavg 3.7; ratios/memo stable), shorter-run consistency. Novelty checked against H0210/H0213 and the 5 October artifact: exact-memo-never-hits and the ~95% quantized rate are known; new are the cold/warm ratio, two-population medians, and capacity arithmetic.

Silver, not lead, because the cold/warm, median, memo and capacity halves are real, reproduced and on-goal; one experiment (re-instrument `fn kick`) from gold. Tree left clean; only `check.md` added to the run folder.
