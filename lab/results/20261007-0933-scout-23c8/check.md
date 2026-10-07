Grade: silver

First H_live measurement, reproduced exactly and extended. Secular-belt scars saturate at ~6 bits/body (q=1e-6) within 2 orbits and then create ~0 bits/body/orbit — still flat at 64 orbits when re-run by this checker; resonant ~0.13, encounter ~0.3–0.6 bits/body/orbit bursting at encounter epochs. The 64-bit/10⁹ budget holds in every regime measured, and shipmem's form-chooser can read stationary scar entropy + q-slope. But the load-bearing surprise — "stable chaos, T_Lyap ≈ 1.2 orbits with flat memory" — is an instrument artifact: the Benettin shadows integrate a different map from the main bodies (drift at updated ash^-1.5 vs main's birth-frozen n; both half-kicks at the end epoch). An honest same-map shadow gives λ ≈ 5×10⁻⁴/orbit (1700× smaller, 0% saturation), consistent with real-belt T_Lyap of 10³–10⁵ orbits. Every λ/KS number in the run is invalid. Adoption cost: the ~200-line instrument plus a rule, no engine code.

## Reproduction

Clean tree, `work/patch.diff` empty. Ran S0, S1, S2, S3 fresh (numpy 1.26.4, same machine class): every printed number and JSON field matches the stored results to displayed precision (S1: H(1e-6) 6.046→6.160, p99|ΔE| 1.3e-5 flat, λ 0.8601, sat 0.984, Pesin 1.207 bits/body/orbit; S2: H(1e-4) 5.77→9.46, p99→3.5e-3; S3: bursty H, enc_frac 8.5/24.5/45.5%). Deterministic (seed 7). One disclosure note: the stored S0 JSON predates the final `h_live.py` (it lacks `frozen_frac`, which the shipped script writes; mtimes: S0 at 9 min, script at 4 min). Shared-key numbers regenerate identically, so the edit was benign — but the stored S0 is not byte-regenerable by the shipped code.

## Predictions

`predictions.md` (9 min) predates the decisive scenes S1–S3 (3–2 min); P0's control ran at the same minute. Scoring against the letter: P0 **failed as written** (predicted H ≤ 0.05 bits; instrument floor is 1.06 bits from two-sided float-noise straddle — benign, but the dossier marks P0 ✓ by redefining "zero" without saying the threshold was missed). P1's λ half: the 60× failure is real in the data but misdiagnosed (see Attack). P2 mostly ✓ (clamped-count prediction failed; disclosed). P3 ✓, P4 (the money number) ✓, P5 ✓ with a caveat (S1b occupied 5387/8192 at q=1e-7 — near the 13-bit sampling cap, biasing that slope point down).

## Attack

1. **Honest-shadow control (decisive).** Patched the shadow step to the main bodies' exact map (kick at epoch t, drift at birth-frozen n, kick at t+h). Same 1e-9 offset, same scene S1: λ_median 0.0005/orbit (was 0.8601), saturation 0 (was 0.984). The two maps' drift rates differ by 1.5·Δa/a; with p99 Δa ≈ 2.6e-5 the phase walk over 16 orbits predicts an apparent λ ≈ 0.95/orbit — matching the measured 0.86. The artifact also explains S1b (0.88) "identical off-resonance": both are the same artifact, so the claimed kill of the 12:1-MMR hypothesis is void. S2/S3 λ values (1.17, 1.92) come from the same broken pair; S3 may be genuinely chaotic (encounters), but these numbers cannot say.
2. **Step-halving** (N=2048, 120 vs 240 steps/orbit): λ 0.8835 vs 0.8837 — h-independent, consistent with a rate-mismatch artifact (h-independent by construction) and ruling out kick-epoch discretization; resolved by (1).
3. **64-orbit long run** (N=2048, original script): H(1e-6) 6.18→6.30 flat through t=64, p99|ΔE| flat — the saturation claim survives 4× the author's window; no Arnold-diffusion onset.
4. **Sampling cap in S2:** H(1e-5)=12.84 with 7549/8192 occupied cells — at the cap; the dossier's S2 claims correctly use q=1e-4, but the cap deserved a flag.

## Novelty

`docs/HANDOFF.md:69`: H_live "not measured yet"; `docs/law.md` defines scars, `docs/plane.md` names the gate, no HISTORY entry measures entropy or distinction rates. First measurement; not a redo.

## Goal fit

Moves the named board item "fitting 10⁹ in 8 GB … decided by distinctions created per game-second" and answers the HANDOFF risk. Principle 24 ("the memory floor is information-theoretic") and principle 6 ("Store the generator, not the generated") are directly served. Floats exploring with behaviours judged (growth laws, tails) respects "floats may explore; only integers decide canonical outcomes".

## Why silver, not gold

The entropy core is real, reproduced, and first-of-kind, and the money number (P4) holds. But the claim sentence's surprise — stable chaos with T_Lyap ≈ 1.2 orbits — is an instrument artifact, and the run's most interesting inversion ("H_live is not the KS rate") was supported only by that artifact: with honest shadows there is no measurable chaos in S1 at all, so the contrast is undemonstrated, not established. A load-bearing false physical claim bars gold.

## The one experiment that would make it gold

Fix the shadow map (identical to the main map, as in this check) and re-measure λ per regime — S3's encounter belt plausibly has real λ>0; if any doll shows genuine λ>0 with flat scar memory, the KS-vs-scar inversion is demonstrated rather than assumed. Add conditional entropy H(scar | birth a,e) (binning the already-stored data) so the form-chooser reads the true floor.

## What the author missed

- The shadow/main map mismatch — the run's central surprise is a bug, though every scar number survives untouched.
- Marginal vs conditional entropy: in a quasi-periodic doll the scar is a smooth function of birth elements, so H(scar) is an upper bound; principle 24's "floor per doll is the stationary scar entropy" overstates it — a program that stores the function absorbs the 6 bits. The dossier notes this only for the transient.
- The 1.06-bit control floor contradicts P0's written 0.05-bit threshold; the mismatch was visible in the author's own first run and was silently re-passed.
