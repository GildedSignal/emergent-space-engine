## The goal

A game: an emergent, faction-based 2D space universe with general-relativistic behaviours, and billions of ships, stars, planets and black holes. It runs smoothly on one fanless 8 GB MacBook Air M1, and it lets the player feel what living at high c would feel like.

Julien, 29 September: "this is a game with insane requirements because i believe that its creates the space for extremely good gameplay and that space is so empty that there's no way that it can't be cheap we need to be about to run billions of entities across a galaxy like it's nothing thanks to simple laws that create the right emergent properties for cheap."

## The philosophy (always on)

Labels are ours; quotes are his. 12–31 were approved on 29 September; 32–35 on 30 September ("the principles are approved") ("Otherwise the principles are correct"). Source keys are under the register.

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
32. **Symmetry is found, not given.** "there are many kinds of symmetries in this world, under the right representation many symmetries can appear, this is a leitmotiv of compute paradigm shifts." Where no symmetry shows, change the representation before paying to simulate.
33. **Each scale resolves only what matters at that scale.** "we need to think in many scales, self-similarity like you said is powerful. An ant cares about a raindrop but the lion does not." The same law repeats at every scale (self-similarity). But a raindrop is an event for an ant and nothing for a lion, so a body resolves only the influences that are significant at its own scale, and smaller ones enter as an aggregate.
34. **A game is an illusion spectacle; the oracles are guards, not shepherds.** "Like said many times, this is game, a game is an illusion spectacle, the oracles are guards, not shepherds." Oracles reject what the player would see as wrong; they never lead the representation.
35. **Start from the goal and the dynamics; aim for the simplest, most powerful form.** "basically this whole project is about asking the right questions, specifically about what we're trying to achieve and how can we make it as simple and powerful as possible based on dynamics and requirements." Every piece of work begins with two questions: what are we trying to achieve (the requirements), and what do the dynamics allow? The answer is the simplest form that does the most.


# How to think here (read before choosing anything)

Julien's working heuristics, distilled from his library (Taleb, Munger, Feynman, Musk and SpaceX, Kelly, Shannon, Moore's Forth, Naval, Waitzkin, Asimov) and from PRINCIPLES. Paraphrased; the sources are his books and Readwise highlights.

**Before you start**
- Restate the question in one sentence. If your restatement differs from what was asked, the gap is the problem.
- Find the bottleneck: the one constraint that, if removed, makes the rest easy. Work on nothing else. Read it off measurements (the plane's dashboard, the gates' verdicts), never off a listicle.
- Question the requirement before solving within it: who imposed it, and does it survive first principles (physics, information, the M1's limits)?
- Fermi-estimate the answer before building anything. If the estimate already kills the idea, stop and say so; that is a result.

**While you work**
- Change the representation when the problem is hard: the right one makes the math trivial (Julien: "we know we have a fish, we need to find its water"). Try another field that solved the same dynamic.
- Via negativa: ask first what can be deleted. The best part is no part; the cheapest compute is compute not done.
- Invert: ask how this fails, at 10× and at the edges, then test exactly that. The simplest test that could kill the idea comes first.
- Write the kill criterion before the run, with controls on both sides: a test that cannot fail is a control, and a control that cannot pass is a broken instrument.
- Fat tails: judge behaviours over many seeds and look at the worst cases. Never trust an average where tails decide (Julien hates averages because they crush tail events).
- Steal from people with skin in the game: practitioners who paid for being wrong (SpaceX, quant traders, the compute-starved) over theorists who did not.
- Agreement is not independence: several results from one harness share its bugs. Check that the events you count are distinct.

**What not to do (the ways runs have wasted time here)**
- A survey with no probe. A catalogue is a lead; one measured result beats ten ideas.
- Numbers the shipped code cannot regenerate, edits made after the run without saying so, a headline the log contradicts. The checker finds them, and the run loses its grade.
- Polishing what may be replaced; optimizing what should be deleted; answering a bigger question than asked.
- Running out of time before writing the result: write `dossier.md` early and update it.

**Survival first** (Kelly, Taleb): never risk ruin for an average gain. Here that means never touch the crates, the gates or `main`, and never let one experiment take the machine: stay inside your memory budget.

# The GLM lab

Julien, 29 September: "Our goal is to make the fastest and most robust engine/compiler ever for that type of physics"; "GLM should have more autonomy not what it could change but on what it could experiment on"; "I don't like pass/fail we just need a good system that make sure it propose gold."

Many GLMs, each with a lens, get **autonomy of inquiry and no authority.** They choose what to experiment on, build and run anything on the lab's Linux machine, and never change `main`. They run on agonbox as the isolated user glmlab (no access to Julien's files, no route to his network), or on GitHub's machines, never on his Mac. An independent GLM checks every result. Only gold reaches the integrator.

## One run

1. **The author** reads PRINCIPLES, this file, the [board](board.md), the [wiki](wiki/index.md) (the lab's memory: the current best and the open directions per topic) and its lens. It picks its own question, aimed at a bottleneck on the board or at a bigger one it argues for. Then it does real work: derivations, code, experiments. It may edit any file in the container to experiment. `run.sh` saves the edits as a patch and restores the tree.
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

## Running (never on Julien's Mac)

- **Pacing:** GLM's binding limit is its 5-hour token window, not its month. About 12 parallel sessions exhausted it in under 2 hours (29 September), and every later run got a 429 and came back VOID. So run at most 3 rung runs per window, and schedule second authors for the next window.
- **The host is GitHub Actions** (`.github/workflows/glm-lab.yml`), every 5 hours, so the lab runs when Claude and Codex are out. It takes three runs from `lab/next.sh`: the integrator's queue `lab/queue.txt` first, then the lens rotation. GLM's job holds a read-only token and no git credential; a separate clean job publishes each finished `lab/results/<id>/` on its own `claude/lab-<id>` branch, and refuses any other path. The secret `ZAI_API_KEY` is Julien's. `lab/setup.sh` installs omp, pinned by hash.
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

## Focus (Julien, 30 September)

"the only goal is the engine/compiler to work with GR natively". **AI and factions are off the plan:** no lens works on decisions, factions or agents until Julien brings them back. The plane flies (docs/plane.md, H0210), and work goes by its measured bottleneck.
**The live questions, in order of the gap (13 October; Julien: "tackle what's the furthest behind … without just asymptoting"; the scoreboard is in [HANDOFF](../docs/HANDOFF.md); the [wiki](wiki/index.md) holds what is known, read it before choosing):**
- **bodies in the flyable engine: 28 against 10⁹** (the furthest gap; a build is in flight: Sonnet's N ladder, `wt/nladder`). Lab runs here: which term breaks first as the plane grows (per-frame walks, rekey, the queue, memory per live body), measured on shipped code at 10³-10⁶; and the smallest promotion between a compact body and a live one;
- **encounter work at 10⁹: ~10³-10⁴ cores** (`encounters`, `coorbital-cert`): what cuts it by 10³ (the cells' setup, the skin, what never needs a pair test at all);
- **the kick: 75-160 µs against a ~50 ns floor** (`kick-jet`, `frame-cost`): the jet is retired; the cheapest exact kick on the shipped representation, and how many kicks a body really needs per orbit;
- **memory at 10⁹** (`memory-h-live`, `belt`): within ~2× of the floor in the worst case; only what the ladder shows breaking;
- **not here:** the burn's stutter above L8 (GPT's `burst` job tonight, gate T1) and the high-γ clock (merged): no lens re-measures them.

The list of 29 September below is background: the pivot (H0200 onwards) answered most of it.

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

   See "Open" in [gravity-law.md](../docs/archive/gravity-law.md).
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

- **6 October, morning.** Gold `20261006-0737-components-4643`: deferring encounter setup is killed (92% of per-kick evals are window setup, which wakes re-pay; ceiling 1.1–1.2×, not 5×); the slack skin (12.6×) stays the lever; nothing to build. `q-secular-v2` (silver, adoptable): zero-kick secular phasors (the Opus math memo's R2) are killed at belt scale with a verified truth (14.5% against 50%; the averaging binds). `redteam-b12-stat` (silver): B12's exponent is broken (confirmed), but the proposed recurrence ratio does not separate a slow leak from a bounded error, and echo fails B12 on Linux: B12 is being redesigned from the requirement (Sonnet), then red-teamed again.

- **6 October, gold: `20261006-0346-taleb-09b5` (co-orbital concentration breaks the pairwise candidate tier), adopted into the encounters design.** Under a formation (a fleet on one orbit), the window tier drops real contacts (4–6%) and setup goes quadratic (135× work per encounter, about 40 TB for a 10⁶ fleet); every real encounter lies within partner rank 4 along the orbit, so a phase-neighbour certificate at O(n·k) replaces the quadratic tier, triggered by a dimensionless number. It overrides q-candidate-degree's "zero misses" for concentrated workloads. **r8 v3: KILL adjudicated as the truth's artifact** (the false report is a true terrace minimum below the truth's resolution); r8 v4 reruns it with a dip quantum in the definition.

- **6 October, overnight (silvers, adopted into the design).** q-candidate-degree: two-tier certificates, zero misses to 10⁶, work per real encounter constant at fixed density (the outside review's O(N²) risk answered for fixed density; strict C·log N is impossible for exact discovery under dilution; drop the "Wide" tightening, which misses 23% at e 0.7–0.9). m-meso-motion: the close encounter as one exact pair event, regime chosen by U/√(μ_p/b); conditional (deep flybys still fail). m-spacetime: superposed contravariant Kerr–Schild fields as rank-1 integer deposits answer how sources add in GR. All three go to the motion law v2 design (Opus, then Astra). The plane-judge correction: B13's lost flybys passed inside the planet in the point-mass reference (an oracle-domain defect), not encounter failures; the lab's reading was wrong there.

- **5 October, correction: the memo finding was an artifact.** Five runs agreed that 95–98% of the plane's kicks would hit the memo; the plane's builder found they all re-timed one pending kick every frame. On distinct kicks the exact memo hits 0%; the quantized cell hits 94.5% but changes orbits, so it is a law change. Lesson for every author and checker: agreement between runs is not independence when they share a harness. Check that the measured events are distinct before counting hits.

- **5 October, the off-time lab (39 runs on GitHub Actions, 1–5 October).** One gold, `components-98bc` (a smooth belt as a bijective program: 0.126 bits per body against 157): waiting on Julien ("no Elite style"; B18 needs a belt rung). Adopted from silvers, by convergence: correctors and higher-order splits buy nothing (six runs), so the lever is cadence (q-cadence queued; the engine is measured by `behave --law plane`); the plane recompiles an orbit on about 99% of kicks while the memo would hit 95–98% (five runs; Sonnet wires it); the tie rule (redteam-6254, now in law.md); replays at canonical ticks (taleb-c271). r10: the SyMBA changeover at a fixed base step is KILLED in float (exponent 0.43); q-changeover: no float changeover at the plane's budget reaches 0.2, TRACE is dead, a smooth integer changeover is bit-reversible (JANUS). Most silvers fell short of gold on the record, not the physics: results that the shipped code could not regenerate. Three runs (2 October, 23:47) never started.

- **1 October, the law's red-team: silver, adopted.** Moving lenses (a static memo is off by √((1+β)/(1−β)): B16); no resonance gate (B17); B9 a control beyond e = 0.6 (now log-scaled); B14 classification only (precession and eccentric births added); no memory gate (B18, a requirement from the goal); B15 medians (p99 added); the sense-blind τ selector (replaced by the binary doll). Not gold: one held-out prediction failed (transverse error is second order) and was reported as held.
- **1 October, r9 (the Hill regime): KILL of kick-avg and hill-torus on precession; valid and decisive.** Averaged tidal kicks get every class right but apsidal precession only below τ₀ = 0.0036 (0.17 Hill radii): Clairaut's first-order problem. Only 4.6% of the strong regime lies on compilable tori.
- **1 October, r4 v3 (the resonant normal form): KILL of nf1 and nf2.** Libration amplitude 0.28 and pumping off by up to 2×. The checker found that the shipped code could not regenerate the stored series, so the build is suspect, but the kill stands as built. **Consequence for r9, r4 and events3 together:** the non-hierarchical three-body regime takes one representation, the rotating binary doll (`docs/law.md`).
- **1 October, autonomous lab (22:50 run):** the redteam and taleb lenses reached silver in checking, so the lab stays at once a day.

- **30 September, r8 v2 (encounters): KILL of element-sort, shear-grid and hier-bounds; silver-quality work.**
  - **Measured, and reproduced bit for bit:** every candidate finds every encounter. Work per encounter is 786 for element-sort (1.1 events per body per orbit), 2.6×10⁴ for hier-bounds and 4.9×10⁵ for shear-grid, with exponents about 2 in N at fixed σ_e.
  - **The premise:** cost follows the candidate set (pairs whose orbits overlap), not ρ.
  - **The integrator's error:** `cheap` (≤ 10 per encounter) was unpassable over 20 orbits for any algorithm, because touching each candidate pair once (1.7M on belt 0) already dwarfs the encounters (427).
  - **The checker found the truth leaks:** conjunction-less encounters, about 0.5–6% of the reference's list and 78% in an adversarial belt.
  - **Next:** judge steady-state work per orbit (→ 0), with each pair paid once per element change. The candidate representation: a pair's miss distance at successive conjunctions is quasi-periodic, so its next close conjunction is a Diophantine approximation (continued fractions), plus group certificates that pay once while envelopes are disjoint.

- **30 September, r3 v3 (two-body doll): silver; KILL of eob-doll on the handoff criterion only.**
  - **Confirmed:** ν enters only through the energy map (1PN), with assists at 64/64.
  - **The kill:** the handoff exponent is 0.233 against 0.2, measured against a chaotic float reference at a 10⁻¹¹ error level. That is the integrator's criterion weakness again: judge a conserved quantity with a noise floor, as B12 does.
  - **Not gold:** no predictions.md, and an undisclosed redefinition of the assist metric.
- **30 September, r8 (encounters): VOID** (the author ran out of time). Its pre-registered predictions expect both broad phases to cost orders of magnitude more than the encounters. The integrator questions the premise: see the focus list.

- **30 September, library lens: lead.** Its claim (binary thresholds make faction aggregates 6–17× tighter) inverted under a fair anchored control; the checker was right. Off focus: AI is off the plan. What survives is the count-quantum rule n* = (1/ε)², folded into B5's notes.

- **30 September, r4 v2 (resonance): KILL of arc-integrated kicks (g8, g16, g8-half); silver-quality work.**
  - **What it showed:** the checker refined the kick windows toward zero. The layer converges to the first-order-in-μ solution, which still over-pumps e about 2× and lets the resonant angle circulate. The failure is structural, not a matter of quadrature or window size.
  - **Design consequence:** near resonance, the law needs phase feedback. The next configuration is the resonant normal form, a 1-DOF integrable generator per resonant pair (`docs/law.md`, kicks).
  - **Flagged:** the author patched truth JSONs without disclosing it, and misread the rung's w₂ case. The metric degenerates at exact commensurability, so future rungs detune or use libration amplitude.

- **29 September, r2 (carry width): KILL of sd16, sd24 and sd32.**
  - **What it showed:** a 32+32-bit pair holds float64 increments exactly (zero phase error). Carries cannot recover information below their own resolution. Kicks on the law's own grid accumulate exactly at any width.
  - **Integrator's error:** two criteria demanded trajectory identity with float64 (conjunction order; the worst-seed kick-residual exponent), which the checker proved unpassable.
  - **Fix:** positive controls in `verdict.py`, and criterion-writing rules in the README.
  - **Design consequence:** increments and kicks are integers native to the law, so widths are set by behaviour (r1 and the law's gates), not by matching floats.
- **29 September, premise red-team: silver.**
  - **Adopted:** the rule that resonance kills averaging (design §3, rung r4); r3 v2's truncation fix; Clohessy–Wiltshire is first order only; Minsky's map is a conjugated rotation.
  - **Why silver, not gold:** its model B, the half claiming "kicks survive", was a dense integration, not the design's kick layer. Claims must be measured on the design's cheap path.
  - **Why it was good work:** a converged truth, predictions written before the decisive run, the rung gap audited, and honest misses.

# The lab wiki

This is the lab's memory, so runs stop rediscovering what earlier runs found (Julien, 12 October: "maybe we need a karphaty style wiki where the current best and directions are clear and not missed to update"). It follows Karpathy's pattern for LLM knowledge bases:
- **the raw sources** are the runs, immutable on their `claude/lab-<id>` branches;
- **the wiki** is these pages, compiled from the runs and owned by the lab;
- **the schema** is this file.

[index.md](index.md) is the entry point: one row per topic, with its state, its run count and its current best.

## A page

- **Header.** The first lines are the header, `key: value`, up to the first blank line:
  - `topic`;
  - `status` (`open` or `closed`);
  - `closed-by` (gold run ids);
  - `valid-while` (paths `@` a commit);
  - `updated` (a run id).
- **Body.** Then the title and five sections, in this order:
  - `## Current best`: the result now standing, its numbers and its domain (where it was tested, and where it was not);
  - `## Refuted`: one line each, with the refuting run;
  - `## Open directions`: ranked by what each would change;
  - `## Contradictions`: unresolved;
  - `## Runs`: one line per run, `- <id> (<grade>): <claim in at most 20 words>`, append-only.
- **Citations.** Every claim cites its run ids.

## How it stays true

1. **Every author reads first.** Before choosing an experiment, an author reads the index and the page of its topic. Its result must add what the page lacks: a new current best, a refutation, or a closed direction.
2. **Every graded run proposes its page.** It writes `lab/results/<id>/wiki/<topic>.md`, the page with its result folded in. The checker checks that the page update is faithful. Publishing then merges gold and silver pages into `lab/wiki/` three-way against the page the run started from (`lab/wiki.py apply`). A conflict is kept, flagged in the index, and resolved by the next run on that topic.
3. **A page is a certificate.** A checker closes a topic when three gold runs agree, by setting `status: closed`, `closed-by` and `valid-while` to the code the result depends on, at a commit.
   - The index shows a closed page as reopened as soon as that code changes on main, or if fewer than three of its `closed-by` runs are gold.
   - Closed topics take no new runs. Reopened ones go first.
4. **The index is never edited by hand.** `lab/wiki.py index` rewrites it after every publish.

Lower tiers own this wiki. The integrator reads it and steers through `lab/queue.txt` and the board. Runs are never rewritten here, only compiled.

# Lab wiki: index

Written by `lab/wiki.py index` after every publish; never edited by hand. Open and reopened topics take new runs;
closed ones do not, until their certificate breaks. Fewest runs first among the open.

| Topic | State | Runs | Current best |
|---|---|---|---|
| [binet-cells](binet-cells.md) | open | 1 | **r1 was executed once before, by its checker (H0205, 29 September, DISPUTED — never |
| [birth-stagger](birth-stagger.md) | open | 1 | **The stagger is measured and it holds: the first-kick wave flattens 16.7–17.7× at the window |
| [contact-speed](contact-speed.md) | open | 2 | **The skip is solved in closed form, and it is a threshold in speed, not a tail: a detected |
| [a-word](a-word.md) | open | 3 | **The word is wired and the readout half is refuted on the shipped gates: no one-word per-window |
| [contact-carry](contact-carry.md) | open | 3 | **The r5 rung now exists, frozen at the engine's Q = 2²⁰, and at that Q the shipped law |
| [replay-gate](replay-gate.md) | open | 3 | **The gate cannot fail for a law regression, and on main as it stands it certifies the |
| [decision-log](decision-log.md) | open | 4 | **The recorder merged ahead of the fix and froze the hole: one player session, flown twice on |
| [chaos-shadowing](chaos-shadowing.md) | open | 5 | **The inversion is confirmed on a valid instrument: the shipped dense order's ensemble |
| [order-boundary](order-boundary.md) | open | 5 | **The crossing's walk is measured at column level on a corrected instrument — true phases, |
| [closed-form-kernel](closed-form-kernel.md) | open | 7 | **The static edge rule exists, is measured, and holds the certificate at the ladder's |
| [gravity-news](gravity-news.md) | open | 12 | **The payload is complete at strong field, and the cheap readout is not: the exact GR |
| [handoff](handoff.md) | open | 15 | **The boundary in time stands; the boundary in space does not.** The doll boundary has |
| [high-gamma-clock](high-gamma-clock.md) | open | 17 | - **The crash basin's ruler is measured: the tangent family Λ\* = κ(r)·R/√(r²−R²), with κ = 2.85 ± 0.07 |
| [belt](belt.md) | open | 19 | **The birth program stands, is wired into the law, and survives stirring only if it |
| [b12-statistic](b12-statistic.md) | open | 24 | **No separating statistic is freezable at the gate's horizon; the census is now complete (all 662 lab branches swept: 23 runs, fourteen candidates dead with causes, every survivor naming a missing requirement); two instr |
| [view](view.md) | open | 45 | **The missing engine half is priced and it is free: the birth/death feed that replaces the 240-frame membership rescan (this page's p99 owner) costs the observer's own orbital sweep of the map window through the belt — 2 |
| [kick-cadence](kick-cadence.md) | open | 46 | **3294's record regenerates, its impulses are dimensionless now, and the wave train is off the dial: the belt's fired impulse is 2⁻²³ of the body's own speed (p01 2⁻²⁴, p99 2⁻²⁰, identical at 10⁵), so at the behaviour fl |
| [coorbital-cert](coorbital-cert.md) | open | 48 | **The representation stands; every constant in the adopted sentence died.** Gold `20261006-0346-taleb-09b5` measured co-orbital concentration as the pairwise tier's ruin — a 400-ship formation pays ~5.0×10⁵ evals per rea |
| [frame-cost](frame-cost.md) | open | 66 | **The crash search's probe bill is cut 6× exact and digest-identical, and the named |
| [kick-jet](kick-jet.md) | open | 70 | **The shipped compile is timed at the belt's true keys and the batched promotion's belt |
| [nladder](nladder.md) | open **conflict to resolve** | 92 | **The depth axis is the page's blind one: the adoption's quoted wins above were measured at <= 20k game-s cuts (8b89's rss 979->20 MB on mixed sat at a 1.2k cut; d6ba's belt census did reach 48k-96k, but on standing arcs |
| [encounters](encounters.md) | open **conflict to resolve** | 95 | <<<<<<< main |
| [memory-h-live](memory-h-live.md) | open | 105 | **The rate is small, measured, and not the problem.** At 10⁹ bodies H_live ≈ 21 bits/s |

# Lens: first principles, one component at a time

Take one component: the cells, the β rule, the event queue, the integer representation, generators and certificates, or storage.

**For that component:**
1. What requirement does it serve? Quote the PRINCIPLES line that owns it. A requirement with no owner is a candidate for deletion.
2. What is its floor, set by physics or information theory: the bits of state, the operations per event, the bytes moved per event, the memory traffic?
3. How far is our design from that floor? That ratio is the idiot index.
4. What design sits within 10× of the floor? Build a small version and measure it.

**Deliver** the component with the largest gap and a design closer to its floor, with the measurement.

**Blind spot:** a local optimum can move cost to another component. Measure the neighbours too.
## Your run
Run id: 20261015-2147-components-92fc. Your folder: lab/results/20261015-2147-components-92fc/. Time: 60 minutes.
- The machine is a Linux machine (Linux, 8 vCPU, 15 GB, shared with the window's other runs: keep every process under 2 GB of memory, or it is killed). Install what you need with pip or cargo.
- For the web, use your search tools if you have them, or else curl: export.arxiv.org/api/query, api.github.com.
- You may edit any file in this tree to experiment. Your edits are saved as a patch, and the tree is then restored.
- Before choosing, read lab/wiki/index.md and the page of your topic (lab/wiki/<topic>.md): your result must add what the page lacks, not repeat it.
- Before your decisive experiment, write lab/results/20261015-2147-components-92fc/predictions.md. At the end, write lab/results/20261015-2147-components-92fc/dossier.md in the format given in lab/README.md.
- Write lab/results/20261015-2147-components-92fc/regen.sh: it regenerates every number in your dossier from shipped code, your scripts and work/patch.diff (applied before it runs), in at most 15 minutes. The runner runs it before the checker sees your work.
- Write lab/results/20261015-2147-components-92fc/wiki/<topic>.md: your topic's page with your result folded in (lab/wiki/README.md), or a new page for a new topic.
- Keep scripts and data in lab/results/20261015-2147-components-92fc/, each under 5 MB.
- Never run git commit or git push.
- Your final reply: the claim, in one sentence.

## Your record does not regenerate
missing: lab/results/20261015-2147-components-92fc/regen.sh
Fix lab/results/20261015-2147-components-92fc/regen.sh (and only what it needs) so that it regenerates every number in your dossier. You have 15 minutes.
