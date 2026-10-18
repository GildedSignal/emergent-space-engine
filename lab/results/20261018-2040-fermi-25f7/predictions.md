# Predictions (written before the decisive run)

Question: the ladder's frame certificate (p50/p99 0.99/10.6 ms at 1e5–3e5, zero over 12 ms)
is flown by `nladder.rs`, whose loop never gathers the view. The game as played
(`flight_sweep.rs`) gathers every frame, and the gather is Θ(n_bodies) by physics (every
tube crosses the observer's past light cone once; no cull). What is the flyable N with the
view in the loop, on shipped code?

Fermi estimate first (from measured constants, not run): warm gather ≈ 5.0 µs per seen body
(dcf1, ladder scene, second call), seen = N+61. Per frame at 60 fps the view alone costs
5 µs × (N+61). The 12 ms engine budget breaks when the frame total ≈ 12 ms, i.e. view ≈
11 ms ⇒ N ≈ 2,200. Above that, every frame is late and game time falls behind at rtf 100.
In cores: 5 µs/body × 60/s = 3×10⁻⁴ core·s per body per s ⇒ ~3,300 bodies per core; the
box gives this run <2 GB and ~8 vCPU shared, the M1 target 8 GB / ~8 cores ⇒ ~2.6×10⁴
bodies absolute ceiling with a per-body gather, ~5 orders under 10⁹.

## Pre-registered cases (not tuned on; the instrument is one flight per N, coast, seed 1)

Rung N ∈ {0, 500, 1000, 2000, 4000, 8000}, 10 s wall each, rtf 100, budget 12 ms,
gather_cached every frame after the first second (the game as played).

- **P1 (break point):** the frame's p99 with the view in the loop crosses 12 ms between
  N = 1,000 and N = 4,000; at N = 8,000 the frame is dominated by the view (> 80% of the
  frame is the gather).
- **P2 (per-body law):** the in-loop warm gather is linear in seen at 4–7 µs/body (dcf1's
  5.0 µs is the same call, so the same law should hold per frame with a warm cache).
- **P3 (the honest flyable N):** game time achieved (game_s) stays ≥ 90% of the viewless
  control through N = 2,000 and collapses (< 50%) by N = 8,000.
- **P4 (the viewless control):** the same flights without the gather hold p99 ≤ 12 ms at
  every rung (reproduces the ladder's N-flatness at this scale) — the break is the view's
  alone.

Kill criterion for my premise: if the in-loop gather is NOT linear in N (e.g. the cache
collapses and it is superlinear, or a cull I have not seen makes it sublinear), the Fermi
ledger below is wrong and the run reports that instead.

## The ledger this pins (composed from measured constants, this run's job to rank)

Per-frame N-growing terms on shipped code, break-N on one 12 ms frame:
1. the view gather, in-loop: ~2.4×10³ (this run measures it);
2. one capture volume's walk: ~5×10⁴ bodies (96f6: ~190 ns/body, formation scene);
3. build bytes: 2,340 B/body ⇒ 3.4×10⁶ on the 8 GB M1 (2 GB box cap ≈ 8.5×10⁵);
4. nothing else per frame grows with N (compiled orbits are write-only in flight, 0e37;
   the scan caps the player's candidates at ~300 locals, dcf1).

So the flyable engine's first break as the player actually sees it is the view, ~3 orders
below the build. Implication for 10⁹: a per-body per-frame gather is 5×10⁵ s of CPU per
game-second — the view must be aggregate (rows, 2df1) or culled before 10⁹ is flyable at
all, independent of memory.
