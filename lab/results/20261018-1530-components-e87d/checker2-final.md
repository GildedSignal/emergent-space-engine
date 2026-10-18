Grade: goldCheck complete. **Grade: gold** — written to `check2.md`, with the page corrected in place and the tree restored.

**Reproduction.** Applied `work/patch.diff` to the clean tree, rebuilt, reran every mode: anchors, control, sweep, slack, stale, and both held-out files all **bit-identical** to the stored outputs; timing within clock noise (1,372 ns vs 1,365/1,394; cut 3.4–3.5×). `predictions.md` (15:41) predates the decisive outputs (15:56); P1 held, P3–P5 failed in the kill direction and fired the frozen kill criterion — honestly reported.

**My adversarials** (all outside the author's populations, fresh seed):
- **Full formation** (their named unmeasured corner): 240,000/240,000 Full sections, pre-kick `d = 0` exactly → due "never" for every pair, one quantum kick flips **44.7%** on at KH=10⁶ — nothing to store; and no cache (δw p50 0.39·w/kick). Kill extends, stronger.
- **Thinnest reachable windows** (a=1, σ_e 0.3): w floor 3.8×10⁴ ticks — 1a29's "w ≈ 23" is a unit artifact; in-crate c₀ ≤ v bounds w, so no δd/w ≈ 10³ class exists. Law holds tighter (ratio 0.99–1.03), drift/slack 1.17, leak 0.18 — kill holds by measurement.
- **Wide attempt** (σ_e 0.3): 0 Wide in 480,000 — P6's branch never fires at the design reach.

**Corrections to the page** (appended in place): the "~10³·w thin class" line is 1a29-unit arithmetic, not an in-crate class (in-crate δd/w ≈ 0.2–0.5); the Full-corner flip constant is formation-dependent (0.227 checker 1 vs 0.447 mine — same verdict).

**Missed by the author:** the cache's tail (their own `IDENTITY max δd/w = 1.4×10⁶` — a full-modulus re-quant tail the invalidation rule must catch; the 3.4× is a p50 statement); Wide still unmeasured but apparently unreachable; stale-leak flatness asserted on three points.
