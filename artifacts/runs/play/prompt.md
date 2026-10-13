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


## Your job (Claude Sonnet, a builder; Claude Opus integrates)

Julien, 12 October: "we want something functional, gotta play that game one day, i just don't want it buggy, fly like the sr 71". Work only in `/private/tmp/emergent-wt-play` on branch `wt/play` (from `origin/main`). Commit there; never merge. End commits with `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`. Each test ≤ 60 s. Return at most 10 lines.

### The facts (the integrator's flight sweep, 12 October)

`crates/universe/examples/flight_sweep.rs` flies the player the way the page does (60 frames a second at rtf 100, scripted keys). Every loss in 20 s flights was a crash into Home:
- **The nose starts retrograde.** The ship spawns at 90° on a counterclockwise orbit, so it moves along −x, while `Thrust.heading` starts at 0, which is +x (`crates/universe/src/universe.rs`, `scenario.rs`). "Forward" therefore burns the orbit down into the planet.
- **The HUD never warns of the impact,** though the engine plans it: `Item`'s impact certificate in `body.rs` is the tube's periapsis below the surface.
- **Braking to rest is refused.** Separately and known, braking to rest above the planet gives `NoBoundOrbit` (a radial plunge has no tube). Codex's partial branch `origin/wt/cx-b-plunge-tubes` compiles inward plunges; outbound returns and the plane's integration are unfinished. Read its evidence before starting.

### In order

1. **Start the nose prograde:** the player's initial heading is along its initial velocity. Fix any test that assumed heading 0 by flying "forward" prograde. Say which digests change, and why.
2. **The HUD warns of an impact course.** The view exposes the planned impact (what, where, and in how many game seconds), and `page.html` shows it plainly: "Impact course: Home's surface in 3 min 12 s". It clears when the orbit no longer crosses a surface. A test checks the warning appears no later than the plan exists, and clears.
3. **Braking to rest is a plunge, not a refusal.** A radial or near-radial state gets a tube, inward and outward, built on Codex's branch: the ship falls, and the player can burn back out. A frozen gate (yours to write first, then run, never weaken): **P1, the plunge**, from rest at r₀ = 2, 5, 20, 100 and 1000 planet radii. Over every case: the time to the surface, in coordinate and in proper time, against exact Schwarzschild radial infall, worst relative error ≤ 1e-2; zero refusals; the ship alive until the surface.
4. **Rerun the sweep,** adding a prograde forward burn, a retrograde brake to rest, and a brake-then-burn-out. Report each line.

### Must hold after

- `cargo test --release -p emergent-universe` and `-p emergent-space`, whole;
- `cargo run --release -p xtask -- behave --law plane --gates B13`: not worse than 60/64 at step 7;
- G1–G6 unchanged;
- the flight view still serves (`cargo run --release -p xtask -- universe --rtf 100`, then `curl -s localhost:8792/ | head`).

Merge `origin/main` before your final runs: main may have moved (the clock fix lands there first).
