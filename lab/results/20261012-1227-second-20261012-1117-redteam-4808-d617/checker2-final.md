Working...
Check complete. `check2.md` written to the run folder; nothing else there touched (author files keep their original timestamps; first checker's outputs never read; all scratch work in `/tmp/check2-d617`).

**Grade: gold** — with two named conditions.

**Reproduction** — all four shipped scripts rerun from clean copies; output identical to run.log's final blocks, no number differed (linger took 6.2 min). `patch.diff` empty; timestamps put predictions.md (12:34) before every script (12:38–13:01).

**Independent verification** —
- Third-method Δφ (adaptive quad + `np.roots`): agrees ≤1e−9 rel at 10 cells incl. near-separatrix; margin round-trips exactly 15/15.
- δL² scaling exact (×100.05/decade); N² runaway confirmed by my own 512-walker run (×15.2–15.3 per 4× N, zero re-anchors, offset 3.9e−2 < 7.3e−2 trigger).
- Classifier vindicated by direct geodesic integration: zero band→plunge, plunge 96–98% genuine, the E≥1 mislabel concern empty (≤0.2%).
- Feed geometry robust: retro-tangential band|cap 15.2% vs 14.3% predicted by the r_p<4.15 birth strip; sustained 10-kick passages keep it ≈30%; outside the strip the band starves (0–1.5%).
- Novelty: prior run graded silver in git with this experiment named; law.md:35's re-anchor rule was calibrated only on df81's correlated kicks ("the second never ran") — this chain is that missing measurement, and it shows the trigger watches the wrong quantity.

**Flaws found (none overturns a conclusion):**
1. kickgate's budget-B column overcounts the alternating train ×2.1 (`|rk|.sum()` charges the return-to-anchor kick a full residual). Frozen μ≤0.3 verdicts survive (fail by 1.4–6.5× even halved), but (e=0.5, μ=1.0) flips to borderline PASS — must be simulated, not shortcut, before B-sep freezes as a rung.
2. The dossier's "reproduces the checker's values (…16.5960)" relocates a number: the first checker's refs at (8.05)=16.596 and (8.01)=17.5661 were *not* reproduced (my instrument sides with this run — the prior checker was wrong); the prose should have said so.

Held-out predictions: the operative frozen claims held (budget B fails at μ≤0.3 for all e; band commonly populated on deep windows; P3 with 17–40× margin); the two letter-misses are disclosed in the scorecard. Every process stayed far under 2 GB.
