Working...
Check complete. Summary:

**Grade: gold** — written to `lab/results/20261018-0143-system-f102/check.md`, with three corrections folded into the author's proposed `wiki/scan-queue.md`.

**What the run claims:** the scan memo's reuse walk is the memo's soundness proof, not overhead — no change-signal coarser than the candidate set certifies a duplicate — killing scan-queue direction (d) ("memo the candidate list") and relocating the lever upstream to the re-timed pending kick.

**Verification performed:**
- **Reproduction:** patch hand-applied on base `39a24a84`; all load-bearing cells regenerate — burn 10³: 217/453 duplicates (47.9%), `both_hit=0`, `cheap_only_soundness=0`; coast inert; 10⁴ held-out holds. 10³ digests bit-identical across modes and load levels; the 10⁴ digest's load-dependence is disclosed and my runs confirm both values (`81e5739a` at load ~7–11, `86690d0c` at load 5.1). Suite on patched tree: 77 passed / 0 failed.
- **Adversarial (3+, one outside the author's range):** held-out seeds 7/23 → 48.3%/47.6%; **N=0** (bare 28-body world) → 0/213 certified, which kills the author's own "belt ships" mechanism sentence while strengthening the kill; **N=10⁵** (one decade past) → 47.3% duplicates, structure intact; 10⁴ off=on digest equality.
- **Predictions:** existed before the final runs; 1–3 held, 4 half-failed (price at 10⁴) — disclosed and correctly diagnosed; my 10⁵ arm corroborates the diagnosis.
- **Instrument:** `sloppy` is the planted-fault path, so the comparison is real candidate-list equality; captures cannot bump the versions they read — the zeros are facts.

**Corrections to the page:** 0.24%-of-wall → ~0.5% (arithmetic didn't close); belt-ships parenthetical scoped as one instance (N=0 evidence); the "two pages, one repair" unification scoped — the memory page's byte fence is untouched by this run; open-direction (d) marked killed.

**Not blockers:** the intermediate global/guard-only arms aren't regenerable from the final patch but are implied by the measured finest arm; `both_hit` never fired anywhere (no positive control exists — noted as the one instrument gap). Tree restored to base; only `check.md` and the page changed in the run folder.
