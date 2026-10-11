# Dossier — 20261011-0517-spacex-d0ea (SpaceX lens): H_live of the plane's belt

## Claim

The belt's live distinguishing information is a **one-time ~146 bits per body (exact quanta) /
~69 bits (memo cell), created within the first orbit and then flat** (+0.08 bit/orbit, clock
field only), and it is dominated by the *orientation-coupled kick scatter* — the synodic
short-period oscillation around the averaged law — not by resonance or rounding; at 10⁹ bodies
that is 8.6–18.3 GB, so **the program+scars store at the law's current quanta cannot hold a
billion-body belt in the 4 GiB budget** — the generator needs the first-order short-period
(epicyclic) terms, and the angle/clock word quanta are the store's real cost.

## Bottleneck

The board's named unmeasured risk: "Distinctions created per game-second (H_live): they, not
the body count, decide whether 10⁹ fit in 8 GB; not measured yet" (also plane.md "Measured on
the whole"). This run measures it for the plane's own belt scene, on the plane's own path.

## The measure

A group = M ships born with the *same* (p, e, phase) at M orientations α_i. The averaged law is
rotation-equivariant, so the program+generator predicts identical (p, k) and periapsis time for
all M and angle α_i + shared precession; any refit absorbs that shared path (one table row per
radius, ~0 bits at 10⁹). The within-group spread of the stored tube's words — mean-centred, in
the store's own quanta — is therefore exactly the scar bits: exact quanta (p at 2⁻²⁴ root units,
k at Q48, angle at 2⁻³² turns, t_p at 1 clock word) and the law's memo cell (12+12 bits).
bits(field) = log₂(1 + range). Scene: star + planet (1/999 of the total) at 5.2 AU; belt
2.0–3.5 AU, e₀ = 0.05; 33 radii (25 log-grid + planted resonance centres) × M = 64 → 2112
ships; the plane's law as shipped (integer tubes, SyMBA kicks, 128 kicks/radial period);
20 mid-belt orbits ≈ 88 yr ≈ 2.8×10⁹ game-seconds.

## Evidence

Commands (from the repo root; the test is `crates/universe/tests/h_live.rs`, saved in this
run's patch):

- Decisive (~136 s, **6.1 GB RSS — over the 2 GB lab budget, reported**):
  `env HL_RADII=25 HL_M=64 HL_ORBITS=20 HL_SNAPS=20 HL_THREADS=8 cargo test --release -p emergent-universe --test h_live -- --nocapture --test-threads=1`
  → `lab/results/20261011-0517-spacex-d0ea/belt-hlive.csv` (this run; 660 rows),
  `analyse.py belt-hlive.csv` prints the table below.
- Small reproduction (12 s, same numbers within ~1 bit): same with
  `HL_RADII=8 HL_M=32 HL_ORBITS=5 HL_SNAPS=5`.
- Cadence control (below): add `HL_STEP=5` vs `HL_STEP=7`.

Numbers (cold = >2% in radius from any j:(j+k) resonance centre; `belt-hlive.csv`):

- **Cold groups (27 of 33 radii): flat.** bits_exact 146.1 at orbit 1 → 148.2 at orbit 20;
  bits_cell 68.2 → 69.6. Field split (means): p 43.6, k 39.6, angle 25.3, t_p 37.8→39.2
  (+0.078 bit/orbit, the only growing cold field — clock decoherence).
- **At the memo cell, (p,k) is cheap:** 15–32 distinct cells per group → ~4–5 bits; angle 25 +
  time 38 = 63 of the 69 bits (91%).
- **Resonant groups grow and keep growing:** within ~2% of 2:1 (3.19–3.42 AU): +0.56–0.77
  bit/orbit (bits_cell 74→83 by orbit 20); 3:1 (2.50): +0.32; 9:4, 11:5, 13:7, 11:6:
  +0.2–0.4. Reabsorption ≈ 0: modal-cell fraction 3–19%, exact-birth-tube fraction 0.
- **Cadence control:** 128 vs 32 kicks/orbit, same scene, 5 orbits: bits_exact 140.4 vs 140.5,
  bits_cell 64.3 vs 64.3 — the scatter is the physical synodic oscillation, not kick sampling.
- **Verdict at 10⁹:** exact 146 bits = 18.3 GB; memo cell + words 69 bits = 8.6 GB; hot-weighted
  (resonant bodies at the 16-byte full tube, ~18% of this grid) 81 bits = 10.2 GB. All exceed
  the 4 GiB budget; even the cold belt alone (18.3 GB exact / 8.6 GB cell) does.
- Side flag: the plane's own RSS for 2112 ships × 20 orbits was 6.1 GB (~2.9 MB/ship live) —
  the plane's in-memory history/catalogue is itself far over target at belt scale.

## Predictions (predictions.md, written before the decisive run)

- Saturation: **held** (flat from orbit 1). Magnitude: **missed 7×** (predicted ≤ ~10 cold bits;
  measured 69–146). The transient is the full kick scatter, not a small residual.
- Resonant growth: slope **held** (+0.3–0.8 bit/orbit, still rising at 20 orbits); the predicted
  "≥5× cold level" **missed** — the one-time scatter dominates both, so resonance shows in the
  slope, not the level.
- The verdict: **missed** — predicted ~14 bits/body (1.75 GB, fits); measured 69–146 bits/body
  (8.6–18.3 GB, fails). My flip condition (cold secular growth or hot > 20%) was the wrong
  axis: the one-time scatter is the killer.
- Game-seconds: per-orbit is the useful unit (1 orbit ≈ 1.4×10⁸ s); H_live ≈ 1×10⁻⁶
  bit/body/game-second after the first orbit, ~1 bit/body in the first orbit.

## What would make it wrong

- The store's generator need not be the *bare* averaged law: the scatter is a deterministic
  function of the synodic phase (α_i − λ_planet), which the program knows. A generator with the
  first-order short-period epicycles (classical perturbation theory's co-rotation terms) should
  cut the scatter to O(μ²) — the same lesson as r4 v1/v2 (first-order-in-μ along-orbit kicks
  fail) now at store level. Measuring that generator's residual is the named next experiment.
- bits = log₂(1+range) is an upper bound (an optimal code over the residual distribution could
  do better if it is strongly peaked); the entropy at these quanta could not be resolved at
  M ≤ 64 (it saturates at log₂ M). A high-M run (M ≥ 1024) on a few radii would tighten it.
- One scene (e₀ = 0.05, μ = 10⁻³, 2.0–3.5 AU); hotter belts (e₀ = 0.2) and inner belts scale
  the scatter but not, on this evidence, the shape of the answer. Floats explored nothing here:
  all counts are integer word deviations.

## Cost of adopting, and fit with PRINCIPLES

Nothing to adopt as code; the finding sets a requirement. It kills the bare-averaged generator
as the belt's store at the law's word quanta and names the two levers: the epicycle generator
(physics) and the angle/clock quanta (a law-level choice, already flagged by the memo finding as
behind B1/B2/B9 re-judgement). "Averaging an orbit … is not the same thing" as averaging ships
(Julien, in law.md) — this measures the orbit side of that line. Principle 24 ("the memory floor
is information") now has its belt number: the floor is set by the synodic scatter, ~69 bits at
the law's own cell, ~5 bits for (p,k) alone. Principle 6 ("store the generator, not the
generated") survives only with the richer generator.

## The lens

SpaceX's idiot index put the memory question first (measured bits vs the information floor) and
the delete question second: the finding deletes the bare average from the store design. The lens
may have missed the compute side (the plane's 2.9 MB/ship live memory and the per-kick compile
are the same scene's other idiot indices — flagged, not measured cleanly). It also biased me to
predict the store would *fit* (optimism of the builder); the measurement said no.
