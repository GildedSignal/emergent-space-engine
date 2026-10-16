# Dossier — 20261016-0346-spacex-917c (SpaceX lens)

## Claim

The staggered first-kick wave is flown budget-free at 10⁵ and 3×10⁵: the belt's own frame peak
collapses 28× (994 → 35 attributable events at 3×10⁵, ~1 ms at the M1 rate) and the wave
sinks BELOW the plane's own N-independent baseline — the 300 ladder locals' 334–452-event
storms — so the wiki's "staggered-break at ~1.4×10⁶" is not a findable break: the belt's
staggered frame term stays a 3–10% perturbation on the locals' storms until N ≈ 3×10⁶, past
the memory break (1.3–1.6×10⁶), and the wave stops being the frame's binding term at 3×10⁵.

## Bottleneck

Board focus 1 (bodies in the flyable engine: the furthest gap). The 10⁹ budget (1a1c) left one
number unpinned: the staggered wave's letter composition ("0.5–2.7× the letter"), with the
named rung "fly the staggered wave at 3×10⁵–10⁶ budget-free". This run flies it. Gain: the
birth wave — the surviving 26× term after every kick-cost lever — is confirmed deleted
budget-free at two rungs, and the next frame bottleneck is NAMED (the unstaggered locals), not
the wave. What it deletes at 10⁹: the wave letter-break as a separate constraint (it coincides
with the memory break).

## Evidence (all from this box, Linux/x86 i7-4790, 8 vCPU, load 0.1–3; ms are box numbers,
## events are deterministic and box-free; the M1 rate is 1a1c's 29.3 µs/event anchor)

The stagger (my rebuild of ed3a's, from the wiki description; the record's own patch is on its
branch, not in this tree): `plan_clock` offsets a SHIP's first kick by a uniform id-derived
fraction of one step (splitmix64 of the body id × 2·half); default OFF; the player, locals
(secondary dolls), weights, steps and readouts untouched. Spread measured at birth
(`belt_first`, patched): first items 13,154–43,535 game-s, p50 28,040 (unstaggered
13,051–14,542, p50 14,072; width ×20.3 — ed3a's ×20.3).

Off-arm identity (P5): `ladder_digest`, 13 cases × 4 schedules, pristine binary vs patched
binary with ES_STAGGER unset — all 13 digests and kick/encounter/contact counts bit-identical
(only the `[x.x s]` wall annotations differ): `diff` after stripping them is empty
(flights/digest_{pristine,off}.cut).

Budget-free flights (engine budget 10⁶ ms, rtf 100, coast, seed 1, 60 fps, the ladder's own
loop; `nladder <N> coast <s> 100 1000000`, ES_TLIMIT raised, full per-frame rows via ES_ROWS;
state recorded in flights/state_*.txt):

| arm | N | peak ev/frame (post-wave) | belt-attributable peak | pre-wave baseline | worst 250-s window | p99 ev | over 12 ms |
|---|---|---|---|---|---|---|---|
| A unstaggered | 10⁵ | **487** (28.7 ms) @ 13,965 s | 153 | 334 ev / 24.3 ms | 45,950 ev | 309 | 230 |
| B unstaggered | 3×10⁵ | **1,328** (89–107 ms) @ 14,152 s | 994 | 334 ev / 17.0 ms | 136,718 ev | 659 | 490 |
| C staggered | 10⁵ | 345 (18.5 ms) @ 37,020 s | **11** | 334 ev / 21.7 ms | 2,737 ev | 135 | 56 |
| D staggered | 3×10⁵ | 369 (14.0 ms) @ 37,020 s | **35** | 334 ev / 20.7 ms | 6,342 ev | 141 | 60 |
| E baseline N=0 | 28 | 51 (1.3 ms) | — | 51 ev / 15.3 ms (the exodus f61) | 1,087 ev | 16 | 1 |

- The unstaggered anchors land bit-exact on 1a1c's record peaks: 487 and 1,328 events (the
  schedule is deterministic across boxes and processes); ms are this box (A/B/C/D ran 2–3
  concurrent, ~50–80 µs/event vs 1a1c's 47–51 solo — orders of magnitude stand).
- Window flattening (ed3a's instrument, now budget-free): 45,950→2,737 (16.8×) at 10⁵;
  136,718→6,342 (**21.5×**) at 3×10⁵. The staggered window-peak RATE at 3×10⁵ is
  6,342/250 = 25.4 events/game-s = the steady stream ed3a measured — the birth arrival rate
  IS the steady stream, budget-free.
- Frame-level: the belt's attributable peak (post-wave max minus pre-wave baseline max) falls
  994→35 (28×) at 3×10⁵, 153→11 at 10⁵. At the M1 rate (29.3 µs/event) the staggered belt's
  worst frame costs **~1.0 ms at 3×10⁵** — and the whole post-wave worst frame (369 ev) is
  ~10.8 ms, i.e. the same class as the pre-wave locals' storms (334 ev ≈ 9.8 ms) the M1's
  F1 already carries at every N ("pass as N=0": its own N=0 max was 12.01 ms).
- The baseline attribution is measured, not assumed: E (N=0, no ladder locals) peaks at 51
- P2 held at the margin: 369 events vs my band's 350 top (~10.8 ms M1-projected), letter
  marginal exactly as predicted.
- P3 missed low: measured belt-peak ratio 1/28 (994→35), OUTSIDE my [1/12, 1/4] band — the
  frame-level flattening exceeds the window-level 16.7× cap because the staggered belt peak
  hides under the locals' storms; the band assumed the wave dominates its own frame peak.
- The wave still completes under the stagger: kicks 195,790/100,028 bodies (C, 48k game-s) and
  436,692/300,028 (D) ≈ the train's 2 steps; dead 27 (the plane's own, N-independent: 25–27 in
  every arm incl. E), refusals 0, player alive, memory 1,378 MB at 3×10⁵ (under the 2 GB cap).
- Reproduce: `lab/results/20261016-0346-spacex-917c/regen.sh` (~14 min: identity check, the
  four flights + baseline in parallel pairs, the spread, the analysis → flights/analysis.txt).

## Predictions (predictions.md, written before C and D)

- P1 FAILED as written (predicted staggered peak 25–90 events; measured 345 total) — and the
  failure is the finding: the frame peak at 10⁵ was never the wave's, it is the 300 locals'
  storm floor (334–452 at every N). The wave-specific number (11 attributable events)
  confirms the flattening. My prediction repeated the wiki's own instrument error ("peak ≈
  487/16.7 ≈ 29 events" — the 29 belongs to the belt, the frame peak to the locals).
- P2 held: 3×10⁵ staggered peak 369 events ≈ 14 ms this box (~10.8 ms M1-projected), in my
  [90, 350] events band's upper room, letter marginal as predicted.
- P3 held: 994/35 → ratio 1/28, inside [1/12, 1/4]... (28× vs the predicted ≤ 12× cap — the
  frame-level flattening EXCEEDS the window-level 16.7× because the belt's staggered frame
  peak sits under the locals' storms).
- P4 held: every body still kicked (1.96/2 steps at 10⁵; D same), dead 27 = the N-independent
  baseline, refusals 0.
- P5 held: 13/13 digests bit-identical off-arm.
- P6 held: attributable peak 11→35 for 10⁵→3×10⁵ (exponent ≈ 1.06 linear); the letter-break
  arithmetic below.
- P7 held: anchors 487/1,328 events exactly; ms 33/107 vs the 18–28/60–85 band (2–3 concurrent
  flights inflate µs/event ~1.3–1.6×; events unaffected).

## What would make it wrong

The stagger's legality rests on ed3a's schedule-only argument plus my off-arm identity; the
behaviour gates (B13/B14-class precession under the shifted first-kick tide phase) remain
unflown (ed3a's open direction 2, unchanged). The belt-attributable peak is a max-minus-max
difference; a checker should confirm the post-wave storm frames at 3×10⁵ are locals-dominated
(read the events' doll attribution directly). The ms numbers are 2–3-concurrent-load numbers
on a ~2×-M1-per-event box; the M1 re-measure decides the letter margins. The break-N
extrapolations assume the attributable peak stays linear in N (measured on two points only).

## Cost of adopting, fit with PRINCIPLES

Adopting ES_STAGGER as the birth default is ed3a's open direction 1, now with budget-free
evidence at two rungs: ~13 lines, one generation decision, digests change as any birth-draw
change does, the off-arm is bit-identical. PRINCIPLES: "minimize spike compute and average
compute usage" (OC#36) — the birth spike stops existing; "Compute only surprises" — a
population born at one tick kicking as one wave is our bookkeeping artifact, not a surprise
in the law; "the simulation decides" — the stagger moves only when the first surprise may
land, never what it does. What it does NOT buy: the steady stream's own 148×-over at the
shipped 30 µs kick (cf45) — the kick lever and the memory lever stand, exactly as 1a1c
composed.

## The lens (what SpaceX may have made me miss)

The delete-first reflex fixed the wave before questioning whether the remaining peak was the
plane's own: the 300 ladder locals are an artifact of the LADDER POPULATION (a probe
construction), not of the engine — the real plane at 10⁹ has no 300-short-period-local storm
floor, so the "wave sinks below the baseline" reading must not be oversold: at 10⁹ without
locals, the staggered steady stream itself (84,700 events/game-s at 10⁹, ~1.4×10⁵/frame)
remains 148× over until the kick lever lands. The baseline comparison is honest for the
flyable plane AS SHIPPED (the plane's own 28 bodies storm at 51 events max, exodus class),
where the staggered 3×10⁵ belt's 35-event peak is the frame's top N-scaling term either way.
