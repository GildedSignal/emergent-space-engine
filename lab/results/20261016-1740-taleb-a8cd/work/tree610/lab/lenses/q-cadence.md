# Lens: how many kicks each body needs, from its own dimensionless numbers (a directed question)

The plane kicks every body at one fixed cadence, `2^step_log2` per radial period (`Config::step_log2`, crates/universe). Kicks are the engine's dominant cost. The lab's runs of 1–5 October agree that correctors and higher-order splits buy nothing, and they disagree on the cadence itself. Read their dossiers and checks first (`git show origin/claude/lab-<id>:lab/results/<id>/check.md`):
- 8 per orbit holds the behaviours, 16 at e = 0.3: `20261001-2353-q-correctors-aa78`; 4–6 for moons through 0.4 R_H: `20261004-1525-scout-2098`; 8 for a belt: `20261003-2306-system-27ce`; 16 for smooth regimes: `20261002-1618-scout-f341`.
- The 64 cadence is already at the cliff: `20261004-0555-quant-5022`. Inside a resonance band no rate up to 64 matches a librating truth: `20261003-0520-dynamics-a9c2`.
- Averaged kicks hold where the motion is predictable: `20261003-0520-components-13ae` (evection kept), `20261003-2306-dynamics-0c67` (an unpredictability wall at 1 − a ≈ C·μ^(1/4)).

**Question:** what rule gives each body its cadence from local dimensionless numbers (the tidal ratio τ, μ, e, the distance to the nearest resonance, the unpredictability wall), so that every behaviour of law.md B12, B14 and B17 holds at the fewest kicks in total? Explain the disagreements above with that rule, rather than averaging them away.
- Build in your folder (never edit the crates). Test the rule on mixed scenes (a belt, moons, a resonant pair, ships crossing a Hill sphere), held out: the regimes where the runs above disagree.
- Report total kicks against the fixed cadences 128, 64, 16 and 8 at equal behaviours, and where the rule breaks.
- The cadence may change only at a body's events, and must be decided exactly (integers), so that the result is independent of schedule.

Gold: a rule, decided from local quantities, that cuts total kicks 4× or more on the mixed scenes with every behaviour held.

Read first the Opus math memo (`lab/refs/opus-math/memo.md`): cadence serves only the part of each body's perturbation that is not integrable (R2, tested by `q-secular`), and a body's state between kicks must be read on a second-order ramp (law.md), or the mid-interval readout's first-order error will be mistaken for the cadence's.
