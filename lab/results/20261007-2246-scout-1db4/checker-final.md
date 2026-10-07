Working...
Check complete — `check.md` written to the run folder, nothing else touched, scratch (~150 MB) removed.

**Grade: silver.**

**Reproduced exactly:** reran the falsifier on all 12 cases — CSVs byte-identical to the stored `.gz` (deterministic), `analyze.py` table matches every cell (medians, worst, ctrl512, relerr columns, the M1/M6 μ-invariance pair 0.352/0.339 @8 and 0.101/0.101 @16). `predictions.md` predates the sweep (mtimes, no self-calibration); the pre-registered kill criterion fired as claimed.

**My five adversarial cases** (author's binary + bars): the load-bearing belt floor replicates independently — clean a=0.44 gives N=2 on 8/8 seeds (ctrl 2.7e-3), near-3:1 gives 4, e=0.30 stays 2, and moon f=0.15 gives 8 vs 128 at f=0.30, cross-validating r9's 0.17 R_H cliff. Case a=0.90 (ctrl 0.75) proves B2's "far from resonance" label wrong — its void is 4:3-band contamination, which strengthens the refuse rule.

**Why not gold:** the claim's "moons need 16–32" is the rate-bar-only read — under the author's own pre-registered walk bar, moons fail on 7–8/8 seeds at *every* n ≤ 128 (cadence buys the moon regime nothing); three dossier numbers are wrong (n=2 error is 8.6%, not 0.4%; B6 has 2 no-N seeds, not 4–5; B2's geometry label); `analyze.py` scores B5 with the wrong resonant angle; and the plane's actual kick form (orbit-averaged, per law.md) is untested — the author names that experiment themselves. Gold path: same sweep with averaged kicks plus a compiled-frequency resonance-distance criterion; if the 2–4 floor and refuse boundary survive, adopt per-body `step_for` and delete the uniform 128 (ctx.rs:42 confirmed).
