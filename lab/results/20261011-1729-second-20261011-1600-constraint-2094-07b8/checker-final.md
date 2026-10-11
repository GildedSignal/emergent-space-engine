Working...
Check complete. **Grade: silver** — written to `lab/results/20261011-1729-second-20261011-1600-constraint-2094-07b8/check.md`.

**What reproduced (clean tree + the one-line clamp, redone by me):**
- All three bench digests **bit-identical** (`41343a14…`, `c4e03c80…`, `577a2568…`) — the physics record regenerates exactly.
- The m4800 collapse: 4331 bodies, gather 36.9 ms/63.6%, engine pinned at 5.118 ms deferring 900/900, player 25.2 ms/item, 44.9k hitches/h, RSS 1.17 GB — every headline number within a few percent.
- Probe outputs from the surviving binaries: readouts/body 1.00–1.15 at m4800, `view_rel` 1.00–1.63 to three digits, `gather_scaling` 15.0–15.5 µs/emitter at 1.98 readouts (third independent confirmation).

**Adversarial finds:**
- Shipped `--unpaced` bench confirms the ~4× paced-gather inflation (0.709 ms vs 3.46 ms, same digest) — the author's decomposition stands on shipped code alone, though the co-tenant attribution doesn't (3.46 ms persists at load 0.35).
- The m480 "zero hitches / contention-inflated then" correction flips on rerun: 240 hitches/h, gather 6.39 ms — matching the *first* author, and the second author's own failed P3. m480-scale timing is ±2× box noise; single-sample claims either way are unsupported.
- The ~700-body ceiling's json/wire terms aren't derivable from the record; measured marginals give ~850–900. Same order.

**Why silver, not gold:** `work/patch.diff` is **empty** despite the dossier's "Both edits are in `work/patch.diff`". The clamp regenerates from its description; `gather_scaling.rs` lives in the original run's branch; but `plane_readouts.rs` — the run's one new instrument — exists only as an orphaned binary in the shared target dir. The run's own brief was "make the record regenerate from shipped code", and H0212 already names this exact failure as what keeps silvers from gold. Every load-bearing number survives my cross-checks; the delivered record doesn't. Gold is one re-delivered patch away.
