# Predictions — second author on 0a46 (checker's gold experiment)

Written before any decisive flight. Calibrations already done (disclosed): two 2e4 6 s
smokes proving the CSV prints and the stagger is inert before the first kicks (ladder
lines identical: kicks_per_body_gs 1.229e-4 both arms).

The checker's named experiment: (1) cc9d's per-item decomposition (items/cost by class)
across one freeze era and one clean era at 1e5, plus held-scan/memory per era — explain
the COST alternation, not just the freeze (the split survives at 5e4 without the
mega-frame); (2) one stagger arm spreading clock phase >= the ~4k-gs comb width.

Instrument (this run's patch, print-only + env-gated, off = shipped bits):
- `ES_FRAME_CSV=1`: per-frame `escsv` line adding to 0a46's columns the Stats deltas —
  `it=` items by class [planet, moon, ship, player, fleet], `cn=` wall-ms by class,
  `op/bo/sl/en` opens/boundaries/slices/encounters. Accounting fact (universe.rs:802,
  975, 980): the player's whole resolve_entity — nested `pull_ships` gulps included —
  lands in cn[3]/it[3]; the parallel ship waves in cn[2]/it[2]. So `kicks - it[2]` per
  era measures the ship kicks served NESTED inside player/fleet items vs by waves.
- `ES_STAGGER_GS=W`: each belt ship's FIRST clock interval stretched by a deterministic
  id-hash offset, uniform over W game-s (step.rs `birth_stagger_ticks`, wired into
  `plan_clock`'s first synchronisation, ships only — the player, planets, doll ships and
  every re-synchronisation untouched). W=0/unset: no stretching, shipped bits. This is a
  probe of the page's re-specified stagger target (clock-phase spread), not an adoption:
  it shifts each staggered body's first kick grid (first-interval midpoint only), so bits
  differ from shipped on stagger arms; disclosed.

Hypothesis under test (H-latch): the 3x cost alternation on identical arrivals is the
budget-admission latch (universe.rs:1010, `item_ns[class]` decayed max) interacting with
the comb. A crest served through the player's nested pull is expensive (sequential,
unbudgeted) and spikes `item_ns[player]`; the decay (1/64 per player item, ~260 frames
~= 1.7k gs) then throttles the player's item to the first-item rule for the NEXT era, so
that era's identical crest is served by budgeted parallel waves — cheap; by the era after,
the latch has decayed and the crest gulps again. On coast the same latch runs on the
player's scan cost instead of a kick gulp.

Arms (all seed 1, 12 ms, this Linux box; ~40-50 s each):
- A0 anchor: `nladder 100000 burn 10 2000 12 1`, CSV off.
- M1 `ES_FRAME_CSV=1 nladder 100000 burn 150 400 12 1` (mechanism, freeze+clean eras).
- M2 same, `coast` (the no-gulp alternation).
- S1 `ES_FRAME_CSV=1 ES_STAGGER_GS=4000 nladder 100000 burn 150 400 12 1` (comb-width spread).
- S2 same with `ES_STAGGER_GS=14000` (full-period spread).

## P1 — where the burn alternation lives (M1)

Freeze eras (1,3) vs clean eras (2,4): the era-wall difference is carried by the PLAYER
class: cn[3] per era alternates >= 5x, and cn[3] deltas explain >= 70% of (era1 - era2)
wall; the nested fraction (kicks - it[2])/kicks is >= 2x higher in freeze eras; ship-wave
µs/item (cn[2]/it[2]) stays within 2x across all eras.
Branch B (kills H-latch for burn): cn[2]/it[2] itself alternates >= 3x across eras 1 vs 2
— the ships' own wave service is 3x more expensive in freeze eras at identical arrivals.

## P2 — the coast alternation (M2)

Coast era walls alternate (5.5/1.7 s in 0a46) with no mega-frame; H-latch-coast predicts
the carrier is again cn[3] (the player's item/scan cost per era alternates >= 3x) with
it[3] roughly constant; ship-wave µs/item does NOT alternate >= 3x.
Branch B: cn[2]/it[2] alternates >= 3x on coast too — the alternation is a property of
the ships' service, present with no player item at all.

## P3 — the stagger deletes the comb (S1, S2)

S1 (4k = comb width): max 2k-bin ev/body <= 0.50 (M1/0a46: 0.717); crest concentration
(events in the 4 hottest bins / all events) drops >= 2x; per-14k-era walls equalize
(max/min <= 1.6x); worst frame <= 250 ms (>= 2.9x below M1's ~718).
S2 (14k = full period): max bin <= 0.35, walls flat.
Branch B (comb not the cost's cause): arrivals flatten but walls/concentration of COST
do not equalize — then the stagger target on the page is wrong about cost.

## P4 — the stagger's own price

S1/S2 total events and total wall over the same gs span stay within ±25% of M1 (the same
stream spread, no new work minted, none deleted). If events rise > 25%, the stretched
first intervals minted work; if walls fall > 25% below M1's CLEAN-era rate, phase spread
is not just redistribution but a real saving.

## P5 — instrument inertness

A0's max_ms lands in the record's shipanchor family (811-948); M1's per-2k-bin arrivals
match 0a46's record (0.400/0.717/0.415/0.702/0.373/0.737/0.393/0.695 for gs 12-28k) to
±0.01 ev/body, worst frames within ±10% of 712-718/42-44/339-346/12.
