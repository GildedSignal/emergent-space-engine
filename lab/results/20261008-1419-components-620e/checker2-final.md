Working...
Check complete. `check2.md` written; the run folder is otherwise untouched, no commits made, and the tree carries only the author's applied patch.

## Verdict: **silver**

**Reproduced.** Clean tree + `work/patch.diff`: bind 18.7 µs / secondaries 7.5 µs / force 1.6 µs at my load (author 28.6/10.5/2.3 at load 5.8) — shares **67.2/27.1/5.7 %** vs the claimed 68/27/5.8, idiot index **25×** both. The deterministic exactness numbers (1.845, 1.573) regenerate bit-identically, resolving the 14:44 source-mtime worry. The bench times unmodified crate functions; no strawman. Predictions pre-dated the run.

**What I found beyond reproduction:**
1. **The author's "unexplained" 1.573-quantum residual is their own harness, not the evaluator.** `accel_floor` never accumulates `fx` (the compiler's `unused variable: ox` warning flags it); the deviation equals |origin_fall_x|·h·2³⁰ = 1.572 quanta exactly. With the one-liner added, the held-out sweep passes the pre-registered criterion at **6.25e-4 quanta**. Prediction (1) was killed by a bench bug, not the Newton chain.
2. **Adversarial near-edge sweep (my case): the integer changeover branch is broken three ways** — `recip_pf = 2^40/half_pf` underflows to 0 for any planet-scale edge (zeroing the x-pull), `py` is never weighted, and its support [E/2, E] mismatches the crate law's W₀ support [E, 2E] by one shell. O(1) disagreement in the annulus (rel 1.44, 4.6e3 quanta). The held-out belt is entirely far-field, so this path was never tested — the "define it as the law" adoption step cannot proceed on this code.
3. Prediction (5) reported "held" while its "today 3–10 µs" half missed by 3–4×.

**The one experiment for gold:** fix the one-liner, implement the crate's actual W₀ in the near branch, rerun exactness across the annulus. The cost decomposition and the shared-epoch-secondaries deletion stand on their own today.
