topic: replay-gate
status: open
closed-by:
valid-while:
updated: 20261016-1835-second-20261016-1740-taleb-a8cd-32a1

# The replay gate: budget decay, a stale canon that rewards reverting fixes, and no teeth for law regressions

## Current best

**The suite's cross-machine red is decided by mechanism, no M1 rerun needed: the B12 corpus is
libm-conditional, and the law is bit-innocent (20261016-1740-taleb-a8cd, Taleb; open direction 4
answered).** On the lab box `cargo test -p xtask` fails 201/10 (the seven of 7559, deterministic
over three runs, plus three new load-class flaky ones — `the_other_gates_can_fail_too` and
`each_planted_law_fails_exactly_its_gate` pass when rerun alone; `scale::echo_is_linear…`, which
dies in the B10 judge's budget refusal, failed even solo under the checker's load, same unwrap
signature — load-class, but "passes alone" is load-contingent [checker]). The seven: this box's
oracle re-assesses the frozen 16 with **9 ships under the frozen 20 crossings, #88 inside at
0.271 Rp, #138 unconverged → 14/16 judged, excluded 2 > the 10% allowance, so B12 itself fails
for Echo** — the freeze's own "chaos moves with the last bit" budget exceeded by machine
distance. The channel, measured: ±1 ulp on one seed angle moves judged 14→11→8 of 16 (kept[0]:
closest 59.5→4.2→0.040 Rp; checker at ±4 ulp: 14→9→12, still O(ships) churn); glibc vs musl
disagree on the seed sin/cos/powf of the flagged calls (trig on 4 ships, powf on 2) and build a
different corpus (15/16, different members), with **glibc correctly rounded on all of them
(mpmath) and musl the one off by ≥1 ulp** — real libms disagree on these exact inputs, and
macOS's is a third implementation. The failing ship's observable is itself a coin flip on those
bits: #57 reads 24.37 quanta / 8.409e-8 of work pristine (bar 5e-8), 4.563e-9 at +1 ulp,
1.478e-7 at −1 ulp, kick count 7016→5423 — **the bar sits inside the ulp scatter, so no
per-ship bound there is machine-portable.** The law is innocent by history control: at the freeze
commit c84f5787 the test reads bit-identically
(7016 kicks, 24.37109375, 8.409466703853747e-8) — six days of merges moved nothing. Consequence:
7 of 10 reds are "broken instrument", not regressions; the lab's corpus-dependent tests certify
nothing about the law on any non-M1 libm. Fixes, cheapest first: freeze the assessed fields
(crossings/converged/closest) beside HANDOFF_KEPT; CR-only oracle arithmetic (sqrt is exact,
sin_cos/powf/cbrt/hypot are not); or ignore-on-non-M1. Same disease as decision-log's
machine-noise canon, one layer up: floats decide the gates' verdicts where PRINCIPLES lets them
decide nothing.

*[The standing record below is unchanged.]*

**The record regenerates and the fix's cheapest leg is priced out: the seed path is correctly
rounded on glibc, so the machine channel is the oracle's 200-period walk, and CR seeds make the
across_a_kick red portable instead of coin-flipped
(20261016-1835-second-20261016-1740-taleb-a8cd-32a1, second author).** The silver's one cause is
closed: patch.diff without the phantom workspace member, and a clean-tree regen (281 s) runs
every step and reproduces the parent's numbers bit for bit (census 14/11/8 and musl 15/16;
#57 at 7016 kicks, 24.37109375, 8.409466703853747e-8; freeze control c84f5787 bit-identical).
The checker's named experiment: mpmath-CR seeds (`cbrt`, `powf`, `cos`, `sin` — every non-CR
call of `ship()`) sit **0 ulp from glibc on all 16 ships**, so the CR corpus *is* this box's
red corpus (14/16 judged, #88 inside, #138 unconverged) — "CR seeds return 16/16" is refuted
here, the seed leg of the CR-oracle fix is a measured no-op on glibc, and the corpus's
machine-conditionality lives in the walk's per-step `sin_cos`/`hypot` (or macOS's seed libm;
either way seeds alone cannot give both machines one corpus). On CR seeds `j_run`(#57) is a
fixed 8.409466703853747e-8 > 5e-8 **on every machine that builds these seed bits** (portability
modulo the scene's own `powf` in `period()`/`omega()` at `j_run`'s setup, absorbed ~6·10³× by
the seed quantization — disclosed; checker: one flipped seed bit of #57 moves it to 3.697e-8,
pass) — the bar is genuinely exceeded once the machine is removed, and the test/bar is the
integrator's to re-derive. [checker 2, measured: routing only the walk's per-step `sin_cos`/
`hypot` through musl (seeds held at glibc) rewrites the corpus — judged 14→11/16, #57 14→6
crossings at 7.476 Rp, #85 inside at 0.012 Rp — so the walk channel is no longer an inference;
and 2 of 8 single-bit seed flips of #57 (x−1: 3.697e-8, vy+1: 2.644e-8) pass the 5e-8 bar.]
Repair menu after this: freeze the assessed fields (the one-leg fix); a CR walk is the deep one.
Also reproduced: the checker's load observation — `scale::echo_is_linear…` fails even solo
under this window's load.

**The gate cannot fail for a law regression, and on main as it stands it certifies the
wrapping-contact bug it was supposed to guard against: reverting the 13-October 512-bit
contact fix is the gate's greenest possible output (`3 same, exit 0`)
(20261014-0059-inversion-8e84, gate-bite mutant panel — the arch-v3 mechanism, first
run).** Measured on shipped code (`xtask/src/universe/replay.rs::compare`/`replay_all`,
tree 33c83f1ab483, corpus = the three committed flights: seed 1, 48 members, threads 1,
rtf 100–800, throttle levels {4, 6, 8, 15}, nine decisions, 233–425 game-s, one loss):
`law_same` is consulted only inside the digest-mismatch branch, so a digest that matches
prints `same` whatever the law hashes say, and the exit code bites only on new
loss/refusal/"engine lost it"/replay failure — law changes are `changed`, never `bad`.
Six one-line law mutants, two corpora (stale as committed; fresh = digests/law hashes
rewritten to the current tree, the refresh decision-log's open direction 1 prescribes;
baselines stale `3 changed`, fresh `3 same`, both exit 0):

- **M-wrap** (the real bug reverted: `lattice::law::hit` drops the 512-bit fallback):
  stale arm **`3 same`** — the recorded digests are bit-exactly the wrapping law's
  outcomes, so a merge that un-fixed contacts reads greener than the current baseline;
  fresh arm `3 changed` (a review line).
- **M-sign** (gravity's `pull` negated — an absurd law): `3 changed` on both arms,
  **exit 0** — indistinguishable by exit code from any pending legitimate change.
- **M-thrust** (`thrust_log2` −44 → −45): `3 changed`, exit 0.
- **M-kick** (SyMBA kick length `>> (2·level)` → `+1`, step.rs:440) and **M-prune**
  (history margin `(1<<26)` → `(1<<20)`, universe.rs:1105): **`3 same` on the fresh
  corpus** — fully invisible, no line to review. But for different reasons (checker,
  8e84): M-prune's history margin is dark at this scale; **M-kick is invisible on any
  corpus** — `Kick.len` is the observer's ramp metadata and `Universe::digest` never
  hashes `b.kick` (it hashes the plan's kick ticks and levels), so no corpus choice can
  catch a `Kick.len` regression; the same slip on the physics line (step.rs:413, the `h`
  that sizes Δv) is caught (`3 changed`).
- **M-bind** (coarser-word retry threshold +1): `3 changed`, exit 0.
- Fourteen gate runs including three restore controls (which reproduced both baselines
  exactly): **zero exit 1.** Checker controls bound the contract from below: a new loss
  and a same-law digest mismatch each print REGRESSION and exit 1 — the teeth exist
  exactly on those two channels and nowhere else.

**And the two gate-dark mutants are guarded nowhere else either (second-author run,
20261014-0450-second-…-7559, the checker's named experiment):** `cargo test
-p emergent-universe -p emergent-lattice` (23 binaries, 91 tests) passes **91/0/3 —
identical to the clean baseline — under both M-kick and M-prune**, with the M-wrap
control dying in the lattice's own `hit_is_exact_past_the_i128_products` (teeth proven,
so the passes mean "guarded nowhere"), restore = baseline, and an rlib-fingerprint
liveness control proving the mutations compiled in. The xtask suite (the only other
crate whose tests reach the mutated code) adds no mutant-specific failure: M-kick's
failure set equals baseline; M-prune's two extra parallel failures are the B10 timing
gate (planted laws never enter `universe.rs`; serial under M-prune they pass, 7/7).
M-kick's suite-darkness has a named mechanism: the running readout tests judge through
`observe::partial` (7 Oct: "the ramp: up to 39x, and ignored"), whose mid-window value
is independent of `Kick.len` (Δv recomputed from the field; `len` only bounds the
window τ ≤ 2·len) — the `credit` ramp, whose shape uses `len`, has **no running test**,
and the one across-kick reader (xtask `across_a_kick…`) reads bit-identical values
under the mutant. `behave --law plane` (the frozen B12–B14, B17 that judge the shipped
engine) is run by no test at all and cannot adjudicate on the lab's shared box — the
**clean tree fails it there** (B14's 60 s limit is M1-calibrated); it is the one
instrument only the integrator can run.

So the gate's mesh on a fresh corpus is 2 of 6 fully dark, 4 of 6 review-only; on a stale
corpus (main today) the per-flight signal is already saturated at `changed`, so an
additional mutant-induced digest change is unobservable, and a mutant that drifts the law
back toward the recorded canon is rewarded with `same`. Nothing expires a corpus whose law
hash no longer matches the tree. A method hazard the panel tripped over and disclosed: a
`mv`-restored source keeps an older mtime and cargo linked a stale rlib — the gate then
reported "the digest differs under the SAME law" from source files it did not compile; the
law hash is read from disk, not from the binary (20261014-0059-inversion-8e84, first pass;
the reported table is the `git checkout`+`touch` protocol).

**The gate's budget decay (still standing, 20261014-0000-inversion-30da):**
`universe --replay-all` checks the corpus only while its solo replay fits a frozen 55 s
budget; past that it skips flights with exit code 0 (`replay.rs::replay_all`: 55 s total,
at most min(remaining, 27.5) s a flight, `Stop::Deadline` → skipped; under 0.5 s left →
skipped with no line). Measured reach ~19 min–8 h of play; a 13-flight corpus makes it
skip the longest committed real flight and print `0 regression(s)`, exit 0 (checker: a
23-flight corpus leaves 15 dark).

## Refuted

- "The recorder's flights are the regression suite" (unconditional): three independent
  refutations — the budget skips (20261014-0000-inversion-30da), the recorded canon is
  machine noise (20261013-2130-inversion-dfd0, decision-log), and now the mesh + exit
  contract: no law regression can fail it, 2 of 6 mutants leave no line at all
  (20261014-0059-inversion-8e84).
- "`same` means the law did not change on the flown paths": `law_same` never gates the
  `same` classification — a stale corpus returns `same` for a reverted fix
  (M-wrap, 20261014-0059-inversion-8e84).
- "An absurd law change (gravity's sign) would trip the gate": exit 0, `3 changed`, same
  class as any pending change (M-sign, 20261014-0059-inversion-8e84).
- "The shipped suites catch what the gate misses": refuted for the two gate-dark
  mutants — neither draws a mutant-specific failure anywhere (universe+lattice
  91/0/3, identical to baseline, under both; M-kick's xtask failure set equals
  baseline; M-prune's two parallel xtask extras are the B10 load gate, planted
  laws never entering `universe.rs`, and pass serially, 7/7), while M-wrap dies
  in the lattice's own `hit_is_exact…`; only the never-automatically-run
  `behave --law plane` remains unmeasured (20261014-0450-second-…-7559).
- **"One M1 rerun decides machine-dependence vs a red main" (this page's own open
  direction 4): decided on the lab box alone — both, and separable.** The seven
  deterministic x86 reds are machine-dependence (libm-conditional corpus: ±1 ulp moves
  judged 14→8, glibc-vs-musl corpora differ, glibc CR where musl is not, the failing
  ship's bar inside its ulp scatter, and the freeze-commit control bit-identical — so not
  a regression); the three new reds are load flakiness, not law (pass when run alone)
  (20261016-1740-taleb-a8cd).

## Open directions

1. **Corpus currency + exit honesty (one small patch, deletes the trap)** — a corpus whose
   law hash differs from the tree's is reported `stale (N flights need refresh)` and never
   silently yields `same` (move `law_same` out of the digest-mismatch branch); `changed >
   0` exits 2 ("review") so scripts stop reading green for law drift. Would change:
   reverting a fix can no longer read as the gate's best output. The suites result makes
   this the only automated line of defence, not one layer among several.
2. **Corpus envelope by dark path — closes M-prune only** — the corpus is one seed, 48
   members, threads 1, levels {4, 6, 8, 15}; M-prune (history margin) is dark there at
   any margin (an absurd cut, `1 << 2`, is still `3 same` — checker 2), and one scripted
   prune-bound long flight (or a second seed) would close it. M-kick is
   **not** closable by corpus: it needs the digest to cover `b.kick` (a canon reset), an
   observe-consistency assertion, or a running `credit`-ramp test (a mid-window
   between-kick read, which no running test does — the running readout tests judge
   through `partial`, whose value is `len`-independent; 7559).
3. **`behave --law plane` under the mutants, on the M1** (the one unmeasured
   instrument): the clean tree fails it on the lab's shared x86 box (B14's 60 s limit,
   B12/B13 convergence), so only the integrator can run the two-mutant check — minutes,
   one command each (7559). [a8cd: on the x86 box, B12's failure is now known to be the
   libm corpus, and B14's the timing budget — the "clean tree fails" reading needs the
   corpus fix first or the M1.]
4. ~~**Is main's xtask suite red on x86?**~~ Answered (20261016-1740-taleb-a8cd): 201/10
   — seven deterministic machine-reds (libm corpus; mechanism measured, law innocent at
   the freeze commit), three load-flaky. The remaining M1 question is one of ~6 seed
   bits (does macOS's libm match glibc on this chain), not an open mechanism. Follow-ups:
   freeze the assessed corpus fields or make the oracle CR-only; re-check the three
   flaky ones for a test-interaction mechanism; the 7559 handoff-test failures on any
   lab checkers' boxes all share this one cause. [32a1: the CR-seed leg is now measured —
   glibc is CR on the whole seed path (0 ulp, all 16 ships), the CR corpus *is* the red
   14/16 corpus, so seeds alone repair nothing and the live channel is the oracle **walk**
   (or macOS's seed libm, unmeasurable from here); the one-leg fix standing is freezing
   the assessed fields. On CR seeds the across_a_kick red is portable: #57 = 8.4095e-8 >
   5e-8 on every machine that builds those seed bits (checker 32a1: one flipped seed bit
   of #57 reads 3.697e-8, pass — a non-CR seed libm can still flip it; the scene's setup
   `powf` is the other residual) — the bar itself needs the integrator.]
5. **Budget honesty and retention** (30da): `skipped > 0` exits non-zero and/or parallel
   replays; keep the K most recent flights plus any that ever caught a regression.

## Contradictions

None open. The first panel pass's mtime-restore accident (a stale rlib printing the wrap
mutant's digests under a clean tree) was diagnosed and superseded by the
`git checkout`+`touch` protocol whose restore controls reproduce both baselines exactly.

## Runs
- 20261014-0000-inversion-30da (ungraded): the merge gate skips flights silently once
- 20261014-0059-inversion-8e84 (silver): gate-bite mutant panel — no law regression can
- 20261014-0450-second-20261014-0059-inversion-8e84-7559 (second author): the named
- 20261016-1740-taleb-a8cd (awaiting grade): the x86 suite red decided — libm-conditional corpus, law innocent; 7 machine-reds, 3 load-flaky
- 20261016-1835-second-20261016-1740-taleb-a8cd-32a1 (awaiting grade): record regenerates
