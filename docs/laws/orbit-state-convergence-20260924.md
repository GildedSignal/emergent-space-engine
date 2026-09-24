# Orbital state convergence — 24 September 2026

Baseline f93f25f. Extend the existing positional numerical screen uniformly to
velocity, Newtonian specific energy and signed angular momentum. Compare paired
samples, not just extrema: cancellation in aggregate errors cannot qualify a run.
Use scales a, sqrt(GM/a), GM/(2a), sqrt(GMa(1-e²)), respectively.

For each observable, require the finest successive Euler change <=0.005 and a
fine/coarse change ratio <=0.75 (or both changes <=1e-10). Compiler/reference
agreement requires a screened reference and difference <=0.02 in EVERY observable.
These are sampled numerical agreement gates, not conservation assertions: the
shared retarded-GEM model need not conserve Newtonian orbital invariants exactly.
Existing physical gates remain unchanged. H0154 velocity diagnostics were already
seen; this uniform extension is retrospective screening, not held-out evidence.
Freeze these limits before executing the new energy/angular-momentum audit.

Reject absent/invalid samples, unequal sample grids, nonfinite quantities,
nonpositive scales, mismatched genesis/case, unsuccessful or uncharged rungs,
and non-doubling Euler steps. Retained runs avoid repeating costly integrations;
report original integration charges separately from sample-comparison work.
Three final Euler rungs and compiler subdivision8 use identical initialized genesis.
No changes to laws, initial conditions, canonical event authority or production_law.

## Measured result

All five retained cases pass the energy and signed-angular-momentum reference
screens and compiler comparisons. Seed4 passes all four state gates. Seeds8/9/10/11
fail the velocity reference screen: finest changes are respectively
0.010106, 0.009850, 0.008256 and 0.010725 times sqrt(GM/a), above0.005.
Their compiler/reference velocity differences are below0.02, but agreement is
NOT qualified while the reference itself fails. Position screening remains PASS.
This is 1 PASS / 4 FAIL for the stricter numerical state audit, separate from
the unchanged physical bank7 PASS /5 FAIL.

The audit executes15,375 sample-pair comparisons across five cases. It performs
no new evolution; original integration and compiler charges are reported as
provenance, not recounted as current work or a performance claim. Raw input
archives stay immutable. Seed10's old report lacks optional work-breakdown
fields; the initial strict-schema read failed and is retained. The final reader
requires only fields actually used by the audit, without inventing counters.

115 law tests PASS,3 manual experiments ignored. New tests reject reversed
velocity despite identical position/energy, isolated bad samples, nonfinite
states, inadequate contraction and inconsistent reference metadata. Five CLI
controls reject changed genesis, missing samples, duplicate subdivision8,
incomplete charge and attempted output overwrite. All final measurements are
under `verified/` in the [evidence directory](../../artifacts/evidence/orbit-state-convergence-20260924).

Next extend Euler resolution beyond1048576 for seeds8/9/10/11 under the same
frozen geneses and gates, retaining and charging all additional rungs. If cost
requires accelerating reference history lookup, first prove equivalence against
the existing exhaustive lookup on adversarial histories. After state convergence,
audit shared force equations and initialization using independent physical anchors.
No physical-model or canonical-gravity promotion follows from this audit.
