# Predictions — run 20261009-1649 (second author on 20261009-1556-redteam-18fc)

Written before the decisive run (`view_kink run <rtf> <frames>`), after harness construction and
tuning only (probe/sweep modes; the tables below have not been run past 60 frames at rtf 1, which
is before the first light of any 0.9999c emitter).

## The experiment (the checker's named one)

Kinked tubes: emitters whose worldlines are kicked by the shipped engine's own stepper (a 1/999
secondary on the convergence point of 12 Toward emitters; `step_log2` 14 so the clock fires), at
β = 0.9, 0.9999 and the mutual 0.9 × 0.9999. Straight control = the same geometry with `step_log2` 7
(no emitter is ever kicked: their clock steps are ~1e11 ticks). The oracle is a bisection on
`g(t) = t + |x(t) − xo| − t_now` (monotone: a tube is timelike), an independent search that shares
only the worldline reads.

## Predictions

- **P1 (control holds).** The straight control at rtf 1 shows the author's straight-tube numbers:
  0 drops, 0 cold-vs-memo disagreement, reads/em ≈ 1.7–2.1, and 0 oracle mismatches. If this fails
  my harness is wrong, not the engine (the control is the instrument check).
- **P2 (kinks exist and are swept).** At `step_log2` 14, ≥ 6/12 emitters rebind (event_time > 0)
  before or during the window; at rtf 1 × 600 frames the arrival burst (the whole flight's light,
  first light ≈ frame 295) sweeps the emission tick across those rebind ticks, so ≥ 5 kinks fall
  inside the swept emission range of the kinked-0.9999 cases. The engine refuses most of the
  player's clock kicks at this step size (sweep: ~10.5k refusals) — engine-side, reported, not a
  view failure.
- **P3 (the premise survives kinked tubes).** Every kinked case: 0 drops while alive, 0
  cold-vs-memo disagreements, reads/em ≤ 4, worst frame ≤ 1000 readouts. Mechanism: the walk is
  bracketed and the memo is only a guess; kinks and stale slopes degrade the guess, never the
  answer. Falsified if any drop or disagreement appears.
- **P4 (oracle agreement).** The gather's emission tick equals the bisection's tick on every
  emitter-frame (0 mismatches), including tick-0 pre-first-light frames and post-passage frames.
  A mismatch means the bracket contract fails on a kinked worldline — premise wrong.
- **P5 (stale jumps).** The stale-jump case (5 jumps of 40 frames) keeps 0 disagreement and 0
  oracle mismatch; reads/em rises (the memo crosses kinks stale) but stays ≤ 8; the cache recovers
  within one frame (the author's stale contract, now under kinks).
- **P6 (what the engine cannot do — the regime limit, stated in advance).** No configuration the
  engine accepts produces a strongly-kinked relativistic emitter: the measured deflection of a
  0.9999c emitter through a 1/999 source at 2e4 root units is ~5e1 root units over a 1.2e9-root-unit
  flight (~4e-8 relative), the clock's steps at β→1 are 1e8–2e9 ticks (1–2 rebinds per emitter over
  the whole flight), and `step_log2` 20 (the only way to force more) does not settle 1.2e9 ticks in
  ten minutes. The kinked-tube content class at the design's worst case is therefore near-empty by
  physics (a tide is 1e-7 of a relativistic body's kinetic energy), not by an engine defect.

## Kill criteria

Any drop while alive, any cold≠memo row, or any oracle mismatch in any kinked case kills the
premise's claim to survive kinked tubes (gold as a refutation). If nothing fails, the premise audit
stands complete with P6 as its scope limit.
