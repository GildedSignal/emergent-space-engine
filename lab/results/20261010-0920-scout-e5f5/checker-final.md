Working...
`check.md` written. Summary of the check:

**Grade: silver.**

**Reproduction** — clean tree, scratch copy (the script writes `out/` relative to CWD):
- Shipped `news_scale.py` → `out/results.json` **bit-identical** (141 s, 1.68 GB peak).
- v2 numbers regenerate **exactly** by deleting the disclosed v3 block (flush 18.581736246744793, t=6 err 0.2383978588454863, n_flushes 3873 — match `results-v2.json` to the last digit).
- v1 regenerates only approximately (t=6: 2.287 vs 2.32; t=4: 0.39 vs 0.95) — exact v1 code unshipped; the compounding conclusion holds either way. `work/patch.diff` empty.

**Held-out** — `predictions.md` predates the decisive artifacts by ~18 min. Cost predictions held (exponent 0.027 ≤ 0.3, fleet 1.48×10⁴, bursts 1.3–1.5, controls both sides passed); two misses, both disclosed by the author (the ≥10⁵ ratio; the ≤6q error bound, whose failure became the run's finding).

**Attacks (4)** — heavy-tail strengths: MC 228.7 vs closed form 227.2 (0.7%); clustered density: 1.74× constant, exponent intact; T=12: v2 compounds to 228q, v3 plateaus at 7.5×10⁴q (author's classification confirmed); seam receivers: worst leak is near member-flush centers, not seams — the structural claim survives, sharpened.

**Novelty/goal fit** — first measurement of the news-delivery cost side (law.md adopts the physics, memo step 5 defers the cost, the queued `q-gravity-cursor` probes agreement only); attacks register risk OC#50 and quantifies R5-literal as DOA (10¹⁸ words at 10⁹).

**Gold-blocking experiment** — per-(cell, shell) FMM accumulators in this harness, error ≤ L·q non-growing at O(1)/body, MC-anchored at two sizes.

**Flagged** — q-unit slips (worst leak is 1.4×10⁷q, not 3.6×10⁴q); "measured exponent" is a closed-form fit anchored at one N; the delivery-formula correction v1→v2 is only visible in run-logs; in-flight memory under-counted 3–4×; v1 unshipped. Nothing else in the run folder was touched; no git commands run.
