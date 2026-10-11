Working...
Check complete. `check.md` written to the run folder — the only file I added; all author files untouched.

**Grade: gold.**

**What I verified:**

1. **Reproduction** (clean tree, `/tmp/check-b04d`): lib is a verbatim crate copy (`diff -r` empty); `battle` regenerated 8/8 scenes with 0 mismatches ex timing (38.6 s); `run-fix.sh` regenerated 24/24 records with 0 mismatches (109 s, every stage < 60 s); `analyze.py` output byte-identical to the stored `analysis.txt`.

2. **Controls**: the 1e-4-H20 scene matches the parent's b1-cross-150 on every shared scalar (kmax 14, kmed 2, all counts); part B's k0 reproduces the parent's 67/100, 166/217, 284/423; seeds and builders are the parent's verbatim; `outside_cone` = 0 in all 21 scenes.

3. **Predictions**: frozen before the fix runs; 9/11 held by the letter; the failed #8 is genuinely pre-registered (wrong by 2–3× on constants) and its corrected model (k ≈ 0.32·n_B) is confirmed by my own 1200-body run (kmax 175 ≈ 0.29·n_B).

4. **Adversarial cases** (mine, fresh seeds): q eternal on two fresh seeds (kmax 4/5 flat to H=320); q at 600 bodies — zero-miss k doubles 8→16 and the eternal 19.0× at zero miss holds; b2 at a 4th size — merge-join 849→175, zero-miss k = 256, ratio 4.06× (the "k ∝ n, constant factor, not O(participants)" claim); a=1.25 fast crossing — mechanism survives (221→57, 3.81×) but the author's "fast crossings shrink k" direction guess is wrong at equal size (57 vs 44).

5. **Adoption target confirmed**: the parent's note in the unmerged `b-coorbital-cert` build contains both wrong claims verbatim ("O(participants), not O(n_A·n_B)"; the 19× headline); this run's replacement sentence is fully measured, one spec edit, no engine changes.

Misses I logged for the integrator: the part-B ratio denominator is cone pairs rather than window sections (honest gain ~5.3×, the 3.9× is conservative); the fast-crossing direction sentence should not survive into the spec; the kicked-fleet cadence question (the likely runtime path) remains unmeasured.
