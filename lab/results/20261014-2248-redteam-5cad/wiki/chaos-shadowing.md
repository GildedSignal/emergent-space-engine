topic: chaos-shadowing
status: open
closed-by:
valid-while:
updated: 20261014-2248-redteam-5cad

# Chaos, the shadowing clause, and trapping statistics under quantization

## Current best

**The shadowing clause of representation.md's thesis 2 is false in mixed-phase-space
chaos, in both directions, and no rung or gate tests it
(20261014-2248-redteam-5cad).** The clause: "Even chaos has invariant statistics, and
by the shadowing lemma a deterministic law with the right statistics is a true orbit
of nearby initial conditions." Standard map K = 1.2, the quantized law = the doc's own
error model (state rounded one floor unit per event, never compounding in magnitude).
Measured on a 256-IC sticky ensemble (thin chaotic band beyond each of 32 angles'
outermost KAM curve, dwell = continuous stay in the enclosing island disk, cap 10⁵):
true dwell p90 = 2,821, capped 0%; quantized **inflates** the tail (Q = 10⁻³: p90 =
cap, 14.1% never escape; Q = 10⁻⁴: 2.7% never escape) and at coarse Q **crushes** it
(Q = 10⁻²: p90 = 512, 5.5× down) — invariant statistics are not preserved at any Q,
non-monotonically. Deterministic rounding is not interchangeable with same-magnitude
noise (noise arm: 1.2% capped): rounding breaks area-preservation, the one symmetry
Hamiltonian chaos has, and builds spurious invariant structures. [Corrected by the
checker:] the noise-deviation arm is retired as an instrument — noisy copies vs the
same-IC reference measures mixing, not shadowing, and a provably shadowable Anosov
control (cat map) shows the same torus-scale decorrelation signature — so no claim
about shadow bounds is made. Non-shadowability of the trapped orbits follows instead
from the dwell arm itself: no sampled true orbit of the band survives past 1.7×10⁴
(0/256 reach the 10⁵ cap), against 14.1% of quantized orbits, so the permanent traps
are shadowed by no nearby true orbit the ensemble can see (heavy-tail caveat: the true
dwell tail is a power law; the 95% bound on true permanent traps is ~1.2%, still 12×
below the quantized rate). The regular island's deviation grows to ~1 by 10⁴ steps
(angle drift on nearby tori, re-diagnosed; actions not measured) — so the
behaviour-class metric, not phase distance, is the instrument. Error-type consequence
(principle 2): the dense order's chaotic orbits are not IC-uncertainty orbits; they
are false behaviour classes (captures that never dissolve, or dissolve early).
Controls: KAM orbit unchanged under Q = 10⁻² quantization; Q = 1.0 scrambles; the
noise arm separates from the quantized arm. Missing rung: trapping-statistics equality
(quantized law vs float oracle, capped-fraction within 2×, p90 within 1.5×; positive
control the float law + sub-quantum noise, negative Q = 10⁻²) — B12's family is the
natural home.

## Refuted

- "A deterministic law with the right statistics is a true orbit of nearby initial
  conditions" (representation.md thesis 2) in mixed phase space: the quantized law's
  trapping statistics are not the true ones at any Q tested (20261014-2248-redteam-5cad).
- "Deterministic rounding per event ≈ noise of the same magnitude" (the doc's error
  model implicit equation): 14.1% vs 1.2% permanent traps at Q = 10⁻³ (same run).

## Open directions

1. **Repeat the dwell arm on the shipped law:** `es-space-v2` dense order around a
   co-orbital island (the wiki's own fleets-as-rotating-frame-structures regime),
   quantized vs float oracle, at the engine's Q. If the distortion is there, the
   design text drops the shadowing clause for a certificate.
2. **Freeze the trapping-statistics rung** (criteria above) once B12's statistic is
   rebuilt — same family, different target (behaviour class, not error magnitude).
3. Hunt a stronger cantorus (K near critical) to bound the Q → 0 rate at which the
   distortion enters; this run's tail was modest (max true dwell 1.7×10⁴).

## Contradictions

None open. The sea-decorrelation arm (exotic, easy) and the trapping arm
(player-visible, hard to calibrate) agree: no shadow bound, statistics not preserved.

## Runs
- 20261014-2248-redteam-5cad (awaiting grade): shadowing clause false in mixed chaos;
  quantization inflates or crushes trapping tails by Q; rounding ≠ noise.
