# Predictions (written before the decisive runs, 2026-10-08)

Tuning happened only on the pilot (seed 1, belt "spread"): plumbing, timing, sample-interval
safety. Nothing below is fitted to the held-out cases. All entropies are exact integer counts.

## Held-out cases

- `s2`: seed 2, n 4096, spread belt, ~30 inner orbits.
- `s3`: seed 3, n 4096, spread belt, ~30 inner orbits (independence of the seed).
- `inner`: seed 7, n 2048, a in [0.5, 3] AU (kicks frequent; Giant weak).
- `outer`: seed 11, n 2048, a in [3, 8] AU (Giant at 5.2 AU inside the belt: strong kicks).

## Point predictions

1. **Gross kick rate** (kicks per body per game-second, spread belt): order 10⁻⁵ (one kick per
   ~10⁵ body-seconds; the law is 128 kicks per radial period and periods are years). Inner belt
   ≥ 20× outer belt's rate.
2. **dv distribution**: strongly peaked at small |dv| quanta; H(dv) per kick between 4 and 14
   bits (the 2-D integer pair, self-entropy of the empirical distribution).
3. **Gross H_live** = rate × H(dv): between 10⁻⁵ and 10⁻³ bits per body per game-second.
   Prediction for the billion-body question: at 10⁹ bodies, one game-hour of this belt creates
   O(10⁴–10⁶ Mb) = O(1–100 GB) of gross distinction stream — the gross stream alone would NOT
   fit 8 GB if every kick were stored as a scar; the net state must be far smaller.
4. **Net deviation** D_i = Σ dv_i (normalized to one exponent): its cross-sectional entropy
   grows roughly as log₂ of its spread (random-walk-like, from ~zero at birth) and does NOT
   saturate within the horizon; bits per body after ~10 game-years: between 6 and 20 bits.
5. **Reabsorption**: most bodies (≥ 80% in the outer belt) never leave their birth (E, L) tube
   key within the horizon (key_changed = 0); in the inner belt a non-trivial fraction (5–50%)
   changes keys at least once. Bodies with D_i = 0 exactly: near zero in the inner belt (kicks
   rarely cancel exactly), majority nowhere — sub-quantum kicks accumulate in the carry, so
   exact zero is rare.
6. **Carry** (sub-quantum, in 2⁻¹⁶ of the velocity quantum): bounded, |carry| < 2¹⁶ per axis, as
   documented; it contributes ~32 bits of one-time state, not a growing stream.
7. **The plane's current store** (PlainBodies, bytes_of): ≥ 100× the 16-byte logical tube per
   body, dominated by the compiled cycle shape (knots) and the plan vec.
8. **Missed-kick check**: stray_items (engine item counter advances without a captured binding
   change) below 5% of captured kick items; if higher, the run reports it and the entropy is a
   lower bound.

## What would make the claim wrong

- If the net deviation entropy after 10 game-years exceeds ~40 bits/body, the "10⁹ fit in 8 GB"
  verdict flips to "cannot fit without reabsorption laws" (8 GB / 10⁹ = 64 bits/body total,
  including the program and the tube).
- If kicks per body per game-second scale with N at fixed distribution (they should not: each
  ship is kicked by the same three planets), the per-body extrapolation to 10⁹ is invalid.
