# Full-orbit probe — frozen before execution

Use the already declared Newton observation-start initializer on the original
Case::from_seed(0) with its original 0.75 dynamical-time calibration horizon.
Then compile the identical resolved genesis through one Newtonian period.
Do not re-shoot or adjust the initial state for the longer demanded future.
Start with this circular case before widening workload.

At 1025 endpoint-inclusive times from t=0 to the period, compare to independent
analytic Kepler motion and record actual relative position/velocity. Frozen
physical screening bands: max position error/a <=0.05; max Newtonian relative
specific-energy and angular-momentum drift <=0.05 of their analytic invariants;
radial extent within a(1-e)-0.05a to a(1+e)+0.05a; signed angular coverage at
least 2pi-0.05. Refused compiler domains remain UNSUPPORTED, observed violations
FAIL. Sampled checks are not interval-wide certificates or perpetual stability.

Charge all initializer compiles and the full-horizon compile separately plus
complete wall time. No performance promotion. This probe is a prerequisite to
expanding duration/seed coverage, not permission to relabel the short arc.

## Bank expansion freeze

After seed 0 passed (position error/a 0.000669, total compile ledger 64765),
expand to all original seeds 0..11 with exactly the same one-period gates,
sample count and absolute timestep rule. Keep every case and its outcome.
Each initializer still resolves only its original short calibration horizon.
This expansion is declared before executing the bank.

## Refinement freeze after the retained bank

The bank yielded 7 PASS / 5 FAIL (seeds 4, 8, 9, 10, 11). Diagnose those
five with half the duration timestep, identical initialization and physical
gates. This is a numerical diagnostic; it does not replace the failed bank
or change the angular threshold. Record all outcomes before interpretation.

## Retained outcome

The full bank gives **7 PASS / 5 FAIL**. Seeds 4, 8, 9, 10 and 11 fail
the signed angular-coverage gate; seeds 8, 9, 10 and 11 also fail position.
All five retain energy and angular momentum within their frozen bands.
Short-arc PASS therefore does not establish full-orbit PASS.

The bank charged 1,639,446 compile ledger units across initialization and
duration compiles, with 1025 samples per case. The single debug run took
15.15 seconds summed over cases; this is no operating-envelope benchmark.

The attempted half-dt check reproduced identical trajectories and errors.
Inspection shows `compile_source_response_opts` passes dt to `seal_compiled`
as domain metadata, while `interval_compile` chooses causal blocks without
that argument. This experiment is **not numerical refinement evidence**.
Raw artifacts retain the original experimental field name; current code
corrects it to `metadata_dt_divisor`. Do not infer physical model error
from this ineffective control. A real causal-block refinement or independently
refined retarded-GEM trajectory comparison remains required.

The schema-3 I6 matrix includes all twelve duration reports and a separate
one-period gate, preserving every earlier finite-arc result. This diagnostic
is offline and does not establish canonical gravitational evolution.

Evidence: [retained run directory](../../artifacts/evidence/orbit-duration-20260923).
