# Same-genesis orbital reference experiment — frozen 24 September 2026

Numerical validation under the existing GEM model; no force-law change.
Load exact saved resolved genesis from H0151's orbit-duration-bank.json. No
re-shooting, zero new interventions, identical genesis-limited field history,
original one-period horizon. Initially seed10 (largest position error); then
seeds4/8/9/11. Retain every refused or failed rung.

Use existing Euler Reference, independent evolution from causal collocation,
sharing GEM field/retarded-root implementation. Thus this does not independently
validate those shared equations/routines. Genuine timesteps span/N for
N=1024,2048,4096 where span=period-genesis. Compare 1025 endpoint-inclusive
samples from observation t0 to period, including initial-state mismatch.

Report consecutive reference position differences/a, candidate/reference
position differences/a, Kepler position error/a, energy and angular momentum
errors, radial extent and signed angular coverage, plus returned work ledgers,
state-query counts and elapsed wall. Failed calls lack partial ledger counters;
flag that rather than claiming complete accounting. Do not reinitialize at t0.

Numerical screening: finest consecutive reference difference <=0.005a and
fine/coarse difference ratio <=0.75 (unless both differences <=1e-10a).
This is observed refinement, not an error certificate. Candidate agreement
requires <=0.02a. Existing physical bands remain 0.05 and angular coverage
>=2pi-0.05. If screening fails, do not attribute discrepancy to the model.
Further resolution needs an explicit appended resource/outcome decision.

## Resource decision after initial seed10 probe

N=1024/2048/4096 measured, but consecutive differences 0.78405 and
0.51968 fail the 0.005 screen. Reference evolution costs 0.018/0.036/0.077s
in this debug probe. Extend to N=8192/16384/32768/65536 without changing
thresholds or genesis. Record t0 mismatch explicitly. These results cannot
yet discriminate model error.

## Resource decision after 65536 steps

Seed10 differences shrink approximately first order (0.1871, 0.1008, 0.0523),
but remain above 0.005. N=65536 takes 5.43s debug. Extend this seed through
131072,262144,524288,1048576 in release profile, keeping a 65536-step overlap
to check profile agreement. Cap this ladder at 1048576 steps; no model verdict
if it still fails. Then use the same ladder for the other four failed seeds.
Retained history/field scans make cost grow faster than step count; these are
charged reference costs, not a production optimization claim.

## Compiler refinement freeze

Seed10 now passes positional screening at N=1048576 (difference 0.003391,
ratio 0.4297). Compiler/reference position disagreement is 0.009006; the
reference Kepler error remains 0.398744. Debug/release N65536 samples match.
Next use real causal-cadence subdivisions 1,2,4,8, same saved genesis and
horizon. Record interval counts, charges, successive position differences,
reference disagreement and all existing physical metrics. Default compiler
remains factor1; there is no automatic production change. The position
screen does not qualify velocity-derived invariants as converged.

For the remaining four seeds, start the already-declared release ladder with
65536/131072/262144. Stop if the frozen positional screen passes; otherwise
continue its declared doubling levels through the same 1048576 cap. This
stopping rule only controls reference cost, never removal of failed cases.

## Pre-fix causal refinement and falsifier

Seed10 factors1/2/4/8 produce 1288/2578/5156/10314 interval functions;
reference position differences grow .009006/.018641/.023233/.025553.
Successive compiler differences shrink .009635/.004592/.002321. Do not
interpret the factor1 agreement as agreement between limiting methods.

A concrete constant-acceleration root counterexample was then identified:
source interval [0,1], x0=(0,0), v0=(0,0), a=(-2,0), c=8;
receiver event t=2, x=(7.0999,0) has exact retarded source time .99.
The old routine's inertial seed and midpoint fallback both start outside the
interval and it returns None before Newton can reach the valid root. Fix this
numerical omission with safeguarded interval root finding; test interior,
endpoint and absent-root cases. Repeat factor1/2/4/8 against the SAME saved
reference/genesis. No initializer rerun; preserve pre-fix evidence.

The remaining Euler cases 8/9/11 fail screening at 262144 steps, and continue
the declared ladder to 1048576. Seed4 passes positional screening at 262144.

## Retained result

**Numerical validation remains incomplete.** All five Euler ladders pass the
frozen positional screen; all five still fail the original orbital behavior
checks. Refined causal blocks disagree with the finest Euler positions beyond
0.02a for seeds8 and10. Therefore no new physical model verdict or promotion.

| Seed | Reference steps | Finest reference change/a | Factor8 compiler/reference difference/a | Reference Kepler position error/a |
|---|---:|---:|---:|---:|
| 4 | 262144 | 0.003113 | 0.003214 | 0.048685 |
| 8 | 1048576 | 0.003625 | 0.037595 | 0.260854 |
| 9 | 1048576 | 0.003164 | 0.006099 | 0.057296 |
| 10 | 1048576 | 0.003391 | 0.025553 | 0.398744 |
| 11 | 1048576 | 0.003490 | 0.005275 | 0.093413 |

The guarded retarded-root fix passes its constructed counterexample and
interior/endpoint/no-root tests. Restoring the old function makes that exact
regression fail with None. However corrected seed10 trajectories differ from
pre-fix results only at rounding scale: this real bug does not explain the
orbital-bank mismatch. Root residual evaluations are now charged as verification.

The initial full law-suite run exposed a historical absolute operation-count
pin (1188 expected,1123 measured). Frozen evidence is unchanged. The live test
now compares source work to the matched current full compile instead of requiring
historical counts, while retaining all exact reuse/repair trajectory checks.
This is not a total-cost speedup claim and no physical band was changed.

Next isolate the earliest divergence between the two numerical paths during
the genesis-to-observation transient for seeds8/10. Record position AND velocity,
compare fields on matched source histories, and check source turn-on handling.
Do not re-shoot initial conditions to conceal it. Only after this discrepancy
is resolved should model/initialization assumptions be judged from the bank.

Evidence: [summary](../../artifacts/evidence/orbit-reference-20260924/summary.json)
and [raw runs/provenance](../../artifacts/evidence/orbit-reference-20260924).
Raw JSON is gzip-compressed losslessly; provenance records original hashes.
