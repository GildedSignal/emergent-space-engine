# Dossier — run 20261003-2306-system-27ce (lens: the whole system)

## Claim

The plane's kick cadence — `1/64` of every forced body's radial period, for every body, forever
(`crates/universe/src/step.rs::step_for`, `per_period_log2 = 6`) — is a magic constant, not a
certificate: measured here, gate-grade behaviour in both the weak regime (belt) and the Hill
regime (moon) survives an **8× sparser** cadence, the boundaries where it does not are measured
(resonance, m=2 aliasing at n=2, walking error type below n=8), and the naive certificate — one
velocity quantum of impulse error — is **falsified** as the sizing rule (it predicts 1.4
kicks/orbit; the walk-free floor is 8). The board's top lever should be re-scoped from
optimizing the cadence (q-correctors) to deriving it.

## Bottleneck

Board focus item 1 (kicks dominate the engine's cost; Sol measured 29 µs per kick, 15 of them
in rebinding; HANDOFF: "the bigger lever is fewer kicks"). Expected gain: 8× fewer kick events
for weakly-perturbed bodies at gate-grade behaviour (4× at near-control fidelity), adoptable
inside `step_for` — one function the plane already re-plans per interval with hysteresis. Most
bodies in any real scene are in the weak regime (principle 33, the ant and the lion).

## Evidence

Float premise probe, the lab's probe idiom (floats explore; only an integer rung decides).
`probe.py` (numpy, fixed seed), two scenes, reference = the same WH scheme at n=512
(convergence n=256↔512: max Δa/a = 3.6e-5, far below every effect reported), control = the
plane's own n=64.

Commands (cloud, 2 vCPU): `python3 probe.py belt` (~505 s, dominated by the n=512 reference —
over one 60 s command; each constituent n-sweep run is ≤ 60 s) and `python3 probe.py moon`
(~378 s). Outputs: `metrics-belt.json`, `metrics-moon.json`; the sweep rows print to stdout.

**Belt** (Sun + circular Jupiter µ=GM/1047 at 5.2 AU + 120 test asteroids, a ∈ [2.45,3.35],
dense 2:1 slice, e0 ∈ [0.02,0.2], 6,000 yr ≈ 1,150 orbits at 3 AU; non-resonant slice, 96
bodies; medians vs reference):

| n/orbit | Δa/a | Δe | apsidal-rate err | Jacobi max drift | walk exponent |
|---|---|---|---|---|---|
| 64 (plane) | 2.9e-6 | 7.5e-6 | 4.1e-5 | 6.2e-3 | +0.36 |
| 16 | 4.1e-5 | 9.1e-5 | 8.1e-4 | 2.4e-2 | −0.60 |
| **8** | **7.6e-4** | **2.1e-3** | **1.6e-2** | **5.2e-2** | **−3.30** |
| 4 | 3.6e-3 | 6.9e-3 | 1.3e-1 | 2.6 | +2.99 (walks) |
| 2 | 5.4e-3 | 1.1e-2 | 2.8e-1 | 8.3 | +1.16 (walks) |
| 1 | 1.4e-2 | 3.1e-2 | 1.03 | 2.7 | −0.01 |

At n=8 every gate-grade metric holds with margin (B14's 10% apsidal bar: 6×; B5's 1% shape
bar: 13×; resonant-pumping proxy emax error 1.0e-3), and the Jacobi error **saturates**
(exponent −3.3): sparsity traded size, not type. At n=4 the error type itself breaks.

**Moon** (the planet's doll, full differential solar tide as `force.rs` reads it; a_m ∈
{0.15,0.25,0.35,0.45} R_H, e0 ∈ {0.05,0.2}; 600 orbits — trimmed from the registered 1,500
after a debug loss, disclosed): class match (bound/escape) 1.0 at n ≥ 4; apsidal-rate error
0.08% at n=8 (the control's own is 0.43%), 6.4% at n=4 (B14-marginal), **121% at n=2** — the
pre-registered m=2 aliasing failure (antipodal sampling of the tide's quadrupole harmonic).

**Resonant slice** (2:1): degrades 3–20× faster than the non-resonant belt at the same n
(at n=4: apsidal 41% vs 13%; max-e error 0.28 vs 0.014 = 20×). Density must be kept there, as
law.md already requires for resonant kicks.

**Certificate arithmetic** (printed by the probe): the impulse-quantum rule predicts
n = 1.4/orbit (belt) and 1.2/orbit (moon) at Q = 2^20, but 141/orbit at the target Q = 2^40.
Since measured behaviour at n = 8 and n = 64 is equally gate-clean, the quantum demonstrably
does not bind at either Q — the constant 1/64 is unanchored at both ends, and the quantum is
the wrong certificate for step size.

## Predictions

`predictions.md`, five, all pre-registered before the decisive runs. Outcome: **1 FAILED**
(n=4 and n=2 do not match — the pre-registered kill criterion triggered; the impulse-quantum
certificate under-prescribes density ~6×), **2 HELD** (moon: marginal at n=4, aliased at n=2,
0.08% at n=8), **3 HELD** (resonant over-pumping, 20× on the emax metric), **4 FAILED below
n=8** (the Jacobi error walks at n ≤ 4; bounded at n ≥ 8 — the error-type gate is the
selector), **5 HELD** (the Q-scaling arithmetic, and its interpretation: quantum ≠ binding).
The two failures are the informative part: they kill "one quantum of impulse" as the step
certificate and locate the true floor at the interaction's own phase resolution, selected by
error type.

## What would make it wrong

- Only one scene pair was probed; the fleet origin and the player's tube are untested (the
  origin is moon-like and should inherit — inference, not measurement).
- The float probe's WH is per-body constant-in-time steps, matching the plane's regime; a
  certificate that re-derives the step state-dependently inside an orbit is probe 1's killed
  configuration and is explicitly not proposed.
- If the integer rung cannot realize the sparse cadence without breaking B8 determinism or the
  rebind's exactness, the 8× does not bank.

## Cost of adopting

One function (`step_for`) gains a step rule from the interaction's phase curvature (the same
tube readouts the kick itself performs); no new state, no new component. The σ-δ carry and the
sub-quantum no-op path (`dvq == [0,0]`) already exist. The named next experiment (silver→gold):
an integer rung `r-cadence` on the plane itself — step rule = phase-resolution certificate,
criteria: identical B5/B14 behaviour at ≥ 4× fewer kick events on frozen scenes (belt-like and
moon-like), walk exponent ≤ 0.2 as the type gate, negative control = the fixed 1/64 (must show
the wasted-event count), positive control = the Hill-close regime keeping ~64.

## Fit with PRINCIPLES

- 14: "no work for no reason, so no ticks… you don't advance a ship tick by tick" — the kick
  cadence is the last phase tick.
- 13 and the engine's error table: the walk at n ≤ 4 is exactly the forbidden type; the probe
  shows the type gate itself selects the floor — the certificate is the error type, not a
  magnitude.
- 19: "if you find yourself fixing things that's oftentimes a signal that it is the wrong
  representation" — correctors fix the cadence's cost instead of asking why the cadence exists.
- 33: most bodies resolve their interactions far below what 64 samples/orbit serves.
- 2: "error type over error size" — the 8× cut is taken where the type is preserved (n=8,
  saturating), and refused where it is not (n ≤ 4).

## The lens (what it may have missed)

1. **Conjunctions.** The step rule must anticipate a secondary's conjunction (|a″| spikes);
   done reactively it degrades into re-planning storms — the rung must state whether the
   encounters crate owns the lookahead.
2. **Chaos inside the doll.** Non-hierarchical bodies have no clean T0 to be "per orbit"; there
   the rotating binary doll (the r9/r4 consequence) may take over before any of this matters.
3. **The single-number trap.** An 8× mean lever hides the tail: the resonant slice and the
   Hill-close regime keep (or exceed) today's density; adoption must be per-interaction, not a
   new global constant — otherwise this run merely replaces 6 with another magic number.
