Working...
Check complete. `lab/results/20261006-1738-b-handoff-surface-18d2/check.md` written; tree restored to clean main; nothing else in the run folder touched.

**Grade: lead** — decided on four findings, three of them mine:

**Reproduced bit-for-bit** (the record is largely honest): P5 asserted tests 4000/4000 at 0.01c/0.3c; the moon test (handoffs 0, 52,237 events; 0.9 R_H released at sample 1); the P4 line 2.180/1,044,735 events; B13 identical before/after (my own clean-tree baseline = my patched run = the author's lines); B17-after identical detail line. The β=0.9 reporter actually gives **4000/4000** on the shipped patch — better than the dossier's 3999 (stale number, disclosed as a record defect in the author's favor).

**Finding 1 — the headline P4 failure is a metric artifact.** The probe's "median" is `d[len/2]` on a time-ordered vector. Sorted on the identical trajectory: ratio **0.998**, medians flat at 9.6e−6. The case the author reported as failing passes; their diagnosis ("the walk is in the child-doll clock") and their named next experiment rest on it.

**Finding 2 — the true P4 table fails elsewhere, worse.** Completed the six cases the author couldn't: 0.5-retro **19.97 with 21,403 handoffs** (capture/release twice per moon orbit), 0.9-pro **4,454** (last-decade median 8.5e−3), 0.9-retro **104.5**. The frozen kill criterion ("ratio > 1.3 on any satellite → kill this configuration") fires on three cases with the corrected metric.

**Finding 3 — the single surface is not single near r_c.** A retrograde circular birth at 0.49 R_H (unambiguously Hill-stable, born inside the surface) flaps 210 handoffs in 20 periods; 0.45 R_H stays. The patch's doc claim that both readings agree "to the words' quanta" is falsified.

**Finding 4 — the suite-green claim is false.** `tests/motion.rs`: 8/8 on main, **4/8 red** on the patch (verified by stashing), including the flyby population test with ship 2 at 5.5e−1 map error — "passing ships need no handoff" holds only for fast flybys. The "12 passed, 0 failed" line is the lib alone.

**Salvage recorded for the next run:** the exact extended map (event boost + simultaneity tick shear — P5 exact at all three speeds), the B13 bit-identity method, and my sorted P4 table as the map of what actually fails.
