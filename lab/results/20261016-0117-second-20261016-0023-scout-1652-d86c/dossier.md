# Dossier — 20261016-0117-second-20261016-0023-scout-1652-d86c (second author, scout lens)

## Claim

The checker's named experiment is flown: **dropping the history stack's `len() > 1` floor
(`PlainBodies::prune` + `droppable_until`, one predicate, behind `ES_DROP_FLOOR` in the same binary)
changes no engine outcome — digests bit-identical across the toggle at every cut, coast and burn,
deterministic frames, kicks identical — and cuts standing history 16× at coast steady state
(1.053 → 0.066 segs/body, everything left in-window) and 3.3× under sustained burn
(1.40 → 0.43, the residue the law's own `oldest` guard requires)**; the only cost is in the view:
per-emitter chain walks are refused (21,206 view misses per cold gather at 20k burn; warm gathers do
~1.7% of the baseline's retired reads, 175 vs 10,052 serves, view 49 vs 207 ms/gather), every
emitter's position moves ≤ 40 m (inside its own disc, no emitter vanishes), and — schedule-
conditionally — the player's own `partial` source read can hit a pruned era and drop the gather to
its documented fallback (`t_read = event_time`), translating the whole sky rigidly by the observer's
displacement (measured −6.94×10⁶ m ≈ 2.3×10⁻² ls in a wall-schedule run; zero emitters lost). The
deletion is adoptable **with the integrator's view call** (accept the fallback, or cap it — e.g.
never prune the player's doll's sources); without that call, the floor stays a view crutch, not a
law requirement.

## Bottleneck

Memory at 10⁹ (board focus 4): the causal history stack (398f: 1.0–1.3 TB at 10⁹; the scout 1652:
the floor pins 1.05 segs/body where 98.4% stands past every certified window). This run flies the
deletion the scout priced and closes the silver's named gap: digest identity across coast **and**
burn, per-call-site serve attribution (view vs engine), and a warm gather loop.

## Evidence (all from `regen.sh`: one build, six flights, each ≤ 60 s)

Scene: the scout's (`scenario::plane_extra`, seed 1, 48 members, N = 10⁴ → 10,028 bodies), rtf 1500,
cuts 15/20/32/48/60k game-s, `settle(cut)` then digest, census, cold+warm(12) gathers, full `seen`
dump; scripts coast and burn (two held reverses at L8, 18–26k and 38–44k, canonical ticks). Frame
budget **deterministic** for the record (`ES_DET`: no wall cap — same game-time per frame in both
builds); wall-budget pair kept as a demonstration.

- **D1 (digests).** Every cut, coast and burn: `digest()` **bit-identical** floor-on vs floor-off,
  and kicks/encounters/contacts identical (burn 60k: 113004 kicks both; `compare_coast.txt`,
  `compare_burn.txt`). Engine retired-read counters identical across the toggle at every cut
  (`census_reads.txt`: 4364/4364 serves 20k, 8854/8854 48k) with **zero engine misses in every
  flight** — the engine never reads an era the deletion removes; the checker's unreported
  between-gather engine serves (4,364–8,854 per interval at N = 10⁴) are now measured and shown
  law-indifferent.
- **D3 (the cut).** Coast steady state: 1.053 → **0.066 segs/body (16×)**, 32–60k, `IN_WINDOW 100%`
  (the residue is what the `oldest` guard keeps); just past the wave (15k) both hold ~1 (in-window
  transient, as predicted). Burn: floor-on itself grows to 1.40 at 60k; floor-off holds **0.43, 100%
  in-window** — under burn the law needs more than coast, and the deletion's standing store equals
  that need exactly. Dead bodies: floor-on pins 18–20 forever; floor-off releases all
  (`dead_with 20 → 0`).
- **D2 (degradation).** Deterministic pairs: **zero emitters vanish** (10048/10046 seen, same ids),
  max position shift 19–40 m, p99 ≤ 22 m, **zero shifts beyond any emitter's own disc** — the
  per-emitter cost is the refused chain walk (`credit`'s back-walk, `partial`'s one-back): cold-gather
  view misses 6 (floor-on) vs 21,206 (floor-off) at 20k burn, i.e. the reads the floor was serving.
  Warm loop: **175 vs 10,052 serves per gather (1.7%), view 49.2 vs 207.3 ms/gather** — the deletion
  makes the view *cheaper*: refused walks stop early. The one coarse mode: in wall-schedule runs the
  player's own `partial` read of its sources (`ext.rs:134` `binding_at` → `Refused("history
  pruned")`) drops the gather to the documented fallback (`t_read = event_time`, `view.rs`): the sky
  translates rigidly by the observer's displacement — measured mean (−6.94×10⁶, −4.6×10³) m over
  10,027 emitters with per-emitter spread ~60 m (a pure origin shift; `compare_wall.txt`), still no
  emitter lost. It is schedule-conditional (the five deterministic cuts did not trigger it) and
  bounded by one kick interval of the player's own motion.
- **Instrument hazard found (side result).** A **mid-flight** settled digest is wall-schedule-
  sensitive in the shipped engine, deletion or not: two runs of the *same* floor-on build and script
  disagree at 32k (11f3e40b vs 08da2dd6; `wall_selfcheck.txt`) — held scans at the cut extend the
  chain in arrival order. `frame_digest`'s schedule-invariance premise holds at a terminal cut; my
  first wall-budget burn pair inherited this noise (the floor-off run agreed with one floor-on run
  and not the other), and the deterministic re-fly resolved it. Judge digests on deterministic
  frames or terminal cuts.

Composition to 10⁹ (scout's published constants, not re-flown): coast-steady 0.066 segs/body × 336 B
≈ 22 GB inline at 10⁹ vs the floor's 353 GB — **the ~10× standing cut the scout priced is 16× on
this scene**, and under burn it is 3.3× because the law itself retains more (both builds), not
because the floor earns its keep: the floor's extra ≥ 1.0 seg/body is 97% past every window in every
flight.

## Predictions

`predictions.md` was written before the flights (the decision rules D1–D3 pre-registered).
**P1 held** (digests identical, coast and burn, deterministic frames). **P2 held and sharpened**:
engine serves exist between gathers (4,364–8,854 per interval at N = 10⁴), identical across the
toggle, zero engine misses anywhere. **P3 held** (view serves collapse 21550 → 353 cold at 20k burn;
misses pick up the difference; warm 175/gather). **P4 held at the measured cuts** (no vanished
emitters, shifts inside every disc — the 50/50 I registered landed on "holds") **and the risk it
named was real**: the observer-fallback mode exists (the wall-run rigid translation, ~7×10⁶ m),
schedule-conditional exactly as the burn-gather phase argument predicted. **P5 held** (0.066 ≤ 0.15;
15k transient ~1 in both). **P6 held** (warm ≤ cold in both builds). Per the pre-registered rule,
D1+D2+D3 hold on the deterministic record: **adopt, with the view call named** (the wall-run
observer mode is the one visible artefact; the engine's own fallback already exists and is
documented — the integrator decides whether to accept it or cap it).

## What would make it wrong

- The digest identity is scene-deep but single-scene: one belt geometry, one burn script, 60k
  game-s (≈ 2.1 kick intervals), N = 10⁴. A flight where an engine path *planned* to read a past era
  (a deep crash-search probe, a resonance chain) could still miss; the falsifier is a rung flight
  with the deletion aboard on `behave --law plane`.
- The observer-fallback magnitude scales with the player's post-event displacement over one
  interval; a high-γ player (the clock lens's scenes) would translate the sky by more. Falsifier:
  re-fly with a relativistic burn script.
- The wall-schedule digest noise (the side finding) means *any* future digest comparison mid-flight
  needs deterministic frames; a checker using wall budgets on this run's scripts will see DIFF lines
  that are not the deletion's (`wall_selfcheck.txt` is the control).

## Cost of adopting

One predicate in `PlainBodies::prune` (`h.len() > hold` with `hold = 0`) and one in
`droppable_until` — 2 lines of change, plus the integrator's view decision: either accept the
documented tube-alone/`t_read`-fallback (a view-only fidelity change, O(Δ) for refused reads), or
keep the floor only for the doll hosting the player / cap walks at `keep`. The instrument
(per-call-site counters, 60 read-only lines, Relaxed) should survive as the adoption meter, as the
scout proposed.

## Fit with PRINCIPLES

- #1 "Less is more… delete before optimizing": the floor stores surprise nobody certified — 97–98.4%
  of it past every keep window in every flight.
- #23 "Nothing past c… it allows to cheaply partition compute": the cone already partitions
  retention in the law; this run proves the deletion costs the law nothing and hands the remaining
  bill to the view, where #28 ("the view is an instrument… real vs displayed is not the same thing")
  says it belongs.
- #3 "Compute only surprises": refusing 98% of the chain walks makes the warm view 4× cheaper —
  the floor was paying serves to reconstruct what the tube already carries to first order.

## The lens

The scout lens again: search by flying the deletion, not by pricing it. What it may have missed is
yours to check: the burn's observer-fallback attribution rests on the code path
(`ext.rs:134` → `view.rs` fallback) plus the rigid-translation measurement, not on a per-call-site
backtrace of the player's own read; and the 10⁹ composition still leans on 398f's measured arc
widths rather than a re-fly with the seam patch.
