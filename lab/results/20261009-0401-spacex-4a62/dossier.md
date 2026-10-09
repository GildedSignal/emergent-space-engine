# Dossier — H_live on the flying plane: the memory law is standing representation, not distinction rate

## Claim

On the plane, distinction *creation* is reabsorbed (net memory growth zero at steady state, retention ≤ 11 segments per body), but a median ship **stands at ~1.46 KB — 90× the law's 16-byte tube** — so 10⁹ bodies cost ~1.4 TB, **175× the 8 GB budget**; the multiplier is the per-body resident compiled trajectory (~530–970 B of quadrature knots) plus a 448 B `BodyRec`, and fitting 10⁹ needs evictable shared shapes and out-of-line records, not a better prune.

## Bottleneck

Board risk "Distinctions created per game-second (H_live): they, not the body count, decide whether 10⁹ fit in 8 GB; **not measured yet**" (HANDOFF, risks; plane.md §36). This run measures it for the first time. Outcome: the *rate* side is harmless at the plane's cadences (2.8 events/s universe-wide; median ship 0 events/s); the *standing representation* is the villain. Redirects the queued build `b-h-live` from "count distinctions per second" to "shrink and share the standing bytes".

## Evidence

Machine: lab Linux, 8 vCPU, load 0.8, 13.7 GB available, ~28–49 °C zones. Reproduce (≤ 60 s):

```
cargo build --release -p emergent-universe --example hlive
/home/glmlab/lab-target-3/release/examples/hlive   # 0.2 s wall, 10.9 MiB maxrss
```

Log: `hlive.log` in this folder. Scenario: the plane, seed 1, Sparse, 1 thread, 64 fleet members; 12 probes of 2×10⁷ ticks (98.5 game-s each), prune at every probe boundary, counting allocator as instrument.

- **Steady state (last 3 probes):** live-after-prune flat at 2.91–3.29 MiB; engine `bytes_per_body` 5,615 B; median ship `body_bytes` 1,456 B, max 3,120 B; history depth median 0, max 11.
- **Reabsorption balances creation:** from probe 5 on, prune reclaims what settle created (e.g. probe 6: +600 KiB created, 2,002 KiB reclaimed; net live *falls* 6.7→2.9 MiB and then holds). Retention = the view's window (2× light distance), not an archive.
- **Event mix per probe (steady):** kick 55, boundary 51, slice 169, open/handoff/decision 0 — the fleet battle's contact slices are 61% of events.
- **Rates per body:** median ship 0 events/s; max ship 5.1×10⁻² /s; player 1.0×10⁻¹ /s. Creation churn ≈ 1.3 KiB of transient allocations per event (compile temporaries), not retained.
- **Attribution:** `BodyRec` 448 B, `Segment` 192 B, `Knot` 88 B; a ship's compiled shape is 6–11 knots = 528–968 B. Median ship ≈ 448 + ~700 (shape) + plan/slots ≈ 1.45 KB.
- **Extrapolation:** 1.456 KB × 10⁹ = 1.42 TB = **175× over 8 GB**. Even the irreducible binding as stored today (tube 16 + residual/turn/kick ≈ 48 + event_time/doll/units ≈ 8) ≈ 80 B/body → 80 GB = **10× over** with zero multiplier.
- **Instrument controls:** live counter rises during settle, falls after prune, returns to +1,400 B above baseline after drop (~0). Disclosed: the `net_KiB` column underflows when negative (cosmetic; all numbers above read from the live columns).

## Predictions

`predictions.md` was written before the run. Outcome: **P1 falsified** (slices 61% > kicks 20% — contacts, not gravity, dominate event count at the plane's cadence); P2 confirmed (prune reclaims ≈ creation in steady state; flat live); P3 confirmed (5,615 B/body engine, 1,456 B median ship ≥ 500); P4 confirmed, stronger than predicted (175×, predicted ≥ 10×); P5 confirmed (median ship 0 new tubes/s; every AU-orbit ship < 1/s).

## What would make it wrong

- Shape sharing: bodies on identical orbit keys already share catalogue entries, so a universe of co-orbital fleets (the 20261006-0346 gold's formations) could cut the shape term 10–50× — but never the 448 B record, so the conclusion stands above ~10⁶ distinct orbits.
- The allocator sees the whole process; the engine's own `bytes_of` attributes only ~0.43 MiB of the 2.91 MiB live, so per-body decomposition uses the engine's attribution while the ceiling uses live totals — the 175× is if anything conservative.
- One star system, 23 ships: per-body rates could rise in denser scenes (belts), which would strengthen, not weaken, the standing-bytes conclusion.

## Cost of adoption, and fit with PRINCIPLES

Two deletions, no gate touched: (1) make catalogue entries evictable (`Arc`→`Weak` + recompile on miss: the plane already recompiles on ~99% of kicks, so the read path pays this today); (2) put plan/thrust/ext out-of-line so a sleeping body costs its tube + residuals (~80 B). PRINCIPLES: "The memory floor is information-theoretic" (#24) — the measured floor of today's integers is ~80 B standing per active body, not 16; "Store the generator, not the generated" (#6) — holding one compiled shape per body is storing the generated; "The cheapest compute is compute not done. Delete before optimizing" (#1). Board fit: H_live measured; it does **not** exonerate the top scaling risk (candidate pairs at N) — different axis.

## The lens

SpaceX's delete bias is a one-way-door hazard here: eviction trades standing memory for compile latency *inside the view's read path* (the past light cone), which this CPU-side run does not measure; that latency, not memory, could become the new worst idiot index. Also, I measured one seed — fat tails across scenes (a hot fleet battle) are one experiment away.

## Files

`crates/universe/examples/hlive.rs` (new), `crates/universe/src/body.rs` + `universe.rs` (two accessor methods: `history_depth`, `body_bytes`).
