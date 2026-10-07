Working...
Check complete. **Grade: gold.**

**What this run did:** it executed the experiment the previous run's checker named as gold-making — the Allan-slope statistic for B12 v2, tested at the gate's real conditions (the 14 judged frozen chaotic ships, N=1601, worst-seed rule) instead of synthetic classes. It killed the candidate: bounded-by-construction errors read leak (+0.586 max) while a real leak reads bounded (+0.037 min), dead band −0.77 with the wrong sign.

**Verification performed:**
- `reproduce.sh` in a clean tree: shipped-gate anchors regenerate **bit-exact** through `b12dump` (the verbatim-subset copies differ from `xtask/src/behave/` only in plumbing — proven functionally identical by exact anchor equality); matrix output line-identical; 71/196 and 98/196 inversion counts recomputed independently.
- Predictions genuinely pre-registered (mtimes 15:59 → 16:01 → outputs); P5 held exactly; P1/P2/P4 failed against the author's own prior position and are reported as the finding.
- Four adversarials of my own, all of which **strengthen** the kill: (1) the open horizon escape closed — at 4× horizon the gap is still −0.19, and 800-period scenes are unfreezable (only 5/16 ships keep a converged reference); (2) formal threshold sweep — no θ exists; (3) four alternative per-series statistics all overlap; (4) the admitted lens gap closed — min-detectable-leak on the real bounded class is ~10⁷× the floor, far worse than reported.

**Notable for the integrator:** B12 v2's statistic must use state recurrence, not any per-series slope — correlation type ≠ memory type on one horizon. Two secondary findings are partly prior knowledge (echo/B12 Linux failure is in the 6 Oct taste log), but the plane's lost-ships failure mode (answered 6/14) is confirmed as a plane-side problem, not a statistic problem.

`check.md` written; nothing else in the run folder changed; my build artifacts removed (folder back to 3.6 MB); no git operations run.
