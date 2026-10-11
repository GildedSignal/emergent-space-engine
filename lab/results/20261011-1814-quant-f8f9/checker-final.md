Working...
Check complete. Summary of what I did and found:

**Reproduction** (clean tree, empty patch, shipped binary at `/home/glmlab/lab-target-1/release/xtask`):
- All 10 dossier commands re-run. **Every digest matches the author's bit-for-bit**, including the invariance triples: engine budgets 1/5/15 ms at rtf 1000 → one digest `6293ce7d…`; paced vs `--unpaced` → one digest `01c9be77…`.
- Readout share 69–93 % in every run (author 68.6–92.7 %); gather 8.8–10.0 µs/body at rtf 100 (author 8.6); per-kind costs exact (ship 105–195, player 579–1213, fleet 28–58 µs); the 10⁹ arithmetic verified (2.95 µs/event at 32 kicks/orbit, ~300 µs at 0.3).
- `predictions.md` (18:17:18) precedes the first data artifact (18:17:46); two honest misses corroborate genuine pre-registration.

**Adversarial** (3 cases): digest invariance holds under brutal saturation at a fresh seed (seed 7, 400 members, 1 ms budget: 788/900 overflow, 82 % short of cut — identical digests); at rtf 10 000 and rtf 10 000 + 400 members, worst frames 11.8/14.7 ms — no hitch above 16.7 ms at the 5 ms budget, gather stays the floor. Engine share never exceeded 38 %.

**Grade: silver.** Why not gold: the two headline facts are already known — H0210 ("the view gather is 83 % of a light frame; kicks cost 29 µs") and H0212 ("one digest over five schedules and budgets"). The run's real additions: the post-cache re-quantification (the cache did not change the asymptote), the allocator knee (hitches only past budget ≈ frame − one event), and the current per-event ledger that hands `b-readout-cost`/`q-cadence` measured targets. It reorders, deletes nothing — the author says so and asks silver.

**Found defects** (all flagged in `check.md`, none fatal): the claim line's "55–72 %" is the gather share mislabeled as readout share (understates: true readout 69–93 %); summary.md's "rtf-independent" gather contradicts its own table; the rtf-1000 magnitudes (gather p50 5.0 ms, 101 overflows, "load ~1") are ~4× contention artifacts — my quieter runs give 1.34 ms and 8 overflows, though the seed-dependence (604 vs 1770 events/s) is real delivered work; digest invariance is partly by bench construction (settle-to-cut); `--members` clamps at 400, bounding all scaling statements.

`check.md` written to the run folder; nothing else touched, no git commands run.
