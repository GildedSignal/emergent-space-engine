# Predictions (written before the decisive experiment, 2026-10-18 15:58)

Run: 20261018-1530-components-e87d. Question: does a beat-resident pair record
(encounters od 1's named design step) cut the wholesale per-kick re-arm soundly,
or does it die the deep-beat re-roll's death?

Instrument: exact integer sections of the shipped tier (`arm_sections` +
`arm_pair`'s integer setup + `dioph::first_hit`) on a `make_belt`-class cell
population (a ∈ [2, 2+2·10⁻⁴] AU, σ_e 0.07 cap 0.5, seed 20261018), ρ = B =
3.34×10⁻⁶ AU (5×10⁵ m, the design reach), kicks = impulsive dv = 2⁻²³·v (belt
quantum, 3294's fired impulse) in random directions, applied exactly through
state → element reconstruction. Not tuned on: a second seed, ρ = 10 B, and
dv arms 2⁻¹⁷ / 2⁻¹⁴ (1a29's checker arms).

Arms not in the tuning set are marked HELD-OUT; everything below is what I
expect before running.

- **P1 (negative control):** dv = 0 → every section, first hit, slack, and
  decision bit-identical; 0 flips of any kind.
- **P2 (positive control, the kill's reproduction):** silent→armed flips of the
  stored due [k_first ≤ 10⁶ passages] at dv = 2⁻²³: **3–10 × 10⁻⁶ per candidate
  per kick**, dv-independent within 2× across 2⁻¹⁷/2⁻¹⁴ (1a29 measured 5–7×10⁻⁶
  on the shipped tier; if my instrument misses this order, the replica is wrong
  and nothing below counts).
- **P3 (the design's premise — slack exists):** at L = 10³ conjunctions, ≥ 90%
  of candidate pairs have slack_L > 10 window widths w, and the slack
  distribution's median is ≫ w (the beat leaves room to live in).
- **P4 (drift):** one quantum kick moves slack_L by less than the slack itself
  at L = 10³ (median |Δslack| < 0.3·slack), the drift growing roughly linearly
  in L (beat-index sensitivity). At L = 10⁴ I expect the drift to approach the
  slack (honest uncertainty; this is where the certificate's horizon may end).
- **P5 (the certificate):** with margin μ = 30 w, leak (certified-safe pair
  acquires an in-window hit ≤ L after one quantum kick) ≤ 10⁻⁵ per candidate
  per kick at L = 10³, and re-arm rate (slack_L falls below μ·w) ≤ 0.02/kick —
  a ≥ 30× cut of the wholesale 1 eval/pair/kick (355 cores → ≤ 12).
- **P6 (risk, the Wide class):** sections of Kind::Wide (the checker's fat
  w/d ~ 0.3–1 windows) carry little slack and own most of the leak; if ≥ 10% of
  pairs carry a Wide section, the certificate must be per-kind and the row
  splits by section kind.

**Kill criterion (frozen):** the beat-resident certificate dies if at every
(L ≤ 10⁴, μ ≥ 30 w) either leak > 10⁻⁵/cand/kick or re-arm > 0.1/kick
(a ≤ 10× cut is not adoption-grade against the 355-core wholesale row).
It also dies if P2 fails to reproduce (the instrument would not be measuring
the shipped tier's object).

**Pricing arithmetic (agreed with the record):** wholesale sound re-arm = 1
eval/candidate/kick = 355 M1-cores per 10⁴-occupancy cell at 1 µs/eval
(1a29's checker clock). The beat record's price = re-arm rate + leak-allowed
news 10⁻⁶, in the same units.
