Grade: silver

**Abstract.** Claim: level-triggered kick scheduling from local field derivatives (magnitude, jerk) is killed as a cadence rule; cadence must come from the certificate residual. Reproduced bit-for-bit (cold 28 s, hot 29 s): matching fixed16's median |da/a| costs ≈560k (mag) and ≈500k (jerk) kicks against the clock's 160k. Three adversarial scenes of mine confirm the direction: truth floor 9.6e-7 (bar is 60× above it), perturber at 1.3 AU (1.4–2.8× worse), wide belt with 36× field range (2.2–4× worse at matched median). Gain: kills a dead rule family before q-cadence builds it; cost: q-cadence reads the register, not the field. Silver: the kill is surrogate-only, one of five lessons is measured, and the median metric carries it.

## Reproduction

`python3 exp_cadence.py cold|hot` in a clean copy: every aggregate (med, p95, kicks, k_med, k_p99, all 14 policies, both scenes) identical to the stored JSONs. Dossier interpolations recompute: mag at fixed16's 6.045e-5 → ≈560k kicks (3.5×); jerk error ∝ δ^0.5, kicks ∝ δ^-0.5 → δ≈1.7e-7 → ≈500k (3.1×). At its best measured point (δ=1e-6) the jerk trigger is strictly dominated: 1.46e-4 error at 207k kicks — worse error than fixed16 while spending more. Integrity note: running the dossier commands in the run folder overwrites the two JSONs; output is deterministic and all values were identical, and my scratch files were removed. `work/patch.diff` empty, git status clean outside `lab/results/`.

## Predictions audit

File order is consistent (predictions.md 4 m before cadence_cold.json 3 m, hot 2 m; run.log empty so first-run order is unverifiable). The post-hoc P5–P8 block is disclosed as such. P4 fired, P8 fired — the pre-registered kill is the result and the author reports P1/P2/P5/P6/P7 failing honestly. **P3 is never reported anywhere**: from the stored JSONs it failed too (mag at cold-matched δ gives the hot scene 2.0e-5 vs its fixed16 6.3e-5, but at 803k kicks — a 5× increase, no ≥2× cut). Another failed prediction would only strengthen the kill; leaving it unreported is the gap.

## Adversarial cases (mine)

- **A1, truth convergence:** |a_512 − a_1024|/a med 9.6e-7, p95 5.2e-6. The 6.0e-5 bar is ~60× above the floor; measured errors are policy error.
- **A2, nearer perturber (a_p = 1.3, field varies ~2×):** at fixed16's med error, mag ≈453k kicks (2.8×), jerk ≈1.4×. Kill holds.
- **A3, wide belt (a ∈ 0.7–1.45, field varies ~36×):** the triggers now allocate (k_p99/k_med up to 20, vs 1.2–4.0 in the author's scenes) yet still lose at matched median error: mag ≈635k (4.0×), jerk ≈356k (2.2×). The kill generalizes beyond the author's near-uniform scene. But at matched **p95** on this scene the mag trigger beats the clock ≈1.5× (≈108k vs 160k) while being 12× worse on the median: on heterogeneous scenes the verdict is metric-dependent, and the dossier argues median only.

## Novelty

No prior run tested event/level-triggered scheduling: the six cadence runs (q-correctors-aa78, scout-2098, system-27ce, scout-f341, quant-5022, dynamics-a9c2) measured fixed rates, correctors and averaging. Probe 1 (29 Sep, gravity-v1-freeze) killed per-body dynamical-time steps on energy-error walking — same spirit, different axis (error walk vs cost at matched error); this run's cost kill is new. Lesson 5's citations check out (a9c2: no rate ≤64 inside resonance; dynamics-0c67: wall at 1−a ≈ C·μ^(1/4), per lab/lenses/q-cadence.md). All six library quotes verified verbatim in highlights.tsv.

## Goal fit

Board focus #1 (kicks dominate cost) and the queued q-cadence: this kills one family of candidate rules before builders spend windows on it, and correctly does **not** claim to kill richer local invariants (resonance-phase distance) — the lens's own candidate list survives. Fits PRINCIPLES 14 ("no work for no reason, so no ticks"), 22 ("the simulation decides; heuristics schedule"), 10 (simplest falsifying test first). Lesson 1's scheduled skin refresh (Åström/GROMACS mechanism) is sound where the quantity is kinematic, but it is proposed, not measured.

## Why silver, not gold

Gold requires the held-out predictions to hold; here the positive predictions (P1, P2, P5–P7) all failed and only the pre-registered kill criteria fired. The kill itself is solid, but it is measured on a surrogate the author admits is not the plane (no averaged tides, no J2, no two-body parents, no resonance, impulse-at-end kicks), one of five lessons is measured, and the mechanism sentence overstates: A3 shows local derivatives *do* carry allocation information (k_p99/k_med to 20) — they simply still lose to the per-orbit clock on the median.

## The one experiment to gold

Run the same trigger family on the plane's own kick layer (averaged tides, J2, two-body parents, `behave --law plane`) or a faithful surrogate of it including a resonant pair, judging B12/B14/B17 behaviours and reporting both median and tail: if the clock still wins there, the constraint "q-cadence may not read the field's local derivatives" is adoptable in one step.

## What the author missed

P3's outcome unreported; the kill is metric-dependent on heterogeneous scenes (median vs p95, my A3); the "nearly flat" claim understates the hot scene (k_p99/k_med reaches 4.0 at mag δ=1e-4); the trigger's cadence is silently capped at the 1/128-orbit evaluation grid (mag δ≤3e-6 saturates to fixed128 — identical rows in the JSONs), which bounds how well the trigger could ever have done and deserves a sentence; lessons 1, 3, 4 and 5 are quotes plus mechanisms with tests proposed and none run.
