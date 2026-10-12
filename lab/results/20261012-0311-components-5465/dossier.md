# Dossier — the individual body's store on the plane (components lens)

## Claim

The plane stores one doll body in **5,186 bytes** (measured, its own `bytes_per_body`, 600 frames,
663 kicks) — **324× the law's own 16-byte `Tube`** and ~22× an honest ~240-B packet — and the bulk
is two things that are not state at all: compiled orbit **knots (58%, proven regenerable
bit-identically from the exact key, i.e. a cache)** and **the view's retired history (~29%)**;
the law's own exactness (`Residual` 64 B + sigma-delta carry 16 B) makes representation.md §4's
"12–16 bytes for an individual" **unreachable as written**.

## Bottleneck

Bottleneck 5 (units, widths, memory: one question) and the risk "fitting 10⁹ in 8 GB". Expected
gain: ~26× memory cut per individual with **no law change** (cache eviction + SoA repack are
bit-identical), and it deletes the premise that the packet floor is 12–16 B. What it deletes:
per-body compiled knots (an evictable cache), the fat `BodyRec` (448 B), dead bodies never freed
(17 × 448 B here), the `Vec<Item>` plan (always ≤ 2 items on the plane).

## Evidence

`cargo test --release -p emergent-universe --test store_census -- --nocapture` (12 s cold, 0.25 s
run; test copied to this folder as `store_census.rs`, output in `census.txt`). Independent second
path: `cargo run --release -p emergent-universe --example plane -- 100` → `bytes/body 2349` at 29
kicks (the number grows with kick history). 600 frames, 71 bodies, 54 alive (49 ships, 3 planets,
1 moon, 1 player), 17 dead still stored. Decomposition per **alive** body:

| Term | Bytes | Nature |
|---|---|---|
| compiled entry (mean 22.5 knots × 88 B, max 130) | 3,028 | **cache**: `Orbit::compile(key)` reproduces knots+crossings bit-identically (8/8 checked, asserted) |
| fat `BodyRec` + binding-beyond-tube + plan | ~634 | record waste; `Binding`=176 of which `Tube`=16, `Residual`=64 (law), turn/kick/units/epoch ~80 |
| history `Segment`s (192 B each) + dead recs | ~1,524 | the view's past (prune bounded, `catalogue_live` 71 = 54 live + 17 history-held: slots recycle, no leak) |

Sharing: **zero** — 54 distinct `Arc<Entry>` for 54 alive bodies; 663 distinct kicks → 663
distinct exact keys (hit 0.000), reproducing `tests/memo.rs`; the law's 44-bit quantized cell hits
93.2% (45 cells). Usage: carry nonzero 25/49 ships, `ext` 12 bodies (root doll), thrust 1
(player), plan length ∈ {1,2} for all bodies.

Floor arithmetic: honest packet ≈ tube 16 + exact key 24 + residual 64 (law.md: "the remainder is
carried and never dropped") + carry 16 + turn/kick/units/epoch/grid ~72 + inline plan 32 ≈
**240 B**; 5,186/240 ≈ 22×; 5,186/16 = 324×. Scale: 10⁹ × 240 B = 240 GB ≫ 8 GB ⇒ **individuals
must be a minority (≤ ~3×10⁷)**; the population program (B18 ladder, 0.126 bits/body) carries the
rest, and each scar costs ≈ 240 B of packet — the price constant the queued `b-h-live` run needs.

## Predictions

`predictions.md` was written before the run. Held: zero exact sharing (54/54, hit 0.000), quantized
hit 0.932 < 250 cells, Knot 88 B / Scalar 16 B / BodyRec 448 B ≥ 120, plan ≤ 2, index ≥ 25×,
carry ~half, thrust = 1. Missed: **P1 undershot 2.6×** (predicted 300–2,000 B; actual 5,186 —
history segments and never-freed dead bodies surprised me); `ext` on 12 bodies not ≤ 3 (every
root-doll body anything can kick carries it); `proper` nonzero on half, not all. H1 half-held: the
gap between my census sum (2,785) and the official 5,186 is history + dead records, not
double-counted sharing. H2 held: slots recycle, no unbounded catalogue growth in 600 frames.

## What would make it wrong

- If the view must read every body every frame, entry eviction converts memory into recompiles;
  that trade is owned by the queued `b-readout-cost` run, not measured here. (Counter: the screen
  caps samples at pixels; visible bodies ≈ 10⁶ at most.)
- The 240-B packet assumes the residual and carry must be carried per body. If they can be
  re-derived at events, the packet drops toward the doc's 12–16 B — a law question (r2-style width
  rung on the residual), not mine to assume in either direction.
- 54 bodies is not belt scale: distinct quantized cells (45 here) may grow with N; exact sharing
  stays 0 at any scale by construction (a kick moves exact (E, L) by an integer).
- Adoption cost: a packed SoA store behind the existing `BodyStore` seam (built for exactly this:
  "PlainBodies … population programs implement the same four calls later, with no rewiring") plus
  an LRU on the catalogue. One step; digest untouched (regeneration is deterministic).

## Fit with PRINCIPLES

- **P6** "Store the generator, not the generated": the knots are the generated; the exact key is
  the generator — 58% of the store is regenerable from 16+24 bytes.
- **P24 / OC#34** "The memory floor is information… why do you need so many bytes per entity?":
  the floor here is law-owned exactness (80 B of residual+carry), not the 3 KB cache.
- **P1** "The cheapest compute is compute not done. Delete before optimizing": the deletion list
  (cache, fat record, dead bodies, Vec plan) is 22× before any cleverness.
- **P21** rough first: measured on the real plane, not a mock.

## The lens

A single component, measured hot: this misses the fleet battle store (`lattice`'s 88-B `Body`,
a different component), belt-scale catalogues, and it asserts the SoA repack from sizes without
building it — the 22× is a decomposition claim, not a flown store. The doc correction it implies
(representation.md §4's "Today's `Body` takes 88 bytes" is the lattice Body, not the plane's
5,186-B stack; "12–16 B individual" ignores the law's own 80 B of exactness) is stated here, not
patched: results live only in this folder.
