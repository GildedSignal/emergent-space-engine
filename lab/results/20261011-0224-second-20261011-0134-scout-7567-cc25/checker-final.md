Working...
Check complete. `check.md` written to the run folder; nothing else touched (all reproduction ran in `/tmp/b12check`; both author records verified untouched by mtime and md5).

## Verdict: **silver**

**The claim is real and reproduced bit-identically.** Harness copies are byte-identical to `xtask/src/behave`; all three dossier commands regenerate exactly (10× md5 `d6989c9e…`, 40× md5 `63b7bd0a…`). The composite as the scout specified it is refuted on the real harness: echo false-fails at sub-floor error (2.23 at 1.4e-14), bounded false-fails (5.15, a-diffusion saturates only at the law's clip ~10× the gate's horizon), and the derived cap degenerates to the AXIS_CLIP for all 16 ships — every level set opens the planet's unbound channel, confirmed by exact scan, 4000-state brute force, and the selection rule itself (kept ships cross R_SOI by construction ⇒ no closed C_J band can exist). The shipped `b12` gate independently confirms the exponent numbers (0.353/0.416, 14/14 judged).

**Why not gold — the record, not the physics:**
1. The dossier's 40× medians (echo 11.4 / bounded 6.9 / compound 3.45) contradict the run's **own stored record** (10.44 / 6.66 / 3.04); the quoted max-errs on the same line match, so only the medians are unregenerable. I tested and rejected the 16-ship-median explanation.
2. Selective predictions ledger: compound's predicted interval [2.5, 4.5] missed low (2.024) yet is reported as "≈ √10"; the 1e-8-leak PASS prediction actually FAILs — both unacknowledged (the echo miss, to the author's credit, is).

**My attacks strengthened the kill:** a 2×/5×/20× horizon sweep shows the composite fails at *every* horizon — below 5× it catches nothing but kick, and at 5× it misses compound outright (ratio 1.41 → PASS). The one step to gold: correct the 40× numbers from the record, complete the ledger, add the sweep.
