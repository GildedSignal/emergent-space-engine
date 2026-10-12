Grade: silver

The plane's individual store holds 5,186 B/body (600 frames, 71 bodies; reproduced exactly, both dossier paths), 324× the law's 16-B Tube. Compiled trajectories are regenerable from the exact key — I recompiled all 50 Cycle entries (the census checked 8), bit-identically, ~32 µs each. Zero exact sharing holds at 200 members (208/208 distinct) and under Dense order. Steady state confirmed (bpb falls 5,697→4,786 over 300→1,800 frames). Verdict: the doc's "12–16 B individual" premise is wrong as written; the honest packet is ~240 B (Residual 64 + carry 16 verified in code), so individuals stay ≤ ~3×10⁷ — the price constant b-h-live needs. Not gold: the 26× deletion is asserted, not flown.

## Reasons

**Reproduction (exact).** `cargo test --release -p emergent-universe --test store_census -- --nocapture` (10.5 s cold, 0.24 s run) matches `census.txt` line for line: 5,186 B/body, 54/54 distinct entries, 663 cycles / 663 distinct exact keys (hit 0.000) / 45 quantized cells (hit 0.932), sizes BodyRec=448 Knot=88 Segment=192. `--example plane -- 100` → `bytes/body 2349`, 29 kicks — exact. The patch applies clean on `a838a284` and equals the saved test byte for byte.

**Pre-registration.** mtimes: predictions.md 03:22:48 → store_census.rs + census.txt 03:26:41 → dossier 03:27:55. Predictions preceded the decisive run. Misses are disclosed (P1 undershot 2.6×; `ext` on 12 not ≤ 3; `proper` half not all). H2 held; H1's "half-held" is generous — see the blind spot below.

**Adversarial cases (4, beyond the census).**
- *A1, consistent decomposition.* The dossier's table mixes denominators (catalogue-side per-alive ÷ plane-side per-body-over-71). Under the plane's own accounting (Σ bytes_of = 368,248 B): compiled trajectories **79.6%** (not 58%), retired Segment history **10.7%** (not ~29%), fat+plan 9.0%. The three-row split doesn't reconcile under any one denominator; the third row was a residual, not a measurement.
- *A2, the cache claim strengthened.* All 50 Cycle entries including dead bodies' recompile bit-identically from `Orbit::compile(key)`; ~32 µs each, so the eviction-recompile trade the dossier defers to b-readout-cost was cheap to bound and benign at this scale.
- *A3, growth.* 300/600/1,800 frames: 5,697/5,186/4,786 B/body; `catalogue_live` = n_bodies throughout; 71→76 bodies. No leak; the store improves with time.
- *A4, scale and regime.* Sparse/200 members: 208 bodies, 208 distinct entries (sharing stays zero), bpb 6,192 — worse, no scale rescue. Dense/48: bpb 5,204, same story.

**What the author missed — the biggest lump.** Dead bodies are charged "17 × 448 B" in the dossier. Measured: they retain their last compiled entries — 14 Cycle at ~9.3 KB plus 3 Passage — totalling **9,018 B per dead body, 41.6% of the store**. The census instrument never walked dead bodies, which is also why H1's gap needed excusing. The store's two true lumps are the regenerable cache (79.6%) and dead-and-retired weight (history 10.7% + dead shapes 38.8% of total shape bytes); "history ~29%" mislabels the second. The headline and the deletion *opportunity* are understated, not overstated.

**Honesty of the gauge.** `bytes_per_body` counts BodyRec + plan capacity + shape + segments but not Entry structs, deque headers or allocator slack — 5,186 is a lower bound. Direction of every claim is safe. Note also the headline number was one flag away (`--example plane` prints it); the contribution is the autopsy, the regenerability proof and the floor arithmetic, not the number.

**Novelty.** No prior census of the plane's store: H0209 priced the program side only ("488 B per 10⁶ convoy ships", design); components-98bc measured the belt (0.126 bits/body); r2 fixed widths, not records. representation.md §4 still says "Today's `Body` takes 88 bytes" (the lattice Body) and "12–16 bytes for an individual" — this run corrects both against measurement. Not a redo.

**Goal fit.** Board focus item "fitting 10⁹ in 8 GB"; P6 ("store the generator, not the generated" — the knots are the generated), P24/OC#34 ("why do you need so many bytes per entity?"), P1 (delete before optimizing). The 240-B scar price is the input the queued `b-h-live` and `b-readout-cost` runs need. Real and on-bottleneck.

**Why silver, not gold.** The 26× memory cut (cache eviction + SoA repack + freeing dead weight) is asserted from sizes, not flown — the author says so; and the central decomposition table needed checker correction (58/29 → 79.6/10.7 + a 41.6% dead lump the author under-priced 20×). Nothing was adopted. One named experiment converts it.

## The one experiment for gold

Fly the deletion behind the existing `BodyStore` seam: LRU-evict compiled entries (keep the exact key), free or shrink dead bodies' retained bindings, repack alive records SoA — then measure the flown bytes/body and the recompile cost on the real plane over ≥ 1,800 frames. Expected: ~200–300 B/alive-body at bounded recompile rate, converting the decomposition claim into a measured, adoptable component and settling the eviction trade b-readout-cost owns.

## What the author missed

1. The dead bodies' retained entries — 41.6% of the store at 9,018 B each — mispriced as 448 B each; the census never surveyed them (blind spot in the instrument, and the real content of H1's gap).
2. The 58%/29% split is mixed-denominator arithmetic; the consistent split (79.6% compiled, 10.7% history) is stronger for the claim and was left on the table.
3. `bytes_per_body` is a lower bound (Entry structs, deque headers, allocator slack uncounted) — the honest headline is worse, which would have helped.
4. The recompile cost (32 µs) was measurable in one line; deferring the eviction trade entirely to b-readout-cost gave up half the result.
5. P3's second half (`catalogue_live ≈ alive count`) missed (71 ≠ 54) and is not listed among the misses.
