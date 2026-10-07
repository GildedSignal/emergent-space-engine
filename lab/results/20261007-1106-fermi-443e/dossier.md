# Dossier — 20261007-1106-fermi-443e

## Claim

Measured on the plane: the HANDOFF's unmeasured risk "distinctions created per game-second (H_live) decide whether 10⁹ fit in 8 GB" resolves to **H_live is not the binding term** — each event injects ~104 near-incompressible bits but is reabsorbed (residual late/early ratio 1.09–1.20 per hour), so at 10⁹ bodies even the worst all-inner cadence creates only ~182 MB/s of live distinctions (300× under the M1's 60 GB/s) and never fills 8 GB; the binding terms at 10⁹ are the **stored representation today (9,846 B/body = 1,231× over 8 GB; the belt-program floor 0.126 bits/body is 508× under)** and **event compute at inner-scale cadence** (the board's "190 cores" re-derives exactly: 10⁹ × 0.014 events/body/game-s × 12 µs = 168 cores).

## Bottleneck

Board item "fitting 10⁹ in 8 GB … decided by distinctions created per game-second" and HANDOFF risk "H_live: not measured yet". Gain: the risk re-ranks from top to non-binding (it deletes the fear that per-second information creation is the wall); what it exposes is that the wall is the per-body cache (shipmem's term) and inner-cadence kick compute. No 10× engine gain claimed — this is a measurement that redirects the next 10×.

## Evidence

All commands ≤ 60 s on this box (Linux x86, 8 vCPU; orders of magnitude only, the integrator re-measures on the M1). Instrument: `crates/universe/examples/hlive.rs` (new, saved in this run's patch) — it walks each body's distinct bindings and measures the residual (exact integer state minus the turned tube, 4×i128) and the deltas between successive ones; deltas are between **distinct event times** (BTreeSet-deduped), so no memo-style double counting.

cargo build --release -p emergent-universe --example hlive -j 6          # 45 s cold, 4 s warm
HLIVE_OUT=<run>/hlive_deltas_s3600_seed1.bin cargo run --release -p emergent-universe --example hlive -- 3600 1 400
HLIVE_OUT=<run>/hlive_deltas_s1800_seed1.bin cargo run ... -- 1800 1 400   # un-tuned variants
HLIVE_OUT=<run>/hlive_deltas_s3600_seed2.bin cargo run ... -- 3600 2 400
HLIVE_OUT=<run>/hlive_deltas_s3600_seed7.bin cargo run ... -- 3600 7 400
python3 fermi.py                                                       # the 10⁹ budget table
```

- **New bits per event:** delta between successive residuals, median 20 bits/component (p99 ≤ 26, max 28) ⇒ **~80–104 bits/event** over 4 components; zigzag-varint stream 13 B/event, zlib compresses only ~5% ⇒ near-incompressible, i.e. genuinely dense distinguishing bits at the law's own quantization, not redundant tags.
- **Reabsorption:** mean residual 4-component bits early-vs-late (run-time halves, 323/292 bindings) = 71.3 vs 78.0 ⇒ **ratio 1.09** (1.10–1.20 across variants): bounded, consistent with the plane recompiling an orbit on ~99% of kicks (taste log, 5 October). No walker population on this scene.
- **Rate:** 1,582 kicks + 0 handoffs in 3,600 game-s over 28 bodies ⇒ **0.010–0.018 events/body/game-second** at the plane's inner scale (ships on hours–days orbits).
- **Footprint today:** `bytes_per_body` = **9,846 B** (includes compiled trajectory share and replay history — an upper bound on the held state, not the information).
- **Wall:** 3,600 game-s settled in 0.23 s (28 bodies) ⇒ ≤ 66 µs/event amortized including fixed machinery.

Budget at 10⁹ bodies (M1: 8 GB, ~10¹⁰ ops/s, ~60 GB/s; `fermi.py` regenerates every line):

| term | 10⁹ belt (2.5 AU, 32/orbit) | 10⁹ all-inner | budget | verdict |
|---|---|---|---|---|
| H_live creation | 3.3 KB/s (31 B/s averaged) | 182 MB/s | 60 GB/s | 300–10⁷× under |
| H_live accumulation | 0 (bounded, ratio ≤ 1.2/h) | fills 8 GB in 44 s **only if** reabsorption breaks | — | measured: holds |
| stored, as today | 9.85 TB | 9.85 TB | 8 GB | **1,231× over** |
| stored, program floor | 15.75 MB | — | 8 GB | 508× under |
| residual, all hot | — | 10.5 GB | 8 GB | needs sparsity (per-disturbed-body, not N) |
| kick compute | 0.02 core·s/s | 168–924 core·s/s | ~1 M1 | inner cadence is the compute wall |

Board cross-check (lens task 3): "10⁹ … about 190 cores" re-derives from measured anchors as 10⁹ × 0.014 events/body/game-s × 12 µs/event = 168 core·s per game-second — it is a statement about **inner-scale event cadence**, not about memory or information; at belt cadence the same 10⁹ bodies cost 0.02 core·s/s (five orders less).

## Predictions

`predictions.md` was written before the decisive run; 9 predictions, 6 held, 2 missed, 1 split:

- Held: bits/event (20 vs 10–50), residual bits (21 vs 40–100), reabsorption ratio < 1.3 (1.09–1.20), rate 0.01–1 (0.010–0.018), representation-binds-not-H_live, belt-scale H_live order.
- **Missed:** bytes/body predicted 100–400, measured 9,846 — I under-modelled `bytes_of` (history + compiled trajectory dominate; it is a cache, not information). Compressed stream predicted < 6 B/event, measured ~12.2 B/event — the deltas are high-entropy, so the ~104 bits/event are real state distinctions.
- My own kill criterion ("bytes/body > 1 kB ⇒ risk is the top bottleneck") **fired**, but on the stored-representation term, not on live-distinction accumulation, which stayed bounded. The risk as written ("distinctions created per game-second") is answered *safe*; the fired part belongs to shipmem/B18's term.
- Disclosure: the first run printed reabsorption ratio 0.00 — an artifact of my own sampling (the "late" set selected the 200th+ distinct binding per body and was empty). Fixed before relying on it; the corrected split is by run-time halves with both set sizes printed (323/292).

## What would make it wrong

The scene is 28 bodies in one star system, no belt, no 10⁶-fleet, AI off the plan; the bounded ratio is measured on one hour of game time. A dense belt or fleet (co-orbital concentration, gold 20261006-0346) could hold far more simultaneously-disturbed bodies, and the reabsorption ratio could drift on 10³+ game-hour horizons — rerun `hlive` there. The ~104 bits/event is churn of a deterministic law's re-encoding, not new information in Shannon's sense: in a closed deterministic universe the only true new information is the player's (principle 5), so the number is an upper bound on what any cache must absorb. Adoption cost: none (a measurement plus one example binary); the instrument stays for the belt rung. Fit: "The memory floor is information-theoretic" (PRINCIPLES 24) — the floor now has measured constants; "Compute only surprises" (3) — the per-event surprise is ~104 bits and it reabsorbs.

## The lens

Fermi ordered everything by magnitude and nearly missed the representation point: the 1,231× overage is not information at all but today's cache layout, and the "190 cores" is a cadence statement disguised as a memory statement. What the lens also made me miss: one hour on a 28-body scene cannot speak for concentrated fleets; the instrument (not the estimate) is what the next run should carry there.
