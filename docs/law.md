# Law `es-space-v2`: contract

Status: **DRAFT.** It freezes when r1 has a clean PASS, r3 v3 and r4 v2 are judged, and GLM has red-teamed this text. On freeze it replaces [gravity-law.md](gravity-law.md) and [universe-quanta.md](universe-quanta.md). The design is [representation.md](representation.md); the judge is `xtask behave`.

## What the law is

A fixed integer algorithm. Exact means bit-identical on every machine, thread count, evaluation order (sparse or dense) and silicon. It does not mean equal to continuum GR: GR is the oracle that judges behaviours. Floats never decide an outcome.

## State

- **Doll:** its mass M (logarithmic form), its parent doll, its centre (a tube in the parent), and its edge radius (the sphere of influence, derived from the mass ratio).
- **Tube** (one per body or photon): its doll, E and L (integers native to the law), epoch t₀ (relative to the doll's clock), the cycle phase at t₀, and a type index (mass, radius and spectrum come from a table). About 16 bytes. Position and velocity are derived when asked.
- **Cycle memo,** keyed by quantized (E, L): the band-crossing table of one radial cycle; integer Δφ, Δt and Δτ; and ∂/∂E and ∂/∂L of each. It is shared by every tube with the same key.
- **Numbers:** 32-bit storage words and 64-bit products. Per band, fixed point with one shared exponent. Wide integers are allowed only at cycle creation. Increments and kicks are integers of the law, exact by construction (r2).

## Motion in a doll (one dominant mass)

1. **Bands:** r_k = 2^(k/m) in the doll's units, with m = 16 (r1: m = 8 is too coarse; m = 16 and m = 32 pass). The band index comes from integer bit operations on the Binet variable u = 1/r.
2. **Inside band k:** u″ + (1 − 6M·u_k)·u = M/L² − 3M·u_k², advanced in φ by an exact integer area-preserving map (a rotation for ω² > 0, hyperbolic for ω² < 0). The implementer writes the map's exact text in `crates/space` before the first gate run. That text is part of this law.
3. **Exits:** the band exit is found exactly in integers. u and u′ are continuous across bands.
4. **Time:** dt/dφ = E/(L·u²·(1 − 2M·u)) and dτ/dφ = 1/(L·u²), each integrated per band by a rule fixed by the band and by (E, L).
5. **The cycle:** after one radial cycle the crossing sequence repeats. The tube then advances by Δφ, Δt and Δτ per cycle, which is additions only.
6. **Light:** the same map without the M/L² term, parameterized by b = L/E.
7. **The horizon:** a tube whose u reaches 1/(2M) is absorbed at that event, and its E and L go to the doll's ledger.

## Events: the only places where work happens

- **Kicks.** The parent's tide and the neighbours' moments change E and L by integers. Kicks are orbit-averaged only far from resonance. Near a mean-motion resonance they keep the conjunction phase; the configuration is open until r4 v2 is judged. A kick updates the cycle through its derivatives, by a multiply-add. A full recompile happens only when the key changes.
- **Handoffs.** A tube crossing a doll's edge is re-expressed in the other doll's frame (a boost and a translation, at this event only). Carries are bounded (H0190 K4).
- **Two comparable masses.** They form one doll with M = m₁ + m₂. ν enters only through the effective-one-body energy map at 1PN. This stays open until r3 v3 is judged. Non-hierarchical regions go to the dense order.
- **Contacts:** the exact integer special-relativity law `es-lattice-relativistic-v1`, in the frame of one of the two bodies. Its carries are the rounding rule everywhere.
- **Decisions:** thrust changes the rapidity linearly in proper time; in a field, E and L change by the work done. AIs are deterministic parts of the law, recomputed when their view crosses a threshold. The player is the only seed.

## Causality and evaluation

- c = 1 cell per cell-update. An influence reaches a cell no earlier than its min-plus arrival time over cell crossings.
- **Sparse order:** jump to the earliest broken certificate, resolve it, notify the dependents. One queue, ordered by slack.
- **Dense order:** lockstep in cache for regions whose events per cell per light-crossing are near 1, inside a free-fall frame (Clohessy–Wiltshire tides to first order; members re-anchor at events).
- **Both orders give identical bits.**

## Observation (never evolved)

A clock reads its tube's length. Colour is −p·u at the observer. Positions are gathered at the observer's past light cone. Lensing takes deflection(b) from the doll's memo.

## Gates (frozen at the law's freeze; each test under 60 s; measured like the player)

| Gate | What must hold | Judge |
|---|---|---|
| B0 flat reduction | With no mass, contacts reproduce lattice v1's digests | ladder7 / chronon |
| B1 precession | ≥ 99% of 256 seeds within 1% of GR | `behave` G1 |
| B2 periods | ≥ 99% within 0.1% | G2 |
| B3 light | deflection within 1% over 64 seeds | G3 |
| B4 capture | no misclassification (massive at E = 1, and photons) | G4 |
| B5 error type | E and L growth exponents ≤ 0.2 on the median seed; shape within 1% over 10⁴ cycles; exact cycle repetition | G5 |
| B6 prograde | every advance > 0 | G6 |
| B7 clocks | derived rates equal the oracle's formula to one rounding | `behave` B7 |
| B8 determinism | bit-identical across reruns, 1/4/8 threads, CPU/GPU, sparse and dense orders | engine tests |
| B9 cost per body | ≤ 64 crossings per cycle at m = 16; after that, zero work per orbit until an event | `behave` B9 |
| B10 cost against N | frozen scenes of 10³–10⁶ bodies; fitted exponent ≤ 1.1. The real-time factor at 10⁹ is reported, and gated only once a physically scaled reference scene is frozen (ladder v8), because the scene's M/c³ time unit is not physical | `behave` B10 |
| B11 binaries | 1024 binaries (p 20–1000, e ≤ 0.6, ν ≤ 0.25), given their 1PN invariants: ≥ 99% precess within (1% + 2·8/p) of the 1PN oracle; ≥ 99% of judged seeds (next-term estimate 5/a² ≤ 5×10⁻⁴) have periods within 0.1% | `behave` B11 |
| B12 handoffs | Ships crossing a Jupiter-like planet's doll edge ≥ 20 times each (16 seeds, circular restricted three-body): the Jacobi constant's error has growth exponent ≤ 0.2 on the median seed and stays within 10⁻⁴ relative | `behave` B12 |
| B13 assists | 64 flybys (periapsis 1.2–50 planet radii, v∞ 5–20 km/s): the changes in the ship's heliocentric orbital energy and angular momentum each within 1% of the reference's, for ≥ 99% | `behave` B13 |
| B14 Hill stability | 128 moons at 0.2–0.9 Hill radii, prograde and retrograde, over 50 planet orbits: bound or escaped as the reference says, for ≥ 99% of the judged (non-chaotic) seeds | `behave` B14 |

Every gate has a positive control that must pass and a planted law that must fail.

## Who builds what

- **Astra:** the in-band map, exits, time rule and cycle compiler (running now), then the resolver's exactness and the carries.
- **Sol** (after the Codex reset): dolls, tubes, handoffs, kicks.
- **Claude:** the orders (sparse, from `lattice-event`'s `Calendar`; dense, from `lattice-metal`), memory and the queue. Claude also builds the judges of OpenAI's modules (`behave`), and OpenAI builds the judges of Claude's modules.
- **GLM:** open rungs r3 v3, r4 v2, r5 (dense order), r6 (view), r7 (AI cost), and the red-team of this text.
