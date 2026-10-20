Working...
Fixed. Two defects, both now proven dead by a full end-to-end run (`EXIT=0`, `regen done`, 97 s wall):

1. **Line 9 `cd … work` failed** — the runner restores the tree before regen, so `work/` doesn't exist at that point (it's my session scratch; only `patch.diff` is contractually present, applied by the runner). Fixed by anchoring on the script's own directory (`RUN_DIR`/`REPO`, immune to the runner's starting cwd) and `mkdir -p "$RUN_DIR/work"` before `cd`.
2. **Latent SIGPIPE abort (exit 141)** — `set -o pipefail` + pipelines ending in `head`/`awk … exit` kill the upstream `grep`/`sort` with SIGPIPE; `set -e` then aborts mid-analysis. The original failure at line 9 masked this. Dropped `pipefail` (analysis consumers all exit 0; the flights already carry `|| true`).

Proof run applied `work/patch.diff` exactly as the runner does (the `ES_ANSWER_ANATOMY` instrumentation lives only in the patch, verified), ran regen.sh from outside the repo, then reversed the patch — tree restored (`git status`: only untracked `lab/results/`). Regenerated numbers vs dossier: integer-decided values exact (cand 299,715/99,715, answer cand 2612/1804, skip_dom 2607 = 99.8%, enc 3, RSS 1,957 MB, 126 ALL walks at 1e5); wall-clock values same-class (11.01 vs 11.07 ms top answer, 4.21 µs/body, 0.28 µs/body capture, biggest answered 2612 vs biggest captured 299,717), within the dossier's disclosed timing convention. No other file needed changing.

Claim: `regen.sh` now regenerates every dossier number from `work/patch.diff` + shipped code unattended (exit 0 in ~100 s), after fixing the runner-time missing `work/` dir and a masked SIGPIPE abort.
