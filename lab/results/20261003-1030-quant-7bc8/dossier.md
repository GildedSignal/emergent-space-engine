# Dossier — 20261003-1030-quant-7bc8 (quant lens, autonomous)

## Claim

The kick's rebind is not compile-bound: `fit_key` is the largest single stage of
`Rebinding::from_state` (30–31%), ahead of the trajectory compile (30–34%, of which
quadrature is 27–31%); an **exact**-key shape intern can never pay (0 hits in 2×1,912
kicks on both seeds — killed, as pre-registered), but the codebase's own memo width
(`OrbitKey::memo_key`, 12+12 bits, already envelope-gated for `MemoCode`) recurs on
**98.1–98.2%** of the kick stream, so compile cost is set by orbit-key *diversity*
(37 distinct quantized keys for the whole plane scene), not by kick count or population.

## Bottleneck

Board focus 1 ("fewer kicks per orbit … kicks dominate the engine's cost") and the
handoff's measured fact "a kick costs 29 µs, 15 of them in rebinding fit and compile".
This run decomposes those µs and prices the precompute bet before anyone spends a step
on it. Expected gain: the memo finding caps compile cost at diversity rather than
population — at a billion ships that is the difference between per-kick quadrature
forever and ~10³ compiled shapes per doll ("store the generator, not the generated",
PRINCIPLES §6). Immediate measured saving if a memo compile were adopted: only ~15% of
the kick — not the unlock by itself.

## Evidence

All commands ≤ 60 s, cloud Linux/x86, 2 shared vCPU — orders of magnitude only.

- Baseline (unmodified tree): `./target/release/xtask universe --kick-bench --seconds 55 --rtf 300`
  → 1,912 samples, median 18.8 µs, p99 25.1 µs, refused 0, seed-1 digest `e9d41fe8…`, replay digest `75029952…`.
- Instrumented (stage counters + exact-key intern + memo observation; patch in this run's tree):
  same command, seeds 1 and 7 → medians 25.6 / 25.8 µs (shared-box contention; the first
  decisive run measured `from_state` at 28.4 µs vs 9.8 µs in the quiet batch — report
  shares, not absolutes), refused 0, and on seed 1 the **digests are bit-identical to
  baseline** (`e9d41fe8…` / `75029952…`) — the intern and instrumentation change no
  outcome (seed 7 was not run on the uninstrumented build; its digests are recorded in
  `kickbench-seed7.json` for the checker to reproduce).
- Stage budget of `from_state` (both seeds): `fit_key` 30–31%, compile 30–34% (quadrature
  27–31 points of it), orientation 8–10%, residual 24–26%, slack ~9% (memo observation +
  instrumentation). `from_state` is 38–50% of the whole kick sample; the rest is readout,
  forces, sigma-delta, apply, plan.
- Hit rates: exact `ShapeKey` intern **0 / 1,912** on seed 1 and seed 7. Memo-width
  (12+12) recurrence **1,875/1,912 = 98.1%** (seed 1) and **1,878/1,912 = 98.2%** (seed 7,
  held out). Raw JSON: `kickbench-seed1.json`, `kickbench-seed7.json`, summary `metrics.json`.
- Capacity (order of magnitude): 19–26 µs/kick ⇒ ~4–5×10⁴ kicks/s/core; at H0190's 32
  kicks/orbit and 90-min orbits, ~5–9×10⁶ ships/core ⇒ 10⁹ ships need ~110–250 cores —
  consistent with the board's ~190-core Fermi estimate.

## Predictions

`predictions.md` was written before the decisive run, with frozen kill rules.

- P1 ("shape build ≥ 50% of `from_state`") **failed**: it is 27–31%, and `fit_key` is the
  largest stage. Reported as held-nothing-back; the kill rule for the "compile dominates"
  premise (< 30%) was *not* triggered — compile and fit_key are comparable, and together
  they are ~60–65%.
- P2 ("exact-key intern < 5%") **held**: 0%. The exact intern configuration is KILLED
  (a `Scalar` continuum never repeats; a table over it buys nothing).
- P5 (seed 7 same qualitative picture) **held**.
- The 98% memo recurrence was **not pre-registered** — it is a new finding from the
  observational counter; seed 7 is its independent replication, not a prediction.

## What would make it wrong

- The memo hit rate is measured on the plane's ~70-body scene. A billion-ship galaxy has
  more dolls, eccentricities and regimes; if key diversity grows ~linearly with
  population, the amortisation claim dies. The scaling law diversity(N) is the unmeasured
  link (the named next experiment).
- Adopting a memo-width compile **changes outcomes** (the binding rides the quantized
  orbit — digest changes). The envelope tests already assert ≤ 0.1% period fidelity at
  12+12 bits for `MemoCode` use, but adoption in the bind path is a law-gate decision
  (B9/B14 behaviour, not bit identity), the integrator's to freeze — not this run's.
- Cloud contention moved absolute µs by up to 3× between runs; only digest-anchored
  counts (0 exact hits, 98% memo recurrence) and within-run shares are load-bearing.

## Cost of adoption, fit with PRINCIPLES

- The *measurement* (prof counters + `observe_memo`) is already outcome-neutral and
  digest-verified. An adopted memo compile is one bounded map keyed by the existing,
  envelope-validated `memo_key` — no new representation; it deletes per-kick quadrature
  (PRINCIPLES §3 "Nothing is evolved that can be derived when looked at", §26 "steal
  what works" — from the codebase's own `MemoCode`). The exact-key intern is dead and
  should not be merged (it also lacks eviction).
- Fit with the lens's own blind spot: 98% hits at 12+12 bits is exactly the temptation to
  shave µs by spending exactness; the bit-identity kill rule (VOID on digest change) is
  what kept this run honest.

## The lens

The quant lens prices stages and tables; it nearly missed that the table's key space was
already designed by someone else (`memo_key`, G1/G2) — a scout of `crates/space` before
designing my own quantization would have saved twenty minutes and a dead prediction (P1).
It also prices one scene; diversity-vs-population at galaxy scale is outside this lens's
evidence, and the fit_key share (30%) has no exact-preserving shortcut this lens can name
— an incremental invariant solver is a dynamics question, not a latency one.

## Grade suggestion

Silver: reproduced bit for bit on both seeds, one configuration killed with a frozen
rule, one replicating edge found (98% memo recurrence) — gold needs the memo compile
adopted behind the law's behaviour gates with diversity(N) measured on a scaled scene,
plus the M1 re-measure.
