topic: service-tail
status: open
closed-by:
valid-while: crates/universe@<this run's tree> + this run's patch (examples/ktail.rs; no law change)
updated: 20261021-1551-quant-39fe

# The frame's service tail: what one item costs, not what items cost on average

## Current best

**NEW (39fe, quant — the whole-item service distribution measured on shipped code, every item timed alone at `Budget::events(1)`, frames drained unbudgeted; per-call fixed cost 6.7-7.0 µs rides every item, so absolute µs are upper bounds).** The frame tail is TWO diseases: **the comb's worst frames are arrival piles at mean service at 1e5** (rtf-1000 window, 203k ship items: worst 4,243 events / 258 ms served, correction served÷(events×mean) 0.90-0.98, seeds 1-2; checker) — **at the 3e5 comb the same frames read correction 1.22-1.28 on two draws (checker): still pile-dominated, but a real service excess grows with N** — so the stagger-class arrival levers own the 1e5 comb — **the steady trickle's worst frames are service-tail events** (1e5/3e5 coast 20 s: worst 42-70 events but 15.8-18.6 ms, correction 1.9-3.3× at the post-settle ramp; steady p99 frames are cheap piles, correction 0.24-0.33). The tail is a *boundary population*: >p99.9 items are 77-84% boundaries at the trickle rungs and the 1e5 comb (the p99-p99.9 band is 64.6% kicks there); at the 3e5 comb the shares shift (67% boundaries, 82% kicks in the band — checker): boundary-majority everywhere, the shares are rung-dependent. Ratios p99.9/mean by kind: ship 3.2-3.8 (trickle) and **10.5 at the comb, N-flat to 3e5** (p99.9 415 µs, max 918); fleet 32.6-45.5 (max 4.5 ms, 155× mean); player 3.4-3.7 (trickle) and 5.1 at the comb (p99 6.0-7.1 ms, max 10.96 ms — one player item alone is 50-92% of the 12-ms budget). The comb's ship mean 39.7 µs confirms the record's 45.3-45.9 µs/kick class. The steady trickle is the locals' stream (1,346 ship items at 1e5 AND 3e5, seed-stable — N-independent, matching 9d3a's zero-read census). **Priced consequence:** the shipped margin rule `item_ns[class]` (peak-with-decay `max(ns, m−m/64)`, universe.rs:1028) forgets a 1-in-10³ tail within ~200-450 class items, then prices the next tail item at the cheap mode — the measured ratios are its overrun multipliers; a per-class quantile (or slower decay) is the fix's shape, unflown.

## Refuted

- **"The kick item's mean is the number the frame budget faces" (the working assumption behind every mean-only cost row: 82.5 µs/item, 45.9 µs/kick, 58 µs/rebind):** refuted as a *budget* number — the item service distribution reaches 10.5× (p99.9/mean, ship, comb) and 33× (fleet), and the worst steady frames are carried by single items (player p99 6-7.1 ms), not by events × mean (39fe).
- **"The comb freeze is an expensive-item phenomenon":** refuted at the item level at 1e5 — correction 0.90-0.98 at the comb's worst frames (every item near mean service; the pile is the disease), consistent with the stagger's 30× kill and 0a46's clean-era 3× per-event reading now sharpened: the service variation lives *between* populations (kicks vs boundaries), not inside the comb's pile (39fe; at 3e5 the checker reads 1.22-1.28 — the pile dominates, a ~25% service excess is real and N-growing).

## Open directions

1. **What the >p99.9 boundary item is** (the tail's mechanism): rebind, doll handoff, or panel mint — kick-jet's stage attribution is the tool; one flight with stage timings on the >p99.9 population.
2. **The margin rule as a quantile** (one-line policy shape, unflown): price the next item by a per-class p99.9 (or slow the decay) and re-fly F1's letter — the measured multipliers are the test's expected overruns.
3. **The player item's 6-11 ms tail** at belt scale: ae40's O(all-bodies) scan reading (1.3-3.4 ms at members 48, no belt) updated to 6-7 ms p99 at 1e5-3e5 — whose channel (scan mint, WH, capture walk) owns it is unmeasured at these rungs.

## Contradictions

- None. The comb's correction ≈ 1 and the trickle's correction < 1 at p99 are different regimes, not a conflict (pile vs item), and 0a46's era alternation (12-17 vs 47-50 µs/event) is the population mix (kick vs boundary combs), consistent with the tail composition here.

## Runs
- 20261021-1551-quant-39fe (quant, this run): the whole-item service law measured — two diseases (arrival pile at the comb, service tail in the trickle); the tail is 79-84% boundaries; p99.9/mean 3.2-33.6 by kind; player item p99 6-7.1 ms; the shipped margin rule's decay forgets the tail it must price.
