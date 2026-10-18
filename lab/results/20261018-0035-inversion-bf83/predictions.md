# Predictions (written before the decisive sweep)

Question: does the shipped frames harness, unsabotaged, at the shipped defaults, fire the
finality assert (`alloc.rs:1451`, "would revise its published tick") on the game's own scene
shapes — a fleet battle and sustained ballistic crossing traffic — where it fires on synthetic
churn gas?

Arms (all `Law::Relativistic`, unsabotaged, margin 2.0, p2+e2 workers, hz 240, 4.5 s,
rate swept 300/600/1200; protocol 3 seeds x 2 replicates per arm):

- `gas min1`: ONE dense slow gas cluster (`scenes::loose_gas`, vmax 2 u/chronon), `min_region 1`.
- `battle`: lattice `worlds::galaxy` fleets (power-law fleets of bouncers, bulk drift, 256-body
  stream), shipped defaults (`min_region 32`).
- `battle min1`: the same, `min_region 1` (the page's named exposure knob).
- `streams`: interpenetrating Pass-disc trains (4 lanes x 4 clumps, opposing drifts q/4 vs q/8,
  NO contact response change) — sustained crossing traffic, the belt's shape, shipped defaults.
- `quiet`: sparse Pass islands far apart, no contacts (negative control).

P1 (instrument check, positive control): `gas min1` fires on >= 1 of 6 draws at rate 600,
panicking inside the first ~150 chronons (the page's scene-start band). If 0/6 at every rate,
my harness cannot detect the known defect and the run is VOID.

P2: `battle` (shipped defaults) fires at >= 1 of 6 draws at some rate on the sweep. Rationale:
the crash needs isolated lineages publishing ahead, then re-meeting behind the published tick;
a battle makes debris-churn by construction (the page's own exposure note).

P3: `streams` does NOT fire at any rate on this horizon: Pass bodies never change velocity, so
the tracked max |k| forecast is exact and publishing cannot overshoot a future clash start.
If it DOES fire, ballistic crossing traffic alone breaks finality — stronger than the churn
reading, and the belt (the 10⁹ population) would be structurally unsafe at these defaults.

P4 (negative control): `quiet` never fires (0/6 at every rate).

P5: any fires are seed-skewed and replicate-unstable (the page's wall-clock-race law).

P6: `battle min1` fires at least as often as `battle` (more splits = more isolated lineages).
