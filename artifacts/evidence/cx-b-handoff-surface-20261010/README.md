# Step 3: measured failure, not integrated qualification

Base `a838a284a27a6813434362cc2adfde946d2085db`, branch `wt/cx-b-handoff-surface`.
Only this worktree was changed. No commit or merge; gates and old evidence are untouched.

Retained: an exact reversible event/momentum chart map using the existing Lorentz shears,
checked half-turn overflow, a strict shared bound/half-Hill predicate and active P4/P5 probes.
The map and predicate are standalone; the runtime handoff remains the base implementation.
The rejected runtime retrofit is in `candidate.patch`; do not apply it as a qualified result.

P5 map: 12,000 exact round trips (1,000 at each of four directions and three speeds),
plus an independent axis-boost oracle and overflow controls; all six helper/control tests pass.
P5 runtime: all 3,000 round trips preserve coordinate words and the Ext register, but all
3,000 discard velocity carries and leave child event time unchanged. The test actively fails.

P4: 2/6 complete 2,000 periods (.5 prograde ratios 1.0482/1.1337; .9 prograde .9876/1.2259).
The other four actively fail at the 55-second watchdog; no 2,000-period claim for them.
See `p4.json` for every denominator, median, handoff count and timeout sample.
These are phase-zero circular seeds at .3/.5/.9 Hill, both directions, default step 7.
Regularity is not independently qualified; especially .9 prograde must not be treated as
an established stable satellite merely because the Jacobi-error check passes.

Rejected retrofit: .5 retrograde ratio 15.49 and .9 retrograde 7.24 at 200 periods;
.5 prograde reaches 2,000 but ratio 1.32197 fails. The other runs time out or lose the ship.
Its runtime P5 discards Ext on all 3,000 round trips (`candidate3-p5-runtime.log`).
Candidate source was archived after the trials; no exact binary/source replay identity claim.

Diagnosis: Ext is minus Kepler energy and stored velocity is coordinate velocity. They are
not total relativistic energy/momentum. Boosting `(-pt,v)` fails the comoving-rest control
at every requested speed; boosting actual four-momentum passes with the same shears.
Persistent extended chart events, carry transformation and root-clock event keys remain
unbuilt. Retrofitting a radius into the current shared-tick scheduler does not resolve them.
This rejects that configuration, not the single-surface method.

`gates.txt` contains every literal before/after detail, including failures. B17 default
times out; the separately labelled existing step-4 operating point passes both ways.
G gates use `--law space`; B gates use `--law plane`. Default is step 7.
Raw logs include commands, machine state and measured RSS where available. Baseline G's
sandbox resource wrapper errored after the gate PASS; unavailable baseline state is not inferred.
Final runs are on battery with concurrent jobs and swap/load recorded; no thermal warnings
were recorded. The monitor kills any sampled process at 2 GiB; this is sampled RSS, not an OS cap.
New tests execute separately under 58 seconds (P4 has a 55-second watchdog); frozen B14/B17
retain their own 60-second limit. Build durations are separate from test execution.

Reproduce: `cargo test --release -p emergent-universe --tests --no-run`, then run each listed
binary/test through `python3 run.py 58 LOG BINARY TEST --exact --nocapture`.
The full test suite is deliberately red because the qualification probes are active.

Existing regressions: 10 unit and 44 integration tests pass; 1 pre-existing test remains ignored.
Every integration case was executed separately with the 58-second/RSS monitor.
Maximum recorded process RSS across these archived monitored runs: 1.097 GiB.
