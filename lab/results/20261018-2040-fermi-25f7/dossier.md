# Dossier — 20261018-2040-fermi-25f7

## Claim

The ladder's N-flat frame certificate is a **blind-player** certificate: with the view in
the loop (the game as played, `flight_sweep.rs`'s own loop), the flyable N on shipped code
is **~6×10² bodies** (p99 crosses 12 ms between N=500 and N=1000 on this box) — the view,
not the engine or the memory, is the flyable engine's first break, 3–4 orders below the
build-bytes wall (3.4×10⁶ on the 8 GB M1) and ~5 orders of CPU below 10⁹.

## Bottleneck

Board #1: "bodies in the flyable engine: 28 against 10⁹ … which term breaks first as the
plane grows". Every prior ladder rung flew `nladder.rs`, whose flight loop never gathers
the view (it gathers once, after the flight, to price it). The game as the player sees it
gathers every frame (`flight_sweep.rs:120`), and the gather is Θ(n_bodies) **by physics**:
view.rs — "each tube crosses the cone once"; every body's worldline crosses the player's
past light cone, so there is no cull and `seen = N+61` at the ladder. The gain from naming
this: it re-ranks every 10⁹ estimate that leaned on the ladder's N-flat frames, and it
makes the view's aggregation (rows) a requirement, not an optimization.

## Evidence

`regen.sh` was verified end to end from a restored tree (patch applied, rebuilt, re-flown):
every deterministic digit identical (game_s, kicks/body/game-s to the last digit,
over-counts), timings within load noise (view 23.3/24.0 µs/body at 4×10³/8×10³, blind
p99 6.0/6.7 ms, 0 over) — see `work/vladder.log`, which regen overwrites on each run.

Instrument: `crates/universe/examples/vladder.rs` (new, this run's patch) — `nladder.rs`'s
flight verbatim (same `plane_extra`, same `frame_to` budget, same seed 1 coast) with one
change: `gather_cached` every frame after the first second, timed separately from the
engine. Reproduce: `lab/results/20261018-2040-fermi-25f7/regen.sh` (~4 min).

| N | seen | view p50 ms | µs/body | frame p50/p99 ms | over 12 ms | game kept % |
|---|---|---|---|---|---|---|
| 0 | 59 | 0.76 | 12.8 | 0.82 / 2.9 | 1 | 1342 |
| 500 | 559 | 8.42 | 15.1 | 8.5 / 14.1 | 14 | 180 |
| 1000 | 1059 | 19.2 | 18.2 | 19.4 / 25.6 | **420/420** | 82 |
| 2000 | 2059 | 42.7 | 20.7 | 43.0 / 49.9 | 420/420 | 38 |
| 4000 | 4059 | 89.6 | 22.1 | 90.1 / 98.4 | 420/420 | 18 |
| 8000 | 8062 | 188 | 23.3 | 190 / 228 | 260/260 | 8.6 |

Blind controls (same flights, no gather): N=2000 p99 6.86 ms, N=8000 p99 7.10 ms, **0
frames over 12 ms both**, game kept 1436%/892% — the engine alone is N-flat at this scale
(P4 held; reproduces the ladder's known law at 8×10³). The view owns 94–99% of every frame
from N=1000 up. Break: the view alone reaches 12 ms at seen ≈ 650 (12 ms ÷ 18.5 µs).

**The in-loop law is not the settled-state law.** dcf1 priced the warm gather at 5.0
µs/body (measured once, after the flight ended). In-loop it is 15→23 µs/body and the
memo degrades: readouts/seen rise 1.23 (N=0) → 1.45 → 1.65 → 1.80 → 1.88 → 1.95 (N=8000),
against the documented warm ≈ 1.0 / cold 2–3 — the engine's own advancing state makes the
cache behave half-cold. The µs/body marginal is flat ~22–23 µs above 2×10³ seen (the
belt's 2,340 B/body working set leaves cache). Box: Linux x86 shared, load 0.59→2.00
during the ladder, load includes these runs themselves; orders of magnitude only, the
integrator re-measures on the M1.

**The 10⁹ arithmetic (the Fermi ledger, one 12 ms frame at 60 fps):**

| term | law (source) | break-N |
|---|---|---|
| view gather, in-loop | 18–23 µs/body/frame (this run) | **~6.5×10² seen** |
| one capture volume | ~190 ns/body (96f6, formation) | ~5×10⁴ |
| build bytes | 2,340 B/body (99da/dcf1) | 3.4×10⁶ (8 GB M1); 8.5×10⁵ (2 GB box) |
| engine frame | N-flat ≥ 8×10³ (this run's controls; dcf1 to 3×10⁵) | >3×10⁵, unbroken |

At 10⁹ the per-frame per-body gather is 10⁹ × 20 µs × 60/s = 1.2×10⁶ core·s per game-s
(~10⁵ cores even at dcf1's settled 5 µs) — five orders of CPU over the ~8-core target, so
**10⁹ is unplayable through a per-body view at any per-body price the physics of this
gather allows**; the view must resolve aggregates (2df1's row-set: 1–3 ms at 10³–10⁶,
unshipped; e401's tier 0.56 µs/member covers formations only). The ledger also sharpens
the memory statement: the build wall (3.4×10⁶) is real but it is the *third* break, not
the first.

## Predictions

`predictions.md` was written before the flight. P1 (break 1,000–4,000): **missed low** —
measured 500–1,000, because the in-loop per-body cost is 3–4× the 5 µs constant the
estimate leaned on. P2 (linear, 4–7 µs/body): magnitude missed (15–23 µs), shape held
above 10³ (marginal flat ~23 µs). P3: direction held, thresholds lower (82% kept at 1000,
8.6% at 8000). P4 (blind controls hold ≤12 ms): **held exactly** (6.9/7.1 ms, 0 over).

## What would make it wrong

The break scales with this box's per-body cost (18–23 µs here); on the M1 it moves with
whatever dcf1-class conditions give (their settled warm was 5 µs — if the M1's in-loop
cost is 5 µs/body the break moves to seen ≈ 2,400, my original estimate; still 3 orders
under the build wall). The *ranking* — view ≪ capture ≪ build — survives any plausible
per-body price because all three scale by the same hardware and the view's per-frame
cadence is 60× the capture's 0.097/game-s rate. It would be wrong if the game does not
need a per-frame gather (a per-event or throttled view), but the shipped pilot loop
(`flight_sweep.rs`) gathers every frame by construction.

## Cost of adopting / fit

Nothing to adopt: this is a re-ranking. The consequence lands on the view page's domain:
the row-set deletion (2df1) or an equivalent cone aggregation is the flyable engine's
*requirement* at any N beyond ~10³, ahead of the memory work at 3.4×10⁶. PRINCIPLES 33:
"each scale resolves only what matters at that scale — a raindrop is an event for an ant
and nothing for a lion": the far belt is a row to the player's eye, not 10⁹ individual
crossings; the current gather resolves every raindrop at every scale. PRINCIPLES 3
(compute only surprises) says the same: each far body's crossing is derivable, not a
surprise.

## The lens (Fermi)

The estimate killed my own prediction's constant before the checker could: the 5 µs/body
I leaned on was a *settled-state* number, and the run's value is exactly that mechanism
(the mid-flight memo invalidation, readouts 1.2→2.0). What the lens may have missed: I did
not measure the view's cost at burn (the burn may invalidate more of the memo per frame),
and I did not probe whether a *stale* cache (gather every k-th frame) recovers the settled
law — the throttled-view door that would soften the ranking's cadence term.
