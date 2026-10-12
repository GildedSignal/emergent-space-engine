Grade: gold**Grade: gold** — written to `check2.md` and `checker2-final.md`.

**Reproduction** (my own run, clean tree): `regen.sh` exit 0 in 178 s. Every anchored row is byte-identical to the author's captured log (slab +22.667/+50.969, hump +8.634…+8.762, creep 0.000×4→+39.084→+55.492, quad +9.579/+9.598/+9.665, echo 0.000/inj +55.491, planted-bounded +0.812, planted-compound +20.560, all four official gate lines). Blip rows differ exactly as `fix-note.md` discloses (patch lost, sin² window inferred) — but every verdict is identical, and the break law passes the **official** gate in both shapes (+3.127 rebuilt, −18.796 author's). The gate's own dt-coefficient fit reads −2.00e-10/horizon on all five leaking ships and is discarded by the verdict. sha256s match the receipt; the receipt's planted-bounded −2.806 grounds the platform-noise claim.

**My adversarial cases** (independent code, official `b12()` path):
- λ = 1e-5/horizon on the 5-ship split (50,000× the declared rate) → official **PASS** +3.152 — the pool is rate-blind.
- 3 leakers of 16 → PASS +4.365; 4 → +2.999 — the window extends below the author's 5/11.
- Fleet-wide 1e-10 blip, no leak → official PASS at −13.570 with sensitivity "RESOLVED" (+43.168); same shape at 1e-6 fails only via masked injection (same arrow) — `arrow <= 5` has no lower bound.
- Controls: 1-/2-ship leaks with below-floor majority FAIL (+17.741/+22.131) — the page states this correctly.
- Same-process rerun bit-stable (+0.812 twice) — the ±3.6 receipt swing is platform, not nondeterminism.

**Novelty**: only B12 run in `lab/results/`; the v2 candidate's own doc demands this red-team before freeze; its shipped controls don't cover a minority leak with a shaped above-floor majority.

**Page**: every number verified; added one second-checker line (window + rate-blindness + determinism). Not closed — one run, not three golds.

Worktrees removed; only `check2.md`, `checker2-final.md`, the page line, and `work/rt-all.log` (regen.sh's own tee, identical content) changed in the run folder.
