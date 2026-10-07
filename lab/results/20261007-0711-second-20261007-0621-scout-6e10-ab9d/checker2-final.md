Working...
Check complete. `check2.md` written; the run folder's files are untouched (my reproduction ran entirely in `/tmp/check2-scratch`).

## Verdict: **Grade: gold**

**Reproduction.** All four dossier commands, bit-identical outputs (`real_kick_ledger.json`, `diag_bands.json`, `int.npz`, `ctrl.npz`), timings 8.2/56.4/25.0/0.4 s matching the claimed 8/58/28/0.4. `predictions.md` (07:22:05) precedes the decisive `int.npz` (07:31:56); the script's later edit is confined to the labelled post-hoc measure path — provably, since the current integrate path regenerates `int.npz` bit-for-bit. Empty `patch.diff`; nothing outside the folder touched.

**Predictions.** P1 ✓, P2 ✓, **P3 ✓ decisively** (the first checker's A1 objection: the original's 12-term basis recaptures 0.0% of 41.45 bits), P5 ✓; P4 ✗ is the author's own pre-registered kill criterion firing with its branch followed — the failure is the result.

**My six adversarial cases all confirmed the claim:**
- Noise floor re-measured per band (σ ≈ 1.4×10⁻⁴): the inner belt's kick is 15× above it — signal, not integrator artifact.
- Every body scarred: min |Δz| = 1.6×10⁻⁶ > q24; 4–8 conjunctions per window.
- Validated KL entropy estimator: true differential entropy 20.76 vs Gaussian-fit 20.72 bits/component — the heavy tail does **not** deflate the 5.2 GB/10⁹ pole (my initial 16.8-bit scare was a bug in my own script, checked and discarded).
- k-NN memorization (16k exemplars): 4.6% — "chaotic for any bounded program" survives an unbounded-richness attack.
- 1-orbit window: 2.0% recapture — not an epoch-length artifact.
- Correct-LL with the α the code omits: 0.09% vs 0.1% (label bug, immaterial); force model verified against `force.rs` (pull − origin fall, no truncation, W₀ = 1 for these separations).

**Why gold, not silver:** it is the named experiment from the original's silver, reproduced exactly, with the decisive held-out prediction holding at the extreme, and it shows a premise wrong by measurement — the smooth pole does not exist for real flybys, correcting the allocator's belt line ≈8.6× (0.6 → 5.18 GB/10⁹ at q24) while preserving the stock-vs-flow core. One-step adoption: rewrite the belt line, type B18b's churn pole, price the replay fork. The author's own caveats (one perturber, 2-D, replica integrator, unpriced derive-on-read path) are honest and recorded in check2.md.
