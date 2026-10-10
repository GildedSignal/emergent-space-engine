# Predictions (written before the decisive jet runs)

The run I am second-authoring (20261010-2141-system-eea5) measured that every
firing kick pays one full trajectory compile (`Rebinding::from_state`), 37% of
the median kick and 91% of the p99 on the resolver, and claimed the already-
adopted jet (offset-from-entry, re-anchored) is the lever, ceiling ~1.6× median
/ ~10× p99. The checker's gold experiment: wire the jet, re-run `--kick-bench`
and the gates (B5's exponent, B12's Jacobi). Wiring under test: a velocity-only
kick whose deviation from its generator stays within `JET_DRIFT` velocity quanta
(L∞, the binding's own residual) joins the residual instead of recompiling —
the readout stays exact at the kick itself; past the bound the kick rebinds
(re-anchors). Handoffs, thrust flushes and re-wordings always rebind exactly.
`JET_DRIFT` swept at 730 (the red-team df81 bound: the 10⁻⁶ floor at 730
correlated quantum kicks) and at 8 (a deliberately tight control).

## Held-out predictions (not tuned on)

- **P1 (compile rate):** with `JET_DRIFT = 730`, `compiles_per_kick` on seed 1
  falls from 1.0 to below 0.2 (the law's own figure is ~0.05). If the tide's
  kicks anticorrelate across the orbit (the residual random-walks rather than
  drifts), re-anchors become much rarer still.
- **P2 (median):** the made kicks' median falls by roughly their compile share:
  to ~15–35 µs from ~47 µs (seed 1) — the jet's honest median ceiling.
- **P3 (the tail, the run's own named blind spot):** the leaver p99 does NOT
  fall the full ~10×: deep-encounter kicks carry impulses of many quanta and
  re-anchor immediately, and the compile is ~91% of those samples, so the p99
  of `kick_us_all` falls to ~100–250 µs (a 2–4× cut), not below 100 µs. A p99
  below 100 µs would mean the tail was not compile-bound after all.
- **P4 (the gates):** B12 on `--law plane` passes with the jet at both 730 and
  8 (median Jacobi growth exponent ≤ 0.2, worst error ≤ 1e-4). Risk named: if
  the red-team's C·drift² does not transfer to the weak-field B12 scene, 730
  fails while 8 passes — then the run reports the largest passing bound as the
  jet's real anchor rate. G5 on `--law space` is untouched by construction (the
  patch never enters `crates/space`) and passes unchanged.
- **P5 (determinism):** the kick replay digest is identical across two runs of
  the same jet build, and `refused = 0` on both seeds.
- **P6 (memory):** `bytes_per_body` in the 10 s unpaced bench is unchanged
  (that window fires no kicks); the jet's memory effect is not measured by this
  bench and is not claimed.

## Kill criteria

- If `compiles_per_kick` stays above 0.5 at `JET_DRIFT = 730`, the plane's
  firing kicks move the velocity by hundreds of quanta each and the jet as
  wired serves nothing on this scene: the ceiling claim stands as the lever's
  obituary, and the run says so.
- If B12 fails at every `JET_DRIFT` that reduces compiles, the jet is killed by
  the gates on this scene (a configuration kill, never a method kill), and the
  37%/91% shares stand as the ceiling of a dead lever.
- If the p99 falls below 100 µs, P3 is wrong in the favourable direction and
  the run's blind-spot warning was too pessimistic — report that honestly.

## Amendment (written before the decisive jet runs, after the first jet build)

The first wiring (bound = 730 velocity quanta absolute, the red-team df81
figure) fired zero jets on 37 + 83 kicks: the plane's firing kicks move the
velocity by 2⁻³²·v…2⁻¹⁹·v each (median 2⁻²⁴·v, measured on this run's bench
`/tmp` diagnostic), and the fit's own residual is ≤ 2⁻²⁶·v — so 730 quanta
(≈ 2⁻⁴⁹·v at this word) is 2²⁵ times smaller than one plane kick. The
red-team's calibration lives where a kick is one quantum; the plane's
sigma-delta carry fires at 2⁻²⁴·v. The bound is re-parametrized as a relative
drift (`v >> JET_REL_LOG2` of the body's own speed), swept at 16, 20, 24; the
absolute-730 result stands as the finding that the calibration does not
transfer. Predictions P1–P3 now read on the relative bound: at 16 I expect
most kicks to jet and compiles/kick ≤ 0.2; at 24 I expect near-baseline
(almost no kick fits under the bound). P4's gate check is unchanged, with B13
(assists, baseline 60/64 within 1e-2 on this checkout) as the comparative
physics probe, since B12 and B14 are red at baseline on this tree (B12: all
judged ships lost mid-flight; B14: 60 s timeout) and cannot judge anything.
