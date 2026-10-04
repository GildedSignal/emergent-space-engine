Working...
`check.md` written — the only change in the run folder. Summary of the check:

**Grade: silver.**

**Reproduced:** `./replica ref` and `./replica sweep` reproduce `ref.txt` and `sweep.txt` **byte-identically** (45 s + 58 s, clean tree, empty patch). Predictions were pre-registered (mtime 06:09:03 < sweep 06:10:13; the sweep is a one-shot deterministic command, nothing tunable). A Newton 8→16 control leaves all seven reference slopes unchanged to 7 digits — the references are solver-converged, and the replica faithfully mirrors `step.rs`'s documented law (DKD midpoint kick, phase step 1/64).

**My adversarial attacks, and what they changed:**

1. **Fine grid kills the 1.34×.** The sweep's power-of-two macro grid quantized the frontier: dkd passes all gates at **22.8** kicks/orbit (macro 22, jac 7.9e-5) on A; y4's true min is ~24.7. Honest ratio ≈ 0.9–1.0 — order buys *nothing*. This strengthens the headline (no 4×, decisively) but corrects a stated number in the adoption-favouring direction. On F, y4 has **no** passing setting at all under the author's own gates, while dkd's true min is 65.5 (not 74.7).
2. **The G cliff is real, silent, and now located.** At 0.45 R_H prograde, dkd@64 gets apsidal precession wrong-sign 11.9× with Jacobi 8.6e-6 and e error 0.09% — and it heals only at ~107 kicks/orbit *spent*, the same spend for dkd@96 and y4@32 (tide resolution, not composition order). The plane's current 1/64 would fail B14's precession gate on judged G-like seeds today.
3. **Novelty and citations hold:** no H entry measures composition order or the 1/64 margin (H0190 was rates/averaging); `q-correctors` is genuinely queued. arXiv:1908.03468 is real and on-point, but by Rein et al., not "Wisdom et al."; the "y6@~8208 sub-kicks" figure is a factor-2 slip (~4232 actual).

**Not gold:** nothing moves 10×, nothing is deleted, and the adoption path is a gate decision plus a warning, not a one-step change; the author itself requested silver-to-lead. **The named gold experiment:** freeze which gate owns moon kick cost (B14-only vs Jacobi 1e-4, exponent pinned above the noise floor on median seeds), re-measure the fine-grid frontier over B14's 256-seed ensemble — if B14-only owns it, 1/64 → ~23 kicks/orbit (≈2.8×) becomes a one-constant change candidate, with G forcing the seed-filter/rate decision alongside.
