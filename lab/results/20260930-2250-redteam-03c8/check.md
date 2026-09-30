Grade: silver

**Abstract.** Claim: r1's frozen Binet-band law breaks its own 1% gate where the rung's sampler cannot look (near-circular ISCO skimmers up to 6.7%, photon-ring sliver), and r5/r6 gates named in representation.md §7 do not exist. Reproduced bit-for-bit (`falsifier`, `isco-scan`); the banded model matches r1's frozen spec literally; an independent elliptic-quadrature oracle confirms the run's exact values (light ≤2.6e−5, timelike ≤1.2e−7 rel); the 6.7% error is invariant from h=2e−4 to 2.5e−5 (model error, not solver). Gain: no 10×; it exposes a certificate-coverage crack and kills "plain fixed bands suffice". Cost: r1 v2 sampler extension plus graded band width. Not gold: H0207 already recorded near-circular precession 1–7% off the same day, uncited; and the proposed fix was asserted, not measured.

## Reproduction

- Clean tree, `patch.diff` empty (no repo edits — consistent with lab rules). Compiled and ran both programs in a scratch dir: `run-out-v3.txt` and `isco-out.txt` reproduce **bit-for-bit** (only wall-time line differs). Dossier commands ≤ 60 s each: confirmed (20 s / 18 s / this checker's runs).
- `predictions.md` (22:55:41) precedes every output file (first 22:56:18); the decisive `run-out-v3.txt` (22:59:47) follows the last `falsifier.c` edit (22:59:26). Scorecard in the dossier matches the outputs honestly (P-B failed in direction, disclosed).
- Model faithfulness: `falsifier.c` implements r1's configuration exactly as frozen in `lab/rungs/r1-rings.md` (bands r_k = 2^(k/m), u_k geometric centre, u″+(1−6u_k)u = 1/L²−3u_k², u/u′ continuous, light variant, sampler box p∈[10,1000] log, e∈[0,0.7], p≥6.5+2e, b∈[10,1000], 1% gates). No strawman.

## Independent checks (adversarial)

1. **Independent oracle** (elliptic quadrature, no ODE integration): timelike advances match to ≤1.2e−7 (e=0.02/r_p=5.96: 58.128079 vs 58.128086; e=0.95/r_p=4.5: 12.535318 exact match); light deflections to ≤2.6e−5 (b=5.205: 5.980359 vs 5.98041). The run's numbers are oracle-sound.
2. **Step-halving at the failing point** (the author only halved elsewhere): e=0.02, r_p=5.96, m16 gives err = 6.662e−02 identically at h = 2e−4, 1e−4, 5e−5, 2.5e−5. The headline 6.7% is model error. Confirmed.
3. **m-scan beyond 32**: non-monotonicity confirmed and extends (r_p=6.02: 1.22e−2 → 2.96e−2 → 5.25e−3 → 6.3e−4 for m=16/32/64/128; r_p=5.96: 6.66e−2 → 1.23e−2 → 1.62e−2 → 2.24e−3). Quantization noise, yes — but m=128 does get <1% at all probed points, so "raise m is not the fix" holds only as "not a monotone or cheap fix" (crossings double per doubling), not "cannot fix".
4. **Fine light scan** (b = 5.200…5.300, step 0.002): the m16 >1% sliver is b ∈ (5.195, **5.209**], not (5.196, 5.22] (at b=5.22 the measured error is 0.69% < 1%). m32 stays <1% throughout. Substance unchanged; upper edge overstated.
5. **The proposed fix, measured** (the author asserted it): gradient-linked band width (halve bands while log-width > 0.25·|1−6u_k|, ≤6 levels, m16 base) drops the whole plateau to ≤0.67% (most ≤0.2%), fixes e=0.05/r_p=5.90 (4.96e−2 → 3.6e−4) and cures the separatrix sticking (both capture), at 12–234 crossings/cycle — inside r1's ≤512 budget. The design consequence is real.
6. **Separatrix knife-edge**: a 1-ulp change in band centres (sqrt(lo·hi) vs pow(2,−(k+0.5)/m)) flips (e=0.02, r_p=5.90, m16) from "stuck, no cycle" to a bound 64.8-rad rosette, while exact GR captures robustly at every step size. A behaviour-type error either way; r1 v2 needs a negative control here.

## Novelty

- **H0207 (30 September, earlier)**: "The viewer found near-circular precession 1–7% off." The phenomenon was already recorded, in HISTORY, the same day; the dossier does not cite it. What is genuinely new here: attribution to r1's frozen banded configuration (not the es-space-v2 law — H0208's Darwin-phase compiler passes G1–G6 at 1e−6), the region map, the non-monotone-in-m structure, the photon-ring sliver quantification, and the r5/r6 gap. Confirmatory at phenomenon level; new at configuration and gate level.
- **"r1 PASS (H0204)"** is miscited: H0204 is r2's KILL; the binet pass numbers are in H0205, where r1 is DISPUTED pending a clean re-run. No H entry records a final r1 PASS. The premise ("the gate passes and cannot see this region") is verified directly against the rung file, so the claim survives the miscite.
- r1 does contain ISCO *behaviour* cases (r=7 stay-bound, r=5.5 plunge) — what is unsampled is the precession gate near the ISCO. "r1 cannot sample this region" overstates slightly.

## Goal fit

B0 and the falsifier ladder. It respects "Gates are frozen before the first run and never weakened after" (the finding is that two named gates were never frozen at all — verified: `lab/rungs/` holds r1–r4, r7–r9, no r5/r6) and "error type over error size" (loop count 8.6 vs 9.3, separatrix lifetime). The ISCO skimmer is player-facing ("navigation, knowledge and dynamics those need to be perfect"). No 10× bottleneck move, no deleted component.

## Number slips (none load-bearing)

- "13/26 grid points > 1%": actual 9/26 for m16, 10/26 for m16∪m32; 13 counts failing *rows* over 26 points.
- "p ≥ 10 with e ≤ 0.05 puts r_p ≳ 9.7": it is ≥ 10/1.05 = 9.52. Direction unchanged.
- "In-box ≤ 1.7×10⁻³": actual m16 in-box max on the grid is 2.3e−4 (1.7e−3 is an out-of-box value) — conservative direction.
- The v3 "hover probe (exact 68.9)" line is a stale v1 hardcode (true exact ≈ 21); unused by the dossier. The separatrix scan's printed "plunge boundary (10.00, 9.95)" lines are a recording artifact; only the 0/483 count is meaningful, and the dossier uses only that.
- Finding 7 (carries vs contacts, the 3-body bit sequences) has **no script and no command** — unreproducible from the dossier. The additive-kick half is trivially exact; the same-cell contacts half is plausible but unmeasured here.

## The one experiment that would make it gold

Freeze r1 v2: seed grid extended to e ∈ {0, 0.02, 0.05} × r_p ∈ [5.9, 7.6] and light b ∈ [5.19, 6]; a graded-band candidate (width linked to |1−6u_k|); a simultaneous-triple separatrix negative control. Run it. My probe already supplies the expected numbers (plateau ≤0.67%, ≤234 crossings/cycle, m16 fixed-band candidate killed). Separately, separate this crack from H0207's viewer error by showing the production Darwin-compiler law is immune (H0208 suggests it is).

## What the author missed

1. H0207's same-day "near-circular precession 1–7% off" — the novelty citation that was owed.
2. The fix they proposed was one 30-line probe away from being measured (it works); gold was closer than they thought.
3. No step-halving at the actual failure point.
4. The light misclassification window: banded b_crit = 5.19535 < exact 5.19615, so photons with b in (5.19535, 5.19615) scatter in the model and capture in GR — thin, but it is a classification error, and the 1.5e−4 b_crit number they cite is itself its evidence.
5. The ulp-sensitivity of the separatrix outcome (probe 6) — the strongest argument that the separatrix needs its own negative control, stronger than the single sticking case they report.
6. m=128 eventually passing (raise-m is expensive and non-monotone, not impossible).
