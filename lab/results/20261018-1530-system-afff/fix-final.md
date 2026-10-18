Fixed: regeFixed. The patch itself was sound — `git apply` failed because the runner executed regen.sh against a tree that already carried the patch (reproduced bit-for-bit: a second apply on a patched tree yields exactly the two `patch does not apply` errors from regen.log). regen.sh's apply step is now idempotent: forward-check → apply; reverse-check → "patch already applied" and continue; neither → exit 1.

Proof, both states, on this machine:
- Clean tree at base 4c3e0b52: exit 0 in 18 s (11 s warm build + 3 flights), every dossier number regenerates exactly — A: 241 scans / 240 bail / 33.3 cand / 113 empty / 128 hits all rank 0; B: 231 / 229 / 323.8 / 29 / 292 with rank_near zero beyond rank 11; C: 241 / 0 / 177.8 / 113 / 128, bit-identical answers to A.
- Already-patched tree (the runner's exact failure mode): exit 0 in 7 s via the skip branch, 3 census lines regenerated.

Tree left restored; only regen.sh changed.
