Working...
Check complete. Tree restored to pristine base; only `check.md` and the corrected `wiki/kick-jet.md` were written in the run folder.

**Grade: silver** (`lab/results/20261016-1120-quant-5ade/check.md`)

What I verified:

- **Reproduction.** The runner's `regen.sh` exited 0; every deterministic number regenerates exactly (W_TAUT 389,211→11, W_TAU0→1, repeat share 0.296, digests `0d8ced80…`/`07891363…` identical across arms, off-arm identical to pristine main). My re-run confirms the timing structure; absolute µs sit ~12% below the dossier (shared-box load, disclosed), ratios hold (fired kick −15.5% vs −17%, wave CPU −9.2% vs −10.2%).
- **Code-level exactness.** `readout_with_state` is line-for-line the shipped `readout` with the orbit state kept; `bind_in` decodes at the same `t` that becomes `event_time`, so `anchor_proper` caches exactly what `old.orbit_state(old.event_time)` re-derives; bindings are immutable, so the cache cannot go stale.
- **Adversarial cases, both outside the author's range.** N=2×10⁵ first wave (2× the decisive N): digest identical, W_TAUT→0, W_TAU0 first-kicks-only. A WH-dominated 70–400 ks window at 2×10⁴ (mix flipped 68/31, encounters 4×, repeat share 0.651): digest identical, W_TAUT 731,015→13, W_TAU0→1, wave CPU recovering ~82% of the deleted walks.
- **Predictions.** Pre-registered with kill criteria; 5/6 held; the failed one (source-repeat ≥0.6 vs 0.029) is reported honestly and kills the memo lever — itself evidence of genuine pre-registration.
- **Novelty (the one real gap).** The anchor-half carry re-derives `20261010-1947-autoresearch-2833`'s unadopted `proper_at_event` cache (silver, microbench); new are the t-walk carry, the decomposition, the memo kill, and the apply-walk pricing. I corrected the author's page to cite 2833 and to fix a double-count I found (W_BIND's clock sits inside FIT's, so "fit + bind decode" counts the decode twice; walks+fit ≈ 93% of the item, not 95%+3.8).

Not gold: 1.2× built (1.5× priced) against the 10×/component-deletion bar, one carry half re-deriving known work. The named experiment to gold: build the apply-walk carry and re-price on the M1 — but that lands ~1.5–1.6×, so gold would require deleting the position-walk component outright, not shaving the cycle.
