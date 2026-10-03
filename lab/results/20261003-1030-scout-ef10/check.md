Grade: silver

Abstract: Claim: output-only symplectic correctors (WHFast orders 3–11) cut Jacobi error 6–8× at fixed kicks and buy a solid 2× fewer kicks at a dCJ≤1e-4 gate in the strong-tide regime (m₂=0.3, e≤0.6); 1× at Jupiter-class masses. Reproduced bit-identically (`decisive.py`, 27 s); predictions pre-registered; coefficients, Z-composition and inverse verified against upstream rebound. My attacks: off-grid thresholds 24 (plain) vs ≤10 (order 5) — the 2× is conservative; on a 3:1 resonance order 7 is 2.3× WORSE than plain at n=8; P4 failed at e=0.6 (orders 3/11 worse than plain) yet is reported held. The novelty premise is false: dcdde70 (20261001-2353-q-correctors, silver) already ran correctors, including the output-only form. Gain 2×, not 10×; adoption is a zero-per-kick read-out transform.

## Reproduction

- Clean tree, empty `work/patch.diff`. `smoke` and `decisive.py` rerun: both `results-sweep.json` and `results-heldout.json` are **bit-identical** to the author's; decisive 27.3 s (claimed 26 s). All eight dossier-table cells re-derived from the JSONs (6.1×, 2.6×, 8.0×, 1.1×, 2.1×, 1.7×, 1.0×, 1.2×).
- Prediction timing (mtimes): final `corrector_falsifier.py` …717 → `predictions.md` …767 → `decisive.py` …779 → JSONs …800/…808. Pre-registration real.
- Provenance: the script's coefficients, Z-call order and `inv` convention match **upstream rebound `main`** (fetched fresh), not just the local copy; rebound's own `reb_whfast_apply_corrector` matches line-for-line. Inverse verified independently: corrector(+1) then (−1) returns the state to ≤4.4e-15 while moving it ~2e-4.
- Controls: oracle positive control present; `corrupt3` negative is worse than plain at every fixed n, exactly as the dossier says. P7 verified: `dCJ_last ≤ dCJ_max` in all 216 cases — bounded oscillation, no walk.

## Adversarial cases (mine)

1. **Off the dyadic grid** (m₂=0.3, e=0.2, dCJ gate): plain first passes at n=24 (8.5e-5), order 5 at n≤10 — ratio ≥2.4×. The headline "2×" is honest-to-conservative at e=0.2.
2. **3:1 resonance** (m₂=0.01, e=0.2, a_out=3^{2/3}, untested by the author): order 5/7 at n=8 give gains 0.86×/0.44× — order 7 is 2.3× **worse** than plain. Detuned +6%: gains 2.3–2.6×. Near resonance the corrector silently degrades at coarse n, the same failure signature as the author's own `corrupt3` control, with no detector proposed.
3. **Unshipped claims**: the RK4 true-flow CJ ("1e-13 over 477 orbits") and "200 random drifts, 5e-15" are not in the repo. My reruns: CJ 1.4e-9 at 1024 steps/orbit (step-dependent; h⁴ scaling makes 1e-13 plausible only much finer — state the step); drift roundtrip 1.1e-13, full-period 3.9e-12 over 200 random states. Both claims roughly hold; ship them.

## Novelty — the dossier's premise is wrong

"Queued, never run, no H entry" is false. `git log`: **dcdde70, "lab 20261001-2353-q-correctors-aa78: Grade: silver"** (2 October) ran the same lever on a plane-faithful replica — plain DKD, SABA2/3/4, and Wisdom–Holman–Touma correctors **including `whc3b`, the boundary (output-only) form this run proposes** — and found every kernel floors at 8 kicks/orbit at behaviour gates (1×), with its checker proving the corrector is an exact conjugation: a readout relabelling, verified to 2e-12. No H entry exists in HISTORY.md (it still lists "correctors" as queued-next), but the checker's instructions require searching `git log`, where it is the 9th commit back. The current run's Jupiter-class rows (1×) independently confirm that result from a different toy. What is genuinely new here: the strong-tide μ=0.23 regime (2× at an amplitude gate), the coarse-step non-asymptotic quantification (why 2× and not the literature's 10×), the silent-degradation control, and upstream provenance. Overlap must be cited, not rediscovered.

## Goal fit

Moves live engine question #1 (fewer kicks per orbit at the same behaviour). Fits "Steal what works, from skin in the game" and "Compute only surprises" (paid only at observation). But the binding gate `dCJ_max ≤ 1e-4` is an error-size gate — the author says so themselves — and it is precisely at an amplitude gate that a readout relabelling converts into step savings; at behaviour gates the prior run measured 1×. P4 also does not hold as reported: at m₂=0.3, e=0.6, n=8, orders 3 and 11 are 2.1× and 3.7× **worse** than plain and the orders span 4.4× ("saturate within 2×" holds only at e=0.2). Practical consequence the dossier omits: fix order ≤7 at n≤32.

## The one experiment for gold

The author's own named rung, amended: `q-correctors` on the engine's own law and scenes at coarse n with **both gate flavours** — B12 amplitude/Jacobi AND behaviour gates (B14 precession and e-behaviour, B17 resonance) — plus strong-tide e>0.6 and the resonant case planted as a must-NOT-degrade control (my case 2 shows it must be "must not hurt", not "must not help"). Gold only if the 2× survives the behaviour gates and the corrector deletes the pending-half-kick read-out defect (HANDOFF l.40) at zero per-kick cost on the real kick layer; if the 2× lives only at amplitude gates, it stays a readout fix, not a kick cut.

## What the author missed

- The prior correctors run (dcdde70) — one `git log --grep=corrector` away; its exact-conjugation proof also explains their own fixed-n gains, and its behaviour-gate floor predicts their Jupiter-class 1× rows.
- P4 marked "held" though it fails at e=0.6 (two orders worse than plain); the Evidence line "orders saturate within 2×" is wrong as stated.
- Resonance: they flagged it unverified; it is worse than unverified — active harm at coarse n, invisible without a detector.
- No control isolating the readout: e.g. plain outputs read at the opposite DKD phase, or a slope-only dCJ gate — if either recovers most of the 6–8×, no corrector is needed (prior run's algebra predicts the amplitude gate is doing the work).
- Wall-clock on the real kick layer (29 µs/kick) unmeasured, so "2×" has no engine-time translation; P5's Hill check is convention-dependent (2.65 vs 2.09 or 2.76).
