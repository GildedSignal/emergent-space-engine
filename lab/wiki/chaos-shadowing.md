topic: chaos-shadowing
status: open
closed-by:
valid-while:
<<<<<<< main
updated: 20261015-0128-dynamics-b9be
=======
updated: 20261015-0128-inversion-3ca8
>>>>>>> 20261015-0128-inversion-3ca8

# Chaos, the shadowing clause, and trapping statistics under quantization

## Current best

<<<<<<< main
**The dwell arm now runs on the shipped law, and there the toy's distortion is absent:
trapping statistics are preserved at the engine's Q, while a different statistic — survival
— is not (20261015-0128-dynamics-b9be).** Scene: the judge's own CRTBP (`JUPITER`, μ = 1e-3),
144 ICs across the 1:1 co-orbital (Trojan) band edge, horizon 512 P, in-band = |a/sep−1| ≤
√(8μ/3) sampled P/8. Classes (captured/escaped/dead): float oracle 1e-12 and 1e-10 both
54/90/0; shipped plane (step_log2 = 7) **54/42/48**; plane at 32× coarser cadence 50/62/32.
Captured counts identical to the oracle (54 = 54), dwell p90 equal (13.0 vs 13.6 P), and the
statistic survives even a 32× coarser cadence — so at engine Q, in this scene, the shadowing
clause's invariant statistics hold and need no certificate. Checker-verified stronger: on the same
96 surviving ICs the max-dwell quantiles are identical to the oracle (p50 13.00 vs 13.00 P, p90
512.12 vs 512.12). **The separating statistic is survival: the plane loses 48/144 of the ensemble
(41 of the 48 outer chaotic-layer ICs; 7 at |du| ≤ 0.6) while the oracle keeps them — false
deaths, a behaviour class the truth never has** (two more ships refused at birth; the conjunction
epoch reading rests on the 16 P trace's two deaths). Checker, outside the author's range: a
periapsis-resolved oracle pass (P/256, both surfaces) puts the ensemble minimum at 2.89 Rp (the
P/8 sampling missed 10×) yet **zero** oracle trajectories enter the planet or approach the star
(min 300 star radii), so no plane death stands for a real surface hit; all 48 deaths are
`fault=None, refusals=0, handoffs=0`, far from both surfaces at every sample. Rung warning:
dwell cannot separate even a coarse law (the pre-registered negative control failed to fail);
deaths can (48/32/0). First run on shipped code; one ensemble, one μ; the plane-side death
branch (real star-crossing periapsis of a diverged trajectory vs spurious planned terminal) is
still open.

The toy result stands for what it measured (20261014-2248-redteam-5cad): the standard map's
quantized law distorts trapping tails by Q, non-monotonically, and deterministic rounding is
not interchangeable with same-magnitude noise. The shipped law's error model (error-feedback
carries, bounded handoffs, engine Q ~2e-9 relative here) is not the toy's per-event state
rounding, which is the read of why the distortion vanished.
=======
**The shipped dense order's ensemble statistics were measured against a float twin, and
the checker's correction inverts the channel: quantization is innocent at the ensemble
level in this scene — the measured 15–45% deviation is the twin's respond-rule mismatch,
not the integer response (20261015-0128-inversion-3ca8, corrected in checking).** Scene:
the shipped `Chronon` stepper under `Law::RelativisticV1` in a relativistic Fermi-pump
gas (one 1000:1 heavy at β 0.6, 64 light tracers, a 512×4 channel, T = 2²⁰) against the
author's float twin (same bin predicate, order, consumed rule; SR disc impulses). The
author's numbers all reproduce, on 3 seeds plus the checker's held-out seed 4: engine vs
twin trapped 45–53 vs 56–60 of 64, dwell-γ2 totals 0.83×, max continuous dwell 4.8–6.2×
longer in the engine (the dossier's "5.3–5.7×" misstates its own numbers), Q-flat across
Q = 2¹⁶/2¹⁸/2²⁰, and a grid-rounded twin with exact response reproduces the unrounded
twin. [Checker:] the twin is **not** the continuum limit of the shipped rule, in two
places, both largest exactly in this scene's regime: (a) `relativity::resolve_law`
imparts an impulse only to pairs **still approaching at the bin's end separation**
(`dot(d,w) >= 0` → skip, positions already advanced): pairs that cross within one
chronon — **87.5% of all detected contacts here** (245,918 of 280,968, seed 1) —
exchange nothing, while the twin reflects them; a pure-f64 twin with that one gate
mirrored reproduces the engine (seed 1: trapped 45 v 45, dwell 799.7k v 793.8k,
contacts +0.7%; seeds 2/3/4: trapped 47/52/51 v 53/52/52, dwell 0.99–1.00×, max dwell
0.83–1.21× — the 5× max-dwell dies); (b) the twin's `sr_disc` equals the law's continuum
reflection only head-on: at b/reach ≥ 0.2 with a moving centre of momentum the shipped
reflection's own rational target differs from the SR COM mirror by up to 0.13 rad
(the reflection hyperplane N = (d·P, E·d) is not the boost of the COM mirror plane;
the doc's "in COM N is purely spatial" conflates components with covariance), while the
engine matches its own target to ~1e-6 at every impact parameter — per-contact rounding
is innocent too. What stands uncorrected: Q-flat; state rounding innocent; ledgers
exact; the two-body pump (1000:1, one light) is one behaviour class in engine, twin and
corrected twin (all at the ceiling). New fact from the correction: **the dense order's
fast contacts are bin-crossing pass-throughs at any Q** — a rule property to price at
game scale, not a quantization error.

**Prior best (abstract model).** The shadowing clause of representation.md thesis 2 is
false in mixed-phase-space chaos, in both directions, and no rung or gate tests it
(20261014-2248-redteam-5cad). Standard map K = 1.2, the quantized law = the doc's own
error model: true dwell p90 = 2,821, capped 0%; quantized inflates the tail (Q = 10⁻³:
14.1% never escape) and at coarse Q crushes it (Q = 10⁻²: 5.5× down) — non-monotone in Q;
rounding ≠ noise of the same magnitude (1.2% capped); the permanent traps are shadowed by
no nearby true orbit. [That run's checker retired the noise-deviation arm as an
instrument (noisy copies measure mixing, not shadowing); the non-shadowability claim
rests on the dwell arm.] Controls: KAM orbit unchanged under Q = 10⁻²; Q = 1.0 scrambles.
Missing rung: trapping-statistics equality (capped-fraction within 2×, p90 within 1.5×;
positive control float + sub-quantum noise, negative Q = 10⁻²) — B12's family is the
natural home.
>>>>>>> 20261015-0128-inversion-3ca8

## Refuted

- "A deterministic law with the right statistics is a true orbit of nearby initial
<<<<<<< main
  conditions" (representation.md thesis 2) in mixed phase space: the quantized law's
  trapping statistics are not the true ones at any Q tested (toy, 20261014-2248-redteam-5cad).
  Not refuted on the shipped law: preserved there, this scene, engine Q
  (20261015-0128-dynamics-b9be).
- "Deterministic rounding per event ≈ noise of the same magnitude" (the doc's error
  model implicit equation): 14.1% vs 1.2% permanent traps at Q = 10⁻³ (same toy run).
- "The toy's distortion transfers to the shipped law at engine Q": not in this scene —
  captured 54 vs 54, p90 13.6 vs 13.0 P, unchanged at 32× coarser cadence
  (20261015-0128-dynamics-b9be).

## Open directions

1. **The survival certificate** (the new separating statistic): the oracle-side pass is done
   (checker, P/256, both surfaces: zero contacts — no plane death stands for a real hit); what
   remains is the plane-side branch — sample the plane's own state at kick resolution through
   each death (or read the binding's terminal/periapsis) to decide real star-crossing periapsis
   of a diverged trajectory vs spurious planned terminal, at μ = 1e-2 too; then a false-death
   bar in B12's family for the co-orbital layer. This is what the integrator would gate.
2. **Stress the regime before trusting the preservation**: μ = 1e-2 (thicker layer), longer
   horizon, eccentric births; the toy's distortion peaked near critical K.
3. **Freeze the trapping-statistics rung** (criteria above) once B12's statistic is
   rebuilt — with the measured warning that dwell alone cannot fail a coarse law: the rung
   must include the survival class or it is a control.

## Contradictions

None open. The toy (rounding distorts) and the shipped law (preserved) measure different
error models at different Q; both stand, and the pair now names the boundary of the claim.
=======
  conditions" (representation.md thesis 2) in mixed phase space (20261014-2248-redteam-5cad).
- "Deterministic rounding per event ≈ noise of the same magnitude": 14.1% vs 1.2%
  permanent traps at Q = 10⁻³ (20261014-2248-redteam-5cad).
- "The standard map's Q-scaling transfers to the shipped dense order: coarser Q distorts
  the classes more, finer Q heals them": refuted — the engine-vs-twin statistics are flat
  across Q = 2¹⁶→2²⁰ (20261015-0128-inversion-3ca8).
- "State quantization is the channel": refuted on the shipped law — a grid-rounded twin
  with exact response reproduces the continuum statistics
  (20261015-0128-inversion-3ca8).
- **"The channel is the integer response's ensemble behaviour": refuted by the checker —
  a pure-f64 twin that mirrors the shipped respond rule (receding-skip) reproduces the
  engine's ensemble statistics on every seed tested, max dwell within 1.2×
  (20261015-0128-inversion-3ca8, checking). The author's 15–45% and 5×-dwell deviations
  measure the twin's rule mismatch, not quantization.**
- "Every single contact is the continuum impulse to 1e-5": true head-on only; at
  b/reach ≥ 0.2 with a moving COM the shipped law's continuum reflection differs from the
  SR COM mirror by up to 0.13 rad (checker, same run).
- "The two-body contact-carry ledger walk by itself mints a false behaviour class": the
  one-light pump is the same class in engine and continuum (both at the ceiling;
  20261015-0128-inversion-3ca8) — the walk shifts rates 10–20%, not classes.

## Open directions

1. **Rebuild the twin as the exact continuum limit of the shipped rule** (mirror the
   receding-skip; replace `sr_disc` with the law's own continuum reflection — e.g. the
   f64 Householder reflection about N = (d·P, E·d), or the law's rational targets at
   Q → ∞) and re-measure the classes across seeds and scenes. Expected from the
   checker's partial probe: quantization innocent; if any class metric still deviates,
   that residual is the real false-class result.
2. **Price the bin-crossing pass-through at game scale**: 87.5% of detected contacts in a
   relativistic gas exchange no impulse (fast bodies tunnel through each other, one
   chronon bin at a time). Contact rates in the real belt are far below this scene's,
   but flybys at game-relevant closing speeds inherit the rule; severity unpriced.
3. **The tilted oblique reflection**: whether the non-covariant bounce plane (axis
   tilted by the COM motion, up to 0.13 rad per contact) matters at game scale or should
   be corrected in the law — it is invisible to every ledger by construction.
4. Freeze the trapping-statistics rung on the shipped law once the twin is exact
   (5cad's missing rung, now with a shipped-scene protocol).
5. Hunt a stronger cantorus (K near critical) to bound the Q → 0 rate at which the
   distortion enters (abstract model; 20261014-2248-redteam-5cad).

## Contradictions

- **Q-scaling, abstract vs shipped:** the standard map distorts non-monotonically in Q
  (5cad); the shipped dense order's statistics are Q-flat (this run). Sharpened by the
  correction: the shipped deviation is not quantization at all, so the abstract result's
  "choose Q" advice does not transfer — recorded so no run spends a window raising Q to
  fix classes.
>>>>>>> 20261015-0128-inversion-3ca8

## Runs
- 20261014-2248-redteam-5cad (awaiting grade): shadowing clause false in mixed chaos;
- 20261015-0128-dynamics-b9be (silver): dwell arm on the shipped law — trapping preserved
- 20261015-0128-inversion-3ca8 (silver, corrected in checking): shipped dense order
