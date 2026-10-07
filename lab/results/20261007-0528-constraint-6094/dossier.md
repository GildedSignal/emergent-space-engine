# Dossier — the constraint, measured on the whole plane

## Claim

On the flying plane, the frame's constraint is not the engine's kicks but the **view gather**: an unbudgeted, synchronous, linear-per-visible-entry re-derivation that already holds 69% of the median frame at play settings and breaks the 16.7 ms frame at 3,770 visible entries, while only 4.7–8.2% of its output changes beyond perceptible quanta between frames — so the first 10× is deletion (surprise-gated reuse), not faster readouts.

## Bottleneck

The board's live list is engine-side (kicks, changeover, encounters, tide, shipmem, candidates). Measured on the whole (`universe --bench`, the play mode: paced, rtf 100), the frame is: **view_gather 69.4%**, engine 17.5% (median demand 0.05–0.24 ms against its 5 ms budget), json 9.2%, wire 3.8%. The engine is budgeted and mostly idle; the gather is neither budgeted nor amortized, although plane.md foundation 7 already forbids exactly that ("Nothing takes an unbounded synchronous claim on the frame, whether a cycle compile, a rebinding burst, a decompression or **a gather**"). The code implements the budget for the engine only (`session.rs`: `frame_to(..., Budget::wall(engine_ms))`, then `gather_cached` with no budget).

Expected gain: the gather's work is >90% re-derivation of unchanged view state; a surprise gate deletes ~92–95% of it at the same observable output (the perceptible quanta are the instrument's: 1 px, 1/255, 1% luminosity). That is ~10× on the largest claim of the median frame, and it is what lets the visible-entry count grow ~10× at constant frame cost. What it deletes: most per-frame tube readouts (the gather is ~1 readout per entry at ~11 µs — readouts are ~100% of it) and, subordinated, most of the JSON/wire payload (deltas).

## Evidence

All commands ≤ 60 s except `behave` (99 s; noted). Machine: GitHub Actions Linux x86, 8 vCPU, shared, load recorded in the JSONs; orders of magnitude only, the M1 re-measures.

1. **The whole, play mode** (`/home/glmlab/lab-target-2/release/xtask universe --bench --seconds 30 --rtf 100`; `bench-rtf100.json`): frame p50 4.37 ms / p99 10.70 ms, zero hitches > 16.7 ms; `where_the_time_goes_ms` shares: gather 0.694, engine 0.175, json 0.092, wire 0.038; engine p99 5.24 ms with 45/1800 overflow frames (its 5 ms budget bites on the tail; overflow is a smooth rtf dip by design).
2. **Engine demand, budget lifted** (`--seconds 20 --rtf 100 --unpaced --engine-ms 1000`; `bench-unbudgeted.json`): engine p50 0.047 ms, p99 1.30 ms; gather p50 0.724 ms — the engine's median demand is 5–15× below the gather's. The gather's *share* (67%) is the same paced or unpaced; paced absolutes are ~4.8× higher (frequency/cache reality of 60 Hz play — the paced numbers are the honest ones).
3. **Gather decomposition and scaling** (`gatherbench/`, standalone bin on the same `frame_to` loop and scenario; `metrics.json`): entries → gather p50: 64 → 0.74 ms; 328 → 3.0 ms; 3,770 → **27.8 ms** (linear, 7.2 µs/entry; max RSS 202 MB). Readouts per gather ≈ entries (median 70/287/2537): the Crossing memo does hold Newton to ~1 readout per entry, and readouts are the whole cost (2,537 × ~10.9 µs ≈ 27.7 of 27.8 ms). A direct `state_rate` readout: 11.5 µs median.
4. **The view's surprise rate** (same bench, quanta fixed in `predictions.md` before the run): 4.7% of entries at members 48, 8.2% at 400, 7.5% at 4000 change beyond perceptible quanta per frame. The gather re-derives >90% unchanged information every frame.
5. **Context, not the constraint:** kick-bench (`kickbench.txt`): 35 µs median per distinct pending kick, exact memo hit 0% / quantized 94.5% (known). Gates on Linux: G1–G6, B7, B9–B12 return no oracle answers (worst inf, "unanswered"); B13 60/64 matches the M1 record; B14 times out. This machine cannot judge law gates — cost and scale numbers only.

## Predictions

All four held (`predictions.md` written before the decomposition run): (1) readouts > 60% of the gather — measured ~100%; (2) linear fleet-path slope — measured 7.2 µs/entry (members that are handed out become doll bodies, so the Newton path itself scales); (3) surprise < 5% — measured 4.7% at members 48 (barely; it rises to ~8% at scale, still >90% unchanged); (4) engine median demand below the gather's — measured 5–15× below. No kill criterion triggered.

## What would make it wrong

- The perceptible quanta are mine (1 px at 1080p, 1/255, 1%). A player-facing view that needs finer quanta (smooth apparent motion of near bodies, precise dials) shrinks the deletable fraction; the near field (the few entries that do change) is exactly the player's own surroundings — the gate must be per-entry, never global.
- If the debug view is replaced by per-pixel gathering (the galaxy plan) before the plane grows, the per-entry path never reaches the scale where it binds, and the constraint moves straight to the engine's kick tail (p99 5.24 ms at the budget, 45 overflow frames per 30 s) and to readout cost.
- Cloud caveat: 7.2 µs/entry is x86; the M1 re-measures. The shares, the linearity and the surprise rate are representation facts, not timings.
- The JSON/wire shares (13%) are the debug instrument's, not the engine's; if they stay per-entry they become the next constraint at the same scale (subordinated: delta protocol).

## Cost of adoption, fit with PRINCIPLES

Adoption is one seam: the gather emits entries gated by their own surprise (recompute when the crossing's Newton slope says the entry could cross a quantum, else re-emit), plus a gather budget like the engine's. No law, gate or digest changes — the view is already a pure read ("Observation is a pure function of the state: the gather reads, never writes", plane.md foundation 5), and the code already blesses view memos ("any cache, however stale or foreign, gives the same view", `view.rs`). It is principle 3 applied to the last unbudgeted claim: "Nothing is evolved that can be derived when looked at (clocks, redshift, **views**)" — and principle 1, "the cheapest compute is compute not done." The risk to watch: the gate must never let the *displayed* view lag a real change (the stale-heading trap of the first flight, HANDOFF); the quantum is the instrument's, per principle 28 ("the view is an instrument").

## The lens

Goldratt's lens measures the whole and names one constraint; it can miss what the constraint *should* be at the goal's scale rather than the plane's. At billions of bodies the gather must be per-pixel/hierarchical regardless, so this finding's real content is: (a) the plane's frame is view-bound today, not kick-bound; (b) the surprise rate of the view is ~5–8% per frame — the number any view representation must beat; (c) foundation 7's "no unbudgeted gather" is unimplemented. A time-boxed lens also stops before building: the surprise gate itself is unbuilt (one experiment away: wire it, gate on Newton-slope bounds, measure the frame at members 4000 — that is the gold run).
