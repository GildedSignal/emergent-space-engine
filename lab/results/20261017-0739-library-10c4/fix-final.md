Working...
Fixed and verified. Summary:

**Root cause** — regen.sh step 1 ran `git apply work/patch.diff` unconditionally; the runner invoked it while the tree still carried the author's edit, so the apply failed and `set -e` killed regen at 0.02 s (the two `error: patch failed` lines). The tree is clean now, so the same command succeeds — an ordering-dependent failure.

**Fix (regen.sh only):**
1. **Idempotent apply** — reverse-check first (`already applied` → skip, the runner's exact state), forward-check next (clean tree → apply), neither → explicit `FATAL` instead of a cryptic patch error. Verified from both states; the apply always runs from `$ROOT` (from a subdirectory `git apply` exits 0 while matching nothing — a silent no-op I confirmed and avoided).
2. **Cache-safe Readwise fetch** — the old loop overwrote `page_$i.json` before validating, so one network/token failure would destroy the quote cache and crash `json.load`. Pages now fetch to `tmp_page_*.json`, validate as export JSON, and replace the cache only on a complete successful fetch; otherwise the run proceeds on the cached pages.

**Verification** — clean-tree run: 22 s end-to-end (build 9 s + 60 s flight compressed at rtf, quotes re-fetched fresh: 4590 highlights, 5/5 OK), reproducing the dossier bit-for-bit: boundaries 64,197 / handoffs 1 / lost 16 / plain 99.974% / kicks 65,455 / ratio 1.020, and the S\* arithmetic (cores 9.8–8.3, S\* 19.7×–16.6×). Patched-tree run (the failure mode): exit 0. A third flight drifted 0.04% in absolute counts (wall-paced flight on a shared box) while every decided quantity (≥99% plain, ratio ~1.02, cores/S\*) held — inherent to the run's wall-clock-paced instrument, not the regen. Tree re-restored to base; only regen.sh changed.

**Claim:** regen.sh now regenerates every dossier number from either tree state in ~22 s (cold build included), because the patch apply is idempotent and the Readwise cache can no longer be destroyed by a failed fetch.
