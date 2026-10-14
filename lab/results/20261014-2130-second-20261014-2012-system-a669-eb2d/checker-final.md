Working...
Check complete. `check.md` written; the author's page corrected in place; the tree left pristine (scratch runs in `/tmp/check-eb2d.uoW4`, outside the repo).

## Verdict: gold (as a refutation)

**Reproduced.** The runner's `regen.sh` regenerated the full dial table, the neutrality verdict (IDENTICAL) and all four Jacobi arms; I re-checked every `work/` record against the dossier — all match (one typo: 24,16 kicks are 33323, not 33223).

**My adversarial arms, all consistent with the kill:**
- **Identity control `48,62`** (untouched by the author): wave counters bit-equal to default, but the digest moves — the quantizer is a last-ulp law change even at full width, and the **Jacobi readout panics at this ~0-reuse dial while coarser (16,32)/(20,36) arms run**. So the dossier's "panics at 13.6% reuse" is a mis-attribution: a `quantize()` rounding-boundary fragility, not the walk. The load-bearing exactness evidence is the 30–500× / ~900–1600× degradation, which stands.
- **Untested `(12,20)`**: map-safe (encounters 928, refused 1) with reuse 0.430 → the best measured map-safe cut is **1.75×, not the dossier's "largest map-safe point (12,24) = 1.33×"**. Still ≤ 2× — the refutation is untouched; Jacobi at (12,20) panics like (12,24), so "no dial has material reuse and a held walk" survives.
- **N=10⁴ (outside the author's range)**: mint still exactly 1.00 compiles/kick (41,606/41,537); `(12,24)` still map-safe (reuse 0.207, encounters 928).
- **Patched-default Jacobi = pristine baseline exactly** — neutrality extends to the instrument the author never ran it on.

**Why gold:** the record regenerates end-to-end and beyond its domain; it kills a live silver's adoption path (a669's ~10²× dial arithmetic is ~600× wrong on shipped code) before the integrator spends a step; the mint becomes a counted fact (1.00/kick, held at 10⁴); the failed predictions are the pre-registered failure branch, honestly reported. Adoption cost is the record itself: the wiring is default-neutral, and the surviving lever is the non-walking key (integer phasor), not a coarser quantum.

**Page corrections applied:** map-safe frontier is scale ≥ 20 (best cut 1.75× at 12,20), panic de-linked from reuse, plus a checker note with the typo.
