# Predictions (written before the decisive run)

Question: read-stream open direction 2's two halves — (a) the compile's split
(shared quadrature `OrbitShape::bound` vs per-key `from_shape` glue) on the flown
key mix; (b) the exactness of `from_shape(exact key, quantized shape)` (the
"cheapest next probe" the page names).

Instrument: keys captured from `ladder_digest "N=3000 coast through"` (the same
case 588d used, digest-neutral control); standalone bench `compmemo` on the
captured stream, interleaved arms, controls both sides (bit-identity of the
identity path; shuffled-class negative).

Pre-registered expectations on held-out structure (not tuned on):

- **P1 (split):** `OrbitShape::bound` ≥ 70% of `Orbit::compile` on the flown mix.
  If glue > 30%, the shape memo's ceiling halves and the direction loses its prize.
- **P2 (exactness, the decisive one):** the exact-key + class-shape arm's period
  error is ~10⁻⁴ class (predicted p50 1–4×10⁻⁴ relative), because the class quantum
  on k is 2⁻¹¹ and the Darwin period's sensitivity is |dlnP/dlnk| = 3k/(2k−1) ≈ 3.2
  at the belt's e — i.e. the shape-class memo is a LAW CHANGE, not a bit-exact
  delete. Upset that would keep it alive as a delete: p50 < 1×10⁻⁶ relative.
  Instrument-broken signal: p50 > 1×10⁻².
- **P3 (vs the known arm):** the shipped QuantizedMemo (quantized key, the known
  2⁻¹¹-period change) is within 4× of the exact-key arm — the exact key removes only
  the periapsis term (1.5·2⁻¹²), the k term dominates both.
- **P4 (hit price):** the memo hit path (class lookup + from_shape glue) ≤ 40% of a
  full compile; the deletion prize per hit ≈ compile − hit.
- **P5 (census):** distinct shape classes ~1.2–1.5k (588d measured 1,161–1,491),
  class hit rate ~0.99; exact ShapeKey repeats ≈ 0 (the page's own finding, a
  reproduction anchor).
