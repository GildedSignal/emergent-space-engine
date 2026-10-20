Working...
Fixed and verified end-to-end.

**Cause.** The runner's save step wrote an empty `work/patch.diff` (0 B); `regen.sh` then failed its `git apply --check` and the `ES_SEED`-already-applied fallback on the restored tree → `FATAL: patch neither applies nor is applied`. `regen.sh` itself was correct — what it needed was its patch file.

**Fix.** Reconstructed `work/patch.diff` (13,676 B) = `work/patch-8994.diff` (8994's `alloc_scope` instrument, verbatim) plus the dossier-disclosed addition: an env-gated `ES_SEED` override, default 1 = shipped bits, passed as `plane_extra`'s seed argument (`alloc_scope.rs`, at the call the dossier's line 118 points to). Generated via `git diff` at base `83982a7`, so it applies bit-cleanly; `git apply --check` passes, `-R` reverses cleanly, and the tree is back to clean.

**Proof.** Full `regen.sh` from the clean tree, 99 s: every dossier number regenerates — A1 193.4 KB/item, ship 3.7 KB/item, 11.35 KB/kick, base 2.04 KB/game-s; A2 193.5, A3 198.7, A4 193.8 + 2.18 KB/kick, A5 194.1 + 3.00 KB/kick and the 7.23 mixture; ladder top exactly 57,344 B, realloc share 79–80%, >2KiB share 70/71/69/71/72%, rung starts ≈2.09 with 1.03 at the cap. The ±0.3% residues are the dossier's own documented budget-fed cadence jitter (A1 kicks 108,319 vs its 108,282/108,383 control band). The only cosmetic artifact is a stale `build.log` in `/tmp/fermi5f76/` that `analyze.py` flags and skips as `NO HEADER` — harmless.

**Claim:** `regen.sh` now regenerates every dossier number from the clean tree in 99 s, the only repair needed being the reconstruction of the zeroed `work/patch.diff` (8994's instrument patch + the disclosed `ES_SEED` knob) that the script applies.
