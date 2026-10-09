Grade: silver

**Abstract.** Claim: in a program+scars belt, live bits per body grow ½·log₂k (identity-tied) and ≈¼·log₂k (interchangeable), so 10⁹ bodies fit in 8 GB with the tie fraction f_tie as the knob. Reproduced bit-identically (all 8 JSONs, sizing table, budget boundary k≈1.9×10³, traffic 0.07–0.7 MB/s); held-out seeds confirm the laws. Adversarial: the √k law survives a 10⁶ tail range (slope 0.532). But the 8.3-bit 2-D coupling is a plug-in ceiling artifact (independent control reproduces 8.4; true MI is 0.31 and 0.005 bits by Kraskov), the no-program control is misreported (11.04–11.83, not flat 11.0), and the multiset law is n-dependent (4.55→3.16 bits, n=2¹⁴→2¹⁷). Gain: B18's floor becomes computable (15–25 vs 157 bits/body). Adoption: no code; fix three record defects.

## Reproduction

Clean tree (/tmp/chk8fb8), `patch.diff` is empty. `main`, `heldout`, `twodim`, `kickentropy`, `size.py`: total 231 s, every command ≤ 60 s. All 8 `mc_*.json` **bit-identical** to the author's. `size.py` regenerates the dossier's sizing table (65.5/76.3/101 b at f_tie=1; 20.4/24.3/33.6 at 0.1; 15.4/18.6/26.2 at 10⁻³), the boundary (k=1.9×10³ encounters = 1.7×10³ orbits) and the traffic numbers. Verified from the shipped JSONs: H_A slope 0.498–0.501 (analytic 0.500, intercept 5.05 = log₂(√(2πe)·σ₁/δ)); H_multiset slope 0.172–0.283; gap at 2¹³ 7.47–8.45; Rutherford inflation 1.08; δ-halving +0.96–0.99; created:retained tied 3.14–3.58×10³.

**Prediction discipline holds.** predictions.md rev 2 at 16:09:11, script finalized 16:11:20, every decisive JSON ≥ 16:11:53 (mtimes). Seeds 2–3 were genuinely held out and confirm P1, P2 (k ≥ 4), P3, P4, P7-ratio.

## Adversarial cases (mine)

- **A1 — the 2-D "penalty" is an instrument artifact.** The author's H_A_2d sits at 16.717 bits for all k ≥ 2¹⁰: exactly log₂(65536) + (N−1)/(2N·ln2), the plug-in ceiling when all cells are singletons. An independent control (separate Poisson counts, independent kicks, ρ=0) shows the same spurious "penalty": 0.10 bits at k=2⁶ growing to **8.40 bits at k=2¹³** — indistinguishable from the author's 8.33.
- **A2 — true mutual information (Kraskov k-NN, no bins, control −0.012).** The author's exact processes at k=2¹³: gauss (ρ=−0.6, shared count) MI = **0.313 ± 0.004 bits** (analytic 0.322); rutherford (shared heavy-tail amplitude) MI = **0.005 bits**. The shared Poisson count carries ≈0.003 bits at k=2¹³ (spread √k/k = 1.1%). So P5 (0.3–1.5 bits, never super-additive) **held**; the reported miss, its "shared encounter-count latent" explanation, and the design consequence "joint scar code ~2× cheaper / 5×H_A conservative by ~2×" are artifacts. The elements are near-independent; ≤0.3 bits per pair are harvestable.
- **A3 — the multiset law is n-dependent.** Same seed, k=2¹³: H_multiset = 4.55 (n=2¹⁴), 4.07 (2¹⁶), 3.16 (2¹⁷); at k=2⁶, 2.93 → 1.87. Quantile residuals scale as σ_k/√n, so "0.216·log₂k + 0.89" is a law at n=2¹⁶, not of the store. Direction: conservative for populations ≫ 2¹⁶, ~0.5 bit optimistic at n≈2¹⁴; the population granularity assumption is never stated.
- **A4 — tail extreme.** Rutherford with u_min=10⁻⁶ (kick range ~1000σ₁): slope 0.532, inflation 1.35 bits at 2¹³. The √k law is robust; the kill criterion (slope ≥ 0.8) is far away.

## Novelty and goal fit

HANDOFF (6 Oct): "Distinctions created per game-second (H_live) … not measured yet" — this run measures exactly that, a live board item (`b-h-live`). Nothing in HISTORY measures steady-state live-bit growth: opus-shipmem's 488 B/10⁶ is static cost, components-98bc's 0.126 b is births, H2557's ~4 bits/collision is the dense-gas regime (correctly set apart by the author). PRINCIPLES 24: "this is nowhere near the floor on the size and information theory says so" — the floor now has a measured growth law, log, not linear; the 157-bits/body fear is deleted (~10×). Principle 5's bounded player influence becomes the f_tie knob. Fit is direct.

## Why silver, not gold

The headline (H_A ½·log₂k + constant, verified analytic, 3 seeds and a 10⁶ tail; f_tie decides the 10⁹ verdict; all sizing arithmetic regenerable) survives every attack. But the record fails gold on three points:

1. **A control is misreported.** "no-program control ≈ 11.0 flat | 11.01–11.05 flat": the shipped JSONs say 11.04–11.83, rising ½ bit per doubling for k ≥ 2⁹ (σ_k overtakes the birth spread — itself informative: the program's per-element saving dies as ½log₂(1+σ_gen²/σ_k²) → 0). "11.01" appears in no shipped JSON. P6 failed at large k and is reported as held.
2. **An artifact is presented as understood.** "Cause, understood after the run" — the cause is the estimator's log₂N ceiling (A1/A2). The prediction was right; the measurement, the explanation, and the "~2× conservative" consequence are wrong.
3. **The multiset law is stated without its n-dependence** (A3).

Minor: gap lower bound 7.5, not 7.6; multiset created:retained range is 8.8–12.0×10³ (gauss seeds 2–3 give 10.6 and 12.0×10³), not 8.8–10.2×10³; h_kick measured 4.84–5.05 bits against P7's predicted "≈ 2–4 bits" (an unreported miss); "~56 s per pass" vs ~26 s measured; `run.log` is empty; `size.py` cites an `analyze.py` that is absent.

## The one experiment to gold

Re-measure the two defective instruments and restate: (i) 2-D coupling by a ceiling-free estimator (Kraskov MI, as here: ≤0.35 bits per element pair), deleting the joint-scar-code consequence; (ii) H_multiset across an n-sweep with the population granularity stated (the law's constant is −½log₂n plus an n-free term); (iii) the no-program control over the full k range. No new physics is needed; the claim, the verdict and the sizing stand.

## What the author missed

- The plug-in 2-D entropy cannot exceed log₂N + Miller–Madow; any "correlation penalty" growing with k from an N-capped estimator is self-refuting. A one-line ceiling check would have caught it.
- The author's own P5 was correct and the honest miss report threw away a right prediction — the cost of not testing the instrument against an independent control (the lab's "controls on both sides" rule, applied to estimators).
- The multiset branch conflates the store's law with the sample's law (n-dependence); population granularity (how many bodies share one program) is a first-order parameter of the sizing, not a footnote.
- Did not report that h_kick landed above its predicted band, nor that the no-program control curves upward exactly where the program stops paying per element (k ≳ 2¹²) — the more interesting statement of that control.
