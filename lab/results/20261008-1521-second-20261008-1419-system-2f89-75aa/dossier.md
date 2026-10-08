# Dossier — run 20261008-1521 (second author on 20261008-1419-system-2f89)

## Claim

The SEM step on the v2 clock is killed **structurally and scene-independently**: across five
scenes (belt, unseen seed, eccentric ensemble, two planets at generic Ω, encounter-dominant
flybys) × two step sizes × three variants (plain states, the SEM manifold, and the most
root-favourable flyable SEM trajectory), the fraction of steps with a **usable** root
(α ∈ [1/2, 2], runaway roots classified out) is **0–24%** — the memo P8 kill line
(solution missing at > 1% of steps) is exceeded ≥ 4× at its *strongest* cell
(ecc k=6: 76.1% of steps without a usable root) and is unbounded at two planets
(0 usable roots in 3,200 plain records and 9,808 trajectory steps).

## Bottleneck

The instrument bottleneck the checker named, not a cost one. The first run killed SEM but
its record had three defects: "no solution at all" was overstated (solutions exist at
runaway α), the decisive diagnostic lived only in a transcript, and the pre-registered
prediction missed 30–50×. This run closes all three: the usable-root census is frozen
beforehand, swept over scenes, and regenerates bit-identically from shipped code. It also
runs the structural probe the checker derived but did not run (K(start)=0 ⇒ no nonzero
root; success at n starves n+1). What it deletes: the exact-constraint closure question
is retired for every scene family tried, so B12-v2 can certify a bounded state-function
offset without waiting for an exact-constraint law.

## Evidence

Linux x86 cloud, orders of magnitude only. All numbers from `census.py` (this folder),
which imports the author's `p8.py` unmodified. `census.py summary` prints the table;
each JSON sits beside this dossier.

**Usable-root fraction (α ∈ [1/2,2]), 8 ships × 200 steps (flyby 300):**

| scene | k | plain | zero (K(start)=0) | best trajectory |
|---|---|---|---|---|
| base | 6 | 0.188 | 0.038 | 0.027 (after-root: 0.0000) |
| base | 8 | 0.043 | 0.010 | 0.006 (after-root: 0.0000) |
| seed99 | 8 | 0.044 | 0.011 | — |
| ecc | 6 | 0.239 | 0.103 | — |
| ecc | 8 | 0.137 | 0.026 | 0.020 (after-root: 0.0000) |
| two | 6 | **0.000** | 0.041 | — |
| two | 8 | **0.000** | 0.009 | **0.000** |
| flyby | 6 | 0.139 | 0.068 | 0.041 (after-root: 0.139) |
| flyby | 8 | 0.082 | 0.014 | 0.011 (after-root: 0.025) |

Every cell is ≥ 4× below the 99% the kill line allows; nan audit 0 everywhere; 0 ships
lost; best trajectories completed 2 planet periods each.

**The overstatement, measured (bracket sensitivity).** On the full grid [1/64, 64] roots
exist for 23–100% of steps (one-signed only 0.3%–77%), but for steps whose only roots are
outside the usable band the median root α is **10.7–32.3**, where the step is a
multi-orbit frozen-force kick: median |K| stays flat to α=2, then leaves the nominal
residual scale (base k=8: 7.6e-12 → 8.2e-11 at α=8 → 3.9e-8 at α=64; k=6 runs reach
|K(64)| ~ 10⁵–10⁶, i.e. the clock pole). These are runaway roots, not solves.

**The structural prediction, probed.** On the SEM manifold (p_t reset so K(start)=0)
usable fractions collapse 2–6× below plain in 8 of 9 scene×k cells (one inversion:
two k=6, 0.000 → 0.041, both ≪ 1). On live best trajectories, a step that *found* a root
is followed by a usable root **0.0000** of the time at base and ecc (the checker's
"success at n nearly guarantees no-solution at n+1", confirmed in the offset regime) —
but at flyby roots come in encounter **bursts** (after-root 0.14–0.03 vs after-no-root
0.04–0.01, inverted): the cubic-competes regime clusters consecutive solvable steps
without ever approaching 99%.

**The new hard scene.** Two planets at generic Ω (0.4·μ at 9.5 AU) is the strongest kill:
0/1600 usable at both k (sensitivity band [1/4,4]: 0/1600 at k=8, 23/1600 = 1.4% at k=6).
With no rotating-frame symmetry there is no per-kick Noether cancellation: the per-step
constraint residual is ~1.3e-7 (verified against a null-second-planet control that reproduces p8's one-planet
8.06e-12 exactly), and the solve never returns a nominal step. The author's own feared
counter-case (encounter-dominant dynamics) tops out at 24%.

**Instrument controls** (`controls.json`, `noether.json`): roots found are true zeros —
worst |K(α\*)| = 7.3× K's float floor, 0/127 eligible sign-flip failures; Kepler-only
negative control flat (spread 2.2e-16) with 0 roots; the Noether identity the author
cited but never shipped now runs: one-planet 8.7e-15, two-planet 1.2e-8 against a
quadratically converging finite difference.

**Commands** (from this folder; solo timings — the parallel batch ran ~24 processes and
stretched these 3–12×):

```
python3 census.py controls                                   # ~8 s
python3 census.py noether                                    # ~1 s
python3 census.py census base 8 plain 200                    # ~31 s
python3 census.py census two 8 plain 200                     # ~2 min
python3 census.py census flyby 6 plain 300                   # ~6 min (slowest)
python3 census.py best base 8 2.0                            # ~60-80 s
python3 census.py summary                                    # instant
```

Regeneration verified: `census base 8 plain 200` re-run after all edits reproduces its
stored JSON **bit-identically** (30.9 s). Code was edited twice mid-set, both times for
crashes that produced no partial output (a shape bug in the two-planet field, a scalar-t
bug in `run_best`); no finished record predates a change to its own code path.

## Predictions

[predictions.md](predictions.md) was frozen before the decisive runs. What happened:

- **P1 (plain usable fractions) missed low everywhere**: I predicted 0.25–0.65, measured
  0.00–0.24. My bands were anchored on root-anywhere fractions and I still guessed near
  them; usable roots are 3–10× rarer. The miss strengthens the kill.
- **P4 (Z collapses below plain) held in 8/9** (inversion at two k=6, both ≪ 1%);
  **P5 held** on frac_usable < 0.5 and on after-root starvation at base/ecc
  (0.0000), **failed at flyby** (bursty encounter roots invert the conditioning).
- **P2 half-held**: runaway median root α 10.7–32.3 > 3 everywhere ✓; median
  |K(8)|/|K(1)| > 10 only at k=6 (k=8 one-planet gives ~5).
- **P7 (roots concentrate at encounters) held in 5/6**, inverted at flyby k=6.
- **P6 (the verdict) held**: every cell ≤ 0.239 ≤ 0.90; kill line exceeded ≥ 4×
  everywhere. **P8 held**: 0 nan; |K(1)| k6/k8 ≈ 10× (ds² ⇒ 16×).

## What would make it wrong / cost of adopting

- The kill is for the SEM solve **on the step's own time** with the whole step scaled,
  exactly as the first run posed it. A different projection direction (kick weight alone,
  half-step solve, KMO's discrete-action step) is untested; the α²-sign structure and the
  two-planet first-order term make me doubt any local variant closes the constraint, but
  doubt is not evidence.
- The two-planet scene uses the standard summed indirect term and per-planet Noether
  p_t updates; any other consistent two-planet split still has no rotating symmetry, so
  the first-order residual (and with it the kill) survives the choice.
- Adoption cost: none — this deletes a candidate (the memo's P8) and frees B12-v2 to
  certify "bounded, state-function offset" (memo §1.7) rather than exact conservation.
- PRINCIPLES: "A failed expectation is not automatically a failed method: diagnose which
  one broke" (H0183) — the equation's root structure is what broke, now measured on five
  scene families; "Errors never compound" (#13) — the representation refuses exact
  closure locally, so v2's shadow-offset error type is the floor for this family.

## The lens

The second-author lens: I inherited the checker's recipe and ran it, so I inherit its
blind spots — the usability band [1/2,2] is the checker's choice, frozen by me without
sweeps; the band-sensitivity column (roots in [1/4,4], 0–31%) brackets it, and no band
inside [1/4,4] rescues SEM anywhere (max 31% vs the 99% needed). What the recipe may
still miss: scenes with genuine three-body chaos (the non-hierarchical regime the board
flags for the rotating binary doll), and whether an integer fixed-iteration solver could
*use* the bursty flyby roots (4% duty cycle) — a question of stability, not existence.
