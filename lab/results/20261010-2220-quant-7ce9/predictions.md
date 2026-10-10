# Predictions (written before the decisive run)

Run: `cargo run --release --bin kickfloor -- decompose` and `-- sweep` in this folder.
Machine: shared GitHub Actions runner, i7-4790 (Haswell, 4C/8T), Linux x86-64. Orders of magnitude only.

The question: where does a kick's time go — (a) secondaries setup (per-kick `Vec<Secondary>` rebuild + tube state reads), (b) the exact force kernel (`force::acceleration`/`field`, Q62 `Scalar` with `isqrt`+exact division per secondary), (c) the rest of `step::process` (drift readout, sigma-delta, rebind/tube recompile) — and how much of (b) is the *arithmetic* rather than memory (working-set sweep), priced against an f64 twin of the same formula.

## Point predictions (not tuned on; the code has not been run yet)

P1. Full ship kick `step::process` on the plane (rtf 1, seed 1, members 48): median 5–40 µs; p99 ≤ 5× median.
P2. Setup (`ctx.secondaries` + `ctx.tide` alone) is 1–5 µs, i.e. 5–30% of the total.
P3. Kernel (`force::acceleration` at level 0, S ≈ 4–10 secondaries in the star doll) is 1–8 µs, i.e. 10–40% of the total; the residual (c) is the plurality, ≥ 40%, because the plane rebinds (recompiles) on ~99% of kicks (taste log, 5 October).
P4. Per secondary, exact kernel: 200–800 ns/eval cache-resident. f64 twin: 20–80 ns/eval. Ratio 5–15×.
P5. Working-set sweep (S=8, 32 KB → 512 MB): exact ns/eval stays within ±30% from L1-resident to 8 MB (L3 on this die) and rises ≤ 2× at 512 MB (DRAM streaming); the f64 twin shows the same shape. I.e. the kernel is arithmetic-bound at every scale the game will run, not memory-bound; layout is not the lever today.
P6. Sharing: distinct (doll, tick) kick epochs per 60 Hz snapshot are ≤ 1/3 of the distinct kicks (many bodies kick against identical secondaries states); per-epoch sharing of `secondaries()` would cut setup by that factor at zero exactness cost.

## Kill rules (frozen now)

- K1: kernel < 20% of total → "cheaper exact kernel" is killed as a lever; cadence/rebind stays the only lever.
- K2: exact/f64 ≤ 3× → exactness is already cheap; no representation change is warranted.
- K3: kernel ≥ 30% of total AND exact/f64 ≥ 10× → the exact arithmetic is the named next lever.
- K4: sweep shows ns/eval ≥ 2× at ≤ 64 MB working set → memory layout becomes a lever at game scale.

Honesty note: the sweep kernel is `field` on synthetic (deterministic LCG) `Secondary` data with plane-like magnitudes; the decomposition runs on the real plane through the shipped `scenario::plane` and `step::process`. Both use shipped crate code, no reimplementation of the exact path.


## Outcomes (written after the run, 22:31 UTC)

- P1: 41.3 µs median — at the upper edge (predicted 5–40). Held.
- P2: setup 10.1 µs / 24.5% — share held (5–30%), absolute 2× my upper bound. Half-miss.
- P3: kernel 1.57 µs but only 3.8% (predicted 10–40%) — share missed low; residual 71.8% ✓ (plurality held).
- P4: exact 578–916 ns/eval ✓ (200–800); f64 21–31 ns ✓ (20–80); ratio **27–30× — missed** (predicted 5–15×; exactness costs twice my upper bound). Per-kick ratio 18×.
- P5: held — 916→647 ns/eval from 32 KB to 8 MB (−29%), 578 ns at 320 MB: no cliff, arithmetic-bound at every scale.
- P6: direction held, magnitude missed high: 487 kicks per epoch (17 epochs for 8280 kicks), not ≤3×.
- New, unregistered: rebind_rate 1.000 (every kick leaves a new entry) — consistent with the 5 October memo finding.