# Predictions (written before the decisive runs)

Scene: `scenario::plane_extra` (the ladder belt), coast, seed 1, rtf 6000, flown past the
first kick wave (~14 k game-s ⇒ 2.3 s wall), cut at 8 s wall (≈48 k game-s). Census at the
cut over every body's current binding. Held-out cases: N=10⁴ and N=10⁵ (the author tuned
nothing; the compile path is the shipped `Orbit::compile`).

1. **Regenerability (the kill test for demotion).** Recompiling every Cycle binding's
   trajectory from the key its own trajectory carries is bit-identical (shape `==`) for
   100% of bodies at both N. Any mismatch kills demote-after-kick as designed (the
   compiled orbit would be state, not cache).
2. **Promotion price.** One `Orbit::compile(key)` costs p50 15–60 µs (below the measured
   59–76 µs/kick wave CPU, which also carries attendant events). If it costs >150 µs p50,
   promotion at 10⁹ (3.5×10⁴ kicks/game-s) exceeds ~5 cores and the promotion surface
   binds on CPU before memory.
3. **What stands.** Compiled knots are ≥50% of the build's bytes per body at the cut
   (predict 55–75%; the plateau is ~4.9 kB/body and the record's ~43 knots × 88 B ≈
   3.8 kB).
4. **The compact record.** The binding without its entry (unpacked, shipped widths) is
   80–160 B/body (the packed floor is known: 448–454 bits). Above 300 B the compact
   record itself needs the shelf before 10⁹ fits 6 GB.
5. **Composed live set under demote-after-kick.** With entries dropped after each kick
   and recompiled at the next event, standing live memory = seen + in-flight bodies
   (O(10²–10³) ⇒ <10 MB at this scene), not O(N); at 10⁹ the belt's kick rate
   (3.5×10⁻⁵/body/game-s) × the measured compile µs predicts 1–2 cores of promotion
   work, moving the 10⁹ memory wall from the live plateau (kill-N 8.8×10⁵) to the
   compact floor.
