# Dossier — the replay gate's mesh, its stale-canon trap, and its exit contract

## Claim

`universe --replay-all`, the check run before every merge, **cannot fail for a law
regression**: its exit code bites only on new losses/refusals, every law change it does see
is an exit-0 "changed" review line with two 12-character digest prefixes, 2 of 6 plausible
one-line law mutants leave it printing `same` on a fresh corpus with nothing to review at
all — and on main as it stands (corpus recorded at 73c98a46, law since moved) the gate
prints a *cleaner* result for the broken law than for the fixed one: reverting the
13-October 512-bit contact fix returns all three committed flights to `3 same, exit 0`,
the greenest output the gate can produce.

## Bottleneck

Not a frame-cost bottleneck: a Truth-instrument bottleneck (PRINCIPLES: "a test that
cannot fail is a control"). The merge protocol's stated regression suite
(HANDOFF: "`universe --replay-all` before every merge") has no teeth for law changes, and
its corpus canon currently enshrines the pre-fix wrapping-contact outcomes. Expected gain:
not speed — it deletes a false assurance from every merge and redirects corpus policy
(what to record, when to refresh) that the recorder's adoption depends on. This is the
arch-v3 "gate-bite mutants" mechanism, run for the first time on the shipped gate.

## Evidence

All numbers regenerate with `bash lab/results/20261014-0059-inversion-8e84/regen.sh`
(~12 min on 8 vCPU Linux; every command ≤ 60 s except the builds). Tree: main
33c83f1ab483, law `es-space-v2` hash `41f180a05c92cfe1`; corpus: the three committed
flights (all seed 1, 48 members, threads 1, rtf 100–800, throttle levels {4, 6, 8, 15},
nine decisions, 233–425 game-s, one loss).

**The instrument.** `xtask/src/universe/replay.rs::compare`: `law_same` is consulted only
inside the digest-mismatch branch; a digest that matches prints `same` regardless of the
law hash, and `replay_all` exits 1 only when `bad > 0` — new loss, new refusal, "the
engine lost it", or a replay failure. Law-code changes are counted as `changed`, never
`bad` (by design: "a change to review").

**The panel** (two corpora: *stale* = `artifacts/flights/` as committed, recorded under
law `be41b063…` at 73c98a46; *fresh* = the same three files with digest/law_hash/commit
rewritten to the current tree, i.e. the refresh decision-log's open direction 1 prescribes;
baselines: stale `3 changed, exit 0`, fresh `3 same, exit 0`):

| mutant (one line, law crates) | stale arm | fresh arm | verdict |
|---|---|---|---|
| M-wrap: `lattice::law::hit` drops the 512-bit fallback (the real 13-Oct bug, reverted) | **3 same**, exit 0 | 3 changed, exit 0 | visible on fresh only, as a review line |
| M-sign: `force::pull` returns the negated acceleration | 3 changed, exit 0 | 3 changed, exit 0 | review line, exit 0 |
| M-thrust: `Config::thrust_log2` −44 → −45 | 3 changed, exit 0 | 3 changed, exit 0 | review line, exit 0 |
| M-kick: SyMBA kick length `>> (2·level)` → `>> (2·level+1)` (step.rs:440) | 3 changed, exit 0 | **3 same**, exit 0 | **fully invisible** |
| M-bind: coarser-word retry threshold +1 (bind.rs:233) | 3 changed, exit 0 | 3 changed, exit 0 | review line, exit 0 |
| M-prune: history margin `(1<<26)` → `(1<<20)` (universe.rs:1105) | 3 changed, exit 0 | **3 same**, exit 0 | **fully invisible** |

Twelve gate runs, **zero exit 1**. A flipped gravitational sign — an absurd law — exits 0
with the same classification as any pending legitimate change.

**The stale-canon trap.** The corpus was recorded before the contact fix (31d124b9) and
before the T1/frame merges; on today's main every flight already prints `changed`
(baseline). M-wrap on the stale arm prints `3 same`: the recorded digests are bit-exactly
the wrapping law's outcomes, so **the gate's best output today certifies the bug**. Nothing
in the gate or the protocol expires a corpus whose law hash no longer matches the tree;
`compare` treats a matching digest as `same` whatever the hashes say.

**Method note (disclosed).** The first panel pass restored mutants with `mv`, which
restores an older mtime; cargo then linked a stale rlib for `law.rs` (its own dead-code
warning proves it) and the "restore" row printed the wrap-mutant's digests. The reported
table is the second pass: `git checkout --` + `touch` before every rebuild, with the
restore control reproducing both baselines exactly (`restore2`: stale `3 changed`, fresh
`3 same`). The law-hash-from-disk vs binary-code divergence that this accident exposed is
itself a live hazard for any build-cache reuse on the integrator's machine: the gate
asserts "under the SAME law" from source files it did not compile.

## Predictions

`predictions.md` was written before the panel. P3 held (zero exit-1 anywhere). P2 half
held: M-kick and M-prune invisible as predicted; M-wrap and M-bind were visible on the
fresh corpus (reported as misses; P4 had flagged the wrap case). P1 failed in the most
interesting way: it predicted the stale arm could not move at all, but M-wrap moves it to
`3 same` — better than baseline — which is the trap, not a pass.

## What would make it wrong

The panel is six mutants on one corpus; a different panel could bite more (the universe
suite's own tests kill M-wrap — `hit_is_exact_past_the_i128_products` — and any physics
test kills M-sign: the gate is one layer of the merge checklist, not all of it; whether
any shipped test kills M-kick or M-prune is unmeasured — the named next experiment). The
fresh arm refreshes digests only, not flights: it assumes the current tree is the truth to
canonize (a bug already on main would be canonized by a refresh). The stale-arm `3 same`
for M-wrap is a three-flight result; a fourth flight that wraps differently could show
`changed` instead — the reward-revert mechanism survives (it needs only one corpus flight
to return to its recorded digest).

## Cost of adoption, fit with PRINCIPLES

Adoption is small and local to `replay.rs` + the merge protocol: (1) a currency rule — a
corpus whose law hash differs from the tree's is reported as `stale (N flights need
refresh)` and never silently yields `same` (the `law_same` check moves out of the
digest-mismatch branch); (2) the exit contract — `changed > 0` exits 2 ("review"), 1
stays regressions, so scripts and humans stop reading green for law drift; (3) one
refreshed corpus per merge that changes the law (the digest rewrite is three `jq` edits,
this run's `corpus-fresh`). Fits PRINCIPLES "write the kill criterion before the run, with
controls on both sides: a test that cannot fail is a control" — this gate, for law
changes, is a control; and "errors never compound": a canon that certifies a known wrap
bug compounds at every merge. Cost: none measured on the hot path (the gate is offline);
the risk is over-trusting `changed` lines once they exit non-zero (review fatigue) —
hence exit 2, not 1, for review.

## The lens

Inversion asked how the freshest merge's safety net fails, not whether it works. It found
three failure classes the two known holes (30da's budget, dfd0's canon noise) did not
cover: mesh (2/6 dark), saturation (stale corpus flattens the signal), and reward
(reverting a fix reads greenest). What the lens may have missed: the corpus's value as a
*law-change detector for humans* — the integrator does read `changed` lines and did catch
real drift with them (HANDOFF records the three flights' digest change as expected
behaviour); the finding is that this reading has no machine contract and decays with
corpus age, not that it is worthless.
