# Predictions (written before the decisive run)

Question: on the shipped plane, what is the rate of live-state growth per ship per game-second (distinctions created), what does the light-cone reabsorption (prune) saturate it at, and how many ships fit in 8 GB at that equilibrium?

Cases I have NOT tuned on (the plane as flown, seed 1, Sparse, 1 thread, 48 members; snapshots at 1–3–10–… game-seconds driven through `frame_to` at 60 Hz, the player's path):

1. **Growth is linear and kick-minted.** Each ship kick mints a fresh compiled trajectory whose exact key never recurs (memo.rs). I predict allocator-live bytes per ship grow linearly in game-time at (kicks/s/ship) × (bytes per retired segment incl. its shape knots), until the prune window bites.
2. **Saturation time ≈ the retention window.** Prune keeps `2·light_distance + 2^26` ticks ≈ (2·500 s + 330 s) ≈ 1300 game-seconds for a ship near 1 AU. Equilibrium bytes/ship = per-kick bytes × kicks in that window. I predict the plane reaches equilibrium between 500 and 2000 game-seconds.
3. **Equilibrium per ship: tens of KB** (shape knots dominate), i.e. 10–100× the 16-byte tube. Consequence I commit to: N_max in 8 GB lands at 10^5–10^6 ships, three to four orders below 10^9 — the exact-rebind history ledger, not the body count, caps N unless per-kick bytes or kicks/orbit fall.
4. **The law's own ledger undercounts.** `bytes_per_body` counts history as `Segment` structs but not the retired shapes their `Arc<Entry>` keep alive; I predict the allocator truth is ≥ 2× the ledger at saturation.
5. **Controls.** The star (no kicks): flat live bytes, zero new entries. The player and fleet members (Fermi frame, contacts) may deviate from orbiters; the tail (worst body) is what I report, not the mean.

Falsifiers: if live bytes saturate at ≤ 2× the base record, or growth is sublinear before the prune window, claims 1–3 are wrong and the memory question is NOT the kick ledger.
