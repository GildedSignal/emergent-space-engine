# Observation-start shooting initializer — freeze before measurement

Version `kepler-observation-shoot-v1`, same GEM equations, separately identified
initialization. Keep all original `kepler-genesis-v0` bank results and thresholds.
The existing six parameter sets at two compactness levels are unchanged.

Requested state: analytic Kepler barycentric position and velocity at t=0.
Unknowns: each body's position/velocity at existing negative genesis. Compile
all the way through the original horizon on every trial; compare the compiled
state at t=0, then update genesis velocity by minus velocity error and genesis
position by minus position error plus elapsed-prehistory times velocity error.
This is a shooting solve, not a state overwrite at t=0 or authored source future.

Before measuring: at most **8** complete compile trials; success requires every
body's position error/a and velocity error/sqrt(G M/a) <= **1e-8**. Otherwise
explicit UNSUPPORTED with all attempts charged; no looser retry. Return the
successful compiled history, avoiding an uncharged repeat compile. Record all
returned compile ledgers, attempt count, residual, resolved genesis and wall.
An internal failed API call does not expose partial counters; report that gap,
never pretend its work was zero. This is offline initialization, not yet a
WorkBudget-resumable engine job or production-law admission.

Run the unchanged physical/numerical bands on the initialized cases separately.
The ballistic negative control uses the same corrected genesis state. The
physical anchor remains the requested orbit, not a trajectory fitted after the
result. Original four FAILs are not deleted or reclassified. This can establish
finite-arc initialization support; it cannot establish full-orbit stability,
canonical gravity, arbitrary many-body initialization, or strong-field behavior.

## Newton variant freeze — before execution

Fixed-point v1 measured 10 supported cases and two UNSUPPORTED cases (seeds 8,
10 exhaust eight trials). Preserve that result. `kepler-observation-newton-v1`
uses the same IC bank, requested state, equations and residual tolerance, with a
separately charged 8D finite-difference Newton solve. Unknowns are scaled by a
for position and sqrt(GM/a) for velocity. Forward Jacobian increment 1e-6;
pivoted linear solve refuses pivots smaller than 1e-10. At most eight Newton
updates and **100 complete compile evaluations**, including Jacobian probes and
rejected line-search proposals. Line search tries alpha=1,1/2,1/4,1/8 and requires
strict residual reduction. No threshold widening. This is not the eight-compile
budget of fixed-point v1; compare full costs separately.

Check the returned history's genesis against the report, independently recompute
its observation-start error, and feed its IC through Engine's WorkBudget-driven
compiler. Do not splice desired positions into the evolved world at t=0.

## Measured results

Original declared bank: **8 PASS / 4 FAIL** (seeds 4,6,8,10). Numerical bands
pass on all 12. The high-eccentricity failures start observation with velocity
offsets up to 12.6%, whereas measured ongoing force differences from Newtonian
acceleration stay below 0.6%. This supports initialization as a contributor;
it does not independently establish the full GEM equations.

Fixed-point initializer: **10 PASS / 2 UNSUPPORTED**. Seeds 8 and 10 exhaust the
frozen eight compiles at residuals 4.67e-7 and 3.00e-7, above 1e-8. Not retuned.

Newton initializer: **12 PASS**, with 19 or 28 complete compilation evaluations
per seed, including derivative probes. Worst measured normalized position error
is about 0.00546 over the original finite arc; each per-body initial residual
is below 1e-8. Across the bank, total compile ledger is 1,254,312 returned units;
total case wall time was 5.79 s in one debug run. These units are not uniform
arithmetic operations and the initializer is not yet a cooperative runtime job.

Three seeds (0,8,10) pass through the real Engine compiler with budgets 1 and
256. Their source interval functions are identical to the accepted initialization
history; every run pauses/resumes and the desired t=0 state is recovered.
No canonical gravitational event or full orbit is thereby qualified.

All 102 law-library tests and both engine integration tests (matrix and seeded
budgeted compilation) passed. `cargo xtask history check` retains the inherited
missing-file failure described by H0149.

New evidence, with old outcomes retained:
[provenance](../../artifacts/evidence/orbit-initialization-20260923/provenance.json),
[original bank](../../artifacts/evidence/orbit-initialization-20260923/two-body-bank.json),
[startup diagnostics](../../artifacts/evidence/orbit-initialization-20260923/two-body-diagnostics.json),
[fixed-point bank](../../artifacts/evidence/orbit-initialization-20260923/initialized-bank.json),
[Newton bank](../../artifacts/evidence/orbit-initialization-20260923/newton-bank.json),
[I6 matrix](../../artifacts/evidence/orbit-initialization-20260923/i6-initialized-matrix.json),
[law tests](../../artifacts/evidence/orbit-initialization-20260923/behavior-law-suite.txt),
[engine tests](../../artifacts/evidence/orbit-initialization-20260923/initialized-engine-suite.txt).

I6's solar, three-body and galaxy-dynamics cards now explicitly remain
UNSUPPORTED: a field bound, an existing inertial asteroid, and direct field sums
respectively do not establish the behaviors described on those cards. Actual
small-field/numerical measurements remain in their separate rows. Solar reports
sampled radius 6.266–6.793 and angular coverage 0.648 rad over H=4, with actual
compiled velocities and sampled Newtonian energy; sustained boundedness is
UNSUPPORTED. The escaping-radius negative test catches the old minimum-only
classifier's false positive.
