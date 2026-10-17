Grade: gold

Abstract: The named gold experiment flew, and it decides against both controllers. The
ratchet's latch is exactly 2^rollbacks and scale-coupled: reproduced E=4→32→64–256 at
44→14,080 bodies; my 28,160-body run reaches E=512 at 10 chronons/s. The decay mirror and
its per-region variant livelock: DNF > 240 s at 14,080 bodies where shipped finishes in
56–74 s, and the wedge recurred in three of my own draws. Outcome digests are bit-identical
across arms, reps and margins wherever arms finish — scheduling never moves results. Cost to
adopt: nothing — the decision is "adopt neither"; the capped escalation is the named
one-line next experiment. A premise (the mirror restores the equilibrium) is shown wrong at
scale, reproduced independently by both checkers.

## Reasons

1. **Reproduction.** Clean tree at `3dc6f621` (matches `base`), `git apply work/patch.diff`
   clean, build ok, and **14/14 shipped allocator tests pass with arms off** (one flaky
   failure only when my batch runs shared the box; clean in isolation — the dossier's claim
   holds). The runner's `regen.sh` (exit 0, 13 min) reproduces every table row within the
   stated nondeterminism; my own interleaved reruns agree at draw level: 128 cells/6k
   shipped 3.6 s, 7 rollbacks, E=128, regions=1, digest `49f5fc2b…`; decay ground 44
   rollbacks at 260 chronons/s with the same digest; local DNF(90 s).
2. **E = 2^rollbacks is exact in every observation**, mine included: 7→128, 6→64, 8→256
   (author, 1,280 cells), 9→512 (my 2,560-cell run). The mechanism claim is not a fit.
3. **Predictions pre-registered.** `predictions.md` 02:55:29; first decisive log 03:00:45;
   dossier last. P1 held (stronger than predicted), P4 held, P5's counter half held; P2 and
   P6 inverted and are reported as the finding, not buried — the question was "does any tax
   survive at scale" and the answer (no: latch-coupling and livelock replace it) is the
   result.
4. **Adversarial cases (five, one outside the author's range):**
   - **2,560 cells / 28,160 bodies, shipped, 1,500 chronons** (outside range): finishes in
     149 s at **10 chronons/s**, E=512, 9 rollbacks, 6,879 regions (wave ⅓ across the row).
     The scale-coupling and the throughput collapse continue into the next decade.
   - **stagger=300 (sparse wave), 128 cells**: 0 rollbacks, E=1, 356 regions — but only
     74 chronons/s. Wave simultaneity, not crossings, drives the latch; and the many-region
     end state is itself the slow one. Both support the page's corrected reading.
   - **TAX_MARGIN=1.0, 128 cells, 6k**: shipped digest `49f5fc2b…` — identical to margin 2.0
     and to the decay arm; decay DNF(90 s) (wedge draw #2 of my session). Digest invariance
     extends across margins, not just arms.
   - **horizon 1,000, 128 cells**: local finishes but pays 30 rollbacks vs shipped's 7,
     digest still identical — the mirror arms' failure is a fat-tailed grind/wedge, not a
     hard always-fail.
   - **relativistic law, 8 cells / 88 bodies, 6k**: finishes (15 s, 388 chronons/s), **zero
     rollbacks, E=1** — the law-derived margin kills every conflict at every size tried;
     what stays unmeasured is the many-region regime's cost (new datum, folded into the
     page's open direction 4).
5. **Novelty.** The published `lab/wiki/allocator-ratchet.md` (updated by the original run)
   holds none of: latch-vs-scale, livelock, the 10⁴-body collapse, ES_LOCAL. Its open
   directions 1–3 are exactly this run's experiments. No HISTORY entry covers any of it.
6. **Goal fit.** The allocator is principle 12's own object ("the algorithm that allocates
   the work … it's the most important one"); the finding is that the rollback response is
   not a controller at scale on either side — "basically we don't want errors that can
   compound" (P13) cuts both ways and is measured here, and adopting the mirror would have
   been ruin (P25: "don't multiply by zero"). Kills a wrong adoption and pins the one-line
   bounded fix: gold's "shows that a premise is wrong".
7. **The one dossier overstatement**: "no player-visible separation … in every arm" (frames,
   1,408 bodies) — ES_LOCAL has a player-visible ruin tail the author's 3 reps missed
   (regen: present 286/600, 64 deadline misses, buffer p50 0). The page already carries
   this correction; my regen evidence confirms it. Does not touch the claim.

## Page corrections made (checker 2)

- The 28,160-body line: "DNFs at 150 s" was the timeout — the run finishes in ~149 s at
  10 chronons/s with E=512=2⁹, so the latch clears 2⁸ at the next decade ("saturation" is a
  band, not a cap). Corrected in place.
- Open direction 4: added the 8-cell relativistic datum (finishes, zero rollbacks, E=1,
  388 chronons/s) — margin-from-law kills conflicts at every size tried.

## What the author missed

- The ES_LOCAL frames ruin tail (3 reps was too few for a fat-tailed arm).
- The 28,160-body DNF was a timeout artifact, not a wedge (see above).
- The relativistic control does work at small scale — the "unmeasured ceiling" is the
  many-region cost, not the conflict kill.
- The livelock cycle is still unopened (the author names this honestly): no core dump or
  instrumented loop naming the spin.
- Everything rests on the synthetic Fermi-cannon battery and one world per size (`seed` is
  dead code) — stated by the author, but it bounds every frequency claim to one scene
  family.
