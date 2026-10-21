Working...
Check complete. Everything the checker owed is done; the tree is restored to the clean base (only `check.md` and the page corrections remain in the run folder).

**Grade: gold** — `check.md` written, the author's page corrected in place.

**What I did:**

1. **Reproduced** from a clean tree at base `00696555`: applied `work/patch.diff` (self-contained; `orig-patch.diff` is the parent session's leftover), ran `regen.sh` — every deterministic number bit-for-bit identical to the runner's regen and the dossier (all 8 digests, walk counts 65.55→1.20→0.46→0.32, memo 362–365/747, fallback 48/58); timing arms drift only inside the dossier's stated jitter.

2. **Flew four adversarial arms, two outside the author's ranges:**
   - **N=100k** (3.3× max): digest-neutral. Found the near set is N-invariant in this scenario — walk-vs-C scaling stays untested.
   - **D=512** (8× max dial): digest-neutral; walk flat at 0.32/scan from D=64 — the churn floor is real and now bounds the ∝1/D claim.
   - **30 s burn** (5× horizon, 471,055 scans): digest-neutral, walk 5.30 → **0.00** re-reads/scan (~1700×), memo 49.9%.
   - **3k fallback timing** — the arm the author predicted in P4 but left out of the cost table: **162.3 → 101.8 µs/call, a −37% net µs win**. This materially corrects the dossier: the µs refutation holds only on fenced arms; where the walk *is* the row (the fallback/m48 regime budget-1e9 reads), the news form already pays today. The page's Refuted line and Current best now say arm-split.

3. **Code-audited the exactness premise**: `cartesian`→`readout`→`decode` never reads `b.kick`, `same()` is kick-blind, `binding_until` mirrors `binding_at`'s segment logic; the same-tick double-rebind hole cannot interleave with capture. 12/12 neutral flights consistent.

4. **One claim failed to reproduce**: "the crate's 10 lib tests pass" — 8/2 here, with the *clean base failing the identical two* `step.rs` tests, so the patch causes zero regressions; recorded in check.md.

Gold rationale: the named gold experiment done and reproduced, the walk term deleted 205×–1700× in work units on the board's scan row, adoptable as wiring — and the failed P4 is the run's own delivered refutation (a premise shown wrong, diagnosed, and now bounded both ways by measurement).
