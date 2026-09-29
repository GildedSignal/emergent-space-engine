# Test ladders

Julien: "test like a spartan would train, harder than for the war"; "extremes inform the mean" (25 September 2026); "even baby spartans started 'small'" (28 September).

## Rules

1. **Every capability gets a ladder.** Rungs are frozen before they run, and each is roughly 10× harder on the dimension it stresses. Climb until a rung fails. The last passing rung is the supported capability. The first failing rung, with its limiting mechanism, is the next work item. A ladder with no failing rung has not been climbed far enough.
2. **Two kinds of rung, both required.**
   - *Extreme:* one dimension pushed to its limit, everything else trivial. This finds which dimension breaks and how cost scales along it.
   - *Chaotic:* many mechanisms interacting at goal scale, with cascades, crowding and sensitive dependence (like 1B ships over 10B years with wars in them). This finds what breaks when mechanisms meet.
3. **A test that cannot fail is not evidence.** Easy fixtures (one shared velocity, parallel lanes, isolated bodies) are controls, not rungs. Example: the population benchmark passed at 10B ships because every group shared one velocity. The first run with any relative motion made the collision search compare every pair of groups ([H0156](HISTORY.md)).
4. **Build worst cases on purpose:** exact ties, grazing tangencies, simultaneous events, crowding on both axes, huge rational operands, near-light speeds, chaotic dynamics.
5. **Correctness before speed.** Small rungs compare against an independent materialized reference. Large rungs keep invariants, replay and digests. A fast wrong answer is a failure.
6. **Report per rung:** pass/fail and limiter; independent descriptions K; new distinctions per unit time; pair checks per description; memory per description (process RSS, not serialized bytes); cost per new distinction; worst cooperative slice against the 5 ms bound; utilisation and the real-time factor. Existing rules still apply: freeze first, never weaken a threshold, keep every failure.
7. **Behaviour over many seeds.** Julien: "if you're actually testing behavior or the bad idea of expecting the same data". Behaviour gates draw many seeds from a frozen sampler over the dimensionless numbers and judge the distribution; one seed's data is never the target. Determinism is checked per seed, bit for bit.

## Current ladder: v7

[scenarios/scale-ladder-v7.json](../scenarios/scale-ladder-v7.json), frozen in H0175 under law es-lattice-relativistic-v1. Ladders v1–v6 and their evidence are in the journal (H0156–H0169); their code is archived (H0182).

- **Tracks.**
  - Extremes: X1 relative motion, X2 horizon, X3 crowded axes, X4 near-miss lattice and X5 carry endurance.
  - Chaotic: C1 packed stop cascade, C2 trapped gas, C3 mixed invariance and C4 near-c mixed.
  - Galaxy: G1 galaxy clusters and G2 galaxy span.
- **Modes.** chronon (the reference), event, metal, hybrid and regions, until they merge into one engine ([engine.md](engine.md)). Every mode must reproduce the chronon digests where invariance runs.
- **Climb.** `cargo run --release -p xtask -- ladder7 <out-dir> [track] [--modes=...] [--full]`. One rung: `... ladder7-rung <mode> <track> <rung> quick`. Every rung runs in its own child process, under one minute.
- **Gates.** empty_space_free, cost_per_event_flat, smooth, useful_work, gas_one_million and galaxy_one_million. Last climb: H0180, with H0181 for the hybrid.

Ladder v8 adds gravity and physically scaled scenes, reported as real-time factors. See the plan in [HANDOFF.md](HANDOFF.md).

## Physics ladders (after the gravity contract)

Same rules, swept over dimensionless numbers: field strength ε, v/c, mass ratio, eccentricity, and time spent together relative to the orbital period. Extreme rungs push one number at a time. Chaotic rungs include three-body scattering, dense galaxy-like populations with changing fields, and a ship steering an asteroid over many orbits.
