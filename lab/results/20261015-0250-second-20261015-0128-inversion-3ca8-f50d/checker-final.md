Working...
Check complete. Verdict: **gold**.

**What I verified:**

1. **Reproduction** — applied `work/patch.diff` (touches only `examples/shadow2.rs`), re-ran pump s1 and all four neg arms: every physics field bit-identical to the author's `out/` (only `wall_s` differs); the full table matches the dossier line for line.

2. **The instrument** (the load-bearing claim) — verified three independent ways: line-by-line source audit (`hit_f` ≡ `hit_narrow`; the twin's skip gate ≡ `relativity.rs:236`; `law_reflect` ≡ `fast_targets`' Householder; `chronon.rs:121` logs Contact for *every* hit pair, so contact counting shares semantics); the micro table (≤ 2.465e-6 rad engine-vs-law at all glancing cases, tilt 0.1555 rad); and a **direct probe of the shipped engine** — a crossed-in-bin pair logs a Contact while velocities and revisions stay bit-unchanged, control pair exchanges. The 87.5% pass-through is the shipped rule's own semantics.

3. **Adversarial, two outside the author's domain** — held-out seeds 6–7, Q=2¹⁴, β 0.95, 10⁴:1 (3 seeds), cold β 0.05 gas: every class metric stayed in band. The one excursion (10⁴:1 max-dwell 1.71×, one seed) proved scatter (0.95×/1.08× on extra seeds). The neg "final γ = phase snapshot" attribution confirmed: seeds 2/3 scatter 5.4-v-248 and 97-v-1.6 in *both* directions while dwell stays one class.

4. **Predictions** — folder mtimes consistent with predictions-first (03:01 → dossier 03:14); 5/7 held, both misses disclosed; the miss I could test (neg final γ) is the metric's fault, as claimed.

5. **Page** — faithful merge of the main/3ca8 conflict, both sides kept; not closable (one gold, not three). I added one bracketed checker line with the held-out extension.

The run deletes the "raise Q to heal dense-order classes" path, prices 87.5% pass-through for the integrator, and makes the trapping rung freezable in one step. Tree restored to as-found; only `check.md` and the page's checker line were added to the run folder.
