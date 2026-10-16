topic: nladder
status: open
closed-by:
valid-while:
updated: 20261016-0117-library-cfe5

# The N ladder: 28 live bodies toward 10⁹

## Current best

**The plan pass's interior is attributed, and it is not an irreducible exact search: 30% of the
birth pass is the planets' exact states re-derived once per body (deleted digest-identically by a
birth-only hoist, 32.4–33.5 → 22.8–23.2 µs/body), the terminal bisection is 0.1% of it, and the
largest term is the per-body clock derivation (`constants`+`project`, 15.4–16.0 µs/body) — with
the SAME planet reads happening a second time through `ext::constants`' `source()` (20261016-0117-library-cfe5,
library lens, shipped code + `ES_BIRTH_SPLIT` counters and an `ES_SEC_HOIST` memo armed only inside
`Universe::start`).** Belt at 10⁴/10⁵ × seeds 1/7 (7 never flown by the author before predicting):
pass 32.40–33.49 µs/body (reproduces 404b's 32.5–33.5 flat in N), secondaries compute 9.75–10.23
µs/body = 30.1–30.6%, exactly one `secondaries` call per body (n+28 calls; the memo serves 10⁵
bodies from 7 entries), `plan_terminal` 0.03 µs/body, digests identical on all 8 flights. The
remainder (~17 µs unattributed) includes a second planet-reread path — code-verified (ext.rs:133,
called once per clock body from `plan_clock`) but untimed: its µs share is inference until the
next rung's timer says so. Consequences: (1) the "irreducible exact search" reading of the pass is
dead — the exact searches (terminal, exits) are free at birth; the bill is shared-state
recomputation plus per-body clock math; (2) one shared "planets at t" readout serving both paths
is the named next rung (predicted pass ≲ 13 µs/body,
amortizing the same structure at every wave-front pass); (3) at 10⁹ the hoisted pass alone deletes
~2.8 core-hours of 404b's ~6 (lab-box orders).

**[Prior best retained — see lab/wiki/nladder.md's standing text: 404b's birth-rail split, the
scout's last-segment floor, the depth axis (398f/57ec), the seam/retention family (e0f9, 0757,
b0ed, quant-0619, f55d), 8b89's ES_LAZY_ALL, b172's formation falsifier, 1343/3dc8's passage
pricing). This proposal folds the plan-pass attribution in; the merge resolves against whatever
side of the page's conflict stands.]**

*[Checker (silver): reproduced from a clean tree — every digest bit-identical to the runner's
regen and across both hoist arms on my own 8-flight grid (pass 33.7–33.9, secondaries 10.2–10.4 =
30.2–30.5%, hoist-on 22.9–23.6, `sec_calls` = n+28, 7 memo keys). Beyond the author's domain:
held-out seed 3 holds at 10⁴/10⁵ (30.2/30.3%); 3×10⁵ holds flat (30.4%, digest-identical, RSS
688 MB); at 10³ the share dips to 26.7% — "30%" is honest for 10⁴–3×10⁵, not a constant of the
ladder. Prediction 1 failed as the dossier reports (30%, not >50%), so the pass's largest term
(the clock derivation) is attributed by arithmetic, not a timer. All five library quotes verified
verbatim in work/library.json with correct authors.]*

## Refuted

- **"The plan pass's interior may be one irreducible exact search per body" (the open direction's
  first horn):** the searches are 0.1% of the pass at birth; 30% is per-body recomputation of
  per-tick shared state (the planets' readouts), digest-identically deletable (20261016-0117-library-cfe5).

## Open directions

1. **One shared "planets at t" readout for both read paths** (`Ctx::secondaries` and
   `ext::constants`' `source`), birth-first then at every shared-tick pass: predicted pass ≲13
   µs/body; then perf the remainder (kepler/field scalar chains vs reads) — that is the true
   floor candidate of birth-on-the-shipped-law.
2. (prior directions stand: the M1 re-measure of plan/add, the compact store, the cadence law,
   the comet class, and the page's standing conflicts for the integrator)

## Contradictions

- (the page's standing conflicts are the integrator's to resolve; this run's sections are
  additive and side with neither)

## Runs

- 20261016-0117-library-cfe5 (this run): the plan pass attributed — secondaries 30% of birth
  (hoisted digest-identically −29.5%), terminal 0.1%, clock derivation the bulk; a second planet
  reread in `ext::constants`; five library lessons, two flown.
