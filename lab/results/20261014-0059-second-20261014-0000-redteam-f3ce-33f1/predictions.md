# predictions.md — written before any Q = 2²⁰ run

Written after instrument development only (Q = 2¹⁶ diagnostics in `run.log`: the
Fermi-pumping mechanism, per-contact dumps). No 2²⁰ measurement exists as of this file.

1. **shipped / frac_1000_1_median (the rung's kill): FAILS the 1% bar.** Predict median
   ≈ 2×10⁻² over seeds 0–4 (plausible range 5×10⁻³–10⁻¹). Reasoning: the γ ~ 30–100
   dance is Q-independent in continuum; the per-contact step fraction scales ~1/Q
   (checker's ladder, 30–100× over 64× Q), so the 2¹⁶ median (~0.16 on the original
   β 0.3–0.7 draw) lands near 10⁻² at 2²⁰ with the rung's fixed β 0.6 (stronger pumping).
   **Disclosed risk:** this is within a factor ~2 of the bar. If it lands under 1%, the
   shipped law passes the frozen negative and the rung's verdict is VOID — then the
   honest finding is that the checker's 1%-at-200-contacts bar overstates severity at
   the engine's Q, and I report the measured number and the contacts-to-1% horizon
   instead.
2. **shipped / frac_equal_median: PASSES ≤ 10⁻³.** Predict 1–5×10⁻⁵ (checker measured
   2–3×10⁻⁵ at 2²⁰ on 3 seeds of the same scene class).
3. **pair-carry / frac_1000_1_median: PASSES ≤ 0.01.** Predict 10⁻⁴–3×10⁻³: the carry
   bounded by ~one quantum of the max-ΔE body per contact. The max-ΔE body switches
   from heavy (low γ) to light (γ ≳ 10), which is the point of scaling to the pair.
4. **pair-carry / frac_equal_median: PASSES ≤ 10⁻³**, predict ≤ 5×10⁻⁵, within ~3× of
   shipped's (J = 0 while owed stays under one quantum; most contacts never widen).
5. **Ledger exactness holds under both configs at every contact** (the fix only changes
   which candidates are scored; e is recomputed from actual four-momenta).
6. **Determinism:** identical runs give identical digests under both configs.
7. **Held-out seeds 11–15 (run only after the dossier's main tables):** same classes as
   0–4 for all four config×scene combinations.
8. **Momentum carry under the fix** (reported, not gated): bounded, ≲ 10⁻³ of one
   body's |p| scale; the shipped law's momentum carry on the pair scene may walk
   alongside the energy (same quantum), reported either way.
9. **`cargo test -p emergent-lattice` with the flag off:** unchanged, all green. With
   the flag on: digest-pinning tests that exercise contacts with nonzero owed will
   differ (it is a law change); I will report which.
10. **Mechanism check at 2²⁰ (diagnostic, after the decisive runs):** the light body's
    γ exceeds 20 within ~20 contacts on most seeds; the largest per-contact |e_E| under
    shipped occurs at the highest γ, scaling as γ³|k|/KE.

## Revisions before the decisive runs (disclosed instrument history)

All at the 2¹⁶ instrument stage, before any 2²⁰ measurement:

- **Seed sampler fixed.** The LCG's low-bit `range(2,5)` draw is constant across
  consecutive seeds (small-period artifact): the first frozen scene had one effective
  y-offset and zero seed diversity. The sampler now draws y-offsets from the LCG's
  high-entropy `f()`. The parent run's pair arm had the same constant offset; its
  diversity came from its β draw.
- **Fix redesigned twice.** Form 1 (wide radial window, J cap 64 then reach-sized):
  worse than shipped at 2¹⁶ — no fidelity anchor. Form 2 (single owed-equivalent
  target shift): engages but cannot repay the fresh corner error. Form 3 (per-corner
  in-contact repayment, the frozen form): engages at both Q. One silent no-op bug
  found and fixed on the way (a rational cone check comparing numerators against the
  integer cone).
- Predictions 1–10 above were written against the frozen bar and the form-3 fix; they
  are scored in the dossier as written, not revised.

## Post-run verification note

The corrected sampler's `(1 + 3f) as i64` truncates to 3 y-offset classes: seeds
collide pairwise (1≡3, 2≡4; the held-out set 11–15 reproduces the same three t
values). The rung's medians are medians over a 3-class multiset; disclosed rather than
re-run, and logged as the sampler rule's second lesson: draw seed geometry at
single-quanta granularity, never through a coarse integer truncation.
