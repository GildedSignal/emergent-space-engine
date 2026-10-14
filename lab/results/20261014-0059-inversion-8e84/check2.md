Grade: silver

**Abstract.** Reproduced in full: regen.sh's sixteen gate runs match every dossier cell,
zero exit 1. Code-verified: `law_same` is consulted only inside the digest-mismatch branch
and the exit code is `(bad > 0)`, so no law change can fail the gate. On main's stale
corpus reverting the 13-October contact fix prints `3 same, exit 0` — the greenest output;
M-kick and M-prune stay dark on a fresh corpus, M-kick because `Universe::digest` never
hashes `b.kick` (the same slip on the physics line is caught). Gain: deletes a false merge
assurance. Cost: a small `replay.rs` patch plus a corpus-refresh rule. Silver: the held-out
prediction (M-wrap invisible on fresh) missed.

## Reproduction

Applied nothing (work/patch.diff is empty — the panel edits crates and restores them; the
tree is main 33c83f1a, clean). The runner's regen.sh exited 0 and its sixteen logs
(regen-logs/) reproduce the dossier table exactly: baselines stale `3 changed, exit 0` /
fresh `3 same, exit 0`; M-wrap stale `3 same` (digests 7a9ec8f1ad0e / d1fba9298aa9 /
67023bcc26bc — bit-identical to the corpus's recorded digests, which independently proves
the canon *is* the wrapping law's outcomes), M-wrap fresh `3 changed`; M-sign / M-thrust /
M-bind `3 changed` on both arms, exit 0 (M-thrust even prints "the loss vanished" — still
`changed`, not a regression); M-kick and M-prune `3 same` on fresh with digests identical
to the unmutated tree; both restore controls equal their baselines. Instrument verified in
source: `compare` (xtask/src/universe/replay.rs:113-156) — `law_same` (line 115) is read
only at line 140 inside `Some(d) if *d != r.digest`; a matching digest falls through
`Some(_) => {}` (line 147) with no note whatever the hashes say. `replay_all` returns
`(bad > 0) as u8` (line 267); `bad` comes only from a new loss, a refusal increase, a
same-law digest mismatch, or a load/replay failure. Gate runs 1.9–2.2 s; only the builds
exceed 60 s, as disclosed.

## Held-out predictions

`predictions.md` predates the panel (mtime 32 m before the first mutant build log at the
session's listing; content is pre-run priors, not fitted). P3 held exactly (zero exit-1 in
twelve runs). P1 failed (M-wrap moves the stale arm off baseline — to `3 same`, the trap);
P2 half-missed (M-wrap and M-bind visible on fresh, predicted invisible); **P4, the case
explicitly labeled held-out, missed**: M-wrap showed `changed` on the fresh corpus. All
misses are disclosed in the dossier with the author's own counting. Under the lab's
precedent (1 October red-team: an honestly reported held-out miss bars gold), that is the
blocker.

## Adversarial cases (mine, none of them in the author's panel)

1. **Teeth, channel 1** — corpus-fresh with one digest tampered under the same law:
   `REGRESSION … the digest differs under the SAME law`, **exit 1**. The teeth exist
   exactly there.
2. **Teeth, channel 2** — the recorded loss erased from flight 3's JSON: `REGRESSION … a
   loss appeared: hit Home at 7.51 km/s`, **exit 1**.
3. **The kick physics line** — the author's M-kick sits at step.rs:440 (`Kick.len`
   metadata). The same shift on the physics line (step.rs:413, the `h` that sizes Δv)
   gives `3 changed` on fresh. With `Universe::digest` (universe.rs:1121+) hashing no
   `kick` field (grep: zero matches), M-kick is dark **on any corpus**, not merely at
   this scale — the author's P2 rationale ("kicks are universal" → visible) was wrong in
   the opposite direction.
4. **Absurd prune margin** — `(1 << 26)` → `(1 << 2)` (the author tested `1 << 20`):
   still `3 same` on fresh. M-prune's darkness is scale-bound, not knob-specific,
   supporting the corpus-envelope reading (a prune-hungry readout would fail the replay,
   the one channel that could catch it).
5. **M-wrap vs the shipped suites** — the author's side-claim verified: under M-wrap,
   `cargo test -p emergent-lattice hit_is_exact_past_the_i128_products` FAILS. The gate
   is indeed one layer, not the whole net.

Also checked: corpus-fresh is self-certifying — the gate itself verifies it (`same`
requires a digest match under the same law), so no hand-tamper could have manufactured
the fresh baseline. The disclosed first-pass mtime/rlib accident is real and the reported
table is the controlled second pass (git checkout + touch), which regen reproduces; the
accident's lesson (law hash read from disk, not from the compiled binary) is a live
hazard worth keeping in the record.

## Novelty

The published page (lab/wiki/replay-gate.md, updated by 30da) holds only the budget decay
and dfd0's canon noise; the board's leads list arch-v3's gate-bite mutants as "not yet
running". Mesh (2/6 dark, one by digest construction), saturation (stale corpus flattens
the signal) and reward (reverting a fix reads greenest) are new, and the trap is
demonstrated with the real 13-October bug, not a synthetic one. docs/HISTORY.md has no
replay-gate entry. Not a repetition.

## The page

Faithful to the evidence; the checker-added corrections (M-kick dark by digest
construction; step.rs:413 caught; teeth bound from below) all match my independent
verification. One correction made: the Runs section self-graded the run `(gold)`; with
this check it is `(silver)` (gold needs both finders). I also folded in the absurd-margin
probe (open direction 2).

## Goal fit

It shows a premise is wrong: HANDOFF's "`universe --replay-all` before every merge" has no
machine contract for law regressions, and today certifies the bug it was meant to guard.
PRINCIPLES: "a test that cannot fail is a control" — this gate, for law changes, is one;
and "errors never compound": a canon that rewards reverting fixes compounds at every
merge. Adoption is one small patch, off the hot path. Not an engine-speed bottleneck, but
a Truth-instrument one, on an open wiki topic.

## Why silver, and the one experiment

Everything reproduced, novel and adoptable — but the held-out prediction missed (P4), and
P1/P2 partially, which the lab's own precedent bars from gold however honest the
reporting. The one experiment that would make it gold: **run M-kick and M-prune against
the shipped test suites** (`cargo test` for the universe and lattice crates under each
mutant; crates/universe/tests/ holds plane, motion, lifecycle, memo integration tests,
none yet measured against these slips). If neither suite kills them, the two dark mutants
are guarded nowhere and the premise-wrong result is total — adoption stops being a
judgement call. If a suite kills one, the finding stands narrowed to the other.

## What the author missed

- M-kick's darkness is digest construction, not corpus scale — the open directions
  originally treated it as envelope-closable; only a canon reset (hash `b.kick`) or an
  observe-consistency assertion can catch it.
- The two no-rebuild teeth controls (digest tamper, loss erasure) were one command each
  and bound the exit contract from below; the dossier asserts the contract from code
  reading only.
- The absurd-margin extreme (`1 << 2`) was the cheaper probe for M-prune's class
  (scale-bound vs always-dark).
- The corpus's self-certification (a `same` under the same law proves the fresh arm was
  not manufactured) deserved a line: it is what makes the fresh arm trustworthy.
