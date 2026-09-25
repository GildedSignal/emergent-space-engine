# Test ladders

Julien, 25 September 2026: test like a Spartan trains — harder than the war. Extremes inform the mean.

## Rules

1. **Every capability gets a ladder.** Rungs are frozen before they run, and each is roughly 10× harder on the dimension it stresses. Climb until a rung fails. The last passing rung is the supported capability. The first failing rung, with its limiting mechanism, is the next work item. A ladder with no failing rung has not been climbed far enough.
2. **Two kinds of rung, both required.**
   - *Extreme:* one dimension pushed to its limit, everything else trivial. This finds which dimension breaks and how cost scales along it.
   - *Chaotic:* many mechanisms interacting at goal scale, with cascades, crowding and sensitive dependence (like 1B ships over 10B years with wars in them). This finds what breaks when mechanisms meet.
3. **A test that cannot fail is not evidence.** Easy fixtures (one shared velocity, parallel lanes, isolated bodies) are controls, not rungs. Example: the population benchmark passed at 10B ships because every group shared one velocity. The first run with any relative motion made the collision search compare every pair of groups ([H0156](HISTORY.md)).
4. **Build worst cases on purpose:** exact ties, grazing tangencies, simultaneous events, crowding on both axes, huge rational operands, near-light speeds, chaotic dynamics.
5. **Correctness before speed.** Small rungs compare against an independent materialized reference. Large rungs keep invariants, replay and digests. A fast wrong answer is a failure.
6. **Report per rung:** pass/fail and limiter; independent descriptions K; new distinctions per unit time; pair checks per description; memory per description (process RSS, not serialized bytes); cost per new distinction; worst cooperative slice against the 5 ms bound. Existing rules still apply: freeze first, never weaken a threshold, keep every failure.

## Scale ladder v1 — frozen and climbed

Frozen manifest: [scenarios/scale-ladder-v1.json](../scenarios/scale-ladder-v1.json) (sha256 `ccaf6374…`, frozen before any rung ran). Runner: `cargo run --release -p xtask -- ladder <out-dir> [track]`; each rung runs in its own process with a 120 s and 4 GiB cap. Results after the H0157 fixes ([run](../artifacts/evidence/scale-ladder-v1-20260925/contact-fixes/ladder.json), C1 re-run after the retest fix in [this run](../artifacts/evidence/scale-ladder-v1-20260925/retest-lookup/ladder.json)):

| Track | Kind | Last pass | First fail and limiter |
|---|---|---|---|
| X1 relative motion (independent bodies, random velocities) | extreme | 65,536 bodies, 257 contacts equal to the exact oracle; 5.9 s; pair checks per body grow ~N^0.5 | 262,144: engine accepts the world, then refuses at the first contact (100,000 resident-body cap) |
| X2 horizon (4,096 bodies) | extreme | 4,096 ticks | 262,144 ticks: every whole-horizon box overlaps, 1M job cap |
| X3 crowded both axes | extreme | 65,536 bodies, 0 contacts, but 537M pair checks (quadratic), 19 s | not reached |
| X4 near-miss lattice (1M-member lanes) | extreme | 16×16 lanes, 0 contacts, 14 s | 64×64: family refinement hits the 1M job cap after 117 s |
| C1 packed stop cascade | chaotic | 4,096 bodies, 2,372 contacts, replay equal; 9.8 s | 16,384: 120 s wall cap (6,878 events done) |

Not a gate in v1 but failing its target everywhere: the worst single slice of 100,000 charged operations took 0.1–7.9 s against the 5 ms cooperative target, so a charged operation is not bounded work.

Proposed extreme rungs still to add: near misses and grazing tangencies between independent bodies; real contacts 1 → 1e6; breaking one group apart 1 → 1e6; independent descriptions to the memory wall; signals and receptions 1 → 1e6 observers; 1e6 course changes on one ship. Proposed chaotic rung: the goal scene (1B ships in groups over 10B years with war islands, burns, signals and policies).

## Day-to-day climbs: scale ladder v3

Run `cargo run --release -p xtask -- ladder <out-dir> [track]` for the quick profile (8 s per rung, 90 s budget; the first climb took 54 s) or add `--full` (120 s per rung) for qualification. Manifest: [scale-ladder-v3.json](../scenarios/scale-ladder-v3.json). v2 ([manifest](../scenarios/scale-ladder-v2.json)) sampled smoothness only during the first 2 s and ran the exhaustive audit at 256 bodies (~40 s), so v3 times every frame of the whole run at the observatory's 24-operation budget and scopes the audit by profile (quick 64 bodies, full 256). Every rung reports frame p50/p95/p99/max, frames over 5 ms, and cores used.

First v3 quick climb ([summary](../artifacts/evidence/scale-ladder-v3-20260925/quick-baseline/summary.txt)): p99 frames stay under 2 ms everywhere, but single frames reach 29 ms (X1 65,536) and 138 ms (C1 4,096), and dense scenes need hundreds to thousands of frames per simulated tick. Every rung used one core of eight.

## Scale ladder v4: the trapped gas

[v4](../scenarios/scale-ladder-v4.json) adds three gas tracks under the elastic law (H0159). **C2** is the trapped-gas climb, 64 → 16,384 ships. **X5** runs the 64-ship gas longer and longer. **X6** is the same gas with exact fractions.

Each gas rung is checked against an independent integer reference simulator ([gas.rs](../xtask/src/gas.rs)) plus scalable invariants: containment, exact momentum and energy ledgers, and bounded energy leftovers.

First quick climb ([summary](../artifacts/evidence/scale-ladder-v4-20260925/quick-1/summary.txt)):
- C2 passes at 64 ships and fails the 8 s cap at 256.
- X5 fails the cap at its first rung (4,096 ticks).
- X6 fails at 16 ships, with 406 ms p99 frames as the fractions grow.

On the reference alone ([endurance](../artifacts/evidence/scale-ladder-v4-20260925/gas-endurance.txt)), energy drift stays within ±0.11% through 1.3 million collisions, and no ship's leftover exceeds 0.00044.

## Physics ladders (after the gravity contract)

Same rules, swept over dimensionless numbers: field strength ε, v/c, mass ratio, eccentricity, and time spent together relative to the orbital period. Extreme rungs push one number at a time. Chaotic rungs include three-body scattering, dense galaxy-like populations with changing fields, and a ship steering an asteroid over many orbits.
