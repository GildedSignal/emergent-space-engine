# Predictions — second author, run 20261010-1816-second-20261010-1706-redteam-e07f-311d

Written after the pilot (conventions fixed), BEFORE the decisive sweep/stair/flip runs.
The question (checker's one experiment): does r1's ISCO phantom shelf / ω_r cliff
survive in the SHIPPED law (`space-darwin16-scaled-v5`, `Rebinding::from_state` —
the plane's own binding path), through its exact-key algebra, its 12+12-bit memo
quantization, or its ψ-cut band panels?

## E1 — classification sweep (band of 6M ± 1 band, ε ∈ {+1e-3, −1e-3, 0}, 2401 r₀ each)

The law's verdict (bound vs NoBoundOrbit) is decided by exact per-state algebra
(fit_key's barrier/discriminant + exact BigInt fallback near the separatrix), so:

- P1: the misclassified set (law=bound where the exact-Binet oracle plunges, or
  law=refuse where the oracle binds) has width **< 1e-5 M** at the boundary —
  i.e. no strip at the sweep's resolution (r1-band: 0.093 M = 1.54% of 6M).
  I expect the only disagreements, if any, to sit within a few 1e-4 of the
  family's separatrix AND to be oracle-resolution artifacts (zoom-whirls deeper
  than φmax): bound-side whirls near the boundary whirl ~10²–10⁴ revolutions
  before acting; the plunge side does the same then falls. I will extend the
  oracle adaptively (φmax 3×10⁵) on any disagreement before counting it.
- P2: the boundary between the law's bound and refuse verdicts is a single
  step (one r₀ interval), the same place for all three ε classes up to the
  physics of the separatrix (inward class boundary slightly below 6.0;
  outward class slightly below that; razor-thin zoom-whirl band between).
- P3: the headline case r₀=5.95: inward class refuses (plunge ✓ GR), outward
  class compiles bound (zoom-whirl ✓ GR, checker measured r ∈ [5.956, 6.102]).

## E2 — staircase error (exact keys, e = 1e-3, p over (6.0021, 7.0))

- P4: max |advance_law/advance_GR − 1| < 1% (r1-band: 31.5%). The crate's own
  near_circular tests gate this family at 1%; the sweep window is inside it.

## E3 — the rim (p → 6+2e, d down to 1e-6, e = 1e-3)

- P5: the compiled advance diverges smoothly, tracking GR's whirl divergence
  (relative error < ~2% at every d ≥ 1e-6), with no cap, no jump, no refusal
  from the ψ-cut panels (r1-band: cliff — first stable band gave 2.4× GR at
  r = 6.05, and ω_r frozen at 0.22 instead of → 0).

## E4 — adjacent-key jump on the shipped law's coarsest grid (memo 12+12 bits)

- P6: worst adjacent advance jump over p ∈ (6.0, 6.6), e = 1e-3, ~1–3%
  (∂Δφ/∂r · δr/r ≈ 5.66·6·2⁻¹²/0.57 ≈ 1.4%), **< 5%** (r1-band: 181.8%).

## E5 — memo quantization flip (storage path, not the live classification path)

- P7: bound exact keys with p within ~1 periapsis quantum (2⁻¹² relative ≈
  1.5e-3 M at r ≈ 6) of the separatrix p = 6+2e flip to refused when compiled
  through `memo_key()` (mirror: a razor-thin whirl destroyed at storage).
  Predicted flip-window width ≈ 1–2 quanta ≈ (1.5–3)×10⁻³ M — ~30–60×
  narrower than r1's 0.093 M strip, and NOT on the engine's binding path
  (engine/tube.rs:158 compiles the exact key; `memo_key` appears only in the
  8-byte population memo). If flips are wider than ~0.01 M, that is a live
  storage defect and I will say so.

## Side finding from the pilot (not the decisive question)

- The exactly-circular state at r = 7.0 M (dyadic radius, r1's frozen probe
  radius) is refused with `Range` by `Rebinding::from_state`; ±8 position
  quanta away it binds, and 5/6/9/10/20/100 bind. binding.rs:275-277's
  word-rounding guard is the suspect (word saturates at 1<<48, then the
  2⁻²⁰ relative check throws). Measure-zero locus; report with the one-line
  reproduction.

## Kill criteria

- If E1 finds a misclassified interval wider than 1e-5 M, or E4 a jump ≥ 5%,
  or E5 a flip window ≥ 0.01 M: the original claim upgrades to a live-engine
  defect (urgent gold) and I report it as such.
- If all pass: the phantom shelf and the ω_r cliff are properties of r1's
  retired band-frozen family alone; the claim stands as the reason that family
  stays dead, plus a two-case r1 gate fix (and this side-finding).
