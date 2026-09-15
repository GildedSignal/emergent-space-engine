# Compact phase generator and navigation inversion (2026-09-14)

Implementation stays on `/private/tmp/emergent-coupled-response` (`codex/coupled-source-response` above `254ba1f`). Journal-home crates do **not** contain this overlay. H0103 is a **draft only** — not appended.

Law id `es-linearized-retarded-gem-response-v0`. `production_law` null. Default `Engine::advance` remains `es-inertial-causal-v1`. Not gravitational qualification.

## Compact stored response

Regular reference motion is a polar phase generator on each smooth piece:

\[
r(t)=r_0+\dot r\,(t-t_0),\qquad
\theta(t)=\theta_0+\omega(t-t_0),\qquad
\mathbf x_{\mathrm{ref}}=\mathbf x_{\mathrm{com}}+r(\cos\theta,\sin\theta).
\]

Corrections are a Chebyshev residual of admitted rank (default 16) on \(x-x_{\mathrm{ref}}\) and \(y-y_{\mathrm{ref}}\). Pieces split at committed interventions so a finite \(\Delta v\) kick is a knot, not a small residual of one global generator.

A single smooth generator of rank 2 on an interval that contains the laboratory kick exceeds the admitted band (Gibbs / insufficient basis). That is an honest refuse, not a missing-jet impossibility. Quiet two-body and the kicked A→B→A loop with splits reconstruct inside band \(10^{-4}\). Stored DOF is \(O(\mathrm{rank})\) per piece vs \(O(H/\Delta t)\) inertial kinks.

`compile_source_response` still also writes piecewise-inertial `worldtubes`. Compact is a fitted stored form used to reconstruct consumers; it does not yet replace compile storage.

## Navigation inversion

Partition the compiled ship map as \(q_1 = A q_0 + B p_0 + d_q\). \(B\) is the finite-difference STM \(\partial x_1/\partial v_0\) of `fly_ship` on the compiled GEM sources. When \(B\) is nonsingular, invert \(B p_0 = q_1-Aq_0-d_q\) by Newton.

Explicit failure domain (fail closed, no seed shopping):

- empty interval \(t_1\le t_0\): \(B=0\), the oscillator half-period identity
- query past compiled horizon
- speed beyond \(v_{\max}\)
- \(\lvert\det B\rvert < 10^{-8}\) (focusing / nonunique inverse)

Forward \(v_0\) on the kicked laboratory slice recovers by invert. That success is the inverse of a completed transport, not a hunted seed.

## Validation (worktree)

`CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/coupled-response-target CARGO_BUILD_JOBS=1 CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never`

- `cargo test -p emergent-law-lab coupled_ --offline -- --test-threads=1` — 29 passed; 0 failed (original 22 + 7 phase/nav).
- `cargo test -p emergent-observatory --no-default-features --lib --offline -- --test-threads=1` — 8 passed; 0 failed.
- Disk ~12 GiB free; swap ~4.7/6 GiB. No wgpu. No `qualify`. No commit.
