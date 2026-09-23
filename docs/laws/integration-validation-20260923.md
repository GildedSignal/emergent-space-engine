# Integration validation continuation — 23 September 2026

The recovered Cursor baseline is `e510b2f`. Work continues in
`/Users/julien_laurent/Research/emergent-integration` on
`codex/integration-continuation-20260923`. Temporary worktree files disappeared;
Git retained the committed integration. The dirty Documents checkout was not
merged or changed. No uncommitted temporary work is claimed recovered.

The pressure rung now passes its existing correctness condition. Full-engine
qualification remains incomplete; `production_law` remains null. The former
three-body, fleet, and reused physical-law held-out PASS rows now report
UNSUPPORTED because their claimed behavior was not measured.

## Implemented and tested

- The pressure reference previously omitted family identities, included tick 0,
  and used rising overlap instead of the documented trajectory-revision contact
  rule. The corrected reference reconstructs affine family history from genesis
  and range inputs and uses independent rational swept-contact and light-cone
  predicates. All **471** contacts in the original case agree. Signal identity
  is retained, so a missing one of two simultaneous arrivals is detectable.
- The ten oracle regression tests cover twelve genuinely varied inertial ICs
  (positions, spacing, velocities) against both compressed and materialized
  families; contact-stop and individual-burn ordering; between-tick contact;
  excluded left-edge tangency; missing contact/signal records; genesis overlap;
  family range-history reconstruction; and explicit resource/unsupported refusal.
- RK2 used an already-updated velocity in its position update. Restoring Heun
  ordering passes the predeclared second-order test: step-halving error ratios
  3–5 at 16/32/64 steps, with RK4 2048/4096 reference uncertainty below 1% of
  the finest RK2 error. Three rotations check coordinate consistency. Restoring
  the old code makes the same test fail with ratio **1.99913**. This validates
  numerical order under shared equations, not an independently validated law.
- The I6 test now writes a new output file (optional `I6_MATRIX_OUTPUT`) with
  `create_new`, never the historical September 15 matrix. Existing evidence
  cannot silently be overwritten.

## Actual results

[Source hashes and scope](../../artifacts/evidence/integration-validation-20260923/provenance.json),
[engine log](../../artifacts/evidence/integration-validation-20260923/final-engine-tests.txt),
[compact log](../../artifacts/evidence/integration-validation-20260923/final-compact-tests.txt),
[old-code negative control](../../artifacts/evidence/integration-validation-20260923/rk2-mutation.txt),
[original oracle failure](../../artifacts/evidence/integration-validation-20260923/oracle-before.txt),
[new matrix](../../artifacts/evidence/integration-validation-20260923/i6-matrix.json).

Commands used `CARGO_BUILD_JOBS=1`, the shared
`CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/full-engine-integration-target`,
and `--offline --locked`:

```
cargo test -p emergent-engine --lib --test oracle_pressure --test i1_increment2_authority --test i6_qualification --offline --locked -- --test-threads=1 --nocapture
cargo test -p emergent-law-lab --lib i4_moving_compact --offline --locked -- --nocapture
cargo xtask history check
```

Engine: **48 passed** (31 library, 6 I1 authority, 1 I6, 10 oracle).
Compact: **3 passed**. Old-order mutation: expected FAIL.
Single debug matrix measurement: pressure wall **31.657 s**, audit **29.940 s**,
advance **0.854 s**, reconstruction **0.840 s**, 217 yields. The pressure digest
is unchanged from H0148. This is improved coverage/correctness, **not a speedup**.
No rendering, release-performance, large-envelope or billion-identity claim.

## Limits and next implementation

The contact/cone reference audits committed trajectories and emissions; it does
not independently evolve the world or detect an emission that was never created.
Phase-family history, phase-burn provenance, and ambiguous overlapping same-tick
range burns explicitly refuse. Materialization is capped at 4096 identities;
combined pair/event tick-work is capped at 5 million. The reference is a bounded
small-world audit, not a production query path or gravitational authority.

The physical held-out bank is still missing. Next implement actual varied
moving-source cases with independently derived physical anchors, declared
outcome classes and numerical refinement; replace the solar classifier that
calls a system bound from minimum separation over a short window. Preserve
shared-input compiler equivalence separately. Do not require every physical
seed to produce the same trajectory or remain bound.

I1 still lacks canonical gravity commits through the integrated authority path.
I4 comparable-mass strong-field behavior and the frozen target envelope remain
unsupported. Failed galaxy quadrupole evidence remains unchanged; do not retry
that rejected representation or relabel direct sums as a skip.

History continuity is already broken in the recovered baseline: **116** distinct
referenced paths are absent. `cargo xtask history check` fails first at
`../crates/law-lab/src/causal_kernel.rs`.
[Failure](../../artifacts/evidence/integration-validation-20260923/history-precheck.txt)
and [inventory](../../artifacts/evidence/integration-validation-20260923/missing-history-paths.json)
are retained. Recover authentic files from backups; no historical record was
rewritten, no replacement evidence fabricated, and the checker was not weakened.
