Working...
Check complete. `lab/results/20261007-1106-fermi-443e/check.md` written; tree restored (patch reversed, scratch variant removed); nothing else in the run folder touched.

**Grade: silver.**

What I did and found:

- **Reproduction — exact.** Applied `work/patch.diff`, built, ran the decisive `3600 1 400`: every number matches the dossier and the delta stream is `cmp`-identical to the author's `.bin`. All three variants match (rate 0.010–0.018, ratio 1.09–1.20). `fermi.py` regenerates every table line (182 MB/s, 1,231×, 508×, 44 s, 168/924 cores). zlib saves 4.5–5.5% on all four streams, confirming near-incompressibility.
- **Pre-registration — real but miscounted.** `predictions.md` (11:09:43) precedes all outputs (11:12:00+), but the dossier tallies "residual bits 21 vs 40–100" as *held* — that's a third miss (5/3, not 6/2), visible in the log and in the safe direction.
- **Three adversarial cases, all surviving the physics:** 10× horizon (ratio tightens to 1.01; bytes/body grows 9,846→45,239, so the "1,231×" is the 1-hour cache point, not a constant); 10× sampling density (bits/event unchanged); 10× denser lattice fleet — which **proved `stats.kicks` counts lattice contact kicks, not doll binding changes** (kicks 1,582→6,036, binding stream bit-identical), so the 0.014 events/body/s anchor mixes populations and overestimates all-inner H_live ~2.3× (≈79 MB/s, still ≥750× under bandwidth).
- **Novelty:** first measurement of H_live (HANDOFF: "not measured yet"; `residual_bits.rs` only did static histograms). It corrects the plane.md outside-review premise on this scene class.
- **Gold blocked by:** single scene class (28 doll bodies, zero handoffs, no belt/fleet), the population-mixing anchor, and the miscounted prediction tally. The one gold experiment: run `hlive` on a concentrated belt/fleet scene at B18b scale, rate anchored per doll binding event, predictions pre-registered.
