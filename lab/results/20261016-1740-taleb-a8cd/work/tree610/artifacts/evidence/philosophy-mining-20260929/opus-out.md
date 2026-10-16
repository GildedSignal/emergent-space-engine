I read the whole corpus: the three message files, both conversations with the AI replies, and the approved build plan. I changed no repository files. Every quote below was checked verbatim against the sources with a script, and each is under 25 words.

**Source labels.**
- **OC#n**: Julien's turn n in `docs/reference/original-conversation.md`, dated before 11 September.
- **OCC#n**: `original-conversation-continued.md`, undated.
- **DC**: Julien's turns inside the design chat he pasted in Claude on 25 September at 11:43. The chat itself is undated.
- **CL**: `claude-user-messages.md`, cited by date and time.
- **CX**: `codex-julien-messages.md`. Only its 11–24 September entries are unique; later entries repeat CL.
- **ABP**: `docs/reference/approved-build-plan.md`. The AI wrote it; Julien approved it with "PLEASE IMPLEMENT THIS PLAN" around 11 September.
- **RM**: the steering quotes in `docs/reference/README.md`.

---

## 1. Missing principles and philosophical facts (ranked by importance to the goal)

**1. Smoothness is the objective, and the allocator is the key algorithm.**
- OC#36: "minimize spike compute and average compute usage so that you get a bigger simulation that runs smoothly"
- CL 09-25 14:06: "i care about the p95/99 results i want the game to be smooth"
- CL 09-25 14:28: "the algorithm that allocates the work to prevent those heavy tails, it's the most important one"
- CL 09-25 14:06: "we must be able to compute faster than what's happening"
- Gap: the goal says "runs smoothly", but no principle names tails, the joint objective, or the allocator's rank.
- Proposed: *The objective is the biggest world that never stutters. Minimise spikes and average load together; the worst frame is the target, and the work allocator is the most important algorithm.*

**2. Spend the whole M1: GPU first, memory as the bottleneck.**
- CL 09-25 14:40: "gpu should heavily be used for anything i believe."
- CL 09-27 09:08: "spacetime is fundamentally the most gpu thing in our system we need a huge amount of parallel compute"
- Same message: "we need to be deeply aware of von-neumann bottleneck and memory"
- CL 09-25 15:58: "we need to leverage AMX too"
- CL 09-25 15:48: "i like the idea of using the AI cores for speculation, it would be unused compute anyway"
- CL 09-25 14:06: "a good algo will efficiently use all of our compute available"
- OC#40: "exactly that was the reason I was thinking of that", on the AI's line that CPUs wait on memory.
- Proposed: *Use every engine on the M1: the GPU by default for spacetime-parallel work, AMX and the Neural Engine where they fit, and idle time buying the future. Budget memory traffic before arithmetic.*

**3. Errors never compound.** PRINCIPLES says "error type over size" but never forbids compounding.
- CL 09-25 14:28: "basically we don't want errors that can compound that's the goal"
- OC#34: "divergence is not a joke and it compounds"
- OC#42: "types of errors and not just errors. because that could change the behavior more than anything else"
- Proposed: *An error may be large but must never compound: bounded or self-cancelling error only, and no secular drift.*

**4. Discrete by design: coarsest quanta, cheapest arithmetic.** This is the direct antidote to the continuum-exactness drift.
- OC#38: "there's no continuum, physics may be quantitized but appear continous at the right scale"
- OC#38: "it's just what's the biggest quantization that we can get away with?"
- OC#38: "no it's about what's cheapest to compute"
- OC#38: "physics loves e while we love 2"
- OC#38: "yes exactly", on "the simulator never makes numerical mistakes relative to its own laws"
- CL 09-25 12:10: "we don't care about values but about behaviors"
- Proposed: *There is no continuum to match: our discrete law is the physics. Use the coarsest quanta and the cheapest (base-2) arithmetic that keep the behaviours.*

**5. Representation first, from requirements, never from a list of methods.**
- CL 09-27 09:08: "we just need to have the right representation so that math is trivial."
- Same message: "you start from a listicle instead of what are our requirements and what would be the best representation"
- Same message: "the less stupid requirements and knowing our constraints"
- OC#38: "the space should make our expensive operations trivial and maybe that's it"
- Proposed: *Start from the requirements and constraints, then pick the representation in which the expensive operation disappears.*

**6. One law at every scale, and no bandaids.**
- CL 09-25 11:58: "I'm very wary of mixing too much systems for no reasons i don't like bandaids"
- CL 09-25 14:28: "that doesn't feel like a smart fix and more like a bandaid, it works in just one case"
- CX 09-14 09:37: "how to have the same mechanics at all scales while not doing the work"
- OC#48: "all of those emerge from the same physical law." and "yes that's the step towards unification of all of our ideas rather than another coat of paint"
- CX 09-14 09:17: "I really can sense a simple thing in unification to do the math for gr."
- Proposed: *One law and one mechanism at every scale. A fix that works in one case is a bandaid, and every new subsystem needs a reason.*

**7. Test behaviours across many seeds; never engineer an outcome.** The old engine line had "Julien's rule: … many-seed capable; fixed ICs are not the universe" (`docs/HISTORY.md` ~line 2191). It is gone from every current doc.
- CX 09-14 09:17: "because it happened to work like that not because the laws were made for it to work"
- CL 09-25 12:10: "if you're looking for a certain arc but you're not getting the same it's not an issue if you get the right behavior"
- CX 09-23 11:07: "if you're actually testing behavior or the bad idea of expecting the same data"
- OC#48: "we want determinism ≠ realistic trajectories"
- OC#40: "how many A weather system is not the same as making THE weather system."
- Proposed: *Judge behaviours over many seeds, never one seed's data. No law is tuned to produce a particular outcome.*

**8. No tick and no frequency, not even per body.** Principle 3 does not forbid per-body stepping.
- OCC#8: "don't think in terms of Hz we've already talked about it."
- CL 09-26 08:18: "no real ticks more like overlap of spacetime occupation which is quite boolean like"
- CL 09-27 09:08: "you don't advance a ship tick by tick you just map where it wants to go"
- CL 09-25 12:10: "not exactly, it is a tube in spacetime."
- OC#46: "calculate and then recalculate if there's a causal interaction"
- Proposed: *No global or per-body tick: a body is a tube in spacetime, and work happens only where tubes or certificates meet.*

**9. Rough first; refine only when a certificate could break.**
- CX 09-14 09:37: "we need refining because it might break the certificate as we are uncertain? simple and powerful."
- OC#36: "\"if … refine\" is how we should work huge savings."
- CL 09-27 09:08: "do we have to be perfect right away? No, as long as the end result is good the method doesn't matter."
- CX 09-14 09:17: "maybe even we can be rough and then increase resolution with passes"
- Proposed: *Compute roughly first and refine only when a certificate could fail. The method is free as long as the canonical result is right.* This fits `docs/universe-quanta.md`: computation adapts, the state grid does not.

**10. The simulation says what happens next; heuristics only schedule.**
- OC#36: "the simulation tells us what's next not us, subtle but deadly."
- OC#34: "you're too much thinking in terms of local vs global which is not the move"
- OC#50: "i kept saying that for a reason", on "near/far is not the fundamental distinction"
- OC#36: "not rely on predictions much is my call", then "by prediction i mean heuristics rather than simulations"
- CX 09-11 21:47: "fermi is there to spot issues early not an oracle"
- Proposed: *The simulation decides what happens; heuristics, forecasts and Fermi estimates only choose what to compute first. Near/far and local/global are not the distinctions that matter.*

**11. Nothing goes past c.**
- CL 09-25 16:44: "beyond c=1 means paradoxes"
- CL 09-26 08:18: "yes because as far as we know nothing can in physics."
- OC#16: "i don't want FTL because of paradoxes"
- OC#34: "FTL would destroyed a tremendous amount of things."
- OCC#10: "it allows to cheaply partition compute, even gravity is light speed"
- Proposed: *Nothing moves, signals or is pushed past c, gravity included. Causality is what makes the engine cheap, so it is never traded away.*

**12. The player is bounded (strengthens principle 5).**
- CL 09-27 10:20: "his direct influence is bounded and propagates at c at most (or more like propagates along the predictions' paths in spacetime)"
- CL 09-27 09:25: "a player won't easily change the orbit of a planet"
- Proposed amendment: *…their influence is bounded by what they can physically do, and it spreads at most at c along the predicted paths.*

**13. Time multiplies small influences (strengthens principle 6).**
- CL 09-27 09:08: "its time that's a multiplier here and not the space bending of its mass"
- CL 09-27 09:25: "they have a lot of mass cumulated they can't just be dismissed like that."
- CL 09-25 12:10: "what if one ship influences the path of an asteroid over time?"
- Proposed amendment: *…a ship beside an asteroid for years must be able to move it.*

**14. The memory floor is information, not count × bytes.**
- CL 09-28 09:48: "this is nowhere near the floor on the size and information theory says so"
- OC#34: "why do you need so many bytes per entity?"
- CX 09-11: "i believe that's there's meaningful overlap so meaningful compression possible"
- Gap: this is a HANDOFF standing decision but not a principle.

**15. Laws are local and must scale to the whole universe.** He said this as questions.
- CL 09-29 08:05: "is it local laws or not? can laws expand to the whole universe?" and "does it scale well for billions of celestial bodies and ships?"
- CL 09-27 09:08: "\"a million ships\" a billion*"
- Proposed: *Every law is local and extends to the whole universe; its cost is shown against N up to billions before it is trusted.*

**16. No sunk cost; avoid ruin; ask better questions.** AGENTS.md has guards against sunk cost, but PRINCIPLES.md, which specialists read, has none.
- CX 09-14 09:17: "if it's good, good, if it's bad it goes away and we learn a lesson from it"
- CL 09-28 12:43: "not making mistakes matters more than doing things efficiently, don't multiply by zero."
- CX 09-14 17:13: "what are the 'zeros' in the multiplicative system that cause total simulation collapse?"
- CL 09-28 11:37: "just like RTS games early gains are huge it's the same here better questions matter."

**17. Steal what works, from people with skin in the game.**
- OC#16: "i need to steal from what works as much as possible"
- OC#34: "we need to learn from the geniuses of the class and the cautionary tales too"
- CL 09-27 09:08: "those guy with simulations don't have much skin in the game for compute and time constraints unlike quant traders"
- CL 09-29 08:24: "This is a solved problem elsewhere for sure"

**18. Measure the goal, never a proxy.**
- CL 09-28 14:51: "it is a bad proxy", about the Readwise word limit
- CL 09-28 10:04: "no don't think like that, what is needed is needed", about a line-count target
- CL 09-27 10:20: "i just care at about how fast it runs compared to real time" and "which will limit effective c in game."

**19. The view is an instrument.**
- OC#38: "real vs displayed is not the same thing"
- CL 09-26 08:18: "modern games are sloppy on purpose to then use algos on top of it for displaying"
- DC: "your dials are made up and hold no informations so you'll need to fix them"
- Proposed: *The view may interpolate, enlarge and symbolise, but every mark carries information, and the world never bends to the view.*

**20. Additions to the goal.** The current goal is engine-only.
- OC#16: "so what really matters is navigation, knowledge and dynamics those need to be perfect, graphics don't matter"
- OC#4: "history being made and learning from it through space and time while you are influencing it yourself"
- OC#4: "a game that cannot loose by construction if done right"
- OC#16: "you are hardin making psycho-history"
- CL 09-27 09:08: "I want the player to feel what a human would feel in space, it's about immersion"
- CL 09-26 08:18: "we need to build towards GR that's the goal that we should not loose track of, the rest are stepping stones"
- CL 09-25 11:58: "i still want to ship one day but don't want taxes of bad implementation, i want my 1B ships"
- ABP: "one billion individually addressable ships and histories spanning ten billion simulated years"

**21. The logs hold the philosophy; keep contradictions; check incentives.**
- CL 09-29 08:05: "Are you still following the philsophy of the conversation logs, yes they are old now but the philosophy is here"
- CL 09-28 14:34: "the things that are contradictory should be separated but not necessarily deleted, anything that serves the goal"
- CL 09-28 14:49: "if it read about incentives it should look at its own incentives and the ones it created"

**22. Iteration: extremes and how things break (strengthens principle 10).**
- CL 09-25 12:51: "extremes inform the mean"
- CL 09-27 09:08: "We need also to map how things break, think in extremes"
- CL 09-28 14:34: "we ought not to underestimate iteration speed that's a common theme amongst the best people for a reason"

---

## 2. Missing register entries

### Engine and compute

| Julien's words | Source | Status |
|---|---|---|
| "broken record moment again, but… hypergraphs?" / "can we learn things from wolfram's hypergraphs?" | OCC#12; CL 09-26 09:17 | **Drifted.** A hyperedge IR existed in the old line (HISTORY H0016, ~line 695), was archived at H0182, and is mentioned in no current doc. This is a second "broken record" request, like multipoles. |
| "\"because it's much simpler\" NO never do that please never dumb down for no reason" | OC#34 | **Drifted.** He said this about the AI choosing Barnes–Hut over FMM. Principle 1 keeps the slogan but loses that context, and FMM was never built (H0196). |
| "true but we're at big scales", on asymptotics not guaranteeing speed | OC#34 | **Drifted** (same cause). |
| "then do it" / "sure do this" (tropical/min-plus); "what if we were to push the min-plus idea to the extreme not just on one thing?" | OC#38; OC#42 | **Drifted silently.** The approved plan says "Use min-plus for admissible arrival-time composition". There is one journal mention and nothing in the docs or code. |
| "KDS is interesting." | OC#40 | Followed in spirit: engine.md certificates. |
| "I would actually make caching part of the mathematics" yes huge / "cache the behavior of a region, not the particles inside it." nice / "good dig" (criticality, dependency graphs, tau-leaping, response operators) | OC#44; OC#46 | **Partly followed.** engine.md has certificates and dependencies. Region response operators and eliminating block interiors are absent; the old line's "regional responses" were archived. |
| "interesting for the ships too can't we do that and switch if collision? cheaper?" (phase-space packets); "how we managed to make 1B ships take basically no space (which we can improve even more)" | OC#48; CL 09-27 09:08 | **Drifted.** Families lived in `crates/engine`, archived at H0182, and no plan step rebuilds them. |
| "quotienting out irrelevant time" very true and important | OC#48 | Followed as principle 3, but the gravity-law v1 step boundaries break it. |
| "oh YES, dig dip on this" (2D mathematical gifts) | OC#50 | **Never pursued.** |
| "the light cone grows continuously meaning that there will always be a point where we cannot handle the universe anymore" | OC#50 | **Open.** Not among HANDOFF's risks. |
| "maybe we just need to draw a lightcone for each object"; "natural compartmentalization for gpu usage" | OCC#10 | Followed in design (engine.md rules 4–5). The GPU half is not. |
| "maybe we can afford in some regions to lag behind?"; "we can even have regions that are delayed if not on screen" | OCC#8; CL 09-25 14:28 | Followed (engine.md rule 8). |
| "Use idle time to compute ahead" yes this is a whole important idea of this project | CL 09-25 14:28 | Designed, not built. |
| "how can we push further the idea of compiler rather than simulation?"; "we need to make computation easier and amortize the one that has already been done" | OCC#14; CX 09-12 11:51 | Followed in design (certified generators). |
| "As the precomputation scheduler" — "interesting i like it"; "does MCTS help us?" | OC#38; CL 09-25 15:34 | Followed as speculation ranked by value × probability. MCTS itself was not chosen. |
| Neural Engine speculation; "we need to leverage AMX too"; "think around this issue, we can be smart about it." | CL 09-25 15:48, 15:58, 16:03 | Designed in engine.md; the machine probes are pending. |
| "since it is deterministic we could have human readable codes"; "a checksum word is a good idea"; "go first principle and information theory style." | CL 09-25 15:48, 15:58, 16:03 | Designed (engine.md share codes); not built. |
| "the algorithm that allocates the work… it's the most important one" | CL 09-25 14:28 | **Demoted.** It is step 7 of 10 in HANDOFF; H0186 called it "a premature scheduler". |
| "we could repurpose entropy equations…"; "you did not talked about the entropy for knowing where to compute you will do this right?" | CL 09-27 10:20; CL 09-28 09:48 | Designed; deferred to step 7. |
| "it's really just the same as the rest, the only difference is that the frequency of surprises is higher" | CL 09-27 10:20 | Followed (engine.md rule 9). |
| "we need to monitor resource allocation" | CL 09-25 14:06 | Partly. The report list in `docs/test-ladder.md` omits utilisation and the real-time factor. |
| "well that's stupid" (the 100,000-ship cap); "\"Impulses ignore mass.\" that's not desirable" | CL 09-25 14:06 | Followed (H0161). |
| "some will be as fast as the player i suppose" | CL 09-26 08:45 | Followed by the law, which caps nothing below c. |
| "one thing i'd like to exploit for the future is debris, maybe i'll go voxel like so keep that in mind" | CL 09-26 08:18 | **Unaddressed.** |
| "communication in more inverse square law like" | CL 09-26 08:18 | **Unaddressed.** |
| "we need to leverage better for collisions that ships are small" | CL 09-26 08:45 | Unknown. |
| "rust and metal are best I believe"; "metal." | OC#32; CL 09-25 15:21 | Followed. |

### Gravity and physics

| Julien's words | Source | Status |
|---|---|---|
| "weak gravity is derived from the strong one i believe" | CL 09-25 11:58 | Followed by v1 (one flow law, GR oracle). |
| "gravity is intrinsic to this spacetime compiler so we should act like it" | CX 09-12 11:51 | Followed from H0195. |
| "i don't think we need newtonian gravity but rather an aprox of gr" | OC#34 | Followed (v1). |
| "for newtonian you would need definitions and thresholds and co which i'm unsure is best"; "what's hard is going up the chain not down" | OC#36 | Followed: no regime thresholds, GR as the oracle. |
| "\"light that bends\" is an emergent property of the shape of the space" | CL 09-27 09:08 | Followed. |
| "I want black holes… but i don't care yet about past the event horizon" | CL 09-27 09:08 | Followed (B6: absorption, nothing evaluated inside). |
| Two black holes: "that's nice gameplay no?" | CL 09-25 11:58 | Planned (step 9). |
| "what if one ship influences the path of an asteroid over time?" | CL 09-25 12:10 | Planned (a chaotic rung in test-ladder). |
| "instead of projecting gravity onto space why not look at the relations between the celestial bodies" | CX 09-14 09:55 | Tried as `es-relational-hierarchy-v0` in the old line, then archived. |
| "that's important work on that", on composing trajectories through a given geometry | CX 09-14 09:55 | Followed from H0195. |
| "gravity is light speed… but also it decays fast" | CX 09-14 09:37 | Planned (step 5, retarded moments). |
| "planet more influence than ship means that you can be corse and refine easily" | CX 09-14 09:17 | Planned (cell hierarchy). |
| "can't we \"giggle\"?" (iterate a rough estimate) | CL 09-27 09:08 | **Not reflected;** v1 is single-pass stepping. |
| "mass is just a coefficient on how much you bend space i guess and on inertia too"; "if special relativity holds, gr is just sitting on top as a multiplier" | CL 09-27 09:08 | Followed: β = 0 gives back the SR lattice. |
| "In tests we also need to see how galaxies and solar systems behave, maybe looking at 3 body problem too"; "But also how light behaves at speeds" | CX 09-14 09:17 | Planned (physics ladders; B4). |
| "it's the actualization of moving objects that's problematic"; "we only care about changes" | CL 09-29 08:24 | Addressed by the HANDOFF proposal; **partly undone** by v1's per-body steps. |
| "fair point", on starting from exact GR solutions | CL 09-28 09:48 | **Superseded:** 1,600× over budget (H0194); "oracle ≠ implementation" (H0195). |
| "wow why?", on Kerr and inspiral being cheap | CL 09-28 09:48 | Never explained to him. |

### Numbers and time

| Julien's words | Source | Status |
|---|---|---|
| "it's simultaneity tolerance of the universe"; "i want a 5% error on resolution for a collision"; "so chronon is just the floor more than the ruler" | CL 09-26 09:31 | Followed (`docs/universe-quanta.md`, δt ≈ 83 ps). |
| "basically the 24fps of cinema (or 12?)"; "the smallest unit is a ship in our world" | CL 09-26 08:45 | Superseded the same day by the missile definition. |
| "do we even need floors?" | CL 09-26 17:32 | **Answered with evidence:** one floor is needed (H0173; universe-quanta). |
| "if its close to me then i care about the precision" | CL 09-26 09:31 | **Disproven:** refinement "could never depend on observation or scheduling" (universe-quanta; AGENTS.md). |
| "what if simply we fix them to fp32 or something like that? simple." | OC#40 | **Disproven:** floats never decide outcomes; they are filters only. |
| "one thing to be careful about like with wolfram's idea is the order of operations because we're quantitized" | OC#38 | Followed (independent of schedule). |
| "ooooh", on JANUS bit-wise reversibility; "smart", on q_k = 2^k q_0 | OC#42 | **Not adopted.** No reversibility and no effective-quanta hierarchy. |
| "could we use quaternions" | CL 09-26 20:00 | Unanswered in any doc. |

### Testing, team and process

| Julien's words | Source | Status |
|---|---|---|
| "if you're actually testing behavior or the bad idea of expecting the same data" | CX 09-23 11:07 | **Drifted:** the many-seed rule was lost. |
| "So our tests shall be more qualitative then quantitative I just have to look at them" | CX 09-14 09:17 | Partly: nothing before the step-4 viewer. |
| "the tests should've been clear from the start and the subdivision of the components too" | CX 09-14 09:17 | Followed (frozen gates, owners). |
| "how does it compare to the competition" | CL 09-27 09:39; OCC#0 | **Unaddressed.** |
| "i'm strafing away from success"; "got lost in details or something like that, no good unificaiton" | CX 09-12 21:15, 21:19 | **Ignored for 17 days,** until H0195–H0197. |
| "the doc should be clear on what's the goal i think that may have been the issue" | CX 09-12 21:26 | Followed on 29 September (PRINCIPLES). |
| "as we're converging towards something tighter i'd expect the need to use more bigger models in proportions" | CL 09-28 18:56 | Not in AGENTS. |
| "It's a wildcard that we're underestimating." (GLM) | CL 09-28 13:23 | Only partly reflected: the register's "without authority" and AGENTS' "volume without authority" are narrower than his words. |
| "maybe even a sub-agent that asks questions and read readwise…"; "we need a polymath like researcher…" | CL 09-28 11:37, 11:45 | Narrowed to "before one-way doors only" (AGENTS line 25); H0191 records his approval of the lean form. |
| "take a guess at how much usage we used with glm so far and then look at it" | CL 09-28 14:54 | Possibly the source of "Julien predicts before each run". |
| "remove the word limit for the readwise search… it is a bad proxy" | CL 09-28 14:51 | Unknown. |
| "i'm not sure how to interpret the numbers you gave me"; "explain me where we are simply" | CL 09-26 07:55; 09-29 07:56 | Partly (the real-time factor rule). |

### Game, world and interface (none are in any living doc, apart from AGENTS' aesthetic line)

- "a game that cannot loose by construction if done right" (OC#4)
- "emergent such that there's never a sole winner or if so factions can emerge, embracing the chaos" (OC#16)
- "flag like in real to know who belong to who but with a reputation system" (OC#16)
- "the more it is transmitted the looser it is" (OC#16)
- "we need a map, but a map that is inferred based on intelligence for the territories"; "Last confirmed information: Alpha, 20 years ago." (OC#16)
- "the historical map is the unchanged map which is very different form the actual map"; "also a planet can obscure another" (OC#34)
- Missions from fast-forwarding: "oh i could fast pace the game such that I know what happens without intervention so that I can create the missions" (OC#16)
- "it needs to be rewarding at multiple time scales"; "i just don't want the rock paper scissors" (OC#16)
- "the zoom level is the minimap" (OC#30)
- "the world should be able to be HUGE, basically infinite but life shall spawn not everywhere" (OC#30). Universe-quanta sizes the world to a galaxy (10^21 m), which was never put to him.
- "gravity, spacetime, light spectrum, factions, resources, money/market, relations" (OC#28). Light spectrum is absent.
- "the camera is on another plane than the character" (OC#16)
- "I need a good visualization to see what's happening with god's view" (OC#16). The approved plan had a diagnostic view; today only a float viewer is planned.
- "I don't see the sub-luminic travel I want to see that don't loose the soul" (OC#20)
- "it needs to be unbelievably fast like dwarf fortress" (OC#16)
- From DC: "it's a space clock literally"; "use those indicator rings to display things like proper time vs ship time"; "oh different patina that's it, perfect"; "not steampunk is NOT the goal"; "i want more of the sinbad aspect"; "the transitions between the scales should be seamless"; "use real materials, don't make it overly saturated and contrasted"; "you really move just in a plane but you have depth to anchor it".

### Approved build plan (AI words he approved around 11 September)

- "bounded FMM as the primary acceleration candidate": **drifted** (H0196).
- "All mass participates, including ship populations": pending (v1 step 5).
- "Use min-plus for admissible arrival-time composition": **drifted silently**.
- "spatial quadtree crossed with an independently refined dyadic time tree": replaced by density-sized cells (H0177). There is no record of his approval.
- "Randomness is keyed by stable semantic identity, event, seed, and purpose": in no current spec.
- "at most 4 GiB", "at least 30 FPS at 1080p", "within one hour from cold start", "at most 20 GiB": **silently dropped** from the living docs. The last mention is in the old line, around H0146. The 20 GiB budget exceeds the roughly 10 GB of free disk HANDOFF reports.
- "Camera operations never alter canonical history" and "camera distance… do not determine fidelity": followed (AGENTS.md).

---

## 3. Contradictions in his own statements (both sides kept, not resolved)

| Topic | Earlier | Later |
|---|---|---|
| Ships as gravity sources | OC#34 (before 11 Sept): "ships can be not taken into account for gravity of celestial bodies or even between themselves tbh"; OC#38: "planets influence ships but not the opposite?" | OC#40: "yeah let's do that to allow emergence"; OC#44: "yeah i missed that important part"; CL 09-27 09:25: "they have a lot of mass cumulated they can't just be dismissed like that." |
| Strong gravity | CL 09-25 12:10: "so i guess we can omit it for now then"; 11:58: "maybe i should drop the two black holes idea" | CX 09-14: "Black holes are also important tests"; CL 09-27: "I want black holes because they create very interesting gameplay" |
| Ticks | OCC#8: "don't think in terms of Hz we've already talked about it." | CL 09-26 08:18: "do we need to run at 60hz while maybe 12Hz interpolated would work?"; 08:45: "basically the 24fps of cinema (or 12?)" |
| What the chronon is | CL 09-26 08:45: "the smallest unit is a ship in our world" | 09:31: "i want a 5% error on resolution for a collision"; "the floor more than the ruler"; 17:32: "do we even need floors?" |
| Precision and proximity | OC#34: "there's no things as far away"; OC#50: "i kept saying that for a reason" (near/far) | OCC#8: "but also the ones the player looks at or closer to the player?"; CL 09-26 09:31: "if its close to me then i care about the precision" |
| How influence decays | OC#36: "that's a series that converges i bet" | OC#44: "yeah i missed that important part, yikes i even thought of it" |
| Floats | OC#34: "divergence is not a joke and it compounds" | OC#40: "what if simply we fix them to fp32 or something like that? simple." |
| Forecasts | OC#36: "not rely on predictions much is my call" | CL 09-25 15:34: "i think we need some messy calculations to have a better idea of where to spent compute"; 09-27: "It's basically entropy calculation that we need for prediction on where things will get messy" |
| Gravity path | OC#34: "i don't think we need newtonian gravity but rather an aprox of gr"; CL 09-28 09:48: "fair point" (exact GR first) | CL 09-29 08:24: "you've confused a bit oracle and implementation" |
| When to optimise | CX 09-14: "optimization is paramount from the start" | CX 09-23: "we'll be able to improve upon the reference in terms of computation based on what will be measured"; CL 09-28: "don't start implementation yet" |
| How to test | CX 09-13: "i want a numbers to leave the numbers approach I think, not sure" (ambiguous); CX 09-14: "So our tests shall be more qualitative then quantitative…" | CL 09-28 11:37: "make sure to measure before making solid claims" |
| Parallel work | RM (~11 Sept): "don't use too many sub-agents my tokens are screaming"; CL 09-25 16:18: "implement in parallel as much as possible the build"; 21:35: "i just wanted less workers added" | CL 09-28 11:37: "the goal is to use the usage limits so that work is done"; 12:10: "not doing too much parallel work because the real issue is caching…" |
| GPU | ABP (~11 Sept): "enable a GPU path only when matched full-pipeline measurements show a benefit" | CL 09-25: "gpu should heavily be used for anything i believe" |
| Test length | ABP: the billion-ship scenario "within one hour from cold start" | CL 09-26: "remember 1min max per test" |
| MVP | OC#16: "for the mvp let's keep it realistic" | OC#34: "ok stop thinking of MVP this is polluting your thinking" |
| Graphics | OC#16: "graphics don't matter" | OC#10: "i'll need something more polished though"; DC: "the materials don't feel like i can touch them" |
| Minimap | OC#16: "there's a minimap but first let's discuss it" | OC#30: "i don't believe that we need a minimap" |
| 2D or 3D | OC#14: "actually it could be a fake 3D maybe?" | OC#28: "i'd want to make it 2D…"; DC: "…you have depth to anchor it" |
| Causal complexity | OCC#4: "It's fairly similar to boids, just more rules but they are simple no?" | OCC#6: "coordination as a result gets slower it's like a game where everything is happening all at once" |
| FTL | OC#16: "i don't want FTL because of paradoxes" | same note: "if i had more time i could play with the paradoxes of ftl" |
| Confidence in multipoles | OC#34: "i'm really a broken record" | OC#34: "maybe when i say multi-pole quadtree is better I don't know"; CL 09-29: "i was led to believe that FMM was a bad move" |
| GR versus game (a tension) | CL 09-25: "we need not to forget that it's a game" | CL 09-26: "we need to build towards GR that's the goal…" |

---

## 4. Where today's plan and rules go against what he said

1. **HANDOFF lines 3, 25–27 and 34, and CARD.md line 8, still head for re-climbing G2 on the exact evaluator.** The next steps are the diagnosis, Astra's weak-field fast path, and "re-climb until step 2 passes". The HANDOFF is still stamped "(H0194)", and line 34 still says "awaiting his go", although H0195 records the go. Further stale lines:
   - Line 69 still names G2.1–G2.5 as the contract.
   - Line 75 still frames step 5 as parent formulas and handoffs (post-mortem framing 3).
   - Line 76 adds `es-lattice-gravity-v0`, which is retired.
   - The Risks list still leads with "exact integer elliptic-function algorithm".
   - This goes against "you've confused a bit oracle and implementation" and "we should not keep for the work out of sunk cost fallacy".

2. **gravity-law.md lines 36–41 bring back per-body ticks.** A step lasts "a fraction η of the local dynamical time", and "a body's own step boundary" counts as an event. B9 allows 512 events per orbit.
   - This goes against "you don't advance a ship tick by tick", "don't think in terms of Hz", "we only care about changes", and the proposal he approved (HANDOFF lines 36–39): a body pays only at crossings, certificate expiry, contacts and commands.

3. **B9 (line 79) is sized to "0.1 core for a million ships in low orbit".** A billion ships at that rate is about 100 cores, so the gate can pass while the goal fails by 100×. He corrected exactly this framing: "\"a million ships\" a billion*". There is no cost-versus-N gate yet; the in-flight row plans one.

4. **Multipoles are still only "Later steps (direction, not frozen)"** (gravity-law lines 88–98), placed after the player slice (HANDOFF lines 74–75). The in-flight row says to add them "from day one", but the contract does not have them yet. PRINCIPLES' register marks them "Followed", which overstates it.

5. **HANDOFF line 76, "Metal only for dense contacts; canonical formulas on the CPU",** and B9's CPU-only cost measure go against "gpu should heavily be used for anything i believe" and "spacetime is fundamentally the most gpu thing".

6. **The v1 ranges and some gates lean on value precision** (medium). Line 51 uses arbitrary-width integers up to 2^96. B7 asks for 10^-9 on clocks and B1 for 10^-6 excursion; both are error-size gates. This goes against "no it's about what's cheapest to compute" and "we don't care about values but about behaviors". The ranges may still be justified by galaxy scale.

7. **engine.md lines 40 and 107 still keep five modes bit-identical,** and HANDOFF line 76 delays the merge to step 6, although H0186 planned it before step 4. This goes against "yes, why not one?" and "We need unification between the engines… i hate bloat".

8. **Generator-native populations were archived at H0182, and no plan step brings them back.** This goes against "how we managed to make 1B ships take basically no space (which we can improve even more)" and principle 6.

9. **The allocator is at step 7 of 10,** against his "it's the most important one".

10. **AGENTS.md line 56, "Read them selectively; later steering governs",** is exactly the rule that let later steering override the philosophy. This goes against "the philosophy is here". Separately, the continuation conversation (per-object light cones, lagging regions, hypergraphs, compiler) is not in `docs/reference/`. It exists only at `/Users/julien_laurent/Research/emergent-space/artifacts/evidence/recovered-20260926/docs/reference/original-conversation-continued.md`.

11. **AGENTS.md line 56 gives the aesthetic as "ink, watercolor, ivory, pale blue".** He asked for Sinbad colours and moody lighting ("i want more of the sinbad aspect"), and the word "watercolor" appears nowhere in his words. The references README itself says those images were "foundations, not the final look".

12. **PRINCIPLES' register overstates three items as "Followed":** multipoles (not in any frozen contract), behaviour-first (HANDOFF and CARD still pursue exact G2), and one engine (engine.md still has five modes). Two wordings are not his: the register's "without authority" for GLM, and principle 11's "build messy" where he said "messy-ish".

13. **No current rule requires many-seed testing,** in gravity-law.md or test-ladder.md. He asked whether tests measure "behavior or the bad idea of expecting the same data".

14. **The approved plan's budgets (4 GiB, 30 FPS, the one-hour run, 20 GiB) were dropped without being followed or disproven.** PRINCIPLES says silence is never disproof.

15. **PRINCIPLES 7 says multipoles serve "causality regions alike",** but engine.md has no mechanism for it.

---

## 5. Unendorsed ideas (AI suggestions often treated as his)

- "Approximate state; certify branches" (the OC reply after #36). He never answered it.
- "precision is adaptive too". He pasted it only as an "ai answer" to his question "do we even need floors?"; universe-quanta later adopted the opposite after his "proceed".
- "bound where influence can exist geometrically; don't assume how large its consequences are". He did not reply to it directly.
- "Keep a stupid reference interpreter". The chronon judge embodies it, but he never explicitly endorsed it.
- "The light cone is allowed to grow forever. The amount of unresolved information inside it is not." He did not reply.
- A de Sitter horizon to cap the light cone. The approved plan later rejects cutoffs.
- "disappointingly simple first engine" and Hz tiers for battles. He pushed back on both.
- Design-bible §103 ("engine before agents is the biggest risk"). This is an AI summary he pasted as context.
- The julien-context skill text inside CL 09-25 11:43. It is a skill file, not his chat.