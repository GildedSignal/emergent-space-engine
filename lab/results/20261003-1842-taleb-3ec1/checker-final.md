Working...
Check complete. `lab/results/20261003-1842-taleb-3ec1/check.md` written; tree restored (patch reversed, scratch test removed, only `check.md` added to the run folder; no commits).

**Grade: silver.**

**Reproduced** — `git apply work/patch.diff`, `fragility a|c|d`, `kicktail`: every deterministic number bit-identical (dormancy fractions at all horizons, eval counts, bucket shares, A/B counters, kicktail candidate counts). Timings same order; the cold/hot per-pair cost inversion reproduced more strongly here (68.8 vs 5.7 µs/pair).

**Held-out** — P1 and P6 held; P2 and P5 failed and were honestly reported. But **P3 is misreported as held**: the author's own coorbital datum shows lazy/eager = 22.79/25.79 µs = 0.88 (Full sections make the "cheap certificate" cost the same as eager), which also punctures the "1.0–1.6 µs/pair" range in the claim.

**My attack** — machinery-independent brute force (dense grid + own refine) over 9558 adversarial candidate pairs, 576 with real encounters: exact commensurabilities (pj = k·pi and ±1 tick), bisected near-tangencies, fat ρ = 2e-2, e up to 0.9, both orderings → **0 dormancy violations, 0 cone leaks**; 6 born-close pairs (within ρ at t=0) classified as boundary cases the l ≥ 0 passage model cannot express. The certificate is sound, with two unstated caveats: encounters may precede their bracketing passage by one arc traversal, and genesis needs a proximity pass.

**Why not gold** — nothing built moves the bottleneck ≥ 10×: the lazy path alone is falsified (worst overrun ~11–12×, not the stated 8×), and refine-on-first-activation is only proposed. The value is the map — cost upside-down (quiet belts pay most, worst at mid-e), a player-triggerable O(N) tail — plus a soundness result that survived an independent attack. One experiment away: the hybrid on the kick path, including the coorbital case where the certificate must skip even the `full_section` build.
