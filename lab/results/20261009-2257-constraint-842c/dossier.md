# Dossier — 20261009-2257-constraint-842c (constraint lens)

**Claim.** At the plane's operating point (rtf 100, 60 Hz) the frame's one constraint is the **view pipeline, not the engine**: gather + JSON are 72–90% of frame CPU, the gather is linear in emitters at ≈ 5.3 µs per body per frame with **no differentiation floor and no pooling** (every emitter re-derived and re-serialised every frame, ~99% of them sub-half-pixel in a battle scene), and the view is the only part of the frame with **no budget** — while the engine, the supposed cost centre, has p50 0.05–0.13 ms (5–24% of the frame) and only its burst tail (p99 ≈ 5.2 ms ≥ the 5 ms budget, 111/1800 overflow frames at 428 bodies) presses the frame at all.

**Bottleneck.** The board's live order says "kicks dominate the engine's cost" — true *inside* the engine, but the engine is not the frame. Measured on the whole (`where_the_time_goes_ms`, rtf 100, unpaced 30 s, seed default):

| members | bodies | gather p50 | engine p50 | engine p99 | frame p50 | overflow frames | events/s |
|---|---|---|---|---|---|---|---|
| 48 | 76 | 0.71 ms | 0.045 ms | 1.29 ms | 0.89 ms | 3 | 242 |
| 400 | 428 | 2.58 ms | 0.13 ms | 5.24 ms | 3.32 ms | 116 | 1107 |
| 1600 | 428 | 2.59 ms | 0.13 ms | 5.23 ms | 3.33 ms | 112 | 1108 |
| 6400 | 428 | 2.53 ms | 0.13 ms | 5.21 ms | 3.28 ms | 111 | 1106 |

Paced at the player's rate (30 s, rtf 100): frame p50 4.4 ms, p99 10.5 ms, worst 12.3 ms, **zero hitches above 16.7 ms** — the plane flies; the shares are gather 69.5%, engine 17.8%, JSON 9.0%, wire 3.8% (`bench-rtf100.json`). Expected gain from flooring the view: it deletes up to ~99% of per-emitter view work in fleet scenes and ~90% of view+JSON in the plain scene (the 11 haulers sit at 1100–3000 light-seconds) — an order of magnitude off the frame, without touching a law, a gate or an outcome (the gather is a pure read; the digest is unaffected).

**Evidence.**
- Sweep (above): `xtask universe --bench --seconds 30 --rtf 100 --unpaced --members {48,400,1600,6400}` — slope (2.58−0.71)/(428−76) = **5.3 µs per body per frame**, linear over the reachable range.
- Live view probe (`view_probe.py 300 1600`, seed 7): 371 emitters/frame, 343 of them fleet members; member distances p50 0.0076 ls, max 0.023 ls → a ~28 m member (radii in lattice units × 1.41 m) subtends 1.2–4×10⁻⁵ rad, **24–73× below a 1080p half-pixel** (2.9×10⁻⁴ rad at 60° fov). A pixel floor keeps the star, 3 planets, the moon and the nearest member(s): ~5 of 371 emitters.
- The gather *already computes* `angular_radius` per emitter (`Seen`), sends neither it nor luminosity on the wire, and filters on nothing (`crates/universe/src/view.rs:300–368`).
- Kick resolver on distinct pending kicks (`--kick-bench --seconds 20 --rtf 100`): median 76 µs, p99 379 µs, memo quantized hit 94.5%, 0 refused — expensive per event but rare per frame; not the frame's constraint.
- Budget asymmetry: the engine runs under `Budget::wall(5 ms)` with causal-deadline order; `gather_with` has no budget path at all — plane.md §7's "nothing takes an unbounded synchronous claim on the frame" is enforced for the engine and absent for the view.
- Gates (context, not throughput): `behave --law space --gates G1,G5` PASSes; `behave --law plane` (default and `--plane-step 7`) returns G1/G5 unanswered (0/256, worst inf, "32 short") and B13 60/64, B14 timeout 60.1 s — the motion law v2 steps 1–2 state, already known in flight; the law itself is not what this run judged.

**Predictions** (`predictions.md`, written before the sweep and the floor count):
- P1 (gather linear, 3–8 µs/emitter) — **held** over 76→428 bodies (5.3 µs), but the top end falsified differently: bodies **cap at 428** for members ≥ 400 because the fleet dissolves (`dissolved: 1`) — the plane's only scale knob saturates; the plane cannot presently be pushed past ~430 bodies.
- P2 (≥80% of emitters below a pixel floor) — **falsified in direction, stronger**: ~99% are below it; even the *nearest* members are sub-half-pixel by 24×. My threshold form (distance 0.05 ls) was the wrong representation; the floor is angular.
- P3 (engine p99 over budget while p50 ≤ 1 ms) — **held**: 111–116 overflow frames at ≥ 400 members, p50 0.13 ms.

**What would make it wrong.** If the page must draw every member as a distinguishable dot always (an instrument choice, not physics — the members overlap in a few pixels), a pure cull changes what the player sees; then the exploit is pooling (one aggregate `Seen` per angular cell: count, flux-weighted centre, mean shift/colour), which keeps the rendered image bit-comparable while deleting the same work. Also wrong if emitters are few by design at the target scenes — but the goal is billions, and every added body lands in this loop.

**Cost of adopting, and fit with PRINCIPLES.** One step: a floor/pool at the gather's push (the number it needs is already computed), plus a budget wrapper identical to the engine's — no crate, law, gate or format changes. This is PRINCIPLES #3 verbatim — "Nothing is evolved that can be derived when looked at (clocks, redshift, views)" — taken to its second half: the derivation must also not be *re-paid* for what the player cannot differentiate (#33: "a body resolves only the influences that are significant at its own scale"; the register: "the floor is what the player can differentiate"; #5: "the zoom level is the minimap"). The same aggregation the co-orbital gold (20261006-0346) forced on the encounter tier, applied to the view tier.

**Where the constraint moves next.** Once the view is floored it is O(pixels), not O(bodies) — and the constraint moves to the engine's **per-body event rate**: measured 2.6 events/s/body at rtf 100 (1108 events/s at 428 bodies; "surprises only", yet still per-body), whose p99 bursts already breach the 5 ms budget at 428 bodies. At 10⁹ bodies that rate must fall ~10³×, which is the board's cadence/doll-depth lever (fewer kicks per orbit; bodies deeper in dolls carry no per-body events) — now with a measured constant to design against. Standing behind both: memory at 5,979 bytes/body (`bytes_per_body`, m1600) against the 8 B/body of 10⁹ in 8 GB — the H_live question, untouched by this run.

**The lens.** The constraint lens reads flow (frame time), and its blind spot is stock: bytes_per_body nearly went unmeasured because no frame-time instrument shows it. It also inherits the bench's own scope — "the plane as built" — where the fleet dissolves at 428 bodies; a scale claim past that point needs the encounters/population work the board already queues. Lens-narrow also in judging the view by the frame: for the player the view *is* the product, so "delete view work" must always mean floor-or-pool, never "draw less truth".
