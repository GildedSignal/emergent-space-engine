# Predictions (written before the decisive runs)

Held-out cases: I have not run `verify` on this checkout, and the numbers below come
only from derivations (Öpik-style encounter rates, impulse scattering), not from the repo's
truth. Graded against `cargo run --release -p encounters -- verify a` (and `d`) and the
script's measured deltas.

## P1 — Encounter rate on the repo's belts

For the belt `r8like-s1e-2-r1e-4` (N=1000, σ_e=1e-2, ρ=1e-4, a∈[1,1.5], 100 orbits),
my Öpik-style estimate:

  r_enc ≈ n₃d · π ρ² · (v_rel · T) ≈ 3e-3 per body per orbit

so truth_enc ≈ 1000 · 100 · 3e-3 = **~300 encounters** (band 30–3000, i.e. ±10×).
For `r8like-s1e-3-r1e-4` (σ_e=1e-3, colder, 200 orbits): v_rel and thickness both fall
with σ_e, so the rate falls roughly like σ_e → I predict **~1/10 of the σ_e=1e-2 rate per
orbit** (truth_enc ~ 30 over 200 orbits, band 3–300).

## P5 — ρ² tube law on the dense belt (added after `verify a`, before `verify d`)

`verify a` returned truth rates 1.75e-4 (σ_e=1e-3) and 1.89e-3 (σ_e=1e-2) per body per
orbit at ρ=1e-4 — both inside my stated bands (P1 holds). The 2-D tube area law says the
rate scales as ρ² at fixed σ_e. For `dense-n3000-s1e-2-r3e-4` (N=3000, ρ=3e-4, 20 orbits)
I therefore predict 1.89e-3 × 9 × 3000 × 20 ≈ **~1000 encounters** (band 100–10,000).
## P2 — Deflection per encounter (the scar condition)

With GM=a=v_K=1 units: b₉₀ = (m/M)/v_rel². At v_rel ≈ 1.4e-2 and mid-tube impact
b ≈ ρ/2 = 5e-5:
- m/M = 1e-12 (Ceres-class in a solar system): Δa/a per encounter ≈ **3e-6 to 1e-5**.
  A belt of such bodies scars immediately (crosses any element quantum ≥ 1e-9 within
  ~1 orbit of accumulated encounters per body); it must live as program+refit, not tubes.
- m/M = 1e-27 (10³-kg ships around a sun): Δa/a ≈ **1e-21**. Random walk over 1e10
  orbits: σ ~ 1e-21·√(3e7) ≈ 5e-18 — **never crosses a 1e-9 quantum. Ships cannot scar
  each other gravitationally**; their mutual-encounter distinctions are exactly zero bits.

## P3 — The ALU claim ("10⁹ orbiting bodies ≈ 190 cores")

Re-derived with the current law (no ticks, 32 kicks/orbit, encounters certified per pair
with ~1 check per real encounter): at 10⁹ bodies, 1 AU orbits, rtf 100, I get
**≤ 0.1 core** for kicks and ~1e3–1e4 encounter-checks/s (**≤ 0.01 core**). If my estimate
is right, the 190-core figure is stale (pre-pivot, tick-based engine) by ≥ 3 orders of
magnitude, and the binding constraint at 10⁹ is memory (H_live), not ALU.

## P4 — What creates H_live at all

In a deterministic universe, only events whose outcome is not derivable from stored
shared state create information: discrete-outcome events (contacts, captures, merges,
deaths) and the player. Gravity-scattering deltas are derivable from (program, field
history) for light bodies (sub-quantum, P2) and for massive bodies act through the shared
multipole field (aggregate updates, O(log) bits amortized over N). So I predict:

  H_live creation rate ≈ player + c-bounded discrete events ≈ 1e3–1e4 bits/game-second,

independent of N. The scar store is then a *cache* (recompute-vs-store economics), not
information; the memory floor is programs + true-event bits.
