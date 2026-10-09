# Dossier: H_live decided by Fermi audit — ship-class belts create zero distinctions; the floor is 16 MB at 10⁹

## Claim

At the goal's 10⁹ scale, mutual gravitational encounters between ship-class bodies are sub-quantum by ≥9 orders of magnitude, so population belts of light bodies are closed programs that never scar; H_live is created only by discrete-outcome events (contacts, decisions, the player) at ≤10⁴ bits/game-second independent of N — bounded iff event history is reabsorbed (the digest layer is load-bearing) — and the ALU budget for the whole 10⁹ is ≤1.3 cores worst-case, so the board's "190 cores" line is stale or mis-scoped, not a live constraint.

## Bottleneck

Board risk "Distinctions created per game-second (H_live): they, not the body count, decide whether 10⁹ fit in 8 GB; **not measured yet**" and lens item 2. This run replaces the missing measurement's *prediction*: it derives what the b-h-live instrument (queued) should read and which term binds, before that build exists. Expected gain: it deletes the fear that 10⁹ populations leak information, and it retires one stale budget number.

## Evidence

All commands from the repo root, each ≤60 s wall (`verify a` 27 s, `verify d` 21 s, script 0.1 s):

```
cargo run --release -p emergent-encounters --bin encounters -- verify a   # truth rates
cargo run --release -p emergent-encounters --bin encounters -- verify d   # dense belt
python3 lab/results/20261008-2349-fermi-c55d/fermi_hlive.py               # full audit -> fermi_hlive.json
```

**Rates (the repo's own truth):** encounters per body per orbit at ρ=1e-4: σ_e=1e-3 → 1.75e-4; 3e-3 → 6.8e-4; 1e-2 → 1.89e-3; 3e-2 → 4.96e-3 (∝σ_e^~1); at ρ=3e-4, N=3000 → 1.74e-2 (ρ² law, 9.2× for 3×ρ; N-independent at fixed density). Method stayed exact (missed 0, false 0) with 1.19 exact checks per encounter.

**Scarring (exact hyperbolic impulse; control: linearized Δa/a=2Δv_t/v_K vs exact Kepler restart, worst rel-err 0.21% over 200 cases; MC first-passage matches analytic):** per-encounter median Δa/a at ρ=1e-4: m/M=1e-27 (10³-kg ship) → 2.8e-21; m/M=1e-12 (Ceres-class) → 2.8e-6. First crossing of element quantum q (rate 1.89e-3/body/orbit):

| m/M | body | horizon @ q=1e-12 | horizon @ q=1e-9 |
|---|---|---|---|
| 1e-27 | ship | 5.9e18 orbits | 5.9e24 orbits |
| 1e-21 | 4×10⁸-kg station | 8.4e6 orbits | 8.4e12 orbits |
| 1e-15 | 100-km body | 1 encounter | 1 encounter |

Ships and stations never scar on any game horizon (age-of-universe ≈ 4×10⁹ orbits at 1 AU), for any quantum ≥1e-19 relative — a 9-order margin over any plausible element quantum. Heavy belts (m/M ≥ 1e-15) scar per encounter and must live as event-logged populations (they are individually few).

**Budget at 10⁹, 1 AU, rtf 100** (cloud ns are x86; orders only): programs 15.75 MB (0.126 bits/body, gold components-98bc); all-tubes would be 16 GB (exception fraction must stay <26.8% of a 4 GiB budget); kicks 1,014/game-second → 0.03 cores at 300 ns; encounters at fixed surface density 6/game-second → 0.0013 cores even at today's unamortized 4.2×10³ evals/encounter; ship-ship contacts at 1 m radius: 2.7×10⁻¹⁴/game-second (never); player 10 bits/game-second. The only multi-core term is a fixed-extent crush (10⁹ bodies in one 0.5-AU belt at ρ=1.5×10⁴ km): 1,258 cores unamortized — but that is the already-owned concentration risk (taleb-09b5, q-candidate-degree), not a population-physics floor.

**History retention:** at the top of the event-rate range (continuous fleet warfare, ~10⁴ bits/game-second at rtf 100), retention-∞ history is 10.8 GB/day — it breaks 8 GB; player-rate history (10 bits/game-second) is 86 Mb/day. Boundedness therefore hinges on hierarchical reabsorption (the news/digest layer), exactly as plane.md says.

## Predictions

`predictions.md` P1 (rates ~300 and ~30 encounters; truth 189 and 35 — inside bands, σ_e-scaling predicted 10×, measured 10.8×) and P5 (dense belt ~1000; truth 1042, +4%) both held. P2 (Ceres-class scars instantly, ships never) held. P3 (ALU ≤0.1 core kicks, ≤0.01 encounter at fixed density) held; the 190-core board line could not be reproduced within 10× from below under current-law assumptions. P4 (creators = discrete events + player; gravity of light bodies = 0 bits) stands as derivation; the instrument check is the next run's job.

## What would make it wrong

- Planet-driven chaotic diffusion (resonance overlap) can scar belt bodies regardless of mutual mass. Information-theoretically it stays derivable from stored field history, so it shifts recompute-vs-store economics, not the floor — but if the b-h-live instrument reads nonzero belt H_live growth at ship masses, my sub-quantum argument failed somewhere.
- The 2-D planar belt ignores inclinations; 3-D spreads encounters thinner (my rates err safe).
- Timing constants are x86 orders of magnitude; the M1 re-measures (lab rule).
- If the integrator's 190-core figure encoded a specific dense fixed-extent scene, it is not "wrong" — it is that scene's number; the fix is to re-scope it, not delete the measurement.

Cost of adopting: none as code; it is a design input. It tells `b-h-live` what to expect (belt gravity ≈ 0; contacts/thrust dominate), tells B18 that belt memory is programs + event log with no per-body leak, and flags one board number for retirement.

## Fit with PRINCIPLES

P3 "Compute only surprises… nothing is evolved that can be derived" and P6 "Store the generator, not the generated": the belt is the generator, and the audit shows nothing forces it to grow. P24 "The memory floor is information": the floor at 10⁹ is ~16 MB of programs, not 16 GB of tubes. P10 "Measure before claiming": rates come from the repo's own truth, not my formula alone.

## The lens

Fermi lenses see populations and rates, not representations: I priced encounters as impulses (Öpik-style; the compute-starved planet-formation school — skin in the game) and may under-weight what the Binet-cone representation already deletes. I did not test resonance-driven diffusion numerically, and the game-time/real-time mapping enters only through rtf=100; a much faster universe scales all per-game-second rates linearly. The held-out predictions were rate-shaped, not point claims — a checker should demand the ρ² and σ_e exponents, which are the load-bearing part.
