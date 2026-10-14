topic: frame-cost
status: open
closed-by:
valid-while:
updated: 20261014-1511-quant-7226

# The frame loop and the kick resolver: cost per body and per kick

## Current best

**The crash search is counted probe by probe on shipped code, and the naive smarter-probe
lever on it is killed with the mechanism named (20261014-1511-quant-7226).** Additive
counters in `step.rs` (`step::searches`, printed by `--kick-bench`; digest
`36637e67…` = the pristine build's, off = shipped verbatim): at the flying arm
(m400/s3/rtf100, 8 game-s) the kick's surface search runs **802 `next_impact` searches
paying 23,552 exact readouts — mean 29.4, worst 32 per search** (held-out s7: 1,225 /
36,367, mean 29.7, worst 33); 29.4 ≈ log₂ of the ~2^30-tick half-orbit bracket, so the
midpoint bisection sits at its policy class's floor — no probe is wasted, the policy wastes
them. `next_exit` searches are **0** wherever the passage's analytic guess applies (its
endpoint probes: 1,188) — the guess retires the whole exit search, not just accelerates it.
The lever this count invites — choose the probe by the radius value the predicate already
reads, float places / integer decides — was built three ways (Illinois on values, Illinois
on signed distances, vertex-quadratic matched to the flat periapsis, plus a pure secant),
**digest-identical in every arm and seed** (canonical + replay; refused 0; a new crate test
asserts fast = slow on every dipping tube of a settled plane, two surfaces, two starts) and
**killed by the pre-registered rule**: best arm −4.6 % probes, worst 57–58 (the 30-probe
fallback fired), leaver median +55 % on the final arm. Mechanism from probe traces: the
crossings are mid-branch with deep dips (periapsis 3–7× the level deeper than the miss
end), local slopes healthy and consistent (~4.4 units/tick over 2×10⁷ ticks), but every
chord through the retained miss anchor (signed distance ~10⁸) lands a fraction
|d_hi|/d_lo across — a one-sided crawl at ratio ≈ 0.23 that no halving rule in this family
breaks fast enough. The named survivor: **Anderson–Björck (or inverse-quadratic through the
newest three probes) — checker-measured, not just named: mean 21.3/22.3 probes at seeds
3/11 (−28/−24 % vs bisection), leaver median −25/−26 %, digests identical, but worst 38
> 30, so the frozen tail rule kills plain AB too**; the update rule must penalize the
retained miss anchor multiplicatively **and** bound the degenerate tail (a bail at 8
probes measured worse: mean 27.5). The counters and
the equality test are adoptable as-is (zero cost unread); they are the contract for the
warm start's freeze and for any Carlson readout change that touches the search. Domain:
Linux/x86 shared box, one scene family (plane battle, seeds 3 and 7), flying pace only
(battle pace fires no surface searches at m400); the grazing-dip regime (crossing near the
periapsis) is where the warm start already settles in two readouts and would flatter a
quadratic policy. Regeneration: `lab/results/20261014-1511-quant-7226/regen.sh`.

**Prior best (20261014-1010-second-20261014-0450-quant-1845-0b85):** the warm start is
built, measured and exact — the kick's rebought crash-tick search falls 38–44 % for zero
fallbacks, shipped digests never move; and (20261014-0450-quant-1845) the fired kick is
46 % bind, 45 % one `next_impact` bisection (≈ 25 readouts × 4.6 µs), 9 % the rest; the
search fires on every fired kick because `rebind` resets `Binding.impact`.
## Refuted
- **"A value-guided probe policy cuts the crash search" as a one-hour build**: three
  bracketed policies (Illinois absolute/signed, vertex-quadratic) plus a pure secant all
  crawl one-sidedly at ≤ 1.4 bits/probe and lose to midpoint bisection (worst 57–58
  probes, leaver kick +55 %; digests identical everywhere) — the miss anchor's value
  dominates every chord until an Anderson–Björck-class update replaces plain halving
  (20261014-1511-quant-7226). The lever itself is not refuted: the pre-registered kill is
  of the update rules built, and the traces name the survivor.
- Illinois's halving applied to the **value** rather than the signed distance to the level:
  2.0× the probes (the halved anchor leaves the level's neighbourhood entirely) — a
1. **Anderson–Björck / inverse-quadratic probe update with a tail guard on the same exact
   predicate** — the named experiment this run leaves, half-built by the checker: plain AB
   already gives mean 21.3 probes (seeds 3/11), −25/−26 % leaver median, digests identical,
   but worst 38 (the frozen rule's tail); a bail to bisection at 8 probes measured worse
   (mean 27.5). The open part: bound the degenerate tail without paying the typical case —
   then compose with the warm start (it deletes searches that moved < 1 tick; AB cuts
   probes on those that did not). Budget: one hour — the harness (counters, env gate,
   equality test, kill rule) is already in the tree. Note: of the four killed policy rows,
   only the pure secant is regenerable from `work/patch.diff`; Illinois-on-signed was
   reproduced by the checker at mean 28.0 (author 28.0, worst 30, digest identical).
2. The warm start (0b85) then lands on top: it deletes the search where the crossing moves
   by under a tick; AB deletes the probes where it does not.

## Contradictions
- (unchanged) The stack's lazy-tier gate regression and the frame-cost page's merge
  conflict are the integrator's to resolve; this run's page proposal folds into whichever
  side stands.

## Runs
- 20261014-1511-quant-7226 (this run, awaiting grade): the search census (29.4 probes mean,
  worst 32; exit searches 0 behind the passage guess) and the probe-policy kill with the
  crawl mechanism traced; counters + equality test adoptable.
