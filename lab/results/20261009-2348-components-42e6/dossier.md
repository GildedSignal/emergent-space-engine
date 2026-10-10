# Dossier — 20261009-2348-components-42e6

**Claim.** On the plane, a live body's exact state packs into 57 B (round-trip exact) against 672 B stored today (11.8×), but no packing of per-body bindings can hold 10⁹ bodies in 8 GB; the measured distinction rate H_live ≈ 0.62 bits/body/game-second spends the whole 8 GB-at-10⁹ scar budget in ≈100 game-seconds, so the billion-scale store must be programs plus a scar horizon under two minutes of game time.

**Bottleneck.** Board risk "Distinctions created per game-second (H_live): not measured yet; they, not the body count, decide whether 10⁹ fit in 8 GB" (the storage component's floor). This run puts the first numbers on it.

**Evidence** (Linux x86, orders of magnitude only; every command ≤ 60 s).

- Probe: `cd lab/results/20261009-2348-components-42e6/hlive && cargo build --release` (binary at `$CARGO_TARGET_DIR/release/hlive`). It replays the plane's own scene (`scenario::plane`, seed, 48 members) and censuses every distinct pending kick via the pure resolver (`step::process`), exactly `xtask --kick-bench`'s pattern, dumping each new binding's fields. Nothing is applied; digests untouched.
- Runs: `hlive --seconds 20 --rtf 300 --seed 1` and `--seed 7` (6000 game-seconds each; 1968 and 2325 kicks; wall ≈ 0.7 s). Census vs the engine's own `stats.kicks`: 1968/2023 and 2325/2444 (0.1–5%; kill criterion was 2×). Calibration run 2 s at rtf 1 in `run100.txt`/`k100.jsonl`.
- Analysis: `python3 analyze2.py` → `analysis2.json`; round-trip check (static per-kind bitfields, widths = max magnitude + sign) on 3711 records: **0 out-of-range — EXACT**. Sizes measured in-process: `BodyRec` 448 B, `Arc<Entry>` 224 B, `Segment` 192 B.
- Numbers (both seeds agree):
  - Live state: naive 672 B/body; packed bitfields 453–459 bits = 56.6–57.4 B/body; plug-in order-0 entropy ≈ 140 bits ≈ 17.6 B (sample-limited, biased **low** — 63 bodies; the honest floor interval is [~140, 459] bits). Packed sits 3.2× the plug-in floor: within the lens's 10×.
  - At 10⁹ bodies: naive 672 GB, packed 57 GB, budget 8 GB = 8 B/body = 64 bits — **7–84× over at any packing**; per-body bindings cannot be the billion-scale store.
  - H_live: scar stream 120.5–122.4 bits/kick (per-body delta coding; plug-in, biased low); belt-like kick rate 0.00514/body/game-second (both seeds) → **0.62 bits/body/game-second**; 8 B/body budget spent in **102–103 game-seconds** (fleet-rate bodies: 83–149 s).
  - Catalogue sharing: exact-shape hit rate **0%** (716/716 and 2291/2292 rebinds created a new entry; quantized 12+12 memo hits 93.0–97.8%) — reproduces H0213 on a different scene: the exact catalogue is a per-body compute cache, never shared structure.
  - Deletion candidate: 0.6% of kicks carry dv = 0, yet 86% of them still allocate a new catalogue entry — a rebind with no distinction ("the cheapest compute is compute not done", P1).

**Predictions** (`predictions.md`, written before the decisive run): kick-rate class split and exact/quantized memo behaviour held (2 confirmed exactly); the 0.5 kicks/body/s calibration rate did **not** hold at length (it was initial-condition transient; steady belt-like rate is 100× lower) — reported as held/missed per item; the "history grows 1 Segment/kick" prediction held (retired 1968/1968, 2323/2325); floor-bytes prediction (20–40 B) held inside the honest interval.

**What would make it wrong.** The scene is 63 bodies, not a belt: B18b's belt (frozen, unwired) may kick far less — a smooth belt far from secondaries absorbs tides into sigma-delta carries, and the true distinction rate is the *quantum-crossing* rate, which this run bounds only through the kick stream (dv = 0 is the visible proxy). The plug-in entropies are biased low at this sample size; the packed 57 B is the trustworthy side. Belt-scale H_live must be re-measured on the wired belt scene; if it is 100× lower there, the scar horizon stretches to hours and the premise softens.

**Cost of adopting.** The packed per-kind SoA layout is a drop-in `BodyStore` (`shipmem`'s packed blocks own this seam) for light-cone residents; no law change. The 100-second scar horizon is a design constraint for the belt store (b-belt-wire), not code. Zero-dv rebind skipping is a small law change (one early-out in `step::process`) that must re-run B12–B17.

**Fit with PRINCIPLES.** "The memory floor is information-theoretic (entropy given shared structure), not bytes × count" (standing decision; P24 "the memory floor is information theory") — this measures the floor's growth term. "Store the generator, not the generated" (P6): the catalogue measured 0% sharing, so today it stores the generated; the generator is the body's own state. "The cheapest compute is compute not done" (P1): the zero-dv rebinds.

**The lens (what it may have missed).** A storage-only optimum can move cost into compute: evicting the unshared catalogue (57 GB → 0) is only free if recompiles are, and kicks dominate the engine — the cache/compute trade is the neighbour component left unmeasured here. The census shares `kick_bench`'s harness; its agreement with H0213's memo numbers is a consistency check, not an independent one (the memo lesson, 5 October).

**Grade request:** silver — real, reproduced on two seeds with exact round-trip, but the belt scene itself (B18b) is the named experiment that would make the H_live number gold.
