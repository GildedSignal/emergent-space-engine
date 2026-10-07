Working...
Check complete. `check.md` written; the author's folder is otherwise untouched (the mid-check mis-targeted edit to `main.rs` was fully reverted and verified byte-identical against the pristine pre-edit copy; all reproduction ran from `/tmp/check-97bf`).

**Grade: silver.** Summary of the evidence:

- **Reproduced:** digests match stored rows exactly (A/2¹⁸ and A/2²⁴, seed 2, both structures); ratio 0.21 vs claimed 0.22; tails 1.6–2.0 vs 4.6–6.7; diff mode clean on A–D; floors regenerate; incumbent heap verified verbatim against `crates/lattice-event/src/lib.rs:218-317`; predictions honestly pre-registered with failures disclosed.
- **Adversarial findings:**
  1. **Correctness hole (falsifies the "identical stream" claim in a reachable state):** with every body beyond the wheel horizon and one re-timed body, `next_tick` returns a stale overflow entry's tick and the wrong body is delivered at the wrong tick — silent divergence (`wheel_next 3145728` vs heap `4194304`).
  2. **Spread regime unmeasured:** on log-uniform delays the wheel wins only ~1.6× at 2²², not 2.2–4.5× — the headline is storm-specific, though no regime showed the heap winning.
  3. **Large-N rows are one-shot** (`sets` = 1–2: fill + one mega-drain); steady-state storm ratio is ~0.43.
- **Novelty:** the idea is a named prior-art lead (`original-research-report.md:643`, radix/bucket queues for integer ticks), never measured before — this run supplies the measurement.
- **Not gold:** gain is 1.6–4.5× by regime (below 10×), the correctness corner needs a fix before adoption, and the gain magnitude as claimed doesn't transfer outside storms. One experiment away: close the staleness corner, then measure a mixed spread+storm workload in steady state and restate gains per regime.
