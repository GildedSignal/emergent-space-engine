# Check — 20261008-1757-system-72ef

Grade: silver

**Abstract.** Author claims a perturbed belt's stored scar information saturates at ~64 bits/body (q=1e-6), killing the H_live rate premise, with 10⁹ bodies needing 7.2–8.2 GB. Reproduced: control exact-zero, main content-identical (31.7 s), resonance and q-series match. But the "level" is the plug-in entropy's sample-size wall (5·log₂N = 66.4 at N=10⁴): dlambda reads 13.278 against a 13.288 per-channel maximum. My adversarial runs: N=10⁵ with identical physics reads 73.85 bits (+10.2); μ×10 reads 66.38 at q=1e-7 — the wall again. The true level is ≈91 bits (distribution estimate) → 11.4 GB at 10⁹: overflows, not brushes. The rate-form kill stands; the level, its quantum-independence claim, and the 8 GB pricing do not.

## Reproduction

- `patch.diff` is empty — no tree edits outside the run folder.
- Control (`N=2000`, μ=0): re-run bit-identical to the stored JSON; every channel p99 ≤ 6×10⁻¹³, entropy exactly 0. The pre-registered instrument kill criteria were checked and pass.
- Main: 31.7 s (dossier: 31 s). Fresh JSON matches every stored headline number to the digit (H_total series 39.563→63.611, q_sensitivity 57.22/63.61/65.95, resonance 0.047 / 2.38e-2 vs 5.64e-3 / 0.191 vs 0.045). Deterministic, seed 20261008.
- Long (310 s): not re-run (CPU shared with my own adversarial runs); its stored arrays are internally consistent with the main run and with my ceiling analysis below.
- Disclosure: my `main` reproduction ran with cwd inside the run folder, so `scars-main.json` and `scars-main-final.npz` were rewritten by the fresh run. I verified content identity against the values extracted from the stored file *before* running (all match to the digit; the run is seeded and deterministic). No other file in the folder was touched.
- Prediction timing: `predictions.md` (18:06) precedes `scars-main.json` (18:11) and the long run (18:18). One flag: `scars.py` mtime (18:13) postdates the main JSON; since the shipped script regenerates the stored main JSON exactly, the artifact is regenerable — the taste-log failure mode ("numbers the shipped code cannot regenerate") does not arise.

## Predictions audit

- #1 called "near-miss" is in fact a double numeric miss (63.6 > 60 bits; 1.75 > 1 bit/octave average); only the shape (no linear channel) held. Disclosed, but softly labelled.
- #2 held on the measured numbers (early ≈0.7–1.3 bits/kick depending on the epoch interval; 1.5×10⁻⁴ over the main run's last octave; ratio ≈5000×) — but see the instrument problem: by the last octave 4 of 5 channels are estimator-pinned, so the measured decay overstates the true decay.
- #3 held: resonance numbers reproduced exactly.
- #4 failed and is honestly reported as failed, with direct inspection (Δϖ non-monotonic). Note the 63.2-vs-63.6 comparison itself is wall-pinned: at N=10⁴ a real few-bits-per-channel compression is unmeasurable; only residual collapse could have shown.
- #5 held directionally (11 200× against a naive per-kick store).

## Attack: the level is the estimator's sample-size wall, not the physics

`entropy_bits` is plug-in entropy over N bodies, so each channel is capped at log₂N = 13.288 bits (5 channels → 66.44). Three independent falsifiers:

1. **Wall proximity (stored data).** At the main run's final epoch: dlambda 13.278, dvarpi 13.250 vs the 13.288 cap; 9 996 and 9 982 of 10 000 quantized codes distinct. dvarpi is pinned by kick ~116, dlambda by ~10³ — their entire late-time "rate decay" is the wall. The dossier's resonance claim ("angle scars saturate below the 22.6-bit mod-2π bound") is vacuous on this instrument: no channel can read above 13.29.
2. **N×10, same physics** (`run(N=100000)`, same seed, μ, kicks; 292 s, < 400 MB): H_total@4500 = **73.85** vs 63.61 — every channel now above the old cap (dh 14.60, dvarpi 16.31, dlambda 16.53), climbing toward the new 16.61/channel wall; q=1e-7 reads 80.2 vs 83.05. A width-set level would not move with N.
3. **μ×10, same N** (`run(muJ=9.5459e-3)`): H_total = 65.96, and 66.38 at q=1e-7 — 0.06 bits under the wall. Ten times stronger dynamics moves the "level" by 2.3 bits; the instrument reads N. (Side finding: at μ×10 bodies scatter unbound — element channels go NaN — so the sums-store domain itself breaks under strong perturbation.)

**True level.** Distribution-level estimate from the stored long-run arrays (256-bin histograms, bin-width corrected; joint (dh,dk) as one 2D channel): da 12.0 + (h,k) 35.1 + dvarpi 21.7 + dlambda 22.5 ≈ **91 bits/body at q=1e-6** (dlambda's estimate 22.5 cross-checks against the uniform-2π bound 22.58). Cross-check: bigN reads 73.85 with an 83.05 wall, consistent with a true value in the high 80s–low 90s. Consequences:

- At 10⁹ bodies the scar layer alone is ≈11.4 GB (q=1e-6), ≈9.4 GB (q=1e-5) — **the 8 GB verdict flips from "brushes" to "overflows"**. Fitting 8 GB needs a scar quantum near 2×10⁻⁴ relative (or joint entropy coding): the quantum, not a time-invariant level, is the budget-derived lever — the exact inverse of the dossier's "the level is set by the scar distribution's width, not by … the quantum".
- The measured q-series (57.2 → 63.6 → 66.0, decelerating) is a wall-flattened curve, not width-boundedness; a width-limited continuous distribution rises 3.32 bits/decade per dimension (~16.6/decade here) and their own series was still rising when it hit the wall.
- The "saturation by 4 500 kicks" tail claim is also wall-contaminated: dh/dk p99–p1 spans grow ×2.19 and ×2.08 from 4 500→45 000 kicks (true entropy ≈ +1 bit/channel/decade, still climbing at 1 500 belt orbits); only da_rel is genuinely flat on this horizon (×1.04).

**What survives my attacks:** the structural kill of the rate-form premise. Angles are wrapped mod 2π by construction (hard per-channel bound log₂(2π/q)); da_rel is flat; dh/dk grow only logarithmically. No channel is linear in kicks, so "distinctions created per game-second decide whether 10⁹ fit" is indeed the wrong quantity — the reframing "measure a level" survives. What does not survive is every number attached to it: the level, its quantum-independence, the tail slope, and the 8 GB pricing. This is PRINCIPLES #10 in the checker's face: "a test that cannot fail is a control" — near the wall, no physics can move the number, and most of this run's decisive epochs were spent there.

## Novelty

First measurement of the H_live question (HANDOFF, risks to attack first: "not measured yet"). components-98bc (gold, 6 Oct) measured the *static* genesis program (0.126 bits/body); H0202's shipmem design priced convoys, not a belt's time-evolving scars; no HISTORY entry measures scar-entropy growth. Novel and on a named board risk.

## Goal fit

Moves a named risk and deletes a framing (the rate monitor) — but the replacement it hands the integrator (a ~64-bit level pricing 8 GB) would mis-price the memory budget in the *optimistic* direction, which is the dangerous direction for a ceiling. Not adoptable as stated; adoptable after re-measurement.

## The one experiment that would make it gold

Re-measure the level with the ceiling removed — entropy-code the saved raw arrays against a fitted population model (or sweep N ≥ 3×10⁵ until the reading stops moving), sweep q, and re-price the 8 GB budget per workload class; report the quantum that fits. I ran the cheap version during this check (N-sweep + histogram estimate): level ≈ 91 bits at q=1e-6, 11.4 GB at 10⁹, quantum ≈ 2×10⁻⁴ to fit 8 GB.

## What the author missed

1. The plug-in entropy cap log₂(N) per channel — the central instrument flaw; all headline levels, the q-scaling claim, the tail slope, and prediction #4's comparison are wall readings. The instrument's own kill criteria (control nonzero, entropy incomputable, runtime) could not catch it.
2. The 10⁹-body pricing extrapolated an N-capped measurement; the honest estimate flips the verdict from "brushes" to "overflows", inverting the paper's design conclusion (quantum becomes the lever).
3. Prediction #1 labelled "near-miss" although both numeric sub-criteria failed.
4. "Saturation is real" asserted from a regime where 4/5 channels cannot move; dh/dk are still spreading at the 45 000-kick horizon.
5. μ-stress breaks the store's domain (unbound bodies → NaN elements) — a guard the instrument lacks, adjacent to the conceded encounter channel.
