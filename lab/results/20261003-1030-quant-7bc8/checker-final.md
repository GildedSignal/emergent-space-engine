Working...
Check complete. `check.md` written to `lab/results/20261003-1030-quant-7bc8/`; tree restored to HEAD; nothing else touched.

**Grade: silver.**

**Reproduced bit for bit** (baseline binary saved aside, then `git apply work/patch.diff`, rebuild 28 s):
- Baseline seed 1: 1,912 samples, refused 0, digests `e9d41fe8…`/`75029952…` — exact.
- Instrumented seeds 1 and 7: digests unchanged, intern_exact **0/1912 both**, memo **1875/37** and **1878/34**, stage shares fit 27.8–30.6% / compile 30.2–31.6% / quadrature 27–31% / `from_state` 37–39% of kick — all match the dossier.
- Closed the author's gap: uninstrumented seed 7 run gives the same digests, so outcome-neutrality holds on **both** seeds, not one. My quiet-box overhead was 0.4% (20.18→20.26 µs), confirming the author's 18.8→25.6 µs was contention and the shares are valid.
- Pre-registration verified by mtimes: predictions 10:34:40 < kickbench JSONs 10:44:13–14 < metrics 10:44:55 (run.log empty — noted).

**Adversarial findings:**
1. Longer horizons: rtf 1000/3000 → 98.89%/98.74% recurrence over 6,338/13,256 kicks; distinct keys grow sub-linearly (37→70→167).
2. **The bench cannot test diversity(N):** `--members 4` vs `400` leaves the sampled kick stream bit-identical (same replay digest, same 1875/37) — the named gold experiment needs a new scene generator.
3. Seed 3: different stream, identical counters — the statistic is stream-stable.
4. "fit_key is the largest single stage" inverts in 3 of 4 runs (including the author's own seed 7); the honest claim is fit ≈ compile ≈ 30% each.
5. rtf 1e6 crashes the bench; the "~15% saving" is really ~10–12% (quadrature share of the whole kick).

**Not gold:** nothing adopted or deleted, no project premise killed (the intern was the lens's own configuration), P1 failed, and the memo bet was already in representation.md ("Identical invariants share one memoized cycle, as in Hashlife") with `QuantizedMemo` existing since H0209 — the run's new facts are the exact-key zero (the memo *must* ride a coarsened key) and the first measured 98% hit rate in the real kick stream.
