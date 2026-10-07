# Predictions (written before the held-out run)

Held-out corpus: 160 randomized keys (LCG seed 0x5eed_1234_5678_9abc), periapsis
log-uniform in [4, 2^40] in M units, e a mixture of uniform [0, 0.995] and a
near-separatrix band [0.995, 0.9999]. Never used in tuning; no grid structure.

The patch under test: exact-capacity preallocation of the knot and crossing
vectors in `OrbitShape::bound` (`crates/space/src/orbit.rs`, +8 lines, no
arithmetic touched).

1. **Bit-identity holds on unseen keys.** The held-out digest of all 160
   compiled answers (knot ψ list, crossings, period/advance/proper period,
   crossing times, states at 9 phases, table read, reflection) is the SAME
   32-byte hash on pristine and patched. This is the constraint "behaviours
   fixed"; the whole point of testing it on unseen keys is that tuning never
   saw them.
2. **Cost moves ~1%, not more.** The preallocation removes ~3-6 heap calls per
   compile (log2 growth of a 96-byte-per-element vector); on a 3.2 µs circular
   compile that is up to ~10%, on a 57 µs e=0.95 compile ~1%. The held-out
   corpus is eccentricity-heavy by construction (30% near-separatrix), so I
   predict the geometric-mean ns/compile improves by 0.5-2% only, within or
   just above run-to-run noise.
3. **Per-knot cost is unchanged (~650 ns/knot across classes).** The patch does
   not touch per-panel arithmetic; knots per key follow the band law
   (bands ≈ 16·log2((1+e)/(1-e)) clamped by periapsis compactness), so mean
   knots per key on the held-out set should sit between the tuning set's
   weak-ecc (44) and strong-gen (85) means.
4. **If any of 1-3 fails**, the diagnosis path is: 1 failing means the reserve
   changed construction order somewhere (it must not - it is allocation only);
   2 outside [-1%, +3%] means the interleaved A/B was noise-dominated and the
   keep/revert decision must be re-run; 3 drifting means the corpus classes
   were mislabeled, not that the law changed.

Not predicted (measured, not tuned): the three-round loop already showed the
bit-identical floor of this compiler is near: cos() is 26-31% of ns/compile,
division plumbing most of the rest, and no bit-identical micro-change moved
the geomean by more than 1% (rounds: +0.6% reverted as noise, +1.0% kept,
-11% reverted as a regression).
