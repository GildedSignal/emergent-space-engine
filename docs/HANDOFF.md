# Emergent Space — handoff

Current as of 28 September 2026 (H0182). The previous handoff, with the old engine's status (H0100–H0164), is in git history and in `~/Research/emergent-space-archive/old-lineage/docs/HANDOFF.md`.

## First ten minutes

1. Read [AGENTS.md](../AGENTS.md), then this file. Run `cargo xtask history list` and search for entries related to your task.
2. Read the heading-check card `~/.cursor/skills/heading-check/cards/emergent-space.md`, then preflight.
3. Run `git status --short` and `git log -8 --oneline`. There is one checkout, `~/Research/emergent-space`, on `main`.

## What the engine computes

It computes the universe's events: the points where a prediction breaks, and what happens there.

**The state is certified generators.** Each generator has three parts:
- a formula (a worldline, a field, a region);
- a certificate: how long the formula stays exact;
- its dependencies: who could break it, limited by c.

**There is one operation.** Resolve the earliest broken certificate that something needs, exactly with the integer law. Then issue new formulas and notify the dependents.

**Costs follow surprise.**
- Cost is the entropy the demanded part of the world produces. For contacts that is about collision rate × log₂(2λ/r) bits; H0173 measured 4 bits per collision.
- Memory is the entropy accumulated.
- Every mode is an evaluation order of the same event graph, so all modes must be bit-identical.

## Where we are

- **Law.** `es-lattice-relativistic-v1` (H0174): exact integer special relativity with contacts, walls, carries and an exact Newtonian limit. Q ≤ 2^20 today; the target is 2^40 ([universe-quanta.md](universe-quanta.md)). Worldlines are straight between events: no gravity, no thrust, no player input yet.
- **Modes.** chronon (reference), event (H0177, density-sized cells), metal (H0179: the 1M v1 gas takes 8.0 s per 1,024 chronons), hybrid (H0181) and regions (the allocator, H0176).
- **Ladder v7** (H0180–H0181). No correctness flag is false anywhere. Failing gates:
  - gas_one_million and galaxy_one_million (at the cap);
  - useful_work for event (0.48);
  - smooth for metal, hybrid and regions.
- **GR oracle** (H0178, H0183). Periapsis advance, light bending, geodetic precession, clock rates, Shapiro delay, bound periods and 1PN two-body motion, two methods each. It shares no code with `crates/` and currently exits 1 because of the retained e = 0.5 two-body failure.
- **Real-time factors.**
  - The ladder gas is a stress test: about 10⁻⁸× real time at 83 ps chronons.
  - A realistic 1M-ship battle is estimated at 10–100× real time. That is a Fermi estimate, not yet measured.

## The plan: engine and GR

Every step has gates frozen before its first run, every test stays under 60 s, and speed is reported as a real-time factor at physical scale.

0. **Clean countertop (done, H0182).** One checkout outside iCloud, the old line archived, 55 tests, ladder rungs identical to v7 evidence.
1. **Finish the oracle (partial, H0183).** Added Shapiro delay, bound-orbit periods and 1PN two-body motion, 66 rows. Everything single-mass passes. All 12 e = 0.5 two-body period rows fail their frozen band: the residual is a clean next-order p⁻² term, and the failure is kept. Before step 3 uses two-body rows, freeze a new protocol (2PN on both sides, or a convergence-order gate) on cases never run before. Remaining here: freeze the lattice-gravity comparison bands against the Schwarzschild rows.
2. **Integer geodesic formulas plus kicks, around one mass, in the lab.** The contract and frozen gates are in [gravity-law.md](gravity-law.md) (river / Painlevé–Gullstrand coordinates). Astra builds `crates/geodesic`; Sol builds the independent reference and the gate.
   - A body's formula is the geodesic of its parent: the source that dominates by a dimensionless ratio, never a label. With no parent, the formula is a straight line (today's law).
   - Near one mass it is a closed-form Schwarzschild geodesic, evaluated by one fixed integer algorithm (elliptic functions by arithmetic–geometric mean), so it is canonical. The interface keeps a spin parameter.
   - Kicks carry only the acceleration the formula doesn't know. It accumulates in carries and is applied as an integer kick each time it reaches one velocity quantum.
   - Horizon crossing is an absorption event. Light follows null geodesics.
   - Gates: agreement with the oracle; no secular drift over 10⁴ orbits; the same bits from one jump or many steps; kicks per orbit.
   - Why this formula (Fermi, at a 0.27 mm/s quantum): a ship in low orbit needs about 33,000 kicks/s with straight lines, and one every few minutes with its orbit as the formula.
   - The old osculating-Kepler rejection (H0133) used Newtonian conics at a = 4M, inside the innermost stable orbit, with coarse kicks. This design starts from the exact geodesic instead.
3. **Many bodies.**
   - The parent hierarchy is the cell tree.
   - Tides come from multipole moments stored as polynomials in time, read at the retarded time t − D/c.
   - The tree is symmetric so momentum stays exact (Dehnen).
   - Handoff between parents is canonical, with hysteresis.
   - The aggregate mass of fleets acts as a source.
   - Oracle: a direct 1PN N-body integrator.
4. **Law `es-lattice-gravity-v0` in the engine.**
   - Contacts between curved worldlines: in a shared falling frame, relative motion is a straight line inside a tidal tube, so the existing exact first-hit test works with a certified margin.
   - Thrust enters as kicks.
   - All modes stay bit-identical, and Metal evaluates formulas and kicks in fixed point.
   - This needs wide coordinates: i128 origins with narrow local arithmetic.
5. **Entropy forecast and least-slack scheduling.** It can start after step 0, in parallel with steps 1–3.
   - One surprise rate per region: collision entropy for contacts, unknown acceleration ÷ quantum for gravity.
   - That rate drives five things: priority (slack = time until needed − forecast work ÷ throughput), the batch window (from event-driven to lockstep, replacing the mode split), cell size, hardware placement, and storage (store high entropy, recompute low).
   - Metal moves from one-chronon lockstep to multi-chronon windows.
   - The forecast steers cost only, never outcomes.
6. **The player.** Commands as kicks; signals and observation along null geodesics; save and replay; a viewer. Port the old engine's contracts, not its code.
7. **Physics v1.**
   - Kerr: equatorial orbits are closed form, with one more constant.
   - Inspiral: the Peters–Mathews drift of the orbit's constants, as kicks.
   - Merger: a single event whose outcome comes from numerical-relativity fitted formulas written as exact integer law.
8. **Ladder v8.** Physically scaled scenes, all reported as real-time factors:
   - 1M ships orbiting a spinning black hole at ≥ 1× real time with no frame over budget;
   - the same scene plus a far dense battle that least-slack scheduling must keep caught up;
   - a galaxy of 10⁹ bodies where only the player's region is current, reporting the maximum sustained time acceleration and memory.

Finish clean: once GR works in the engine, collapse the modes into one engine with the batch window, and remove what stopped being useful.

## Standing decisions

- **Microstates are canonical.** Entropy only schedules, and observation never changes outcomes.
- **Everything is emergent** (see the design principles in the reference conversations). There is no central control, and no object categories: regimes are chosen by dimensionless numbers.
- **The memory floor is information-theoretic** (entropy given shared structure), not bytes × count.

## Risks to attack first

- Canonical parent handoff without energy leaks.
- An exact integer elliptic-function algorithm, identical and fast on CPU and Metal.
- Contacts between curved generators.
- Retarded tides across very different scales.

## The machine

A fanless MacBook Air M1, macOS 26.5.2:
- 4 performance cores (12 MB L2) and 4 efficiency cores (4 MB L2);
- a binned 7-core GPU;
- 8 GB of unified memory, with 16 KB pages;
- about 10 GB of disk free.

Swap runs near its 10 GB limit in daily use, and timing swings about 30% with heat. Timed evidence needs AC power, a quiet machine and a recorded thermal, swap and load state. Eight probes of at most 60 s each are pending for a quiet machine: i128 throughput on performance versus efficiency cores, GPU u32/u64/u128 cost, memory bandwidth, SSD streaming, the GPU round-trip floor, Accelerate/AMX exactness and throughput, Neural Engine latency, and a thermal metronome.

## Where things are

- Frozen evidence: `artifacts/evidence/`. The map for relocated or archived journal paths: [history-evidence-map.json](history-evidence-map.json).
- Remote (private): https://github.com/GildedSignal/emergent-space-engine, `main` only.
- Retired code and the old repository: `~/Research/emergent-space-archive`.
- Original conversations, research and aesthetic references: [reference/](reference/README.md) and `assets/reference/`.
