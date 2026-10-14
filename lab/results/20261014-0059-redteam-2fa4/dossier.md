# Dossier — the seen instruments at speed: exact where flown, Newtonian on the fleet seam

**Run:** 20261014-0059-redteam-2fa4 (lens: premise red-team). **Time:** 60 min.

## Claim

The premise "observables are emergent — −p·u *is* the colour, the aberrated direction
*is* the view" (representation.md §2) is measured for the first time on shipped code
for a **moving observer**: exact to the float floor (≤1.4×10⁻¹⁰ shift, ≤6.4×10⁻¹⁵°
direction) at observer β 0.9–0.99 and emitter β 0.9 in every geometry — and it is
computed **non-relativistically on the one seam where the game's fast content lives**:
every fleet member's seen colour and luminosity omit the member's kinetic γ, wrong by
γ−1 (colour) and γ⁴−1 (luminosity) — 1% at β 0.14, 130%/27× at β 0.9, the contact
law's own tested range — while no rung, gate or example judges any seen value.

## Bottleneck

Not a compute bottleneck: a correctness premise of the design's cost thesis ("views
are derived, never evolved" — principle 3). What it deletes: nothing today; what it
gates: the relativistic-battle view (the dense order's spectacle) and the missing
`Seen`-value criterion in the unfrozen r6. The exact-path result retires the view
page's "moving observers, the seen/Doppler instruments — not measured anywhere" hole.

## Evidence

All numbers regenerate (`regen.sh`, < 1 min; Linux/x86, orders of magnitude only):

- **The exact path is exact.** `crates/universe/examples/seen_oracle.rs` (new, this
  run's patch) builds B15's `stream` scene (bare straight tubes at 1e8 root units,
  gravity 2×10⁻⁸), gathers cold 6 frames × 24 emitters, and judges the shipped
  `Seen.shift`/`Seen.direction` at the engine's own retarded events
  (`observe::state_rate`/`root_state` at the engine's emission tick) against an
  independent SR oracle (my own closed-form crossing solve and boost-matrix Doppler/
  aberration, written from the scene's construction, never from the engine's
  readouts). Max over 7 cases (still observer; 0.9c/0.99c observer × across/toward/
  away/still emitters at 0.9c): **|Δshift| ≤ 1.38×10⁻¹⁰** (0.99c observer, 0.9c
  approaching), **|Δdir| ≤ 6.4×10⁻¹⁵°**, and exactly 0.0 shift for the still observer
  — the two arithmetic paths agree to float noise (`oracle.txt`). Prediction 1 asked
  for 10⁻⁵; the result is 10⁻¹⁰.
- **S1 — the fleet seam (`view.rs:395-399`).** A member's rate is
  `rate0·√(1−2μ/r_doll)`: the member's own kinetic factor never enters (for every
  non-fleet body it does, via `state_rate`'s `√(f − v_r²/f − v_t²)`), so the shipped
  rate = true rate × γ(β_m) and `shift` (÷ rate, view.rs:308) is high by γ:
  **1% colour at β_m 0.14, 5% at 0.31, 40% at 0.70, 130% at 0.90** (the contact law's
  tested range, contact-carry's page), luminosity (×shift⁴, view.rs:319) **−4.0% /
  −22% / −285% / −26.7×**; at the plane's flown battle speed (2⁻¹⁵ c) it is
  4.7×10⁻¹⁰ — invisible today (`seams.txt`, exact arithmetic).
- **S2 — the nested-doll numerator (`observe.rs:272` `vel = vel + v`).** The Doppler
  numerator's root-frame velocity is a Galilean sum up the doll chain while the rate
  denominator composes exactly (`rate /= 1 + v·vb`): at planetary β_p = 10⁻⁴ the
  worst shift error is 1.2×10⁻³ (invisible), but at β_p 0.1 the parallel sum
  **leaves the physical domain** (Galilean β ≥ 1) — the handoff page's "fast
  grandchild" hole, extended from keys/clocks to seen values.
- **S3 — the burning observer (`view.rs:288` `vo = vo + dv`).** The owed burn enters
  the colour numerator Galilean; in the root doll (one level) this is exact, and the
  clock side is safe anyway (`clocks_with` re-derives the rate with dv in the chain).
  Binds only nested-doll + burn, by S2's arithmetic.
- **Consistency note (not a finding):** the engine's cold crossing tick sits up to
  ~1.7×10³ ticks from my analytic root for approaching 0.9c emitters — fully
  explained by my oracle's straight-line worldline neglecting the star's pull
  (~72 units over the flight, ÷ the 0.1/tick arrival rate). The engine's bracket is
  ≤ ~10 ticks wide there (≤ 9×10⁻⁶ relative), inside the view's read quantum.

## Predictions

`predictions.md` was written before the decisive run. All four held: (1) the body
path exact — better than the 10⁻⁵ asked; (2) S1's error is exactly γ(member), 1% at
0.14; (3) no rung/gate/example judges a seen value (r6 cost-only, B7 bodies' rates,
all view examples count readouts); (4) the contact-law domain makes S1 reachable. One
oracle-side bug was found and fixed mid-run (my quadratic's coefficient; disclosed
above in the run history — the first table in the transcript was garbage from it).

## What would make it wrong

The exact-path measurement is scoped to the `stream` scene class: straight tubes,
Schwarzschild 1-mass background, plane-symmetric aberration, one observer. Lensing,
delay and multi-image structure are the view page's standing (gold-attacked) holes
and are not re-measured here. S1's arithmetic could mis-transcribe the shipped line:
it is `view.rs:397` verbatim; if a future build adds the member's kinetic factor the
threshold table collapses to zero.

## Cost of adopting, and fit with PRINCIPLES

The fix is one factor: `rate *= √(1 − |v_member|²)` (one multiply) at `view.rs:397` —
or route members through `state_rate` like every body. The gate: one `Seen`-value
criterion in the unfrozen r6 (a fast-fleet scene, |shift − SR| < 10⁻³, the Newtonian
rate as the negative control). Fits: "behaviours matter, not continuum fidelity" (2)
— the error is a wrong behaviour class (a Newtonian readout in a relativistic law),
not size; "the player is the only wildcard" (5) — what the player *sees* is the
product; violates "compute only surprises" (3) in no way — the fix is free.

## The lens

The premise red-team overweighted the exact path (hours on formula verification that
ended at the float floor) before finding the seam in the fleet branch — the code
paths a player never flies today. The blind-spot warning applies to my own ranking:
S1 is dormant at today's flown speeds; its gold case is a future relativistic battle.
What this lens may have missed: the crossing's own quantization at extreme closing
speeds (β→1 brackets widen as 1/(1−β)) — sub-resolution here, but the same 1/(1−β)
amplification that made my Δte diagnostic jump 10×.

## Grade (author's self-assessment)

Silver: real, reproduced, one named experiment from gold — the r6 `Seen`-value
criterion plus the one-line fix, on a fast-fleet scene the engine can already build
(`scenes::battle` with `speed_div` small). The exact-path measurement alone is a
survivor report, worth one line on the view page.
