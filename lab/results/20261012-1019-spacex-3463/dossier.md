# Dossier — spacex-3463: the plane's idiot index at scale

## Claim

On its own dashboard, the plane is readout-bound below ~500 bodies, budget-bound above
(overflow on 26% of frames at 480 members, 100% at 4,000), and its true marginal memory is
~330 kB per handed-out body and **growing with body count** — about 20,000× the 16-byte tube
contract, five orders of magnitude from 10⁹ in 8 GB — while the dashboard's `bytes_per_body`
under-reports it ~40× by charging compiled Passage tubes a flat 4 kB.

## Bottleneck

Board focus item 5 ("fitting 10⁹ in 8 GB") and the premise in focus item 1 ("kicks dominate the
engine's cost"). The idiot index says where the next 10× must come from: not the kick law
(its builds dominate the queue) but the **store and the readout**. Expected gain from acting on
it: memory 20,000× off its floor; readout is ≥ 65% of every frame below 500 bodies.

## Evidence (Linux/x86, shared 8-vCPU box, load ~2.9, unpaced, seed 1; orders of magnitude only)

One local edit lifts the harness's `--members` clamp from 400 to 400,000
(`xtask/src/universe/mod.rs:32`; the patch carries it) — the stock plane cannot even be asked
this question. Commands (each ≤ 55 s):

```
/usr/bin/time -v xtask universe --bench --rtf 100 --seconds S --unpaced --members N
# N ∈ {4, 48, 480, 4000} × S ∈ {1, 2, 4, 8}; data in data/bench-m*.json, data/time-m*.txt
```

| members | bodies | engine share | gather+json+wire | eng p99 ms | overflow frames | peak RSS |
|---|---|---|---|---|---|---|
| 4 | 32 | 0.11 | 0.89 | 0.44 | 0/480 | 31 MB |
| 48 | 71 | 0.25 | 0.75 | 1.8 | 3/480 | 31 MB |
| 480 | 406 | 0.32 | 0.68 | 5.6 | 125/480 | 49 MB |
| 4000, S=8 | 2296 | 0.11 | 0.86 | 52 | 479/480 | **845 MB** |

- **Per-item engine cost:** ship 73 µs at 48 members, 66 µs at 480 (flat), 185 µs at 4,000
  (3× growth under full backlog); fleet slice 7.7 ms per slice item at 4,000. Floor for the
  law's integer kick ≈ 50–100 ns → **idiot index ≈ 10³** on the kick, ~10⁴ on the slice.
- **Readout:** gather is 10–16 µs per emitter per presented frame at every scale (N=4: 0.69 ms
  for ~76 emitters; N=4,000: 65 ms for ~4,000 emitters) — linear, but at ~100–300× a read floor.
  Below ~500 bodies the readout is ≥ 65% of the frame; the player's frame pays it every wall
  frame regardless of game events (principle 3 violated by the view, not the law).
- **Memory:** construction at 4,000 members is 5.6 MB; the growth is the run. 1 game-second →
  268 MB; 8 → 845 MB, with 2,268 bodies live. Marginal ≈ 270–500 kB per handed-out body early,
  and the in-crate probe (patch) shows the per-handout cost **rising with body count**: ~17 kB
  per handout at #0–500, ~430 kB–1.2 MB per handout at #3,600+ (`PROBE handout` lines in the
  patch's stderr). Superlinear per-body cost: at 10⁹-shaped growth this is the wall before any
  physics.
- **The instrument lies:** `bytes_per_body` reports 8.2 kB at 2,296 bodies (real marginal
  ~330 kB avg): `body.rs:170` counts Cycle knots exactly but charges `Passage(_) => 4096` flat,
  while a Passage holds an `Arc<OrbitShape>` knot table plus a tail of `(Scalar, Integral)`
  panels that shrink x by 15/16 to the endpoint (`orbit.rs:910–978`) — deep-well leavers (most
  of a battle's handouts) are exactly the big ones.
- **Service level:** frame p50 = 59.9 ms at 4,000 members (target 16.7); rtf overflow on every
  frame. At the plane's own clamp (400) it still overflows 26% of frames at rtf 100.

Controls: N=4 negative (engine 0.11 share, engine p99 0.44 ms — the instrument reports no
engine cost where there is none); positive — engine max exceeds the 5 ms budget at every N ≥ 48
and overflow counts rise exactly where demand crosses the budget; digest reproducibility is the
harness's own (deterministic cuts, `digest` field present in every JSON).

## Predictions (predictions.md, written before the ladder; only N=48 seen)

1. Readout ≥ 45% at 480 and 4,000, engine ≤ 40% — **held** (0.68 / 0.86 vs 0.32 / 0.11).
2. Budget crossing between 480 and 48,000 — **crossed earlier than predicted**: 26% overflow
   already at 480 (the bracket was right in direction, loose below).
3. Marginal memory ≥ 64 B/member — **held and blown through by 3 orders** (~10⁵ B; predicted
   class 10²): I under-called it; the acceleration with N was not predicted at all.
4. `bytes_per_body` ≥ 2 kB at every N — held (2.4→8.2 kB, growing).
5. Ship µs/item flat in N — held to 480 (66–73 µs), 3× growth at 4,000 under backlog.

## What would make it wrong

The shares are of the frame's measured parts on one thread of a shared x86 box; the M1's
absolute numbers will differ (integrator re-measures), but the ratios (per-item cost, per-body
bytes, readout-vs-engine share) are structural. The memory attribution stops at "per-handout,
superlinear": the acceleration (Vec reallocation transients vs per-body O(N) work in
`requeue`/`pull`) is **not yet attributed** — a heap profile must confirm before anyone deletes.
If the acceleration is realloc transients, steady-state marginal cost is the early ~17–50 kB,
and the index drops to ~10³ (still 1,000× off the contract). N=40,000 was not run (it would
exceed the 2 GB process cap by linear extrapolation — itself a datum: the plane cannot be
constructed at 4×10⁴ members on this box).

## Cost of adoption, fit with PRINCIPLES

Fix `bytes_of` (charge the Passage's real knots+tail) — one afternoon, no law change; lift or
parameterise the members clamp so scale questions are askable; attribute the superlinear
per-handout cost before the memory design (B18b, shipmem) is judged. This is the lens's
"question the requirement, delete, then accelerate": the queue holds six kick-law builds while
the measured worst ratios sit in the store (2×10⁴) and the readout (~10²–10³) — "The cheapest
compute is compute not done" (principle 1) and "we need to be deeply aware of von-neumann
bottleneck and memory" (17). Nothing here weakens a gate; B18b/B15 unaffected.

## The lens

SpaceX's delete-first eye sees law builds where the idiot index points at plumbing; it may
under-weight that the kick law's cost is *game-visible* physics while the readout is a debug
view (docs/plane.md: "for now this is physics, not visuals") — the integrator may rightly keep
the kick builds first. The 60 s test bound also bit: no heap profile, no N=40,000 confirmation.

## Files

`data/bench-m{4,48,480,400,4000}.json`, `data/time-m*.txt` (peak RSS), `predictions.md`,
the tree patch (clamp lift + RSS probe in `resolve_handout`).
