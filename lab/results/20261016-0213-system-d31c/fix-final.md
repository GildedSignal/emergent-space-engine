Working...
Tree clean (`?? lab/results/` is the untracked run folder itself — its pre-existing state). Fix complete and verified.

**What was broken:** `regen.sh` walked four levels up from `lab/results/<run>/` but the checkout root is three levels up (`…/emergent-space-engine/lab-3`), so cargo ran one directory above the repo; a second latent bug used a relative `$0` for a later `cd`; and the build didn't target the directory `grid.sh` reads its binary from (`/home/glmlab/lab-target-3`).

**Fixes (only `regen.sh`, plus one dossier number it regenerates):**
- `cd "$RUN_DIR/../../.."` with `RUN_DIR` made absolute — cwd of invocation no longer matters, both cds corrected;
- `CARGO_TARGET_DIR=/home/glmlab/lab-target-3` exported so the build refreshes the exact binary `grid.sh` flies;
- dossier's "48 tests" corrected to 77 — the original record (`out/suite_on.txt`) and the regenerated sum both say 77; 48 was a transcription error.

**Proof (ran the runner's exact flow: patch applied → `regen.sh` → patch reversed):** build 12 s; all 7 flights' digests pair OFF↔ON bit-identically; pass 33.2–34.8 → 22.7–23.7 µs/body (dossier table, −31%/−28%); suites `memo-off: passed=77 failed=0`, `memo-on: passed=77 failed=0`; total ≈ 9 min, inside the 15-min budget; working tree restored clean so the runner's own `git apply` of `work/patch.diff` proceeds unconflicted.

**Claim, one sentence:** `regen.sh` now regenerates every dossier number end-to-end from `work/patch.diff` in ≈ 9 minutes on this box — digests bit-identical OFF↔ON at all seven flights, pass 33.2–34.8 → 22.7–23.7 µs/body, both suites 77/0 — verified by running it.
