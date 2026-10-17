Working...
**Grade: gold** — `check2.md` written.

**Verification performed (45-min budget):**
- **Reproduction:** ran `sh regen.sh` myself (13.7 s, exit 0); all 32 scene rows bit-identical across the author's record, the runner's regen, and my regen — only timing cells move (<1%).
- **Code-verified the premise correction independently:** `scenario.rs:344` belt branch ships `Scalar::raw(34, -10)` = 49.06 m (doll 0); the 12,850-km `+18` variant is the Home-doll branch — the silver's 2¹⁸ misread is code-true. Root unit ≈ 1476.9 m anchored by the "7,000 km: 4,740 root units" comment; `ENCOUNTER_LOG2 = 10` → near = 68 root = 6.7127×10⁻⁷ AU; belt genesis redraws e > 0.4.
- **The fix:** re-derived the closed-form margin analytically (stationary point of dν/dM), confirmed it numerically *outside* the author's domain (e = 0.995/0.999/0.9999: matches a 2²⁰ grid to the 1e-9 widening) and in independent Python (e = 0.4 → 0.816004).
- **Five adversarial probes, all pass:** margins at e ≤ 0.9999; querent e = 0.99 full scene (sound, keep1 92.6%); belt-side margin extreme co-located at d0 = 7×10⁻¹⁶ (kept — clamp bug was querent-side only); fresh epochs/seeds (all fractions in-band, 0 misses); short-h colocated e = 0.8 (miss 0, miss_old 1 — margin, not tk, is load-bearing).
- **Predictions** predate the run and held; the one failed band (short-h series keep) is honestly disclosed with a corroborated mechanism.
- **Wiki page:** every number in the new paragraph matches the record; the author even fixed the dossier's trivial "2.8 ns" lower edge to 2.7. No correction needed.

The named gold experiment from the silver (regenerable, all-seed, true-point record + e < 1 soundness) is done; the wiring of integer widenings and the 10⁶ λ-index stay open, as the dossier and page honestly scope.
