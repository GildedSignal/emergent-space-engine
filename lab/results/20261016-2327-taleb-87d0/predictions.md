# Predictions (written before the decisive experiments; 20261016-2340)

Topic: wiki-memory. Closing silver 20261016-1835-inversion-de18's named residual
(defuse mis-pairs interleaved depth ≥ 2 damage; heal and its check count `<<<<<<<`
only; the truncated-block fallback emits captured sides raw, letting markers back
in through crafted interleaves), then the checker's named gold experiment: truly
zero marker lines on the real pages, before and after a publish.

## Pre-registered

- **P1 (today's census, all three marker kinds).** nladder: 7 `<<<<<<<`, 7 `=======`,
  5 `>>>>>>>`; ≥ 1 orphan `=======` and ≥ 2 blocks that never close; encounters
  balanced; scan-queue carries ≥ 1 never-closed `<<<<<<<` (5 open / 4 mid / 4 close).
  The index prints marker text as "Current best" for exactly 3 of 30 topics.
- **P2 (arming control, shipped code, real inputs).** Replaying the two real
  20261016-1637 nladder runs (pages + base `2ac3c8d2` from their branches) through
  shipped `apply()` against the pre-window page yields ≥ 1 `<<<<<<<` marker. I do
  NOT predict byte-identity with today's page (marker label order may differ);
  I predict marker count ≥ 1 and depth ≥ 1.
- **P3 (patched heal, the three real pages).** Zero lines matching any of the three
  marker kinds (`^<<<<<<< `, `^=======$`, `^>>>>>>> `) after heal; every non-marker
  line of each original present with equal multiplicity (only defuse's banner and
  `*Version` labels added); each page's `## Runs` list unchanged; the regenerated
  index has no row leaking marker text.
- **P4 (the gold case: a further publish on healed nladder).** One more nladder
  publish (a next-run page based on the healed state) through patched `apply()`:
  zero markers of all three kinds before and after; the runs-union gains exactly
  the new run's line.
- **P5 (the checker's killer cases).** Concurrent publishes from damaged/marked
  starts (interleaves like the checker's E1/E2/E3, built from the real nladder
  damage) through patched `apply()`: zero marker lines in the final page.
- **P6 (amplifier).** Patched `apply()` over a results directory that re-presents
  an already-folded gold run: a no-op (the run's page line already in the Runs
  list ⇒ skip). The same replay without the skip: the page grows ≥ 1 labeled
  version block (or worse). 
- **Held-out (not tuned on).** The exact orphan counts on encounters and
  scan-queue; whether P2's replay lands byte-identical to today's page; the exact
  number of labeled-version blocks P5 leaves.

## Kill criteria

- Any marker line of any of the three kinds surviving P3/P4/P5 ⇒ the fix fails.
- Any content line (non-marker, non-label) lost by heal ⇒ the fix fails.
- Shipped apply() NOT deepening on P2 ⇒ my premise that compounding is live on
  real inputs is wrong (then the whole topic is process hygiene, not ruin).
