# Dossier — 20261011-1332-constraint-acff (lens: the constraint)

## Claim

On the plane as it flies, the engine's *mean* cost is not the constraint (12–34% of the frame budget at 76–428 bodies); the constraint is **per-frame and per-item structure**: the view gather, which is O(N) every frame (8.5 µs/body: 3.4 ms at 76 bodies, 6.4 ms at 428 — the frame-time constraint), and single events bigger than the whole 5 ms engine budget (a fleet's battle slice, 6–12 ms in one item; the player's step, 1.3–8 ms with an O(N) neighbourhood scan), which no allocator can fit under the budget — overflow frames grow 45/1800 (2.5%) → 394/1800 (22%) from 76 → 428 bodies at rtf 100, and the achieved rtf's worst 1% falls to 0.

## Bottleneck

Board bottleneck 4 (smoothness and the allocator) as it lands on the plane, feeding the queued b-readout-cost (the view) and b-encounter-skin / b-coorbital-cert (the player's O(N) scan, measured here at ~6 µs per body per player event: player per-item cost 1.29 ms → 3.40 ms for 76 → 428 bodies). Expected gain from the named exploit (deadline-sized battle slices, certified below): removes the >5 ms single items, i.e. the overflow tail, without touching a law — order 1 for the frame, but it unblocks the allocator entirely (today the worst frame is one item at 2.4× the budget).

## Evidence (all commands ≤ 60 s, Linux x86 8 vCPU, load 0.6–0.9, files in this folder)

Build: `cargo build --release -p xtask` (38 s cold). Binary at `$CARGO_TARGET_DIR/release/xtask`.

- `xtask universe --bench --seconds 30 --rtf 100 [--members M] [--threads T] [--engine-ms B]` — the patched bench adds a per-frame trace (engine ms per frame + items and cost by kind + overflow flag; `trace-*` files, summarised by `summarize.py`).
- m48 t1 (76 bodies): frame p50 4.19 / p99 10.55 ms, 0 hitches >16.7 ms; engine p50 0.234 ms, p99 5.24 (the cap), share 0.18; overflow 45; rtf median 100, lowest 1% 9.9. Engine totals: ship 407.7 ms / 1541 items (264 µs each), player 374.8 / 291 (1.29 ms each — one body of 76 is 35% of all engine time), fleet 283.5 / 4647.
- m400 t1 (428 bodies): frame p50 8.78 ms (view gather p50 6.43 ms = 64% of the frame; engine p50 0.414); overflow 394/1800 (22%); rtf lowest 1% = 0; first hitch >16.7 ms (1); player per-item 3.40 ms (823 ms / 242). Ship items get *cheaper* per item (105 µs) — the player's cost grows with N, ships don't.
- m400 t4 (threads 4): **digest identical to t1** (`3db02d3d61e77e6e…`); overflow *worse* (503), engine total +20% (3630 ms) — parallelism as wired does not relieve the budget constraint at this scale.
- rtf 1000 m48 (10 s): median rtf holds 1000, lowest 1% = 4.0, overflow 101/600 (17%) — the ceiling is not the mean (engine 115 ms/s vs 300 ms/s of budget) but the same burst items; several engine costs are per-*frame*, not per-game-second (player items and fleet slices per game-second fall ~4× from rtf 100 to rtf 1000), so rtf cannot be Fermi'd from mean demand.
- `xtask universe --kick-bench --seconds 30 --rtf 100`: 1158 distinct ship kicks, resolver median 76 µs / p99 407 µs; **exact memo hit rate 0.0** (1125 distinct shapes; the quantized 12+12 key hits 95.5% but is a law change) — confirms the 5 Oct finding on this commit.
- **Budget invariance:** `--engine-ms 0.5` (10× tighter, overflow 811/1800, presented tick 40% behind) gives the **identical digest** `41343a14…` as the 5.0 ms run — the budget changes when, never what, measured, not just claimed.
- **Slice invariance (the exploit's certificate):** with the fleet's slice halved (2^18 → 2^17 ticks, a one-line experiment, reverted after the run; `trace-rtf100-m48-slice17.json`), the digest is **identical** (`41343a14…`; 5846 slices instead of 4647, same bits). The battle slice is pure scheduling: the allocator may cut items to any quantum — deadline-sized slices, split handouts, chunked player work — without changing an outcome. (One halving is one point; a rung should sweep slice lengths across powers of two and member counts before freezing the change.)
**When the constraint moves:** once no item exceeds the budget (items split, allocator free to order them), the plane's frame-time constraint is the view gather — O(N) per frame at ~8.5 µs/body, i.e. 8.5 s per frame at 10⁶ emitters — and after that the goal's constraint returns to the board's known one: events per body per game-second times the per-event cost (the kick's rebind; exact memo hit 0%), the cadence and slack-skin levers already queued. The next run starts at the readout (b-readout-cost), not the engine.

## Predictions (predictions.md, written before these runs)

- P1 (tail is ≥50% player): **wrong** — the worst 5% of frames split roughly in thirds (ship 190.7, player 132.1, fleet 125.8 ms at m48), and the single worst frames are *fleet* items of 6–12 ms with 0–1 counted items (a whole battle slice inside one item).
- P2 (rtf 1000 median falls to 800–950): **wrong** — median held 1000; my Fermi assumed cost per game-second is constant in rtf, but player and fleet costs are per-frame, so demand per game-second *falls* with rtf. The dip is in the tail (lowest 1% = 4.0).
- P3 (m400: overflow ≥300, median rtf 20–80): **half right** — overflow 394 ✓, but median rtf held 100 (only the lowest 1% fell to 0). The budget defers and catches up; the mean hides it.
- P4 (threads 4 recovers, overflow ÷3): **wrong** — overflow 503 > 394, engine cost +20%. The digest is thread-invariant, but the wiring does not buy throughput here.
- P5 (player per-item cost flat in step length): **right** — 1.29 ms → 1.29 ms per item from rtf 100 to rtf 1000; the cost is per event (the clock law's step: readout + burn + rebind), and on top of it the O(N) scan adds ~6 µs/body. A late prediction, written into the run log before the slice run: the digest is slice-invariant — it is.

## What would make it wrong

The trace attributes cost by *kind*, not by event type (a kick, a boundary and a handout inside one ship-class item are not separated); if the 6–12 ms fleet items are not the battle slice but something else inside `resolve_fleet`, the exploit targets the wrong item — the code read (`universe.rs` `resolve_fleet` → `Fleet::advance(ctx, slice, limit)`, slice fixed at 2^18 ticks) says slice, and the 0-item frames are handout makes attributed to fleet cost. Linux/x86 shared cloud: orders of magnitude only; the integrator re-measures on the M1 (AGENTS.md). Threads-4 inflation may be contention on this shared runner, not a property of the design.

## Cost of adoption, and fit with PRINCIPLES

The exploit (slice sized to the deadline, or the battle advanced in smaller canonical quanta) is a scheduling change if the slice is not part of the law — the digest test above decides it for free. Fit: "The budget changes *when* work is done, never *what*" (plane.md foundation 7) — measured true; "Nothing takes an unbounded synchronous claim on the frame, whether a cycle compile, a rebinding burst, a decompression or a gather" (same) — measured false today: the battle slice and the player's step take exactly such claims, and the view gather is a per-frame O(N) claim. Principle 1 (less is more): the fix deletes the overflow tail rather than adding an allocator fast path. Principle 12 (smoothness): p99 frames are the budget cap itself; no allocator can beat an item bigger than the budget.

## The lens: what it may have missed

Goldratt looks at one constraint at a time, but the measurements show *two* per-frame structures trading places (view gather vs oversized items) as N grows; picking the wrong one first wastes a window. The lens also says "exploit before elevate", and the cheapest exploit here is negative (make items smaller, delete the tail) — but whether the *view* is in scope depends on Julien's visual layer decision, which a constraint lens cannot weigh. Gate adjudication (`behave --law plane` fails G1–G6 with `worst inf`/`unanswered` on this commit, B14 times out at 60.1 s) was set aside as off-lens; a judge run should look at whether that is a Linux artifact or a regression of the adapter, before anyone cites gate status from this machine.
