Working...
Check complete. Summary of what I did and found:

**Reproduction** — applied `work/patch.diff` to a clean tree, ran all three dossier commands: every count reproduces **bit-for-bit** (engine T=1, F=470/4,209, misses=0; offline belt/cold/crosser T, F, e-graded, index reads all identical). Timings jitter with load (walk 57–103 ns/body vs the dossier's 64/105 — same order). I verified the probe's semantics against shipped code: the truth window is radial.rs's own certificate law and a sound superset of the exact `hit` (encounter.rs:130–155), and the phase cut is phase.rs's own bound (ω = 2·asin(ρ/2·r_min), equation-of-centre, phase.rs:39–49) — so F ⊇ T is forced by triangle inequality and held empirically everywhere.

**Predictions** — existed before the run; P1/P2/P4/P5/P6 held, P3's ratio missed by ~3 orders, honestly reported, and the miss *is* the finding (T = O(1); the dilution is the e-bulk). The kill criterion (a soundness miss) never fired.

**Adversarial (10 arms beyond the author's 5, scratch example removed after):** formation crowd of 10⁴ **kept whole, 0 misses** (taleb-09b5's invariant holds — the unflown arm now has a number); hot belt (e≈0.3) floods F to 49% — the 21–24× is the cold e-bulk's property (domain boundary, now on the page); e-caps 0.7/0.9 immaterial; radial spread immaterial; crosser sweep continuous; index 0.29 µs at 10⁷. Zero misses in all.

**Novelty** — b083/5f36 measured the phase axis on concentrated rings/keys fleets; 4f59 prices it on the diffuse shipped belt at the band, the regime 396d named "(b)". Not a repetition; composes with the prior work.

**Corrections made:** the page's "class caps read 2–20× more" was wrong — the e-graded column reads 2.0× (belt), 1.3× (crosser), **178×** (cold, destroying the 100× collapse); fixed in place (it strengthens the author's per-body-cap constraint), plus a checker bracket with my arms. Also recorded: the engine arm's e readout is e/(1−e) (conservative, percentiles mildly inflated), and the offline table mixes the two invocations' numbers undisclosed.

**Grade: gold** — reproduced, sound, 21–24× on live-question-1's seam read (100× cold), deletes fix (a), premise-corrected on the crosser, adoptable in one step. `check.md` written; tree restored; nothing else in the run folder touched.
