# Predictions — run 20261006-1436-components-ed09 (the event queue's floor)

Written after tuning ONLY on `belt` (w=1 tick, B=32768 buckets fixed by that tuning;
ratio there: heap ≈ 500 ns vs wheel ≈ 119 ns per pop+set at n=10⁶, order bit-identical,
negative control fails as expected). The decisive run below covers cases I did NOT tune on.

## Held-out cases and predictions

1. **churn** (2 lateral re-sets per pop, ±128 ticks, plus a cancel+re-add every 10th pop):
   the heap pays `up()` for earlier moves and `down()` for later ones; the wheel pays lazy
   stales and frontier-heap traffic. Predict: ORDER-MATCH, ratio ≥ 3× at n=10⁶.
2. **burst / formation** (one shared 4096-tick interval; ~n/4096 entries per bucket,
   the taleb-09b5 concentrated regime): predict ORDER-MATCH, ratio ≥ 2.5× at n=10⁶.
3. **tail** (every 20th pop re-sets a slot 16–64 intervals ahead → ~5% of live events
   beyond the wheel horizon): predict ORDER-MATCH, ratio ≥ 2× at n=10⁶. If the far
   fraction were pushed past ~30% (not tested here) the wheel could lose.
4. **Scaling** n = 10⁵ → 3×10⁶: heap ns/op grows (log₄ n sift depth plus cache depth;
   the heap array is 24 B/entry, so ~12 MB at 5×10⁵ crosses L2): predict ≥ 1.5× growth
   10⁵→3×10⁶. Wheel within ±25% flat. Idiot index at 3×10⁶ ≥ 5×.
5. **Controls:** wheel-nosort must FAIL the order check on belt and churn; wheel must
   match bit for bit everywhere else.

## Kill criterion for the wheel idea

If the wheel fails ORDER-MATCH anywhere, or the ratio on the held-out workloads falls
below 2× at n=10⁶, the bucket wheel is not adoption-grade for this queue: report the
failure, do not tune further in this run.
