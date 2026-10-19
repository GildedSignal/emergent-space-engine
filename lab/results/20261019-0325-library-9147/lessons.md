# Five lessons: the E9 far-scheduling door (the per-reader horizon)

4a71's named fix — "the oldest term's scope (only items that can READ body i hold its history),
not the margin" — composed and priced; each lesson holds one moving part. Quotes 5/5
byte-identical, fresh 4,590-highlight export (`python3 verify_quotes.py`).

**1. Delete the requirement, do not tune the margin.** "Step one should be to question the
requirements," he says. "Make them less wrong and dumb, because all requirements are somewhat
wrong and dumb. And then delete, delete, delete." — Elon Musk | Walter Isaacson. *Mechanism:*
the global `oldest` ("any pending item anywhere holds every body's history") was free at one
star and is ruin at the first interstellar doll. *Change:* delete the global read, replace with
the per-reader scope; 2²⁶ untouched. *Test:* 4a71's probe, third arm — per-reader rule with a
far item live: near-body retained at the control 1.02/body while the global arm staircases.

**2. The freeze gate is the second-order term.** "**First-order thinking is fast and easy.** It
happens when we look for something that only solves the immediate problem without considering
the consequences. For example, you can think of this as I'm hungry so let's eat a chocolate
bar." — Second-Order Thinking | Farnam Street. *Mechanism:* the global rule is first-order sound
(universe.rs:1230) and second-order ruinous: retained = 1+⌊min(D,elapsed)/27.6k gs⌋, unbounded
in play time. *Change:* E9's gate bars retained/body flat in play time with a far item in
flight, not just zero `history pruned` refusals. *Test:* one wave period with the item live.

**3. Sandals, not leather.** "To walk a thorny road, we may cover its every inch with leather
or we can make sandals." — The Art of Learning | Josh Waitzkin. *Mechanism:* leather is every
body carrying history for every pending item; sandals are each body carrying only its own read
window. *Change:* body i's horizon = min over items whose read window covers i; the shipped
`child_ticks` germ (universe.rs:170, filter `doll(i) != 0`) is the pattern, `ship_ticks` has 8
uses all set/peek — one site (`oldest` in `Universe::prune`, :1240). *Test:* cross-doll reads
are the soundness hole: `ladder_digest` bit-identical + a boundary scan; any
`Refused("history pruned")` widens the scope to the item's light diameter.

**4. Retention is arrival-keyed.** "Intelligence is not only the ability to reason; it is also
the ability to find relevant material in memory and to deploy attention when needed." —
Thinking, Fast and Slow | Daniel Kahneman. *Mechanism:* retention serves retrieval by pending
readers, not archival; a far item needs a near body's history only from its arrival minus the
body's light distance. *Change:* the horizon key is the item's read time at the body, not its
emission tick. *Test:* a near body's horizon under a 4-ly item equals the scene's own bound
(max gap 2,302.5 s → retained 1), never the 4-year transit.

**5. The falsifier must run long enough to see the law.** "In the short term, you are as good
as your intensity. In the long term, you are only as good as your consistency." — Brain Food:
Gather and Synthesize | FS. *Mechanism:* the 20-s rung under-reads the steady state ~7–11×
(d839); the staircase is invisible in any 20-s window. *Change:* fly ≥ one wave period (27.6k
gs) past the far item, both controls — global arm staircases, per-reader arm holds the control
flat (d839's 45.5k+ gs protocol). *Test:* compose_e9.py's P4 table is the divergence (4/37/182/
4,577 vs 1 generations).
