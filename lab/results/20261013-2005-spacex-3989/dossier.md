# Dossier — 20261013-2005-spacex-3989

## Claim

Holding a fleet's hand-outs **dormant** (the exact `Leaver` words, no body, no queue entity, no
scan candidate) until a reader wakes them is canon-free in 4 of 5 measured cells and cures the
plane's first N-wall outright — 1,500 members at rtf 100: overflow 447/480 → 27/480, engine p50
21.7 → 1.7 ms; 4,000 members at rtf 1 (fermi's "even rtf 1 collapses" rung): overflow 286 → 0,
delivered rtf 0.0 → 1.0 — but the cheap census gate I built is **not sound**: seed 3 breaks the
digest, exactly the pre-registered failure, so the gate's bound (not the dormancy) is what stands
between this and adoption.

## Bottleneck

Board #1: bodies in the flyable engine, 28 against 10⁹. The measured first wall
(20261013-1915-fermi-367f) is the leak × sticky promotion: every handed-out member becomes a live
body (~0.5 ms, ~8.3 kB standing, no demotion). This run deletes the promotion for members no
reader has touched — the "ephemeral, census-gated" half of that run's conclusion — and measures
where the wall moves to. Expected gain: the hand-out stream (~67% of battle-regime events at
4,000) leaves the flying budget; standing bodies per unread leaver 1 → 0 in flight.

## Evidence

All numbers: `universe --bench`, 8 s, threads 1, paced 60 Hz, the patch in `work/patch.diff`
(`ES_DORMANT` holds leavers dormant; `ES_PLAYER_ANGLE` moves the player to the fleet's opposite
point on the same circle, ~14,000 km co-orbital; the `--members` clamp lifted as in fermi-367f).
Regenerate: `sh lab/results/20261013-2005-spacex-3989/regen.sh` (~2 min). "Dormant" arms hold
leavers as `Leaver` records (4 words + tick + radius ≈ 80 B), wake them only at the player's item
through a drift-bound gate, and at `settle` (the digest's cut) wake the rest — the bind+replay
then runs through the shipped `resolve_handout` unchanged.

| cell (seed, rtf, members) | arm | digest (12 hex) | bodies pre-settle | overflow | p50 CPU ms | worst CPU ms | settle ms |
|---|---|---|---|---|---|---|---|
| near, 1, 100, 48 | shipped | a2ae2910b624 | 71 | 4/480 | 1.12 | – | 0.2 |
| near, 1, 100, 48 | dormant | a2ae2910b624 **=** | 71 | 2/480 | – | – | 0.2 |
| near, 1, 100, 1500 | shipped | 0b9db5950190 | 1386 | 449/480 | 21.7 | – | 5431 |
| near, 1, 100, 1500 | dormant | 0b9db5950190 **=** | 1392 | 432/480 | 23.96 | 251.4 | 5242 |
| far, 1, 100, 1500 | shipped | 351e5b8ec9e4 | 1386 | 447/480 | 21.66 | 25.5 | 5475 |
| far, 1, 100, 1500 | dormant | 351e5b8ec9e4 **=** | **28** | **27/480** | **1.69** | 16.8 | 7133 |
| far, 3, 100, 1500 | shipped | 46c7652f3985 | 1380 | 447/480 | 22.74 | 32.7 | 2879 |
| far, 3, 100, 1500 | dormant | **4ac2d175db7c ≠** | 28 | 22/480 | 1.83 | 20.5 | 4388 |
| far, 1, 1, 4000 | shipped | e81b138959ad | 2191 | 286/480 | 39.41 | 62.6 | 6 |
| far, 1, 1, 4000 | dormant | e81b138959ad **=** | **28** | **0/480** | **7.09** | 22.7 | 1427 |

Detail (far, 1, 100, 1500): 1,425 held, **0 woken in flight** (55,629 gate checks, all negative),
fleet items 4,773 → 1,166 (fleet ms 1,035 → 557), ship items 10,868 → 2 (1,427 ms → 0.2 ms: the
leavers' kick stream riding player items), settle 5,475 → 7,133 ms (the deferred binds + replays
land unpaced). At 4,000/rtf 1: 2,163 held, 0 woken, delivered rtf median **0.0 → 1.0**. Near
scene (player 20 km ahead): the gate wakes everything (1,364/1,368 at 1,500) and nothing improves
— as the scene's construction dictates; that cell is the gate's positive control, and the near
shipped 1,500 rung reproduces fermi's 449/480 collapse digit for digit (seed 1; fermi had seed 3).

## Predictions

Written before the decisive runs (`predictions.md`). Held: digest identity in the near cells and
(seed 1) the far cells; the far-scene hand-out stream left the flying budget (overflow 447→27,
≥ 2× predicted, 16× measured); the deferred work landed in the settle; the near scene bought
nothing. **Failed, as pre-registered: the seed-3 far cell broke the digest** — the kill criterion
("a missed encounter would show as a digest break"). My prediction that the gate would hold all
leavers *soundly* was wrong at seed 3: it held 1,398 with 0 wakes where the shipped arm's scan had
live candidates — the break is a reader-event difference (the shipped arm's player scans saw
leavers; the dormant arm's never did), not a replay difference, since seeds 1 and the 4,000 rung
are bit-identical through the same settle-wake path.

## What would make it wrong

The identity cells could be seed-lucky: the digest asymmetry is proven real at seed 3, and the
mechanism is structural — `PlayerNeighbourhood::capture` takes the bodies alive **at the scan's
moment** as candidates, so any representation that changes which bodies exist at a player item
changes the encounter log (canon) whenever a leaver is within encounter reach. Dormancy is
adoptable only with a gate that is *sound against the scan's reach over the scan's interval*
(mine is a f64 drift guess padded 4×; seed 3 shows the guess, not the dormancy, fails — the bound
must be derived from the doll's exact maximum speed and the scan's interval, or the wake must be
schedule-forced for same-doll members). The gate checks themselves are cheap (55,629 checks ≈
invisible next to the 33 ns/body scan they replace), but I did not isolate their per-check cost.
The far scene is co-orbital (constant ~14,000 km separation): it exercises "a fleet the player
never comes near", the realistic 10⁹ case, not a fly-by.

## Cost of adopting, and fit

The dormant store is ~60 lines env-gated (digest-identical when unset, verified in the near
cells); the real adoption cost is the sound wake rule (above) plus one design decision the
asymmetry forces: either the scan's candidate set becomes a *canonical* function of the cut
(bodies with `born < scan tick` — which dormancy violates by construction) or dormant members
must appear in the scan through their bound-at-wake replay. That decision is Julien/integrator
level (it touches the encounter canon, not the store). PRINCIPLES: "Compute only surprises" (3),
"the player is the only wildcard" (5), "Store the generator, not the generated" (6) — the Leaver
words are the generator; "a failed experiment kills that configuration, never the method" (9):
the gate's bound died, not the dormancy. The 10⁹ arithmetic: a far fleet's hand-out stream
(fermi: 0.107 hand-outs/member/game-s at 8,000 × ~0.5 ms) is deleted from the flying budget
entirely; what remains is the battle's own events and the origin's kicks.

## The lens

SpaceX: delete before optimize — I deleted the promotion itself rather than making the bind
cheaper, and the idiot index of an unread leaver (500 µs + 8.3 kB standing for zero reader
events) was the worst on the board. The lens's blind spot bit exactly where warned: I blew up a
cheap prototype (the f64 gate) and it broke at the first adversarial seed, which is the point of
blowing up cheap prototypes — but a merged gate would have been a one-way canon break.
