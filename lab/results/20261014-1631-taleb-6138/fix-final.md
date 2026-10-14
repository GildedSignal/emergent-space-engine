Working...
Fix verified and the tree is restored to clean (only the untracked run folder remains, so the runner's patch application won't collide).

**What was broken:** `regen.sh` line 6 resolved the checkout root four directories up (`$here/../../../..` → `/home/glmlab/actions-runner/_work/emergent-space-engine`, which has no `Cargo.toml`); this job's checkout is one level deeper at `.../emergent-space-engine/lab-1`.

**Fix:** one line — `D="$(cd "$here/../../.." && pwd)"`.

**Verification, each step of `regen.sh` exercised exactly as the runner will:**
- `work/patch.diff` applies cleanly on the restored tree (`git apply --check` passes).
- `cargo build --release --manifest-path <lab-1>/Cargo.toml -p emergent-universe --example nladder --example belt_first` succeeds (9 s; deps warm in `CARGO_TARGET_DIR=/home/glmlab/lab-target-1`, which line 9 already honors).
- `belt_first 20000` and `nladder` with the exact `fly` env block (`NLADDER_MAX_S`/`NLADDER_TRACE`/`NLADDER_SEED`) run to exit 0, including full-size args `200 100`, and emit every line format `table.py` parses (`ladder:`, `belt:`, `worst frames`, `frames over the budget`, `the player's doll`).
- `python3 table.py` reproduces the dossier table from the existing `raw/` files (exponent 1.94, all arms, belt row).

The record now regenerates: the wave-flight burn's worst-frame superlinearity (exponent 1.94, 10⁵→2×10⁵) is reachable from shipped code via the corrected `regen.sh`.
