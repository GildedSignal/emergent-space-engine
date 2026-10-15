# Predictions — 20261015-1338-quant-1d52 (written before any retention flight)

Build: the record's seam patch (e0f9) + `ES_RETAIN=1` (a retained-entry cache in the demoted
slot: first read after a kick mints and keeps, reads until the next kick hit the cache, the
kick's settle drops it). Arms per scene: control (no env) / seam (`ES_LAZY_ENTRY=1`) /
seam+retain (`ES_LAZY_ENTRY=1 ES_RETAIN=1`), same binary, canonical cut digest.

Scenes: 10⁴ coast 20,000 s1; 10⁵ coast 20,000 s1; 10⁵ coast 48,000 s1 (the wave-train anchor
arm, `2109a2e0…`); held-out 10⁴ coast 20,000 s7.

1. **Identity.** Digest bit-identical across all three arms on every scene (retention changes
   when compiles happen, never values; `Orbit::compile` is pure). Any difference: VOID, the
   instrument is broken, not the rule.
2. **Redundancy of the read stream.** With retention on, cache hits / total reads ≥ 85% at
   10⁵ (the record's 8.7–9.9 promotions per demotion implies ≥ 88% repeat reads) and ≥ 90% at
   10⁴ (15.6–19.6 per demotion).
3. **Residual bill.** Promotions under retention land in [0.3, 1.5] × demotions at 10⁵ (vs
   9.9 × as flown) — i.e. one mint per kicked-and-read body per kick interval, not per read.
4. **Wall.** The retain arm's total_s is within +15% of control at 10⁵/20k (vs the seam arm's
   +40–100% as flown).
5. **The memory tension (the number the integrator needs).** At 10⁵, if the between-kick
   reads touch ~all bodies (the record's read density), retained_now ≥ 0.8 × bodies and
   bytes/body under retention returns to within 15% of control (~1.5 kB), erasing most of the
   seam's standing-memory win at full read density; the CPU win (2) stands. If reads are
   sparse, retained_now ≪ N and both wins hold. Either outcome decides adoption at 10⁹.
6. **10⁹ composition.** With (2)+(3) holding, the no-retention promotion bill (~130 cores at
   10⁹ rtf 100) falls by the redundancy factor to ≤ ~15 cores, and the residual folds into
   the kick's own compile only if residual ≈ demotions (one mint per kick interval).

Kill rule (frozen): retention deletes < 50% of promotions at 10⁵ → the rule is wrong (the
read stream does not cluster between kicks); report as KILL of the retention rule, not of the
seam.

Not measured here (named): per-callsite read attribution, the M1 compile price, contacts-rich
scenes (the checker's open `same()` experiment).
