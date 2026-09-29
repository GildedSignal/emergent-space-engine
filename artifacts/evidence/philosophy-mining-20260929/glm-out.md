Working...
All corpora and current docs read. One note before the findings: `docs/reference/original-conversation-continued.md` does not exist in the repo (`docs/reference/` holds only `original-conversation.md`, `original-research-report.md`, `approved-build-plan.md`); its Julien turns survive only as the `[original-conversation-continue #N]` entries extracted in `julien-turns-original.md`, without the AI replies. Endorsements from that thread are therefore harder to confirm; flagged where relevant.

---

# 1. Missing principles and philosophical facts (ranked by importance to the goal)

**1. The player lives inside the causal universe — no god view, no omniscient present; knowledge has latency.**
- "we need a map, but a map that is inferred based on intelligence for the territories" — [original-conversation.md #16]
- "i don't believe that we need a minimap basically the zoom level is the minimap" (…sensor limitations) — [original-conversation.md #30]
- "I want the player to feel what a human would feel in space, it's about immersion" — [2026-09-27T09:08 claude]
- Proposed principle: *The player is one embedded observer: they see only what physically reached them, and their map is a model, never the universe.*
- PRINCIPLES' goal has "feel what living at high c would feel like" but the epistemic rule (stale/inferred knowledge, sensor-limited zoom, "Last confirmed information: Alpha, 20 years ago" [#16]) is absent, though it drives engine, gates and UI.

**2. The universe makes its own history; the game cannot be lost by construction.**
- "it's really about a game that cannot loose by construction if done right" — [original-conversation.md #4]
- "emergent such that there's never a sole winner or if so factions can emerge, embracing the chaos" — [original-conversation.md #16]
- "history being made and learning from it through space and time while you are influencing it yourself" — [original-conversation.md #4]
- Proposed principle: *Dominance breeds its own counters; the simulation never converges to an endgame, and history is the product.*

**3. Ask the right question before computing anything.** His most-repeated method statement, absent from PRINCIPLES.
- "hence why i'm such a pain with finding the right question to ask" — [original-conversation.md #42]
- "i think we're making it harder than we should because we're not asking the right question" — [original-conversation.md #48]
- "Your goal is not to answer the questions but to ask the right questions" — [2026-09-14T17:13 codex]
- "what do we want vs what do we get is the right question" — [original-conversation.md #36]
- Proposed principle: *Finding the right question is half the solution; question the framing before working inside it.*

**4. Priority order: navigation, knowledge, dynamics perfect — graphics don't matter.**
- "what really matters is navigation, knowledge and dynamics those need to be perfect, graphics don't matter" — [original-conversation.md #16]
- Proposed principle: *Polish what the game is (navigation, knowledge, dynamics); graphics serve legibility only.* (Contradicts-in-tension with his later aesthetic investment; see §3.)

**5. Steal from what works, prefer fields with skin in the game.**
- "i need to steal from what works as much as possible" — [original-conversation.md #16]
- "those guy with simulations don't have much skin in the game for compute... unlike quant traders" — [2026-09-27T09:08 claude]
- "we need to learn from the geniuses of the class and the cautionary tales too" — [original-conversation.md #34]
- Proposed principle: *Import solutions from fields that pay for compute with their survival, not just from game dev.* (engine.md's "fields to borrow" list implements this without crediting the principle.)

**6. Compute ahead; speculation stays deterministic — "a whole important idea of this project."**
- "'Use idle time to compute ahead' yes this is a whole important idea of this project" — [2026-09-25T14:28 claude]
- "using the AI cores for speculation, it would be unused compute anyway and via speculation it still stays deterministic" — [2026-09-25T15:48 claude]
- Proposed principle: *Spare silicon buys slack ahead of the player; discarded speculation is free and never changes results.* (In engine.md rules 7/10, not in PRINCIPLES.)

**7. Rough first, refine later — the end result matters, not intermediate perfection.**
- "can't we 'giggle'? like do we have to be perfect right away? No, as long as the end result is good the method doesn't matter" — [2026-09-27T09:08 claude]
- "we could be rough and then increase resolution with passes" — [2026-09-14T09:17 codex]
- Proposed principle: *Approximate eagerly, refine only where the outcome could change.*

**8. The simulation tells us what's next — no heuristic stands in for it.**
- "the simulation tells us what's next not us, subtle but deadly" — [original-conversation.md #36]
- "the cautionary tale is to not rely on predictions much is my call, unless i'm wrong well inside the lightcone" — [original-conversation.md #36]
- Proposed principle: *Forecasts schedule compute; only the simulation decides outcomes.* (engine.md rule 6 says this; PRINCIPLES principle 5 implies it only.)

**9. Test behaviour, not the same data; change seeds when the law changes.**
- "all I'm wondering is if you're actually testing behavior or the bad idea of expecting the same data" — [2026-09-23T11:07 codex]
- "a planet orbit a star... because it happened to work like that not because the laws were made for it" — [2026-09-14T09:17 codex]
- Proposed principle: *Gates judge behaviour distributions across seeds, never bit-identity with old data.* (gravity-law.md follows this; PRINCIPLES never states it.)

**10. The chronon is a perceptual floor and a simultaneity tolerance, "the floor more than the ruler."**
- "the smallest unit that doesn't feel like it creates saccades is our goal in space and time" — [2026-09-26T08:45 claude]
- "so a chronon is an event differentiator... it's simultaneity tolerance of the universe" — [2026-09-26T09:31 claude]
- "chronon is just the floor more than the ruler" — [2026-09-26T09:31 claude]
- Proposed fact: the quantum is grounded in perception (24 fps of cinema), not physics; precision is spent only where it distinguishes outcomes.

**11. The player is bounded.**
- "he is the only non deterministic part but he is bounded" — [2026-09-25T15:48 claude]
- Proposed strengthening of principle 5: the wildcard's influence is bounded by thrusters, human action rate, and c.

**12. Concrete wants that anchor the goal.**
- "i still want to ship one day but don't want taxes of bad implementation, i want my 1B ships" — [2026-09-25T11:58 claude]
- "I want it to be believable at all scales" — [2026-09-25T12:10 claude]
- "what if one ship influences the path of an asteroid over time?" — [2026-09-25T12:10 claude]
- "I want black holes because they create very interesting gameplay but i don't care yet about past the event horizon" — [2026-09-27T09:08 claude]

**13. Interface philosophy: an instrument, never a dashboard; ornament must inform.**
- "as if it were a celestial clock... it connects everything, it's a space clock literally" — [2026-09-25T11:43 claude, pasted You-turn]
- "your dials are made up and hold no informations so you'll need to fix them" — [2026-09-25T11:43 claude, pasted You-turn]
- "oh different patina that's it, perfect" (observed vs inferred) — same turn
- "the transitions between the scales should be seamless, because basically that system view is the view" — same thread (Westworld turn)
- Proposed principle: *Every displayed element answers a question; material state encodes epistemic state.*

**14. Don't think in Hz; motion is spacetime-tube overlap, not ticks.**
- "don't think in terms of Hz we've already talked about it" — [original-conversation-continue #8]
- "there's no real ticks more like overlap of spacetime occupation which is quite boolean like" — [2026-09-26T08:18 claude]

**15. Anti-bandaid, anti-bloat; mistakes cost more than inefficiency.**
- "I'm very wary of mixing too much systems for no reasons i don't like bandaids" — [2026-09-25T11:58 claude]
- "that doesn't feel like a smart fix and more like a bandaid, it works in just one case" — [2026-09-25T14:28 claude]
- "red-teaming because not making mistakes matters more than doing things efficiently, don't multiply by zero" — [2026-09-28T12:43 claude]
- "we ought not to underestimate iteration speed that's a common theme amongst the best people" — [2026-09-28T14:34 claude]

**Secondary facts worth recording:** "we're lucky space is empty so things can be easily approximated" [#32]; "basically we're trying to not be Minecraft with that poor optimization" [#32]; "it needs to be unbelievably fast like dwarf fortress simple as that" [#16]; "99.9% of what's happening could be simplified instead of recalculated" [2026-09-14T09:17 codex]; reputation is local ("flag like in real... but with a reputation system" [#16]); information decays in transmission (telephone-game idea [#16]); "the world should be able to be HUGE, basically infinite but life shall spawn not everywhere" [#30]; "gravity is light speed and that's a good help for us but also it decays fast" [2026-09-14T09:37 codex]; the light-cone partition unlock: "we just need to draw a lightcone for each object... even gravity is light speed" [continue #10]; "gravity is intrinsic to this spacetime compiler so we should act like it" [2026-09-12T11:51 codex]; endorsed AI formulations he adopted: "compile gravity into geometry once, then let ships traverse that geometry cheaply" ("yes", [#40]); "store high-entropy information; recompute low-entropy information" ("yes", [#42]); "composing trajectories through a given geometry is easier than compiling mutually interacting sources" ("that's important work on that", [2026-09-14T09:55 codex]); the open problem he named himself: "the light cone grows continuously meaning that there will always be a point where we cannot handle the universe anymore" [#50].

---

# 2. Missing register entries

| Statement (his words) | Source | Status |
|---|---|---|
| "beyond c=1 means paradoxes so relativistic collision rule seems the way to go"; "as far as we know nothing can in physics" | [2026-09-25T16:44], [2026-09-26T08:18 claude] | **Followed**: lattice speed limit, relativistic contacts in `es-lattice-relativistic-v1` (HANDOFF); gravity-law `\|u\| < Q` |
| "i don't want FTL because of paradoxes" | [original-conversation.md #16] | **Followed**: c-limit throughout engine.md; no FTL path exists |
| "we want to be lazy in a smart way, it's a game not a physics simulation" | [2026-09-25T12:10 claude] | **Followed**: engine.md "only surprises"; gravity-law "Only changes cost" |
| "the goal is simply to have the right behaviors and simplify how we test for them with litmus tests" | [2026-09-14T09:17 codex] | **Followed**: gravity-law gates B1–B9 are behaviour litmus tests |
| "all I'm wondering is if you're actually testing behavior or the bad idea of expecting the same data" | [2026-09-23T11:07 codex] | **Followed**: gravity-law "never bitwise continuum floors"; gr-oracle kept failing (exit 1) |
| "So our tests shall be more qualitative then quantitative I just have to look at them and know what to look for" | [2026-09-14T09:17 codex] | **Drifted**: gates are quantitative tolerance bands (1%, 10⁻⁶); defensible, but the preference is unrecorded |
| "fermi is there to spot issues early not an oracle like we've just exemplified" | [2026-09-11T21:47 codex] | **Followed**: HANDOFF marks the 10–100× battle figure "a Fermi estimate, not yet measured" |
| "we should not keep for the work out of sunk cost fallacy, if it's good, good, if it's bad it goes away" | [2026-09-14T09:17 codex] | **Followed**: v0 contract retired (H0195), old lineage archived (H0182) |
| "gravity is intrinsic to this spacetime compiler so we should act like it" | [2026-09-12T11:51 codex] | **Followed**: one event queue, gravity as field claims |
| "i still want to ship one day... i want my 1B ships" | [2026-09-25T11:58 claude] | **Open**: galaxy_one_million failing at the cap (HANDOFF ladder v7); billion-scale exists only as descriptions |
| "I want it to be believable at all scales" | [2026-09-25T12:10 claude] | **Followed in design**: rungs R0–R5 up to galactic nuclei (gravity-law.md) |
| "Ok we need to build towards GR that's the goal... the rest are stepping stones" | [2026-09-26T08:18 claude] | **Followed**: plan steps 2–9 |
| "i don't care yet about past the event horizon" | [2026-09-27T09:08 claude] | **Followed**: gravity-law "nothing is evaluated at r < 2M", B6 |
| "i care about the p95/99 results i want the game to be smooth" | [2026-09-25T14:06 claude] | **Superseded then in progress**: worst-frame target adopted (see §3); smooth gate currently failing for metal/hybrid/regions |
| "gpu should heavily be used for anything i believe"; "spacetime is fundamentally the most gpu thing in our system" | [2026-09-25T14:40], [2026-09-27T09:08 claude] | **Drifted from**: canonical gravity runs on CPU, "Metal only for dense contacts" (HANDOFF step 6); narrowing never debated with him |
| "we can even have regions that are delayed if not on screen"; "maybe we can afford in some regions to lag behind?" | [2026-09-25T14:28 claude], [continue #8] | **Followed**: engine.md rule 8 sacrifice order |
| "human readable codes... used to share exact seeds and game state" | [2026-09-25T15:48 claude] | **Followed**: engine.md share codes |
| "thermals on the computer influence a lot the result of the tests, maybe 30% fluctuation" | [2026-09-25T21:47 claude] | **Followed**: HANDOFF machine section records the 30% |
| "one test i'd like to run is a closed box... akin to a trapped gas" | [2026-09-25T13:45 claude] | **Followed**: ladder C2 trapped gas |
| "we should test like a spartan would train, harder than for the war... extremes inform the mean" | [2026-09-25T12:51 claude] | **Followed** (test-ladder.md), but the doc stores a rewording, not his words (see §4) |
| "it needs to be remembered and either disproven or followed i can be wrong" (defines the register itself) | [2026-09-29T08:39 claude] | **Followed**: PRINCIPLES preamble, incl. "Silence is never disproof" |
| "why was the philosophy lost?... normally the philosophy is clear and meant to be known at all time" | [2026-09-29T08:39 claude] | **Followed after the H0184–H0194 drift**: heading-check card, preamble; the incident itself is only implicit in the multipoles row |
| "you don't give AGI the task to count the cookies"; "bigger models have more wisdom" | [2026-09-28T11:37], [2026-09-28T18:56 claude] | **Followed**: AGENTS.md team tiers |
| "the things that are contradictory should be separated but not necessarily deleted, anything that serves the goal" | [2026-09-28T14:34 claude] | **Followed**: corrections appended, archive kept |
| "we need a whole system to run this project for the long term that doesn't grow out of hand... imagine documentation and intent is bad when you auto-compact?" | [2026-09-28T14:51 claude] | **Followed**: AGENTS text budgets, HANDOFF in-flight table |
| "You can abuse GLM it has a LOT of usage (you barely used a percent)"; "It's a wildcard that we're underestimating" | [2026-09-28T12:10], [13:23 claude] | **Partially drifted**: AGENTS caps GLM to pull-based loops, "at most one finding waiting" — a throttle he never stated (see §4) |

---

# 3. Contradictions (both sides kept, unresolved)

1. **MVP vs cathedral.** "it's a MVP for today so what you'll output i'll have to make it today" [original-conversation.md #16, early ideation] vs "build cathedral foundations, not an MVP" (PRINCIPLES principle 8, in force by 28–29 Sep 2026) and "start clean build messy-ish and then finish clean" [2026-09-28T10:04 claude/codex].
2. **Smoothness metric.** "i care about the p95/99 results i want the game to be smooth" [2026-09-25T14:06 claude] vs the build he approved two hours later: "The target is the single worst frame, not p99" [2026-09-25T16:18 claude, pasted plan]. engine.md now watches p50/p99 *and* max.
3. **Fundamental quanta.** "what if we were to define plank constants that are useful for us and meaningful?... use decimals instead of floats?" [original-conversation.md #36] vs "do we even need floors?" [2026-09-26T17:32 claude], with the AI's adaptive-precision answer ("precision is adaptive too") left as a pasted suggestion — current truth is fixed integer lattices with rounding carries.
4. **Graphics.** "graphics don't matter" [original-conversation.md #16] vs the sustained aesthetic programme: "use real materials, don't make it overly saturated and contrasted use more the color style of sinbad" [2026-09-25T11:43 claude, pasted You-turn] and the AGENTS.md aesthetic line (ink, watercolor, ivory, pale blue).
5. **Minimap.** "there's a minimap but first let's discuss it" [original-conversation.md #16] vs "i don't believe that we need a minimap basically the zoom level is the minimap" [original-conversation.md #30].
6. **Black holes / strong gravity.** "maybe i should drop the two black holes idea" and "so i guess we can omit it for now then" [both 2026-09-25T11:58–12:10 claude] vs "I want black holes because they create very interesting gameplay" [2026-09-27T09:08 claude] and plan step 9 (Kerr, inspiral, merger).
7. **Parallelism.** "implement in parallel as much as possible the build" [2026-09-25T16:18 claude] vs "not doing too much parallel work because the real issue is caching" [2026-09-28T12:10 claude] and HANDOFF's "one job at a time".

---

# 4. Current violations

1. **GPU under-used against an explicit instruction.** "gpu should heavily be used for anything i believe" [2026-09-25T14:40] and "spacetime is fundamentally the most gpu thing in our system" [2026-09-27T09:08] vs HANDOFF step 6: "Metal only for dense contacts; canonical formulas on the CPU", and gravity-law.md's canonical integer algorithm (Astra's crate, CPU). The exactness rationale may justify it, but neither doc records his statement or shows the narrowing was ever put to him.
2. **Mode-collapse timing deferred without his sign-off.** The plan line he was shown read "collapsing the five engine modes into one before step 4, not after" [2026-09-28T12:10 claude, quoted; he asked "what does that mean?"]. Today's plan collapses at step 6, after the player slice and many-body work, while five modes remain live through steps 2–5. His 29 Sep "yes, why not one?" [2026-09-29T08:05 claude] records the decision, never the deferral.
3. **"Finish jobs before starting new ones" (register, marked Followed) vs four concurrent in-flight jobs** (geodesic crate, GLM red-team + probe, philosophy mining, gate-harness merge pending) in HANDOFF. The integrator's carve-out ("parallel work is limited to read-only briefs and independent judges") is a weakening of his rule that he never endorsed.
4. **Qualitative-testing preference silently dropped.** "So our tests shall be more qualitative then quantitative" [2026-09-14T09:17 codex] vs gravity-law.md B1–B9 as purely numeric tolerances. Behaviour-grounded, but the preference is nowhere recorded or disproven.
5. **Quiet-machine probes vs measured-like-the-player.** HANDOFF: "Eight probes of at most 60 s each are pending for a quiet machine" vs AGENTS (his rule): "heat and load are part of reality, not noise to sidestep". Silicon characterization may warrant it; the tension is unaddressed in the doc.
6. **His words are reworded in normative docs**, against AGENTS' "models propose changes and never reword". test-ladder.md attributes "test like a Spartan trains — harder than the war" (his actual: "test like a spartan would train, harder than for the war", [2026-09-25T12:51]); AGENTS renders "Measure the way the player plays" as "Measure the way the player will run it".
7. **Unendorsed plan element attributed to him:** HANDOFF step 4 "Julien predicts before each run" — no basis anywhere in the corpus. Mark unendorsed.
8. **Minor:** AGENTS' "one process change per week, and none in a week with no physics merge" and the GLM pull-based single-finding throttle both constrain "always improve how you do things" [2026-09-28T11:45 claude] and "abuse GLM… spend every provider's usage" [2026-09-28T12:10] — reasonable integrator inventions, but they go beyond, not merely implement, what he said.

Two corpus caveats for whoever reconciles this with the parallel Opus run: the `original-conversation-continue` AI replies are missing (see note above), so endorsements from that thread rest on Julien's turns alone; and the 2026-09-26T08:54 codex block is a replay of the Claude session into Codex (duplicates, not new material), while the two 2026-09-28 specialist briefs in `codex-julien-messages.md` (11:41, 15:09) are agent-written prompts, not Julien's words.
