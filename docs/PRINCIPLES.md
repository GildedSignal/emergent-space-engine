# The goal and the philosophy

These are Julien's words. Every model reads this before acting, and every specialist prompt begins with its first two sections. Models propose changes and never reword. Julien can be wrong: each statement is remembered and then either followed or disproven with evidence. Silence is never disproof.

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

## Proposed principles (awaiting Julien)

None pending. Models propose here; Julien approves, rewrites or rejects.

## Register of Julien's statements

Status words: **Followed** (built, or a rule in force), **Adopted** (decided in a living doc, not built), **Partly**, **Drifted**, **Open**, **Disproven** (with evidence), **Superseded** (by his later words), **Unendorsed** (not his).

| Statement | Source | Status |
|---|---|---|
| Multipoles as the core mechanism of gravity, of aggregate sources (ships), and of causality regions | OC; about 10 times | **Adopted, not built:** in the v1 draft from day one (gravity-law.md). Never built before: one GEM quadrupole failure (0.478, H0139) was generalized into a ban (H0196). No mechanism for causality regions yet (engine.md rule 11) |
| A failed experiment kills the configuration, not the method | about 5 times | **Followed:** principle 9 |
| Behaviours, not continuum fidelity; error type over size | OC; repeated | **Adopted, not built:** the v1 draft gates on behaviour and error type (H0195). Drifted H0184–H0194 |
| Less is more; make compute cheap | throughout | **Followed** |
| Clocks and observables are emergent: derived, never computed ahead | 29 September | **Adopted:** principle 3, v1 draft B7; not built |
| One engine, not five modes: "yes, why not one?" (chronon only as a test judge) | CL 09-29 08:05 | **Adopted, not built:** engine.md is one engine; the code still has five modes |
| Measure like the player, heat included, with the state recorded | 28 September | **Followed** (AGENTS.md) |
| Sonnet for well-scoped work, Opus for hard problems and decisions; "You can abuse GLM"; "It's a wildcard that we're underestimating"; GLM for red-teaming and autoresearch | CL 09-28 12:10–18:56 | **Followed** (AGENTS.md). "Volume without authority" and pull-based loops are the integrator's, approved with the architecture (H0191) |
| "GLM should have more autonomy not what it could change but on what it could experiment on"; "Don't run on my machine use the cloud session"; "I don't like pass/fail we just need a good system that make sure it propose gold"; "an independent GLM that checks its work is good" | CL 09-29 | **Adopted:** [lab/](../lab/README.md) (lenses, independent checker, gold/silver/lead with reasons); it runs once the cloud environment holds the key. Supersedes the pull-based loops |
| "Our goal is to make the fastest and most robust engine/compiler ever for that type of physics" | CL 09-29 | **Adopted:** the lab board's target. A candidate line for the goal: his call |
| "we need to think in terms of requirements and from that find out what the best solution is not just based on what is normally done, that's how we got as good as we are now"; "We should tackle bottlenecks as much as possible" | CL 09-29 | **Adopted:** the scout lens and the lab's bottleneck board |
| "we need to make light speed hardware native… light speed is basically how fast the causal chain is updated"; "a causal cellular automaton"; "rethink our units from scratch, time and spatial ones", "tied to hardware and end goal"; "we need to expand what steps mean"; "we want to guess in a way that is perfect how the simulation will run to bypass it"; "we are ok with errors but we want them consistent across the different types of simplifications"; one number representation for every unit ("less components") | CL 09-29 | **Open, top of the lab board** (bottleneck 0). The v1 gravity freeze waits for it |
| Speed is reported as a real-time factor, since effective c depends on it | CL 09-27 10:20 | **Followed** |
| Every test ≤ 60 s | 26 September | **Followed** |
| Everything emergent; no scripted events, designed families or central control | 27 September | **Followed** |
| The heading card and principles live in git; Julien owns them | 28 September | **Followed** |
| "don't create busy work"; "not doing too much parallel work because the real issue is caching when you go back to working to finish half done jobs" | CL 09-28 12:10 | **Partly:** three or four jobs often run at once; limiting parallel work to read-only briefs and judges is the integrator's reading |
| "broken record moment again, but… hypergraphs?"; "can we learn things from wolfram's hypergraphs?" | OCC#12; CL 09-26 09:17 | **Drifted:** a hyperedge IR existed (H0016), archived at H0182, in no living doc |
| "NO never do that please never dumb down for no reason" (the AI chose Barnes–Hut over FMM "because it's much simpler") | OC#34 | **Drifted** until H0195 (FMM never built, H0196); principle 1 keeps "never dumb down" |
| "what if we were to push the min-plus idea to the extreme not just on one thing?" (OC#42); ABP: "Use min-plus for admissible arrival-time composition" (ABP line 118) | OC#42; ABP | **Adopted in the draft** [representation.md](representation.md): min-plus composes arrival times, light-cone spread and scheduling, as the logarithm of ordinary arithmetic. Not built |
| "I would actually make caching part of the mathematics" yes huge | OC#44 | **Partly:** certificates (engine.md); region response operators absent |
| "how we managed to make 1B ships take basically no space (which we can improve even more)" | CL 09-27 09:08 | **Drifted:** families archived at H0182; HANDOFF now tracks their return |
| "the light cone grows continuously meaning that there will always be a point where we cannot handle the universe anymore" | OC#50 | **Open:** a HANDOFF risk |
| "the algorithm that allocates the work… it's the most important one"; "you did not talked about the entropy for knowing where to compute you will do this right?" | CL 09-25 14:28; CL 09-28 09:48 | **Adopted, not built:** was step 7 of 10; HANDOFF now builds it with the one engine |
| "gpu should heavily be used for anything i believe."; "we need to leverage AMX too"; the Neural Engine for speculation | CL 09-25 14:40, 15:58, 15:48 | **Adopted:** engine.md and the v1 draft allow the GPU (until 29 September: "Metal only for dense contacts"). Machine probes pending |
| "since it is deterministic we could have human readable codes"; "a checksum word is a good idea" | CL 09-25 15:48, 15:58 | **Adopted, not built** (engine.md share codes) |
| "we can even have regions that are delayed if not on screen" | CL 09-25 14:28; OCC#8 | **Adopted** (engine.md rule 8) |
| "we need to monitor resource allocation" | CL 09-25 14:06 | **Followed** in test-ladder rule 6 (utilisation, real-time factor) |
| "one thing i'd like to exploit for the future is debris, maybe i'll go voxel like so keep that in mind" | CL 09-26 08:18 | **Open** |
| "communication in more inverse square law like" | CL 09-26 08:18 | **Open** |
| "we need to leverage better for collisions that ships are small" | CL 09-26 08:45 | **Open** |
| "how does it compare to the competition" | CL 09-27 09:39; OCC#0 | **Open:** one comparison in the continued conversation |
| "gravity is intrinsic to this spacetime compiler so we should act like it"; "i don't think we need newtonian gravity but rather an aprox of gr"; "weak gravity is derived from the strong one i believe" | CX 09-12 11:51; OC#34; CL 09-25 11:58 | **Adopted** (H0195, one flow law, GR oracle) |
| "it's the actualization of moving objects that's problematic"; "we only care about changes" | CL 09-29 08:24 | **Adopted:** the amended v1 draft has no per-body steps; the H0195 draft had them |
| "planet more influence than ship means that you can be corse and refine easily" | CX 09-14 09:17 | **Adopted:** curvature-sized cells (v1 draft) |
| "gravity is light speed and that's a good help for us but also it decays fast" | CX 09-14 09:37 | **Adopted:** moments read at the retarded time (v1 draft) |
| "I want black holes because they create very interesting gameplay but i don't care yet about past the event horizon" | CL 09-27 09:08 | **Adopted:** v1 B6; Kerr later |
| "what if one ship influences the path of an asteroid over time?"; "In tests we also need to see how galaxies and solar systems behave, maybe looking at 3 body problem too" | CL 09-25 12:10; CX 09-14 09:17 | **Adopted:** physics ladders (test-ladder.md) |
| "can't we \"giggle\"?" (iterate a rough estimate) | CL 09-27 09:08 | **Open** |
| "wow why?", on Kerr and inspiral being cheap | CL 09-28 09:48 | **Answered 29 September:** in the plane, Kerr keeps rotational symmetry, so its orbits still repeat; inspiral is a per-cycle ΔE and ΔL (Peters): additions ([representation.md](representation.md)) |
| "fair point", on starting from exact GR solutions | CL 09-28 09:48 | **Superseded:** "you've confused a bit oracle and implementation" (CL 09-29 08:24); H0195 |
| "instead of projecting gravity onto space why not look at the relations between the celestial bodies" | CX 09-14 09:55 | Tried (`es-relational-hierarchy-v0`), archived |
| "it's simultaneity tolerance of the universe"; "chronon is just the floor more than the ruler" | CL 09-26 09:31 | **Followed** (universe-quanta.md) |
| "do we even need floors?" | CL 09-26 17:32 | **Disproven:** one floor is needed (H0173, universe-quanta.md) |
| "if its close to me then i care about the precision" | CL 09-26 09:31 | **Disproven:** refinement may never depend on observation (universe-quanta.md) |
| "what if simply we fix them to fp32 or something like that? simple." | OC#40 | **Disproven:** floats never decide outcomes; filters only |
| "one thing to be careful about like with wolfram's idea is the order of operations because we're quantitized" | OC#38 | **Followed** (schedule independence) |
| "ooooh" (bit-wise reversibility); "smart" (effective quanta q_k = 2^k q_0) | OC#42 | **Open:** not adopted |
| "could we use quaternions" | CL 09-26 20:00 | **Open:** unanswered |
| "So our tests shall be more qualitative then quantitative I just have to look at them" | CX 09-14 09:17 | **Partly:** gates are numeric; the viewer comes with the player slice |
| "the goal is simply to have the right behaviors and simplify how we test for them with litmus tests" | CX 09-14 09:17 | **Adopted** (v1 behaviour gates) |
| "i'm strafing away from success"; "the doc should be clear on what's the goal i think that may have been the issue" | CX 09-12 21:15, 21:26 | **Followed** since H0197; ignored for 17 days before |
| "as we're converging towards something tighter i'd expect the need to use more bigger models in proportions" | CL 09-28 18:56 | **Open:** not in AGENTS |
| "we need a whole system to run this project for the long term that doesn't grow out of hand" | CL 09-28 14:51 | **Followed** (AGENTS text budgets) |
| "Julien predicts before each run" (HANDOFF step 4 until 29 September) | none: added by the integrator (862ab8a) | **Rejected** by Julien: "i don't like that too slow my words are the intended behaviors i'm seeking" (CL 09-29) |
| "\"a million ships\" a billion*" | CL 09-27 09:08 | About something else, not local laws (Julien, 29 September); removed from principle 15 |
| "I want it to be believable at all scales" | CL 09-25 12:10 | **Adopted:** rungs up to galactic nuclei |
| "we need a map, but a map that is inferred based on intelligence for the territories"; "the historical map is the unchanged map which is very different form the actual map" | OC#16; OC#34 | **Open** |
| "flag like in real to know who belong to who but with a reputation system"; "the more it is transmitted the looser it is" | OC#16 | **Open** |
| "oh i could fast pace the game such that I know what happens without intervention so that I can create the missions" | OC#16 | **Open** |
| "it needs to be rewarding at multiple time scales"; "i just don't want the rock paper scissors" | OC#16 | **Open** |
| "the world should be able to be HUGE, basically infinite but life shall spawn not everywhere"; "About world size is there any real limit? Like is it better to use local/relative coordinate system or global?" | OC#30; CL 09-29 | **Open:** answered 29 September (exact integers set no distance limit; hierarchical local coordinates proposed); awaits his choice |
| "gravity, spacetime, light spectrum, factions, resources, money/market, relations" | OC#28 | **Open:** light spectrum is absent |
| "I need a good visualization to see what's happening with god's view"; "I don't see the sub-luminic travel I want to see that don't loose the soul" | OC#16; OC#20 | **Partly:** only a float viewer is planned |
| "the transitions between the scales should be seamless"; "use those indicator rings to display things like proper time vs ship time" | DC | **Open** |
| ABP: "bounded FMM as the primary acceleration candidate"; "All mass participates, including ship populations" | ABP | **Adopted again** in the v1 draft (drifted H0184–H0194); not built |
| ABP: "Randomness is keyed by stable semantic identity, event, seed, and purpose" | ABP | **Open:** in no living spec |
| ABP: "spatial quadtree crossed with an independently refined dyadic time tree" | ABP | Replaced by density-sized cells (H0177) without his recorded approval |
| ABP budgets: "at most 4 GiB"; "at least 30 FPS at 1080p"; "within one hour from cold start"; "at most 20 GiB" | ABP | **Open:** dropped from the living docs (last seen near H0146), neither followed nor disproven. 20 GiB exceeds the ~10 GB free disk; the one-hour run is a scenario, not a 60 s test |

**Source keys.** OC#n and OCC#n: Julien's turn n in `docs/reference/original-conversation.md` and `original-conversation-continued.md`. CL and CX: his Claude Code and Codex messages, by date and time (2026). DC: the design chat he pasted on 25 September. ABP: `docs/reference/approved-build-plan.md`, AI-written, approved by him around 11 September. The two minings and the turn numbering: `artifacts/evidence/philosophy-mining-20260929/`.

## Contradictions (kept side by side)

| Topic | Earlier | Later |
|---|---|---|
| Ships as sources | "ships can be not taken into account for gravity of celestial bodies or even between themselves tbh" (OC#34) | "yeah let's do that to allow emergence" (OC#40); "they can't just be dismissed like that." (CL 09-27 09:25) |
| Strong gravity | "maybe i should drop the two black holes idea" (CL 09-25 11:58) | "I want black holes because they create very interesting gameplay" (CL 09-27 09:08) |
| Ticks | "don't think in terms of Hz" (OCC#8) | "do we need to run at 60hz while maybe 12Hz interpolated would work?" (CL 09-26 08:18) |
| Proximity | "i kept saying that for a reason" (near/far, OC#50) | "if its close to me then i care about the precision" (CL 09-26 09:31) |
| Floats | "divergence is not a joke and it compounds" (OC#34) | "what if simply we fix them to fp32 or something like that? simple." (OC#40) |
| Forecasts | "not rely on predictions much is my call" (OC#36) | "i think we need some messy calculations to have a better idea of where to spent compute" (CL 09-25 15:34) |
| Gravity path | "fair point" (exact GR first, CL 09-28 09:48) | "you've confused a bit oracle and implementation" (CL 09-29 08:24) |
| Smoothness metric | "i care about the p95/99 results" (CL 09-25 14:06) | the plan he approved: "The target is the single worst frame, not p99." (CL 09-25 16:18) |
| When to optimise | "optimization is paramount from the start" (CX 09-14) | "don't start implementation yet" (CL 09-28 09:48) |
| Parallel work | "implement in parallel as much as possible the build" (CL 09-25 16:18) | "not doing too much parallel work because the real issue is caching" (CL 09-28 12:10) |
| GPU | ABP: "enable a GPU path only when matched full-pipeline measurements show a benefit" | "gpu should heavily be used for anything i believe." (CL 09-25 14:40) |
| Test length | ABP: the billion-ship run "within one hour from cold start" | "remember 1min max per test" (CL 09-26) |
| MVP | "for the mvp let's keep it realistic" (OC#16) | "ok stop thinking of MVP this is polluting your thinking" (OC#34) |
| Graphics | "graphics don't matter" (OC#16) | "use real materials, don't make it overly saturated and contrasted" (DC) |
| Minimap | "there's a minimap but first let's discuss it" (OC#16) | "i don't believe that we need a minimap" (OC#30) |
| Multipoles | "i'm really a broken record" (OC#34) | "i was led to believe that FMM was a bad move" (CL 09-29 08:39) |
| FTL | "i don't want FTL because of paradoxes" (OC#16) | "if i had more time i could play with the paradoxes of ftl" (OC#16) |
| Game versus GR | "we need not to forget that it's a game" (CL 09-25) | "we need to build towards GR that's the goal" (CL 09-26 08:18) |
