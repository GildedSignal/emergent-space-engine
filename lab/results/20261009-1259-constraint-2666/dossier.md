# Dossier — 20261009-1259-constraint-2666 (lens: the constraint)

## Claim

The flown frame's constraint is not the kicks but the view gather's per-emitter **exact tube readout**: an unbudgeted O(catalogue) scan at 60 Hz that is 69% of every frame (97% of it Newton light-cone crossings at ~42 µs each), and ≥96–99.9% of those readouts are replaceable per frame by advancing the last exact state (measured within 15–150 m), so the readout must become a scheduled event, not a per-frame scan.

## Bottleneck

The board's focus list ranks kicks first ("kicks dominate the engine's cost"). Measured on the whole, the flown frame at rtf 100 (76 bodies, paced, the player's mode):

| term | p50 ms | share |
|---|---|---|
| view_gather | 3.46 | **69.1%** |
| engine (budgeted 5 ms) | 0.24 | 18.1% |
| view_json | 0.43 | 9.1% |
| wire | 0.18 | 3.8% |

- Kick resolver (kick-bench, 20 s): 32 kicks, median 47 µs, 0.056 s total = **0.3% of wall**. Kicks dominate the *engine's internal* split; the engine is 18% of the frame and already defers (budget overflows 56/1800 frames; rtf low 1% = 9.9).
- The gather runs every frame over every body with no budget (plane.md §7 names the gather as work that must never take an unbounded synchronous claim — it currently does).
- Expected gain: the crossing term (2.77 ms of the 3.46) falls to ~1 µs/emitter (the fleet path's measured rate) → gather ~25–40× cheaper; at 417 bodies the same term is 6.12 ms (61% of an 8.75 ms frame, rtf low 1% = 0). What it deletes: the per-frame exact readout as a concept, replacing it with the same cadence logic the engine already uses for kicks (H0190).

## Evidence (Linux x86, orders of magnitude only; 8 vCPU shared, load ~1.0–1.7)

Attribution (instrumented gather, paced rtf 100, 1200 frames): `crossing_ms=2.767` of `bodies_ms=2.874` (96%), `player_ms=0.094`, `fleets_ms=0.053`; `readouts_per_frame=66.5` ≈ one per emitter (the Newton memo already works; the cost is the readout itself: 41.6 µs paced, 12.5 µs cache-warm unpaced).

The two decisive probes:

1. **Surprise rate** (does the Seen payload change above a player floor? direction 4e-4 rad ≈ ½ px, offset 1e-5 ls ≈ 3 km, colour 4e-3, shift/closing 1e-3): `per_frame=60.2` of ~66 emitters change. Wholesale skipping fails — the view is high-surprise at game-time rates. (Prediction 3's "skip most emitters" form is **refuted**; the refined form below holds.)
2. **Advance-instead-of-readout** (per emitter, exact crossing state vs linear advance of the previous frame's exact (x, v) over the ticks the crossing moved; error in root units, 1 unit = 1 light-tick ≈ 1.48 km):
   - rtf 100, 76 bodies: `lt_1.5m=0.485 lt_15m=0.963 lt_150m=0.999 lt_1.5km=1.000`
   - rtf 100, 417 bodies: `lt_150m=0.997 lt_1.5km=1.000` (295.8 readouts/frame, crossing 4.16 ms of the 4.32 ms bodies loop)
   - rtf 1000, 76 bodies: `lt_1.5m=0.316 lt_15m=0.516 lt_150m=0.716 lt_1.5km=0.995`

Existence proof already shipped: the fleet path renders members at ~1.1 µs each (advance from the stepper's committed tick, no exact readout) — 38× cheaper than the tube path for the same information class.

Commands (each ≤ 60 s except the 30 s benches; probes are the patch saved with this run):

    cargo run --release -p xtask -- universe --bench --seconds 30 --rtf 100          # shares table
    cargo run --release -p xtask -- universe --bench --seconds 20 --rtf 100 --members 400
    cargo run --release -p xtask -- universe --kick-bench --seconds 20
    # with this run's probe patch: gather_profile / surprise_profile / extrap_profile keys in the bench JSON
    cargo run --release -p xtask -- universe --bench --seconds 20 --rtf 100          # attribution + surprise
    cargo run --release -p xtask -- universe --bench --seconds 10 --rtf 1000        # horizon scaling

## Predictions

Written before the probes (`predictions.md`). Held: attribution (crossing readouts dominate, player fixed part 3% < 20%); per-emitter floors (7.8 µs measured marginal per fleet member against predicted 5–10; ~42 µs paced per tube readout against predicted 50–150). **Refuted as stated**: "skip the crossing for distant slow emitters on most frames" — the surprise probe shows 60/66 emitters legitimately change above floor each frame at rtf 100; the correct exploit is advance-then-refresh, not skip. Reported as held-out miss, not tuned away.

## What would make it wrong

- The floor is the load-bearing choice: if the instrument needs better than ~150 m freshness on distant emitters (a future visual layer with parallax at extreme zoom), the skippable fraction drops (at 15 m it is already only 96.3%); the refresh cadence adapts but the win shrinks. The floor must be derived from the view's own resolution ("the zoom level is the minimap", OC#30), per doll scale.
- Fast approachers (arrival windows of 0.1 ticks at 0.9c closing) invert the cadence: they need per-frame refresh; the selector 1 + n·β exists and is already computed for the Newton memo.
- Colour/aberration use velocity at emission; v advanced linearly on the same cadence — if colour floors bind tighter than position floors, the cadence shortens.
- Staleness is a representation change for the instrument only: the universe digest is untouched (observation still never writes; `cargo test -p emergent-universe` green with the probes in).

## Cost of adopting

`ViewCache` gains a per-emitter (x, v, rate, t_e) advance cache plus a refresh scheduler with the kick queue's shape; the gather becomes budgeted like the engine; Seen payloads become floor-quantized. One builder step on the plane; no law, crate or gate changes. PRINCIPLES: "Compute only surprises. ... Nothing is evolved that can be derived when looked at (clocks, redshift, views)" (#3); "no work for no reason, so no ticks ... we only care about changes" (#14); "The view is an instrument ... your dials are made up" (#28).

## Where the constraint moves next

With the gather off the frame, the frame's next constraint is the **engine's budget overflow at scale**: at 417 bodies 338/1200 frames overflow (28%) and rtf low 1% = 0 — the stepper's per-slice cost and cadence (4635 slices / 30 s; fleet slices 65.5 µs each), which is where the board's kick-cadence work already aims. The lab should measure the slice term next, not the resolver.

## The lens

The constraint lens measured the whole and inverted the board's assumed ordering (kicks → view); it may still under-weight what only appears at billions of bodies (encounter tiers, H_live), where absolute costs differ but the O(catalogue)-per-frame scan is fatal first (10⁶ emitters × 42 µs ≈ 41 s/frame). Cloud-vs-M1: shares are the claim, not microseconds.
