Working...
Check complete. **Grade: silver** — written to `lab/results/20261012-0311-autoresearch-3d4e/check.md`; tree left pristine (`git checkout` after the A/B), no commits.

**Reproduced** (clean tree, `git apply work/patch.diff` myself):
- Baseline 16.33 µs tuning (3-run median) / 30.36 µs heldout; kernels 22.1/3.0/75.5/39.2/1.9 ns — all within noise of the dossier.
- Patched: −2.7% tuning, −2% readout; hashes `a4ca5799aa979f44` / `34ad080fe9afcf1b` identical to pristine; `cargo test -p emergent-space -p emergent-universe --release` all green.

**Adversarial:** built a 1400-key near-separatrix corpus (p swept through the true separatrix p = 6+2e with 5·10⁻¹¹ steps crossing the `fast` gate, e → 0.9999999; 339 knots/orbit, 17× slower compiles): hash identical, no panic, ~0% timing delta — corroborates the "cost is structural" attribution.

**Why silver, not gold:** held-out P1 (−25%) and P2 (−15%) failed (−2.4%, −2%), honestly disclosed; the gain is 3%, not a 10× move. The kill of the "divisions dominate compile" direction is real and redirects to the named gold experiment (P5: shape reuse on the plane's kick distribution).

**One finding the author missed:** the patch comment's exactness proof ("already casts `as u64`") is logically insufficient. I closed it from the crate's guards — `fast` ⟹ delta ≥ 2⁻³² ⟹ root ≥ 2⁴⁶ > 2⁴⁰ (margin 2¹²); x ≥ floor = 2k−1; q < 1/(4k+2) ≤ ¼ ⟹ horizon ≥ ½ — so all four quotients are provably < 2⁶⁴ on the reachable domain. Conclusion stands; the justification should name the `fast`-gate invariant, since lowering that gate below ~2¹⁸ would silently corrupt division 1 in release.
