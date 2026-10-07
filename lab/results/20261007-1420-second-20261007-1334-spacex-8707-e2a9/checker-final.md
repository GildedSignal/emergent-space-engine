Working...
Check complete. `check.md` written to the run folder — **Grade: gold**.

**What I did:**

- **Reproduction (all bit-identical in a clean tree):** the port proof (`--sampler orig` vs the shipped branch record, every original key), all six decisive runs (317 s wall vs ~290 s claimed), the null control, and `aggregate2.py` regenerating `aggregate2.json`. Verified `orig/` matches the `claude/lab-20261007-1334-spacex-8707` branch byte for byte, and the sampler matches `belt.rs:SPEC` exactly; the placement math checks against the repo's own constants (`STAR_RADIUS 471_000`, Home periapsis `99_300_000`, `AU 101_300_000`, Giant 2⁻¹⁰ at 5.19 AU).
- **Predictions:** timestamped before the decisive outputs; 6/7 held, the one failure (b16 exponent 0.013) is disclosed and strengthens the claim — the quiet placement saturates with zero q=3e-3 crossings.
- **Relabels verified against the shipped record:** 10/10/20 and 50/50 yr (vs the mislabeled 6.2/21.7), 24.29×, and I regenerated the 3.7e-2 early rate on the fraction basis (seed 7: 0.774/20 = 3.87e-2) — it stands.
- **Five adversarial probes, all supporting:** held-out seed 11 (rate 1e-3, T* 5, exponent 0.626); causal refit (−0.6% on residual, rates unchanged); dt halved (statistics unchanged to five decimals — the e≤0.6 tail doesn't break the dt=0.1 slab map); ejection channel counted directly (1/30000 per seed = 3.3e-8/body/yr, the NaN-silent wart I flagged); q-insensitivity on the record.
- **Novelty/goal fit:** this is the silver's checker-named gold experiment, closed at both defensible placements — rate 1.22× at the loaded 2¹⁷ placement (inside the 5× bound), and the plane genuinely has no `belt_birth`, so the harness route was the only runnable one.

Nits recorded for the integrator: the "no Jovian MMR inside b16" wording (6:1/7:1 are inside, high-order), the 13× seed spread behind the session-lag median, and the O(1)-scar-per-crossed-body assumption in the ≤4 GB bound. No git operations; only `check.md` touched.
