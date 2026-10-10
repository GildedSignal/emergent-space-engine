Working...
Check complete. Verdict written to `lab/results/20261010-0448-inversion-03c1/check.md` — **Grade: silver** — and the tree restored (author patch and my experiments reversed; only `check.md` added to the run folder).

**Reproduction:** every counted field of all 25 evidence.log lines regenerates bit-exact from `work/patch.diff` in a clean tree (only wall-times differ, ~25 s total). The one gap: `ring600` is claimed in P1 and the dossier but has no line in evidence.log — I ran it: fires, 17 encounters, 0 missed, 0 false (claim true, log incomplete). Build 152e confirmed never executed (0-byte run-log, 429 in checker-final) — "first execution" is accurate.

**Predictions:** P1/P3/P4-decline/P5 held; P2's pre-registered kill (<5% certified at σ_e 0.02) failed against the author's own criterion and is honestly reported as failed, with the transitive-closure mechanism verified in code.

**My three attacks:**
1. **Forced high-e fire** (fixed e 0.7/0.85, aligned ϖ, tight λ̄ — fires where every author scene declines): the watch is **sound** — 141–270 encounters, 0 missed, 0 false. Closes the dossier's admitted untested half, in the certificate's favour. But at e 0.85 the train costs *more* than the pairwise tier (370,870 vs 168,820 evals/enc) while ζ reports 0.077 — ζ gates pair count, not sweep cost.
2. **a-dispersion** (author pinned a to ±1e-5 everywhere): at σ_e 0.02, a ±1e-3/±3e-3/±1e-2 → certified 66.6/11.0/0.5%, admitted 11.3/28.6/50.2% of all pairs ≈ 8/21/36 TB at 10⁶. The oasis is narrower than reported; the 0.7–12.6 TB headline is a lower bound.
3. **Second latent ζ bug:** the spread loop misses the circular wrap gap, so tight-λ̄ clumps get spread ≈ TAU and ζ under-reports ~100× (code 0.055 vs honest 5.4 on my e 0.7 scene). I audited honest-ζ on all author scene families: no fire/decline decision flips — latent, same over-fire class as the author's δ bug.

**Silver, not gold:** the headline dispersion premise was already gold-killed twice (efc9, 6f01) on fixed-rank proxies — the new content is the shipped design's first execution (sound where the kills died), the trigger's calibration, and the silent-declined-budget finding; the 10⁶ figures are n=600 extrapolations; the author's own kill didn't land. The gold-making experiment: run the shipped binary at 10⁵–10⁶ with joint (a,e) dispersion and both one-line ζ fixes, measuring the store instead of extrapolating it.
