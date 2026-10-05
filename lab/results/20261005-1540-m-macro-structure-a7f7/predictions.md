# Predictions (held out before the decisive runs)

Run 20261005-1540-m-macro-structure-a7f7. Written before any of the three probe
scripts was run past a smoke case. The cases below are deliberately ones I did not
tune on; each probe also has a control whose outcome is already known (a control
that misbehaves voids the probe).

## P1 — integer multiresolution moments (dyadic quadtree, Haar-style) for the kick field

Scenes: an annulus belt (4096), a two-arm Zipf galaxy (4096), belt+one dense battle
cluster (4096+256). None was tuned on; the ε sweep is the measurement.

Predictions:
1. **Error is ε-controlled:** max relative potential error grows ≈ linearly in ε
   (up to a log factor), with no erratic outliers on any scene, including the
   battle scene. If the error is erratic or jumps by >10× when ε halves, the
   representation's error model is wrong — kill.
2. **Sparsity where the scene is smooth:** at 10⁻³ relative error, node visits per
   query ≤ ~1/10 of direct terms on belt and galaxy (i.e. the smooth field is read
   from O(polylog) nodes), and the battle cluster only forces deep traversal near
   itself: the belt points' visit p99 changes by <2× when the cluster is added.
   If visits per query on the smooth scenes scale like N^0.3 or worse at matched
   error, the wavelet criterion buys nothing over per-body summation — kill.
3. **Per-level shared exponent:** the bit-length spread of detail coefficients
   (|D|₁/(M·S), per level) fits within ~16 mantissa bits for ≥99% of nodes at each
   level. If a level needs >24 mantissa bits, 32-bit level-indexed packets
   (bottleneck 0's "level as shared exponent") do not hold — kill the packet claim.
4. **Determinism control:** integer tree evaluation is bit-identical under a
   randomized visit order (expected: identical); the same experiment in float64 is
   not (expected: some queries differ in the last bits). This is the control; if
   the integer sums differ, my arithmetic is broken, not the representation.

Outcomes I would count as negative but informative: matched-error work within 2×
of Barnes–Hut with θ=0.75 (then the win is exactness + no geometric criterion, not
raw work — I state this as the likely outcome, not a failure); visits per query
growing with N on the galaxy scene (then the gain is per-scene, not asymptotic).

## P2 — holonomy of integer-shear handoff loops (three dolls, R3's shears)

Three frames A, B, C with pairwise relative velocities at β ≤ 0.9; the loop
A→B→C→A applied n times to an event offset. Controls: (a) out-and-back is the
identity bit for bit (R3's measured claim, 4000/4000 — I expect to reproduce
1000/1000); (b) the rational (unfloored) composition of handoffs *derived from one
consistent frame table* is exactly the identity — if not, my construction is wrong.

Predictions:
1. **Atlas consistency:** if each pairwise handoff quantizes its own relative
   velocity, the un-floored rational loop is *not* the identity: a systematic
   defect ~2⁻ⁿ per loop (n = the shear coefficient word) that grows **linearly**
   with loop count. If handoff parameters are derived from each doll's quantized
   absolute state (one table, group-consistent by construction), the rational loop
   is exactly the identity. Expect: per-pair quantization drifts; derived
   quantization does not. This is the adoptable rule either way; measuring it is
   the point.
2. **Floor holonomy without carry:** the floored loop's defect grows with exponent
   ≈ 0.7–1.0 (mostly systematic drift; floors are deterministic and correlated on
   a periodic orbit). If it is already bounded (exponent ≤ 0.1), no ledger is
   needed and I report that.
3. **Floor holonomy with a sigma-delta carry per shear:** bounded, exponent ≤ 0.1
   (defect ≤ ~1 unit per handoff, forever).
4. **Per-event budget:** each single handoff's rounding defect ≤ 1 coordinate unit
   at β ≤ 0.9 (the error model's "one floor unit per event"). If a single handoff
   moves an offset by >2 units at moderate β, R3's own error budget fails at B12's
   20 crossings — that would be a red flag for the plane, not for this probe.

## P3 — self-sizing memo keys: the sensitivity map of the Schwarzschild cycle map

Δφ, Δt, Δτ per radial cycle in Darwin's phase, by quadrature, over the bound plane
(p from ~7 to 1000 M, e from 0 to 0.99). Measured: the largest cell width (relative,
dyadic) over which sharing one compiled cycle keeps every output within one
quantum (w_safe), and whether the first-order jet (offset + stored derivatives,
law.md's strong-field reuse) suffices at that width.

Predictions:
1. **Bulk:** w_safe ≥ 2⁻¹² for p ≥ 8M and e ≤ 0.6 (a 12-bit shared key is already
   behaviour-exact; far coarser than 32 bits — massive sharing).
2. **Separatrix/plunge boundary:** w_safe collapses (< 2⁻²⁰) in a boundary layer
   whose relative thickness in (p, e) is small (a few % of the plane's area).
   If instead w_safe is uniformly tiny everywhere (≤ 2⁻²⁴), sharing never pays and
   the memo/jet design is dead weight — kill the sharing claim.
3. **Jet validity:** at w = w_safe, the second-order term is ≤ 1 quantum over
   ≥ 90% of the bound plane (the stored first derivatives, already in the memo per
   law.md line 14, make reuse exact to the quantum). If the jet needs second
   derivatives over a large fraction, the "jet" form is the wrong representation —
   report where.
4. **Smoothness:** the sensitivity field is smooth (no fractal contour structure),
   so a dyadic key width chosen from the leading bits of the *already stored*
   derivative is sufficient. If the field is non-smooth, adaptive dyadic keys fail.

## What would make each probe's claim wrong (pre-stated)

- P1: erratic error vs ε; no sparsity gain on smooth scenes; level packets need
  >24 mantissa bits.
- P2: floors already bounded without any carry (kills the ledger claim — fine);
  out-and-back control failing (voids my construction).
- P3: w_safe uniformly tiny (kills cycle sharing); non-smooth sensitivity (kills
  dyadic adaptation).
