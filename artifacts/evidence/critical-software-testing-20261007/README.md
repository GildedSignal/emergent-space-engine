# How fields that cannot break test, and what we steal (7 October 2026)

Julien's ask: research extremely critical software, keeping in mind that our tests exist "so that we reduce the time towards detecting when we're fooling ourselves, not to prevent issues". These fields can't afford to break, so their heuristics are battle-tested. We steal the ones that cut detection time, and leave the ones that only buy prevention at a cost we can't pay.

## What they do

| Field | Practice | Why it matters to us |
|---|---|---|
| Space Shuttle on-board software (IBM/Lockheed Houston) | Errors fell to about one per version of ~420,000 lines. Every escaped error is traced to the process step that let it through, and that step is fixed. An independent verification group competes to find bugs. | Fix the process that let the escape through, not only the code. Reward the judge per bug found. |
| JPL "Power of Ten" (Holzmann, 2006) | At least two assertions per function on average; loop bounds fixed; no allocation after start-up; every return value checked; zero warnings | Assertions are tests that run in every test and every flight, with detection at the source |
| TigerBeetle (TigerStyle, VOPR) | Assert the positive and the negative space; assertions stay on in production; a deterministic simulator speeds time up, so an hour of simulation covers about a month of real time | Keep invariant checks on in flight (we refuse with a reason); speed simulated time up |
| FoundationDB | The simulator was built before the database. BUGGIFY fault points make rare paths common in simulation, and one 64-bit seed replays the whole failure. | Make rare things common: test knobs that force ties, worst-tick handoffs, registers near their limit, small budgets |
| SQLite | 590 lines of test per line of code, 100% MC/DC, four independent harnesses. The "veryquick" set runs before each check-in, in minutes; the full set, hours long, runs before release. They inject faults: out-of-memory, I/O errors, power loss. SLT compares 7.2 M queries against other databases; dbsqlfuzz runs about 500 M cases a day. ALWAYS/NEVER macros mark assumptions. | The barbell in practice (quick per check-in, full per release); fault injection; differential testing |
| AWS (Newcombe et al., CACM 2015) | TLA+ model checking of designs found subtle bugs, one with a shortest trace of 35 steps (DynamoDB replication). Engineers became productive within weeks. | Exhaustively check the small, hairy, order-sensitive cores (events, ties, handoffs, gravity's cursor) |
| Alloy (Jackson): the small scope hypothesis | Most bugs have small counterexamples, so test every input within a small bound | Enumerate every ordering of ≤ 4 bodies' events within a bound: exhaustive, cheap, model-free |
| Paris Métro line 14 (B-method, 1998) | The safety software was refined by proof from its specification. Faults were found at the assumptions about the environment, not in the proven core. | Proofs work where applied; bugs live at the edge of the proven part (domains, interfaces) |
| Csmith and CompCert (Yang et al., PLDI 2011) | Random differential testing found hundreds of bugs in GCC and LLVM. In CompCert, it found none in the verified middle and some in the unverified front end. | Random differential testing between two implementations: sparse against dense, chronon against the engine |
| Airbus fly-by-wire | Dissimilar redundancy: a command channel and a monitor channel, built by different teams, in different languages, on different processors. The monitor is simple. | A small, dumb envelope monitor separate from the clever step |
| Knight & Leveson (1986), replicated with coding agents (arXiv 2606.20158, June 2026) | Independently written versions fail together far more often than independence predicts, on the hard parts of the spec. The 2026 agent replication finds the same thing, with common-mode failures tied to ambiguities in the spec. | Model diversity is not independence; a judge must use a different method. Removing ambiguity from a spec is a test. |
| Trading: pre-trade risk checks, kill switches | Simple independent limits sit outside the clever system. Knight Capital (2012) lost $440 M in 45 minutes: one server of eight left un-updated, and a repurposed flag that woke dead code. | An envelope monitor; delete dead code; check that every machine runs the same build (digest parity) |
| Jane Street (OCaml) | "Make illegal states unrepresentable" | Types for frames, exponents and ticks: the compiler is the fastest test |
| Google SRE | Error budgets: ship fast while the budget lasts; stop and harden when it is spent | A fooling budget: escapes per window decide how much effort goes to tests |
| SpaceX | Prototypes (Starship) fly to learn and may break; crewed Dragon flies to NASA's rules; "test like you fly" | A barbell by kind of artefact: branches and the lab break fast; the law, main and frozen gates do not |
| Toyota (jidoka, andon) | The machine stops itself on any abnormality; anyone can stop the line | Fail loudly at the first violated invariant; a red main stops the line |
| Erlang | "Let it crash" under supervisors: fail fast, recover fast | Never continue on corrupt state; restart from the last good state (the view's fallback) |
| Aviation (ASRS; checklists) | Anonymous near-miss reports with immunity; blameless investigation; short checklists. Checklists cover only what can be foreseen (Bevelin). | Log near-misses, not only escapes; checklists only at one-way doors |

## The failures they paid for

| Case | What happened | The pattern here |
|---|---|---|
| Ariane 5, flight 501 (1996) | Ariane 4's inertial code converted a 64-bit horizontal velocity into a 16-bit integer, which overflowed on Ariane 5's faster trajectory. The function was not even needed after lift-off. Both units ran the same code, so both failed. | **Our 6 October v2 regression**: a register sized for the old regime overflowed in a faster one. Identical redundancy does not protect against a design error. |
| Boeing 737 MAX (MCAS) | One sensor; authority raised late in development without redoing the safety analysis | A change of range or authority invalidates old evidence: re-check each test's domain |
| Therac-25 (1985–87) | Software replaced hardware interlocks; a race at fast operator input; reused code; cryptic "MALFUNCTION 54" messages | Never remove an independent check when adding a clever one; test at player speed (fast keys); plain messages (the loss report) |
| Mars Climate Orbiter (1999) | pound-force seconds against newton seconds at the interface between two teams. The navigators saw the anomaly but did not escalate it. | Units in types at interfaces between owners; an unexplained anomaly is a stop |
| Challenger (1986) | O-ring erosion on earlier flights was read as margin. Managers estimated 1 in 100,000; engineers estimated about 1 in 100. Feynman: nature cannot be fooled. | Normalisation of deviance (Vaughan): a partial failure that "passed" is a failure. Our B13 at 60/64 is a ratchet, never a pass. |

## What we do not steal

| Practice | Why not |
|---|---|
| Certification paperwork and traceability matrices (DO-178C) | Months of cost |
| 100% MC/DC as a target | SQLite's 590:1 suits a 25-year-old stable library; our representation changes weekly. Coverage serves only to find untested code. |
| Whole-system proofs | seL4 took years of person-effort for about 10,000 lines |
| N teams using the same method | No independence |
| Requirements frozen up front | Ours are still being discovered. We freeze a gate per step instead. |

## Sources

**From Julien's library:**
- Taleb, *Skin in the Game* (Hammurabi's builder).
- Taleb, *Incerto* (automation dulls pilots).
- Bevelin, *Seeking Wisdom* (ASRS, critical incident analysis, the limits of checklists).
- Munger, *Poor Charlie's Almanack* (the pilot's checklist).
- Hijink, *Focus: The ASML Way* ("It's not about preventing errors, but how well you manage them").

**Web:**
- [SQLite testing](https://www.sqlite.org/testing.html)
- [Knight & Leveson 1986](https://www.kth.se/social/files/564df871f2765419e306178d/KnightLeveson.pdf)
- [N-version programming with coding agents (2026)](https://arxiv.org/abs/2606.20158)
- [AWS formal methods](https://6826.csail.mit.edu/2019/papers/formal-methods-amazon.pdf)
- [TigerBeetle VOPR](https://docs.tigerbeetle.com/about/vopr)
- [FoundationDB-style simulation (Antithesis)](https://antithesis.com/docs/resources/deterministic_simulation_testing/)
- [Alloy and the small scope hypothesis](https://en.wikipedia.org/wiki/Alloy_(specification_language))

**From general knowledge, not re-fetched:** the Shuttle group, Power of Ten, Ariane 5, the 737 MAX, Therac-25, Mars Climate Orbiter, Challenger, Knight Capital, Airbus, Csmith, and line 14.
