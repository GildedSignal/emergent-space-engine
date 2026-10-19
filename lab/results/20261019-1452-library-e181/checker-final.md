Working...
Check complete. **Grade: silver** — written to `check.md`, with corrections folded into the author's proposed wiki page in place.

**What I did:**
- **Reproduced** from the clean tree at base `8b51786`: applied `work/patch.diff`, rebuilt, re-flew per `regen.sh` plus four arms of my own. Arm A reproduces exactly (guard frame 17,739 / 29,563 gs, answers latched 2,521, encounters 3,986); arm B flat 613–702 MB to 41,898 gs, identity exact, 8 encounters lost of 3,986 (0.2%); C flat 642 MB. Predictions verified pre-registered by file time (15:03:28 < flights 15:03:58+); P1/P2/P4/P5 held, P3 half-held as reported.
- **Adversarials:** TTL=1 (outside the author's grid) stays flat at 642 MB and loses only 1.1% of encounters vs TTL=8 — the "dead tail" price survives the extreme; TTL=16 on coast is digit-identical to off; TTL=0 ≡ unset; the fence code itself is sound (FIFO-front, saturating tick arithmetic, safe `taken()` default).
- **The blocking defect:** the patch silently deletes the shipped frame-loop `self.prune()` call in **both** arms — so the dossier's "off = shipped bit for bit" and its adoption-cost line are false as shipped. It's outcome-neutral (prune is forget-only) and doesn't confound the ratchet attribution, but adoption would inherit a silent regression. Also: the expired splits (227/263 vs regen's 260/294) are schedule-elastic points, and B's own encounter count varies run-to-run (3,976/3,978) — the law change coupled to schedule.
- **Novelty:** the expiry clause was already the page's named fix (b77d-1fcf/b8e2/acf2); the run's genuine addition is flying it and pricing the add-back (≤ 0.3% vs the 10% bar) — the dossier states this honestly.
- **One step to gold:** restore `prune()`, correct the "off = shipped" line, re-fly A/B once.

Tree left pristine (`git status` clean; the pristine example's Linux link failure on `proc_pid_rusage` is pre-existing — the author's cfg//proc patch is the necessary instrument).
