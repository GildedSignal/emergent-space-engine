# Five failed orbital cases — 24 September 2026

Baseline3b0f697. Keep exact H0151 geneses, current GEM equations, one-period
horizons, physical0.05 gates and H0155 state convergence gates unchanged.

Opt-in reference lookup: continuous subluminal Euler histories have monotone
source-start arrival times s+|x-X(s)|/c. Binary search gives a conservative upper
candidate index; original root/field routines still evaluate candidates in reverse
order. Default exhaustive reference and compiler are unchanged. Predicate work
is charged as verification. Only finite, unforced genesis is admitted. This is
floating laboratory lookup, not canonical branch authority.

Before use: compare fields exactly on101-segment bent paths at three receiver
positions and six offsets around every start arrival (1818 comparisons), including
before/at/after wavefronts. Compare complete2048-step histories across six varied
geneses. Both tests pass. Then require bitwise sample equality with archived
exhaustive full-period runs at matching resolution before accepting new finer rungs.

Run saved seeds8/9/10/11 at524288,1048576,2097152,4194304 steps, sequentially.
Seed4 already passes full-state screening; preserve it and diagnose physical
behavior together with the other four. A numerical PASS does not erase any
physical FAIL. Save every rung, source work, memory segment count, query count
and wall time. No speed/scale or GR promotion from lookup equivalence.

## Attribution control frozen before execution

After numerical state screening, evolve an independent Newtonian RK4 control
from the finest reference's EXACT relative position/velocity at observation t=0.
This deliberately compares different equations from the same observed state; it
neither changes nor re-shoots the retarded genesis. Use4096/8192 steps over the
same horizon, all1025 observation times, require all four state differences
<=1e-6. Validate RK4 against analytic Kepler on all five varied cases with
1024/2048 steps and >10x error reduction. Apply original physical gates to both
GEM and the same-state Newtonian control, without replacing either's verdict.
If the Newtonian control passes while GEM fails after full-state convergence,
initial observation mismatch alone cannot explain the failure.

GEM-v0 explicitly omits acceleration-dependent terms at kinks and specifies a
low-order Lorentz-like force. It is not a complete1PN GR model. Independent
context: [Mashhoon, section1.2 equations1.10–1.11](https://arxiv.org/pdf/gr-qc/0311030)
derives the simple Lorentz-like form under stationarity and low-velocity
assumptions. Numerical agreement between our two GEM implementations cannot
validate omitted terms. Do not change the versioned law to fit the Kepler gate.

## Separate initializer experiment freeze

All original five state screens now PASS. Same-observed-state Newtonian controls
PASS for4/9/11 but FAIL for8/10: initial mismatch is a contributor in two cases,
while GEM adds a larger separation in all five. Keep original evidence intact.

Introduce `kepler-observation-newton-block8-v2`: same targets, trial budgets,
Jacobian and tolerance1e-8, but evaluate the Newton map with causal subdivision8.
Do not alter existing initializer versions or patch observed states. Initialize
all five cases again as a separately named experiment; charge every trial. Run
new geneses at1048576/2097152/4194304 Euler steps and compare with subdivision8
full-period compiler samples, then repeat the same-state Newtonian control.
A change of genesis is NOT evidence of fixing the original same-genesis failures.
Do not claim physical PASS unless the unchanged actual physical checks pass.

## Results — completed25 September2026

All five ORIGINAL cases now pass position/velocity/energy/angular-momentum
numerical screening and compiler/reference agreement. Seeds8/9/10/11 have
4194304-step references; seed4 retains its already-passing262144-step reference.
All8200 overlapping sampled states at524288/1048576 are exactly equal to archived
exhaustive-reference samples. Extra indexing predicates are charged.

The separately versioned refined initializer converges for all five in19–28
charged evaluations, with maximum accepted residual4.52e-11. Each NEW genesis
has its own1048576/2097152/4194304 reference ladder and full-period compiler
subdivisions1/2/4/8. All five new full-state numerical screens/comparisons pass.
All five same-observed-state Newtonian controls now pass the ORIGINAL physical
gates (previously3/5), so the initializer contamination is removed in this
separate experiment. Worst control positional error is0.000432a.

| Seed | Original GEM position/a | Refined-initializer GEM position/a | New signed angle | Physical result |
|---|---:|---:|---:|---|
|4|0.048685|0.042407|6.222672|FAIL: angle|
|8|0.258200|0.201631|5.789567|FAIL: position and angle|
|9|0.054956|0.047116|6.165542|FAIL: angle|
|10|0.396290|0.355888|5.446204|FAIL: position and angle|
|11|0.090993|0.084253|6.073360|FAIL: position and angle|

GEM's five physical failures remain. Energy/angular momentum and radial ranges
stay within their physical bands in the new experiment. These are now resolved
numerical trajectories with corrected initialization, not proof that remaining
phase shifts are correct GR or that a correct relativistic model must match a
Kepler ellipse at finite compactness. Causal prehistory and omitted model terms
still require independent physical validation.

120 law tests pass; final public-classifier invalid-state regression also passes.
Four engine integration tests are recorded separately. Default reference,
canonical law and historical matrices are unchanged. The new initializer is an
opt-in laboratory API, not an Engine promotion. Diagnosis exit0 denotes completed
numerical/control resolution; each physical FAIL remains explicit in JSON.

Accounting limitation: the first seed8 ladder executed successfully but could
not save because cargo's test working directory made its relative output path
invalid. Its25.06s log remains; lost detailed counters make ALL-attempt cost
accounting incomplete. Accepted reruns retain full ledgers and samples. Failed
builds also remain. There is no total-cost speedup or target-envelope claim.
The seed4–11 runs were sequential on the same host. Default dt semantics were
not changed. Indexed lookup is limited to unforced, continuous Euler histories.

Next implement an independent weak-field relativistic benchmark with explicit
coordinate/order conventions and physical observables (including periapsis
advance and period); compare against the Newtonian limit and a static
Schwarzschild anchor. Then test GEM-v0 and its causal prehistory against that
benchmark before proposing a separately versioned force-law correction. Retain
these Kepler failures; do not tune the new law or relax the old bands to pass them.

[Machine-readable evidence](../../artifacts/evidence/orbit-refinement-20260924/summary.json)
and [all retained runs](../../artifacts/evidence/orbit-refinement-20260924).
