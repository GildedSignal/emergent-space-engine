Working...
Check complete. `lab/results/20261009-1649-dynamics-ec3a/check.md` written; nothing else in the run folder touched.

**Grade: silver** (agrees with the author's self-assessment).

**Reproduction**
- Clean tree (empty patch); my C0 rerun is **bit-identical** to the author's (crossing arrays equal; S 3.299, waste 0.697, f/l/w 0.083/0.562/0.328, burst 1.359). All 8 stored JSONs match the dossier table digit-for-digit. C1's exact zero is structural (kick branch skipped at m'=0), verified in code and output.
- Predictions timing holds: `predictions.md` 17:09:59, decisive outputs 17:14+. P1/P3/P6/P7 held; P2/P4 failed because both stress belts truly sat past the S-type edge — I verified Holman–Wiegert gives a_c ≈ 0.375 (e'=0.15) and ≈ 0.28 (e'=0.3), so the author's diagnosis is physically correct, not post-hoc.

**My adversarial cases**
1. Seed 21: S 2.99, classes unchanged — shape robust on a third seed.
2. dsamp 0.1 (instrument attack): absolute rate ×1.74 exactly as disclosed, S/waste/classification stable — the load-bearing shape survives.
3. H3 freeze audit: "J2 freezes 81% outright" is **overstated** — 100% of those bodies still re-key (e-key, median 0.177/orbit) and carry 53% of H3's crossings; J2 freezes the a-key layer only.
4. Cut sensitivity: the librarian/walker **work** split ranges 0.15–0.61 across reasonable cuts, not the disclosed ~10 pp; at the author's cut librarians carry 0.62 of work.

**Not gold:** it measures a shape (first input for q-cadence and the unmeasured H_live risk; no prior HISTORY entry) but delivers no 10× and deletes no component. The named gold experiment stands: a predictability-tiered cadence policy judged by the plane's cost judge at equal behaviour, plus the corrected just-inside-the-edge control. Novelty clean; goal fit quoted correctly ("No work for no reason, so no ticks").
