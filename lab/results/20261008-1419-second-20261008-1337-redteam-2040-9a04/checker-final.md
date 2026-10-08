Working...
Check complete. `check.md` written — **Grade: gold** — the only change to the run folder.

**What I verified (45-minute check):**

1. **Reproduction:** all three dossier commands ran bit-for-bit identical in a clean tree (md5-matched to the stored JSONs; `falsifier.py` is byte-identical to the original branch's script and its output matches that branch's record — the original run's number now regenerates). Every headline number (E1–E6c, V1–V4, slope 1.979, C 1.85→1.66, stiffness 1.19×10⁸, 3600/3600, 11/11) extracted from the JSONs matches the dossier.

2. **Predictions:** exact mtimes put `predictions.md` (14:34:38) before both decisive runs; the two disclosed mid-run bug fixes predate any stored output. All twelve predictions held, including the blind ones (E2, the exponent/band, scale-free, E6b's plunge-not-escape, V3/V4).

3. **My attacks (independent truth — analytic V² extrema, spec re-implementation of the predicate, my own integrator):** 8508/8508 agree on a box far wider than the author's; 9/9 near-threshold orbits (3×10⁻⁴ from the critical curve, both sides, falling starts that exercise the barrier) match predicate = truth = integration; the oracle's T_t confirmed to all printed digits by my own peri→peri integration. My first attack draft had two bugs of my own (a dropped term in the radial acceleration, and event logic) — after fixing them, everything the author claimed survived.

4. **Findings recorded for the integrator:** three prose misquotes, none load-bearing — dL_sep/dE ≈ 18 is really **9.06** (confirmed with the run's own `L_sep_of`; the "all measured out" sentence is false for this anchor), L_crit(1.005) = **4.0397** not 4.037, and the p=80 advance is 0.250082 not 0.25013. Two measure-zero degenerates: E=1 exactly (predicate says plunge, truth escape for L>4M — covered by their |1−E| margin, which the rung must carry forward) and L=0 radial (invariants genuinely cannot decide).

The named experiment is done, the record regenerates, the claim holds — gold under the second-author bar.
