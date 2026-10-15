# Predictions (written before the bounded-cache runs)

Question: quant-1d52's adoption sentence says the retention cache must be **bounded** to
"the N-independent locals, O(10^2-10^3) entries". Nobody measured the hot set's cardinality
or its behaviour under the correlated reads of the first-kick wave. I build the bounded
cache (FIFO eviction at `ES_RETAIN_MAX=S`; FIFO is an UPPER bound on re-mints vs LRU) on
top of the flown seam+retention patch, and fly it.

Held-out cases (not tuned on): the first-kick wave at 10^5 (cut 48,000 game-s, seed 1 —
the arm whose anchors I reproduce first), seed 7 at 10^4, and N-scaling at fixed S.

## Predictions

- **P1 (the bet itself):** at S = 4,096 the re-mint bill stays small: promotions ≤ 1.10 ×
  demotions at BOTH 10^4 and 10^5. If the hot set were ~2×N (what global retention holds),
  S=4,096 at 10^5 would re-mint ≳ 95% of the 2.44M reads the unbounded cache hits.
- **P2 (tail shape):** the miss ratio at fixed S grows with N (hot set is only locally
  N-independent): promotions/demotions at S=4,096 is measurably higher at 10^5 than at 10^4
  (I predict ≥ 1.3× higher), but stays under the P1 ceiling at both — i.e. slow growth, not
  a cliff, across one decade of N.
- **P3 (the wave):** the first-kick wave does NOT storm the cache: no arm shows a promote
  p99/max blow-up versus the unbounded arm (max stays within 3× of the unbounded arm's
  155 µs), because wave reads coincide with the reader's own re-bind (compulsory mints the
  unbounded arm also pays).
- **P4 (memory):** retained_now ≤ S + small slack at every arm, and rss returns to the seam
  arm's level ±5% (the 2×N retained set was the memory cost; bounded deletes it).
- **P5 (identity control):** every bounded arm's digest is bit-identical to the unbounded
  retain arm on the same scene (cache policy only moves WHEN a pure re-compile happens).
  A digest change means my bounded build is wrong, not the rule — that arm is void.
- **P6 (the cliff):** S = 1,024 is below the hot set: promotions > 1.5 × demotions at 10^5.
  (This names the floor of the adoptable constant, not a failure of the rule.)

Kill criterion for the adoption sentence, pre-registered: if P1 fails at S=4,096 (or the
ratio at S=4,096 more than doubles from 10^4 to 10^5), "bounded to the locals" is wrong in
the tail and the integrator must not adopt a small bounded cache this step.
