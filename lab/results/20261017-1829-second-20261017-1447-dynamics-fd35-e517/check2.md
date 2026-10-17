Grade: gold

**Abstract.** e517 closed fd35's named experiment: the finality assert's firing is
state-decided at certify. 9/18 protocol draws fired; every fire preceded by PRE
`D = 16 = fin_hi − s0` (9/9, on the preceding line in 7) and by armed `A > 0` from
publish 8–12 (lead 51–452); all 2,286 non-fatal realized clashes at m = 0; `out=`
(sibling-closure gap) empty on 0/2,295 RB events. I reproduced 6 further fires
(sweep, batch, rate-1200) — D = viol exact, armed preceded, `out=` shut — and the
equality law held on ~2,300 further RB events at 2× N, drift, wave and window 32.
Gain: the engine fix's gate becomes the per-draw state certificate, deleting the
window Monte Carlo. Adoption cost: none (print-only patch); the fix itself is untouched.

## Reproduction

Clean tree at the recorded base 781875d7; `work/patch.diff` applies; the runner's
regen exited 0. Verified independently, not from the summaries:

- **Harness provenance:** `finpol.rs` byte-identical to 01e7's branch copy;
  `race.rs` byte-identical to fd35's run patch. The alloc.rs instrument is fd35's
  verbatim plus the `out=`/`mo` RB field (37 delta lines, all print-only; the
  assert and its message untouched — fires panic at the shipped line).
- **Author's window logs re-derived from raw:** 9/18 fires (s11/13/15/16 2-of-2,
  s14 1-of-2, s12/17/18/19 0-of-2), 2,295 RB events, 9 m≠0 (exactly the fires),
  `out=` 0/2,295, mo = 0, D<0 never, 950 PRE at D = 0, 18 D = 16 lines = 2 per
  fatal certify (the benign armed twin, disclosed), 9/9 survivors armed. Per-fire:
  fatal PRE adjacent in 7/9, gap 8 lines in the two s13 late-reclash fires (s0 = 80,
  viol 16); first armed p8–12; lead 51–452.
- **My own hands (fresh processes):** sweep s11/13/15/16 fired first-try, s14
  survived armed — 4 fires, all D = [16] = viol, 0 armed-before-fire fails, `out=`
  0/548. Regen's numbers (4/7 fires, `out=` 0/852) sit between, as raced.

Numbers that differ from the dossier, all raced/schedule-moved counts with the
invariants identical: regen churn-arm rollbacks 1300/1283 (dossier quoted its own
regen's 565/558) and 1,101 clashes (vs 1,123); h_nosab 13 armed publishes (vs
14–15), A = 128, rb = 0 as claimed; regen RB events 852 (vs 906); s13 gap 8 lines
(vs "9"); lead up to 452 (vs 449). None touches a claim.

## Predictions

`predictions.md` mtime 18:33:44, after the disclosed pilot (work/smoke 18:32:22)
and before the sweep (work/sweep 18:35:29). P1–P6 all held on the sweep; the kill
criteria were pre-written and none triggered.

## Attack (my own cases; two outside the author's range)

1. **2× N** (480 bodies, n240, seeds 11/15 — outside the author's range): both
   survived armed; 894 RB events, all m = 0, `out=` shut, D<0 never.
2. **Double load** (rate 1200, s15 — outside the range): **fired**, viol = 16,
   PRE D = (16, 274, 32) then FIRE s0 = 32 fin_hi = 48, armed from p9, `out=` shut.
3. **Batch driver** (selfchurn batch 1800, s11): **fired**, D = (16, 310, 32)
   immediately before FIRE — the first checker's batch extension reproduced by hand.
4. **Window 32** (s12): survived; 231 RB all m = 0; 17 armed D = 32 lines with 0
   fires — the page's "armed ≠ incidence" note, confirmed.
5. **New scenes** drift (bulk approach) and wave (zero churn): 2 RB each, m = 0,
   `out=` shut.

Total: 19 fires now recorded across all executions, every one D = viol exact and
armed-preceded; zero invariant failures on ~2,300 further RB events. The claim's
domain is honestly scoped and my extension widens it.

## Novelty

The published page (updated: fd35) names this exact gap: "the named experiment
left is one firing reproduction on the integrator's selfchurn harness to time the
armed lead before a fire", and flags `affected`-outside-the-closure as
asserted-not-shown. e517 does the first and measures the second (`out=`). Not a
repetition; no HISTORY entry covers it.

## Page

Faithful; every number I could trace checks against the logs. One correction
made in place: "which is WHY D is exact" overstated a mechanism as fact —
containment (out empty) proves D never misses; exactness is the measured
equality, the derivation stays open (the page's own direction 7). Now says that.
The "114–116 D = 32 lines per draw" figure is draw-dependent (my w32 draw: 17);
the phenomenon, not the count, is the claim. Not gold-closing: one gold here,
fd35 awaits its first-checker grade.

## Goal fit

Direction 7 of the allocator-ratchet board topic; supplies the test for the
confirmed-necessary engine fix (open direction 1) and deletes the window Monte
Carlo. PRINCIPLES 34: "the oracles are guards, not shepherds" — D judges the
boundary, it does not move it; PRINCIPLES 13: "errors never compound" — the
certificate reads the state the assert would abort on.

## What the author missed

- The geometry derivation (why `alone_at` and `certify` pin the same tick; why
  `affected` never escapes the descendants closure) is the missing soundness
  argument the fix will be written against — the page says so; a next run could
  attempt it from the snapshot-sharing invariants in code.
- The certificate's online cost is unmeasured: HAZ's armed scan is O(busy ×
  truths) per publish. Print-only here, but if the fix adopts "armed ≤ 0 ∧ D ≤ 0"
  as a live gate, that scan ships — its cost belongs in the fix's design.
- The author's own sweep stayed on one family and one load; my rate-1200 fire
  shows the load axis was worth one arm.
