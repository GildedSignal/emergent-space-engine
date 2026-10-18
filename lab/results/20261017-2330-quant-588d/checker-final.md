Working...
Check complete. Summary:

**Grade: silver** — written to `lab/results/20261017-2330-quant-588d/check.md`.

**Reproduction.** Applied `work/patch.diff` myself at the run's base `d28f9352`. Runner's regen and my own arms agree with the dossier to the 3rd–4th digit on every hit rate and class count (cycle totals −1.6%, inside the disclosed ±3% wall truncation); `quant_err=0` everywhere; digest controls bit-identical (`d2632de9…`, kicks 34537, encounters 934, contacts 0).

**Adversarial (3, one outside the domain):**
1. **N=30000** (3× the author's max): shape-class hit 0.9926 at **1,656 classes** — 1.11× classes for 3× bodies. Saturation holds at the next decade; exact still dead (0.0001). Quant cell hit falls to 0.861 (~1.04 cells/body) — the dossier's quant range doesn't extend, corrected on the page.
2. **Burn N=3000** (regime never censused): shape 0.9913 at 1,324 classes. Holds.
3. **Digest neutrality on five untested cases** (belt-crossing both N — including d399's `4995f384…` — and key-mashing all N): all bit-identical.

**Boundary claim given a count proof the author left implicit:** cycles 154,992 ≈ kicks 154,043 (1.006×) while boundary events number 152,489 ≈ kicks — boundaries demonstrably add no `from_state` fits.

**Not gold:** nothing adoptable in one step — the compile's quadrature-vs-glue split (the delete's actual size) is unmeasured and the serving key is a law decision; the exact-memo kill extends memo.rs's known law rather than overturning a live premise. The gold experiment is named: split the 12.33 µs compile on the flown corpus + probe `from_shape(exact, quantized)` exactness.

**Page corrections:** the "0.9917–0.9924" range now includes the pre-registered rtf-600 arm (0.9784); "3.04× bodies" → 3.3×; checker brackets added (domain extensions, digest cases, count proof). Also flagged: the patch's `Print` drop-guard is const-init TLS — its `end`/`top10` output never fires (dead instrument code, harmless).

Tree restored pristine; temp binaries removed; nothing else in the run folder touched; no git commands run.
