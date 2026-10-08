# check.md — 20261008-0458-second-20261008-0338-library-f045-0102

Grade: silver

**Abstract (for the integrator).** Second-author kill of yesterday's library-run measurement (A(τ) crossing 1 at 0.17–0.25 Hill radii, "on top of r9's τ₀"). All three defects reproduce exactly: vr-flip at 71.7–75.2% of steps (drift control 3.141 rad broken vs 9.6e-7 fixed), the 180° start teleport (fires at τ = 0.25: 183.6° vs 3.6°), the 2π mislabel (6.28 and 100.5 kicks/"orbit"; 47.75 true orbits for "300"). The decisive v2 sweep regenerated bit-for-bit (4 of 7 rows inside my window; medians 0.849…0.567, non-monotone, frac>1 ≤ 0.67). My attacks confirm the kill: v2's Kepler = 1e-12 vs 2M-step RK4; interleaved 24-phase and μ = 1e-2 grids show no τ-crossing anywhere. Silver for two overgeneralized dossier claims; adopt the kill (zero cost).

## Reproduction (clean tree /tmp/check; `work/patch.diff` is 0 B — nothing to apply)

- `shock_probe.py` here is byte-identical to the original branch's published copy (`git diff` clean vs `origin/claude/lab-20261008-0338-library-f045`), so the audit targets the real artifact.
- `python3 shock_probe.py` (28 s): the original row digit for digit — A(1/16) = 0.45, 0.80, 0.75, 1.68 at τ = 0.05/0.10/0.17/0.25 (0.86, 0.88 at 0.35/0.50).
- `python3 control_p1.py`: worst |Δω| over 4800 drift steps = **3.141e+00** (broken) vs **9.602e-07** (fixed). `v2_controls.py`: (a) 7.464e-08, (b) 2.005e-16. `flip_rate.py`: 71.65–75.23% across the grid. `single_case.py` at M0 = 4.651: vel_err 1.521e-02 = 2|vr|, position 1.1e-9, a and e exact — the mirror-state corruption exactly as described.
- `python3 sweep_v2.py fixed 300`: rows τ = 0.05/0.10/0.13/0.17 **bit-identical in every column** to `sweep_fixed_300.log` (0.849, 1.236, 2.078, 0.567; quantiles, frac>1, medErrs all match). τ = 0.20/0.25/0.30 did not finish inside the 45-minute window; same code, same numpy 1.26.4, 4/4 bit-match — divergence is not a live concern, but I record it as partial.
- Defect 3 re-derived by my own arithmetic: GM = 1 → T = 2πa^1.5, so K = 1 is 6.28 kicks/orbit, K = 16 is 100.53, "300 orbits" is 47.75 — the dossier's numbers exactly.
- Defect 2 re-derived by my own script (below): real, deterministic, reach corrected.

## Predictions

`predictions.md` + amendment mtimes precede every decisive log (sweep +25 min, horizon +13, φ0-detail +9, conv +3); `run.log` is 0 B again, so mtime order is the only trail — the same weakness the first checker named, repeated. Held: P1 exactly (3.141 vs 9.6e-7); P2' (published row does not regenerate on v2: 0.102, 0.945, 0.093, 3.402); P4' (150 vs 300 orbits within factor 2, worst 1.96 at τ = 0.17); amendment controls (a), (b). **Failed, disclosed:** P3/P3' point estimate — medians 1.236 and 2.078 at τ = 0.10/0.13 (predicted < 1 everywhere, 0.2–0.9), frac>1 up to 0.67 (predicted ≤ 1/3). The decisive pre-registered content — no phase-robust crossing at 0.17–0.25 — held, and the failure direction (more noise) strengthens it; but the gold bar says the held-out predictions held.

## Attack (four adversarial cases of my own; all ≤ 2 GB)

1. **Independent v2-Kepler validation** (my script, 2M-step RK4 reference, 20 orbits, K = 16/orbit): rel pos/vel err 1.6e-12 at e = 0.05, 3.5e-12 at e = 0.2 — reference-truncation level. The corrected instrument is sound far beyond the toy's e ≈ 4e-7. (e = 0.5/0.7 exceeded my time budget; irrelevant at this e.)
2. **Phase-set adversarial** (24 interleaved phases, kπ/6 + kπ/6+π/12, 300 orbits): τ = 0.17 medA16 = 0.792 (frac>1 = 0.29); τ = 0.25 medA16 = 1.836 but q25 = 0.93, q75 = 7.80, frac>1 = 0.71. At fixed τ = 0.25 the median swings 0.833 (150 orb) → 1.069 (author's 12 phases) → 1.836 (my 24) — horizon- and phase-set-sensitive noise, not a regime boundary. Confirms non-robustness.
3. **μ = 1e-2 on v2** (the first checker's crossing mass; 12 phases, 150 orbits): medA16 = 1.23/22.8/67.3/13.4 at τ = 0.05/0.10/0.17/0.25, frac>1 = 1.00 at 0.10–0.25; err16 converges (2–7e-4) while err1 stays ~2e-2. No τ-crossing at μ = 1e-2 either — uniformly ≫ 1 — so the kill generalizes across mass. But this falsifies the dossier's "the toy never supported a batching-vs-sampling convexity measurement at these cadences, broken or not" as a toy-level statement: it is true only at μ = 1e-3 (where err16 ≈ err1, phase-coherent); at 10× the tide the toy measures convexity cleanly.
4. **Teleport-reach map** (my 10-line script, all published grids): the circular-start e-vector is exactly (0,0) at most τ — `atan2(0,0) = 0`, no rotation. The teleport fires at **τ = 0.25 only** for μ = 1e-3 (the author's row and the checker's φ-shifts), at τ = 0.10/0.17 for μ = 1e-2, and at 0.05/0.25/0.35 for μ = 1e-4.

## What attack 4 corrects (the record, not the kill)

"a deterministic ~π teleport at step 1 in every run" and "Every published number … shares this same rotation" are **false**: at μ = 1e-3 five of six τ values do not rotate at all. The truth is sharper: the teleport lands on exactly the cells that carried the crossing — the author's only A > 1 value (1.68 at τ = 0.25) and the first checker's μ = 1e-2 crossing evidence (1.52, 5.87 at τ = 0.10/0.17). Every published pro-crossing cell is a teleported cell. "Bit-faithful reproduction proved nothing" remains true for a different reason: defects 1 and 3 sit in every cell of every run.

## Novelty

The toy and its A(τ) claim are one day old (`20261008-0338-library-f045`, silver this morning; docs/HISTORY.md has no entry for it — the taste log ends 6 October). No prior run audited this harness. The meta-lesson (shared harness ⇒ agreement is not independence) is registered (AGENTS.md, 5 October) and cited; the increment is real and stronger: the defects are deterministic, so the *checker's own reproduction silently inherited them* — two independent finders, one instrument — plus two cheap pre-flight checks (a ≤ 60 s element-invariance drift control before trusting ω read from a ~1e-7 e-vector; a period-label check against the period formula actually used). r9's own KILL (τ₀ = 0.0036 ≈ 0.17 Hill radii, measured on the engine path, r9-hill rung, B14) is untouched; only the toy's "independent corroboration" dies, and the dossier scopes that correctly.

## Goal fit

Board item 1 (cadence is the lever). Verified: q-cadence sits at `lab/queue.txt` line 31 and no cadence rung exists in `lab/rungs/` — the kill lands before criteria freeze, which under "gates are frozen before runs and never weakened" is the cheap kind of 10×. PRINCIPLES 2 ("'Exact' means deterministic and reproducible" — the row was reproducible and meaningless), 20 ("behaviours over many seeds" — one phase of a broken instrument), 9 (kills the configuration, never the method), 13 (a sign error at ~72% of steps). Adoption cost: zero — deletes a criterion, adds two one-line instrument rules.

## The one experiment that would make it gold

No new physics needed: measure the teleport's reach per (μ, τ) and the μ = 1e-2 convexity (both < 60 s; I have run both), restate the two overgeneralized lines to match the logs, and cite an interleaved-phase confirmation. With the record equal to its log, this is gold — every decisive number already reproduces bit-for-bit.

## What the author missed

- Defect 2's reach was measured at one a and generalized six-fold; the 1-second per-(μ,τ) map both corrects the dossier and sharpens the kill (all pro-crossing cells were teleported).
- "Never supported a convexity measurement … broken or not" is μ = 1e-3-specific; at μ = 1e-2 the corrected toy is a clean convexity instrument (A = 23–67, 12/12 phases) — worth knowing before anyone rebuilds a toy for the cadence question.
- Why the flip rate is ~72% and not 50%: the mirror error biases the corrupted trajectory's own phase distribution — instrument and corruption are entangled; one sentence would prevent a future reader from "correcting" the number.
- `run.log` empty (0 B) again — no execution trail, the identical weakness the first checker flagged.
