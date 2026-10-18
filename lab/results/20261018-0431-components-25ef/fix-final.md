Working...
Fixed and verified. Root cause: `regen.sh` line 5 did `cd ../../../..` — **four** levels up from `lab/results/<run>/`, landing outside the repo, where the relative `work/patch.diff` path doesn't exist → `git apply` exit 128 before any number ran. Second latent bug: the runner pre-applies the patch (`regen()` line 18), so regen.sh's own apply had to be idempotent or it would have failed next as "already applied".

Changes (regen.sh + the one dossier clause it needed):
- `cd ../../../` (three levels = repo root), verified by running it exactly as the harness does.
- Patch step is now idempotent: skip when `git apply --reverse --check` says it's already applied (the runner's flow), apply when standalone, and hard-fail with a clear message only if the patch is absent *and* the arm is missing from the tree (no silent shipped-numbers record).
- Widened the arm-ON grep so gate 1's per-ship ratios print (dossier's 0.98–1.11× range now regenerates, not just the worst).
- dossier.md: the burn controls line didn't regenerate — it said "t1_burn 4 … throttle's single test `#[ignore]`d"; the truth (from the test sources and the run) is `p2_burn_out` 3 passed, `throttle` 8 passed, and `t1_burn`'s single test is the frozen-`#[ignore]`d T1 gate. Corrected.

Verified twice, harness-style (`git apply work/patch.diff` from repo root, then `bash regen.sh`): **exit 0, 2m26s** (budget 15 min), and every dossier number reproduces — worst ratio 1.11× (ship 4), per-ship 0.98–1.11×, step-squared fall 15.9–18.3×, map 14.9–16.9×, raw-tube control 1.8–12.8×, bounded 5.29e-6, bit-identical OFF arm, motion 4 / replay 2 / memo 1 / clock 4 / origin 3 green, p2_burn_out 3 + throttle 8 green with t1_burn ignored. Tree restored to shipped afterwards, so `fix.diff` stays empty and `patch.diff` remains the single author patch.

**Claim:** the record now regenerates — regen.sh ran one directory too high (four `..` instead of three) and died at its own patch-apply before any number; with the root fixed, the apply made idempotent against the runner's pre-applied patch, and one non-regenerating dossier count corrected, `regen.sh` exits 0 in ~2.5 minutes reproducing every dossier figure bit for bit.
