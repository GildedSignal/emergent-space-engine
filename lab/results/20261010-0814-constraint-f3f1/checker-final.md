Grade: silv**Grade: silver** — written to `lab/results/20261010-0814-constraint-f3f1/check.md` (and `checker-final.md`).

**Reproduction** (clean tree, patch applied by me, then reverted): the digest `6ce636fa…` matched the author's pre-patch run, their post-patch recheck, and my own run — tree identity and bit-neutrality proven in one shot. Gather share 0.66 (author 0.67–0.72), per-readout 11.6 µs cheap / 57.7 µs expensive mode, kick-bench digest and 35 µs median exact, `behave`/`engine-judge` verdicts identical line for line. Predictions were genuinely pre-registered (08:21:39 vs first decomposition run 08:22:05) and the author graded them honestly.

**My attacks** all survived: seed 7 (gather 0.62, bodies 93% of gather), rtf 400 (engine share rises to 0.28 but gather still leads), unpaced (0.61 — not a pacing artifact), members 1000.

**Why silver, not gold:** the headline (gather dominates the frame) is already H0210's recorded limitation and `b-readout-cost` is already queued; the run prices the 4–6× lever without pulling it. The one experiment to gold: implement the readout fix and re-measure on this harness. 

**Catches the checker found:** the dossier's "E1–E8 pass" is contradicted by its own evidence (E6 FAIL UNSUPPORTED); the gate block under-reports a wholesale oracle blow-up (G1–G6, B7, B9, B10 all `worst inf` — which actually strengthens the author's B11 reading); `--members` saturates at 417 bodies so the scale point sits at the CLI's ceiling; the kick-bench command omits `--rtf 100` (33 vs 1158 samples without it).
