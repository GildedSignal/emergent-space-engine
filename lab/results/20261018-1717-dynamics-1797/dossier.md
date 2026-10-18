# Dossier — 20261018-1717-dynamics-1797 (dynamics lens)

**Claim.** The order boundary's circle ratchet obeys an exact diffusion law — the minted
deficit satisfies D² = 2Cn (R² = 0.99999, β = 0.50) with rate = C/D a function of state,
not history — so the walk self-arrests onto the 1-ulp translation floor, and the
do-nothing price of the compact row's k column is ≈ 2.8×10¹² crossings to 1% of range,
4000× the record's linear pricing.

**Bottleneck.** Not a hot-path cost: this closes order-boundary open direction 2's named
gap ("the circle ratchet's deceleration law — one rung would close it") and re-prices the
page's frozen decision (anchor w and t, or carry the residual, or do nothing). Expected
gain: deletes any urgency on the w-anchor/residual-carry work for k at circle scale —
the measured law is 4000× more harmless than priced — and names the census's two classes
by exponent (eccentric: β = 1 translation; circle: β = ½ diffusion).

**Evidence** (all from `regen.sh`, 13 s warm / ~3 min cold; every number below is in
`analysis.txt`):

- Probe: `crates/space/examples/circle_ratchet.rs` (the run's only code change,
  `work/patch.diff`), chaining the shipped seam map — `Orbit::compile` → sample at a
  true odd-eighth phase of the key's own period → `binding::cartesian` at the doll word
  (position integers ~2⁶¹, velocity 2⁻⁶²) → `Rebinding::from_state` → next key —
  8 arms × depth 65536, 327,680 crossings, zero refusals, zero class flips, ~36 µs each.
- **Instrument anchors, exact**: e = 0.5, p = 2²¹ M, φ = 3/8 → **−13 ulps on 4096/4096
  crossings**; e = 10⁻³, p = 2²¹ M → **−1 on 4096/4096** (both are 9dbb's recorded
  constants, reproduced first try); depth-1024 circle rates 3.5–4.1k ulps/crossing,
  within 2× of the record's 5.2–7.6k band.
- **The law**: D² = 2Cn fit over 64 points per arm — p21 φ=1/8: C = 2.602×10¹⁰,
  R² = 0.999991; φ=5/8: C = 2.536×10¹⁰, R² = 0.999993; w₀=3/8: C = 2.606×10¹⁰,
  R² = 0.999985; log-log β = 0.497–0.501, rate α = −0.494 to −0.498 (predictions' band
  [−0.75, −0.35], centred on −0.5).
- **State feedback (P2)**: arm seeded at e₀ = 10⁻⁶ diffuses with C = 2.568×10¹⁰ — 1.2%
  from the circle's 2.602×10¹⁰; e₀ = 10⁻³ sits at the −1 floor (see below).
- **Word control (P7)**: doll word 2⁴³ instead of 2⁶¹: C = 2.289×10¹⁰ (−12%), same class
  (99% negative, β = 0.488, R² = 0.99993).
- **Price**: composite law — diffusion to D = C at n = C/2 ≈ 1.3×10¹⁰, then the 1-ulp
  pin — gives ≈ 2.8×10¹² crossings to D\* = 1% of k's range (2.8×10¹² ulps); the
  record's linear price was ~7×10⁸. Minted e ≤ 2.6×10⁻⁶ at any horizon ≤ 10⁹ crossings.
- **w column**: 99% of Δw increments negative at φ = 1/8; drift −1.4×10⁻⁵ turns/crossing
  (−5.3×10⁻⁶ at φ = 5/8, −5.1×10⁻⁵ at p = 2³⁰); rare jumps (7 > 10⁻², 1 > 0.1, max
  0.375 turns); cumulative path = drift × n exactly by 65536 (one turn per ~7×10⁴
  crossings); the e = 10⁻³ arm's w is frozen (0 jumps, drift 2×10⁻¹⁰).
- **Invariants**: max |ln r| = 1.5×10⁻⁷ < 2⁻²⁰ on every arm; periapsis drifts −2.1×10⁻⁷
  relative over 65536 crossings; k_exponent = 0 throughout.
- **Domain edges**: strong field p = 12 M mixes signs (40% negative; D²-linearity R² =
  0.70, β ≈ 0.46) — the clean one-signed diffusion is measured at 2¹²–2³⁰ M only as a
  clean law at ≥ 2²¹ M; the pin's approach (D between 5.8×10⁷ and C = 2.6×10¹⁰) is
  interpolated between two measured ends, not traversed (it would need ~10¹⁰ crossings).

Commands (each ≤ 60 s after one build): `sh lab/results/20261018-1717-dynamics-1797/regen.sh`
(build + both runs + full analysis into `analysis.txt`).

**Predictions** (`predictions.md`, written before the deep run): P1 (rate = C/D, D ~
n^½, α ∈ [−0.75, −0.35]) **held** (−0.494 to −0.498); P2 (state feedback within 2×)
**held** for e₀ = 10⁻⁶ (1.2%); the e₀ = 10⁻³ arm pins at the 1-ulp floor — the floor
consequence was anticipated but the pin itself was not pre-registered as a number, and
against the naive C/D curve that arm reads 10× high: the composite law is the post-hoc
synthesis, measured at both ends. P3 (w a fair lottery within a √n envelope) **failed in
substance**: my Gaussian yardstick was the wrong instrument for a jump process, and the
real finding is a one-signed w drift, −1.4×10⁻⁵ turns/crossing, dominant by depth 65536
— the record's "pure lottery" read was depth-limited, not wrong at its depth. P4 (radius
< 2⁻²⁰) **held** (1.5×10⁻⁷). P5 (zero refusals) **held**. P6 (β ∈ [0.4, 0.6]) **held**;
its numeric price mis-stated D\* as 2.8×10¹¹ (the correct 1% of 2⁴⁸ is 2.8×10¹²) —
corrected above, and the "quadratic in target" statement needs the floor qualifier.
P7 (word class-invariance, C within 10×) **held** (12%).

**What would make it wrong.** The diffusion law is measured on the composed seam map at
one observation phase per arm (odd eighths), unity-scale doll words, planar prograde
arms; the real boundary re-quantizes to the belt Spec's column widths (rates are lower
bounds, as the page already records) and mixes cw senses. The pin segment assumes the
one-signed walk cannot fall below 1 ulp/crossing (integer quantum) and that the −1 class
it decays onto is the e₀ = 10⁻³ class — a walk could instead alternate −1/0 (b9c8's
mixed class) and halve the pin's rate, moving the price by ≤ 2×. The strongest falsifier
would be a seeded arm at e₀ ≈ 10⁻⁵–10⁻⁴ run to ~10⁷ crossings landing off the C/D curve.
Adoption cost: zero — this is a measurement that re-prices a frozen decision (do nothing
on k; the w drift adds a slow term to od 4's encounter-tier question). PRINCIPLES 13
("errors never compound… divergence is not a joke and it compounds"): the k compounding
is real but self-arresting (β = ½, floored), and the record's Principle-13-at-the-seam
verdict is strengthened: violated in the letter, satisfied in effect at any flyable
horizon, now with the exponent measured. Lens (dynamics): the attractor question the lens
asks of every rounding walk is answered here with a clean exponent and a mechanism
(state-fed rate), but the lens bought it at one phase class and prograde senses only;
the retrograde and even-phase refusal classes (b9c8's domain notes) were not swept, and
the w drift's interaction with real contact outcomes is unmeasured.
