# Predictions (written before the decisive arms)

Scene: shipped plane bench (`xtask universe --bench --unpaced --no-record --seed 1 --threads 1 --engine-ms 5` default),
probe = print-only counters (`scans_in/out`, `held_scans`) + counting allocator, per 4b8c/7bd9 precedent.
Load = 6 CPU spinners pinned to cpus 0–5; the bench pinned to cpus 0,1. Quiet = no spinners (ambient load ≈ 0.6).

Model (the queueing reading of universe.rs: `encounters_for_player` arrivals, `drain_scans` service gated by
`room ≥ 2·max(scan_ns, 750 µs)` of the frame's wall budget, `SCAN_BACKLOG=2048` count-latch):

1. **λ is member-independent** (one scan per player item; the player's own cadence sets it):
   λ(m=100) ≈ λ(200) ≈ λ(400) ≈ 0.05–0.10 scans/game-s. If λ ∝ members, arrivals are fleet-driven and my reading of the arrival site is wrong.
2. **Load collapses service**: under load6, `scans_out` stops tracking `scans_in` (µ ≈ 0), `held` grows linearly in
   presented game-s at ≈ λ, and live bytes grow at λ·pin(m). Quiet, held stays 0 (470f/4b8c reproduced).
3. **pin(m)**: quiet-arm-subtracted slope pin = Δlive/Δheld. 4b8c: 84–100 kB at m100, ~112 at m200 ("not ∝ N");
   7bd9: ~171 kB at m400, ~2 MB at m1600 ("∝ N"). I predict pin(400)/pin(100) ≈ 2–4 (candidates grow with the window
   population, capped by the radial filter): between the two claims, closer to 7bd9.
4. **Law innocence**: digest(quiet, rtf100 s30 m400) = digest(load6, same cut), bit for bit.
5. **The latch (instrument arm `RUIN_BACKLOG=256`, one disclosed constant)**: once held reaches the cap (~2,700 gs at
   λ≈0.096), held pins at ≤ 256+ε, live bytes plateau at fill+256·pin(400), `scans_out` resumes at ≈ λ (answers paid
   inside the frame budget), and the presented-time rate drops (the game pays in rtf, not memory). If memory keeps
   growing past the cap, the latch is not an attractor and 7bd9's "not a safe fence" is stronger than I think.
   Shipped-cap arithmetic: 2048·pin(400) ≈ 0.2–0.4 GB plateau.
6. **Budget dose under load (`--engine-ms 12`)**: per-game-s growth UNCHANGED (the item loop eats any budget; the
   drain's 1.5 ms margin never appears), presented gs faster ⇒ memory grows faster per wall-s. If growth slows,
   the budget knob (4b8c's reading) generalizes to the loaded path.
7. **Pace dose quiet (`--rtf 600`)**: growth even quiet — 6× target work per frame squeezes out the drain's room
   (the player's own pace is a ρ knob). If flat, room survives target growth and only machine load flips ρ.

Held-out for the checker: seed 2 on arm A2 (growth slope within ±20% of seed 1), and the plateau memory in L1
(256·pin within ±25%).
