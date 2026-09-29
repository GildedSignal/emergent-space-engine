Working...
Check complete. Deliverables written: `metrics-check.json` and `check.md`; nothing else in the author's folder touched; no git operations.

**State found:** the author's 60-minute phase expired mid-run — no `metrics.json`, `dossier.md`, or picture; 4 of 192 flybys done (the 5th was killed buffered); `run.log` empty.

**Reproduction (nothing differed where the author had numbers):**
- Seeds/flybys regenerate byte-identically; the 1024-seed binary sweep is **bit-identical** to my rerun (all 17 columns); flyby law-0 row 1 matches to ~1e-6.
- Oracle port verified line-by-line against `gr_oracle_extended.rs`, plus two independent integrations of my own (1PN harmonic ODE → DD's expected O(1/p) gap; u-space quadrature vs Darwin-χ `refine` agreeing to 3e-8). `doll_eob` implements the rung's EOB map exactly.

**Criterion outcomes (mine):**
- `judged` = **0**: the v2 truncation exclusion leaves zero judged precession seeds at p ≤ 1000 M (min estimate 0.0079 > 0.005) — a rung-design defect failing all configs identically, exactly as the author predicted.
- eob-doll: period 652/652 = 1.0 pass; ν **690/697 = 0.98996** — a real 7-seed miss of the 0.99 bar; assists fail by 21.9%–105× on the frozen sequence's first seeds (criterion needs 64/64, so already determined FAIL).
- Transfer: law-0 reference unconverged (half-step **10.9** vs the frozen 1e-9 bar, 3×10⁷-step cap); laws 1/2 collapse to 1 handoff each via chaos — exponent 0.0 there is vacuous.
- Found and reported: a law-permutation bug in `metrics.py` (would have attributed newton's transfer/flyby results to eob-doll), NOAIM-vs-bisection and geometry deviations from the frozen spec, and predictions.md finalized 4 min after `bin.csv` existed.

**Mechanical verdict (dry-run of `verdict.py`): DISPUTED — author missing on all 21 outcomes**; eob-doll fails judged/prec/nu/assist, negatives fail as designed (not stuck). `check.md` details what would make the rung decidable: widen the p-window or drop prec, a non-chaotic transfer geometry, and a stitched pre-SOI patch (or an admission) for R⊕-scale assists.
