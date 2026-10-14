# Dossier — 20261014-1137-inversion-62c1

**Lens:** inversion (invert the most recent success). **Topic:** view (cost side) / the N1 gate's reading.

## Claim

The plane's flyable ceiling is ~10³ bodies, not the merged gate's 10⁶: gate N1 certified the engine slice of the frame, but the page the player flies pays the view per browser frame, the view is Θ(N) with no culling, and the frame crosses the 16.7 ms display budget at the gate's own first rung — 21.5 ms p50 at 10³, 255 at 10⁴, 2,614 at 10⁵ — while the set of rows the page can actually draw stays ~73, flat in N.

## Bottleneck

The board's top row ("real bodies in the flyable engine: 10⁶ against 10⁹" — now 10³.3 real, 10⁶ engine-only). The term is `gather_with`'s bodies loop (crates/universe/src/view.rs): a Newton crossing + a `Seen` push for every alive body, no zoom/frustum/brightness test, then name+kind+9 floats per row on the wire, every frame. Gain from the named lever (row-set deletion: read on-canvas rows exactly, far rows only when their displayed pixel moves): the gather collapses from O(N) (measured 2,351 ms at 10⁵) to O(visible + display-moved) ≈ 10² rows ≈ 2–3 ms — **~10³× at 10⁶**, and it deletes the wire's 27 MB/frame with it (serve the display quantum, not 9 floats × N). It deletes no component of the engine; it changes one function's row set and the wire's shape.

## Evidence

What the player runs (shipped code): `page.html`'s `requestAnimationFrame` → `POST /frame` → `Session::step` (xtask/src/universe/session.rs:116) = `frame_to` under a 5 ms wall budget → `gather_cached` → `view_json` → `serde_json::to_vec`; the served dashboard's own frame metric is "engine + view + wire". The gate's ladder timed the engine slice only and listed the view as "outside the engine's F1; the page pays it" (artifacts/runs/nladder/ladder.txt — its own column: 136 ms at 10⁴, 1,377 at 10⁵, 29.8 s cold at 10⁶ on the M1).

Measured here (`flyframe`, a new example that flies the page's exact frame on the ladder's own population, `scenario::plane_extra`, coast, rtf 100, seed 1, the page's 5 ms engine budget and wire shape row for row; census at the page's own `fitLog` zoom and both displays, 1920×1080; Linux/x86 shared — orders of magnitude):

| bodies | rows/frame | flyable p50 ms (engine/gather/wire) | over 16.7 ms | on-canvas | sky-static |
|---|---|---|---|---|---|
| 28 (the plane) | 65 | 0.99 (0.04/0.80/0.13) | pass | 67.7% | 83.9% |
| 1,028 | 1,062 | **21.5** (0.07/19.3/1.9) | **1.3×** | 6.8% | 96.8% |
| 10,028 | 10,065 | **255** (0.18/231/22.9) | 15× | 0.73% | 99.6% |
| 100,028 | 100,066 | **2,614** (1.06/2351/256) | 156× | 0.073% | 99.96% |

- The flyable frame is linear in N (exponent 1.08 then 1.01 over the two decades 10³→10⁴→10⁵), the gather 90–91% of it at every rung, the engine flat exactly as the gate certified — the gate's number is real and 0.03–4% of the page's frame. Extrapolated 10⁶: ~26 s/frame here; the M1 ladder's own cold gather at its "pass" 10⁶ rung was 29.8 s.
- The visible set does not grow: **72/73.7/73.3 rows on-canvas at 10³/10⁴/10⁵** (the ~300 locals near Home/Moon plus planets, star, fleet rows). The page draws nothing for off-canvas kind≥3 rows (page.html's map loop: only planets/moons/star get edge markers) — ≥93% of the gather's rows at 10³, ≥99.9% at 10⁵ buy zero pixels in map mode.
- In sky mode every row is a dot, but **99.6–99.96% of dots are pixel-frozen frame-to-frame** at 10⁴–10⁵ (the log-scale radial display quantizes far bodies into stillness) — 0e54's display-quantum cache, refuted on plane scenes (5.5–31.2% served at 28–948 bodies), serves ≤0.4% here: the domain where N actually bites is the domain where the deletion works.
- The wire churns regardless: name+kind+9 floats × N per frame = 0.29/2.7/27 MB at 10³/10⁴/10⁵, with 99.2–99.6% of row bytes changing every frame (float low bits) — a pure per-frame tax.
- Controls: at 28 bodies the flyable frame is 0.99 ms and 67.7% of rows are on-canvas (the instrument passes where the shipped game lives); readouts/row 1.16–1.96, the crossing cache near-perfect as the record says — the row cost is the readout itself, which is why the lever is the row set, not the row's µs.

Commands (each ≤ 60 s except 10⁵, ~4.5 min; full set ≈ 6 min — `lab/results/20261014-1137-inversion-62c1/regen.sh`):

```
cargo run --release -p emergent-universe --example flyframe -- 0 240 100
cargo run --release -p emergent-universe --example flyframe -- 1000 480 100
cargo run --release -p emergent-universe --example flyframe -- 10000 240 100
cargo run --release -p emergent-universe --example flyframe -- 100000 48 100
```

The probe is this run's patch (`work/patch.diff`: the example + a serde_json dev-dependency; shipped code untouched otherwise).

## Predictions

Written before any run (predictions.md). Held: the crossing point (sharper than predicted — at 10³, not between 10³ and 10⁴), the gather share ≥80% (measured 90–91%), on-canvas <2% at 10⁴ (0.73%), sky-static ≥90% (99.6%+), both N=0 controls. Died and disclosed: map-pixel-staticness ≥95% (measured 2.5–13.3% — parallax at the fitted zoom moves far map dots; the map-side lever is the canvas test itself, which is the page's own draw condition, not my proxy) and the wire-identity range (0.4–0.8%, below my 60–95%).

## What would make it wrong

- A page that does not poll per frame (it does; and `Session::step`'s own dashboard includes view+wire in the frame it reports).
- A gather whose cost is not per-row but per-event (it is per-row: linear in alive bodies with zero events in these windows).
- The deletion breaking the game's own use of far rows: a player who zooms out to see the belt, or turns (a heading change rotates every sky dot at once), re-reads in bursts — the lever's contract, not its refutation; unmeasured here (coasting, fitted zoom, one canvas).
- The M1 disagreeing on the crossing rung: the ladder's own M1 column (136 ms at 10⁴) already rules this out; the integrator re-measures anyway.

Cost of adopting: one function's row set (canvas test + display-quantum far rows) and the wire's shape (deltas or quanta). No law change; the view is pure derivation ("Compute only surprises"; "clocks, redshift, views" are derived, never evolved — PRINCIPLES #3), so nothing canonical moves. The client's own per-frame `[...seen].sort()` of 10⁵ dots is the twin term on the browser side and dies with the same row set.

Fit with PRINCIPLES: "Compute only surprises. Nothing is evolved that can be derived when looked at (clocks, redshift, views)" (#3) — a far belt body's dot is not a surprise; recomputing its crossing and shipping 9 floats for it every frame is exactly the evolved view the principle bans. And "The view is an instrument" (#28): the instrument's resolution is the display quantum, not the row.

## The lens

Inversion found the composition failure: two records each true (view.md: "the view is the frame constraint" at ≤948 bodies; ladder.txt: the engine flat to 10⁶, the view column printed and passed over), one false scoreboard row ("10⁶ in the flyable engine"). What the lens may have made me miss: the physics of the view (the timing/memo holes are the page's other open front — a cheaper gather that stays Θ(N) fixes neither), and the engine-side breaks the ladder already named (the wave at 140 s, the player seam) are real and remain the *engine's* next walls; this run only re-hangs the flyable number on the term the player pays.
