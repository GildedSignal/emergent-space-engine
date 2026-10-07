Grade: silver

**Abstract.** H_live is now measured: a quiescent belt (a∈[2.2,3.2] AU) produces 0.27 L-key changes/orbit at the law's 16+16 key (1.49×10⁻³ at 8+8, a 182× quantum drop) and exactly zero E-key changes (no body enters Jupiter's tidal radius: min gap 0.92 vs 0.18 AU), so 10⁹ belts write ~1.3 B/s (0.05 GB per 100 play-hr, RTF 100), while a 10⁻³ short-period fraction at 1 change/orbit writes 1.16 GB and breaks 4 GiB at f·κ ≳ 3×10⁻³. Reproduced bit-identically; seed-stable ±1%; LL core independently verified. Silver because the hot-tail κ is parameterized, one pre-registered magnitude failed, and the headline rate undercounts converged sampling by 1.5×. Adoption cost ≈ 0: it prices B18b's dynamic rung.

## Reproduction

- `python3 lab/results/20261007-2057-library-26cb/probe_hlive.py` in a clean tree: output **bit-identical** to `probe-out.txt` (9.7 s, deterministic integer bin-change counts). `work/patch.diff` empty; no repo files touched — consistent with the dossier.
- Held out in time: `predictions.md` 21:06:08 < `probe_hlive.py` 21:09:59 < `probe-out.txt` 21:10:08.
- Predictions: P3 held (182×). P2 held in structure but κ is assumed, not derived (author labels this). **P1 failed in magnitude** (predicted 0.01–0.1 bits/orbit; measured 1.43) — honestly reported. By the lab's own precedent (1 Oct red-team: silver, "one held-out prediction failed") this alone caps the grade.
- Controls: μ_J = 0 gives exactly 0.0 key changes (verified). The pre-registered LL control said "within 1%... either control failing ⇒ VOID"; the measured 5.4% is against the *(5/4)α asymptote*, which no exact LL value can match at the belt's α — the 1% threshold was unpassable as written and was silently reframed to "expected ~0.05". My independent check (below) confirms the LL implementation is correct, so this mis-specified control does not poison the result, but the reframe is the r3-v3 class of slip (number disclosed, redefinition not).

## Adversarial cases (5)

1. **Sampling/time-window** (the probe samples 2,000 yr at 10-yr steps; the secular period is 8.6–17.6 kyr, so only 11–23% of one cycle is covered): at 30 kyr with 2-yr steps the 16+16 rate converges to **0.397/orbit vs the reported 0.272** — a 1.5× undercount of re-key *events*. The invariant statistic is sum|d| (total bin-boundary crossings): 0.38–0.40/orbit at every window and sampling tried. Bits/orbit at converged sampling: **1.37** (rate up 1.5×, step entropy down to 1.01 bits), so the pre-registered kill criterion (≥1.5 bits/orbit) still does **not** trip and the GB arithmetic is unchanged.
2. **Seeds**: 0.271–0.273/orbit (16+16) and 1.48–1.50×10⁻³ (8+8) across 5 seeds — stable to ±1% (PRINCIPLES 20 satisfied).
3. **Outer belt a∈[3.5,4.9], e~0.1**: 10,626/20,000 bodies resolve encounters (min conjunction gap −1.66 AU vs 0.29 AU tidal radius) and the L-rate triples to 0.80/orbit. The "exactly zero E-key changes" is specific to a belt truncated inside the perturber's reach — physically why real belts are sculpted, but the rung must pin the belt's radial extent or the zero is cherry-picked geometry.
4. **LL core, independent**: b₂/b₁ over (5/4)α = 0.9987 at α=0.1, 0.966 at 0.5, 0.927 at 0.7 (200,001-point quadrature) — implementation correct; the probe's 5.4% at α≤0.615 is genuine higher-order α terms.
5. **Arithmetic and quotes audited**: 1.28 B/s, 0.046 GB/100-hr, 1.16 GB hot, fκ≈3.4×10⁻³ for 4 GiB all reproduce from the printed lines; all 7 probed lens quotes exist in `highlights.jsonl` (4,580 total).

## Novelty

Genuine. `docs/HISTORY.md` has no prior re-key-rate measurement; HANDOFF line 70 says H_live is "not measured yet". Closest priors: `components-98bc` (static belt program floor, 0.126 bits/body — a different question) and `taleb-09b5` (tail owns the *encounter* rate). What is new: the measured belt distinction rate, the f·κ threshold, and the design rule that the population program must carry the secular phase (PRINCIPLES 3, compute only surprises: the secular cycle is derivable, so storing it deletes the distinction stream; PRINCIPLES 6, store the generator).

## The one experiment for gold

Derive κ on the design's cheap path: measure the re-key rate of a real short-period population under the motion law's own kick layer (plane-scale, frozen key width, converged sum|d| statistic) instead of the κ ∈ {0.1,1,4} parameterization. Then f·κ ≳ 3×10⁻³ becomes a measured gate-able threshold rather than arithmetic on an assumption — the same bar the premise red-team was set (silver until measured on the design's path).

## What the author missed

- The 0.27/orbit headline is a lower bound; converged sampling gives ~0.40/orbit. Report sum|d| — it is the sampling-invariant statistic and the honest event rate for churn accounting.
- "Memo-recompile churn (10⁹ × 0.27/orbit) dominates compute" is overstated: that is ~2 re-keys/s at sim rate for 10⁹ belts, and law.md's cycle memo is shared per (E,L) key, so churn scales with distinct keys, not bodies. The real cost is memory (unbounded scar growth at 16+16 without the secular phase in the program), which the dossier does price correctly.
- The E-key zero's dependence on belt extent (adversarial 3) belongs in "what would make it wrong".
- The pre-registered 1% LL control was unpassable and was reframed without saying so; predictions.md's own rule made that a VOID.
