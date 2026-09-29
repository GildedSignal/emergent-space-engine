# Gravity law `es-lattice-gravity-v1`: contract

Status: **draft** (29 September 2026, H0195). The gates freeze only after GLM's red-team and the float premise probe below. The v0 contract (exact continuum floors, H0184–H0194) is retired: its evaluator, the Arb judge (`artifacts/evidence/g2-reference-20260928/`) and `xtask gr-oracle` now serve as the **oracle**, which measures behaviour. None of them is the implementation.

## Principles

- **The law is a fixed integer algorithm,** like the lattice's collision law. "Exact" means bit-identical on every machine, thread count, partition and event order. It does not mean equal to continuum GR.
- **The oracle is exact GR.** Gates judge behaviours and error type against it, never bitwise continuum floors.
- **Only changes cost.** A body pays at events. Observables (clocks, redshift, lensing, delays) are derived when queried, never evolved.

## Space flows (river coordinates)

In lattice units (positions in quanta, time in chronons, c = Q):

    ds² = −Q² dT² + |dX − β dT|²

β is the flow of space. For one static mass M: β = −Q √(2M/r) · X/r.

- Let u = v − β, the velocity relative to the flow. Local physics is the lattice's special relativity applied to u: contacts, and the speed limit |u| < Q.
- **Clocks** follow dτ/dT = √(1 − |u|²/Q²), evaluated on demand.
- **The horizon** is where |β| = Q.
- **Coordinate light speeds** fill the disc of radius Q around β, so dependency bounds use Q + max|β|.
- **With no source,** β = 0 and the law is today's lattice exactly.

## The law (v1)

**Body state:** integer x and k (quanta per chronon), mass, cell, the error-feedback carries on E and L, and the time of its last event.

**Cells** are the event core's density-sized cells. Each holds:
- the integer mass moments of what it contains, as sums that commute: exact and independent of order;
- a **field record** with a certificate: "valid until the source moments change by more than ε", with ε a fixed integer threshold.

In step 2 the field is the single source's analytic flow, so its certificate never expires. In step 5 it comes from a hierarchical multipole solve over the cells, with moments read at the retarded time.

**Motion between events** follows a fixed, time-symmetric integer drift-kick algorithm in the cell's field:
- A step lasts Δ = a fixed function of the body's integer state: a fraction η of the local dynamical time, clipped to the next cell boundary or certificate expiry.
- Within a step, the body drifts straight in the local sheet. At the step boundary, the change in tilt is applied as an integer velocity kick.
- Rounding uses error feedback on the carried E and L. It stayed bounded in H0190.
- **The implementer writes the exact algorithm in the crate before the first gate run:** the integrator and its order, η, the step rule, the rounding recipe and the horizon test. That text is the law.

**Events:** a body's own step boundary, a cell crossing, a field-certificate expiry, a contact (step 6 onward), a command.

**The horizon:** a body whose step would reach r ≤ 2M is absorbed at that step's chronon. Its E and L go to the source's ledger, and nothing is evaluated inside.

**Light** follows the same law with |u| = Q, starting from an anchor direction.

**Queries** never change state. Reading a position between events evaluates the current drift.

## Step 2 scope

One static mass, with test bodies and light, in the equatorial plane. No contacts. Ranges: per component |x_c| ≤ 2^96, 1 ≤ M ≤ 2^80, Q ≤ 2^40, |T − T0| ≤ 2^80. Intermediate products use arbitrary-width integers.

## Premise probe (float, run by GLM before the freeze)

This is the cheapest falsifier: a 64-bit-float version of the law with a time-symmetric drift-kick in the Schwarzschild river flow, measured against `gr-oracle`. **Kill criteria,** each on its own:
- no η at or below 1/64 (with the probe's best integrator order) keeps precession within 1% of GR at p = 20M and p = 1000M;
- the energy error grows with an exponent above 0.2 over 10^4 orbits;
- the capture threshold at E = 1 lands more than 1% from L = 4M;
- deflection at b = 10M lands more than 1% from GR.

The probe also reports events per orbit against p.

## Gates B1–B9 (freeze after the red-team and the probe)

Each test runs in under 60 s. Cost is measured the way the player runs it, with the thermal, power, swap and load state recorded. **The cases:** the oracle's G2.2 anchors (bound, (p − p_sep)/p ≥ 10^-4), its G2.4 horizon cases and its light anchors, plus long-run cases.

**Rungs,** each passing before the next runs: circular → radial infall → eccentric → light → horizon → long runs.

| Gate | What must hold |
|---|---|
| **B1 Error type** | Over 10^4 orbits, E and L have a growth exponent ≤ 0.2 and a maximum relative excursion ≤ 10^-6 |
| **B2 Precession** | \|Δφ_law − Δφ_GR\| ≤ 1% of Δφ_GR + 10^-6 rad per orbit, for p ∈ [10M, 10^4 M] |
| **B3 Periods** | Radial period in coordinate time within 0.1% |
| **B4 Light** | Deflection within 1% for b ≥ 10M; capture iff b < 3√3·M, with a ±1% band |
| **B5 Capture** | For E = 1 inward anchors: absorbed iff \|L\| < 4M, with a ±1% band |
| **B6 Horizon** | The absorption chronon lies within one step of the oracle's ⌈T_h⌉, and nothing is evaluated at r < 2M |
| **B7 Derived clocks** | Static and circular rates at a given state agree with the oracle to 10^-9 |
| **B8 Determinism** | Bit-identical across 3 runs, 1, 4 and 8 threads, and different cell partitions; queries never change results |
| **B9 Cost** | At p ≥ 10M, isolated in a static field: ≤ 512 events per orbit and a median ≤ 2 µs per event on the M1. That is about 0.1 core for a million ships in low orbit |

## Division of the work

- **Astra:** the integer algorithm and its written law, in a new crate `crates/gravity` that Astra owns.
- **Sonnet:** the behaviour harness `xtask gravity-behave`, run against the oracle.
- **GLM:** red-teams this contract and runs the premise probe, both before the freeze.
- **The integrator:** this contract, the merges and the journal.

## Later steps (direction, not frozen)

- **Step 5, many bodies.**
  - Cells hold multipole sums, and a hierarchical solve builds the field (FMM on the cells), with moments that are polynomials in time read at the retarded time, including source-velocity terms (Laplace aberration).
  - Certificates expire only when the moments change beyond ε.
  - Binaries, transfers, oblate parents and fleets need no special formulas.
- **Step 6: one engine.**
  - The modes merge; chronon survives only as a test judge.
  - The law enters the engine.
  - Contacts happen in the flow frame, with an integer β at the contact from an exact isqrt of 2MQ²/r.
- **Kerr:** Doran flow, with twist. **Inspiral:** field energy loss. **Merger:** a single event.
