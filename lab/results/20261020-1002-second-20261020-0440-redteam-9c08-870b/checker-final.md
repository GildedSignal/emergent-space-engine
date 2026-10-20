Working...
Check complete. Summary of the check I wrote (`check.md`):

**Grade: silver.**

**What reproduced exactly:**
- `regen.sh` (44 s, ~275 MB): metrics byte-identical both seeds, verdict `PASS` identical, rung sha256 `ed91f4c0…` verifies.
- The struct read is verbatim-true on the 959a branch: `e.lum += row.luminosity` with `row.luminosity = lum·shift⁴`, served `luminosity: lum` — the shipped record already stores the exact per-member seen-flux sum. 9c08's brightness kill hits a readout the record never serves; its cure was already shipped.
- Verdict semantics hand-checked; PASS is correct (candidate passes all 4 criteria, negative fails bright+colour, positive passes).

**Why not gold — one headline the log contradicts, one misreported prediction:**
- The dossier claims the γθ_f collapse holds "in 2D at the p99 readout… to 4 digits (0.628794 both floors at γθ_f=4)". Its own evidence table reads **0.708354 fine vs 0.628794 stock** (and 0.2688 vs 0.2784 at γθ_f=1). I re-ran 3 seeds: 1.127× systematic. The author read the forward-cell column (which does collapse) as the p99; P7 reported as held when it half-failed. Verdict unaffected — both floors fail the negative ≥14×; the E(γθ_f) law stands for the continuum, 3D p99 and 2D saturation.

**Adversarial (one beyond the swept range):** γθ_f→10⁶ — one-shift still fails (0.77), and frozen B=128 holds colour ≤0.060 oct (~40× beyond its claimed domain — candidate stronger than stated). Heavy-tailed luminosity doesn't rescue the negative (p99 0.785). The `lc/lum` "linear-mix identity" is false for the shipped `blackbody()` (per-member max-normalization + 1/2.2 gamma before the mix: ≤0.5 oct on mixed temperatures) — γ-independent, so the substantive "no k needed" guard survives; wording corrected.

**Page corrections made in place:** the collapse line now states its true domain, the "identity" claim reworded, predictions count 6/8 with P7's misreport named.

**Gold path:** re-fly the floor-split as its own criterion (it strengthens the negative) with the record corrected — every number already regenerates from the shipped script.
