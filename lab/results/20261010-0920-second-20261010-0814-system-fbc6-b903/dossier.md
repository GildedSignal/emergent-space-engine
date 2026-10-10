# Dossier — second author on 20261010-0814-system-fbc6: the accumulator link holds, with two named conditions

## Claim

The checker's named experiment — the accumulator actually modeled (principle 6:
sub-quantum member news accumulating until it crosses the parent's coarser quantum),
plus the ghost question for sub-quantum readers — **upholds the original claim,
conditionally**: on the real B12 scene (JUPITER: μ = 1e-3, sep = 5.27e8, Hill doll
R_sub = 3.65e7, parent R_p = 5.27e9), with member news folded at arrival into a
running moment error, the parent chain **flatlines at λ_agg·min(r_q_agg, R_p) —
measured 8,341 live records against 8,379 predicted (0.5%) — with zero unserved
reads at the bound** (half-bound misses 336), while KEEP-FOREVER grows through
70,182. The bound survives only under two conditions this run measured and named:

1. **The published aggregate program must carry velocity** (a doll's real state).
   A position-only program re-published against a moving source makes the aggregate
   rate grow with time — the wall returns through the accumulator (half-vs-half
   stationarity z up to +348). With the first-order program the rate is stationary
   (|z| ≤ 1.3) and its quantum scaling matches derivation on all four process/fold
   laws: −1.004 vs −1 (coherent/impulse), −1.974 vs −2 (signed/impulse, 1.5 decades,
   the event cap's honest limit), −0.514 vs −1/2 (coherent/drift), −0.682 vs −2/3
   (signed/drift) over 4 decades each.
2. **The fold's own light delay sets a quantum floor.** An impulse δ arriving at the
   fold after its member's light-crossing r_k lands as an immediate error δ·r_k; a
   parent quantum below σ·R_sub publishes at ~the member rate (driven cell: λ_agg =
   0.70·λ_tot, 83,792 aggregate events from 120,635 member news). Still bounded and
   still flat-lining exactly — but the accumulator thins nothing unless the doll's
   quantum exceeds its members' news impulse × the doll radius.

And the original run's mechanism is now measured, not asserted: **the death rule at
the member level is false without the aggregate** (the checker's ghost question). If
sub-quantum readers read member tubes individually, TTL = min(r_q, R) misses **173,860**
of their reads (zero misses at TTL = R); served by the published aggregate instead,
the same policy misses **0**, and the served version's error is capped at exactly one
quantum (max 200.0 = dx, 0 violations in 31 publishes). Principle 6 is load-bearing
for the bound, not a refinement.

## Bottleneck

The named gap between that run's silver and gold: run C's zero-contribution rule was
an `if` statement and "the link is assumed one-level … exactly where the bound could
break." This run breaks it or holds it, on the real scene's numbers. What it deletes:
the unbounded member log (1,317,170 records under KEEP-FOREVER → 1,617 flat at the
fold-arrival death rule, Little's law 1,762, TTL = R_sub over-retaining 2.3×), and
the design risk that `b-news-gravity` ships a position-only publish (condition 1) or
a doll quantum below the fold floor (condition 2).

## Evidence

Real scene throughout (`xtask/src/behave/restricted.rs` JUPITER; geometrized G = c =
1). Commands (this folder, single-threaded Python, < 600 MB):

```
python3 causal.py a|b|c --json run_*.json   # 36 s: the original record regenerates bit-for-bit (cmp identical)
python3 accum.py d1  --json run_d1.json     # 7 s:  real scene, 1.3e6 member news, 3 quantum cells + the giant
python3 accum.py d1b --json run_d1b.json    # 3 s:  driven cell, populated parent chain
for c in coherent,impulse,0 signed,impulse,0 coherent,drift,0 signed,drift,0 coherent,drift,1 signed,drift,1; \
  do python3 accum.py d2 --only $c --json run_d2_$(echo $c | tr ',' '_').json; done   # ~4 min; largest combo ~90 s
python3 accum.py e   --json run_e.json      # 1 s:  the ghost question, both service modes
python3 accum.py equiv --json equiv.json    # 1 s
python3 check.py                            # every table below + the 24 verdicts
```

1. **Member wall killed by the fold** (d1): KEEP-FOREVER 131,153 → 1,317,170 (linear);
   death-at-arrival flat 1,617 mean (Little 1,762), no trend; the half-window control
   starves 609,692 folds; TTL = R_sub holds 2.3× more for zero extra served reads.
2. **The fleet at the parent, real parameters** (d1): at r_q_agg ≤ sep (the quantums
   where planets resolve the doll), **0 aggregate crossings** from 1.3e6 member news —
   the fleet is absorbed below the quantum. At the finest cell (r_q_agg = R_p,
   Δx = 5.27e6): **5 crossings** — the integrated drift does surface there. My
   prediction missed this constant twice (<3, then 10–25 re-predicted; measured 5).
3. **Parent chain on accumulator-produced records** (d1b): rule flatlines 8,432 → 8,341
   (predicted 8,379.2), zero misses, half-control misses 336; KEEP-FOREVER reaches
   70,182; TTL = R_p holds 8.4× the rule at run end, still filling toward its own
   asymptote λ_agg·R_p/R_sub = 144× (beyond this run's horizon).
4. **λ_agg exponents + stationarity** (d2): all six cells above; the two order-0 drift
   cells are the negative demonstration (exponent −1 in Δx as derived, z to +348).
5. **The doll-less thrusting giant** (d1): the original dossier's conceded wall case is
   a level, not a slope — rule flat at 50 vs predicted 52.7 (λ_g·R_p), KEEP-FOREVER
   11 → 127; at r_q = R_p/3 flat 16–22 vs 17.6. The death rule buys 1× there (window
   = R_p): honest, as the original run conceded.
6. **The ghost question** (e): numbers in the claim. The aggregate chain holds 10 live
   vs 50 for member tubes at TTL = R (the saving is λ → λ_agg, not the window).
7. **Fold equivalence**: integer fold vs reverse-order recompute bit-identical (ℤ),
   1e5 events — the fold consumes news at arrival; no log recompute is ever needed.

## Predictions

`predictions.md` (with its dated pre-rerun addendum: two instrument fixes — exact
crossing solve, program order — made after the first pass, all disclosed there and in
run.log's copy of the first-pass numbers). **23 of 24 verdicts hold** (`check.py`).
The miss: prediction 2's constant at the finest quantum (above). Two further honest
notes: the first pass's zero-delay-free drift cells measured −0.698/−1.003 before the
delay-jump term was isolated (those numbers regenerate by reverting the one marked
line in `run_d2`); and d1b's λ_agg = 0.70·λ_tot is the delay floor of condition 2,
not a sizing error.

## What would make it wrong

- Correlated fleets are the adversarial case and are covered (coherent cells hold,
  stationary), but a fleet whose news rate itself grows with time (a battle's opening
  minute) would grow λ_agg with it — the bound is per source-rate, as the original
  claim always said (λ is the certificate-breaking news rate).
- The toy's fold is scalar (one moment component). A real doll publishes a multipole;
  each component has its own quantum and crossing rate; the sum could exceed the
  scalar bound by the component count. Cheap to check; not checked here.
- Readers are static circles; feedback (a reader newsing because of what it read,
  through the front) is the original run's named unbuilt adversarial case, still
  unbuilt.
- Everything here is a toy on the scene's numbers; `b-news-gravity` (the crates
  build) may meet layout costs (allocation, cache lines) the record-count metric
  cannot see.

## Cost of adoption

Three rules for `b-news-gravity` (the queue's build), each one line of design:
publish the aggregate as (position, velocity); delete member ghosts at fold arrival
and aggregate ghosts at min(r_q_agg, R)/c; size the doll's quantum ≥ the members'
news impulse × the doll radius, or accept an aggregate chain as costly as the member
chain (the doll's own light-crossing is the accumulator's resolution limit).

## Fit with PRINCIPLES

- Principle 6 ("influences below one quantum accumulate"): now measured as
  load-bearing — without the accumulator the death rule misses 173,860 reads.
- Principle 19 ("a fix signals the wrong representation"): the position-only program
  was the wrong representation, and its fix was the representation (carry velocity),
  not a patch: z +348 → ≤ 1.3, exponents −1 → −1/2.
- Principle 3 (compute only surprises): the fold consumes news at arrival; the member
  wall (1.3e6) collapses to in-flight news (1,617).
- Principle 33 (each scale resolves only what matters): the fleet never surfaces at
  the parent at planet-resolving quantums — 0 of 1.3e6 news cross.

## The lens

The second-author lens trusts the toy: the sharpest thing it may have missed is that
the two conditions are stated as universal from one scene's parameters — the quantum
floor (condition 2) especially wants a second scene (a compact binary's doll, where
σ·R_sub is huge) before it is called a law. The multipole-component count and the
growing-λ battle minute are named above but unmeasured. And the checker's full ask —
the death rule wired into the crates' engine with per-frame work measured — remains
one build away; this run hands that build its measured law and its two named
conditions rather than a bare confirmation.
