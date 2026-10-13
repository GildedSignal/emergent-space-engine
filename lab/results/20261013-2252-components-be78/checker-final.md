Working...
**Grade: gold** — written to `lab/results/20261013-2252-components-be78/check.md`.

**What I did:**

1. **Reproduced.** The runner's `regen.sh` table holds: digests `=` on all 7 scenes + plain build, main-thread retries →0, hand-out −30…−36%, bind −40…−45%, aggregate 519→343 µs (dossier: 538→360 — the shared-box wobble the dossier discloses).
2. **Predictions.** `predictions.md` (23:02:11) precedes the first held-out run (23:02:28); only the disclosed tuning scene ran before. P1/P2/P7 (soundness + deletion) held everywhere; P3 missed low, P6 wrong for this box — calibration misses, honestly reported.
3. **Adversarial (mine, past the author's range):** m16000 seed 3 (2× the largest tested N; 13,729 hand-outs, 52% retry rate off), seed 5 at flying pace (68% retry rate — above even the author's band), and a doubled 16 s horizon. All three: digests bit-identical, retries→0. The m16000 −94% hand-out timing is a collapse artifact (off2 control predicts exactly that wobble); the invariants held.
4. **Structure verified in shipped code:** `word_of_key` = `word_for(entry)` by construction — `from_state` passes `passage_edge.unwrap_or(r.scale(1))` to `Passage::compile`, which stores it verbatim as `outer_radius` (orbit.rs:1009); `ending_at` returns the `from_state` fit whenever one exists; the pre-shifted bind receives bit-for-bit the retry's second-bind input; every error path falls back verbatim.
5. **Novelty:** quant-7055 named "choose the word before the first bind" as a path; this run converts it into a measured, structurally-proven, adoptable deletion (also killing the memo's reason to exist). Not a repetition.
6. **Suite:** 0 failed in every binary on the patched tree (first attempt starved at 420 s under sibling load, completed in 96 s on retry).
7. **Page:** the proposed `wiki/frame-cost.md` is additive-only and faithful — no corrections needed.

Tree left clean (patch applied, tested, reverted; only `lab/results/` untracked).
