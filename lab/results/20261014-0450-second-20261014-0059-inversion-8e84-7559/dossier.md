# Dossier — the named experiment: the shipped suites do not bite where the replay gate is dark

## Claim

The second checker's named experiment is done, and its "total" branch holds: **neither the
universe and lattice test suites nor the xtask suite kills M-kick or M-prune — the two
mutants that leave the replay gate printing `same` on a fresh corpus are guarded nowhere
in `cargo test`** — while the same panel's positive control (M-wrap) dies in the lattice's
own `hit_is_exact_past_the_i128_products`, so the suites have teeth where the gate is
dark and the passes mean "guarded nowhere", not "instrument broken". The parent run's
premise-wrong result (the merge protocol has no machine contract for law regressions) is
therefore total for these two mutants: adoption stops being a judgement call. The one
instrument left that could bite them, `behave --law plane`, is not run by any test and
cannot be adjudicated off the M1 (it fails on the clean tree on the lab's shared box).

## Bottleneck

Truth-instrument, not frame-cost (PRINCIPLES: "a test that cannot fail is a control").
The parent run (20261014-0059-inversion-8e84, silver) measured the replay gate's mesh;
check2 named the missing experiment: "run M-kick and M-prune against the shipped test
suites… If neither suite kills them, the two dark mutants are guarded nowhere and the
premise-wrong result is total". This run does that, plus the two arms check2 could not
have named: xtask's own unit tests (the only other crate whose tests reach the mutated
code) and `behave --law plane` (the gates that judge the engine itself).

## Evidence

Tree: main 8498d1c8 (crates identical to the parent's 33c83f1a; only `lab/wiki`
differs). Mutants: the parent's line-exact edits — M-kick `step.rs:440`
(`Kick.len >> (2·level+1)`), M-prune `universe.rs:1105` (margin `1<<26`→`1<<20`),
M-wrap `law.rs:337` (the 13-October contact fix reverted). Protocol: `git checkout` +
`touch` (the parent's mtime-rlib lesson). All numbers regenerate with
`bash lab/results/20261014-0450-second-20261014-0059-inversion-8e84-7559/regen.sh`
(warm ~8–10 min; every command ≤ 60 s except the crate builds).

**Arm 1 — the named experiment** (`cargo test --release --locked --offline
-p emergent-universe -p emergent-lattice`, 23 test binaries: both crates' lib tests,
all 16 universe integration files, both crates' doc-tests; `panel-logs/`):

| arm | passed | failed | ignored |
|---|---|---|---|
| baseline (clean) | 91 | 0 | 3 |
| **M-wrap** (control) | 3 | **1** | 0 |
| **M-kick** | 91 | **0** | 3 |
| **M-prune** | 91 | **0** | 3 |
| restore | 91 | 0 | 3 |

M-wrap dies at `law::tests::hit_is_exact_past_the_i128_products` (assertion at
`law.rs:711`: d [157, 106] w [20, 22] reach 32 scaled by 2^61 — left true, right
false); cargo's fail-fast stopped the remaining binaries, which is why the row counts
4 tests. The 3 ignored: a minutes-long γ-clock run (`clock.rs:154`), the frozen-broken
T1 harness, and a known-chaos failure whose ensemble version runs and passes. The
ramp-reading tests ran and passed under M-kick: `the_readout_between_kicks_is_bounded`,
`the_readout_between_kicks_reads_the_boundarys_error`,
`the_readout_at_a_boundary_is_the_state_bit_for_bit…`,
`the_readout_error_falls_as_the_step_squared`.

**Why M-kick is suite-dark (the mechanism, new this run).** Since 7 October the
running readout tests judge through `observe::partial` (their own note: "the ramp: up
to 39x, and ignored"), and inside its validity window the partial step's value is
*independent of `Kick.len`*: its Δv is recomputed from the field
(`field.accel · τ`), and `len` only bounds the window `τ ≤ 2·len`; the tests read
mid-interval, inside the halved window. The `credit` ramp — whose shape genuinely uses
`len` (`s = (t−m−len/2)/len` over `[m, m+len)`) — has no running test. So M-kick is
dark on all three instruments for complementary reasons: digest construction (the
gate: `b.kick` never hashed), mid-window partial reads (the suites), and not being run
at all (behave plane).

**Arm 2 — xtask's suite** (`cargo test -p xtask`, 227 tests; `xtask-logs/`). The
clean tree on this shared box has 7 pre-existing failures (5 `handoff` tests,
`events_tests::echo…`, `plane::tests::across_a_kick…`) — identical in the baseline,
M-kick and restore arms, so the mutant verdict reads on *failure-set equality*:
M-kick adds none. M-prune's parallel run added 2 (`behave::tests::each_planted_law…`,
`the_other_gates_can_fail_too`), but both are the **B10 timing gate** (`["G5","B10"]`
against `["G5"]`): planted laws run the behave harness's own steppers and never enter
`universe.rs`, so the margin is causally unreachable; run serially under M-prune the
two pass (7/7, `serial-logs.txt`), same as clean — load flakes, not kills. The one
test that reads across kicks, `across_a_kick_the_register_and_the_angular_momentum…`,
produces **bit-identical values in all four arms** (1.0 / 3.0 / 1.0 / 24.4 quanta):
M-kick does not move it, and its ship-3 failure is pre-existing and deterministic on
this x86 box (a lead for the integrator, below).

**Arm 3 — `behave --law plane`** (the frozen gates B12–B14, B17 that judge the
shipped engine; no test runs them — `behave_cli` uses echo/planted laws only). On this
box the **clean tree fails** (B12 "1 not converged, median exponent inf", B13 worst
2.12e-2 against 1e-2, B14 "60.0 s over the 60 s limit", and every non-applicable gate
"unanswered" by design — the plane law answers only restricted-problem questions),
so it cannot adjudicate the mutants here; `behave-logs/` holds the four runs
(baseline, both mutants, restore — all exit 1). This is the one instrument only the
integrator's M1 can run.

**Liveness control** (an all-pass mutant arm could mean the mutation never compiled
in): the freshly built `libemergent_universe` rlib fingerprint differs between clean
and each mutant build (`liveness-check.txt` / `regen-logs/` regenerates it), and the
M-wrap arm's failure is itself positive evidence the protocol compiles mutations in.

## Predictions

`predictions.md` was written before any run. P1 held (the universe suite does not
kill M-kick, 0.55; the motion readout tests were the named risk and passed — the
mechanism above is the post-hoc reason). P2 held (M-prune survives, 0.8 — pending
resolutions pin history, as predicted). P3 held exactly (baseline 91/0/3; M-wrap
killed by the lattice's own test; restore equals baseline). P4 was conditional on
M-kick dying, so it resolved vacuously — but its substance (only ramp-readers could
die) is confirmed: the one across-kick reader is bit-unmoved. Not predicted: the 7
pre-existing xtask failures on this box and the B10 parallel flakes — both
diagnosed with controls above.

## What would make it wrong

The suites are measured on one box (shared 8-vCPU x86, release mode, the shipped
`--locked --offline` invocation); a machine-dependent pass is possible for the 7
pre-existing xtask failures but not for the 91-test universe+lattice arms (physics
and digest asserts, 0 timing gates among them — B10 belongs to xtask's behave tests).
`behave --law plane` on the M1 remains unmeasured under both mutants: if it bites
there, the finding narrows to "guarded everywhere except the instrument nobody runs
automatically" — which still leaves the merge protocol without a machine contract,
since no test or pre-merge command invokes it. M-kick's verdict on the M1 also rests
on `across_a_kick…` passing there; here it fails clean with a deterministic
signature.

## Cost of adoption, fit with PRINCIPLES

Adoption is unchanged from the parent run (the small `replay.rs` patch: corpus
currency + exit 2 on `changed`), and this run removes its last judgement call: the
suites will not catch what the gate misses. PRINCIPLES: "write the kill criterion
before the run, with controls on both sides" — this run is that control for the
parent's panel; "a test that cannot fail is a control" — for M-kick and M-prune,
every automated instrument on the merge path is one. Lead for the integrator (free,
from the controls): `cargo test -p xtask` fails 7 tests on this x86 box with a
deterministic `across_a_kick` signature — worth one M1 rerun to know whether main's
own suite is red there too.

## The lens

The second-author lens: do exactly what the checker named, from the run's own
scripts, and report whether the claim then holds. It holds, on the total branch.
What the lens may have missed: machine-dependence of the xtask arm (controlled for,
not eliminated), and the possibility that a mutant other than the parent's six bites
the suites — the panel bounds *these* mutants, not the mesh of all possible law
slips.
