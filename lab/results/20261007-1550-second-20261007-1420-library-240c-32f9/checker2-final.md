Working...
Check complete. **Grade: gold** — written to `lab/results/20261007-1550-second-20261007-1420-library-240c-32f9/check2.md`, nothing else in the folder touched (tree clean, temp work removed).

**What I verified (45-min budget, ~35 used):**

1. **Full reproduction from shipped code.** Rebuilt release `xtask` from main and ran the shipped gate: all five anchors match the dossier and the dump's recomputation exactly (planted-bounded 0.353/1.27e-5, compound 0.416/9.80e-7, drift 1.355/2.40e-9, echo 2.31e-15 with 2/16 excluded → platform FAIL, plane inf at 6/14 answered). `b12dump` series regenerate **bit-identical** (14/14 files `cmp`-equal, 49 s); `b12_matrix.py` reruns **byte-identical**; `work/patch.diff` is empty and nothing outside the folder was edited.
2. **Pre-registration honest.** mtimes 15:59:20 (predictions) → 16:01:23 (matrix) → 16:02–16:05 (outputs); P5 held exactly, P1/P2/P4 failed and the dossier reports the failures as the finding.
3. **Attack, all failed to rescue the Allan slope:** instrument controls pass (white −0.507, RW +0.452, ramp +1.000); no θ at any level (law-level contradiction: leak-per-period needs θ<0.230, planted-bounded θ>0.586; per-ship 33/42 leak slopes under bounded max); non-slope statistics (lag-1/64 autocorr, end/start growth, Hurst) all overlap too; sine aliasing erratic across periods, confirming "not a period count". The two outputs whose scripts were **not shipped** (rootcause, lags) I regenerated with an independent implementation within rounding — all five lag-grid gaps negative.
4. **Novelty:** no Allan entry in HISTORY; the proposal is today's 1420 run (this is its queued second author); builds on H0215 and the 6 Oct recurrence-ratio kill without duplicating them. On-goal: `q-b12-design` is queue entry #1, HANDOFF:71.

**Faults recorded (not grade-changing):** the two unshipped scripts and `reproduce.sh`'s overstated "everything below"; the headline's "leak side min +0.037" (true min is compound's −0.188 — gap worse than quoted); the ladder's 224 correlated cases (16 distinct leaks); echo-fails-on-Linux already in the 6 Oct taste log.
