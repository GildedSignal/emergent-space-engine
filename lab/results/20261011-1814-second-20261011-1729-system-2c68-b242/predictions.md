# predictions.md — 20261011-1814 (second author on 20261011-1729-system-2c68)

Written before the decisive runs (gates and held-out seeds), after the calibration runs on seed 1
only. The jet is implemented in the crate's two kick paths (`Config::jet_bound_log2`); the trigger
is `off·age > 2^θ·r·T` (carry offset × window age, both maintained; the tube's own radius and
period; no exact-state reads). Calibration facts on seed 1 (already run):

- The offset-only trigger (the checker's Σ|Δv|·Δt, law.md's "offset reaches √(floor/C)") does NOT
  bound the error for Wisdom–Holman bodies: err ≈ ω·Δt·off (the window age multiplies the offset),
  2×10⁻⁴ at θ=10⁻⁶ on the orbiter. The age term had to be added (that is already a finding).
- The clock bodies (motion law v2, the ships of B12/B13/B17) hold the floor: err ≤ 5×10⁻⁷ at
  θ=2⁻²⁰ (intervals 50–165 kicks), seed 1.
- WH bodies compound ACROSS rebinds (the rebind anchors to the carried state, not the truth; the
  old probe reset to the exact state, which is why its "bounded by construction" held): the orbiter
  reaches 3×10⁻⁵ over 47 rebinds at θ=2⁻²⁵.

## Predictions (held-out)

1. **Gates.** `behave --law plane --gates B12,B13` with the jet on (θ=2⁻²⁰): both still PASS.
   The gates' ships are all clock bodies (the scene is star + planet + ship; the planet is a pure
   tube — nothing kicks it — and the ship rides the v2 clock), where the jet holds ≈10⁻⁶.
   B12's Jacobi judge reads a bounded error of that size as noise, not growth. B17 (slow): if it
   finishes in time, PASS as well; resonant pumping is a clock-body behaviour.
2. **Held-out seeds (2, 7), clock bodies (Hauler 2 = ships[1], Hauler 7 = ships[6]), θ=2⁻²⁰,
   3000 kicks:** median interval 40–150 kicks on both seeds (the checker's own numbers were
   146–903 at 10⁻⁶ with the exact-state shadow; the age trigger fires earlier than the offset
   alone), and max relative error ≤ 2×10⁻⁶ on both seeds. The recompile rate stays inside
   1/30–1/300 per kick.
3. **Held-out seeds, WH bodies (Orbiter 3 = ships[14], Home = id 1):** the compounding shows on
   every seed — max relative error ≥ 10⁻⁵ at 1000 kicks at any θ that amortizes (interval ≥ 10);
   i.e. the WH-side failure is structural (curvature lag per interval, summed over rebinds), not a
   seed artifact.
4. **Cost.** The pure kick resolve (cost_split, ship 14) drops from ~34 µs to ~21–25 µs under my
   load with the jet on at θ=2⁻²⁰ (rebind amortized at 1/interval, carry arithmetic added);
   order-of-magnitude only (cloud, shared load).

If (1) fails: the reader path (which does not carry the carry) leaks into the gates' answers —
that would be the named gap for the builder, and I report the failure mode.
