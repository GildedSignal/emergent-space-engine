# I3 osculating Kepler evidence — 15 September 2026

Not canonical gravity. `CANONICAL_GRAVITY_ACCEPTANCE = diagnostic-only`. `production_law` null.
Not I3 exit. Not I4–I6. Nested Charge `ledger_total` is the denominator.
Gates declared before this slice’s runs: `OSC_POS_BAND = 0.20` (5% of circular `a=4`). H0132 accel-fit band 0.05 was **not** widened.

## What ran

Worktree `/private/tmp/emergent-full-engine-integration`, branch `codex/full-engine-integration`, parent `0b72990`. Target `/Users/julien_laurent/.cache/emergent-space/full-engine-integration-target`. `CARGO_BUILD_JOBS=1`, `--offline --locked`, `--test-threads=1`.

| Command | Result |
|---|---|
| `cargo test -p emergent-law-lab --lib i3_ -- --test-threads=1` | PASS (7) |
| `cargo test -p emergent-law-lab --lib coupled_ -- --test-threads=1` | PASS (54) |

## Method

`compile_osculating_response`: Kepler-advance to the next knot, retarded GEM lookback on the osculating history, Δv = (GEM−Newton) Δt, refit elements. Knot cadence `OSC_DT = 0.25` (half the circular-pair light crossing), not collocation `dt = 1/32`. Positions would have come from Kepler(elements(t)), not a post-pass residual. Construction does not call `interval_compile`.

## Result: REJECT

| Case | Outcome |
|---|---|
| Circular `a=4` H=4 | Refused: `e=0.886 > 0.85` (a drifted to 18.47). Collocation ledger **1551** (se 30, ret 618) |
| Circular `a=4` H=6 | Same refuse at the same e. Collocation ledger **2057** (se 46, ret 775) |
| Eccentric H=6 | Refused `e=0.890` |
| Radial rest pair | Refused `e≈1` (close-encounter fixture still closed) |
| Resonance kicks / weak Δv=0.02 | Refused high-e; explicit fallback, not a guessed event |

`OSC_POS_BAND` was never reached: construction left the admitted Kepler domain. The 0.85 eccentricity refuse was **not** raised after seeing 0.886.

GEM−Newton on this pair is not a small osculating perturbation of Kepler (H0132 already measured peak residual 0.078 on a force ~0.125). Varying elements absorbs that difference as Δv and drives the ellipse through the close-encounter gate.

## I3 exit

Not proven. H0131/H0132 keeps unchanged (H≤3 collocation vs Euler; quiet-kick prefix-repair; lazy pair-inverse without Schur consumer). Those are not skipped long-time GEM.

## Next representation

Do not use Kepler as the GEM two-body reference. Discriminating test: **low-rank / memory-kernel compression of the retarded Volterra collocation operator** (plan hypothesis “small boundary responses replace interior dynamics”), with construction that is not `interval_compile` over every `dt` knot, compared to collocation at H=4 and H=6 on this same circular pair. Failure if boundary rank/memory grows into a new dense fill-in or Δx misses a predeclared gate.
