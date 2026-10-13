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

Julien, 12 October: "fly like the sr 71". Work only in `/private/tmp/emergent-wt-frame` on branch `wt/frame` (from `origin/main`). Commit there; never merge. End commits with `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`. Each test ≤ 60 s. Return at most 10 lines. Another builder is working on `wt/play` (scenario heading, the HUD, plunges in crates/space): keep out of `scenario.rs`, `view.rs`, `page.html` and `crates/space`.

### The fact (the integrator's flight sweep on the M1, 12 October)

`cargo run --release -p emergent-universe --example flight_sweep -- 100 20` flies the page's frame loop at rtf 100. From throttle L8 up, the worst frame hits the 12 ms engine budget and the presented time lags the frame's target by up to 1.6 s of game time: a visible stutter. Coasting frames take about 8 ms.

### What the lab measured (gold runs; their patches are on their branches, `git show origin/claude/lab-<id>:lab/results/<id>/work/patch.diff`)

- `20261012-0036-quant-115e`: the presented frame pays ~43–60 ns per planned body even with zero events (the per-frame `rekey` of every deadline). The kick is 70.7% rebind bookkeeping, with an 11× tail at p99.9. Lever: lazy deadline re-keying, O(events), bits preserved.
- `20261010-0656-second-20261010-0541-system-d51f-3e48`: the incremental deadline (the last doll-chain readout carried forward by its velocity, re-anchored by a real walk only when the carried displacement could pass 1/8 of the light distance) deletes the scheduler's per-event walk (1,123 → 42 walks at seed 7, rtf 100). Digest and view are bit-identical at settle cuts in eight flight configurations.
- `20261011-1729-components-b063`: a kick costs a median 75.6 µs against a floor of ~42 ns, and 89% of it is the rebind (the per-kick tube refit plus step re-derivation). **Its proposed lever, the multiply-add "jet", is retired** (docs/law.md, 12 October: six golds refute it). The refit stays exact.

### In order

1. **Measure on the M1 what a held L8 and L15 frame spends**: kicks per frame, the cost per kick by stage, the rekey and the walks, the rest. Write it down before changing anything.
2. **Land the bits-preserving levers:** lazy re-keying and the incremental deadline. Port them from the golds' patches, rebuilt to this code as it is.
3. If the frame still overruns, **find what else deletes cost with every digest bit for bit:**
   - fewer refits per frame where the state cannot have changed by a quantum;
   - work done once per frame instead of once per kick;
   - the refit itself made cheaper, exactly.

   **Never a law change:** if one would help, write it up and stop.

### The gate (frozen by the integrator, 12 October)

**F1, smooth flight:** in the sweep at rtf 100, 20 s per flight, at every level 0–15: zero frames over the 12 ms budget after the first second, and a lag of zero. Report the worst frame time and the worst lag per flight. Every digest must be bit for bit: run the replay and digest tests, and compare `Universe::digest()` before and after on at least five scripted flights. The whole `cargo test --release -p emergent-universe` stays green, and B13 is not worse than 60/64 at step 7.

Merge `origin/main` before your final runs. Report F1 before and after, the stage costs before and after, and the digests.
