# Predictions (written before the decisive experiment)

Run: 20261011-1917-fermi-b946. Question: at 10⁹ bodies on the 8 GB M1, which budget
term breaks first — event compute, memory bandwidth, or memory capacity via H_live
(distinctions created per game-second)?

## Inputs taken as measured (not predicted)

- Kick cost today: 29 µs (H0210), of which 92 % is window setup (gold 20261006-0737),
  so the kick floor is ≈ 2.3 µs.
- Kicks per orbit: 32.5 raw, 0.285 with quadrupole averaging (H0190 K1/K2, 114×).
- Belt program: 0.126 bits/body (gold components-98bc). Tube store: 16 bytes/body.
- M1: 8 GB unified (~5 GB safely usable for sim), ~60 GB/s, ~10¹⁰ simple ops/s (board).
- LEO period ≈ 5.4 ks; belt period at a ∈ [1, 1.5] AU-like units ≈ 1 year ≈ 3.15×10⁷ s.

## Predictions, held out (not tuned on)

P1. Encounter rate (the H_live creation rate input), steady belt n=1000, σ_e=0.01,
    ρ=1e-3, a∈[1,1.5]: hits per body per orbit in [0.3, 5] (Fermi: circular-shear
    conjunction count ≈ 4; eccentricity spread and the ρ geometry reduce it; r8 v2's
    belt-0 measured 1.1 for its own definition).

P2. Density scaling: at fixed a-range and ρ, hits per body per orbit scales linearly
    in n (n σ v at fixed volume): steady n=3000 gives 3× the n=1000 rate, within ±30 %.
    Held out: I will not tune anything on the n=3000 result.

P3. ρ scaling: hits per body per orbit ∝ ρ^α with α ∈ [0.7, 1.3] (shear-dominated 2D
    conjunction geometry: rate set by a radial window, so near-linear, not ρ²).
    Held out: ρ=1e-4 vs 1e-3.

P4. Compute at 10⁹, all bodies in LEO, 1× real time:
    - raw 29 µs kicks, 32.5/orbit → ≈ 170 core-equivalents (re-derives the board's
      "about 190 cores" from first principles);
    - setup fix alone (2.3 µs) → ≈ 14;
    - averaging (0.285/orbit) + fix → ≈ 0.1 core. Belt scale: ≈ 10²–10³ kicks/s total,
      ≥ 5 orders below the machine.
    So after the two already-measured levers, compute clears at BOTH scales.

P5. Bandwidth: a per-frame touch of every body (60 FPS, 64 B read) needs ≈ 3.8 TB/s,
    64× over 60 GB/s. Events are fine (≤ 10⁹ events/s at 64 B); full sweeps are not.
    "No ticks" is a bandwidth law, not a preference.

P6. Capacity is the term that breaks first, three ways at 10⁹:
    - tube store: 16 GB > 5 GB usable (≈ 3× over);
    - one pending event per body (16 B): 16 GB (≈ 3× over) → the event queue must be
      sublinear in N, i.e. per-body events must be absorbed into generators;
    - scars: with P1's rate ≈ 1/body/orbit, unreabsorbed 16-byte scars add ≈ 16 GB
      per orbit of play. Only reabsorption (canonical microstates + program
      recompiles) holds the steady state near the program floor.
    Verdict: H_live reabsorption, not compute or bandwidth, is the binding constraint
    at 10⁹; the compute ask ("10–100× less") is already met on paper by measured
    constants (12× setup, 114× averaging, event-driven work).

P7. If P1 comes back > 10× my Fermi number, my conjunction geometry model is wrong
    and I report which term of n σ v failed, not the conclusion.

## Decisive experiment

`cargo run --release -p emergent-encounters -- steady <n> <rho> <orbits>`
for (n, ρ) ∈ {(1000, 1e-3), (3000, 1e-3), (1000, 1e-4)}, plus the budget arithmetic in
`budget.py`. Orders of magnitude only (Linux/x86 host, shared).
