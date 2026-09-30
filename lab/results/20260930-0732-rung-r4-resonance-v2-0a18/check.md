# check.md — rung r4 v2, run 20260930-0732-rung-r4-resonance-v2-0a18 (checker: independent GLM)

**Verdict (lab/verdict.py, on my reproduced metrics-check.json, bit-identical to the author's): KILL — no candidate passed; killed: arc-g8, arc-g16, arc-g8-half. Positive control passes; both negatives fail as required. No DISPUTED outcomes.**

## Abstract

First-order arc-integrated (Gauss–Picard) conjunction kicks cannot reproduce 2:1 mean-motion-resonance behaviour: they over-pump eccentricity 2.4–4.5×, the resonant angle circulates (libration ratio 0.02–0.09), and spurious resonance appears at 7.5 % detuning (controls 1/3). Everything reproduces bit-exactly from the author's scripts; my independent reimplementation of the law, my DOP853 oracle check, and my finite-difference audit of the Gauss rates (3×10⁻⁷) all agree. My adversarial window-refinement study strengthens the kill: even at 512 kicks/orbit the layer converges to a limit that still over-pumps ~2× — the failure is structural to first-order-in-μ arc integration, not to quadrature or window scale. Cost of adopting: none (nothing adopted); the truth ladder, validated rate layer and control behaviour are reusable. Bottleneck #2 updated: the event layer needs intra-window phase feedback.

## Reproduction

Clean scratch copy, author's commands unmodified. All 5 law JSONs, `ic-scan.json`, and all 40 `samples/*.npz` arrays **bit-identical**; truth JSONs identical in every physics field (emax/emin/R/n_samples); `metrics-check.json` written from my run is bit-identical to `metrics.json`. Round-trip gate 1.128×10⁻¹³ (< 10⁻¹²). `predictions.md` (07:54:21) precedes every sample and summary (≥ 07:54:27); its four predictions held in direction and mostly in magnitude, including the two honest misses the dossier reports (control fraction 1/3 not 2/3; `averaged`'s spurious lib pass).

**One undisclosed fix, reported as required:** running `r4v2.py truth` today yields `windows: null, orbits: null` in the truth JSONs, which crashes `metrics.py` (TypeError). The author's truth JSONs carry `windows: 0, orbits: steps/nsteps` and all three have mtime 07:57:44 (within 1 ms of each other, after the samples and after `metrics.py`'s own creation) — they were patched post-hoc to make `metrics.py` run, and the dossier's command list does not reproduce without that patch. Physics unaffected (windows=0/orbits only feed `kicks_per_orbit` = 0 for the positive control either way); I replicated the patch explicitly in my metrics-check computation. The dossier should have disclosed it.

## Independent audit of the implementation

- **Gauss rates:** all four rates match centered finite differences of my own restricted acceleration (direct + indirect), DOP853-graded, to ≤ 4×10⁻⁷ at three geometries — including `rate_M` after correcting my first comparison (the author's rate excludes the Keplerian n, as it should).
- **Truth oracle:** leapfrog-1200 vs my DOP853 (rtol 10⁻¹², my own heliocentric equations): max |Δe| = 6.7×10⁻⁵ over 20 synodic, emax 0.13172 vs 0.13169, R 0.8450 vs 0.8451, φ to 1.5×10⁻³. Ladder extended: truth-4800 vs 2400 emax 0.131735 vs 0.131743. The oracle is right, not merely self-consistent.
- **Law:** my from-scratch window loop (only `gauss_rates` and GL nodes shared) reproduces the author's arc-g8 to all digits on all five cases (emax, R, window counts).
- **Micro-windows:** at q = 5.00, 796 of 996 window ends are < 0.05 synodic; their median |Δe| is 2.4×10⁻⁸ of a real conjunction kick (author claimed ≤ 10⁻⁶). Count inflation only.
- **Assembly:** JSON summaries consistent with the decimated npz arrays (gaps ≤ 2×10⁻³ rel., decimation as expected).

## Attack

1. **Window→0 refinement (decisive).** Fixed windows per synodic, q = 2 base: pump ratio 5.84 (1 kick/orbit) → 1.49 (4) → 1.20 (16) → 1.19 (64), and K = 256 vs 1024 give the *same* trajectory — the layer converges in K to a limit that still over-pumps ~2× in e-growth within 10 orbits. Single-window flow map: exact at generic phases (ratio → 1.0000 as h→0), but carries a constant-in-h **+5.8 % bias exactly at conjunction-phase windows** (both Δ's scale h²). So the failure is structural — the h→0 limit is the first-order-in-μ solution, which at exact resonance lacks the self-limiting phase feedback. This confirms and sharpens the dossier's mechanism; it also explains arc-g16 pumping harder than arc-g8 (better quadrature of the wrong limit).
2. **The rung's w₂ = 4.0 case.** The rung froze "truth has libration concentration 0.867"; the author's radian reading gives R = 0.227. Of my interpretations, λ₂₀ = 4° gives R = 0.830 (closest); ϖ₁₀ = 4 and λ₁₀ = 4 give 0.05/0.03. The author's case is not the rung's intended one and the mismatch is not flagged in the dossier. Verdict-robust anyway: arc-g8 on the 4° case over-pumps 3.86× with lib ratio 0.041, and the author's IC scan shows 2.4–4.5× over-pump at every phase.
3. **Extremes.** e₁₀ = 0.2: pump 1.18 (passes pumphi) but lib 0.083 — still fails. m₂ = 3×10⁻⁴: pump 1.32, lib 0.79 — still fails, marginally; the failure softens as μ→0, consistent with a first-order-in-μ structural bias.
4. **Metric degeneracy (author's claim verified).** At exact q = 2, `none` gives R = 1.000 (φ frozen, drift 0.00 rad) and `averaged` R = 0.937 with halves 0.985/0.983 and net drift −1.23 rad: slow circulation masquerading as libration. Both negatives still fail pump, so no VOID, but future rungs should detune or use libration amplitude.

## Novelty and fit

r4 v1 killed instantaneous per-conjunction kicks; the red-team (silver) named arc-integrated kicks as the experiment that would decide its "kicks survive" half. No HISTORY entry covers the arc-integrated variant (H0190 K2 is the averaged control, reused here as the negative). This run kills it on the design's own cheap path — new, and it deletes the whole first-order-jump event layer for resonant scenes. Fit: "A failed experiment kills that configuration, never the method" (#9); the surviving pieces (validated rate layer, truth ladder) are exactly what the method keeps.

## What the author missed

The λ₂₀ = 4.0 rad vs the rung's 0.867-concentration case (fidelity gap, unflagged); the undisclosed JSON patch; and the refinement study that would have turned "conjunction windows are too coarse" into "first-order arc integration cannot self-limit a resonance at any window scale" — the kill's real content, and the fact the next rung should be designed around (second-order/phase-feedback windows).
