Grade: gold

**Abstract.** Claim: Levi-Civita (`z=u²`, `dt=|u|²dτ`, `u''=(E/2)u`) serves the conic representation's singular set (radial L=0, plunge, near-radial — where the engine refuses `NoBoundOrbit` and Julien's ship froze) exactly, at K events independent of depth. Reproduced bit-identically (181 floats, 9 s). No-tide error 3.5e-16…7.4e-12 at every depth; stepping fallback pays 18–93× at matched error, >62,500× or non-termination on the singular set; DOP853 itself cannot pass r=0. Gain ≥ 10× on a live open item (HANDOFF: "plunge and radial orbits have no tube"); deletes the stepping fallback there; corrects opus-math:291's blanket rejection of LC-as-drift. Cost: one unbound/radial drift branch in the doll, reusing v2 kicks and R1's integer phase; integer form still to be measured.

## Reproduction

`python3 falsifier.py` in a clean copy: results.json byte-identical on all 181 floats (worst relative difference 0.0), 9 s, < 50 MB. The dossier's table and the "cost at matched error" column derive exactly from results.json (coarsest measured α with err ≤ C_K8's, evals ÷ 8: 18.4/26.4/28.5/29.1/93.1).

## Predictions

predictions.md mtime precedes the final falsifier.py and results.json by ~15 min; run.log is empty, so pre-registration rests on mtime plus content — acceptable internal evidence, since the addendum amends predictions 5 and 6 *against* the author's favour before the grid. Held: (1) no-tide ≤ 1e-12 everywhere ✓ (3.5e-16…7.4e-12); (3) A-rt error grows 70× ✓; (4) cost-to-match ≥ 10× ✓ (18–93×); (5) C passes r=0 at 1.2e-15, A-rt err ~190 ✓, refusals verified in code ✓. Boundary, honestly reported: (2) K8 grew 3.04× vs "~3×" (K16 flat); (6) exponent −0.36 vs amended [−1, −0.4].

## Attacks (mine)

1. **Fairer stepping rule** — the strongest strawman risk. I gave A dt = min(cap, β√(r³/μ)) (depth-aware Kepler rule), β calibrated on the same single case. Result: A still needs 18× (q0.3), 52× (q0.003), **211× (q=10⁻³ r_H), 268× (q=10⁻⁴ r_H)** more events at matched error. The claim survives and strengthens at depth; the 93× headline understates the deep end.
2. **Deeper grid** (q = 10⁻³, 10⁻⁴ r_H): C's K8 error flat at 2.0e-3, no-tide ≤ 6.6e-10 — depth-independence extrapolates an order below the author's grid.
3. **DOP853 through r=0** (no tide): status −1, step underflow at r = 8.3e-12 after 5,498 evals — the literal regularization claim verified; LC passes at 1.2e-15 with zero force evals.
4. **Exit-point error cancellation**: C no-tide q0.003 at exit 0.5/1.0/1.5·r_in: 4.0e-12/7.4e-12/1.1e-11 — no artifact.
5. **Citations**: certified_bank.rs:26–29, binding.rs:196–248, kicks.rs:157–176, orbit.rs:59–60, lib.rs:188+, HANDOFF ("no tube", ship freezes on near-radial fall), opus-math:63 (oscillator angle) and :291 (LC rejection, verbatim) — all verified. (The dossier cites the quotes to "the opus-math memo" correctly; line 63 is opus-math, not opus-motion — both files exist, no fabrication.)

## Novelty

LC is 1911 and present in repo context (original-conversation.md:8129–8145; opus-math:63 uses this oscillator as the bound clock). What is new: the measured demonstration that opus-math:291's rejection of LC-as-drift ("Kepler's equation anyway… the doll is already the regularized frame") covers only the bound branch — the doll regularizes the origin, not the conic's discriminant — and that the certified bank's unsupplied list is exactly that residue. HISTORY has no prior run on it (r1 was Binet, different). The author states this scoping honestly.

## Goal fit

A live board item: HANDOFF names "plunge and radial orbits have no tube (`NoBoundOrbit`)" as Astra's open item, and the flight merge recorded the player-visible freeze. PRINCIPLES: #19 ("if you find yourself fixing things… wrong representation" — the refusals are the signal), #3 (zero force evals between tide kicks), #13 (drift exact at any depth; error confined to second-order kicks), #7 (geodesics as trivial as straight lines, made literal at r=0). ≥ 10× on cost, deletes the stepping fallback on that set, and corrects a standing premise: gold bar met on all three alternative counts.

## What the author missed

- The integer/Q48 form (kick linearity in u′, exact phase accumulator, table cos/sin) is designed, not measured; "adoptable within one step" holds for the float replica, not yet the exact law — the one experiment that matters next.
- The "18–93×" column uses measured grid points, not interpolation: interpolated cost-to-match at q0.003 is ~51×; the discrete choice overstates by ~1.8×. Direction favors the claim; conclusion unaffected (and my fairer-rule test shows the true deep-end gap is 211–268×).
- "hit" at α smaller than the locked 0.2 does terminate (err 0.029 at α=0.05): the dossier's "(A never terminates)" is true only at the locked rule; results.json discloses it.
- Label nit: "q ≈ 3e-6 = 0.1 r_surf" — 3e-6 is 1.0 r_surf (R_SURF = 3e-6).
- Long resonant captures (B13's deep regime) with tides non-smooth in τ remain untested; the th_win = 24π pre-pass window and 6K+16 iteration cap would refuse there (disclosed, but it is the next failure surface).
