# Predictions — 20261006-1354-fermi-c9fa

Written BEFORE running `budget.py`. All numbers below are head-math from the
anchors listed in `anchors.json`; the script is the first precise computation.
Belt hits rate = close encounters per body per orbit (steady.jsonl, ρ=1e-4).

## Head-math anchors already read (not predictions)

- hits/body/orbit = 5.87e-3 (steady.jsonl, converged 1e5 orbits)
- enc/body/orbit ≈ 0.039–0.041, N-invariant 1e3→1e5 (scale.jsonl)
- element swaps 1.56/body/orbit (steady.jsonl line 2)
- kicks: 32.5/orbit raw, 0.285 averaged (114×, H0190 K1/K2); plane kick 29 µs (H0210)
- program floor: 0.126 bit/body belt, 488 B per 1e6 convoy (H0208)
- caps: 8 GB unified, 4 GiB state cap (scale-ladder-v7.json), 8 cores, 60 GB/s

## Predictions (each falsifiable by budget.py output)

- **P1** Cores for kicks at 1e9 bodies, RTF 100, averaged cadence (0.285/orbit),
  today's 29 µs kick: **100–200 cores** (head: ~150). Verdict expected: FAILS the
  8-core M1 by ~20×.
- **P2** Same at RTF 1, UNaveraged (32.5/orbit): **140–220 cores** (head: ~175).
  Expected reading: tide averaging is load-bearing even at RTF 1, not a polish.
- **P3** Time to fill the 4 GiB state budget with encounter scars, zero
  reabsorption, 90-min orbits (T=5400 s), 64-bit scars: **2–10 days** (head: ~5.7 d).
- **P4** The live set S_live (bodies off program form) is capped by COMPUTE
  (kicks at RTF 100, 29 µs) at **3e7–8e7 bodies**, while memory alone would
  tolerate **4e8–7e8** scars. Compute binds ≥ 10× before memory.
- **P5** Any per-body RESIDENT candidate/pair store (≥ 16 B/body, the killed
  r8 tiers were 575 B–51.6 KB/body) exceeds the 4 GiB cap at 1e9 by **≥ 4×**;
  certificates must be program-derived (belt phase neighbours are ordinal
  neighbours, ~0 bytes) plus per-scar only.
- **P6** From raw scale.jsonl (no new runs): hits/body/orbit is ∝ ρ within 20%
  across the N sweep (scale sweep belts sit at 3.3× the steady belt's ρ, so
  0.020 there vs 0.0059 at ρ=1e-4 would confirm).
- **P7** Cross-check of a standing claim (board: "1e9 ships in 90-min orbits ≈
  190 cores"; H0190: 0.6 core/M unaveraged, 0.01 averaged): my independent
  reconstruction from 29 µs × 32.5/orbit lands in **140–220 cores** at RTF 1
  (i.e. agrees with 190 within 30%).

## What I expect the decision table to say

Memory is NOT the binding constraint at 1e9 for session-scale play (hours to
days of headroom with zero reabsorption); kick cadence × kick cost is, and it
decides the allowed live set. If P3 or P4 come out the other way (memory binds
first), that kills the "programs + scars" memory design at 1e9 and the run
reports that instead.
