# Predictions (written before the decisive run)

Anchors already measured in-repo (not tuned by me): 32.5 kicks/orbit unaveraged low orbit
(H0190 K1), 114× averaging cut (K2), kicks cost 29 µs in the plane (H0210), tube 16 B
(law.md), smooth belt program 0.126 bits/body (components-98bc), plane cadence 128
kicks/radial period (`Config::step_log2 = 7`).

Scene: root unit ≈ 1.5 km ⇒ 1 tick ≈ 5 µs; Home at 1 AU; fleet + low-orbit ships about
Home (T ≈ 5.4×10³ s); star-orbiting ships at AU scale (T ≈ 3×10⁷ s).

## Held-out cases (not tuned on)

1. **`xtask universe --kick-bench`** (this Linux box, orders of magnitude only):
   median kick cost 10–100 µs (M1 measured 29 µs).
2. **`xtask universe --bench --rtf 100 --seconds 10`** (default scene, ~50–150 bodies):
   - events_per_second: 0.5–20 per game-second total (dominated by low-orbit bodies at
     128 kicks / 5.4×10³ s ≈ 2.4×10⁻² events/s/body; AU ships contribute ~4×10⁻⁶/s/body).
   - bytes_per_body: 10–100 B (plain tubes + catalogue; shipmem not wired).
   - frame p99 CPU under 3 ms; no hitch (plane measured 2.45 ms on the M1).
3. **Events per body per game-second scales as 1/T_orbit of the body's host** — if the
   bench's per-kind µs/item or events/s shows AU-orbit ships costing anywhere near
   low-orbit ships per body, my capacity model is wrong by that factor.

## The capacity claims these runs test (the Fermi result)

4. **Re-derivation of the board's 190 cores:** 10⁹ × 32.5 kicks/orbit / 5.4×10³ s ×
   29 µs = **174 cores ≈ 190** ✓. The board number is the *unaveraged low-orbit corner
   at rtf 1*. Applying low-orbit cadence to belt-scale bodies overstates their cost by
   T_belt/T_low ≈ 2.4×10⁴.
5. **10⁹ cold bodies (T ≥ 1 yr) fit trivially:** memory ≈ program = 0.126 bits/body →
   ~16 MB; CPU at rtf 100 ≈ 10⁹ × 0.28/(3.15×10⁷ s) × 29 µs ≈ 2.6×10⁻⁵ s CPU per
   game-second → ~0.003 cores. Compute AND memory ~4+ orders below budget.
6. **Horizon bound:** a belt body's individual (non-program) drift within any playable
   horizon is negligible (≤ ~10⁻³ orbits per 100 h session; even T_Lyap = 10³ orbits
   gives ~3×10⁻³ e-foldings) ⇒ cold populations create ~0 distinctions/game-second;
   H_live is created by hot bodies (ships), battles and the player only.
7. **The binding constraint at 10⁹ is hot bodies × rtf, not memory:** N_hot ≈
   cores / (rtf × kicks/orbit / T_orbit × cost_per_kick). Today (128/orbit, 29 µs,
   4 cores, rtf 100): ~6×10⁴. With the planned averaging (×114): ~7×10⁶. With the
   slack skin too (×12.6): ~8×10⁷. Memory would allow ~2×10⁸ at 16 B/body — compute
   binds first today by ~3.5 orders, by ~2× after averaging+skin.
8. **H_live for the plane's scene** (what b-h-live should find): ~10¹–10² bits per
   game-second, all from the fleet, contacts and the player; the belt/star-orbit
   ships contribute ~0. A belt contributing non-negligibly falsifies claim 6.
