# Dossier — 20261016-1740-taleb-a8cd (Taleb)

## Claim

Main's xtask suite is red on the lab box because its B12-family corpus is **libm-conditional**: the frozen 16 ships are re-assessed at every run by a chaotic float oracle seeded through non-correctly-rounded libm calls, and a different machine's last ulp moves both *which ships are judged* and *the value of every chaotic per-ship observable* — the law itself is bit-innocent (proved at the freeze commit), so this is silent cross-hardware nondeterminism of the *instrument*, not a regression.

## Bottleneck

Not a compute bottleneck: a **ruin-state bottleneck** (PRINCIPLES, Truth: "Canonical outcomes are exact and independent of … hardware. Floats never decide them"). Every GLM checker runs on this box; the xtask suite is the control behind half the wiki's "reproduced on shipped code" claims (replay-gate's direction 4 lead, 7559: "one M1 rerun decides machine-dependence vs a red main"). Gain: the M1 rerun is no longer needed — the mechanism is measured; and 7 of the 10 red tests are reclassified from "possible law regression" (integrator alarm) to "broken instrument" (fixable once, not chaseable per-failure). It deletes the ambiguity, not code.

## Evidence (all on this box, tree a523ace9 + work/patch.diff; regen: `bash lab/results/20261016-1740-taleb-a8cd/regen.sh`, core ≈ 6 min)

1. **The red set, today: 201 passed, 10 failed** (`cargo test -p xtask -j 6`, 523 s; REGEN_FULL=1). Seven are deterministic across ≥ 3 runs (suite, filtered rerun, probes — identical messages and values; 7559 saw the same 7 on 14 Oct): five `behave::handoff` tests, `events_tests::echo_passes_the_four_events…`, `plane::across_a_kick…`. Three are new and **flaky**: `the_other_gates_can_fail_too`, `each_planted_law_fails_exactly_its_gate`, `scale::echo_is_linear…` fail in the parallel suite, **pass** when rerun filtered minutes later (load class; the scale one dies in `Option::unwrap()` on the B10 judge's "never starts a run it cannot finish" refusal).
2. **The corpus drift**: this box's oracle reads the frozen 16 as `crossings [10, 8, 8, 14, 16, 30, 22, 22, 12, 34, 42, 8, 28, 12, 12, 22]` against the frozen "≥ 20 when frozen"; #88 passes at **0.271 planet radii** (inside), #138 unconverged → **14 of 16 judged**, and B12's own pass term `excluded ≤ 10%` reads 2 > 1.6 → **B12 fails for Echo** (`left: [("B11",true),("B12",false),…]]`). The freeze's design line — "A frozen ship whose reference now passes inside the planet (chaos moves with the last bit) is excluded… and counts toward the 10%" — is a per-machine budget, and the machine distance exceeds it.
3. **The ulp census** (probe `lab_corpus_ulp_libm_census`, 48 assesses): judged = **14/16 pristine, 11/16 at α+1 ulp, 8/16 at α−1 ulp**; per-ship (crossings, converged, closest) flip O(1) on nearly every ship (kept[0]: crossings 10→38→30, closest 59.5→4.16→**0.040 Rp**; kept[12]: unconverged→converged). One bit of one seed angle rewrites the corpus.
4. **Two real libms, one box**: glibc vs musl (`libm` crate) disagree on the seed calls themselves — sin/cos on 4 ships (#70, #83, #88, #138), `powf(r,−0.5)` on 2 (#83, #106) — and the musl corpus differs (**15/16 judged**, different members: #88 judged at 1.578 Rp, #106 inside at 0.030 Rp, #138 converged). mpmath at 80 digits: **glibc is correctly rounded on every flagged call — musl is the one off by ≥ 1 ulp** (`work/crcheck.py`), so real libms demonstrably disagree on these exact inputs; macOS's is a third implementation with its own error pattern.
5. **The failing ship's observable is a libm coin flip** (probe `lab_across_a_kick_ulp_stability`): #57 (the test's ship 3) reads **24.37 quanta, 8.409e-8 of its work** (bar 5e-8) pristine; **3.17 quanta, 4.563e-9** at all-components +1 ulp (passes); 2.84 quanta, 1.478e-7 at −1 ulp; kick count 7016→5423/5424. The bar sits *inside* the ulp-to-ulp scatter — no per-ship bound at 5e-8 can be machine-portable.
6. **The law is innocent** (history control): at the freeze commit **c84f5787** (6 Oct, xtask and crates as frozen) on this box, `across_a_kick` reads **bit-identically** — 7016 kicks, `across_kick 24.37109375`, `across_kick_over_work 8.409466703853747e-8`, ships 0–2 also identical to HEAD — so six days of merges (clock, contacts, range, nladder, skew) moved nothing in this walk. It failed here the day it was frozen and passed on the M1: machine, not main.

## Predictions

Written before the decisive runs (`predictions.md`): P1 failure anatomy ✓ (all seven deterministic failures flow through `kept()`'s oracle fields or oracle-selected ships); P2 the 24.4 ship ✓ exactly (24.37; filter keeps kept[0..3]; the channel is seed-ulp chaos of the observable, one level deeper than the predicted membership flip — reported as held with that amendment); P3 ulp flips ✓ (14→11→8); P4 two-libm corpus divergence ✓ (14 vs 15, different members; glibc CR, musl not); P5 determinism ✓ (three runs, identical). The kill criterion (corpora identical to frozen, no flips) did not fire.

## What would make it wrong

- The M1 rerun: if the M1 *also* reads 8.409e-8 on #57 and 14/16 judged, then macOS's libm bit-matches glibc on this chain and the red is real on main too (the census says this is a matter of ~6 seed bits; the mechanism — verdicts decided by libm bits — stands either way).
- The three flaky failures are load-class on my evidence (pass when filtered); a mechanism I did not isolate (test interaction vs wall budget) could hide a real regression there. Named, not chased.
- The musl arm understates the machine channel by design: the oracle's per-step `sin_cos` and `hypot` stay glibc in every arm, so the true cross-machine distance is larger than measured.

## Cost of adoption, and fit

Adoption is an instrument fix, one of: (a) freeze the *assessed* corpus (crossings/converged/closest) beside `HANDOFF_KEPT`, so membership stops being re-derived per machine — the gate keeps its physics, loses its libm; (b) derive seeds and oracle steps from CR-only ops (sqrt is IEEE-exact; `sin_cos`/`powf`/`cbrt` are not) — the honest long fix, matching the integer law's own standard; (c) mark the corpus-dependent tests `#[ignore]`-on-non-M1 so the lab stops reading them as regressions. Cost: (a) is a frozen-table patch to `kept()`; (c) is one attribute per test. PRINCIPLES: "Laws are versioned. Canonical outcomes are exact and independent of cache, partition, observation, schedule and **hardware**. **Floats never decide them**" — today floats decide the *gates'* verdicts, which is the same disease one layer up; and "a test that cannot fail is a control" — these tests can fail for the machine's sake alone, so on this box they certify nothing about the law.

## The lens

Taleb: I looked for ruin, not speed — and found the ruin is in the instrument, concave to one bit (fragility measured: 1 ulp → corpus 14→8, verdict flips both directions). What this lens may have made me miss: the three load-class failures got only a black-box classification (pass-alone/fail-together), and I did not price the fix's effect on gate throughput; the fermi/system lenses would.
