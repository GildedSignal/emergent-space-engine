Working...
Check complete. **Grade: silver** — written to `lab/results/20261008-0148-components-df14/check.md`; tree restored pristine; nothing else in the run folder touched.

**What I did**

- **Reproduced bit-identically**: applied `work/patch.diff` to a clean tree, ran all three dossier commands — CSVs md5-identical (including the stride-2 file rebuilt through my own gzip+awk pipeline), digests and event totals match, `analyze.py` output byte-identical.
- **Controls verified**: kick-bench `digest`/`replay_digest` identical pristine vs patched; `--h-live` deterministic across three executions. P3's refutation is real in code (prune every 64 frames at 2× light distance), and law.md line 13 really does say "+62 bits per kick and −60 per reabsorption" — my first grep missed it to display truncation; P6's citation is legitimate.
- **Adversarial**: held-out seed 3 → 63.9 bits/kick; 50-member fleet → 64.7 (both inside ±10%); frequency-entropy saturation confirmed (16.5 vs log₂n = 16.6 — the method result stands). Found `--members` is CLI-clamped to [4,400], so the billion-body projection rests on one system size. Probes the author missed: the shape term omits **sign** (+1.93 bits → floor 62.1, making law.md's +62 *exact*, not "3% honest"), and delta-coding each body's log against its previous dv saves ~10 bits — the "exact floor" is coding-dependent (~50–62 bits), an upper bound.

**Why silver**: fully reproduced and the assigned "H_live not measured yet" gap is closed with a correct method, but the 88×→1.12× varint-scar store is measured ex ante, not built, and the brief's `--bench`/page wiring and tests are undelivered. Also noted for the integrator: the patch silently removes `--unpaced`, and `analyze.py`'s "kept forever (no prune)" line contradicts the dossier's own correct P3 refutation.
