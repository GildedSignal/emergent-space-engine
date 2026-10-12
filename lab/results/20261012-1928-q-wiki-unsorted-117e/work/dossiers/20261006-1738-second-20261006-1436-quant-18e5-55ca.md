# Dossier — 20261006-1738-second (second author on 20261006-1436-quant-18e5)

**Claim.** The checker's named experiment is done and it upgrades the original claim from a location
to a name: the frame-budget-passing item is **the player item, and inside it the hand-out drain** —
`resolve_body`'s loop `while handouts.front().tick < key.0 { resolve_handout() }` (universe.rs,
`resolve_body`, the player branch) — which runs unbudgeted because the player's deadline is its own
tick (light distance 0), so it jumps the queue over hand-outs with earlier ticks but later
light-deadlines, and the completeness rule (the player must read a finished doll) then makes its one
item drain every pending hand-out: 19–64 members × ~1.4–1.5 ms per bind = 26–58 ms in a single item
under a 5 ms budget, on 3 of 6 seeds at the tail config (worst frames 33.7–51.3 ms); on the other
seeds the max item is still the player's (6.9–12.3 ms, ship-lane-pull-dominated) — over budget on
6 of 6 seeds. The author's side-claim "paced costs 2.7–5× unpaced" is **refuted** as a contention
artifact: on a quiet box it is 1.12× (p50 1.634 vs 1.456 ms).

**Bottleneck.** Board bottleneck 4 (smoothness/allocator). The named item converts "allocator
ordering cannot fix the tail" into an actionable defect with three one-line fix directions (below),
and kills the reading that battle contact itself (fleet slices, ≤ 4.8 ms) or kick work is where the
played tail lives. Expected gain: the worst frame drops from 34–51 ms to ≲ 12 ms (the drain
re-spread over budgeted items), i.e. the 33–51 ms hitch class disappears at this scale.

**Evidence** (all `--release`, Linux x86 shared runner, load recorded per run; scripts
`sweep.sh`, `loaded.sh`, `digest-control.sh`, `digest-control2.sh` in this folder; JSONs+CSVs in
`data/`; the instrumentation is this run's patch: max-per-kind in `Stats`, player-item phase split,
drain member count — off in no code path, reads nothing):

| run (m480/l15/5 ms, 30 s) | worst cpu | player item max | its drain | members | other items max |
|---|---|---|---|---|---|
| q1 seed 1 quiet | 37.2 | 30.6 ms | 28.1 ms | 19 | fleet 1.0, ship 1.5, handout 3.2 |
| q2 seed 2 quiet | 24.9 | 10.3 ms | 2.6 ms | 29 | fleet 4.8, ship 2.0 |
| q4 seed 4 quiet | 33.7 | 28.3 ms | 26.5 ms | 19 | fleet 1.1, ship 2.3 |
| q5 seed 5 quiet | 18.7 | 6.9 ms | 0 ms | 0 | fleet 0.9, ship 2.6 |
| q6 seed 6 quiet | 51.3 | 47.8 ms | 46.7 ms | 31 | fleet 1.0, ship 2.3 |
| L-quiet-s1 / L-loaded-s1 | 40.1 / 56.9 | 32.0 / 66.3 | 28.3 / 57.8 | 64 / 64 | — |
| L-quiet-s4 / L-loaded-s4 | 50.3 / 55.7 | 42.0 / 44.0 | 38.7 / 40.6 | 55 / 55 | — |
| e2b (20 ms budget) | 50.0 | 28.0 | 25.0 | 64 | hitches >16.7 ms: 92 vs 6 at 5 ms |

1. **The name.** The three giant seeds (1, 4, 6) put 92–98% of their max item inside the drain; the
   max item *is* the drain item (item total ≥ drain, within 1.2–2.6 ms). Per member ~1.4–1.5 ms
   (28.06/19, 26.50/19, 46.69/31) — many binds, not one slow bind (P3 held). Other phases of the
   player item are small: encounters ≤ 3.8 ms, fleets catch-up ≤ 0.9 ms, step+apply ≤ 1.8 ms;
   ship-lane pull is 5.5–9.7 ms and is what dominates the *non-giant* player items.
2. **The mechanism, from the code** (verified, not asserted): `advance` pops strictly by deadline;
   `deadline_of` = key tick + `light_distance`, and the player's `light_distance` is 0 while a
   hand-out's is its battle's root position. So every hand-out pending in the player's drain had a
   deadline *later* than the player's (else it would have been resolved as its own budgeted item
   first), while its tick is *earlier*. The worst frames sit at the battle's opening contact
   (frames 126–155 in q1/q6), never within 3 frames of a burn — contact-shaped, as the author said.
3. **The batch size is wall-schedule-dependent, not canonical:** seed 1, same config, digest
   identical (`a73ef0f4…`, 4 runs) yet max drain 19 members (q1) vs 64 (L-quiet-1). The world is
   exact; which unbudgeted lump the wall eats varies per run. Smoothness cannot be certified from
   one run per seed.
4. **Load doubles the giant or barely moves it** (s1: ×2.07; s4: ×1.05; same member counts, same
   digests): the drain is CPU work (not descheduling), but its magnitude is not load-invariant —
   shared-LLC/frequency effects are real on the played machine. The author's "could be an x86
   artifact" worry was half right: the *mechanism* is code, the *magnitude* is machine.
5. **The dial grows the lump** (P7): 20 ms budget → 92 hitches >16.7 ms (vs 6), drain n=64 (vs 19):
   deferring more work into one item also grows the unbudgeted batch the player must later drain.
6. **Paced/unpaced (this box, quiet):** p50 1.634 vs 1.456 ms = **1.12×**; digests equal. The
   author's 2.7–5× was their shared window's contention (the checker's reading, confirmed here).
7. **View share holds:** gather 59.5–66.8% + json 9–11.5% + wire 3.6–4.4% of frame CPU in every
   paced run (engine 20–27%), including m4800 (gather 63.5%). Bodies cap at 428 at m480 and m4800
   alike (the author's bench caveat, still true).
8. **Digest controls.** (A) Clean tree at 70f27a9 vs instrumented: same digest `a73ef0f4…` (and
   the clean JSON lacks the new fields — truly the clean binary). (B) At the author's base 110c3e0,
   same command: `a0746ad1…` twice (two builds), **not** their `bc132cb0…` — config identical
   (seed/rtf/frames/budget/level/cut_tick/encounters 178/leavers 400), but kicks 9563 vs their
   10575, opens 442 vs 762: the world itself differs across lab machines at the same commit. Their
   record regenerates on their machine class (author + checker agreed bit for bit), not on this one.

**Predictions** (`predictions.md`, written after a 5 s instrumentation smoke run on seed 1 only,
before all 30 s runs; scoring is honest): P1 held on the giant seeds (drain ≥ 92% of the item),
**failed on non-giant seeds** (max player item is pull-dominated there, drain ~0); P2 half-held
(giants on 3 of 6 as predicted, but "every seed > 10 ms" failed: seed 5 max item 6.9 ms, still over
the 5 ms budget); P3 held (19/19/31 members, ~1.4–1.5 ms each); P4 held after correction — the
digest mismatch is the machine, not my patch (control A); P5 half-held (mechanism and member counts
identical under load, but the ×1.5 magnitude bound failed: s1 doubled); P6 held (1.12×); P7 held
(92 vs 6 hitches, and the dial *grows* the drain batch, which P7 did not predict).

**What would make it wrong.** The M1 re-measure (the integrator's): per-member bind ~1.5 ms and the
pull ~6–10 ms are x86 numbers, and load sensitivity (point 4) is this runner's; the *name* and the
queue-jump mechanism are code-level and machine-free. The tail could move again when main moves
(main 70f27a9 already changed the contact frames vs the author's 76/102/373 → my 126/155/341).

**Cost of adoption.** The instrumentation is measurement-only (digest-proven) and folds into
`Stats` as-is. Fix directions it names, all cheaper than any allocator work: (1) bound the drain —
make K hand-outs per player item and requeue the player (the hand-out comment already says "when it
is made changes no outcome", so this is outcome-invariant); (2) give pending hand-outs with tick <
the player's next tick the player's deadline, so they drain as budgeted standalone items *before*
the player pops; (3) the per-member bind at ~1.5 ms is itself ~15× the mean item (103 µs) and worth
one look (replan/bind path). The `Seen` 152 B trim stands as before.

**Fit with PRINCIPLES.** "the algorithm that allocates the work to prevent those heavy tails, it's
the most important one" — this names the tail's address; "we only care about changes" — the drain is
a completeness dependency paid as one lump, exactly the kind of work the allocator should spread;
"Measure before claiming" — six seeds, loaded and quiet, digests as controls.

**The lens (second author) may have made me miss:** whether the cross-machine digest split (point 8)
is a rustc/FMA difference or a real hardware float leak — it deserves its own run (it touches Truth:
"Canonical outcomes are exact and independent of … hardware"); and whether the pull-dominated
player items (6–10 ms) hide a second, milder unbudgeted path.

## Reproduce (from the repo root, each ≤ 60 s; scripts in this folder)

```
cargo build --release -p xtask && T=/home/glmlab/lab-target-3/release/xtask
$T universe --bench --seed 6 --rtf 100 --members 480 --level 15 --seconds 30   # giant: player 47.8, drain 46.7, n=31
$T universe --bench --seed 5 --rtf 100 --members 480 --level 15 --seconds 30   # no giant: player 6.9, drain 0
$T universe --bench --seed 1 --rtf 100 --members 480 --level 15 --seconds 30 --engine-ms 20  # 92 hitches, n=64
bash lab/results/20261006-1738-second-20261006-1436-quant-18e5-55ca/sweep.sh    # the full quiet sweep (seeds 1-6, e2b, a/g, c1)
bash lab/results/20261006-1738-second-20261006-1436-quant-18e5-55ca/loaded.sh   # loaded-vs-quiet pairs (6 spinners)
```
Read `engine_item_max` (new, this run's patch) and `engine_cost_by_kind[].max_item_ms` in the
printed JSON. Per-frame series: `PLANE_FRAME_DUMP=<path>` (the original run's patch, kept here).
