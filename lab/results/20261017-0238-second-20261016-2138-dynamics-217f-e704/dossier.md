# Dossier — 20261017-0238-second-20261016-2138-dynamics-217f-e704 (second author)

## Claim

The checker's named gold experiment is flown and it decides **against the fix**: at scale the
rollback ratchet's tax is not a number, it is two failure modes — the shipped ratchet latches
at E = 2^(conflicts before quench), which **grows with the conflict wave** (measured frozen at
E = 4 → 32 → 64–128 → 256 for 44 → 88 → 1,408 → 14,080 bodies) and merges the whole scene
into one region at 10⁴ bodies (throughput ~82 chronons/s), while the ES_DECAY mirror that
restores the equilibrium **falls into a livelock basin** (first `run_to(3000)` never returns,
8 workers at 100% CPU — DNF in 5 of 9 narrow-margin runs at 1,408 bodies across all flights
(decay 2/5, ES_LOCAL 3/4; one more ES_LOCAL run ground through 185 rollbacks / 4.1M wasted
ops / 20 s against 7–8 rollbacks clean), and both arms DNF > 240 s at 14,080 bodies where
shipped finishes in 74 s) — so neither the ratchet nor its
10-line mirror is adoptable at scale, and the controller needs a **bound** (capped
escalation, or margin from the law at genesis), which is the named next experiment.

## Bottleneck

Principle 12's own object (the allocator) and principle 25 (never trade ruin for an average
gain): the original run priced the ratchet's standing tax at 44 bodies and the checker found
it law-confounded and player-invisible; the open question was whether any tax survives at
≥10⁴ bodies. Answer: the tax does not survive — its place is taken by the latch's scale
coupling and the mirror's livelock. Gain: kills the adoption of the 10-line mirror at scale
(adopting it would have introduced an unbounded tail), and pins the next representation fix.

## Evidence

All numbers from the shipped `crates/allocator` plus my patch (`work/patch.diff`: the `tax`
example — the original run's Newtonian battery parameterised in cells, public API only,
`run_to`/`run_frames`/`Report` — the original's `ES_DECAY` arm verbatim in semantics, and the
new `ES_LOCAL` arm: per-region escalation, rollback doubles only the clashing lineages,
same-grid halving; both default-off; all 14 shipped allocator tests pass with arms off).
Scene family: per=8 clusters, 8,000-unit spacing, stagger 30 (ignitions every 30 chronons);
1280 cells = 14,080 bodies, 2,560 initial regions. Seed 1 throughout. Shared box, load
1.6–3.1; arms interleaved where compared; wall rows are order-of-magnitude only.

| scene (batch) | arm | wall | rollbacks | E end | regions end | merges/splits | avoided | wasted | chronons/s |
|---|---|---|---|---|---|---|---|---|---|
| 4 cells, 34k chr (3 reps) | shipped | 0.3 s | **3 / 0 / 1** | **8 / 1 / 2** | 13/38/38 | — | — | — | — |
| 8 cells, 16k chr | shipped | 0.4 s | 5 | 32 | **1** | — | — | — | 37,000 |
| 128 cells, 20k chr | shipped | 10.6–11.9 s | 6–7 | 64–128 | **1** | 123/0 | 32 | 122–763k | 1,675–1,890 |
| 128 cells, 20k chr | decay | 15.7 s | 7 | 1.0 | 1,247 | 398/1,594 | 4,614 | 84k | 1,279 |
| 128 cells, 20k chr | local | 14.9 s | 7 | 1.0 | 1,247 | 399/1,508 | 4,690 | 94k | 1,342 |
| 128 cells, 6k chr, 3 tries | decay | **DNF(60 s)**, 6.0 s, 5.3 s | —/9/7 | 1.0 | — | — | — | — | — |
| 128 cells, first `run_to` | local | **3 of 4 tries never return** | — | — | — | — | — | — | — |
| 1,280 cells, 6k chr | shipped | **74 s** | 8 | **256** | **1** | 1,186/60 | 609 | 1.79M | **82** |
| 1,280 cells, 6k chr | decay | **DNF(240 s)** | — | — | — | — | — | — | — |
| 1,280 cells, 6k chr | local | **DNF(240 s)** | — | — | — | — | — | — | — |

- **The latch level scales** (P1 held): E frozen at 2^(#conflicts before the global quench);
  the conflict wave grows with cells, so the permanent margin grows with scene size: 4 → 32 →
  64–128 → 256 across 44 → 14,080 bodies. The ratchet is not a constant tax, it is a
  scale-coupled one — the original's "frozen at ×4" was the smallest sample of the family.
- **The livelock is real, recurring, and belongs to the narrow-margin regime** (P2's mirror
  half inverted): with E re-narrowed, ignitions every 30 chronons keep breaking promises;
  at 1,408 bodies the allocator wedges — all 8 worker threads burn CPU (utime 800–980 ticks
  each, one in R state), the frame of reference: shipped at margin 0.5 / 1.0 / 2.0 **never**
  wedged (3.3–3.6 s; 25/12/8 rollbacks — the ratchet latches higher and absorbs the
  recurrence). The ratchet's permanence is what prevents the livelock; the mirror's
  equilibrium sits inside it.
- **Certificate** (P4 held wherever an arm finishes): outcome digests bit-identical across
  all three arms and all reps at 4, 8 and 128 cells (`d75dee4a…`/`42e4e3b4…` at 128;
  `cac731da…` at 8). At 1,280 cells only shipped finishes, so identity is unverified there.
- **Frames** (P3, honest nil at this size): 128 cells, 60 Hz, rate 600, 3 interleaved reps ×
  3 arms — present rate 575–585 vs target 600 everywhere, deadline misses 3–5 per run in
  every arm: **no player-visible separation at 1,408 bodies**, matching the checker's
  44-body finding. At 14,080 bodies the player-visible surface is the batch collapse itself
  (82 chronons/s < any playable rate), not per-frame misses.
- **ES_LOCAL** (P5 half-held): far regions keep escalation ~1 and its clean runs match the
  decay arm's counters almost exactly (4,690 vs 4,614 avoided) — but locality does not buy
  safety: it wedged 3/4 at 1,408 bodies, and its one grinding run paid 185 rollbacks
  (vs 7–8 for both other arms): per-lineage doublings decay at the next sync grid before
  the quench can globalise, so conflicts persist 20× longer. The wrong locality of the
  doubling is not the binding problem; the absence of a bound and of a persistent quench is.

## Predictions

`predictions.md` was written before any arm comparison. Held: P1 (latch grows with scale —
stronger than predicted), P4 (digests identical where arms finish), P5's counter half
(local ≈ decay when it finishes). Inverted and reported as such: P2 — the avoided-merge tax
does not separate shipped-from-decay in the predicted direction at scale (decay pays MORE
avoided merges, 4,614 vs 32, because late narrow-margin plans get undone more), and the
decay arm's rollback cost is not a 3× counter, it is a livelock; P6 — the collapse branch
happened (regions → 1 at ≥8 cells), though at 1,280 cells the sweep lights physically couple
the row, so how much of that collapse is forecast-forced versus physical is not separated by
this experiment (named below). P3's nil branch is the honest outcome at 1,408 bodies.

## What would make it wrong

- The 1,280-cell collapse attribution: the battery's lights sweep the whole row by
  construction, so one region is partly the physics, not the margin; a scene with
  non-sweeping conflicts (e.g. ignition without cluster crossing) would separate the two.
- The wedge is timing-nondeterministic: frequencies here are 3-try samples; the 1,280-cell
  DNFs could be extreme slowness rather than never (no run was allowed past 240 s). The
  mechanism (narrow margin + recurring conflicts + many regions) is consistent across all
  observations, but I did not open the allocator's loop to name the exact cycle.
- The relativistic 14,080-body control produced no RESULT in 100 s (wedge or slowness
  unresolved), so the no-conflict throughput ceiling of that geometry is unmeasured.
- One seed, one layout per size; the shared box's load moved wall rows (interleaving
  mitigates, does not remove).

## Cost of adopting, fit with PRINCIPLES

Adopting the 10-line mirror on this evidence would be ruin (principle 25: "not making
mistakes matters more than doing things efficiently, don't multiply by zero"). The evidence
supports instead: **cap the escalation** (`escalation *= 2` then `min(cap)` — one line, keeps
the quench, bounds the fan and the collapse coupling; untested here, the named next
experiment), and for relativistic scenes derive the margin from the law at genesis (wiki
open direction 3) where the c-cap makes conflicts a one-stride window. "Errors never
compound" cuts both ways: the margin compounds with the wave (shipped), and the conflicts
compound into a livelock (mirror); neither half is a controller.

## The lens

As the second author I inherited the scene family and flew it bigger, not differently: the
sweep-coupling confound at 1,280 cells and the unopened livelock cycle are what this lens
skipped. A red-team should attack the collapse attribution first, then the wedge mechanism
(a core dump or an instrumented build naming the spinning loop).

## Commands

`regen.sh` regenerates every table row (≤ 14 min; DNF rows re-verify as timeouts). Raw logs:
`batch-128.log` (interleaved 3-arm record incl. the DNF rows), `wedge.log`, `frames-128.log`, `relativistic.log`, `probe.log`; single
runs: `cargo run -p emergent-allocator --release --offline --example tax -- batch <cells> 8
30 <stages> <step> 1` with `ES_DECAY=1` / `ES_LOCAL=1` / `TAX_MARGIN=<m>` / `TAX_LAW=relativistic`.
