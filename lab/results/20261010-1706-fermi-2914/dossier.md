# Dossier — 20261010-1706-fermi-2914 (Fermi lens)

## Claim

Measured on the plane's own kick resolver: a ship's kick stream creates ~20 bits of live distinction per kick (key Δ ≈ 5 bits + four residual components ≈ 3.4–3.9 bucket-bits each) and revisits its own orbit programs 82–97% of the time, so H_live per body is bounded by the *current binding* (~15–25 bits entropy-coded, 33 B raw), not by accumulated history — and at 10⁹ bodies the first-breaking term is kick **compute** for short-period populations (~40 µs/kick here caps them near 10⁵ ships at rtf 100), while for long-period (belt) populations both compute and storage sit orders below budget; raw residual storage is the one term that misses the 4 GiB floor (~8× at 10⁹) and is the representation question to attack.

## Bottleneck

Board item "fitting 10⁹ in 8 GB, decided by distinctions created per game-second" (b-h-live; HANDOFF: "not measured yet"). Expected gain: deletes the "N² candidate/byte anxiety" for massive *smooth* populations and names the two real budget breakers. Order of magnitude: 10⁰–10¹ bits/body (creation), against a 34 bits/body total budget.

## Evidence

Instrumented `xtask/src/universe/kick_bench.rs` (the plane's own resolver, unmodified law; patch is this run's `work/patch.diff`) to record, per distinct kick: Δk on the law's Q48 lattice (signed log2 buckets), quantized memo-code revisits per body, the four binding-residual components (log2 magnitude buckets), per-body kick counts, and game-seconds. Runs (Linux x86, 8 vCPU, orders of magnitude only):

```
target/release/xtask universe --kick-bench --rtf 1000 --seconds 40 --members 2000   # → kb-rtf1000-m2000.json
target/release/xtask universe --kick-bench --rtf 100  --seconds 45 --members 5000 --seed 7  # → kb-rtf100-m5000.json
```

| quantity | rtf 1000 | rtf 100, seed 7 |
|---|---|---|
| distinct kicks / bodies that kicked | 34,544 / 393 | 15,997 / 376 |
| kicks per body per game-second | 2.0e-3 | 8.4e-3 |
| Δk bits (bucket entropy) | 4.93 | 4.57 |
| memo-code revisit rate (per body) | 0.825 | 0.968 |
| residual bucket-entropy, 4 comps | 3.63/3.86/3.83/3.85 | 3.63/3.58/3.42/3.35 |
| kick µs median / p99 (resolver only, x86) | 36 / 414 | 58 / 365 |
| exact memo hit / quantized memo hit | 0.0 / 0.989 | 0.0 / 0.983 |

The exact-memo 0% on distinct kicks reproduces the 5 October correction on the real stream (independence check: the events here are distinct pending kicks by construction).

**Budget at 10⁹ (M1: ~4 GiB universe budget, 4 P-cores, rtf 100):**
- Tube store: 16 B × 10⁹ = 16 GB — massive populations must be family generators (galaxy scene already stores 0 B/ship). Live budget = 34 bits/body.
- Kick compute at measured 40 µs: plane-cadence ships (8.4e-3 kicks/body/s) → 8.4e6 kicks per game-second → 336 core-s per game-second at 10⁹; sustainable N ≈ 4 core-s/s ÷ (8.4e-3 × 100 × 4e-5) ≈ **1.2e5 ships**. Belt at 3 AU (0.3 kicks/orbit secular): 1.8 kicks/s at 10⁹ → 72 µs per game-second: **no constraint** (~10 orders of headroom).
- Amendment storage, belt cadence: 1.8e-9 × 3600 s × 33 B ≈ 2e-4 B/body: none. Raw *current-binding* storage is the real term: 33 B/body × 10⁹ = 33 GB = **8× over 4 GiB**; entropy-coded at the measured stream (~20 bits + phase/time ≈ 25 bits ≈ 3 B) ≈ 3 GB: fits.
- Reabsorption is real: 311 distinct quantized programs absorb 28,801 cycle rebinds (99%), and 82–97% of a body's kicks land on programs it already visited — the program walk is confined, so shared-cycle compilation + binding-residual storage is the correct "programs plus scars" shape.

## Predictions

`predictions.md` was written before the decisive run. (1) held: compute is not the breaker for belt cadence (orders below), and un-reabsorbed storage is the representation question — but sharpened: it is the *current* residual, not accumulated history, that matters (I had overestimated accumulation; pruning and confined walks bound it). (2) half-held: residual dominates Δk, but by ~3× (≈15 vs ≈5 bits), not ≥10× — and bucket entropy is a floor, not exact bits. (3) held strongly: revisit 0.83–0.97. (4) held: sustainable short-period population ~1e5 (I guessed 1e5–1e6), at the measured 36–58 µs/kick.

## What would make it wrong

- Bucket entropies are *lower* bounds: residuals' within-bucket low bits could carry up to 4×65 bits; only a full-precision entropy measurement of the i128 components (not done; the recorder buckets by log2) would close that. If true residual entropy is ≫15 bits, the 3 GB "fits" line inverts.
- The plane's ships are a hand-made population (~400 bodies, low orbits, fleet members): belt-cadence numbers are derived from H0190's 0.3 kicks/orbit, not measured here; a real belt population at 10⁶+ could behave differently (encounters add distinctions that do not scale with 1/P — unmeasured).
- x86 timings, resolver-only (allocator, application, view excluded); the M1 re-measures.

## Cost of adoption, fit with PRINCIPLES

Adoption cost: near zero for the finding (a measurement + a patched bench that any later run can rerun). The lever it names — residual representation at birth (fold-into-tube vs carry) — is the existing changeover/handoff work (JANUS, single-surface handoff), not a new component. Fits: "the memory floor is information-theoretic" (measured ~20 bits/kick against a naive 260), "compute only surprises" (99% program reuse), "store the generator, not the generated" (311 programs for 29k rebinds).

## The lens (what Fermi missed)

The Fermi lens estimated before measuring and got the *ordering* right but the *sizes* wrong by 10–40× (µs/kick: guessed 1, measured 36–58; residual-vs-key ratio: guessed ≥10×, measured ~3×; accumulation: guessed linear history, actual confined walk). The lens also cannot see encounters and the player (both create distinctions not proportional to 1/P); that is the next run's territory, and `q-candidate-degree`'s domain.

## Reproduce

```
cargo build --release -p xtask
target/release/xtask universe --kick-bench --rtf 1000 --seconds 40 --members 2000
target/release/xtask universe --kick-bench --rtf 100  --seconds 45 --members 5000 --seed 7
```
Raw outputs: `kb-rtf1000-m2000.json`, `kb-rtf100-m5000.json` (this folder); bench patch in `work/patch.diff` (saved by `run.sh`).
