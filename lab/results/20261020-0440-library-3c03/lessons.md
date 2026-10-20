# Five lessons — the finality fire's survivor, pinned and priced (each holds one decision)

1. **FS, "Reversible and Irreversible Decisions"** — "You can tell where a decision lies on
   this spectrum by asking how much it would cost to undo. The higher the cost to undo, the
   more irreversible it is."
   Mechanism: `fin_parts` are the allocator's published commitments; undoing one costs the
   whole process (the assert, exit 101). `regroup` mints a region whose fin parts are the
   members' union (`union_parts` → `make_region`'s `set_final`) — an irreversible decision
   taken as if free, exactly when undo is costliest (after rollbacks, live truths sit below
   the merge tick). Measured: FIREWHY `why=["merge@864"]`, parts owned by donors 11/3/37.
   Decision: the fix gates the mint. Cheapest test: flown here (arm 3).

2. **Taleb, Antifragile** — "clip your downside, protect yourself from extreme harm, and let
   the upside, the positive Black Swans, take care of itself."
   Mechanism: deferring every merge that would mint past a touchable live truth clips the
   downside (fires 3/10 → 0/10) and the upside with it: on the battle class that is every
   merge (42–168 defers/draw, merges 11→0, regions 23→23, present 1792→538 = the
   no-conflict floor, final lead pinned at 0). Downside-clipping that deletes the upside is
   a control, not a fix (min_region's splits all over again).
   Decision: the shippable form caps the mint — inherited parts publish only down to the
   touchable truths' floor — never defers the merge. Test: one cap-not-defer arm; kill:
   fires return, or `expect("final parts…")` panics on an empty cap.

3. **Korzybski, via FS "All Models Are Wrong"** — "A map is not the territory it represents,
   but, if correct, it has a similar structure to the territory, which accounts for its
   usefulness."
   Mechanism: `certify` keys truths by lineage id and exempts only `t.id == d.id`; `regroup`
   mints a fresh id for old territory, so a merged region can clash with — and be restored
   by — its own members' outstanding truths (id 44 ≠ minted id 51). Rollback's `affected`
   already works on the territory (shared snapshots; `aff=[(51,976)]` from lid 44's truth).
   The fire is that asymmetry: publish by map, crash by territory.
   Decision: the mint must inherit its members' live truths as its own (self-clash ⇒ no
   restore below own stride start), or carry lesson 1's cap. Test: the FIRE draws' RB lines
   (already measured — every fire's affected set is snapshot-sharing with the truth).

4. **Feynman, "Surely You're Joking"** — "The first principle is that you must not fool
   yourself—and you are the easiest person to fool."
   Mechanism: both gates (da23's and this run's pre-registered (d) fix) guard
   `alone_at`/`final_through` — and on the battle class those paths decide NOTHING (0
   DECIDED lines in 22 instrumented draws, every arm): all publication is the frontier
   advance plus the regroup mint. The survivor lived in the unguarded path; the guarded one
   was dead code on this class.
   Decision: before freezing any gate, count the decisions the guarded path makes per scene
   class; a guard over zero decisions is presence, not protection. Test: one instrumented
   draw per class; the DECIDED counter is the falsifier.

5. **Taleb, The Black Swan** — "There is no such thing as END, Evidence of No Disease."
   Mechanism: arm 2 (truth ids) ran 0/10 clean in the author's quieter window while arm 1
   fired 3/10 — but arm 2 is behaviorally identical to arm 1 on this class (lesson 4), and
   the regen's loaded window (load 6.7–15.6) inverted it: arm 2 fired 2/3. Cleanliness was
   NED, not END; sequential blocks confound load with arm.
   Decision: fire-incidence tables come from interleaved paired draws only, and an arm is
   credited through its mechanism (state evidence: FIREWHY chains), never through absence
   of fires. Test: this run's interleaved matrix is the protocol.
