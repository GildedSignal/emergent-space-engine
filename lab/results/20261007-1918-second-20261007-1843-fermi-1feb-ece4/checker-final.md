Working...
Verdict written. Summary of the check:

**Grade: silver** — `lab/results/20261007-1918-second-20261007-1843-fermi-1feb-ece4/check.md`

**Reproduced bit-for-bit in a clean tree:**
- `capture 1 10 48` → 663 kicks, refused 0, **byte-identical** to the stored JSON; shipped `--kick-bench` independently confirms 663 rebinds; 682 = 663+19 excluded; pooled = exact concatenation (11,076)
- All six shelf numbers regenerate exactly: 39.1 / 41.2 / 56.1 / 62.2 / 43.5 / 55.1 bits/kick, readback bad 0, birth 1.91 bits/body
- Slice-free rate 49.07÷100÷32 = **0.0153** (seed 7 identical); `budget2.py` regenerates 45.9 core-s, 13 % hot fraction, 75–107 MB/game-s
- Domain kill verified structurally in shipped code: `Key::darwin` caps p at 8192 M, `pop::orbit` draws [100, 8000), plane orbits at 5.5×10⁷–6.1×10⁸ root units — p_q16 overflows u32 outright

**Adversarial finds (mine):**
1. **"Saturated ~70 bits/body" is false** — extending the author's own dense run to 200/400 rounds gives 116→141 bits/body (~86 %/98 % scarred), still climbing. Direction of the conclusion (refit-not-delete) strengthened; the 2.2× number understated (≥4.4×).
2. Two evidence-line stats contradicted by the logs: doll-0 deltas have medians 2^22/2^25 quanta and 0 % zero-t_p (the "≈2^14, 62 %" figures are the pooled doll-2-dominated stats — subset conflation; the doll-0 magnitudes actually fell *inside* the predicted band).
3. Robustness confirmed: fresh seed-7 doll-0 deltas → 26.8 bits/kick (39.1 not inflated); different belt seed → 39.1 exactly.

**Why silver, not gold:** every adopted number reproduces and the premise kill (B18b's shipped belt columns can't hold game orbits) is real — but by the lab's own rule a headline the log contradicts costs the grade: the saturated-70 sentence, the doll-0 stats, the stored `readback_bad: 1` against the blanket "bad=0", and an undisclosed mid-run `shelfrun.rs` edit (benign — all numbers regenerate). The one experiment to gold is minutes: adopt the measured stock-growth curve and fix the two evidence lines.

No other file in the run folder was touched (build artifacts under `work/scarkick/target/` are the dossier's own documented reproduce path).
