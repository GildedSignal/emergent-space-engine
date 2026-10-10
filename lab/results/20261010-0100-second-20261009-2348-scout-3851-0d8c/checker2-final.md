Working...
Check complete. `check2.md` written to the run folder; nothing else in `lab/results/20261010-0100-second-…-0d8c/` was touched, and no git state was modified.

**Verdict: gold.** The evidence chain:

1. **Reproduction, bit for bit.** `run-all.sh` in a clean /tmp copy regenerated `val.json`, all six `results2-*.json` and `analysis.txt` **byte-identical** (cmp), 4:15 wall, 148 MB peak RSS, every command under 60 s. Every dossier number prints from the regenerated files.

2. **Physics verified from scratch, third path.** I derived Christoffels and the full Riemann symbolically from the metric (sign anchored on the physical radial stretch, −2w), and contracted the tide independently of both author paths: Λ₁₁/Λ₃₃/Λ₁₃ match the closed forms to ≤2.1×10⁻¹⁵; ω = −⟨∇ᵤf1, f3⟩ matches to 6×10⁻⁶ (circular: 4×10⁻¹⁶, and I re-derived the geodetic −2π√(1−3u) by hand). The chart — the object the tube compiles — is right.

3. **Pre-registration holds.** marck.py finalized 01:59:06, predictions 02:01:51, sweeps 02:11–02:14: a 12-case sweep takes ~4.5 min, so held-out bands physically could not exist at prediction time. P1–P5, P7 held (P4 stronger); P6/P8 failed and are honestly reported.

4. **Attacks.** Grid hole (1e6, 0.6): 18=18. Strong field rp=6: 16=16, domain guard works. Threshold stress 0.01/0.02/0.05: chart 0 missed everywhere, frozen ~90% missed. Quantization to Q=2⁸: all bands survive — stronger than claimed. Extreme e=0.9: (100, 0.9) shows truth 12 vs chart 14, adjudicated as the *truth's* artifact (transport-derived ω off by 3.5×10⁻³ vs my independent 3.9×10⁻⁵) — the chart is the robust side, which supports adoption but bounds the transport cross-check to e ≲ 0.7.

5. **Novelty & fit.** Exactly the gold-lock experiment the scout's checker named; the prior fermi runs built only the scalar kernel (the phase-2 build graded "missing"). Kills the scout's shipped scalar certificate (142/144 missed) and fixes the adoptable form: one 4-column quantized table per (E,L) tube.

Misses recorded: undisclosed two-pass provenance (dossier mtime sits mid-pass; the mtime note in it is wrong), the e-ceiling on the truth side unprobed, "8×10⁻⁵" is relative not absolute, P2's static-edge clause tallied without a printed number.
