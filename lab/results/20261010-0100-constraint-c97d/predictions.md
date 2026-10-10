# Predictions (written before the decisive runs)

Runs: `xtask universe --bench --unpaced --seconds S --members M` for M in {4, 48, 400} (fresh
seeds for held-out), and `xtask galaxy --bench --ships N` for N in {1e6, 1e8, 1e9}. These cases
were not tuned on; only M=48/N=default was measured before writing this.

1. Plane frame CPU grows with fleet members M at *least* linearly in the handed-out member count
   (fleet events per game-second ∝ M). I predict `view_gather` and fleet engine cost both scale
   ~linearly in M, so at M=400 the frame p99 exceeds 2 ms — i.e. the plane's cost per body per
   game-second, not the body count, is the wall.
2. Per-body event cost: fleet items cost ~16 µs each on this machine (measured at M=48). I predict
   it stays O(10 µs) at M=400 (cost per event is flat; count grows) — if it *grows* with M, the
   constraint is per-event work (e.g. a scan over siblings), not event count.
3. Held-out seeds (2, 3, 7): same orders of magnitude (within 2×) — event rates are set by the
   law, not the seed.
4. Galaxy density bench at 1e9 ships: frame stays under 5 ms if bodies are stored as tubes with
   no per-body per-frame work (the "compute only surprises" claim); if it blows the frame budget,
   the galaxy view itself is a constraint.
5. The one constraint I expect to name: per-body *event cost × event rate* (µs per body per game
   second) in the plane's engine+view path, because 10^9 bodies at the measured ~1.5 events/body/s
   × 16 µs ≈ 2.4×10^4 CPU-seconds per game-second ≈ 25,000 cores — 4 orders above the M1.
