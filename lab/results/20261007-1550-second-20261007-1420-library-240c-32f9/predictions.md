# predictions.md — written before the decisive run (2026-10-07, before b12_matrix.py ran)

The decisive experiment (the one the checker named): the classification matrix on the B12 gate's
**real** series — the plane's own Jacobi errors and the gate's control laws on the same frozen
chaotic ships, N = 1601 (200 periods × P/8, the gate's own length) — against the frozen triple:
N = 1601, Allan-slope threshold θ = 0.10 (overlapping Allan deviation, lags 8…512, OLS in log),
min-detectable-leak stated as a ratio to the 1e-12 floor. Verdict rule: worst seed decides (any
judged ship above θ ⇒ the law fails B12 v2), ships under the floor not judged, exactly as today.

Series source: `b12dump` dumps `err_series` per law per judged ship via the gate's own code
(verbatim copies of xtask's restricted/handoff/plane/laws/fit). Anchors already recorded from the
shipped binary (`behave --law X --gates B12`, this machine): planted-bounded median-exp 0.353 /
worst err 1.27e-5; planted-compound 0.416 / 9.80e-7; planted-drift 1.355 / 2.40e-9; echo 0 rising /
2.31e-15; plane loses ships (inf). 14 of 16 frozen ships judged here (chaos moved 2 out of the
oracle's domain on this platform). The dump must regenerate those numbers exactly.

## P1 — the controls at real conditions (θ = 0.10, worst seed)
- **echo**: all series under the 1e-12 floor → not judged → **passes** (no false leak).
- **scaled1e-11** (smooth bounded, above the floor): max Allan slope **< 0.10** on every ship → passes.
- **planted-bounded** (bounded by construction, killed by today's exponent at 0.353): max slope
  **< 0.10** on every ship → **passes**. This is the decisive row: the miscalibration case.
- **planted-compound** (random walk per encounter): min slope over ships **> 0.10** → fails.
- **planted-drift**: min slope **> 0.10** → fails.
- **leak-per-period** (1e-12/period, end ~2e-10 ≫ floor): min slope **> 0.10** → fails.
- **plane** (the real population): fails B12 regardless (it loses ships ⇒ no answer ⇒ fail, as
  today); on the ships it **does** answer I predict the slopes read **bounded** (max ≤ 0.10):
  its handoff error is per-event, a function of the state, not a memory. If it reads leak instead,
  that is a finding about the plane, not about the statistic — either way it is reported.

## P2 — the inversion dies per seed
Today's exponent interleaves bounded and leak on the same ships (gate's own test:
median bounded 0.49 > median compound 0.31 at freeze; here 0.353 vs 0.416 with per-seed overlap).
Predicted: with the Allan slope, **bounded max < leak min** across all matrix rows, with a margin
wider than 0.05 (i.e. the dead band survives contact with real chaotic series).

## P3 — checker's adversarials, re-run at N = 1601 with θ = 0.10
- Slow bounded oscillation (sine, amplitude 1e-6): **≤ 2 periods per scene → false leak 16/16**
  (slope ≈ +0.7); **≥ 4 periods → 0 false leaks**. Freeze as a scene requirement: the horizon
  spans ≥ 4 periods of any bounded structure (B12's ships' a-oscillation is per-orbit; the
  200-period horizon gives ~200 periods, so the requirement holds at the gate's own conditions).
- AR(1) ρ = 0.99 (stationary, long-correlated): reads **leak** (as at N=2048). Freeze states it:
  on the horizon the gate cannot tell it from a walk and classifies by correlation structure —
  stated in the freeze, not hidden.

## P4 — min-detectable-leak (leak-rw planted on the real bounded-floor scale)
Detection is ratio-dependent: end magnitude ≈ 1× floor reads bounded (invisible — information,
the horizon sets the floor); detection becomes reliable (16/16) at end magnitude ≈ 2–4× floor.
Freeze: **min-detectable-leak = 3× the floor (3e-12 relative) at the 200-period horizon**, stated
as part of the gate (below it the gate certifies "under 3e-12", never "no leak").

## P5 — record regeneration
`b12dump` regenerates the shipped gate's detail-line numbers (median exponent among rising,
worst err, per law) from the dumped series to displayed precision — the record regenerates from
shipped code; if it does not, the run is VOID on its own rule.

## What would kill the claim
- Any false leak on echo/scaled/planted-bounded (bounded side) or any miss on
  compound/drift/leak-per-period (leak side) at θ = 0.10, N = 1601, with no other threshold in
  the dead band fixing both sides at once.
- The plane's answered ships reading leak while its worst err stays flat (statistic fights the
  err bound) — then the Allan slope is not measuring what B12 needs on the real population.
