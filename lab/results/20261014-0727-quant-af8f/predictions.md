# Predictions (written before the held-out runs)

Tuned on: `battle m4000 s3` only (one arm, warm on/off, digests c0ab0b4b7d0d9d10 both arms).
The arms below have NOT been run with `ES_IMP_WARM` at the time of this file.

## Held-out cases and what I expect

1. **battle m1500 s3, m4000 s7, m1500 s11, flying m400 s3 (rtf 100), handout m16000 s3** —
   digests identical with the warm arm off and on (the hint only ever returns a tick the exact
   predicate verified, or narrows a monotone bracket; counters touch no arithmetic).
2. **Warm hit rate** ≥ 80% of *hinted* searches on every arm (the kick moves the orbit little;
   m4000/s3 gave 921/1032 = 89%), and every miss within 2^8 ticks of the answer (m4000/s3: all
   ≤ 2^6).
3. **Untouched half:** exactly the first-binding searches (hand-outs: no predecessor binding)
   get no hint — `no hint` ≈ their count; at m16000 the hinted fraction of hand-out searches is
   near zero, so reads/search falls little there even though the dipping hand-out pays the search.
4. **Reads/search** ≤ 20 on every battle arm (m4000/s3: 18.2 vs 29.5 shipped) and the search's
   own time (IMP_NS) falls by the same fraction as its readouts (~−40% overall, ~−85% on hinted
   searches). Whole-arm wall: −0-20% (the bind dominates the rest; at flying pace, where the
   bisection is 57% of a 192 µs kick, I expect the largest relative drop of the kick-side wall).
5. **Model arm stays dead** on every arm (0 first-guess hits; it fires on ≤ 5% of searches and
   misses by ~half an orbit): the crossings are grazing dips of near-circular orbits, where a
   radius-model error divides by a near-zero radial speed.

## What would make the lever wrong

- Any digest moving off↔on (identity is the whole claim: the crash tick is canonical).
- Hit rate < 50% or misses beyond 2^12 ticks on hinted searches (the kick then moves the impact
  more than a bracket's worth, and the warm seed is not a seed but a coin flip).
- The search time not falling with the readouts (then the readout is not the cost inside the
  search, and the 4.6 µs/readout story is wrong at these arms).
