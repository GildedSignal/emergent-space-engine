# Predictions (written before the decisive sweep)

Question: at and beyond the plane's frame capacity, does foundation 7 hold — overflow is a
smooth real-time-factor dip with no debt, no unbounded synchronous claim, and identical bits —
or does the plane become convex (backlog makes each event dearer, hitches grow, bits drift)?

Setup: `xtask universe --bench`, scene = the plane (star, planets, moon, a battle of `members`
in a Fermi frame, scripted player), threads 1, seed 1. Sweeps: demanded RTF (unpaced and paced),
engine budget (engine-ms), battle members, throttle level.

Cases I have NOT tuned on, and what I expect there:

- P1 capacity: delivered RTF ≈ demanded (ratio ≥ 0.9) up to some capacity R* (I expect
  R* between 10² and 10⁴ at the default 5 ms budget), then delivered flattens near R*
  (slope ≈ 0), it does not collapse (delivered/demanded falling faster than 1/demanded).
- P2 no debt: CPU ms per game-second at 100× beyond capacity stays within ~1.5× of its
  value at capacity. Doubling per decade of demanded RTF = debt = fragility (falsifier).
- P3 bounded frame: in paced runs at any demanded RTF, p99.9 frame ≤ ~17 ms and the worst
  hitch ≤ ~50 ms. A worst hitch ≫ engine budget + gather p99 means an unbudgeted synchronous
  claim (a compile, a rebinding burst, a gather) — falsifier for "nothing hitches".
- P4 identical bits: same (seed, rtf, seconds, level), engine budget 5 / 1 / 0.2 ms and
  paced vs unpaced → one digest. A differing digest is silent nondeterminism under load
  (ruin), the worst outcome this lens looks for.
- P5 fat cell: members 4 → 400 (100×) at fixed rtf below capacity: engine cost per frame
  grows ≤ 10×. Convex growth (> 30×) says one battle sizes the frame (Extremistan claim).
- P6 the wildcard: throttle level MAX at rtf 3k: cost per game-second within ~2× of level 0;
  > 5× says the player's own held burn is the tail that sizes the machine.
- P7 recovery: in the paced RTF series, the dips follow the script's 4-second burn/coast
  pattern (oscillation), they do not ratchet downward over the run.

Kill criteria for the plane's smooth-dip claim (any one): delivered RTF collapse past capacity
(P1), cost per game-second growing by ≥ 2× per decade of demanded RTF beyond capacity (P2),
worst paced hitch > 50 ms at saturation (P3), or digest mismatch across budgets (P4).
