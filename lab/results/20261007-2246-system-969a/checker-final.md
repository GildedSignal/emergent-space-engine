Working...
Check complete. Summary of what was done and found:

**Reproduction — exact.** Both probes re-run in a clean scratch copy (`/tmp/check-969a`, so the author's JSONs stayed untouched) produce **byte-identical** output: `store_probe.py` (25 s) and `ctrl_probe.py` (55 s). Every dossier number matches the stored JSONs (S1 75 206 median candidates vs 2×10⁵ Cartesian; kick median move 2 cells, 15 % unchanged; ctrl 0 misses / ctrlA 12 and 15 / ctrlB 0).

**Repo claims verified.** `OrbitKey{periapsis, k=1/(1+e) Q48}` with `MEMO_SCALE_BITS=MEMO_SHAPE_BITS=12` (`crates/space/src/orbit.rs`), `PlayerNeighbourhood`'s literal O(N) Cartesian loop behind `trait Encounters` (`crates/universe/src/encounter.rs`), and the encounters crate's float `rmin`-sort. The probe's key faithfully models the shipped memo key.

**Adversarial cases (4):**
1. **Soundness sweep (2M (a,e), e→1 heavy):** the pad covers the true annulus everywhere **except e ≳ 0.9995**, where the shape gap falls below the 2⁻¹² bucket floor and the window covers ~⅓ of the true apoapsis — an unreported boundary the author's scenes (e ≤ 0.9) never approach.
2. **Constructed edge shell at plane-like reach:** full window 4000/4000, noR 286/4000 — the R-widening is load-bearing; also explains why the author's control was silent at R=5×10⁻⁴.
3. **Extreme-e belt (e∈[0.95,0.985]) + precession:** 0 misses — recall extends up to the boundary in (1).
4. **Retrograde same-annulus pair:** chirality-blind window is sound; adoption must window on (p,k) ignoring the Catalogue's chirality bit.

**Novelty:** the memo-key-as-tier unification is absent from HISTORY; it composes with r8 v2, q-candidate-degree, gold 20261006-0737 and H0213's memo-hook note rather than repeating them.

**Grade: silver** — `check.md` written to the run folder (only that file changed). Reproduced exactly with pre-registered, honestly-reported predictions, but the deletion's load-bearing half (the dioph timing tier stacked on the same key cells) is unmeasured, the speed gain is 2.7× not 10×, and the e ≳ 0.9995 pad boundary was missed. The one gold experiment: run `dioph::first_hit` over the window's pairs and measure steady-state work per real encounter against the fine truth (r8 v4's `steady` shape), then wire the key index behind `Encounters` and A/B the plane.
