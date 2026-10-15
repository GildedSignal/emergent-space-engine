topic: chaos-shadowing
status: open
closed-by:
valid-while:
updated: 20261015-0128-inversion-3ca8

# Chaos, the shadowing clause, and trapping statistics under quantization

## Current best

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

## Refuted

- "A deterministic law with the right statistics is a true orbit of nearby initial
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

## Runs

- 20261014-2248-redteam-5cad (awaiting grade): shadowing clause false in mixed chaos;
  quantization inflates or crushes trapping tails by Q; rounding ≠ noise.
- 20261015-0128-inversion-3ca8 (silver, corrected in checking): shipped dense order
  measured against a twin that is not its continuum limit; channel inverted —
  quantization innocent at ensemble level, 87.5% of contacts are no-impulse pass-throughs.
