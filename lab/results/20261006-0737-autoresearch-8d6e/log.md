# Log (lens: autoresearch; metric = kick-bench median µs per kick, behaviour = replay digest)

Machine: lab-4 x86-4790, 8 vCPU, load 0.16–0.9 during the run (co-tenant), 15 GB.

| # | Hypothesis | Change | Measurement | Kept/reverted |
|---|---|---|---|---|
| 0 | — | baseline bench seed 1, 15 s | median 45.4 µs, p99 61 µs, digest 50b705f1; 55 s: 37 kicks, exact memo hit 0% (confirms taste log) | — |
| 1 | the rebind (fit+compile) dominates a kick | env-gated dump of `bind` inputs + replay harness (`prof/`) | bind is 13–25 µs (cycles) of the ~45 µs median; readout 3.2 µs; the rest ≈ secondary readouts in `force` | kept (knowledge) |
| 2 | compile is the rebind's cost | split bind into compile/at_radius/fit via replay | cycles: compile ≈ 0.57 µs/knot (6→3.4, 20→13.5, 52→34.7, 92→61.5 µs); **passages: 14/72 binds = 86% of bind µs (330–2022 µs each, ~90% in `Passage::compile`)** | kept (knowledge) |
| 3 | wide divisions (u128/u128) in `fast_quad` are fat; `div_word` is exact | swapped `g`, `g1`, `ratio` to `div_word` | divbench: 1.32× per division (18.1 vs 23.8 ns); outputs hash-identical (95fafd8590f8f8ee, 72 inputs incl. 14 passages); replay compile median 4.94 µs vs baseline 6.00/4.53/4.47 µs — inside machine noise (repeat runs drifted 20–50% under co-tenant load) | **reverted** (kill criterion of predictions.md: <8% unresolvable) |

Three rounds without a ≥10% metric move → stop, per the lens.

## Attribution (the run's result)

Median kick (45–47 µs) ≈ own readout (3.2) + bind (13–25, cycles) + ~10 secondary tube readouts (3.2 each, in `force`/`ctx.secondaries`).
The tail (p99, 570–910 µs on seeds 1–3) is passage rebinds: `Passage::compile` builds ~0.5–1.5k panels because
outer_radius is the doll constant `2·edge` while endpoint = periapsis/outer drives the EDGE band ladder (16 bands/octave)
plus the ×15/16 tail. Cost ∝ log₂(edge/periapsis) — every kick on such a body pays it again (exact memo hit 0%).
