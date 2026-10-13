# Dossier — 20261013-2130-second-20261013-2005-spacex-3989-bc2b

## Claim

The dormancy lever is **canon-exact and deterministic once the settle drains its dormant list
inside its loop**: the silver run's seed breaks and its load nondeterminism were **one bug** — a
one-shot drain losing every leaver the fleet hands out *during* the settle (a wall-budget-dependent
count) — not the scan-candidate canon; with the fix, dormant digests equal the shipped arm bit for
bit at seeds 1/3/7/11 near and far, at every engine budget and under four-way concurrent load, with
the cure intact (far 1,500/rtf 100: bodies 1,384–1,403 → 28, overflow 427–447 → 48–61, p50 ~20 →
~5 ms, rtf 0 → 100; 4,000/rtf 1: overflow 261 → 0, delivered rtf 0 → 1); the canon-exact wake rule
(force-wake same-doll at the player's item, `ES_DORMANT_WAKE=doll`) is identity-by-construction and
measured, but wakes every member of a same-doll scene and the flying-pace cure dies there (overflow
393/480, rtf 0) — the win the drift gate keeps is bought with an unproven f64 bound that missed
nothing measured (0 wakes, 0 missed encounters at every far cell).

## Bottleneck

Board #1, bodies in the flyable engine (28 against 10⁹). The silver run (20261013-2005-spacex-3989)
built the dormant store and priced the cure but was gated on three named walls: the gate's
soundness, the "integrator-level canon decision", and the arm's own load nondeterminism. This run
removes the third (a 9-line fix, root cause measured), answers the first two with a canon-exact
rule whose price is measured, and re-runs the silver record: identity where it broke, stability
where it diverged, the cure where it was claimed.

## Evidence

All numbers: `universe --bench`, 8 s (4 s at 8,000), threads 1, paced 60 Hz, the patch in
`work/patch.diff` (the silver patch + the settle fix + the `doll` wake rule + the fleet-at-cut
field + the silver run's deleted `stats.slices/kicks/refused` accumulation restored, disclosed
below). Regenerate: `sh lab/results/20261013-2130-second-20261013-2005-spacex-3989-bc2b/regen.sh`
(~7 min measured, private target dir).

**The root cause, measured before any fix** (seed 3, far, 1,500/rtf 100): the dormant digest moves
with the wall budget with no load at all — engine-ms 100 → `46c7652f3985` (the shipped digest),
ms 5 → `7f1641e8df40`, ms 0.5 → `5f4aede2ee30`; shipped `46c7652f3985` at every budget — while the
fleet's own state at the cut is **identical at every budget** (tick = cut 162420357, hand-offs
1403, members 97). So the battle is budget-independent; what moved was the bodies. The settle's
drain ran once, *before* its advance loop; the settle's own advances run the fleets to the cut,
which hand out more members into `dormant` after the drain — never woken, never bound (6 lost at
ms 5, 13 at ms 0.5, 0 at ms 100). How many the flight's budget starved into the settle is
wall-dependent: the load nondeterminism (same cut tick, held 1398 vs 1397, 0 wakes) and the
seed-3/7/11 breaks were all this one bug. The checker's cap-interleaving inference was close (the
budget feeds it) but the channel is the drain, not the cap.

**After the fix** (drain inside the settle loop, until neither half produces anything):

| cell | arm | digest | bodies | held/woken | ovf | p50 ms | rtf |
|---|---|---|---|---|---|---|---|
| far s1 1500 rtf100 | shipped / dormant | `351e5b8ec9e4` **=** | 1,386 / 28 | 1,425/0 | 447 / 50 | 21.7 / 4.6 | 0 / 100 |
| far s3 1500 rtf100 | shipped / dormant | `46c7652f3985` **=** | 1,384 / 28 | 1,397/0 | 434 / 48 | 20.5 / 5.1 | 0 / 100 |
| far s7 1500 rtf100 | shipped / dormant | `d5f75e970e4a` **=** | 1,403 / 28 | 1,440/0 | 434 / 50 | 20.5 / 4.8 | 0 / 100 |
| far s11 1500 rtf100 | shipped / dormant | `2b524171f776` **=** | 1,388 / 28 | 1,405/0 | 427 / 61 | 19.9 / 5.0 | 0 / 100 |
| far s3 1500, doll rule | dormant-doll | `46c7652f3985` **=** | 1,395 | 1,367/1,367 | 393 | 20.1 | **0** |
| far s7 1500, doll rule | dormant-doll | `d5f75e970e4a` **=** | 1,412 | 1,386/1,384 | 391 | 20.5 | **0** |
| near 48 | shipped / dormant | `a2ae2910b624` **=** | 71 / 71 | 43/43 | 54 / 40 | 5.0 / 5.0 | 100 |
| near 1500 | shipped / dormant | `0b9db5950190` **=** | 1,386 / 1,396 | 1,371/1,368 | 447 / 423 | 21.7 / 21.4 | 0 |
| far 4000 rtf1 | shipped / dormant / doll | `e81b138959ad` **= =** | 2,191 / 28 / 28 | 2,163/0 | 261 / **0** / **0** | 35.8 / 9.5 / 9.9 | 0 / **1** / **1** |
| far 8000 rtf100 4 s | shipped / dormant | `304df5e33ec4` **=** | 3,518 / 28 | 7,785/0 | 240 / 78 (of 240) | 37.5 / 4.5 | 0 / 100 |

Identity holds at the checker's held-out seeds 7 and 11 with **0 wakes** (52,704–54,204 gate
checks, all negative) and 0 in-flight encounters in *both* arms — in these scenes no leaver ever
entered the player's scan reach in flight, so the scan-candidate canon the silver run escalated
never fired: its "canon-free in 4 of 5 cells" was the drain bug's footprint, not the canon's
boundary. Budget sweep after the fix: one digest (`46c7652f3985`) at engine-ms 0.5/5/100 with
held 1,387/1,398/1,403 (the flight/settle split moves; the canonical state does not), bodies 28
always. Load probe (the checker's, twice): eight of eight concurrent dormant seed-3 runs print
`46c7652f3985` — the shipped digest, held 1397 and cut identical in every one; the shipped
control ×4 stable. The nondeterminism is dead.


Column sensitivity (so no number here is unregenerable): the digests, `held`, `woken`, gate
`checks`, `enc`, the cut tick and the dormant arms' body counts are load-independent and reproduce
exactly across `matrix.log`, `load.log` and `regen.log`; the overflow, p50/worst, settle and the
*shipped* arm's pre-settle `bodies` (how much binding the flight's budget did: 1,384–1,389 at s1)
swing on the shared box — `regen.sh` (~7 min) regenerates the whole record with the same
load-independent values and the same classes.

**The canon-exact rule's price.** `doll` (force-wake same-doll at the player's item — exactly the
shipped queue's rule; other-doll members stay dormant for good, the scan's candidate filter is
`other.doll != me.doll`, so their dormancy is canon-free by construction) gives identity by
construction, measured at s3/s7 — and kills the flying-pace cure in this scene: the fleet and the
player share home_doll, so 1,367/1,368 members wake, overflow 393/480 (shipped class), rtf 0. At
4,000/rtf 1 the doll arm keeps the cure (overflow 0, rtf 1) because the player's in-flight items
there never met a non-empty dormant list (0 gate checks — the flight starved the player's items
past the leak). A provably sound *radius-only* bound (vis-viva annulus: wake unless the leaver's
[periapsis, apoapsis] and the player's radius are disjoint beyond reach + max-speed × interval)
also wakes everything co-orbital — the annuli overlap — so **in a same-doll scene every sound
rule without phase information pays the binds**; the phase (the leaver's conic at the scan tick,
i.e. a Kepler evaluation) is what the drift bound fakes with an f64 acceleration pad. The drift
gate's measured record here: 0 wakes at every far cell, 0 missed encounters, identity at all four
seeds; its soundness remains unproven and is the one open edge left.

**The near-regime storm, discussed** (the silver table's undiscussed column): near 1,500 dormant
worst frame 253.7 ms (shipped 23.9), near 48 worst 76.3 vs 12.0 — the wake-at-first-player-item
binds ~1,370 members in one frame. The doll rule shows the same storm (224–228 ms): it is
intrinsic to waking at the player's item in the near regime, not to the drift gate (PRINCIPLES 12:
the deferral moves the spike to the wake, it does not delete it there).

Diagnostic footnote: `stats.encounters` is schedule-dependent at fixed digest on the *shipped* arm
too (near 48: 40/40/41 over three runs, digest `a2ae2910b624` each time — scan reuse re-logging);
this dossier cites digests and body counts, never that counter.

## Predictions

`predictions.md` was written before the decisive matrix (P1–P6 with kill criteria). **All held**:
identity at seeds 1/3/7/11 (P1), one digest across budgets and under four-way load (P2), the doll
rule killing the flying-pace cure in the same-doll scene (P3: 393/480 vs the predicted ~440 class),
the drift gate keeping it with 0 misses (P4), the near scene unchanged (P5), and 4,000/rtf 1
identity with the cure under `drift` (P6; under `doll` the cure also held there, for the starving
reason above — richer than predicted, not contrary).

## What would make it wrong

The identity claim is measured, not proven: it holds where no in-flight scan sees a leaver within
reach (0 encounters in every far cell measured, both arms) and where everything wakes (near cells,
doll rule). A scene where a leaver closes to within `1024 × reach` of the player mid-flight under
the drift gate is where the gate's unproven bound decides — that scene has not been constructed
here (the near scene plants the player 20 km ahead, so the gate wakes everything at once). The
cost numbers are shared-box Linux timings: orders of magnitude, not M1 numbers. The doll rule's
"other-doll dormancy is canon-free" is by construction of `capture`'s doll filter; if the scan ever
gains cross-doll candidates, that half needs re-deriving.

## Cost of adopting, and fit

The adopted form: the settle-loop drain (9 lines — without it *no* dormant arm can be trusted, and
it is the reason the silver run's identity cells could not stand as certificates), plus the choice
of wake rule: `doll` where canon-exactness must be provable (cost: the binds, in same-doll
scenes), `drift` where the fleet's doll differs from the reader's or the win matters more than the
unproven bound (cost: proving the bound, or accepting it as a guard). PRINCIPLES: "Exact means
deterministic and reproducible" (2) — restored, measured under load; "Compute only surprises" (3)
and "Store the generator, not the generated" (6) — the `Leaver` words are the generator, and the
settle now genuinely replays them all; "A failed experiment kills that configuration, never the
method" (9) — the silver run's gate-bound kill is confirmed, its determinism kill is refuted as a
drain bug. The 10⁹ arithmetic is unchanged from the silver run (the hand-out stream leaves the
flying budget wherever dormancy holds), with the honest boundary now drawn: it holds for readers
in other dolls by construction, and for same-doll readers only as far as the wake rule is willing
to defer.

## The lens

Second author: the checker named one experiment and I ran it, but its first half (the sound bound)
split into a measured impossibility (radius-only soundness wakes everything co-orbital) and a
construction (the doll rule) whose price had to be paid in the open — the useful move was fixing
the determinism first, since every identity claim was untrustworthy until then. The lens's blind
spot: I nearly cited `stats.encounters` as an arm difference (40 vs 41) before checking it varies
within the shipped arm alone; digests decide. Operational finding worth one line in the lab's
memory: the shared default target dir (`lab-target-3`) is a race between windows — a concurrent
window's build replaced my binary mid-matrix (cells printing stats without the probe's fields);
this run's regen uses a private dir, and future regens should too.
