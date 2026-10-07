# Predictions (written before the decisive runs)

Question: at 10⁹ bodies, which budget term breaks first — compute (events/s × cost), memory (H_live), or bandwidth — and by how many orders, using the shipped plane as the measured anchor?

Runs I have NOT done yet (the decisive experiment, all on this shared Linux box, orders of magnitude only):
- `xtask universe --describe` (scene size)
- `xtask universe --bench --rtf 100 --seconds 20 --seed 1` (paced, the player's loop)
- `xtask universe --kick-bench --rtf 100 --seconds 10 --seed 1`

My estimates before any measurement (derived from law.md's 16-byte tube, H0190's 32 kicks/orbit, r8's 1.1 encounters/body/orbit, the taste log's "recompiles an orbit on about 99% of kicks", and the board's M1 numbers 10¹⁰ ops/s, 60 GB/s, 8 GB):

1. **Scene size** (`--describe`): between 40 and 150 bodies at the default 48 members.
2. **Kick cost** (`kick_us` median, plane-made ships): between 2 and 30 µs (recompile-dominated if the 99% recompile share holds). Leavers (fleet members): between 0.3 and 10 µs.
3. **Event rate per body** (bench: total events / bodies / game-seconds, rtf 100): between 1e-4 and 3e-2 events per body per game-second.
4. **Bytes per body** reported by the plane today (no population programs): between 40 and 400 B (i.e. ≥ 2.5× the 16-byte logical tube; 16 B × 10⁹ = 16 GB already busts 8 GB).
5. **Term ranking at 10⁹** (extrapolating the plane's own per-body rates, scars never reabsorbed, ~8–16 B per scar): compute breaks first (cores needed at rtf 100 land within a factor of 30 of the board's "about 190 cores"), memory second (4 GB of scar bits fills in less than one game-year at belt-like kick rates), bandwidth last (needs ~100× more traffic than the event rate implies).
6. **The board's headline** "10⁹ orbiting bodies at today's rates would need about 190 cores" reproduces from my measured constants within 3×.

What would make me wrong: if measured kicks cost < 1 µs AND events/body/game-second < 1e-4, compute stops binding at the plane's orbit scale and the ranking flips to memory-first; if bytes_per_body > 1 kB, today's store is already > 1000× the information floor and the memory term tightens by that factor.

Kill criterion for the run: if the bench cannot report events and game-seconds consistently (events_per_second is per WALL second — I must divide by rtf × wall to get per game-second), or the scene is so small (< 30 bodies) that per-body rates are dominated by the player and fleet battle rather than orbiting bodies, the extrapolation is honest only to an order of magnitude and I say so.
