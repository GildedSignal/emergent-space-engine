Working...
Fixed and verified. Root cause: regen.sh assumed a pristine starting tree, but the runner executed it on the tree where the run's edits were still applied — `git apply` hit `already exists in working directory` plus content-mismatched hunks (atomic failure, `set -e` abort). The patch itself is sound: `git apply --check` passes against pristine HEAD.

**Changes to `regen.sh` only:**
1. **Idempotent heal** after `cd` to repo root, before the pristine digest: `git checkout -- crates/` + `rm -f` of the two example files — regen now converges to a clean base from any starting state (clean checkout, the author's still-applied edits, or a partially restored tree).
2. **Parity comparison** now strips the trailing wall-time field (`[6.4 s]`) before `diff`, so the digest/count comparison is exact and prints `PARITY: bit-identical` — previously `diff` exited 1 on the timing tail and the dossier's "bit-identical" evidence never appeared in the log.

**Verification:** (a) reproduced the runner's exact failure state, ran the heal, confirmed the patch then applies; (b) two full end-to-end runs (199 s, 202 s), both exit 0, restoring the tree clean (`git status`: only untracked `lab/results/`) — all dossier numbers regenerate: parity bit-identical on digests and counts, census 84,064/31,654 vs the recorded 84,252/31,652 (~0.2% on a shared box), real-state bind ~17.6-17.9 µs, compile medians 4.5 µs belt / 13.9 µs strong, `div_word` 2.9 ns vs wide division 23.3 ns.

Claim: regen.sh failed only because it inherited the run's still-applied edits; a three-line heal to pristine HEAD before step 0 (plus a timing-tail-stripped parity diff) makes it regenerate every dossier number in ~200 s from any tree state, verified end to end twice.
