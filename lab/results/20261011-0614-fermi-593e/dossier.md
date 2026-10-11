# Dossier — the 10⁹ budget priced in one law, with the engine measured

Run: 20261011-0614-fermi-593e (lens: Fermi). Box: GitHub Actions Linux, 8 vCPU x86, load 0.10–0.40 (quiet), uptime 44 d. Timings are orders of magnitude only (Linux/x86; the integrator re-measures on the M1).

## Claim

At 10⁹ bodies the M1's walls are, in order: **the per-event cost of the kick path (measured 18–69 µs today; ~0.2 µs at a memo hit — a 150–350× lever, not the board's 10–100×)**, then **the view at 10⁹-in-view (measured 25–37 ms/frame, ~2× over the 60 Hz budget)**, then **memory as un-reabsorbed scars (budget ≈ 1 per body per session)**; cold orbital compute for 10⁹ is 2+ orders inside budget, and the board's "190 cores" is not an engine property but one scene (hour-period bodies, 32 kicks/orbit, rtf 1, 30 µs/kick) — re-derived to 178 cores, and 1.2% of one M1 under the law's own averaging plus a memo hit.

## Bottleneck

Board #3 ("Cost at a billion") and the H_live risk line: which term breaks first at 10⁹, and by how much. Everything reduces to one law (units checked):

```
events/wall-second = N · e · R / P        cores = N · e · (R/P) · t_event
```

(N bodies, e events per orbit, R = rtf, P orbital period in simulated seconds, t_event the per-event cost.) The M1's event ceiling is compute-bound at 4·P-cores/t_event: 1.3×10⁵ events/s at today's 30 µs, 2×10⁷/s at 0.2 µs. Bandwidth (60 GB/s ÷ ~96 B touched) only becomes the wall below ~64 ns/event — the hardware floor of an event.

## Evidence (exact commands, each ≤ 60 s, from the repo root with `cargo build --release -p xtask`; binary at `$CARGO_TARGET_DIR/release/xtask`)

1. **The plane today** — `xtask universe --bench --rtf 100 --seconds 15 --unpaced` →
   71 bodies, 368 events/s, frame CPU p50 0.94 ms, engine share 22% / view gather 66%;
   per resolved item: **ship 69 µs, fleet 18–25 µs**, player 352 µs; **bytes/body 5,044**.
   Repeat with `--members 4096` → 417 bodies, 1,745 events/s, ship 60 µs, fleet 25 µs, bytes/body 6,227: per-item cost stable across 6× scene growth (extrapolation defensible within 2×). Files: `plane-bench.json`, `plane-bench-m4096.json`.
2. **10⁹ ships, whole scene** — `xtask galaxy --bench --ships 1e9 --tubes 1e6` →
   build 0.43 s (**2.3×10⁹ ships/s instantiation**), 10⁶ tubes + 9,990 families, 13,963 compiles, memo hit 0.987, **peak RSS 106 MB (0.85 bit/ship; 247 MB with render = 2.0 b/ship)**, density view with 10⁹ ships in view: **25.8–37.2 ms/frame median on 3.9 cores** (0.03–0.06 ns per ship in view). Files: `galaxy-bench.json`.
3. **The budget table** — `python3 lab/results/20261011-0614-fermi-593e/budget.py` (output `budget-out.txt`). Key rows, N = 10⁹:
   - belt (P = 5.2 yr, e = 1.4, rtf 100): 875 events/s → **0.026 cores today**, 0.0002 at 0.2 µs. Cold orbital compute is 2–5 OoM inside budget.
   - all bodies in hour orbits (P = 5.4×10³ s, e = 1.4, rtf 100): **778 cores today → 5.2 cores at 0.2 µs** (borderline = the M1's honest ceiling).
   - the board's scene (e = 32, rtf 1, 30 µs): **178 cores ≈ "about 190 cores"**; with averaging + memo hit: 1.2% of one M1.
   - hot-body count (the approved plan's "measured limit for independently active ships", here estimated): a hot body (hour orbit, rtf 100, e = 1.4) draws 0.026 events/s → **5×10⁶ hot bodies today; 8×10⁸ at memo-hit cost**.
   - memory: state budget 34 bits/ship; programs measured 0.85–2.0 b (2.5–6%); scars get ≤33 b → **~1 un-reabsorbed 32-bit scar per body per session** (4 at 8 b). Belt orbit = 444 wall-hours at rtf 100, so even all-bodies-scar-every-orbit lasts 423 wall-hours; 3% scarring lasts 588 wall-days. Memory binds through *battles and chaos that never reabsorb*, not through belt orbits.

## Predictions (predictions.md, written before the runs)

- **Held:** galaxy 10⁹ < 60 s, < 1 GB, ≥ 10⁷ ships/s, compiles < 10⁵ (0.43 s, 106 MB, 2.3×10⁹/s, 1.4×10⁴). Per-item cost 1–100 µs for ships/fleets (18–69 µs). Belt compute ≤ 10⁻² utilization (0.7%). The 190-cores headline re-derives from rtf 1 + hour orbits + 30 µs kicks (178 vs 190, 7% off).
- **Missed, reported:** bytes/body predicted 40–600 B, measured **5,044–6,227 B** (the first flight is ~150–400× above the 34 b/ship envelope; shipmem is not wired into the plane). events/s predicted ≥ 5×10², measured 368 (1.4× below my band — the default scene is quieter than I guessed). Player items 352 µs exceed my band (thrust/handoff resolutions, 1 body only).

## What would make it wrong

- t_event was measured on x86 at load 0.1; the M1 re-measure can move it ×2 either way, not ×10 — the ranking of walls survives.
- The 4 GiB state budget is the approved plan's, not Julien's final word; at 6 GiB the scar budget triples, at 2 GiB it halves.
- `bytes_per_body` may count catalogue slack that does not scale linearly; the 10⁹-scene RSS (0.85–2 b/ship) is the trustworthy memory number.
- The hot-body estimate assumes kicks dominate an active body's events; a battle's contact epochs could double the draw (a factor 2, not an order).

## Cost of adopting, and fit with PRINCIPLES

Adoption is a re-ranking, not code: the queue's order for "cost at a billion" becomes (1) the kick path's memo (Sonnet already wires it; this prices it at **150–350× at 10⁹, larger than the board's stated 10–100× need**), (2) the readout's cost at 10⁹-in-view (b-readout-cost, already queued), (3) H_live's reabsorption fraction (b-h-live, already queued — this dossier gives it the ceiling to compare against: ≤ ~1 un-reabsorbed scar per body per session). Fits principle 1 ("the cheapest compute is compute not done" — cold belts are already free), principle 3 ("compute only surprises" — the event rate, not the body count, is the cost), and principle 27 (the goal, not a proxy: rtf and P are the player's scene choices, t_event is ours).

## The lens

Fermi hides dynamics in averages: the tail regimes (resonant chaos, fleet concentrations — the co-orbital gold of 6 October) do not enter N·e·R/P until they blow e or the candidate work; that risk (q-candidate-degree) is untouched here and could sit below the kick-path wall. The 60-minute budget also left the E-core/GPU split unexamined: the 2×10⁷ events/s ceiling is CPU-only; the GPU dense order changes the ceiling, not the law.
