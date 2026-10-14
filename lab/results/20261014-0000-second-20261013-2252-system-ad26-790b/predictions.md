# Predictions (written before the decisive census; the m4000/seed-1 pilot is the only run seen)

The checker's named experiment, done as a build: the record's engine-path levers — 009b's word
fix, 7055's exact memo, 5eb6/8b43's lazy tier — stacked on one binary against shipped code at
f687ec25 (ad26's probe for the census; every lever env-gated for the A/B arm:
`ES_BASELINE_ARM=1 ES_EAGER=1` restores the shipped bind and the shipped frame loop). de99's
Carlson kernel is priced, not wired: it delivers the walk's three increments, and the bind's
compile exists to build the panel grid the readout interpolates (`orbit.rs`: `from_shape` reads
`knots.last().sum`), so the kernel is not a drop-in for `bind_surface`'s compile — the endgame's
"×10 on 70% of the bind" is tested below as arithmetic on the measured compile share, and its
applicability is a code-reading claim the checker can attack.

Pilot (m4000, seed 1, rtf 1, 8 game-s, not held out): digest bit-identical to shipped
(`5c8fe1a8e439221d`, 1,058 kicks, 2,163 leavers), fit2 1,141 → 0 calls, hand-out bind
930.8 → 504.6 ms, rekey 961 → 4, requeue 2.09 M → 12.6 k, take_due 377 k → 4 k calls.

## Pre-registered expectations (held-out arms; not run yet)

1. **Digests hold everywhere the settle resolves the scene** (m48, m400, m1500 s1/s7, m4000 s1,
   m400 rtf 100): the lazy tier's known break is sustained starvation (3-event budgets, rtf 5e6,
   seeds 2/5/9, threads 4 — 8b43's checker), which no census arm is. **Risk arms:** the
   overflow-dominated rungs m12000 (seed 3) and m20000 (seed 1) — ad26's own record shows counts
   moving with the wall there on shipped code; I predict digest identity still holds at m12000
   (the settle resolves everything to the same cut) but the m20000 counts may move with the
   budget exactly as shipped's did. Kill criterion: a digest that differs between the stacked and
   the shipped arm at m4000 or m1500 kills the "one adoption queue" claim outright.
2. **The 009b×7055 interaction:** with the word fix landed, the memo's hit rate at m4000 falls
   from 33% to < 2% of compiles (7055's hits were exactly the retry's recompiles, which the word
   fix deletes), and the memo moves hand-out bind by < 5%. If the hit rate stays > 20%, the two
   levers compose multiplicatively and ad26's arithmetic stands; my reading says it does not.
3. **The composite:** D (process + hand-out + fleet item + decisions) at m4000/rtf 1 falls to
   70–78% of the shipped arm's D on the same binary (pilot: ~142 against ~198 ms/game-s); with
   the fixed tier (outside D but inside the frame) the total event-class work falls to ~60%.
4. **The gold bar fails as stated:** the checker's bar was measured D at m4000 within ~2× of the
   42.3 ms/game-s arithmetic. Predicted measured D ≈ 140–160 ms/game-s ≈ 3.3–3.8× the
   arithmetic, because (a) word fix and memo overlap on the retry (ad26 counted both), and
   (b) Carlson's kernel does not replace the bind's compile. Even pricing Carlson ×10 onto the
   measured compile share of the surviving bind lands ≈ 90–100 ms/game-s, still above 2×.
5. **Overflow and tails:** at m4000 the stacked arm's overflow frames fall (the fixed tier's
   700 ms/8 s is freed; baseline overflow 291–309/480 → predicted ≤ 250) and the worst engine
   frame improves by the same order; at m20000 the mix shifts as the checker measured (fixed tier
   gone entirely, bind share rises).
6. **The suites pass** on the stacked default paths (`cargo test --release -p emergent-space -p
   emergent-universe`, 0 failed).

## Kill criteria

- Digest moves at a canonical arm (m4000/m1500, seeds 1/7): the stack is not adoptable; KILL the
  one-queue claim.
- Memo hits > 20% on the word-fixed bind: my interaction reading is wrong; the composite's
  arithmetic gets a second chance.
- D_stack > 0.95 × D_shipped: the levers do not compose at all; KILL.
