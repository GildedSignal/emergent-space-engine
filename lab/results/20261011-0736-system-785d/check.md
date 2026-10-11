Grade: silver

**Abstract.** Claim: the resonance gate is one certificate, excursion(δ) = min(2·ṗ_coh/|θ̇(δ)|, c_H·μ^(1/3)), from numbers the engine already computes, deriving B17's W = 2.5·μ^(2/3) as the crossing of its two terms. I reproduced everything bit-exactly in a clean tree (quad, calib, two held-out scans, every final.json number, κ, W, boundary) after re-deriving the author's c_H definition. ṗ_coh is exactly μ-linear; P4a (never under-predict) held at 0 violations, also with the capped form. But the headline capped law is post-hoc (P1 as written failed, 165 violations; the cap is fitted on the same truth at δ=0), and my adversarial cases show the domain is narrow: at 3:2 μ=3e-3 it under-predicts 16× and degenerates to "unsafe everywhere"; at 4:3 μ=3e-4 the guard itself fails (4 cells); at 4:3 μ=1e-3 the μ^(1/3) cap breaks (c_H = 18.8, e→ejection). Adoption cost: engine wiring unmeasured. Silver: real, honest, one experiment from gold.

## Reproduction (clean tree, /tmp copy, OUT patched)

- `selftest`: passes (μ=0 ringing 4.395e-4 vs pred 4.386e-4, no drift).
- `quad`: **bit-identical** to quad.json; ṗ_coh exactly μ-linear (7.311e-4 / 2.437e-3 / 7.311e-3; ratios 3.333, 10.0).
- `calib`: **bit-identical** (all six far bands, negative control frac_fail 0.875, T_agree 34.5).
- Fresh scans of two held-out cases (j2 μ=1e-3, j1 μ=3e-3): band, theta_net, Tage, emax **all bit-identical** to the saved npys.
- final.json: **no shipped script generates it** (see below), but I independently reproduced every number: c_H and cH_spread exactly (definition recovered: median band at exact resonance ÷ μ^(1/3), c_H = mean over μ); capped-law per-case and ALL (n=327, med 0.884, p10 0.426, p90 1.137, 99.39%; the two outliers are F=0.24 safe-side and one F=3.42 in j2 μ=1e-3); P4a = 0 under **both** the uncapped and my capped recomputation; κ(q=0.0096) = 2.98/3.48/6.40/5.62/11.13; W = 0.0100/0.0230/0.0229 vs B17 0.0112/0.0250/0.0112; regime boundary meas/pred = 1.20/1.04/0.52 (definition: outermost δ with circ_frac ≤ 0.5).
- predictions.md mtime precedes all four held-out scan files; the calibration case (j1 μ=1e-3) was scanned before predictions, and predictions.md discloses this. patch.diff empty — nothing outside the run folder touched.
- Truth robustness (author's admitted gap): half-step rerun (j1 μ=3e-3, 5 detunings) — bands match to 0.3%. The bands are converged, not step artifacts.

## Predictions

- P1 **failed as written** (165 violations — the 1/|θ̇| law over-predicts up to 500×; all violations are on the safe side). The capped form that headlines the dossier is post-hoc, fitted on the same scans it is scored on. Reported honestly, but it is a diagnosis, not a held-out prediction.
- P2: held-out medians 0.64 / 1.02 / **0.486 (below the [0.5,2] window)** / 0.96 — 3 of 4 pass, one marginal fail. As reported.
- P3 **failed 3 of 4 held-out** (κ = 6.40, 5.62, 11.13 vs [1,4]). The dossier's "2 of 4 held-out cases pass" is wrong: it counts κ=3.48 from j1 μ=1e-3, the calibration case. Held-out truth: **1 of 4**.
- P4a **passed** (0 violations; I re-verified with the capped form — the q_e/2 margin absorbs the one 3.4× under-prediction).
- P4c: held for 2:1, 2× off at 3:2 — but "within 20% and 4%" is grid-resolution luck (detunings log-spaced ×2; the honest bound is one grid step).
- P5 untested (author says matched pairs sit in the saturated zone where the cap is symmetric by construction).

## Adversarial cases (four of my own)

1. **Missing corner 3:2 μ=3e-3** (author ran only its far control): ejection regime (emax up to 2.1e4 from e₀=0.02; Edrift 4e-12, so physics). Certificate under-predicts the excursion **16×** at exact resonance (band 2.13 vs cap 0.135); coverage 0.26. P4a stays 0 only vacuously: the cap exceeds qgrid/2 everywhere, so the certificate says "unsafe" at every detuning — safe as a switch, zero changeover/cadence information. The author's caveat anticipated this; the headline does not carry it.
2. **New family 4:3, μ=3e-4**: c_H = 0.78 (O(1), quadrature re-run), coverage 0.85 — but **4 P4a violations**: the guard itself under-predicts at 4 (δ, q_e) cells. The certificate is not guard-safe outside j ∈ {1,2} even with a re-fitted constant.
3. **4:3, μ=1e-3**: c_H = 18.8 (vs 0.78 at μ=3e-4) — the μ^(1/3) saturation is gone (e pumps to ~1.9, near-ejection); coverage 0.43. The two-term form breaks at resonance overlap.
4. **e₀=0.05 at 2:1 μ=1e-3**: c_H = 1.04 (7% from 1.117), coverage 1.00, P4a = 0. Robust in e₀ — the breaking axis is resonance strength, not eccentricity.

## Novelty

B17's W = 2.5·μ^(2/3) is the live convention (law.md: "detuned by thirds of the half-width W = 2.5·μ^(2/3)"); H0203 established "resonance kills averaging"; r4 v2/v3 killed first-order kick layers and chose the rotating binary doll for the zone. No prior entry derives the gate's width or expiry from the engine's own quadrature; the crossing-derivation of the μ^(2/3) scaling is new and genuinely elegant (ṗ ∝ μ, cap ∝ μ^(1/3) ⟹ δ* ∝ μ^(2/3)). The unification framing (quantum ÷ rate = cadence/jet re-anchor/slack) is the board's culture; the resonance gate joining it is the new claim.

## Goal fit

Aims at board focus lines 1–2 (changeover near a secondary; fewer kicks) and would delete the resonance classifier + width table (principle 1; "regimes are chosen by dimensionless numbers", 4). Respects the guard philosophy (34). But the deletion is not yet clean: c_H is per-family and per-geometry (my 4:3 runs show a table by stealth or a per-geometry quadrature re-derivation), the guard property does not extend to 4:3, and the engine-facing premises (θ̇ from compiled frequencies; ṗ_coh = the kick layer's own orbit-average) are asserted, never measured against the plane or the law. Float probe; the integer law must re-derive c_H (acknowledged).

## The one experiment for gold

Wire the certificate into the engine's cheap path — the plane's kick layer — and run B17's gate on r4 v3's cases with the classifier and the W table deleted: switch to the binary doll exactly when excursion ≥ q_e, ṗ_coh taken from the kick quadrature the engine already computes (zero added work), c_H re-derived per geometry by that quadrature. Gold if behaviours (pump ratio, regime match, controls) are unchanged and a 4:3-class geometry either passes or the certificate fails safe there by construction.

## What the author missed

- **final.json has no generating script** — the record lesson of 5 October (results the shipped code cannot regenerate keep runs at silver). Every number in it is real (I reproduced them all), but the record does not show it.
- The P3 "2 of 4 held-out" count includes the calibration case; held-out truth is 1 of 4.
- The 327-system headline includes the calibration case (held-out only: 270 systems, 99.3% — immaterial, but should be stated).
- The negative control's frac_fail 0.875 against the code's own "must be 1.0" was not flagged.
- No 4:3 or overlap-corner scan: the guard fails at 4:3 μ=3e-4 and the certificate degenerates at 3:2 μ=3e-3; "one constant per resonance family" is falsified one family out.
- P4a's power is grid-scoped: qgrid stops at 0.16; at design quanta ≥ 0.27 the corner case would violate. "Never under-predicts" should carry that bound.
- The regime-boundary precision claims (20%, 4%) should be "within one grid step" (×2 spacing).

## The lens

A whole-system lens found a real unification and was candid about its own over-claim risk (the 3:2 miss is in its data). What the lens hid: the unification is family-local (2:1/3:2 below overlap), and the zone's interior clock (κ), the piece that would make it "one arithmetic" everywhere, is exactly what failed. The elegant crossing is least reliable where encounters are strongest — the same edge where the co-orbital certificate (20261006-0346) broke. Two certificates now fail in the same direction at the same edge; the motion-law v2 design should treat strong-resonance geometry as the certificate's declared domain boundary, not a tuning case.
