Working...
Check complete. `check.md` written: **Grade: silver.**

**What I did:**
- **Reproduction — exact.** Clean tree + `work/patch.diff`, both dossier commands rerun (target dir is `~/lab-target-3`). Every deterministic quantity bit-identical: kicks 34,544/15,997, Δk 4.93/4.57, residual buckets, revisit 0.825/0.968, memo exact 0.0 / quantized 0.989/0.983, 311/260 programs, digests equal. Only wall-clock µs moved 1–2%.
- **Predictions verified as pre-run** (file times 17:11 vs JSONs 17:16; priors mis-estimate µs/kick 36–58× low — a post-hoc file wouldn't).
- **Adversarial:** seeds 3/13/21 (totals 17.8–18.0 bits, revisit 0.94–0.96, exact memo 0.0 everywhere) and rtf 2000 × 50 s (131.8 kicks/body, 1.5× horizon — revisit 0.837, walk stays confined). Arithmetic on 10⁵ ships, 7.7× overshoot, belt terms all checks out.
- **The refutation:** extended the recorder with `(bucket, low-N)` histograms. Low-4 bits conditional entropy 3.98/4; low-8 7.8/8 — uniform through bit 8, no saturation. True kick entropy ≥ 49.7 bits, not ~20; per-body coded store ≥ 6 GB, not 3 GB. The "entropy-coded fits" line inverts on the author's own named-but-unprobed hole. Tree restored to author-patch state; run folder untouched except check.md.

**Verdict:** reproduced and novel (first H_live measurement; HANDOFF said "not measured yet"), revisit/compute-cap/term-ordering survive — but the headline bits-per-body number is a quantization floor titled as a value. One experiment from gold: full-resolution residual entropy + the fold-into-tube decision.
