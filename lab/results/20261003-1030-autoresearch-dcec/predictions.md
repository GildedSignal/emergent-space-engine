# Predictions (written before the loop)

Artifact: `crates/lattice` CPU chronon reference (`Chronon::step`), the bit-exact
reference every mode must reproduce. Metric: **ns per body-chronon**, median of 3 runs,
on the tuning config `n=100000 fill=0.1 q=1024 vmax=256 seed=1 steps=100`.
Behaviours held fixed: `outcome()` (world digest + log digest) bit-identical to the
baseline binary on every config below, and `cargo test -p emergent-lattice` green.

Measured before the loop (n=100k): detect ≈ 78% of the step; inside detect, the
`ranges` HashMap **build** is ~34 ms of a ~46 ms chronon (the 100k SipHash inserts and
the fresh ~2.5 MB allocation every chronon), key+sort ~5 ms, the actual neighbour pair
loop only 2–4 ms (~245k visited pairs), advance+walls ~0.8 ms, respond ~0.8 ms.

## Hypotheses to test, in order (one change per round)

- H1 kill the per-chronon hash structures: counting-sort cell table (linearized cell
  index, direct array indexing, reused scratch) replaces sort + `ranges` HashMap.
- H2 reuse all per-chronon scratch (order/pairs/walls/involved/local/batch), no fresh
  Vec/HashMap allocation inside `step`.
- H3 cheaper `consumed` lookups (small custom hasher; pure lookup structure, no bit
  change) if the profile still shows it.
- H4 cheaper advance/keying (fuse the kmax scan and the cell pass; avoid the second
  full pass over bodies).

## Held-out set (never tuned on; run once at the end)

seed 2718281828 n=100000 fill 0.1 q 1024 vmax 256 steps 100 (the ladder seed);
seed 7 n=40000 fill 0.4 (dense, 37× the events);
seed 11 n=200000 fill 0.02 vmax 16 (cold sparse, zero events);
seed 13 n=50000 fill 0.05 q 4096 vmax 1024 (hot, large quanta);
seed 17 n=1000 fill 0.3 q 64 vmax 8 (tiny; fixed-overhead regime).
Baselines in `baseline-heldout.txt`.

## Predictions on the held-out set

1. Digests: identical to baseline on all five (this is the constraint; any mismatch
   kills the round).
2. Speedups (ns/body-chronon, same order-of-magnitude reading): standard ≥ 2.5×;
   cold-sparse ≥ 3× (detection-dominated); dense ≥ 1.5× (respond fraction grows);
   hot ≥ 2×; tiny between 1.2× and 2× (fixed overheads dominate).
3. The gain ranking cold-sparse > standard > dense holds after all rounds.
4. The single idea carrying most of the gain: stop building hash structures per
   chronon — the cell layout is a counting sort over a linearized index, reused.
5. Structural ceiling this loop will not reach: the pair loop still touches every
   neighbour pair every chronon (~2.4 predicates per body). A sweep that carries cell
   occupancy across chronons (bodies move ≤ 1 cell per chronon by construction of
   `cell`) would remove the keying pass entirely; I predict that is worth another
   ~1.5–2× and is the next run's change, not this one's.

Stop rule: three consecutive rounds under 10% gain.
