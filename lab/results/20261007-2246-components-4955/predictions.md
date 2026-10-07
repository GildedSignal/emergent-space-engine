# Predictions (written before the decisive grid)

Tuned on: belt n=1e5 and n=1e6, seed 1, all four structures + floor; verification
passes at n ∈ {999, 30000, 4096} across 5 seeds. Everything below is held out:
n=1e7, formation/averaged/perturbed at 1e6, seeds 2 and 3, and all p99/max-sample tails.

Machine: shared Linux box, i7-4790 (Haswell, 8 MB LLC), loadavg ~0.2 at write time.
Orders of magnitude only (the integrator re-measures on the M1).

1. **belt n=1e7** (footprint ~160 MB, all cold): calendar_scalar 900–1700 ns/event,
   calendar_u64 600–1200, binaryheap 800–1500, wheel 180–400, floor 2–5 ns/event.
   Ratio calendar_u64 / wheel grows with n (log n + colder): 2.5–5× at 1e7
   (it was 2.1× at 1e6, 3.3× at 1e5).
2. **Scalar keys cost real money**: calendar_scalar / calendar_u64 ≥ 1.4× at every n
   (it was 1.45× at 1e6).
3. **formation n=1e6** (co-orbital fleet, 64-tick phase band, same-tick batches):
   calendars ≈ belt cost per event (their per-op cost is uniform); wheel amortized
   ≤ belt wheel (batch sort replaces many O(1) ops): 100–300 ns/event, but
   max_sample = the burst sort + the rebuild rebin: 10–200 ms (the honest spike;
   bounded in design by chunked rebin, which is pure scheduling).
4. **averaged n=1e6** (1 kick/orbit, huge lookahead): wheel 100–350 ns/event,
   one rebuild total; calendars ≈ their belt cost (heap depth is the same n).
5. **perturbed n=1e6** (a cancel + an earlier re-set every 64 pops): wheel rises
   vs belt (side heap, log-depth ops on 1/64 of events): 220–500 ns/event, still
   ≤ calendar_u64; wheel p99 rises but stays < calendar p99.
6. **Tails**: calendar_u64 p99 at 1e7: 700–1500 ns; wheel p99 ≤ 500 ns everywhere
   except formation (batch sorts push p999 to µs–ms). Wheel max_sample at 1e6–1e7
   is the rebuild: 50–400 ms. The heap's tail is flat by construction — that is the
   real smoothness tradeoff, and the frame-budget law (plane foundation 7) already
   forces chunking of any such spike.
7. **binaryheap control**: at 1e6/1e7 it loses to calendar_u64 (it beat it at 1e5
   where everything is cached); if it wins at 1e7 the harness is suspect.
8. **Seed spread** (quiet box): ≤ ±25% on means; verdicts (ratios) stable across seeds.

What would make the design wrong: if wheel p99 at 1e7 belt exceeded calendar p99
(structure ops going cold), or if averaged/formation showed rebuild thrash
(rebuilds ≫ pops/n), or if perturbed wheel cost exceeded calendar_u64 (side heap
degenerate — handoff-heavy real scenes would then need the changeover skin, not
this queue).
