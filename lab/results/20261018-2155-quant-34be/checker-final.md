Working...
Check complete: **Grade: gold**, written to `lab/results/20261018-2155-quant-34be/check.md`. Tree restored to pristine (patch reverted, scratch harness removed).

**What I did:**

- **Reproduced** from the dossier's commands in a clean tree (`git apply work/patch.diff` → `regen.sh`). Deterministic parts bit-exact: naive-port mismatches 166/180/215/206 per 100k, sound form 0 mismatches + identical step counts on all 400,000 tuples, census 0/400,000 ≥ 2⁶³, depths p50 4/2 max 11/7, sec/pair 2.000. Timings within shared-box noise (my wins 1.59/1.58/1.42/1.42 vs author's 1.60/1.58/1.42/1.42). The shipped `dioph` tests do pass 2/2 — `regen.log`'s `tail -3` had only shown empty trailing test binaries.
- **Predictions**: pre-registered before the decisive run (22:00 vs 22:05); the operative ones held (census, the <2× kill rule — which fired against the author's own 3–8× forecast); P2/P3 were falsified and disclosed as such.
- **Adversarial cases** (one outside the author's range): keyed belts keys=8/2 → trap doesn't fire, win 1.43–1.50×; **a=30 AU (m≈2⁴²) → naive port 41% wrong**, sound form exact, win 1.73×; worst-case Fibonacci continued fraction at belt-scale m (depth 30 vs measured ≤11) → win 1.71×, so the <2× kill survives the strongest depth attack. Dissected the mechanism: every divergence is exactly the compose product `m·y` wrapping u64 (products 2⁶⁵·¹/2⁶⁶·⁵).
- **Novelty**: e87d's page named this lever "unpriced"; nothing in HISTORY or the wiki prices it.
- **Page**: faithful; I corrected one truncated Runs line in the author's `wiki/encounters.md`.

**Noted defects (not load-bearing):** the dossier's threshold "y ≳ 2⁶⁴/m ≈ 1.3×10¹⁰" is arithmetically wrong (correct: ≈1.3×10⁸ — the port is *more* fragile than claimed, consistent with my 41% at a=30); m²≈2⁷⁴·¹ not 2⁷⁴·⁴; the 2⁶³ gap is ~1.6×10⁵ in a, not ~10⁷.

**Why gold:** fully reproduced, the premise ("all values < 2⁶³" ⇒ safe port) is refuted with an exact mechanism on the shipped class, the board-named next lever on the encounter-work bottleneck is closed by its own pre-registered rule, and the trap was caught before anyone wired it into the certificate path.
