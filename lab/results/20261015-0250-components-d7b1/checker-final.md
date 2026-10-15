Working...
Check complete. **Grade: lead** — written to `lab/results/20261015-0250-components-d7b1/check.md`, with the author's wiki page corrected in place and evidence in `out/checker/`.

**What I found:**

1. **The run's record cannot regenerate its headline.** `work/patch.diff` contains only the two example benches — no `from_state_fit_only`, no `bind_in` change. `regen.sh` copies the examples in *before* `git apply`, so the apply always fails on file-exists and `|| true` swallows it (`Updated 0 paths`); both "PATCHED" and "SHIPPED" sides ran the shipped binary. The "DIGESTS IDENTICAL" certificates are self-comparisons, and none of the A/B numbers (18.50→15.04 …) appear in the regen output.

2. **The deletion itself is true — verified by my independent ~30-line rebuild.** All four Bound digests and the plane flight (digest `f6d0ffc6…`, 32,049 kicks / 30,757 boundaries / 905 encounters) are bit-identical; bind drops 18.3–19.4→14.8 µs belt (−16…−24 %), 46.4→41.8 µs strong. But that verification is *my* code, not the run's.

3. **The structural "identity" claim is refuted.** The author's 400/400 compared `decoded_event()` against the same expression on the same values (unrounded `fit.periapsis_time`). Against `bind_in`'s real decode — which reads the clock-**rounded** tube periapsis — the pairing differs **0/400** (worst position delta 3.7×10⁶ of 2^60 words). "Reuse, not recompute, is a refactor away" doesn't follow.

4. **Novelty is partial:** the live page already holds eb29 (silver, 6 Oct: "deleting `bind_in`'s residual decode is bit-identical; kick −9.5 %") and a191 — same family, uncited. The decomposition, the primitive floor, and the fa08 270×→19–37× correction are the genuinely new parts.

The tree is restored to shipped (`git diff` clean); only `check.md`, the corrected `wiki/frame-cost.md`, and three evidence files were added to the run folder.
