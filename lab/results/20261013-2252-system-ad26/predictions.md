# Predictions (written before the decisive runs)

The question: is the plane's engine cost **one wall** — the tube rebind (`bind_surface`: fit →
compile → readout) — shared by every item class (ship kicks, fleet hand-outs, player decisions),
so that the record's named levers (the Carlson closed forms for the compile, the word-transition
fix, the (OrbitKey, edge) memo, ephemeral promotion) move the whole scoreboard at once?

Arms: `universe --bench`, rtf 1 (the battle resolved), 8 wall seconds, threads 1, prof feature
on, members 48 / 400 / 1500 / 4000, seed 1. Held out (not tuned on): seed 7 at 1,500 members;
members 12,000 at seed 3; rtf 100 at 400 members (flying pace).

## Pre-registered expectations

1. **One wall:** FIT + FIT2 ≥ 60% of the summed item walls
   (P_KICK + P_KICK_CLOCK + P_KICK_SUB + P_BOUNDARY + P_OPEN + P_CRASH + P_DECIDE + HANDOUT)
   at every member count. (Published per-caller shares, different scenes/eras: kick bind 84.6%,
   compile 49–97%; hand-out bind 355–421 of 486–585 µs.)
2. **The retry:** FIT2 / FIT ≤ 0.75, rising with members (the coarser re-fit rides 52–63% of
   hand-outs, and hand-outs grow with the battle).
3. **The promotion is a bind:** H_BIND ≥ 50% of HANDOUT wall.
4. **Event shape:** total events per member per game-second at 4,000 members, rtf 1, in
   0.03–0.15 (367f's battle pocket: 0.041 at 48 members, falling ~6× by 4,000).
5. **Held-out:** seed 7 at 1,500 reproduces every share within ±10 points; 12,000 members does
   not change the ordering (only the overflow mix); at rtf 100 and 400 members the hand-out
   stream collapses (~0 hand-outs in 8 game-seconds) while kick shares hold.
6. **Endgame arithmetic** (cited levers only, no new claims): with the compile replaced by the
   Carlson kernel (42–2378× per channel on the compile share), the word fix (−13–17.5% of bind)
   and the hand-out memo (−31% of hand-out) landed, the per-member battle cost falls by ~10×,
   putting the resolved-battle ceiling near 10^4 members on a ~4-core budget — the 10^6.4
   bodies gap reduces to belt wiring + the quiet-belt stream, not a new engine mechanism.

## Kill criterion

If FIT + FIT2 < 40% of the summed item walls at two or more member counts, the one-wall claim is
dead: the classes pay different mechanisms and the levers do not compose. If prediction 4 fails
by an order of magnitude either way, the endgame arithmetic does not transfer and the dossier
says so.

## What would make the run VOID

Digest instability across repeats (same seed, same cut, different digest), or the prof counters
counting zero (feature not wired through the build).
