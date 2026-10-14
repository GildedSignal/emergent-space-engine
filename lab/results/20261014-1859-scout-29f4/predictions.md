# Predictions — 20261014-1859-scout-29f4

Question: can the encounters tier deliver a conjunction impulse as **exact integers on the
shipped key's own quanta** (b29a's named dependency for the 0.11 µs key-space arm), and does
increment-rounding stay inside the shipped refit's own discretization class over a kick train?

Setup: shipped pub API only (`OrbitKey::bound`, `Orbit::compile`, `Orbit::state`,
`binding::cartesian`, `Rebinding::from_state`); the impulse is applied as exact power-of-two
fractions of the state's own integer velocity components (no rounding in the draw); the key-arm
delivery is ΔE = E(v+Δv) − E(v), ΔL = L(v+Δv) − L(v) with E, L the fit's exact rational
invariants (fit_key's algebra: kinetic = vr²/lapse + vt², den = lapse − kinetic, L = r·vt/√den,
E² = lapse²/den with den = (dτ/dt)² = lapse − kinetic, u = 1/r, lapse = 1 − 2u; corrected pre-run from the C0 control's failure — the first grouping multiplied by L² and failed C0 by ~10⁶ quanta) — a deterministic integer
function of the event's exact integers, O(1) work, no O(u) approximation.

Cases below are **not tuned on**: belt-band keys at p ∈ {2048, 20000, 2×10⁶} M (u = 4.9×10⁻⁴ …
5×10⁻⁷), e ∈ {0, 0.07, 0.3}, readout times spread over the cycle, impulse scales 2⁻⁴⁰ … 2⁻¹⁰ of
the state's own velocity, three directions (radial / transverse / parallel).

- **P1 (single-kick equivalence).** |E_arm − E_refit| ≤ 2 Q48 quanta and |L_arm − L_refit| ≤ 2
  Q32 quanta at every swept point where the impulse moves E by ≥ 1 quantum: both paths are
  quantizations of the same exact kicked invariants (the refit via its OrbitKey, the arm via the
  rounded increment), and the refit's own input grid (i64 state at per-state exponents) is ~2⁻⁶⁰
  relative — far finer than Q48.
- **P2 (the walk).** Round-to-nearest increments: |E_arm − E_true| grows ≈ ½√N quanta
  (unbiased random walk); floor-to-nearest-increment (shipping darwin's floor semantics applied
  to the *increment*) grows ≈ ½N one-signed — the delivery must round to nearest, never floor.
  The refit stays bounded ≤ ~1 quantum at every N (re-anchoring; this is also control C1).
- **P3 (observability).** At belt energies (|1−E| ~ 10⁻⁴ … 5×10⁻⁹ in key units) neither channel's
  walk reaches an observable orbit change at N = 10⁴: predicted |Δa|/a ≲ 10⁻¹⁰ for the rounded
  arm (≈ 2·|ΔE|/|1−E| with |ΔE| ~ 50 quanta = 1.8×10⁻¹³ absolute), ~100× more for the floored
  arm — both far under the belt's own e ~ 0.07 spread; the encounter calendar and the view
  re-derive from the current key, so no stored state compounds.
- **P4 (sub-quantum control, f0a2's domain).** For impulses < ½ quantum: the arm's key moves on
  0 of the cases (accumulator domain); the refit's key flips only where the exact E crosses a
  lattice cell — flips ≈ lattice crossings, each flip exactly 1 quantum.
- **P5 (price).** The delivery arithmetic (≈ 12 i128 multiply/square + 2 isqrt + 2 wide divs)
  measures ≈ 0.1–0.5 µs; `Rebinding::from_state` re-measures ≈ 20–30 µs on belt keys (b29a: 21 µs
  p50); the honest composed key-arm kick = 2 exact state reads (~4–5 µs each, the tier's own
  event reads) + delivery — the reads dominate, so cf45's 0.11 µs row is the update alone, and
  the eager compile (the refit's) is deferred, not paid.

Kill criteria (frozen before the run):
- **K1:** any swept point with impulse ≥ 1 quantum and |E_arm − E_refit| > 4 quanta (or L > 4)
  → the delivery is not equivalent; investigate the algebra before any adoption claim.
- **K2:** the rounded-increment walk grows faster than √N (superdiffusive), or the floored walk
  is < 10× the rounded walk at N = 10⁴ → the rounding-semantics claim is wrong.
- **K3:** the arm's orbit-shape drift (binding-relative |Δ(1−E)|/|1−E| and ΔL/L) exceeds the
  refit's by > 100× at N = 10⁴ → the arm leaves the law's discretization class.

Controls:
- **C0 (algebra):** my exact-rational E, L evaluated on the *un-kicked* shipped state must equal
  the initial key's darwin-inverse E, L to < 0.1 quantum (else my invariants are wrong and
  everything stops).
- **C1 (positive):** the refit arm's own |E − E_true| ≤ 1 quantum at every N (if the re-anchored
  control walks, the truth tracker or the fit comparison is broken).
- **C2 (negative):** zero-impulse (2⁻⁵⁰ scale) kicks leave every key bit-identical in both arms.
