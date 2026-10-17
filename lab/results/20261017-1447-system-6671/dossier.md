# Dossier — 20261017-1447-system-6671 (system lens)

## Claim

The plane's source-read stream is one shared field evaluated per body: 64.5% of it is
bit-identical repetition — 169,145 of 262,198 `secondaries`-driven `state_of` calls repeat
an exact (source, tick) key, with **zero bit-conflicts in all 262,198 reads** — and the
non-repeating residue is the belt's kick comb itself (74% distinct ticks after the birth
wave), so the belt's read tax splits into a **free, bit-exact memo half** and a **structural
half whose cure is a representation change** (one canonical-tick field read per comb), not a
scheduling change. Together with the cited rebind share (68–85%) and the memory plateau it
names one component — the per-body tube — as the single payer of the belt's CPU crest, its
read stream and its memory wall.

## Bottleneck

The board's `read-stream`/`kick-cadence` axis at 10⁹ (the belt's two-comb stream, 10.3 M1
cores composed, 4e2d). Expected gain: the memo half is free (~1.7× ceiling on the N-linear
read stream's `secondaries` term, read-stream's own open ceiling); the structural half
points the 55-run cadence effort at the representation (one field pass per comb, BELT_SPLIT's
legality class) instead of at per-body scheduling. No new gate needed for the memo half.

## Evidence (all from this run's commands; see regen.sh)

Instrument: a print-only census on `Ctx::state_of` (`crates/universe/src/census.rs`, opt-in
`ES_CENSUS=1`), keyed by (call site, source j, tick t), counting calls, distinct keys,
bit-conflicts per repeated key, per-source tick spreads, and the sources' position drift
(f64 magnitudes, reporting only). Digest control: `ladder_digest "N=3000 coast through"`
prints the identical digest `d2632de90255f5c10de9fd7372a3790d` (kicks 34537, 4 schedules
agree) with the census off and on — the census writes nothing into the universe.

Flight: `nladder 10000 coast 60 600` (10,028 bodies, 35,386 game-s ≈ 1.26 belt intervals,
kicks 65,172, events 131,587, 0 frames over 12 ms; `census-n10000.txt`):

- **All reads:** 318,937 `state_of` calls = 2.42/event; site `secondaries` (ctx.rs:87):
  262,198 calls, 93,053 distinct (j,t) keys, **169,145 repeated (64.5%)**, conflict_frac
  **0.000000**, top key multiplicity 9,714.
- **The belt's birth wave is one field read done 29,142 times:** j0/j1/j2 at t=0, each read
  9,714 times (once per belt body, `project` at birth, step.rs:614→ctx.rs:87), all
  bit-identical. At 10⁹ that is 3×10⁹ identical evaluations at genesis.
- **The locals' doll batches naturally:** its source j3 is read 112,277 times at only 3,579
  distinct ticks — **96.8% repeated**, top 342× (its kicks sit on the doll's dyadic grid).
- **The belt's kick comb does not batch:** the root doll's three sources are read 49,973×3
  times; minus the t=0 birth key, 40,259 reads per source at 29,823 distinct ticks —
  **74% distinct** (read-stream's open question 1, answered for the belt: no shared-tick
  batching in the drain). Post-dossier, regen's own held-out arm N=3×10⁴: the structure is
  invariant — ex-birth 123,210 reads per source at 91,187 distinct ticks (26.0% repeated /
  74.0% distinct, the same split), birth top key 29,714×3 at t=0 (the whole belt), j3
  unchanged and N-independent (`census-n30000.txt`).
- **Conflicts = 0 everywhere** (P2): a per-(j,t) memo is bit-safe by measurement and by
  mechanism (bindings change only at the source's own events; items resolve in tick order).
- Drift across the flight (reporting only): j0 3.0e-2, j1 7.5e-3, j3 9.8e-2 relative — the
  field is smooth at comb scale (P3 held: a canonical-tick read is a bounded quantization).

## Predictions

`predictions.md` was written before the runs. **P1 was wrong in the belt's favour's
opposite:** I predicted < 5% exact collisions at the kick site; measured 64.5% repeated
overall, but decomposed — the belt comb is 74% distinct (as predicted) while the locals'
doll and the birth wave are the colliding mass. **P2 held** (0 conflicts).
**P3 held** (drift 6e-4–1e-1 relative, smooth). **P4 held** (`secondaries` = 82% of all
`state_of` calls; the remainder is the doll-centre read, site 2). **P5 held** (identical
digests). Held out for the checker: a burn flight and N=3×10⁴ (`census-n30000.txt` in
regen.sh).

## What would make it wrong, adoption cost, fit

- Wrong if: repeated keys ever conflict (a source's binding could change between two reads
  at the same tick — out-of-order resolution would do it; the queue's tick order and the
  measured 0 conflicts say no today); or if the census's per-call lock distorted delivery
  enough to change which kicks were delivered (digest control says the universe cannot
  move; the delivered-set itself is wall-dependent and was 0-frames-over-budget here).
- Adoption: the memo is a cache on `(j, t)` in `Ctx` (invalidated never, keyed on exact
  ticks; bounded by distinct ticks per window) — bit-exact by the measured 0-conflicts and
  the tick-order mechanism, ~64.5% of the secondaries read stream, digest-identical by
  construction. The structural half (one canonical-tick field per comb) is a law change in
  BELT_SPLIT's legality class (its B-gates are open, kick-cadence od1) — this run prices
  its ceiling, it does not fly it.
- Fit: PRINCIPLES 1 (the memo is compute not done) and 3 ("compute only surprises": the
  repeated reads carry zero information — literally the same bits); 19 (the comb's
  re-derivation per body is the wrong representation showing itself: "if you find yourself
  fixing things" — 55 cadence runs scheduling what is one shared evaluation).

## The unification (the lens's deliverable)

Three taxes, one payer. The belt body's per-body tube pays: (1) its share of one shared
drifting field, re-evaluated per body per kick (`secondaries` = 27% of kick wall, 620e;
64.5% of that stream now measured bit-identical); (2) a rebind per fired kick (68%, 620e;
84.6%, 96b4) to keep its own compiled cycle exact; (3) standing memory for that cycle
(4.85–5.06 kB/B plateau, b30b; the ladder wall = 6–8 GB ÷ plateau, e7ef). The combs are
phase-locked and metronomic (8ffc) — the signature of a dense-order region run through the
sparse order. The engine's own knob (engine.md rule 9) exists; its CPU arm just passed r5
(68e7); the plane never slides it for the belt. **One belt layer — one field pass per comb
at a canonical tick, members as compact-store records, one compiled cycle per cell — deletes
all three taxes at once.** The cheapest first step is the memo (free, bit-exact, measured
here); the layer is the named direction.

Blind spot (the case that breaks it): resonance cells and the belt's secular content — a
shared field pass does not rescue near-resonance structure (29/30 rows fail at any cadence,
kick-cadence), the synodic scatter (~146 bits/body, d0ea) must survive the layer, and the
frame's own refusals under thrust are measured (56cd). The layer deletes redundant shared
work, never the secular physics; near-resonance cells stay sparse.

## The lens

The whole-system lens made me look past kick cost and cadence (136 runs) at what the kick
*shares*; it may miss what the memo does to cache locality at 10⁹ (the census is at 10⁴,
one scene, one seed, coast — the held-out arms are the checker's), and the census's site
keying by (file, line) cannot separate `kick_clock` from `observe`'s mid-read where lines
collide by construction (they did not here: two sites only).
