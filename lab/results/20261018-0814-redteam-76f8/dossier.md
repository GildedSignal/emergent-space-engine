# Dossier: the two-orders crossover, measured (representation.md §3, L70–76)

## Claim

The premise that both evaluation orders are needed survives, but its boundary is
measured for the first time and the letter is wrong by an order of magnitude: lockstep
(the dense order's CPU arm) only becomes cheaper than the sparse event core at
**ρ\* ≈ 0.15–0.2 contacts per body per chronon (K ≈ 0.1 events per q²-cell per
chronon — not the doc's "near 1")**, a rate that in the physical range only a
**confined grind at near-touching packing (spacing ≤ 1.5q, touching = q) reaches — no
battle-shaped scene does (the densest slam is 3.3× short; the shipped battle scene's
density is ~40× short)** — while at the game's dominant density (empty flight) the
sparse core is **4,275× cheaper** (0.0002 s vs 1.037 s for the same 1600 bodies, 2080
chronons, zero events).

## Bottleneck

The board's "bodies in the flyable engine" ladder and the doc's two-orders
architecture (§3): which order each region runs under is decided by the doc's
"Knudsen-like number", and that number had never been calibrated — every prior
measurement (the shipped `cost.rs` probe, r5's bonus) sat at the battle scene's single
fixed density (5q spacing), where sparse wins 28×. The gain is not a speedup but a
**domain certificate**: it sizes the boundary in the law's own units (contacts per
body per chronon; the q×q cell, whose light-crossing is exactly one chronon since
c = 1 quantum/chronon), so the allocator can engage each order where it is actually
cheaper. Engaging the dense order by the doc's letter ("K near 1") would concede the
whole band K ∈ [0.1, 1] to the wrong order (lockstep costs 1.4–28× more there);
engaging it in battles (the doc's own example) costs 1.7–9× more than the sparse core
today.

## Evidence

One command (the runner's regen: `sh lab/results/20261018-0814-redteam-76f8/regen.sh`,
or directly `cargo test --release --test xdense the_crossover -- --nocapture`, 43–50 s,
shared x86 box, load 1.4–1.5 during the run, machine state printed in `sweep.txt`).
New file `crates/engine/tests/xdense.rs` (in `work/patch.diff`): seeded scenes on
shipped code only — `Chronon` vs `EventCore`, law `es-lattice-relativistic-v1`, q =
1024, radius q/2 for all bodies (the touching floor is exact), and **the two orders'
world+log digests asserted equal in every cell** (r5's property, extended here to 21
walled gas worlds the r5 scenes did not cover). Full table: `sweep.txt`. Key rows
(lock/sparse wall ratio; < 1 = lockstep wins):

| Scene (n=1600, T=400) | contacts/body/ch | K (per q²·ch) | lock/sparse |
|---|---|---|---|
| miss (empty flight, T=2080) | 0.000 | 0.000 | **4275×** |
| gas s=5q v=q/4 (≈ battle density) | 0.010 | 0.000 | 5.9× |
| gas s=2q v=q/4 | 0.066 | 0.015 | 1.75× |
| **gas s=1.5q v=q/4** | **0.129** | **0.050** | **1.06× (par)** |
| **gas s=1.25q v=q/4** | **0.204** | **0.112** | **0.85× (crossover)** |
| gas s=1.0q v=q/4 (touching) | 0.371 | 0.306 | 0.59× |
| gas s=1.0q v=q/2 | 0.509 | 0.421 | 0.72× |
| slam s=1.5q scatter (densest battle shape) | 0.041 | 0.017 | 2.50× |
| slam s=1.5q formation | 0.045 | 0.019 | 1.71× |

- The crossover is robust: at v = q/8 it falls between ρ = 0.126 (1.36×) and 0.264
  (0.84×); at v = q/4 between 0.129 (1.06×) and 0.204 (0.85×); at v = q/2 between
  0.211 (1.03×) and 0.312 (0.84×). **ρ\* ≈ 0.15–0.2**, i.e. K ≈ 0.06–0.11 per q²-cell
  per chronon (the Chronon's own adaptive cell is ~2q wide, so on its own cell size K
  ≈ 0.2–0.4 — still not "near 1").
- N does not move it: at fixed density (s=1.5q, v=q/4), N = 400/1600/6400 gives
  1.25×/1.09×/1.09×.
- Max lockstep win inside the physical range: 1.7× (0.59× ratio, touching packing,
  v = q/4). Sparse's ops at the grind are 2.8× lockstep's (45.8M vs 16.5M) — it does
  more, cheaper ops; lockstep wins on wall time only.
- Determinism: ops counts bit-identical across passes (16,522,351 and 45,805,416 in
  both); wall ratios stable 0.71–0.76 across load 0.4→1.5.

## Predictions

All five held (`predictions.md`, written before the run): P1 empty flight < 5% (actual
0.019%); P2 crossover inside the physical band 0.02–0.3 between 3q and 1q at v=q/4
(actual ρ\* ≈ 0.15 at s ∈ (1.25q, 1.5q)); P3 no N-flip (1.25→1.09→1.09); P4 all slam
and formation cells sparse-side (worst 1.71×); P5 ops agree in direction everywhere.
Disclosure: the first two miss-control runs leaked (elastic exchanges threw drifting
bodies across my 8q offset: 1,616 events); fixed by forcing formation velocities in
the miss arm — the final control has exactly 0 events. Nothing else was re-tuned.

## What would make it wrong

- These are scalar CPU timings on shared Linux/x86 (orders of magnitude only, per the
  lab rules). The doc's dense order targets "the GPU and NEON": a vectorized lockstep
  gaining ~8–16× would move ρ\* down toward ≈0.02–0.06 [INFERENCE, unmeasured] —
  potentially inside the densest battle shapes. The M1/Metal arm owns that
  measurement; the CPU-arm domain measured here cannot be extrapolated to it.
- The grind is sustained by a container (a box). A gravity-confined grind in the game
  may cool and drop below ρ\* before the dense order pays; the box is the worst case
  the physics allows, and it bounds the domain from above.
- Wall-clock on a shared box: the ops columns are deterministic and agree in
  direction; the ratio band across load is 0.71–0.76 on the hottest cell.
- What would kill the reading outright: a digest mismatch (none — asserted per cell),
  or the crossover moving with N (it does not).

## Cost of adopting, and fit with PRINCIPLES

Adoption is a doc edit plus a frozen cost rung: correct §3's "near 1" to the measured
K ≈ 0.1 (contacts/body/ch ≈ 0.15–0.2), and move the letter's example from battles
("the normal case of many necessary interactions") to confined grinds at
near-touching packing — no fleet battle reaches the boundary. Fit: principle 22, "the
simulation tells us what's next not us" — the Knudsen number must be measured from
the world, and now it has a calibrated CPU-arm boundary; principle 1, "the cheapest
compute is compute not done" — the 4,275× empty-flight row is the sparse certificate
doing exactly that at the game's dominant density; and the board's rule that gates
"derive the representation native to the operations at stake" — the boundary is
expressed in the law's own units (q²-cells, one-chronon light crossing), not in
machine units.

## The lens

A premise red-team overweighting exotic cases is the standing blind spot: the
touching-packing grind is exotic. The mitigation is that the ranking is anchored on
the game's own scenes (battle/slam densities measured 3.3–40× below the boundary),
not on the exotic cell alone. What this lens may still have missed: the GPU/NEON arm
entirely (the one the letter actually names); the allocator's mixed-world scheduling
(the boundary's real use is per region, not per world); and whether any *gameplay*
path (a debris grind after a fleet dies in a gravity well, an accretion scrap) holds
a world at ρ > ρ\* long enough to matter — that is a design question, not a physics
one.
