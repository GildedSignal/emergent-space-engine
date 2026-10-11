# Predictions (written before the N-sweep)

Baseline already measured (tuning, not held out): `universe --bench --rtf 100 --seconds 30`,
members 48 → 76 bodies at end, 1 thread, this Linux box:
frame p50 4.22 ms / p99 10.77 ms; **view_gather 69.5% of the frame** (p50 3.46 ms), engine 17.4%
(p50 0.24 ms, budget 5 ms), view_json 9.2%, wire 3.8%; rtf median 100.0, lowest 1% 9.9,
53 overflow frames; events/s 240; ship 280 µs/item, player 1330 µs/item, fleet 62 µs/item.

Held-out cases: the same bench with `--members 480` and `--members 4800` (never run before).
Reading of the code (view.rs `gather_with`, encounter.rs `PlayerNeighbourhood`):
- the gather does ~1 cached Newton crossing per body per frame, each a tube readout up the doll
  chain → **O(N) per frame, unbudgeted** (plane.md foundation 7 forbids exactly this);
- the player's item runs an exact O(N) neighbourhood scan → player µs/item grows with N;
- ship items read only the planets/moons lanes → ship µs/item ~flat.

## Predictions

1. **Gather dominates and grows linearly.** Gather p50 rises with bodies at roughly
   30–50 µs per body per frame. At ~500 bodies: gather p50 ≥ 12 ms, frame p50 > 13 ms,
   first hitches above 16.7 ms appear. At ~4800 bodies: gather p50 in the 100+ ms range,
   frame time dominated by it outright.
2. **Player per-item cost grows ~linearly with N** (the O(N) scan): at ~500 bodies the
   player's µs/item is 5–10× the 76-body value (≥ 5 ms/item); at ~4800 bodies it alone
   exceeds the engine's whole 5 ms frame budget, so player items overflow every frame and
   the rtf's lowest 1% collapses (below 1).
3. **Ship µs/item stays within 2× of 280 µs** across the sweep (no O(N) term in a ship item).
4. **The engine budget (5 ms) protects the frame from the engine** (overflow defers work):
   frame p99 tracks the gather, not the engine backlog; but overflow frames and rtf lowest 1%
   worsen with N as events/s grows past what 5 ms/frame can buy.
5. **The constraint does not move back to the engine at these N** on the frame side; it stays
   the view gather until the player's O(N) item makes the engine itself starve (prediction 2),
   i.e. the *next* constraint after the gather is the player's neighbourhood scan, then the
   events/s wall.

## What would make this wrong

- Gather p50 flat or sublinear in N (the cache makes it incremental) → the frame constraint
  is not the gather; my reading of `gather_with` is wrong.
- Player µs/item flat in N → the neighbourhood scan is not O(N) in bodies as I read it.
- Hitches appearing while gather share < 50% → the constraint is elsewhere (json/wire/engine).

## Kill criterion for the claim

If at ~500 bodies the gather is under half the frame and frame p50 < 10 ms, the claim
"the view gather is the frame's constraint at scale" is dead, and the run reports that.
