Working...
Check complete. `lab/results/20261004-1525-system-d1d1/check.md` written; tree restored to main (only the untracked `lab/results/` remains).

**Grade: silver.**

What I did:
- **Reproduced** everything from a clean tree with the patch applied: `memo_bench` cutover 3.55× (37.3→10.5 µs; author 3.74×), deterministic columns identical digit-for-digit (codeΔ 0.000/0.190/0.667, flyby hit 0.000), all 22,000 exactness asserts pass; kick-bench 23 samples/0 refused, median 49.0 µs (author 40.4, shared container); tests 50/0.
- **Adversarial cases (3):** (A1) the quantization bucket costs up to 4.4×10⁻⁴ relative period error — the number the B-gate re-freeze must judge, never measured by the author; (A2) the headline "key change rate ≈0" fails early: e=0.95 at the author's *smallest* kicks gives codeΔ 0.724, strong-field e=0.6 at 2⁻²⁰ gives 0.923, and bound near-parabolic e=0.999 gets nothing (hit 0.407, 120.5 vs 120.9 µs) — the memo's hard case is a population class, not just flybys; (A3) aliasing soundness holds.
- **Novelty:** the memo's existence, 12+12-bit widths and weak-field hit rate are prior art (bba2d57, Astra's envelope; `law.md` State declares the wiring); Sol's kick arithmetic is on main (1932f6c). New: the kick-path cutover with event-exactness, the key-change-rate certificate measurement, the fit-dominated floor (readout 3.3 µs).
- **Predictions:** mtime order consistent (15:31 < 15:39) and internally convincing (P3 honestly held-failed), but `run.log` is empty — pre-registration unauditable; noted.

Why silver: real, reproduced, adoptable in one step, but the 10× bar fell by the author's own P3 and nothing is deleted. The gold experiment: wire it into `crates/universe`'s bind path plus the certificate step, re-run B-gates and digests with high-e and near-parabolic populations in the mix.
