Working...
Check complete. **Grade: silver** — written to `lab/results/20261010-1544-system-97ce/check.md`.

**Reproduced bit-for-bit** from `work/patch.diff` on a clean tree: 406,220 events / 203,017 kicks / rebinds and rekeys 203,017 (1.000/kick) at the engine's default cadence (`Config::default().step_log2 = 7` — verified); 2⁴ gives 50,939/25,401 (work ratio 7.98× for 8×); control 397/397; sizes 176/192/448 B; extrapolation arithmetic checks (3.4% of a core at 10⁹). Code reading confirms the author's honesty claims: `kick_clock` never populates `kick.dv` (step.rs:638), and `Catalogue::insert` has no dedup — the "memo" is the not-adopted law.md design, correctly proxied by key equality. The law.md re-anchor quote (0.05 compiles/kick) and HANDOFF's "H_live not measured yet" both exist.

**Three adversarial cases:**
1. **Revisits** — all 101,519 keys globally distinct, per-body distinct = per-body kicks. Even an unbounded memo misses every kick; the claim is stronger than stated.
2. **Saturn** (2⁻¹², 9.58 AU) — still 1.0000 rekeys/kick; saturation is not a Jupiter artifact.
3. **Cost attribution** (the dossier's own open question) — `bind()` = 21.9 µs/call = **43.7% of wall**. The 20× is the compile-count reduction; the belt's wall-clock gain from the re-anchor is bounded at ≈1.7×. This is what keeps it from gold alongside the failed held-out predictions (lab precedent: the 1 October law red-team).

**Gold path:** wire the re-anchor and measure compiles/kick vs 0.05, wall, and behaviour on the belt.

Tree left exactly at the author-patch state; my instrumentation removed; nothing else in the run folder touched.
