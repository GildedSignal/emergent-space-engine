Check compl**Grade: gold** — `check2.md` written, page corrected in place, tree restored clean.

**What I did (independent, clean tree at b86c418c, both patches applied by hand in order):**

- **Reproduction, bit-for-bit:** baseline gate 9 FAIL 63/64 `inf` + lost trace; walk fault `Refused("periapsis")` at tick 910984136830 (period 3.195e19 ticks); scan 2/229 (draws 27, 104). Fixed: gates 8/9/10 PASS 5.30e-3 / 1.33e-3 / 3.32e-4 (8 and 10 identical to 3b88's baseline prints on its branch), walk alive with a clean 601/1202/2405 kick ladder, scans 0/229 at 7–10. `tests.diff` verified byte-identical to 3b88's `fix.diff`; 3b88's `patch.diff` double-diff defect confirmed.
- **Adversarial (two outside the flown range):** scans at steps 6 and 11 → 0/229 both; draw 104 completes (faults 0, dE 1.65e-3/3.98e-4/1.02e-4); B13 step 11 → PASS 8.41e-5, ladder continues ~4×/octave; code reading confirms `Ok(None)` → `MAX_STEP` saturation, no panic path.
- **Two defects found and named:** (1) `regen.sh` never reverts patches, so the publish runner's rerun on the dirty tree wrote fixed numbers under the `baseline` header — `base-gate-9.txt` on disk contradicts the dossier; `regen-verify.log` is authoritative and my clean-tree rerun confirms every number. (2) Dossier item 5: the plain `cargo test -p emergent-universe` fails on Linux at the pre-existing `nladder` link; the reproducible form is 77 passed / 0 failed — the author's "46" is a partial sum (Runs line corrected).
- **Predictions:** all four held; kill criterion untriggered; the fix patch predates the predictions, which predate the clean-tree flight record.

Gold because the named gold experiment (3b88's checker pre-registered it) is flown and reproduced exactly, the held-out predictions held, and it deletes a component — a whole `lost`-ship class — adoptable in one branch.
