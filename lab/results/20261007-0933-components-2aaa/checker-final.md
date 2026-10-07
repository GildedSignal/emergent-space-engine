Working...
Check complete. **Grade: silver** — written to `lab/results/20261007-0933-components-2aaa/check.md`.

**What I did:**
- **Reproduced** the full 90-config run in a clean tree (178 s): 0/30 hash mismatches, heap 98→443 ns/op growing with N, wheel flat 18–93 ns, median ratio 4.6–6.6× at N ≥ 10⁷, amortized 1.7–3.3×; the heap2 control loses 1.20–1.50× at scale; deterministic artifacts (chain 44,943/44,742 at wide 3×10⁷) match the author's stored results exactly. Mean divergences at two configs are shared-runner tail noise; no conclusion flips.
- **Verified the mirror claim**: `ih_up`/`ih_down`/`ih_remove_at` are line-for-line `calendar.rs`'s `up`/`down`/`remove_at`; the plane.md and world quotes check out (the latter lives in `crates/universe/src/world.rs`, not "world.md").
- **Predictions**: mtime order confirms predictions.md (09:45) predates both result files; the author disclosed both misses honestly.
- **Four adversarial workloads**: ultra-dense (interval 1 for all), synchronized burst, non-dyadic intervals, and 2³⁰–2⁴⁴ span. First three: hash-identical, oracle passes, wheel still wins. The fourth found a real missed boundary — **at sparse tick density the wheel inverts to 3.5–7× slower than the heap** (one cascade per empty window; 88,774 cascades/300k pops). Correctness holds; it is a performance cliff bounding adoption to tick-dense regimes, absent from the dossier's "what would make it wrong".
- **Novelty**: no prior queue-floor/wheel work in HISTORY or git log; noted the uncited textbook prior art (Varghese–Lauck).
- **Named a reporting defect**: the dossier's "heap4 p99/p50 ~75–98× at N ≥ 10⁷" exists only in the discarded transient run; the final results show 1.2–1.7×.

Silver, not gold: measured 4.6–6.6× median / 1.7–3.3× amortized is below the lens's own 10× bar, and the gold-making experiment is the one the dossier already names — phase rings priced per surprise, which my sparse-tick finding says must be included. Nothing else in the run folder was modified; all reproduction work lives in `/tmp/check-2aaa`.
