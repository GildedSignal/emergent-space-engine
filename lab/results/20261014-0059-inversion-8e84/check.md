Grade: gold

**Abstract.** Gate-bite mutant panel on `universe --replay-all`: no law regression can exit 1 — exit bites only on new loss/refusal/same-law digest drift, verified in code and by two tamper controls (both exit 1). On main's stale corpus, reverting the 13-October contact fix prints `3 same, exit 0`, the gate's greenest output: the canon bit-exactly enshrines the bug's outcomes. 2 of 6 one-line mutants leave no review line on a fresh corpus. Gain: deletes a false assurance from every merge; adoption is one small `replay.rs` patch (law-hash currency, exit 2 on `changed`) plus a per-law-change corpus refresh. Checker correction: M-kick's invisibility is digest construction (`b.kick` is never hashed), not corpus scale — no corpus closes it.

## Reasons

**Reproduction.** `regen.sh` exit 0 in a clean tree at 33c83f1a (only `lab/results/` untracked); every dossier row matches `regen-logs/` exactly: baselines stale `3 changed` / fresh `3 same` (exit 0), M-wrap stale `3 same` exit 0 with the wrap law's digests (`7a9ec8f1…`, `d1fba929…`, `67023bcc…` — bit-exactly the corpus's recorded values) and fresh `3 changed`; M-kick and M-prune fresh `3 same` with law hashes moved; restore controls equal the baselines. `corpus-fresh` differs from `artifacts/flights` in exactly `digest`/`law_hash`/`commit`. The instrument claim is the code: `replay.rs:115` `law_same` is consulted only at `:140` inside the digest-mismatch arm; a matching digest prints `same` whatever the hashes; exit is `(bad > 0)` at `:267`.

**Predictions.** `predictions.md` (mtime 6 min before the first panel log) pre-dates the panel. P3, the central pre-registration (zero exit-1 in twelve runs), held. P2 half-held and the misses are reported as misses; P1 failed and the failure *is* the headline (the reward trap), diagnosed per H0183 — not papered over.

**Adversarial (mine).** (1) New-loss tamper → `REGRESSION … a loss appeared`, exit 1. (2) Same-law digest tamper → `REGRESSION … the digest differs under the SAME law`, exit 1. These are the positive controls the author's all-exit-0 panel lacked: the gate's teeth exist exactly where claimed, and nowhere else. (3) The author's M-kick mutated the ramp-metadata line (`step.rs:440`); I applied the same slip to the physics line (`:413`, the `h` that sizes Δv): `3 changed` on fresh — the corpus *does* fly kicks. (4) Structural: `Universe::digest` (`universe.rs:1121-1221`) hashes the plan's kick ticks and levels, the tube, residual, carries, thrust, encounters — never `b.kick` (`Kick{len,dv,…}` is observer ramp state, read only in `observe.rs`), and the mutated `len` feeds no schedule computation. So M-kick is invisible on **any** corpus, by construction. Tree restored, baseline reproduced (`3 same, exit 0`) after every mutation.

**Novelty.** The page's known holes are 30da (55 s budget skips) and dfd0 (canon is record-time machine noise). This run adds three classes those do not cover: the exit contract (law changes are `changed`/`same`, never `bad`), mesh (mutants with no line at all), and the reward inversion (a stale corpus certifies a reverted fix as its greenest output). It sharpens dfd0's own "the gate is a fine law-change detector": only as human-read `changed` lines, with no machine contract. First run of arch-v3's gate-bite mutants on a shipped gate. Nothing in docs/HISTORY.md touches the exit contract.

**Goal fit.** Truth, not cost, and the topic is on the wiki's open list; HANDOFF names this gate as the merge protocol's regression suite. PRINCIPLES: "a test that cannot fail is a control" — for law changes, this gate is one; and "errors never compound" — a canon certifying a known wrap bug compounds at every merge. A premise is shown wrong; adoption is within one step.

## What the author missed

1. **M-kick's mechanism.** The dossier/wiki attribute both invisible mutants to "paths dark at 48 members" and propose closing them with a dark-path corpus. For M-kick this is wrong: the digest never covers `b.kick`, so no corpus can ever catch a `Kick.len` regression (my physics-line control caught the same slip). Closing it needs digest coverage of the ramp (a canon reset) or an observe-consistency assertion. I corrected the page in place.
2. **No exit-1 positive control.** Fourteen runs, all exit 0: the panel never demonstrated the gate *can* fail, so "cannot fail for law regressions" was not bounded from below (my two tamper controls close this).
3. The M-wrap stale-arm `3 same` proves the recorded canon is the wrapping law's outcomes bit-exactly; the commit-order claim ("recorded before 31d124b9") is consistent but was not itself evidenced — immaterial to the finding.

## Page corrections made (author's wiki copy)

- The M-kick/M-prune bullet: split — M-prune stays scale-dark; M-kick is digest construction (`b.kick` never hashed; physics-line control caught), invisible on any corpus.
- Open direction 2: a dark-path corpus closes M-prune only; M-kick needs digest coverage of `b.kick` (a canon reset) — "would close the measured 2/6" removed.
- Added the checker's exit-1 controls to Current best (teeth bounded on both sides).
