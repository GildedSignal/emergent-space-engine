# Predictions (written before the decisive sweep)

Question: what is the real skip rate of detected contacts in the flown fleet (contact-speed
od 3), and does it follow the Chronon-bin law P(skip) = max(0, 1−ρ) (8144)?

Setup: `xtask universe --bench --unpaced --rtf 100 --seconds 30 --seed 1 [--members N]`,
`SPACEX_SPEED_DIV` dial on `scenes::battle`'s speed divider, `SPACEX_ORDER=dense` flies the
same world through `Chronon`. Census at the resolver gate (`relativity.rs`): every pair that
reaches a response batch logs (|w|², d·w, reach); skip ⟺ d·w ≥ 0, exact integers.

Scene geometry: reach = r_a + r_b ∈ [q, 2q] with q = 2²⁰, radii drawn q/2..q; per-side speed
v = q/speed_div; |k| < q (subluminal). ρ = reach/|w|.

Arms (speed_div, members, order): (32768, 48, sparse) = shipped; (32768, 400, sparse);
(128, 48, sparse); (8, 48, sparse); (2, 48, sparse); (2, 48, dense); held-out seed 2 on
(2, 48, sparse) and (2, 48, dense).

Predictions:

- **P1 (shipped arm).** Skip fraction exactly 0; |w| ~ 10–200 quanta/chronon; ρ ~ 10³–10⁵.
- **P2 (fast sparse arms, 128 and 8).** Skip fraction still exactly 0, even where ρ < 1
  appears, because EventCore resolves a pair at its root tick with bin-start positions,
  which `hit` guarantees approaching (d·w < 0): a single-pair component cannot skip at any
  speed. Any skips that do appear must come from multi-pair components (contamination);
  I expect ≤ 2% (1648's fleet-speed contamination bound).
- **P3 (fast dense arm, speed_div 2).** The same world through Chronon skips: the pairs with
  ρ < 1 skip at ~max(0, 1−ρ) over arrival phase — I expect a skip fraction of order 10–30%
  of detected contacts there (closing ~q..1.4q against reach 1..2q straddles ρ = 1).
- **P4 (held-out seed 2).** Same qualitative verdicts on both steppers.
- **P5 (structural bound).** In every arm, ρ ≥ ~0.5 by construction (reach ≥ q against
  |w| < 2q): the battle scene cannot reach the deep-skip regime (ρ ≪ 1) at any legal speed,
  so even the dense arm's skip fraction is capped well below the gas scenes' 48–87%.

What would falsify the mechanism reading: skips > 2% on any sparse arm at ρ ≥ 1, or zero
skips on the dense speed_div-2 arm with a non-trivial ρ < 1 subpopulation.
