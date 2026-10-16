# Predictions (written before the decisive grid)

Exploratory, disclosed: one 12-frame smoke at fleet 48 / level 8 / 12 ms (instrument check only,
`f0-f11`): the burn rides the player's kicks at ~5-15 items/frame, player-class 2-6 ms/frame,
heldscans 0 in those frames. Everything below is registered before the 150-frame grid.

The composition (check2's named experiment): the player holds a forward burn from tick 0
through the opening (mode 1: `input(0, word(1, level))`; a held key is one decision, the
engine's rule), at the page's own arms — fleet 48 and 400, N = 0, seed 1, rtf 100, 12 ms —
plus one arm where a single decision lands at the coast's crest tick (mode 2, schedule at
f62's target), the served 5-ms budget at 400, and level 4 as the low-throttle control.

1. **The cap holds (the kill criterion).** Worst presented lag ≤ 1.667 game-s (one frame's
   advance at rtf 100) in every arm, burn or coast, 12 ms or 5 ms. Mechanism: `frame_to`'s
   target follows the presented time (structural, confirmed by both checkers). If any arm
   shows lag > 1.667, the "rtf dip, not a freeze" claim fails under burn.
2. **The wave is the fleet's own.** Total leavers by f150 identical to the same-binary coast
   baseline: 43 at fleet 48, 357 at 400 (the crossings are the battle's canonical ticks; the
   player's burn at level 8 changes η by ~5×10⁻⁴ over the opening — no member's tube is
   touched). Opens = leavers in every arm. If the totals move, the wave is player-coupled and
   the attribution is incomplete.
3. **The hand-out price is untouched.** Fleet-class µs ÷ leavers on leaver frames stays in
   300-800 µs (the measured band) in every burn arm; the burn adds cost in the player class,
   never the fleet class. Outside the band ⇒ the composition changed the promotion price.
4. **The burn's own bill (the smoke's implication, registered as a band).** At level 8 the
   player's opening bill (player-class µs summed over f0-f100) is 100-400 ms — **larger than
   the 48-member hand-out bill (26-32 ms) by ~3-10×**, and the same order as the 400-member
   bill (240 ms). So under burn the opening's worst frames at served fleets become the
   *player's thrust cadence* (each flush pays the same `bind_surface` fit a hand-out pays),
   not the hand-out wave — the exodus claim needs that boundary. At level 4 the player bill
   is < 30 ms at fleet 48 (invisible: α drops 16×, the cadence falls below one kick a frame).
5. **The scan latch breathes, never drowns.** heldscans > 0 only inside the drain frames
   (the latch freezes below 2× the longest recent scan), peak < 100 at fleet 48/400 level 8,
   0 in quiet frames, and never ≥ 2048 (the backlog cap that would block the player's next
   item). Total encounters logged differ from coast (the player's tube differs) — reported,
   not predicted.
6. **The crest decision (mode 2).** One decision landing at the coast's crest tick f62
   resolves inside the drain as one flush (≤ 1 ms, one rebind + replan); the drain lengthens
   by ≤ 3 frames at 48 members; the lag stays ≤ 1.667; the leaver teeth unchanged in total.
7. **The served budget (5 ms, fleet 400, level 8).** Worst frame ≤ 6.5 ms (one item over the
   baseline's 5.2-6.2); frames ≥ 2.5 ms rise from the baseline's 82-87 toward ~110-120 of 120
   (the burn's cadence fills the quiet frames); no dropped frame, lag capped at 1.667 — a
   deeper, wider rtf dip, still a dip.

Kill criteria, restated: any of (1) lag > 1.667, (2) leaver totals ≠ baseline, (3) per-leaver
fleet price outside 300-800 µs, (5) heldscans ≥ 2048 or growing at f150 fires, and the claim
does not hold as stated; (4) and (6) report the boundary either way.
