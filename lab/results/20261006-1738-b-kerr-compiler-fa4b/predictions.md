# predictions.md

Written before the decisive experiment: the frozen-seed gate run
`cargo run --release -p xtask -- behave --law space --gates B19` (plus the regression set
G1–G6, B16). What I have tuned on so far: the module's own tests (golden vectors from an
independent mpmath derivation, BPT closed forms, structural physics) — cases I chose myself,
not the gate's frozen seeds. The gate's seeds are drawn from `rotating.rs`'s frozen streams and
I have not run them yet.

## P1 — Criterion 1 (cycles)

All six cells (χ ∈ {0.5, 0.9, 0.998} × pro/retro, 256 seeds each, p log-uniform from 1.1×
separatrix to 1000, e < 0.7) pass: advance within 1e-2 and periods within 1e-3 for ≥ 99% of
each cell. Expected worst relative error ≤ 1e-5 (the trapezoid stops at 2^-34 ≈ 6e-11
agreement, and Scalar carries ~62 significant bits; the golden-vector tests measured ≤ 3e-9).

Risk I predict bites: seeds very close to 1.1×separatrix at χ = 0.998 prograde, where the
whirl makes Δφ large and the trapezoid may need > 2^14 panels (CYCLE_MAX); if the cap binds,
a few seeds' advance error could rise toward 1e-3 — still inside the 1e-2 tolerance. I predict
no cell drops below 254/256.

## P2 — Criterion 2 (fates, exact)

All five groups (circular, E=1 capture, bound/plunge, photons, dense capture) match the oracle
exactly: the classification is the same root-structure predicate evaluated at 2^-50 relative,
and the frozen seeds keep |x − 1| ≥ 0.01 margins. Predicted: 1680/1680. Risk: the dense
massive E=1 family near x = 1.01, where the quadratic discriminant sits closest to zero —
the margin 0.01 is still ~2^13 quanta of the discriminant's scale, so I predict no
misclassification.

## P3 — Criterion 3 (frame dragging)

All ~128 tubes per spin answered with dφ/dt > 0 (including L < 0) and rates within 1e-6;
static and ZAMO clocks outside the ergosphere within 1e-12 (closed forms at 62-bit precision —
the measured error against the golden ZAMO state was 1e-9-limited by my golden rounding, and
against exact closed forms 1e-15); no static clock inside. Predicted: full pass.

## P4 — Criterion 4 (Penrose)

Negative-energy tubes answered, forged ones refused (the refusal test has ≥ 2^-20 relative
margin, my tolerance accepts only ≥ −2^-44·scale); splits conserved within 8 ulps (measured:
≤ 3 truncation units ≈ 2^-60), energy gained inside, none outside, fragments within 1e-6 of
the oracle. Predicted: full pass.

## P5 — Criteria 5 and 6 (light; χ = 0 digest)

Light: 6/6 cells within 1e-2 (the deflection agrees with the 50-digit golden vectors to
≤ 5e-6 including the near-critical b = 2.3 = 1.09 b_c at χ = 0.998). χ = 0: the digest kinds
route through the law's own Schwarzschild methods with |b| and |L| mirrors, so the three
digests are equal by construction; predicted identical hashes, zero unanswered.

## P6 — Regression

G1–G6 and B16 pass exactly as before (the Schwarzschild path is untouched; the only shared
file changes are lib.rs's module list and the adapter's new method).

## P7 — Cost

The B19 phase finishes well inside its 60 s kill limit: I predict < 10 s on this 8-vCPU
runner (1536 cycle compiles at ≤ 2^14 panels each, 384 deflections at ≤ 2^11 GL16 panels,
~1700 cubic root solves at 120 bisections).

## What would falsify the build

- Any criterion-2 group wrong on more than isolated seeds: the root-structure predicate
  differs from the oracle's somewhere (most likely the E = 1 quadratic or the horizon
  comparison).
- A cell failing criterion 1 with errors of order 1 (not 1e-3): the (p, e) → (E, L) Newton
  diverged for that family (I fixed a missing 2aWE factor found this way; a second instance
  would show as a systematically wrong E at one spin).
- Criterion 6 differing: the routing misses a kind or a sign mirror.
