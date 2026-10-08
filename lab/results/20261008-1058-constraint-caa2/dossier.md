# Dossier — the constraint, measured on the whole plane

## Claim

The frame's constraint is the **view gather**, not the engine: a synchronous, unbudgeted,
unculled `for i in 0..n_bodies()` scan (`crates/universe/src/view.rs:300`, plus the fleet
member loop at `:339`) that costs **24–35 µs per body per frame** (linear, no distance,
brightness or change culling), takes **64–89 % of frame CPU** from the plane's own 28
bodies upward, and makes every scale-up on the board (the 2²⁰-body belt of B18b, the
galaxy doll, 10⁹ bodies) land on a wall of **25–36 s, and 7–10 hours, per frame** — while
the engine the whole bottleneck board optimizes is **1.3–7.8 % of the same frames**.

## Bottleneck

Board bottleneck 4 (smoothness, p99 on the frame) hiding inside it the representation
question of bottleneck 0: the view is *per-tick work over all bodies*, exactly what
principle 14 bans for the engine and the view escapes only because no one had measured it.
Expected gain from fixing the representation (not the constant): the gather goes from
O(N·readouts) to O(visible + dolls) — at the belt's 2²⁰ bodies that is ~3 orders of
magnitude of frame time deleted, and it deletes the Seen list's O(N) JSON/wire tail with it.

## Evidence (all on this Linux runner, 8 vCPU, load ~1.0; orders of magnitude only)

Shipped code, unpatched (`/tmp/x-target/release/xtask`, release, seed 1 unless said):

| run | bodies+members | frame CPU p50 | gather p50 (share) | engine share |
|---|---|---|---|---|
| `universe --bench` (paced 30 s, rtf 1) | 39 + 48 | 3.30 ms | 2.37 ms (**74 %**) | 4.5 % (max 11.8 ms) |
| `universe --bench --rtf 100` | 39 + 48 | 4.25 ms | 3.45 ms (**70 %**) | 17 % (p99 5.24 ms, 36/1800 overflow, rtf low-1 % = 17) |
| `universe --kick-bench` | — | — | kick median 44.6 µs (made), 384 µs (leavers); exact memo hit 0 % on 27 distinct rebinds | — |

Scaling ladders (4 s, unpaced; the two env/arg patches are in this run's saved diff and
disclosed here: `ES_SHIPS` multiplies the star ships in `scenario.rs`, `--members` clamp
raised to 200 000 in `xtask/src/universe/mod.rs` — the gather itself is untouched):

| bodies | gather p50 | share | per body |
|---|---|---|---|
| 28 | 0.69 ms | 64 % | — |
| 136 | 4.45 ms | 82 % | ~35 µs |
| 1216 | 42.55 ms | 85 % | 35.0 µs |
| 1216, seed 7 | 29.20 ms | 89 % | 24.0 µs |
| 1216, seed 42 | 29.39 ms | 88 % | 24.2 µs |

Members (the fleet's cheaper loop): 1600 → 3.71 ms, 6400 → 22.56 ms gather p50 ≈ **3.9 µs
per member** — also linear, ~9× cheaper per head than a body's Newton crossing, as predicted.

Extrapolation (linear, measured slope): 60 Hz affords **~480–700 bodies per frame**;
B18b's belt (2²⁰) = **25–36 s/frame**; the goal's 10⁹ = **7–10 h/frame**. Engine at 1216
bodies: p50 0.61 ms, share 1.3 % — the gather outbids it 70×.

Gates (`behave --law plane`, this run): G1–G6 and B7–B11 fail as *unanswered* (the plane
cannot express the space-law scenes — the handoff's known adapter limit, not a new
failure); B12 miscalibrated and B13 60/64 (both known); **B14 timed out at 60.1 s** under
this window's load and stopped the run before B17+. No smoothness gate exists for the
view (B15 is p99-of-frame: the gather drives it but no gate sizes a representation).

Reproduce (each ≤ 60 s here): `CARGO_TARGET_DIR=/tmp/x-target cargo build --release -p xtask`;
then `/tmp/x-target/release/xtask universe --bench [--rtf 100]`, `... universe --kick-bench`,
and with the patch `ES_SHIPS=1200 ... universe --bench --unpaced --seconds 4 [--seed 7]`,
`... --members 6400 ...`. Raw JSONs sit next to this dossier (`bench*.json`,
`scale-ships-*.json`, `scale-members-*.json`, `kick-bench.json`, `behave-plane.txt`).

## Predictions

All three held ([predictions.md](predictions.md)): (1) linear bodies scaling at 20–90 µs
— measured 24–35 µs, and at 1200 ships the gather alone (42.5 ms) is 2.5× the whole
16.7 ms budget with the engine inside its own; (2) members linear and cheaper per head
(3.9 µs vs the predicted 0.3–2 µs band — slope underestimated ~2×, ordering correct);
(3) at rtf 100 the engine's p99 (5.24 ms) reaches its 5 ms budget and pulls rtf's lowest
1 % to 17 while the gather stays flat per frame.

## What would make it wrong

- The belt/galaxy scope routes bodies through a visibility structure of its own and the
  plane's gather is replaced wholesale — then this wall is an artifact of the plane's
  first-flight scope. As shipped, `gather` loops the one `BodyStore` everything lands in.
- The engine's own tail (rtf 100: p99 5.2 ms, max 11.9 ms at 39 bodies) becomes the frame
  constraint before scale arrives — true only if the player's flights stay ≤ ~500 bodies,
  which the goal (billions) contradicts.
- Linux/x86 vs the M1: the *share* (64–89 %) and the linear exponent are robust across
  seeds; the absolute µs re-measure on the M1 (heat included).

## Cost of adopting, and where the constraint moves next

- **Exploit the constraint as-is** (hours): advance each emitter's crossing memo by its
  stored arrival rate (`ViewCache` already holds root and slope; the arrival rate is exact
  physics) and read state only when the extrapolated bracket fails — deletes the 1–3
  `state_rate` readouts per body per frame; also stop cloning a `String` per `Seen` per
  frame. Constant-factor only (2–3×), still O(N): not the fix, but it buys the near term.
- **Subordinate**: nothing else may add per-body per-frame work; `view_json` and `wire`
  inherit the gather's O(N) through the Seen list, so the cull must sit *before* `seen.push`.
- **Elevate (the representation, one design step)**: cull by **distinction, not
  distance** — walk the doll tree, ask per doll how many emitters the player can
  differentiate at the current angular resolution and brightness floor, cross individual
  worldlines only for those; aggregates below one quantum accumulate (principle 6). This
  is OC#30's "the zoom level is the minimap" made load-bearing, on the same doll tree the
  engine already holds. Gather becomes O(visible + dolls).
- **Constraint moves next** to the engine's event tail at rtf ≥ 100 (p99 5.2 ms vs the
  5 ms budget at 39 bodies) and then to candidate work per real encounter at belt scale —
  i.e. the board's current top items are the *next* constraints in line, not the current one.

## Fit with PRINCIPLES

- P3: "Nothing is evolved that can be derived when looked at (clocks, redshift, views)" —
  the gather re-derives every body's crossing every frame, changed or not.
- P14: "no work for no reason, so no ticks" — the view is the last per-tick loop in the plane.
- P5/OC#30: "we need a map, but a map that is inferred based on intelligence for the
  territories"; "the zoom level is the minimap" — the cull's law.
- P1: the cheapest compute is compute not done — 24–35 µs × every body × every frame.

## The lens (what it may have made me miss)

Goldratt sees throughput; it can undervalue the trust work that moves no frame time: B12's
miscalibration and the unanswered G-gates block confidence in the law regardless of speed,
and B14's timeout under load says the instrument itself is marginal on shared runners. I
measured the plane, not the M1 (orders of magnitude only, per the lab rules), and the
per-body split *inside* the gather (Newton readouts vs chain walk vs String clones) is
inferred from the code, not separately timed — the total and the linearity are measured.
