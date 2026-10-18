Working...
Check complete. **Grade: gold** — written to `lab/results/20261018-2040-dynamics-834e/check.md`, with three corrections folded into the author's wiki page.

**Basis:**

- **Reproduction:** regen.sh exit 0; every dossier number reconciles with raw `fill.jsonl` (38 arms, spike ≤ 1.094, Fano₁ ≤ 1.0205, ratio ≤ 0.9862, fit a=4.02 b=8.03); one arm rerun from the patch is bit-identical; instrument verified as shipped code (`Chronon`, lifetime `max_batch` including burn-in — the genesis-shock attribution is correct; Enskog cross-section checks out with r = Q).
- **Predictions:** kill lines untouched everywhere; two letter-misses (P3 +2% on one held-out seed, P5 −10% at 2¹⁸) and P7's wall-flash half-refutation all disclosed unprompted. Claim sentence unaffected.
- **My 13 adversarial arms, all confirmatory:** horizon ×4 at φ=0.78 (Fano₁ 0.57, Henderson ratio unchanged — the author's own named failure mode doesn't materialize); fresh seeds 7/8/9 match within 0.02; 2¹⁹ with β_max ≈ 0.8 still anti-bunched; even an *overlapping* genesis past the generator's ceiling (φ_req 0.85) shows no avalanche (component 36 < n/10 = 40).
- **Novelty:** closes `contact-speed` od 2's explicitly open residue (φ ≫ 2%), adds the rate law, the affine cost law, and engagement pricing — not a repetition of 1648's dilute-Fano result.

**Corrections made to the page:** Fano₆₄ "up to 1.7" understated the n=1600 held-out arm (2.545); added that g_eff falls with speed at fixed φ (0.93 → 0.80 from 2¹⁷ → 2¹⁹ — the price formula over-prices at high β, conservative); bracketed checker note with the extensions and the n/20-letter breaks. Also flagged in check.md: the dossier's fleet-ν adoption number is 5× optimistic as written (1.4×10⁻², not 3×10⁻³ at β = 0.1) — conclusion stands, arithmetic doesn't.

Working tree restored (my probe examples removed); nothing outside `lab/results/<run>/check.md` and `wiki/chaos-shadowing.md` touched; no git commands beyond status.
