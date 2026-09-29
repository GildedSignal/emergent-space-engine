## The goal

A game: an emergent, faction-based 2D space universe with general-relativistic behaviours, and billions of ships, stars, planets and black holes. It runs smoothly on one fanless 8 GB MacBook Air M1, and it lets the player feel what living at high c would feel like.

Julien, 29 September: "this is a game with insane requirements because i believe that its creates the space for extremely good gameplay and that space is so empty that there's no way that it can't be cheap we need to be about to run billions of entities across a galaxy like it's nothing thanks to simple laws that create the right emergent properties for cheap."

## The philosophy (always on)

Labels are ours; quotes are his. 12–31 were approved on 29 September ("Otherwise the principles are correct"). Source keys are under the register.

1. **Less is more.** The cheapest compute is compute not done. Delete before optimizing, and make compute cheap. Simplify, never dumb down.
2. **It's a game.** Behaviours matter, not continuum fidelity: error type over error size. "Exact" means deterministic and reproducible, not equal to reality. Exact physics is the oracle, not the implementation.
3. **Compute only surprises.** Cost follows change and entropy. Nothing is evolved that can be derived when looked at (clocks, redshift, views). "redshift and co are not derived but emergent" (CL 09-29); "chaos is normal it's just the necessary interactions happening within a short time" (CL 09-29).
4. **Everything is emergent.** No central control and no categories: regimes are chosen by dimensionless numbers.
5. **The player is the only wildcard,** and their influence travels at c. Precompute everything else; light cones partition compute. Priority is slack, not proximity. "his direct influence is bounded and propagates at c at most" (CL 09-27 10:20); "we need a map, but a map that is inferred based on intelligence for the territories" (OC#16); "the zoom level is the minimap" (OC#30).
6. **Store the generator, not the generated.** Aggregates matter: influences below one quantum accumulate, and ships' aggregate mass can become a source. "its time that's a multiplier here and not the space bending of its mass" (CL 09-27 09:08); "they have a lot of mass cumulated they can't just be dismissed like that." (CL 09-27 09:25).
7. **Spacetime, not space plus time.** Geodesics are as trivial as straight lines. Gravity is compiled into geometry held by cells (flat pieces, tilted by the flow). Multipoles are the mechanism, for gravity and for causality regions alike.
8. **First principles.** Question every requirement, and build cathedral foundations, not an MVP.
9. **A failed experiment kills that configuration, never the method.**
10. **Iteration speed.** Measure before claiming. Run the simplest falsifying test first, then test like a Spartan; baby Spartans start small. Measure the way the player plays, heat included. "We need also to map how things break, think in extremes" (CL 09-27 09:08); "we ought not to underestimate iteration speed" (CL 09-28 14:34).
11. **Text has a cost; no busywork.** Start clean, build messy-ish, finish clean: "it's ok to try but it's not a reason to wreck havoc either" (CL 09-29).
12. **Smoothness; the allocator.** "minimize spike compute and average compute usage so that you get a bigger simulation that runs smoothly" (OC#36); "i care about the p95/99 results i want the game to be smooth" (CL 09-25 14:06); "the algorithm that allocates the work to prevent those heavy tails, it's the most important one" (CL 09-25 14:28).
13. **Errors never compound.** "basically we don't want errors that can compound that's the goal" (CL 09-25 14:28); "divergence is not a joke and it compounds" (OC#34); "types of errors and not just errors" (OC#42).
14. **No work for no reason, so no ticks.** "more fundamentally it's about not doing work for no reason, ticks make no sense to me they seem like a bad solution for synchronization and preventing doing too much or too little which is not compatible with our certificate/compiler idea" (CL 09-29); "you don't advance a ship tick by tick you just map where it wants to go" (CL 09-27 09:08); "we only care about changes" (CL 09-29 08:24).
15. **Local laws.** "local laws are great because parallelizable and simple and efficient in general, again the goal is to reduce compute" (CL 09-29).
16. **Discrete by design, cheapest arithmetic.** "there's no continuum, physics may be quantitized but appear continous at the right scale"; "it's just what's the biggest quantization that we can get away with?"; "no it's about what's cheapest to compute"; "physics loves e while we love 2" (all OC#38).
17. **Every part of the machine; the best part is no part.** "basically leveraging EACH part of the computer that can work for us and aligning the work to what they are best at and gpu are great because they can do many operations per seconds but remember that the best part is no part" (CL 09-29); "we need to be deeply aware of von-neumann bottleneck and memory" (CL 09-27 09:08); "\"Use idle time to compute ahead\" yes this is a whole important idea of this project" (CL 09-25 14:28).
18. **The right question, then the representation.** "hence why i'm such a pain with finding the right question to ask" (OC#42); "we just need to have the right representation so that math is trivial." and "you start from a listicle instead of what are our requirements" (CL 09-27 09:08); "better questions matter" (CL 09-28 11:37).
19. **A fix signals the wrong representation; one law at every scale.** "bandaids are basically fixes resulting due to a poor representation and question they accumulate like trying a patch a drowning car in the ocean, don't get a car get a boat, if you find yourself fixing things that's oftentimes a signal that it is the wrong representation, the right representation always just feels right it does the job like cutting butter in summer" (CL 09-29); "how to have the same mechanics at all scales while not doing the work" (CX 09-14 09:37).
20. **Behaviours over many seeds; no engineered outcome.** "if you're actually testing behavior or the bad idea of expecting the same data" (CX 09-23 11:07); "because it happened to work like that not because the laws were made for it to work" (CX 09-14 09:17); "we want determinism ≠ realistic trajectories" (OC#48).
21. **Rough first, refine when a certificate could break.** "we need refining because it might break the certificate as we are uncertain? simple and powerful." (CX 09-14 09:37); "do we have to be perfect right away? No, as long as the end result is good the method doesn't matter." (CL 09-27 09:08).
22. **The simulation decides; heuristics schedule.** "the simulation tells us what's next not us, subtle but deadly." (OC#36); "fermi is there to spot issues early not an oracle" (CX 09-11 21:47).
23. **Nothing past c.** "beyond c=1 means paradoxes" (CL 09-25 16:44); "i don't want FTL because of paradoxes" (OC#16); "it allows to cheaply partition compute, even gravity is light speed" (OCC#10).
24. **The memory floor is information.** "this is nowhere near the floor on the size and information theory says so" (CL 09-28 09:48); "why do you need so many bytes per entity?" (OC#34).
25. **No sunk cost; avoid ruin.** "if it's good, good, if it's bad it goes away and we learn a lesson from it" (CX 09-14 09:17); "not making mistakes matters more than doing things efficiently, don't multiply by zero." (CL 09-28 12:43).
26. **Steal what works, from skin in the game.** "i need to steal from what works as much as possible" (OC#16); "those guy with simulations don't have much skin in the game for compute and time constraints unlike quant traders" (CL 09-27 09:08); "This is a solved problem elsewhere for sure" (CL 09-29 08:24). "we need to keep doing those smarter math and old tricks when people used to be compute deprived their had the right incentives and skin in the game" (CL 09-29).
27. **The goal, never a proxy.** "it is a bad proxy" (CL 09-28 14:51); "what is needed is needed" (CL 09-28 10:04); "i just care at about how fast it runs compared to real time" (CL 09-27 10:20).
28. **The view is an instrument.** "real vs displayed is not the same thing" (OC#38); "your dials are made up and hold no informations" and "it's a space clock literally" (DC).
29. **History, not a winner.** "a game that cannot loose by construction if done right" and "history being made and learning from it through space and time while you are influencing it yourself" (OC#4); "emergent such that there's never a sole winner or if so factions can emerge, embracing the chaos" (OC#16).
30. **What must be perfect.** "what really matters is navigation, knowledge and dynamics those need to be perfect, graphics don't matter" (OC#16); "I want the player to feel what a human would feel in space, it's about immersion" (CL 09-27 09:08); "we need to build towards GR that's the goal that we should not loose track of, the rest are stepping stones" (CL 09-26 08:18).
31. **The logs hold the philosophy; keep contradictions; check incentives.** "the philosophy is here" (CL 09-29 08:05); "the things that are contradictory should be separated but not necessarily deleted" (CL 09-28 14:34); "if it read about incentives it should look at its own incentives and the ones it created" (CL 09-28 14:49).


# The GLM lab

Julien, 29 September: "Our goal is to make the fastest and most robust engine/compiler ever for that type of physics"; "GLM should have more autonomy not what it could change but on what it could experiment on"; "I don't like pass/fail we just need a good system that make sure it propose gold."

Many GLMs, each with a lens, get **autonomy of inquiry and no authority.** They choose what to experiment on, build and run anything in a cloud container, and never change `main`. They run only in the cloud, never on Julien's machine. An independent GLM checks every result. Only gold reaches the integrator.

## One run

1. **The author** reads PRINCIPLES, this file, the [board](board.md) and its lens. It picks its own question, aimed at a bottleneck on the board or at a bigger one it argues for. Then it does real work: derivations, code, experiments. It may edit any file in the container to experiment. `run.sh` saves the edits as a patch and restores the tree.
2. **Held out before the run.** Before its decisive experiment, the author writes `predictions.md` in its run folder: the cases it has not tuned on, and what it expects there.
3. **The checker** is a fresh GLM session with no author context. It reproduces the work from the dossier's commands, runs the held-out cases plus adversarial cases of its own, and checks novelty against `docs/HISTORY.md` and the docs. Then it grades the work and writes the abstract.
4. **Gold is checked twice.** A second checker runs blind to the first; gold stands only if both grade it gold (two independent finders, arch-v3 §3).
5. **Canaries calibrate the checkers.** `lab/canaries/` holds dossiers with known answers, some subtly wrong. Now and then a checker grades one blind; a checker lens that passes a bad canary is rewritten.
6. **The integrator** reads only gold abstracts, at most three a day, ranked by gain × probability ÷ cost of adoption. It records each decision (adopted or rejected, and why) in the board's taste log. Every author reads that log: it is how the lab learns what gold looks like.

## The dossier (`lab/results/<run>/dossier.md`)

- **Claim:** one sentence.
- **Bottleneck:** which one, the expected gain in orders of magnitude, and what it lets us delete.
- **Evidence:** the numbers, plus the exact commands that reproduce them (each ≤ 60 s where possible).
- **Predictions:** point to `predictions.md` and say what happened there.
- **What would make it wrong,** the cost of adopting it, and its fit with PRINCIPLES (quote the line).
- **The lens:** what this lens may have made you miss.

"Nothing worth adopting, and here is why" is a legitimate dossier. One substantive result beats five shallow ones.

## Grades, with reasons, never bare

- **Gold:** reproduced, and the held-out predictions held. It moves a board bottleneck by 10× or more, deletes a component, or shows that a premise is wrong. It can be adopted within one step.
- **Silver:** real, but one named experiment away from gold. The next run picks that experiment up.
- **Lead:** not reproduced, marginal, off-goal, or already known or tried (cite the H entry). Leads are kept, never deleted.

## Rules

- Every prompt begins with PRINCIPLES.md's goal and philosophy (`run.sh` prepends them).
- Floats may explore; only integers decide canonical outcomes.
- Cloud timings are Linux/x86: report orders of magnitude only. The integrator re-measures on the M1.
- Results live only in `lab/results/<run>/` on the run's own branch. Never edit or push `main`, the docs, the crates or frozen evidence.

## Running (cloud only)

- A routine runs `lab/run.sh <lens> [minutes]` in a cloud environment that has `ZAI_API_KEY`. `lab/setup.sh` installs omp, pinned by hash.
- The lenses are in [lenses/](lenses/). The integrator owns [board.md](board.md), `checker.md` and this file.

## Directed rungs
- `lab/run.sh rung <file> [minutes]` runs a rung file that is committed and unchanged: prose, a `configs` block (`<name> candidate|negative`) and a `criteria` block (`<id> behaviour|type|cost <metric> <op> <threshold>`).
- The author writes `metrics.json`, a checker reproduces it as `metrics-check.json`, and `verdict.py` decides: PASS (after a blind second checker), KILL, VOID or DISPUTED. A KILL kills configurations, never the method.
- [canaries/](canaries/) holds rung files with known verdicts: a checker lens that misgrades one is rewritten before real rungs count.

## Writing rung criteria (lessons from r2)

- **Controls on both sides.** Every rung has a `positive` control that must pass (an ideal configuration: the oracle itself, or the law-native exact reference) and a `negative` that must fail. If either misbehaves, the verdict is VOID.
- **No trajectory identity.** Never demand long-run identity with an external float truth. Rounding makes that a random walk, so the demand is error size in disguise. Judge behaviours and statistics.
- **Robust growth exponents.** Judge them on the median seed or on an ensemble fit, never on the worst seed of a noisy estimator.


# Bottleneck board

Owned by the integrator and rewritten in place. **Target:** the fastest and most robust engine and compiler for relativistic many-body physics at game scale. That means billions of bodies on one fanless 8 GB M1, exact and deterministic, computing only surprises (see [PRINCIPLES](../docs/PRINCIPLES.md)).

## Bottlenecks, ranked (29 September)

0. **The representation, from scratch** (Julien, 29 September). It is one question, and the others below may be its consequences.
   - The engine is "a causal cellular automaton that runs as fast as possible or maybe that is guided by light speed".
   - "we need to make light speed hardware native… light speed is basically how fast the causal chain is updated".
   - "a 'simple' tube is tracing a straight line through spacetime which means that space time needs to be represented in such a way that it is possible while respecting gr".
   - "we want to guess in a way that is perfect how the simulation will run to bypass it"; "steps are there to solve a problem of how much error we are ok with… we want them consistent across the different types of simplifications… We need to expand what steps mean".
   - "rethink our units from scratch, time and spatial ones", "tied to hardware and end goal"; the number representation from first principles; "how we travel [memory] limiting useless movement".

   - Later the same day he added:
     - "We need to make this whole thing GR native that's THE unlock"; "GR is just one thing".
     - Sheets as nested dolls of a fixed bit size, whose size is linked to the spacetime gradient ("we can infer it from the size").
     - AI and player decisions as the seeds of change.
     - "the floor is what the player can differentiate like frame rate in early cinema"; units from the hardware.
   - Later still:
     - The sheets encode GR only: "collisions is just how you move inside them". Contact compute is a separate, on-demand structure that is never stored in the geometry.
     - The ship-versus-asteroid threshold must be cheap.
     - AIs create emergence that is hard to predict.
     - Local laws, but global algorithms are allowed: "make the memory dance tighter from a causal pov".
   Derive it from the requirements (the goal, the behaviours, the M1) before any known method. Candidates to test, not adopt:
   - fixed-bit cells in a dyadic tree, where the level acts as a shared exponent (block floating point, OCP microscaling);
   - geometry partly encoded by the tree's shape;
   - AIs as part of the deterministic law, recomputed only when what they see changes, so the player is the only seed;
   - one chosen floor (spatial), with time derived through c = 1 and velocity precision derived from the certificate's length;
   - each cell a freely falling local frame, with bodies stored as small offsets from it;
   - c as one cell per update, so each cell's time unit is its light-crossing time;
   - exact shortcuts in the spirit of Hashlife;
   - a bit-reversible integer law, so errors cannot compound;
   - asynchronous variational integrators, which keep energy bounded across cells with different steps.
1. **What cells add for many sources.** Mass moments add; the river flow does not, because β ∝ √M. We need a rule from a cell's multipole expansion to its local β that:
   - is exactly Schwarzschild for one mass;
   - is curl-free for static sources;
   - is right to 1PN for two masses.

   See "Open" in [gravity-law.md](../docs/gravity-law.md).
2. **Stepping owned by cells, or no stepping.** Probe 1 killed per-body steps: the energy error walked, and distant light jumped over the lens. We need bounded energy error, correctly bent distant light, and ≤ 512 events per orbit. Probe 2 (29 September) killed cell-owned staircases: every shell crossing injects energy error (up to about 3×10⁻³), as Calvo and Sanz-Serna predict. One fixed step passes the physics at about 350–700 steps per orbit, and light costs 20,000–77,000 steps. The live path is no steps at all: analytic generators in the dominant field, with multipole residuals as kicks (H0190: 32 kicks per orbit, 0.3 with averaging), and integration only where no generator exists.
3. **Cost at a billion.** 10^9 orbiting bodies at today's rates would need about 190 cores. We need 10–100× less: fewer events per orbit, cheaper events, and never computing what nobody can observe.
4. **Smoothness and the allocator.** The worst frame and the p99 on a fanless M1 that throttles when hot. Least-slack scheduling fed by surprise rates; five modes to become one engine.
5. **Units, widths and memory: one question.** The quanta couple position, velocity and time. The position quantum is c·δt/Q = 2.3×10⁻¹⁴ m, so 32 bits span only 49 µm, and an AU needs 83 bits. That is set by the worst case, a near-c 50 cm missile, and applied everywhere.
   - Can each cell own dyadic quanta sized by its content, with cell-relative coordinates and positions derived from generators, so that most state fits in 32-bit packets?
   - The M1 GPU is native at 32 bits, emulates 64, and has no 128 and no fp64.
   - The memory floor is information-theoretic.

## Known: don't redo it, build on it

- Exact continuum geodesics as the implementation ran 1,600× over budget (H0194). They are now the oracle.
- Per-body dynamical-time steps make energy error walk ([probe 1](../artifacts/evidence/gravity-v1-freeze-20260929/probe-out.md)). The fixed-step control stays flat.
- One GEM quadrupole failure (H0139) is not a ban on multipoles (H0196).
- Premise probe H0190:
  - averaging tides cuts kicks 114×;
  - J2 must be in the formula;
  - binaries need a two-body parent.

## Leads from earlier work (unexplored; a lens may pick one up)

- The polymath scan (GLM, 28 September): commutative-monoid messages between regions; largest-remainder splits; choosing the error-feedback kernel by its low-frequency error; a replay-bisect tool; an LSM- or CRAM-style body store.
- Mechanisms from arch-v3 not yet running: gate-bite mutants; adversarial mining into a shadow corpus; blind panels of 3–5.
- Prior-art scout (29 September, `artifacts/runs/prior-art-timestep/out.md`): Calvo and Sanz-Serna (1993) show that a state-dependent step is never symplectic. The working schemes put the adaptivity in time (Sundman, logarithmic Hamiltonian), in the hierarchy (HOLD) or in the mesh (AVI).
- Julien, 29 September: local sheets and no teleportation make the engine an asynchronous cellular automaton that follows causal chains instead of cataloguing. Positions are re-derived, never global. 32-bit packets per region. Memory laid out in causal order, as Crash Bandicoot laid out its levels. Are the quanta sensible? (see bottleneck 5)

## Taste log (the integrator's decisions on gold, newest first)

- **29 September, r2 (carry width): KILL of sd16, sd24 and sd32.**
  - **What it showed:** a 32+32-bit pair holds float64 increments exactly (zero phase error). Carries cannot recover information below their own resolution. Kicks on the law's own grid accumulate exactly at any width.
  - **Integrator's error:** two criteria demanded trajectory identity with float64 (conjunction order; the worst-seed kick-residual exponent), which the checker proved unpassable.
  - **Fix:** positive controls in `verdict.py`, and criterion-writing rules in the README.
  - **Design consequence:** increments and kicks are integers native to the law, so widths are set by behaviour (r1 and the law's gates), not by matching floats.
- **29 September, premise red-team: silver.**
  - **Adopted:** the rule that resonance kills averaging (design §3, rung r4); r3 v2's truncation fix; Clohessy–Wiltshire is first order only; Minsky's map is a conjugated rotation.
  - **Why silver, not gold:** its model B, the half claiming "kicks survive", was a dense integration, not the design's kick layer. Claims must be measured on the design's cheap path.
  - **Why it was good work:** a converged truth, predictions written before the decisive run, the rung gap audited, and honest misses.

# Lens: the checker (independent; the integrator owns this file)

You did not write this work, and you gain nothing if it is good. The default grade is lead; gold must be earned.

1. **Reproduce** from the dossier's commands in a clean tree. Apply `work/patch.diff` yourself if there is one. Record every number that differs.
2. **Check the held-out cases.** Did `predictions.md` exist before the decisive run? Compare file times and the log order. Did the predictions hold?
3. **Attack.** Run at least three adversarial cases of your own: extremes, chaotic scenes, the case the lens would miss.
4. **Novelty.** Search docs/HISTORY.md, the docs and `git log` for the same idea. If it was tried before, cite the H entry and say what differs now.
5. **Goal fit.** Does it move a board bottleneck, delete something, or show a premise is wrong? Does it respect PRINCIPLES? Quote the line.

**Write `check.md`:**
- the first line exactly `Grade: gold`, `Grade: silver` or `Grade: lead`;
- then an abstract for the integrator of at most 120 words: the claim, the reproduced numbers, the expected gain, the cost to adopt;
- then your reasons;
- for silver, the one experiment that would make it gold;
- then what the author missed.

# Rung r4 v2: arc-integrated kicks keep resonances that averaging erases

Frozen by the integrator on 29 September 2026. r4 v1 (claude/lab-20260929-1940-rung-r4-resonance-3530) killed instantaneous per-conjunction kicks: the checker corrected the author's sign error in the osculating elements, and the kill still stood, with over-pumping of 2–9× and failed controls. That kills the configuration, not the method. v2 tests kicks integrated along the arc. Source: the premise red-team (claude/lab-20260929-1835-redteam-2ef5), whose checker named this as the experiment that would make it gold. Its truth integrator, `e1_resonance.py`, may be reused as the reference.

**Question.** Does the design's event layer reproduce mean-motion-resonance behaviour when each kick is the first-order integral of the perturbing acceleration along the unperturbed Kepler arc between conjunctions? Resonance behaviour means eccentricity pumping and a librating resonant angle. The arc is never integrated: the orbit is held fixed within each window, and the change of the invariants is applied at the window's end (Gauss–Picard, first order). Osculating elements must round-trip position and velocity to 10⁻¹².

**Configurations.**
- `arc-g8`: windows between conjunctions, with the kick computed as Gauss quadrature at 8 nodes along the unperturbed arc, using the full direct and indirect perturbing acceleration.
- `arc-g16`: the same, with 16 nodes.
- `arc-g8-half`: the same as arc-g8, with two windows per synodic period.
- `truth-1200` (positive): the dense truth at 1200 steps per orbit, judged against truth at 2400. It must pass, or the criteria are unpassable.
- `averaged` (negative): orbit-averaged kicks, as in H0190 K2. It must fail.
- `none` (negative): no perturbation. It must fail.

**Cases.**
- **Resonant:**
  - a 2:1 case with perturber mass ratio 3×10⁻³, as the red-team ran it;
  - the red-team checker's phase-shifted 2:1 case (w2 = 4.0), whose truth has libration concentration 0.867.
- **Controls, far from resonance:** period ratios 5.0, 2.55 and 2.15.
- **Truth:** a dense float64 N-body integration, converged over 600, 1200 and 2400 steps per orbit (the red-team's).
- Each case runs for at least 200 synodic periods.

**Metrics,** one set per configuration:
- `e_pump_ratio_min`: over resonant cases, the minimum of (the law's maximum e₁) / (the truth's maximum e₁).
- `e_pump_ratio_max`: the maximum of that ratio.
- `libration_ratio_min`: over resonant cases, the minimum of the law's resonant-angle concentration / the truth's.
- `control_pass_fraction`: the fraction of controls whose secular e₁ envelope is within 20% of the truth's.
- `dense_steps`: the number of dense integration steps inside the configuration. It must be 0 for candidates; quadrature nodes along a fixed arc are not dynamics steps. The positive control reports 0 by convention.
- `kicks_per_orbit`: the median number of kicks, i.e. window ends, per inner orbit. Quadrature nodes are reported separately in the dossier.

**Output.** `metrics.json`, plus one picture: e₁ against time, with the law and the truth overlaid for each case, and the histogram of the resonant angle.

```configs
arc-g8 candidate
arc-g16 candidate
arc-g8-half candidate
truth-1200 positive
averaged negative
none negative
```

```criteria
pump behaviour e_pump_ratio_min >= 0.8
pumphi behaviour e_pump_ratio_max <= 1.25
lib behaviour libration_ratio_min >= 0.8
ctrl behaviour control_pass_fraction >= 1.0
cheap type dense_steps <= 0
cost cost kicks_per_orbit <= 8
```

## Your check (a directed rung)
Run id: 20260929-2040-rung-r4-resonance-v2-14b1. The author's folder is lab/results/20260929-2040-rung-r4-resonance-v2-14b1/: dossier.md, metrics.json, the picture, its scripts, and work/patch.diff, its edits (git apply to reproduce).
The rung above is frozen, and lab/verdict.py computes the verdict from the metrics files: ignore the Grade line rule above.
Time: 45 minutes. The machine is a cloud container (Linux, 4 vCPU, 16 GB).
- Reproduce the author's numbers from the author's scripts, and fix nothing silently: report every number that differs.
- Check the author's implementation independently against the rung's specification, and check each oracle value.
- Write lab/results/20260929-2040-rung-r4-resonance-v2-14b1/metrics-check.json in the same shape as metrics.json, from your reproduced numbers.
- Write lab/results/20260929-2040-rung-r4-resonance-v2-14b1/check.md: the abstract, then your reasons. Change nothing else in lab/results/20260929-2040-rung-r4-resonance-v2-14b1/. Never run git commit or git push.
