Grade: gold

**Abstract.** The rebind half of gravity-is-news gains the first error model: every source
rebind leaves each consumer a permanent scar |ΔE| ≈ 0.7·(β_c²/2)·|δv| (exponent 1.963,
reproduced bit-identically; my extensions: k = 0.72 at β_c = 0.5/0.6, bounded accumulation
under kick sequences, zero scar from a zero-δv re-key). The thrust half is the wrong law as
specified: a (pos, vel) free-fall tube lags a burning source by the cadence-invariant ½aT²,
the consumer absorbs β²/2 of the burn's Δv (2.2×10⁻² at β_c = 0.3, 200× B12), and no gate,
rung or oracle can see either. Acceleration-carrying versions collapse the lag to machine
zero (3×10⁻¹⁸, my check): adoption is one payload vector plus the freeze-ready `r-news`
criterion. Page corrected in place (two overstatements).

## Reproduction

`bash regen.sh`: exit 0, 0.7 s, and `run2.txt` (decisive) vs `regen-run.txt` is **bit-identical**
(diff empty). All dossier headline numbers regenerate from `scar.json`: exponent 1.963,
k̄ 0.702, twin_max 0.0, burn lags 0.0001/0.0002–0.0003/0.0022–0.0023 vs pred ½aT², dE 2.187×10⁻²
(β 0.3, cad 8), dt-conv 0.000. patch.diff is empty (the probe is self-contained); the tree is
clean at the recorded base 941f6941.

## Predictions

`predictions.md` predates run1/run2 (mtimes 15 m vs 9/7 m; author's stamps 02:49 vs 02:58).
P1 exponent 1.963 ∈ 2.0 ± 0.1 ✓; P2 k̄ = 0.70, invisible at moon β, percent at 0.3 ✓; P3 ret ≥
10× news at every geometry (min ratio ≈ 13×) ✓; P4 plateau cadence-invariant (0.0022 vs 0.0023),
damage 0.022 vs 0.028 predicted ✓; P5 0.000 rel ✓; P6 scoping honest ✓. The retraction of
"one-signed across seeds" is correctly reported as a refinement (the sign varies with geometry;
the time structure — all damage inside the window — is what holds, and it does: final ≤
at-switch everywhere).

## Attacks (mine)

1. **Outside the tested range (β_c = 0.5, 0.6):** mean k = 0.72 at both — the β²/2 law holds a
   decade past the author's sweep. Held.
2. **Eccentric consumer (e = 0.3, kick at pericentre; the author's named untested case):** k =
   0.60 at β_p = 0.1, **k = 1.83** at β_p = 0.3 — wider than the circular spread (scar.json full
   sweep: 0.019–1.175), still inside the proposed criterion's 2·β² margin. The domain note
   stands; the law survives with local β.
3. **Kick sequences (multi-kick extension, validated against the author's own numbers at all
   four geometries, ratio 1.000):** a zero-δv re-key adds nothing (ratio 1.001); a canceling
   pulse (+DV then stop) accumulates boundedly (2.4× the single scar, signs geometry-set);
   alternating kicks 2.08×. No compounding amplification — criterion (b)'s "bounded random-walk"
   is supported. (Two earlier drafts of my own multi-kick harness were wrong — a negative
   time segment and an emission-position error — each caught by validating against the author's
   logged rows before trusting anything. The author's controls caught their two broken builds
   the same way.)
4. **The fix:** with acceleration-carrying versions (the dossier's proposed payload), the readout
   lag collapses from 0.0022/0.0023 to 3×10⁻¹⁸/0.0 (criterion (c) "must pass" passes by ~15
   orders), and consumer damage drops 2.187×10⁻² → 1.34×10⁻³ (cad 8) and 1.61×10⁻² → 5.1×10⁻³
   (cad 32). The fix is real, not just argued. Note: the residual is cadence-dependent and
   nonzero at β = 0.3 — the dossier does not claim otherwise.
5. **Fit robustness:** LSQ over all six means gives 1.968 vs the author's endpoint pair 1.963.

## Novelty

a237 measured free-fall sources (binaries, flybys, the switch onset; 10⁻⁷-class agreement) —
never what a rebind or burn *leaves*. e300 wired the cursor and printed byte-identical gates,
explicitly because no gate scene rebinds inside a light window; 05b0 is the cursor's exactness.
lab/rungs contains no r5, r6 or news rung; the gravity-news page was an empty integrator seed
(the 12 October compile run 9bbc graded missing). The doc-drift attacks verify: representation.md:32
still calls Minsky's map "the primary in-cell solution" after law.md:20 replaced it; :67 still
describes the multiply-add kick after law.md:36 retired it. Nothing in HISTORY or the wiki
measures the consumer-side scar or the ½aT² lag. New.

## The page

Faithful on every number I could trace to scar.json/run2.txt. Corrected in place, two
overstatements: (i) "one-sided orbital scar" → permanent, accrued inside the light window, sign
set by kick geometry (the dossier's own P1 retraction; "one-sided" survives only for correlated
kicks); (ii) deleted the claim that the news-lag channel *exceeds* the consumer's direct tidal
signal at 20M in a 100M binary — unmeasured, and the parenthetical "r_c/d ≪ β²/2" is backwards
at the quoted numbers (0.2 vs 0.0125; the tide (r_c/d)³ ≈ 8×10⁻³ also sits above my lag-channel
estimate ≈ 1.2×10⁻³ in magnitude — the one-way-vs-bounded argument is the defensible form).

## Goal fit

Board item 0 / law.md:33, the causality primitive. Shows a premise (the thrust half of "gravity
is news" as specified: free-fall (pos, vel) tubes) is wrong, with the measured law (½aT²,
cadence-invariant), the consumer-damage law (β²/2 of burn Δv), the validated one-step fix, and
the first instrument that can fail it (r-news, freeze-ready, controls on both sides). PRINCIPLES
#13 "we don't want errors that can compound" — the scar is permanent and one-signed under
correlated kicks, now with a bound; #19 — rekeying 4× faster bought 0.0022 → 0.0023; the fix is
the payload. Adoptable within one step; a237's own probe already recorded (t, x, v, a).

## What the author missed

- Side numbers in the dossier that scar.json cannot regenerate: the E1 at-switch column matches
  no single statistic (mean is 7.44×10⁻⁶ at β = 0.003, dossier says 6.5; "~1.5×" is ~2× on
  means, 10–40× in the safe direction for geometry 4); the β = 0.003 ret range drops geometry 2's
  3.9×10⁻³ (true min); "3–4 orders everywhere" is 1.5–4.2 orders (P3's ≥ 10× still holds); "fitted
  exponent" is the two endpoints (LSQ 1.968 — survives); "spread 0.086–1.2" vs the sweep's
  0.019–1.175. None touch a load-bearing result, but a future reader cannot check them.
- The strong-field-binary dominance claim (E3's tail) — see the page correction.
- The integer law and the plane's actual wiring are untouched (probe is standalone float; the
  dossier says so), and the ½aT² verdict rests on the instantaneous-gauge oracle family — a
  retarded 2PN oracle could move the required payload to jerk (the dossier names this; my A4
  confirms acceleration suffices for *constant* burns only).
- My A2 eccentric result (k = 1.83) widens the k spread the criterion must absorb; worth a line
  in r-news when frozen.
