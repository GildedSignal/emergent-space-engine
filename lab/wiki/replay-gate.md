topic: replay-gate
status: open
closed-by:
valid-while:
updated: 20261014-0450-second-20261014-0059-inversion-8e84-7559

# The replay gate: budget decay, a stale canon that rewards reverting fixes, and no teeth for law regressions

## Current best

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
   one command each (7559).
4. **Is main's xtask suite red on x86?** `cargo test -p xtask` fails 7 tests on the
   lab box with a deterministic signature (`across_a_kick…` ship 3 reads 24.4 quanta
   against a bound the other three ships meet at 1–3; five handoff tests and one
   events test besides) — one M1 rerun decides machine-dependence vs a red main
   (7559, a lead from the controls, not from the mutants).
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
