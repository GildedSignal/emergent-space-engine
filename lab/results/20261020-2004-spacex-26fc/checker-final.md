Working...
Check complete. **Grade: gold** — written to `lab/results/20261020-2004-spacex-26fc/check.md`, page corrected in place, tree restored (patch reverted, no stray files).

**What held under reproduction:**
- `regen.sh` in a clean tree + patch: every certificate line exact — `alive-missing 0` in all five arms, `drop none` = 0 in every gather, identical missing-id sets (fleet 25/47 bench; 13/25/27/47 deep), identical death times, 30 dead members at depth, 0 belt-ship deaths. Digest/game-s drift is the known wall coupling, flagged.
- Predictions preceded all decisive arms (file times 20:14:22 vs 20:15–20:20). P1–P3 held; P4/P5 failed and were reported as failures — P4's failure *is* the cadence-bound finding.

**My three adversarial arms (all outside the author's flown domain):**
1. **Burn at depth** (221k gs — the dossier's own domain sentence names burn but never flew it): alive-missing 0, drop-none 0, same 4 dead ids; one-leg re-measures the halving (24.48 → 10.28 segs/body, −58%), confirming the coast's 2.5% is cadence, not noise. 34.502 eval-Nones → 0 drops: a None probe is not a dropped emitter.
2. **N=10⁵** (next decade): alive-missing 0, drop-none 0, 7 missing ids.
3. **rtf 6×10⁴** (deepest probe stress): alive-missing 0, drop-none 0, 11 missing ids.

**Found and closed an instrument hole:** `keep_probe2` never alive-checks fleet ids (≥ n_bodies), so "dead" for them was unverified — I cross-checked every missing member against the engine's own drop-dead census; all confirmed dead. Caveat added to the page's od 5.

**Also closed the author's open item:** view/memo tests pass with the patch (5+1); their run failed only because plain `cargo test` links the macOS-only `nladder` example on Linux — pre-existing, not the patch.

**Page corrections:** 264 → 384 gathers (clamp arm excluded), the retained-depth p50 "keep-independent" clause annotated as run-coupled (sign flips in regen; segs/body is the certificate), od-5 instrument caveat, plus my adversarial extensions. Topic stays open — one gold, not three.
