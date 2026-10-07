# Dossier — 20261007-0800-constraint-7a39 (lens: the constraint)

## Claim

On main, the frame's one constraint is the readout pipeline, not the engine — the engine is 5% of the frame while `view_json`+`wire` are 21% and the per-frame `serde_json::Value` tree they build also pollutes the allocator enough to triple the gather's own cost — and deleting the tree (a `#[derive(Serialize)]` pass over the borrowed `View`, byte-identical wire) cuts the paced frame p50 4.6× (3.31→0.71 ms) and p99 4.8× (5.19→1.07 ms) with identical digests, leaving the light-cone crossing readout (~9 µs/emitter, 88% of what remains) as the named next constraint.

## Bottleneck

The board's implied constraint ("kicks dominate the engine's cost") is true inside the engine but the engine is not the frame: measured on the plane as the player runs it, engine 5.1% / view_gather 73.6% / view_json 14.7% / wire 6.6% of frame CPU. The readout is also the only O(seen)-per-frame work, so it is the constraint at every scale up to the goal (billions of bodies, 16.7 ms frames): a sky with 10⁴ visible emitters is impossible at 40–80 µs/emitter and needs ~1 µs. This run deletes the serialisation half and names the remaining half. Expected gain: ~4–5× on the frame today (measured), and it deletes a whole mechanism (the per-frame `Value` tree, one allocation per field per emitter per frame — "the best part is no part").

## Evidence

Machine: the lab's Linux x86 runner (8 vCPU, load 0.3–1.1); orders of magnitude only, the integrator re-measures on the M1. All commands ≤ 60 s unless noted; every JSON cited is in `work/`.

1. **The whole, as the player runs it** (`work/bench-seed1.json`, 30 s):
   `xtask universe --bench --seconds 30 --seed 1` → frame p50 3.31 / p99 5.19 / p99.9 11.65 ms; engine p50 0.149 ms (5.1%), view_gather 2.37 ms (73.6%), view_json 0.536 ms, wire 0.241 ms; 0 hitches > 16.7 ms; 39 bodies, 76 emitters seen.
2. **Kicks inside the engine** (`work/kickbench-seed1.json`, 20 s): `xtask universe --kick-bench` → 61 µs median per distinct ship kick (369 µs leavers), only 23 distinct kicks in 20 s. The engine's own cost is event-driven and small at this scale.
3. **The exploit** (`work/patch.diff`, 269 lines: `session.rs`, `http.rs`, `mod.rs`): `view_json`'s `Value` tree replaced by `FrameJson<'a>`/`SeenJson<'a>` (`#[derive(Serialize)]`, fields declared in the `json!` map's serialised — alphabetical — key order), serialised once into a reused buffer; `Session::step` returns ms and exposes `wire()`/`last_seen()`; the page's response is spliced from the same bytes; the old tree is kept only inside the byte-identity test.
4. **After** (`work/bench-seed1-after.json`, same command, ~30 s): frame p50 0.713 / p99 1.074 / p99.9 3.220 ms; view_json 0.536→0.000 ms; wire 0.241→0.031 ms; view_gather 2.373→0.650 ms (**unchanged code**: the tree's allocator churn had been charged to the gather); **digest identical** (`d96acc05…` both runs).
5. **json-dominated profile** (`work/bench-m480*.json`, 10 s): `xtask universe --bench --seconds 10 --members 480 --unpaced` → frame p50 1.636→0.739 ms, view_json share 50%→0.3%, wire 0.237→0.157 ms, digest identical.
6. **The wire is pinned byte for byte**: `cargo test --release -p xtask wire_bytes` → 1 passed (the derived output equals `to_vec(json!(…))` on a View covering every field kind, `None` and `Some` loss, all emitter kinds).
7. **The page still flies** (the surface a player runs): `xtask universe --port 8799` then `curl -X POST :8799/frame -d '{"keys":1,"throttle":1}'` → HTTP 200, 22.4 KB valid JSON (`dash`,`frame`,`server_ms`), frame carries `tick`/`seen`.
8. **Gates on this runner**: `xtask engine-judge` → E1–E5, E7, E8 PASS; E9 FAIL at short periods only (phase 1, by design); E6 FAIL "UNSUPPORTED … prepared-mutants.json" (a missing artifact on this checkout, not physics). `xtask behave --law plane` (also with `--plane-step 7`) → G1–G7, B9–B14 all FAIL with `worst inf`/`NaN`/0.00 s and B9 reporting "advance_per_cycle after the first call: median 5 ns": every oracle call returns nothing instantly. That contradicts main's recorded state (G1–G6 pass, B13 60/64) — an instrument anomaly on this host that the checker should reproduce before trusting any plane-gate reading from the Linux lab; it is not adjudicated here.

## Predictions

Written before the decisive experiment (`predictions.md`). Held: bytes identical (test), json+wire ≥ 5× (26×), m480 json share < 10% (0.3%), digests unchanged, and the constraint moves to the gather's crossing readout. Missed, in the informative direction: I predicted the gather would stay at ~2.37 ms; it fell to 0.650 ms on unchanged code — the per-frame `Value` tree was polluting the allocator for the gather's own allocations, so the readout constraint was even larger than the dashboard said (an instrument lesson: the dashboard's parts share one allocator; shares are not independent costs).

## What would make it wrong

If the page drew from the `Value` tree with different semantics than serialisation (it does not: it receives the same bytes), or if the M1's allocator makes the tree cheap (unlikely: the cost is per-field allocations, and 4.6× on x86 is not a margin effect). The 10⁴-emitter extrapolation assumes the gather stays O(seen) with culling at scale — not yet measured above 428 emitters (`work/bench-m4800.json`: 28 bodies, same profile; members beyond what the fleet hands out are not bodies yet).

## Cost of adoption

One small patch (`work/patch.diff`: 3 files, no crate changes, no physics, no representation change — the wire bytes are pinned by a test and both digests are identical). The next constraint it exposes: `view_gather`'s per-emitter light-cone crossing (Newton on `state_rate` readouts, ~8.6 µs/emitter paced at 76 seen; 4.4 µs at 428 seen unpaced) plus the `Seen` allocation per emitter per frame. At ~9 µs/emitter, 1.8k visible emitters exhaust a 16.7 ms frame; the crossing readout must fall ~10× (incremental crossings, `readouts` is already counted in `ViewCache`) before a crowded sky (fleet battles, dense belts) is smooth — that, not the serialisation, is where the readout meets Julien's "the zoom level is the minimap".

## Fit with PRINCIPLES

- "The cheapest compute is compute not done. Delete before optimizing" (#1): the tree was pure deletion.
- "the best part is no part" (#17): the `Value` tree is a part that no longer exists.
- "i care about the p95/99 results i want the game to be smooth" (#12): p99 5.19→1.07 ms, p99.9 11.65→3.22 ms.
- "Compute only surprises" (#3): nothing observable changed — identical digests, identical wire bytes.
- Measured before claiming; the simplest falsifying test (digest + byte identity) came first.

## The lens

Goldratt finds one constraint and this run exploited it, but the constraint lens can mislead at goal scale: the plane has 39 bodies, so "the readout is the frame" may be a small-N artifact — at billions of bodies the engine's event cost and the memory floor (2293 B/body here; H_live) re-enter, and the queue's encounter/co-orbital work attacks those. Also this lens measured the plane only as the bench runs it (one observer, one system): multi-observer or high-zoom readouts were not probed, and the behave-gate anomaly (point 8) left the law's gate state unverified on this host.
