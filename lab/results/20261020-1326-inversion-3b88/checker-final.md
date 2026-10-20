Grade: silv**Grade: silver** — written to `lab/results/20261020-1326-inversion-3b88/check.md`, with the author's wiki page corrected in place and the working tree restored.

**What reproduced (bit-for-bit):**
- Items 1–2 came from the runner's own regen.log: gates 8/9/10 = PASS 5.30e-3 / FAIL 63/64 `inf` (`lost=1 kicks=926`) / PASS 3.32e-4; `b13_by_draw` draw 27 verbatim.
- Items 3–4 the delivered regen never reached — I applied `work/fix.diff` and reproduced all of it: the mechanism walk (fault at tick 910984136830, doll 0, `Kick(0) Refused("periapsis")`, period **3.195e19 ticks** > i64::MAX; min-E triple; alive/dead/alive), and the scans **2/229 (step 9), 1/229 (step 8, draw 104, kicks 358), 0/229 (step 10)**.
- Independent physics check: at the fault state E = ½v² − 1/r ≈ −1.5e-13 doll-units ⇒ Kepler T ≈ 3.8e19 ticks — the overflow reading is real, not a print artifact.

**Why the runner's regen exited 1:** `work/patch.diff` carries the same diff **twice**; `git apply` refuses it on a clean tree (`run.log` records the error), so the two diagnostic tests never existed and the script died at the `escape_refusal` grep. `work/fix.diff` is the clean half; the fix session's "exit 0, verified" run only exercised the already-applied tree. That record defect is what caps the grade, per the taste log's own rule ("results that the shipped code cannot regenerate").

**Adversarial (3, one outside the author's range):** step 7 — an octave the author never flew: 0/229 (lottery misses; claim survives, domain now 128–1024); draw 104 walked at step 8: identical mechanism, T = 1.525e20; threshold arithmetic: the wall starts at |E| ≈ **3.9e-13**, not the dossier's 5.7e-13 — page corrected.

**Two corrections on the page:** the threshold constant, and the loss branch — the body ends fault-tagged `Kick(0)` with one refusal/one fault, i.e. at the refused kick's own replan (`step.rs:851-855`), not at a later `Boundary` item (`:845-849`). Mechanism unchanged.

**Novelty holds:** gold 7076 left the `inf` row "unattributed"; HANDOFF's no-tube limit covers plunge/near-radial/γ≳2000 and high-gamma's `Range` wall is the far-hyperbolic fit — a barely-*bound* period overflow is a new, measured class. Gold-making experiment: dedupe the patch for a clean-tree exit 0, and fly the `Ok(None)`/"beyond the horizon" fix class to show the 2/229 ships survive with B13 otherwise unchanged.
