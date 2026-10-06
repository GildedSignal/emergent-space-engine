# B12's statistic red-teamed: the growth exponent is a level test, not a compounding test

**Claim.** B12's Jacobi growth exponent cannot measure compounding on chaotic ships — it fails the
judge's own reference at every tolerance (medians 1.23–1.81) and every bounded state-only plant
(0.28–0.40) while passing iid noise (0.16) and a time-periodic bounded error (0.06) — and no
single threshold-preserving statistic separates bounded from compounding (the harness's own leak,
a linear drift under a state-only oscillation, defeats pair-diff recurrence at 1.55 and the
cell-drift detector defeats walk-13 at 1.05), but two orthogonal memory probes together do:
pair-diff recurrence (cells 0.02 sep × 0.005 e, windows 4–16 / 64–200 P) ≤ 1.8 AND per-cell
early/late median drift ≤ 1.5 fails every compounding law that fails today and passes every
bounded state-only probe, with ≥ 27% margin on both sides.

**Bottleneck.** The motion law v2 is designed against B12 (HANDOFF: "B12 fails at exponent 1.41");
a miscalibrated gate wastes Astra's window. This run kills the exponent as the deciding statistic
and hands the integrator a frozen replacement with both controls measured. No threshold was
loosened: the 1e-4 cap, the 1e-12 floor, 16 ships, 20 crossings and the 10% exclusion budget are
untouched; the exponent ≤ 0.2 is replaced by the ratio ≤ 1.8.

## Evidence

All numbers on the 16 frozen ships (`sample::HANDOFF_KEPT`), 200 planet periods, P/8 samples.
Reproduce: `cd probe && cargo run --release` (≈2 s, writes `out/*.f64`), then `python3 stats.py`
and `python3 sstar.py` (≈1 min each) in this folder; the real gate: `xtask behave --law <name>
--gates B12` and `cargo test -p xtask the_recurrence_ratio_separates -- --ignored --nocapture`.

**1. The premise is false: the exponent reads level and noise, not compounding.**

| Law (my harness, 16 ships) | Median exponent | Gate today |
|---|---|---|
| raw reference rtol 1e-11 | 1.408 (worst err 7.8e-9) | FAIL |
| raw reference rtol 1e-12 | 1.229 (2.4e-9) | FAIL |
| raw reference rtol 1e-13 | 1.806 (1.1e-10) | FAIL |
| bounded-a 1e-7·(a−a₀)/(R_H/sep) | 0.277 | FAIL |
| bounded-e 1e-7·(e−e₀)/0.01 | 0.332 | FAIL |
| bounded-1/r₂ | 0.395 | FAIL |
| compound walk (1e-7/encounter) | 0.301 | FAIL |
| plane-like encounter jumps (bias +1e-6, rms 5.4e-6) | 0.599 | FAIL |
| leak 1e-12/P, drift 1e-9/P | 1.001 | FAIL |
| **iid noise at 1e-11** | **0.157** | **PASS** |
| **time-periodic bounded 1e-7·sin(2πt/100P)** | **0.057** | **PASS** |

The reference's own float64 rounding (worst err 1.1e-10 at rtol 1e-13, above the 1e-12 floor)
reads as near-linear growth. Above its floor the exponent fails *everything*, including three
bounded errors that never compound; below it nothing is judged. It is a level test with noise
amplification. The real gate agrees on this machine: `planted-drift` (= the reference at RTOL)
fails at median 1.355, `planted-bounded` 0.353, `planted-compound` 0.416 — and law.md's "ranks a
bounded error above a compounding one" did not reproduce here (0.353 < 0.416): the ordering is
itself machine-fragile. What fails is the separation, in both directions.

**2. The recurrence ratio separates, after repairing the grid.** Drafted in `handoff.rs`'s
ignored probe (cells 0.02 sep × 0.05 e, near 2–8 P, far 64–200 P, p90 of |Δ signed err| floored
at 1e-12): its own controls read 0.91–1.06 vs ≥ 1.25, but a bounded state-only error in **e**
reads **1.75** and in r₂ **1.34** — the cell (0.05) is coarser than the plant's e-gradient, and
any slow coordinate the grid under-resolves fakes memory (slow: correlated at 8 P, decorrelated
at 64 P; fast coordinates are innocent — near pairs already randomize them). Soft state-distance
matching (S*, `sstar.py`) makes it worse (bounded-a 2.90: matched balls do not equalize the
marginals, near pairs are always close in (a,e)). The repair is hard fine cells on the slow
coordinates:

**Frozen config A (pair-diff recurrence): cells (a/sep ÷ 0.02, e ÷ 0.005), far-field only
(r₂ > 3 R_H), near 4–16 P, far 64–200.1 P, p90 of |Δ signed err|, floored at 1e-12, pooled over
the 16 ships.** And the harness's own probe test (their cells, their laws) confirms the draft's
fragility independently: it FAILS today on this machine — leak 1.094, bounded-a 1.103, i.e. a
compounding law reads *below* a state-only one — and its random-walk control reads 3.1e5.

| Law | A: ratio | A across 4 one-ulp nudges | B: cell-drift | verdict (A ≤ 1.8 AND B ≤ 1.5) |
|---|---|---|---|
| bounded-a | 0.95 | 0.92–0.93 | 0.96 | pass |
| bounded-e | 1.04 | 1.03–1.07 | 1.07 | pass |
| bounded-1/r₂ | 1.31 | — | 0.53 | pass |
| iid noise 1e-11 | 1.01 | 0.99–1.04 | 0.53 | pass |
| walk, final 5.6e-12 | 2.31 | 2.92–3.78 | 1.05 | fail (A) |
| compound 1e-7/encounter | 3.09 | 6.4–13.3 | 4.64 | fail (A) |
| saturating walk (stops at ~50 encounters) | 3.10 | — | 4.63 | fail (A) |
| plane-like encounter jumps | 2.37 | 9.6–19.8 | 2.90 | fail (A) |
| **the harness's true leak** (v·(1+1e-12·t/P), exponent 1.13) | **1.55** | — | **1.97** | fail (B) |
| pure linear drift/leak plants | 9.35 | — | — | fail (A) |
| raw references 1e-11/12/13 | 13.3 / 17.0 / 4.8 | 6–169 (1e-12) | — | fail (A) |
| **time-periodic bounded** | **1.87** | — | 2.61 | **fail (gray, see F3)** |

Detector B (cell-drift): within each fine cell, |median err over late visits (t ≥ 100 P) −
median over early visits (t < 100 P)|, divided by the within-cell median spread (both floored at
1e-12), median over cells; it sees monotone drift that hides under a state-only oscillation,
which pair-diff recurrence cannot (the leak's error is 2ε(t)·v²/c0: v² swings over the orbit, so
every pair difference is dominated by the state-only oscillation, and the drift underneath only
moves the per-cell median). Neither probe alone suffices — A misses the true leak (1.55 < 1.8),
B misses walk-13 (1.05 < 1.5) — but each must-fail law trips at least one, with margin: state-only
maxima A 1.31 / B 1.07 (27% and 29% below their thresholds), memory minima above: walk-13 A 2.31
(28% above 1.8), leak-true B 1.97 (31% above 1.5).

State-only max 1.31 (27% below 1.8), memory min 2.31 (28% above); every pass/fail decision is
stable across all four one-ulp nudges (the ratio's *value* is heavy-tailed for walks — 6 to 169 —
but the decision is not). Every compounding law that fails today's B12 fails the replacement:
compound, drift, leak, walk-13, plane-jump, and the raw references. Positive controls: echo
(C held to 2e-15, under the floor — not judged) and every bounded plant.

**3. The floor is below the reference's own reproducibility, and the judged set is ulp-fragile.**
The frozen ships' two-tolerance C agreement is median 2e-11, max 2.4e-9 (converged bound 1e-9):
on this Linux box 1 of 16 is unconverged and 1 passes inside the planet, so **`echo` itself fails
B12 here** (2 excluded > the 10% budget) — the positive control fails for oracle-domain reasons,
before any statistic is read. Closest approach moves > 50% under a one-ulp nudge on **16/16**
ships; ships 1, 4 and 13 flip inside/outside the planet; per-ship exponents scatter across the
0.2 limit (bounded-a median 0.14–0.36 over nudges). Only medians over the 16 carry information;
single-ship numbers are noise (this is §1.8 of the Opus memo, confirmed harder: 16/16, not 9/16).

## Findings, named by the invariant, with dispositions

- **F1 (error type): the growth exponent cannot measure compounding on chaotic ships.** It
  conflates the law's error with the trajectory's own diffusion and the float floor. *Disposition:
  remove it as B12's deciding statistic (keep worst err ≤ 1e-4 and the floor); law.md's B12 line
  "miscalibrated" is confirmed, but replace "ranks them backwards" with "cannot separate — the
  ordering is not stable across machines".*
- **F2 (memory): no single statistic separates; a pair of orthogonal memory probes does.**
  Pair-diff recurrence with cells (0.02, 0.005) and windows 4–16 / 64–200 P at 1.8, AND per-cell
  early/late median drift at 1.5, both required. *Disposition: adopt as B12's replacement
  (two numbers replace the exponent; the cap and floor stay); re-freeze with controls on both
  sides of both (bounded-e 1.04/1.07 positive; walk-13 A 2.31 and the true leak B 1.97 negative).
  The e-cell at 0.005, not 0.05, is load-bearing: with 0.05 a bounded error in e reads 1.75.*
- **F3 (what the replacement guards): the pair's invariant is "the Jacobi error is a function of
  the ship's state", which is sufficient but not necessary for "never compounds".** A bounded
  time-periodic error (1e-7·sin(2πt/100P)) passes today (exponent 0.057) and fails both probes
  (A 1.87, B 2.61). *Disposition: the integrator chooses; my recommendation is to keep the
  memory-free reading (a law whose error tracks absolute time has a clock bug; catching it is a
  feature), and to reword B12's contract line accordingly.*
- **F4 (noise floor): the 1e-12 floor sits below the reference's own reproducibility (2e-11
  median, 2.4e-9 max).** Any unprojected law at reference accuracy fails both statistics (ratios
  4.8–17). Only laws that hold C to the floor (echo's projection, v2's J conservation) or are
  bounded in state pass. *Disposition: keep the floor (not loosened); state in law.md that B12
  demands "conserve the invariant to 1e-12, or be state-only and bounded" — that is what it has
  always measured.*
- **F5 (oracle domain): the judged set is one-ulp fragile — echo fails B12 on this Linux box**
  (2 ships flip: 1 unconverged, 1 inside), and 3 of 16 ships flip inside/outside the planet under
  one ulp. *Disposition: the freeze's convergence/inside assessment should be taken as the median
  over ulp replicas (cheap: the probe integrates 112 runs in 2 s), or the exclusion budget
  revisited — integrator's call; no threshold moved here.*

## Predictions

`predictions.md` was written before the statistics ran. Held: the reference fails at all three
tolerances (P1, stronger: 1.8 at the finest), the bounded/compound inversion reproduces as
"cannot separate" (P2), the draft ratio's thin compound margin (P3 — and the grid flaw it did
not predict), the periodic false-positive-by-principle (P4, ratio 4.5 on the draft cells), the
saturating-walk disagreement surfacing (P5: it fails both statistics, correctly), ulp chaos
(P6: 16/16, more than the predicted 5), and the floor below the reference's noise (P7). Missed:
the draft cells' failure on bounded-e (predicted the separation would hold as drafted); S*
(soft matching) making bounded-a worse; and the biggest one — the true leak's hiding under the
v² oscillation, which my pure-linear leak plant masked (my plant read 19.4 where the harness's
law reads 1.09): the harness's own failing probe test exposed it, and only reproducing the law
faithfully (err = 2ε·v²/c0 on the true states) showed the blind spot. Lesson: plant the law, not
its idealization.

## What would make it wrong, adoption cost, fit

Wrong if: a real law holds a bounded, state-only error in a slow coordinate with a gradient so
steep that a 0.005-wide e-cell (or 0.02-sep a-cell) under-resolves it — then probe A reads memory
and fails it wrongly (the cap at 1e-4 still bounds the damage: a steep-gradient law at full scale
fails the cap anyway); or a compounding law hides from BOTH probes — slower than walk-13 (final
error 5.6e-12, which today's gate also fails, at 0.527) for A and non-monotone for B; the true
leak already hides from A and only B catches it, so the pair is load-bearing, not belt-and-braces.
Detector B was not re-measured under one-ulp nudges (its mechanism, a monotone drift per cell, is
path-stable by construction; its closest positive, bounded-e at 1.07, has 30% margin). Cost: one
pass over the samples' pairs and cell medians (P/8 × 200 samples, 16 ships — seconds; the ignored
probe in handoff.rs already implements A in the harness; B is about 30 lines beside it). Fit:
principle 13 ("errors never compound") is enforced as error *type* (memory vs state), which is
what "types of errors and not just errors" (OC#42) asks; principle 22 ("the simulation tells us
what's next not us") — the ships' own returns decide, no fitted scale.

## The lens

The red-team lens made me probe the statistic and its replacement to destruction, but on one
scene (Jupiter, circular) with synthetic plants; I did not run the real plane through the ratio
(it cannot be expressed in my folder's harness), so the claim "the plane fails the replacement"
rests on the plane-like jump plant (its measured mechanism, memo §1.1) and the real gate's
`planted-drift`, not on the plane itself. Multi-planet scenes, where no Jacobi constant exists,
are outside B12 today and outside this run.
