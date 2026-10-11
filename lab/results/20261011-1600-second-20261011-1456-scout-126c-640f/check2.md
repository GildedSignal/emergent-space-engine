Grade: gold

**Abstract.** The named gold experiment is done and it held. Every `metrics.json` number
regenerates from `python3 falsifier.py` (27 s; two fresh runs bit-identical; E1–E6
bit-identical to the silver's git record; both orphaned keys live). My held-out attacks —
intermediate δ, L̃² ∈ {12.05, 12.5, 14}, kick fracs 0.1/0.5/0.9 — keep the fixed ladder at
≤ 4.2e-7 (m=1, ≤ 57 panels) and ≤ 1.1e-7 (m=2, ≤ 79) at every δ ≥ 1e-8; uniform fails up
to 0.32. Three independent quadratures cluster within 4.5e-7 at δ=1e-10 where DOP853
shifts 4.1e-6: the oracle degrades, not the candidate — measured, not inferred. Gain:
valley at 61–87 fixed panels vs 3765 adaptive; kicks rescued from unusable to 1e-7;
deletes the NoBoundOrbit refusal. Cost: one `crates/space` sector extension, cut rule concrete.

## Reproduction

Clean tree; `work/patch.diff` is empty (no edits outside the run folder). I ran the dossier's commands from a copy in `/tmp` (so the stored record was never overwritten):

- `python3 falsifier.py` twice: 26.7 s and 28.8 s, both exit 0. The two runs are **bit-identical on every key** except `machine`/`wall_seconds`, and identical to the stored `metrics.json` (key sets equal in both directions).
- E1–E6 vs the silver's record (`git show origin/claude/lab-20261011-1456-scout-126c:.../metrics.json`): every prior physics key bit-identical. `separatrix_valley_panels_to_1e-11` regenerates exactly (43/83/133/205/3765) and is now called from `main()`; `bound_control_apo_to_peri` is a live path with all three seeds. The record bottleneck — the taste log's named silver-killer — is deleted for this representation.

Timing evidence for predictions-first: `predictions.md` 16:16:36, `falsifier.py` 16:46:12, `run-log.txt` 16:46:49, `metrics.json` 16:48:00 (mtimes only, as with the silver; consistent). The m=2 rung measurement and the rtol-1e-13 comparison are labeled post-prediction in the code and disclosed in the dossier.

## Held-out predictions

- **P-D (the named experiment): held fully.** Everything regenerates from one command; E1–E6 bit-identical.
- **P-C: held.** All three seeds run; my exact reference below confirms the reported values (and the author's diagnosis of the flat residuals).
- **P-A/P-B: cost held, accuracy failed.** Panel counts 32/41/47/55/61 vs predicted ≈32/38/44/52/58; ≤ 64 panels held; uniform fails at δ ≤ 1e-6 exactly as predicted. But the predicted ≤ 1e-9 accuracy failed by ~1.5–2.5 decades (measured 4.1e-8…3.0e-7 at m=1, 2.8e-8…5.3e-8 at m=2 for δ ∈ [1e-4, 1e-8]), and the predicted Rfun-cancellation floor did not appear. **Every failure is reported with magnitudes in the dossier's predictions section; no pre-registered kill criterion tripped** (the ≤ 1e-6 kill line held at every δ ≥ 1e-8). The claim as shipped is stated at the measured level, not the predicted one.
- P-C's mechanism changed after the prediction (turn-event end + exact root endpoints instead of `r₂+ε`), disclosed and explained.

## Adversarial cases (mine)

1. **The δ grid is not cherry-picked.** Intermediate δ = 1e-3, 1e-5, 1e-7, 3.16e-8, 1e-9 at L̃²=13: m=1 err 5.7e-10 / 4.4e-8 / 2.7e-7 / 3.0e-7 / 4.7e-7 at 37/45/51/53/57 panels; m=2 ≤ 2.8e-9 except 9.1e-7 at δ=1e-9 (non-monotone, still under the kill line). Uniform-64 fails (1.7e-3…0.32) everywhere below δ=1e-4, matching the stated P7 domain.
2. **The layout rule generalizes in L̃².** L̃² ∈ {12.05, 12.5, 14} at δ = 1e-6, 1e-8: m=1 ≤ 3.5e-7 (≤ 53 panels), m=2 ≤ 1.2e-7 (≤ 75) everywhere; σ = C(L)·√δ adapts as the rule intends (C = 23.5, 4.2, 1.6). Deeper terminal r_end = 2.1 at δ=1e-8: unchanged (6.3e-8 at 75 panels, m=2).
3. **Valley kicks beyond the author's fracs.** fracs 0.1/0.5/0.9 at δ = 1e-6, 1e-8, plus L̃² = 14 and 12.5: uniform-64 fails everywhere (1.2e-3…2.5e-1); the fixed ladder m=1 ≤ 4.2e-7 at ≤ 53 panels, m=2 ≤ 9.7e-8 at ≤ 71 panels. Against my own r-quadrature truth for the kick leg (self-converged 2.7e-10 at δ=1e-6), the ladder errors are real candidate errors, not oracle artifacts (oracle sits 1.4e-10 from my truth there).
4. **The δ=1e-10 truth-limitation is real — the oracle is the outlier.** Three mutually independent evaluators — the candidate ladder (fixed η-cuts), my θ-substitution quadrature (r = r₃ − span·sin²θ, factored R with the turning-point factor exact, geometric rungs in θ, self-refined 256→1024 panels), and scipy's adaptive quad — agree within 4.5e-7 at δ=1e-10, while DOP853 rtol-1e-12 sits 6.6e-6 and rtol-1e-13 sits 2.4e-6 from that cluster, with its own 4.1e-6 tolerance-to-tolerance shift. At δ=1e-8 and 1e-6 the oracle and the quadrature cluster agree to ≤ 4.5e-9, so the shared R-algebra is not the explanation. The dossier flagged this as inference; it is now measured. The candidate's true δ=1e-10 error is ~5e-8 (m=1), i.e. the run *understated* its own accuracy at the deep end.
5. **The bound-control residuals are the reference's floor, proven.** My exact factored rquad (both turning points absorbed via sin²θ/cos²θ, no Rfun cancellation; self-converged to ~1e-15) shows the candidate at 2.3e-13…9.9e-12 (mid-field / near-Vmax@16p), while the author's Rfun-rquad4096 sits exactly the reported flat residual from exact (4.56e-10 mid-field). The oracle's turn-event floor on the near-circular seed is 3.7e-7 from exact — the author's √δ-amplified floor attribution (predicted 4.2e-7) is confirmed digit for digit.
6. **Safety/base/m invariance:** safety=4 changes nothing (identical errors, +4 panels); base=64 does not fix the m=1 error level (confirming "the transition rungs are the limiter") but costs 95–107 panels; m=4 adds nothing over m=2. All as the dossier states.

## Novelty

The new element over the silver is the rescue measured on the law's **fixed** cut layout — exactly what the silver's checker flagged as unmeasured ("adaptive float bisection, not the law's fixed integer cuts") — plus the live record and the valley kicks. The pattern is the law's own (law.md:20 "band edges are cuts in ψ"; B9's 2m·log₂ budget), applied to distance-from-barrier-top; no valley-ladder or cosh-branch band layout exists in docs/HISTORY.md or ENVELOPE.md (which still declares plunges outside the compiler, line 93–94; HISTORY:3176 "plunge orbits have no tube"). The oracle-degradation finding is new.

## Goal fit

Board item "plunge and radial tubes"; deletes the NoBoundOrbit refusal class with a concrete, fixed-function-of-(E,L) cut rule (base 32 + dyadic rungs to σ/2, σ from the complex root pair, η(r_U) from the critical radius — all integer-law-native, degenerating to the uniform base when no valley). Principle 19: the fix is the law's own geometric bands, not a new category. Principle 13: fixed cuts ⇒ identical error every evaluation; it does not compound. Principle 34 cuts the other way, in the run's favour: the oracle's degradation near the barrier top must not lead the representation — and the run refused to let it.

## Why gold, and the blemishes

Gold because: the named experiment is delivered in full and verified; the record is perfect (two fresh runs, prior record, key sets — all identical); the shipped claim survived every held-out attack I could mount, including configurations the author never ran; the premise correction (oracle degradation at the barrier top) is independently established; adoption is one step. The failed ≤1e-9 accuracy predictions do not block gold: they were the author's a-priori GL4 convergence estimate, failed in the safe direction (predicted better than measured; claim restated at the measured level; kill line held under a wider envelope than the author's own), and the run reports them as failures with magnitudes. The silver pattern in the taste log — record defects, undisclosed redefinitions, misses reported as held — is absent here.

## What the author missed

- **The valley has a bound-side twin the layout does not cover.** The ladder is cosh-branch-only; a bound orbit just *below* Vmax degrades on uniform cos panels: my Vmax(1−1e-6) seed gives 7.5e-5 at 8 panels (3.2e-9 at 32). The B9 budget absorbs it today (32–64 panels), but the builder should know the same bands are needed on the cos branch as E² → Vmax⁻, or state the budget growth.
- **δ=1e-9 quantifies the "m=2 measured, not derived" risk:** m=2 reads 9.1e-7 there — non-monotone (17× worse than at 1e-8) and 10% under the kill line. The builder's re-derivation of the per-octave rung count from the panel-error budget is load-bearing, not polish.
- **The trap is on the wrong branch as described.** The shipped clamp already returns *exact* η at cos-branch turning points (measured 0.0 and π exactly, τ penalty 0.0); the sharp trap is cosh-only, and it is a hard `None` (cosh-domain exit at the turning point, at both δ=1e-4 and 1e-8), i.e. a crash for a builder, not a ~1e-7 error. The guidance ("use the turning points directly") is right; the diagnosis should name the cosh branch.
- **The bound-control path evaluates R via Rfun, not the factored form** used for the valley; at very near-circular seeds the candidate's own floor grows (3.3e-8 at 64 panels at Vmin(1+1e-6)). The factored form would remove it.
- One loose sentence: "under both the P2 budget (96) and B9 (~78) throughout" is true for the pre-registered m=1 (max 61) but m=2 reaches 87 (>78, <96) at δ=1e-10. The table shows it; the wording does not.
