# Predictions (written before the decisive runs)

## The diagnosis these predictions are drawn against (already measured, probes only)

The dormant arm's digest depends on the wall budget with no load at all (seed 3, far, 1,500/rtf 100:
ms=100 → `46c7652f3985` = the shipped digest; ms=5 → `7f1641e8df40`; ms=0.5 → `5f4aede2ee30`;
shipped `46c7652f3985` at every budget). At every budget the fleet's own state at the cut is
identical (tick = cut 162420357, hand-offs 1403, members 97) and the shipped arm logs **0
encounters** in flight. The one-shot drain in `settle` runs before the settle's advance loop, so
every leaver the fleet hands out *during* the settle lands in `dormant` after the drain and is
never bound; how many that are is budget-dependent (in-flight starvation moves hand-outs into the
settle). That is my candidate root cause for both silver findings (the seed breaks and the load
nondeterminism), replacing the scan-candidate canon as the operative mechanism in these scenes.

## The changes under test

1. `settle` drains the dormant list **inside** its loop (before each `advance`, until neither
   produces anything): no leaver below the cut can stay unbound.
2. `ES_DORMANT_WAKE=doll` (new arm): the canon-exact wake rule — at the player's item, wake every
   same-doll leaver with hand-out tick < the item tick (exactly the shipped queue's rule), keep
   other-doll leavers dormant (the scan filter skips other-doll bodies, so their dormancy is
   canon-free by construction). `ES_DORMANT_WAKE=drift` (default): the original f64 drift gate,
   minus its "other doll → wake" clause (pure cost, no canon reader).

## Cases not tuned on (the decisive matrix; digests decide, floats never)

- **P1 (identity).** With the drain fixed, dormant (both wake rules) = shipped, bit for bit, at
  far 1,500/rtf 100 for seeds 1, 3, 7, 11 — the seed-3/7/11 breaks of the silver run were the
  drain bug, not the scan canon (the shipped arm logs 0 in-flight encounters in these scenes, so
  the scan-candidate channel never fires). If identity fails at a seed, that seed is a real
  scan-canon firing and I report which.
- **P2 (budget and load stability).** Dormant digest = shipped at engine-ms 0.5, 5, 100 (budget
  moves work between flight and settle, never the canonical state), and 4 concurrent identical
  dormant seed-3 runs print ONE digest (twice).
- **P3 (the sound rule's price).** With `doll`, the far-scene cure dies: the fleet and the player
  share home_doll, so force-wake binds every leaver in flight — overflow returns to the shipped
  class (~440/480), bodies at the cut ~1,390. The silver run's cost win was bought by skipping
  canon-forced binds in a same-doll scene.
- **P4 (the drift gate's measured miss rate).** With `drift`, the cure stands (overflow tens/480,
  bodies 28) and P1 still holds: the gate fired 0 wakes in every far cell and missed nothing
  measured; its soundness stays unproven (an f64 acceleration bound), and a provably sound
  radius-only bound (vis-viva annulus) wakes everything co-orbital — the annuli overlap — so in
  same-doll scenes the choice is: pay the binds (sound), or trust the drift bound (unsound).
- **P5 (near scene unchanged).** Both rules wake everything (positive control): identity, no win.
- **P6 (4,000/rtf 1).** Identity with both rules; the cure (overflow 286→0, delivered rtf 0→1)
  stands under `drift` and dies under `doll`.

Kill criteria: identity failing at any seed/rule after the drain fix (a real canon channel — name
it); load instability persisting after the drain fix (a second channel — dig); the far-scene cure
surviving `doll` (my same-doll analysis wrong — re-derive).
