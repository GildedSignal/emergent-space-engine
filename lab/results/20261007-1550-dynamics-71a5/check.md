# Check — run 20261007-1550-dynamics-71a5 (checker: independent GLM, fresh session)

Grade: gold

**Abstract (for the integrator).** The claim: the encounters certificate's "valid until a kick"
premise (fixed elements; `crates/encounters` models a static `pom`) has a finite horizon under
the law's own compiled apsidal precession. Everything reproduces bit-for-bit on this host:
equal precession is an exact rigid rotation (both controls, m0 to 6 digits); differential
precession kills the standing "never" certificate at t_tang = travel/Δϖ̇ (exact halving over
3 rates; 7/7 realized sub-ρ encounters after tangency, none before) and decorrelates the
active schedule (waste 9→27 of 27 proposals; first miss at Δϖ̇ = 10⁻³/time). The engine
translation checks out (≈40–400 orbits at p ≈ 50 M; ≈4×10⁸ weak-field). My adversarial cases
(toward-tangency direction, e = 0.7) confirm rather than break it. Adopt at design level in
one step: sections cut in the pair's co-precessing frame; a crate rung follows.

## Reasons

**1. Reproduction (exact).** Ran all three dossier commands in a scratch copy
(`/tmp/chk71a5`; author artifacts untouched).

- `python3 cert2.py` (220 s ≈ stated 3.7 min): regenerated `results2.json` **identical** to
  the author's except the `machine` block (different host: GitHub Actions vs agonbox).
  Controls: 0 misses, 0 waste, m0_true = m0_frozen to 6 digits (G6: 0.000083; G4n: 0.006934).
  A2 ensemble: props 27 at every rate, waste 9 → 21 → 25 → 27 → 27, first miss only at
  Om = 10⁻³ (earliest = 1458.606). dm0/dΔϖ = −0.1087 (G2), −0.0903 (G6). All as claimed.
- `python3 cert.py` (72 s ≈ stated 1 min): stdout identical to `run1.log` (calib, controls,
  A-sweep values, slope 0.4457), and the **disclosed** crash reproduces exactly (TypeError in
  the drift print, line 223).
- `results3` snippet (61 s ≈ stated 50 s): all 12 `first_below` values **bit-identical** to
  the author's fourth column. All 7 realized encounters fall after their analytic tangency
  (delays 3.97–2145.2, matching "by 4–2145"), zero before.

**2. Predictions.** `predictions.md` predates the decisive artifacts (file times:
predictions ≈15:56; cert.py 16:07; run1.log/cert2.py 16:11; results2.json 16:14;
results3.json 16:16). Held: 1 (both controls exact, both sides) and 5 (strong field 40–400
< 10³; weak field 4×10⁸ > 10⁷ — I re-derived the arithmetic: δ = 6π/50 = 0.377 rad/orbit,
horizon = 1.5/(0.377·Δp/p) = 40/400 orbits; 3.6×10⁻⁹ rad/orbit at p = 5.27×10⁸ M). Failed as
written: 3, and the author exercised its pre-registered fallback ("report the measured law
instead") — the corrected t_tang = travel/Δϖ̇ is confirmed by the exact halving plus the
brute-force realization times. 2 unresolvable with this instrument (disclosed); 4 not run
(disclosed). This is the honest pattern the rubric wants, unlike the 1 October red-team that
reported a failure as held.

**3. Adversarial cases (mine).**
- *Direction the author did not run:* precession **toward** the near tangency (Om = +om,
  travel 0.0269 instead of 1.427). 7/12 phases realized sub-ρ encounters, **all after**
  t_tang (80.5 vs 26.9; 464.6 vs 53.85; 224.8 vs 13.46). The "after tangency, none before"
  law survives both directions (now 14/14 realized events).
- *Independent constants:* bisection on the Binet cone gives tangency Δϖ* = 0.726924, near
  travel 0.026924, far travel 1.426924 — the author's 0.7268 / 0.027 / 1.427 confirmed.
- *e = 0.7 (the admitted-untested eccentricity):* kepler and equal-precession controls exact
  (0 misses, m0_true = m0_frozen = 0.004738 — rigid-rotation exactness and the Kepler solver
  both hold at e = 0.7); differential Om = 3×10⁻⁴ produces real missed encounters (first at
  t = 513.8, at d = 0.0019 and 0.0005). The aging mechanism operates there too.

**4. Novelty.** Verified against docs/HISTORY.md, docs/law.md, board.md's taste log and the
crate: `crates/encounters/src/kepler.rs`'s `Body` has no precession rate and `full_section`
cuts sections at a static `bj.pom`, exactly as the dossier states. law.md's encounters
paragraph claims "the pair's timing is an exact integer circle rotation … A kick re-sets only
its body's candidate pairs, with no work per orbit in the steady state." No history entry
couples Δϖ̇ to section aging: r8 v2/v3, q-candidate-degree and taleb-09b5 (6 October) all
judge candidate algorithms on fixed elements; r9's precession finding is about averaged
tidal kicks; H0178/H0203 concern the law's own precession accuracy. Complementary fact this
run implies and the board can use: taleb-09b5's phase-neighbour certificate (co-orbital
formations, equal p ⇒ equal δ) is immune by the rigid-rotation control.

**5. Goal fit.** Board focus "finding encounters without work per orbit or per element
change" and the top scaling risk (candidate work must track real encounters): the horizon
bounds how long a standing certificate stands, i.e. the forced per-pair setup rate the tier
pays with no kicks at all — ≈1/(40–400) per pair per orbit at p ≈ 50 M. This *shows a
premise wrong* (the "valid until a kick" / "no work per orbit" premise fails in the law's
native strong-field regime under the law's own compiled dynamics) and is adoptable within
one step at the design level: parameterize each pair's section by Δϖ tracked exactly from
the tubes' compiled per-cycle advance (integer adds), rebuilding windows only when the
differential rotation exceeds the arc width. Principle 32 ("under the right representation
many symmetries can appear") is exactly the proposed fix; principle 13's error type (13:
"basically we don't want errors that can compound") is respected — the aging error is
bounded per rebuild, but unbounded and silent without one, "exactly the type a certificate
must bound." Cost claim is honest: "no work per orbit" becomes "none in the weak field; O(1)
angle updates in the strong field."

## What the author missed

- The A2 miss evidence is one event (1 miss in 12 phases at the top rate); the
  decorrelation claim rests on the waste metric (27/27), which is solid, but the miss-rate
  quantification at G6 is thin. My e = 0.7 case adds misses at 3×10⁻⁴.
- The parenthetical "6×10⁻⁴ rad/orbit" for the first-miss rate is off ~10× (Om = 10⁻³ per
  time ≈ 6.3×10⁻³ rad per body-0 orbit of 2π). The conclusion (well below the 0.038
  rad/orbit strong-field rate) is unaffected.
- `results2.json`'s B2 rows and `results3.json`'s third column record t_cross = K/om from
  the near-side linearization (0.0269/om), which is the tangency time for the direction
  *not* run (Om = +om); for the run direction (Om = −om) the true value is 1.427/om. The
  dossier's text is corrected, but the stored columns would mislead a reader who trusts
  them, and the reproduce snippet (3 printed fields) does not regenerate `results3.json`
  (4 columns) exactly.
- The certificate's unsafe onset strictly precedes t_tang by the travel needed for the
  cycle-minimum envelope to reach ρ (measured consequence: realization waiting dominates —
  all realized events still land after t_tang in both directions — so the offset, ~1% of
  typical travel, is negligible at the stated orders; worth one sentence in the design).
- Still untested, as disclosed: mutually perturbing pairs (kicks landing mid-drift), the
  resonance shelf (prediction 4), retrograde/inclined pairs, e > 0.7, and the aggregate tier
  cost (derived, not simulated). The natural next rung: implement the co-precessing section
  in `crates/encounters` and judge it against this brute-force truth.
