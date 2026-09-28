# Emergent Space — handoff

Current as of 28 September 2026 (H0187). The previous handoff, with the old engine's status (H0100–H0164), is in git history and in `~/Research/emergent-space-archive/old-lineage/docs/HANDOFF.md`.

## First ten minutes

1. Read [AGENTS.md](../AGENTS.md), then this file. Run `cargo xtask history list` and search for entries related to your task.
2. Read the heading-check card `~/.cursor/skills/heading-check/cards/emergent-space.md`, then preflight.
3. Run `git status --short` and `git log -8 --oneline`. There is one checkout, `~/Research/emergent-space`, on `main`.

## What the engine computes

Only surprises. The state is certified generators, compute follows entropy, and priority is least slack. See [engine.md](engine.md).

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

Gates are frozen before their first run, tests take ≤ 60 s, and speed is reported as a real-time factor, measured like the player (heat included, state recorded). Work runs one job at a time; parallel work is limited to read-only briefs and independent judges.

0. **Clean countertop (done, H0182).**
1. **The oracle (partial, H0183).** Every single-mass row passes. The e = 0.5 two-body period rows fail with a clean p⁻² residual; the failure is kept. Before step 3 uses them, freeze a new protocol on unseen cases.
2. **One mass, in the lab** (running). The contract is [gravity-law.md](gravity-law.md): river coordinates, the canonical ladder, and gates G2.1–G2.5, with rungs R0–R5, planted bugs and ranges up to galactic nuclei (H0184, H0187).
   - Astra builds `crates/geodesic`.
   - The judge's reference floors come from python-flint/Arb (`.venv`), precomputed and frozen.
   - Sol's harness is paused.
3. **Premise probe, before any more building.** A float probe with frozen kill criteria: star, planet and moon, low orbits, a Hill-sphere transfer, a near-equal binary, one oblate parent. It measures kicks per orbit, `position` calls per second, handoff jumps, and what averaging known tides saves.
4. **The player slice** right after step 2: one mass, one ship, thrust as kicks, a float viewer, save and replay. Julien predicts before each run.
5. **Many bodies:** parent hierarchy, the kick rule (continuous integral, error-feedback re-anchoring, averaged tides), retarded tides with source-velocity terms, canonical handoff. Oracle: 1PN N-body.
6. **Collapse the modes, then put the law in the engine.** Keep the chronon judge plus one production engine (regions with a per-region batch-window dial; Metal only for dense contacts; canonical formulas on the CPU). Then add `es-lattice-gravity-v0`, thrust as kicks, and contacts in the flow frame.
7. **Scheduling from surprise:** least slack, fed by measured surprise rates (the formula's residual plus entropy).
8. **The player, fully:** commands, signals and observation on null geodesics, and the viewer.
9. **Physics v1:** Kerr, inspiral, merger.
10. **Ladder v8:** physically scaled scenes reporting real-time factors.

**Candidates from the polymath scan** (GLM, 28 September):
- commutative-monoid messages between regions;
- largest-remainder splits;
- choosing the error-feedback kernel by its low-frequency error;
- a replay-bisect tool for divergences;
- an LSM or CRAM-style body store for the memory floor.

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

Swap runs near its 10 GB limit in daily use, and timing swings about 30% with heat. Measure in real conditions, with the state recorded. Eight probes of at most 60 s each are pending for a quiet machine: i128 throughput on performance versus efficiency cores, GPU u32/u64/u128 cost, memory bandwidth, SSD streaming, the GPU round-trip floor, Accelerate/AMX exactness and throughput, Neural Engine latency, and a thermal metronome.

## Where things are

- Frozen evidence: `artifacts/evidence/`. The map for relocated or archived journal paths: [history-evidence-map.json](history-evidence-map.json).
- Remote (private): https://github.com/GildedSignal/emergent-space-engine, `main` only.
- Retired code and the old repository: `~/Research/emergent-space-archive`.
- Original conversations, research and aesthetic references: [reference/](reference/README.md) and `assets/reference/`.
