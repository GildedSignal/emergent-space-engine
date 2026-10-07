# Dossier — 20261007-1801-fermi-bb60 (Fermi lens)

## Claim

At 10⁹ bodies on the M1 no wall is set by N: memory, event bandwidth, encounters and folded H_live each hold with 1.5–6 orders of margin, and the only binding constraint is the product **strong-tide population × kick cadence × fold cost**, which today's corner (unaveraged kicks, 29 µs recompile-dominated fold) puts 3,500× over budget but the designed corner (orbit-averaging where stable, hot integer fold) puts 15× under — a ~50,000× swing from representation alone, no hardware change.

## Bottleneck

Board item 3 ("cost at a billion": the 190-core figure) + the handoff risk "H_live: not measured" + lens items 1–3. Expected gain: deletes the idea that 10⁹ needs memory or encounters work now (they hold by ≥25× and ≥10⁷×), and names the one number that decides 10⁹: the **hot fold cost per kick**, whose design-carrying ingredient is the shared cycle memo's hit rate. Nothing to build; a reordering.

## Evidence

Machine: this run's Linux/x86 box, single-thread micro-benchmarks, orders of magnitude only (the integrator re-measures on the M1). All engine constants cited in `budget.py` (H0190 K1/K2/K6, H0210's 29 µs kick, law.md's 16 B tube and 0.05-compiles/kick re-anchor, shipmem 0.126 bits/body, r8 v2 + q-candidate-degree encounter rates, board M1 budgets).

Reproduce (each ≤ 5 s):

```
cd lab/results/20261007-1801-fermi-bb60
cc -O2 -o bench bench.c && ./bench all        # -> bench-out.txt
python3 budget.py 3.2 19.6                    # -> budget-out.txt (values from bench)
```

Measured here: integer fold (two u128 fixed-point updates + heap push/pop) **3.2 ns/op**; sequential read **17 GB/s**; random 16 B tube update over 1 GiB **19.6 ns/op** (~5×10⁷/s/core, memory-level parallelism hides latency).

- **Claim check (lens item 3):** the board's "about 190 cores at 10⁹" re-derives to 175 cores (32.5 kicks/orbit ÷ 5,400 s × 10⁹ × 29 µs), 301 with the probe's 50 µs, 600 from H0190's own 0.6 core/10⁶ — the claim stands (same wall, 190 is its low end).
- **Kick frontier at RTF 100, 5 eff. cores:** all-10⁹-strong-tide: 17,454 cores (3.5×10³× over); with a free 200 ns fold still 120 cores (24×); K2-averaged + 64 ns hot fold **0.34 core**; K2 + law.md's cold re-anchor (0.05 × 29 µs = 1.45 µs) **7.7 cores (1.5× over)** — the cycle memo must stay hot. Realistic scene (10⁹ belt + 10⁷ fleet strong-tide): 0.39 core hot, 8.7 cold. Frontier N* (strong-tide bodies): 2.9×10⁵ today → 1.3×10⁸ (K1 + hot fold) → 1.5×10¹⁰ (K2 + hot fold).
- **Other walls at 10⁹:** event bandwidth 0.5% of 60 GB/s; full 60 Hz sweep of 10⁹ tubes = 16× total bandwidth (event-driven mandatory — principle 14 quantified); memory 16 MB bulk programs + 0.16 GB tubes at 1% live; encounters (belt-0 density, work tracks real ones) 2.3×10⁻⁸ cores.
- **H_live (the unmeasured risk), now bounded:** with kicks folded (rebinding with remainder carried), net new state ≈ 1 bit/s wall → **435 B per hour of play** at 10⁹ — five-plus orders below concern. If kicks scar instead: 34.7 GB/h at 10⁶ unaveraged strong-tide ships (4 GiB breached in ~7 minutes), 30 GB/h at 10⁸ even averaged — **folding is load-bearing at any fleet scale**, 30× lower a threshold than my pre-registered guess.

## Predictions (`predictions.md`, written before the run)

Held: P4 (claim check 175 vs 190, <2×), P5 (adversarial scenes 3.5×10³× and 24× over), P6 (averaged + hot fold ≤ 3 cores: 0.34). Failed, all in the feasibility-favoring direction: P1 fold floor 3.2 ns vs predicted 100–1,000 ns (arithmetic is free; cost lives in memory and recompiles); P3 random update 19.6 ns, 21× sequential, vs predicted 50–200 ns and ≥30× (the random-access wall is mild: 2.4× over only in the absurd unaveraged corner); P9 sweep 16× over, not ≥10³× (mis-derived in the prediction against one core). Failed against me: P7's "≥2 orders everywhere" — compute's margin in the realistic scene is 13× (one order); P8's scar threshold was 100× optimistic (forgot RTF: scars bill game-time memory against wall-time play). Three honest misses, none touching the headline.

## What would make it wrong

The strong-tide rate is LEO-specific (5,400 s orbit, 114× averaging measured there); scenes needing >1.3×10⁸ unaveraged strong-tide bodies at RTF 100 (K1 + hot fold) break compute — and nothing in the goal forbids them. The far bodies' kick rate is unmeasured (I charged all 10⁹ the full K2-averaged LEO rate: 0.13× budget, so the conclusion survives it, but the true belt rate is a cheap rung). x86 → M1 and the 5-effective-core figure are order-of-magnitude transfers. Cost of adoption: zero (no code); it says measure **compile cost + cycle-memo hit rate** on the plane (the fold's hotness is now a design-carrying number) and keep q-cadence as the lever. Fit: "The cheapest compute is compute not done" (the 50,000× swing is representation, not optimization) and "the memory floor is information-theoretic" (0.126 bits/body + 435 B/h).

## The lens

Fermi sees budgets, not dynamics: it assumes law.md's fold is exact (integer, non-compounding) rather than verifying it, it cannot see whether averaged kicks *behave* right (B12/r9 territory), and its scene choices (RTF 100 everywhere, LEO strong-tide) may misprice what the player's galaxy actually looks like — the frontier table is the guard: any other scene is three factors multiplied.
