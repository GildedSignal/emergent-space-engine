Working...
Check complete — `check.md` written, tree restored to pristine, scratch removed.

**Grade: silver.**

What I verified in a clean tree (all reproduced):

- **Bit-identity, attacked and held.** Tuning digest `05cbbb1d…` and held-out digest `c8c103c7…` byte-identical pristine↔patched, matching the dossier exactly. My own 386 adversarial keys (fresh seed, e=0.999999999, 1−2⁻²⁰, e=0, periapsis 2²–2⁵⁰, e≥1 rejections) — also byte-identical. The patch's band predicate mirrors the loop it feeds; measured reserve slack never goes negative (worst −1/−2, so "exact capacity" is literally true).
- **Timing.** Interleaved A/B min-of-3: 16374 patched vs 16775 pristine = −2.4% (author: −1.2%); held-out −0.6% (author −0.6…−1.8%); knots 70.8/key exact; op probes within ~10% under load 1.2; ns linear in knots (6→3.3 µs, 86→59 µs), confirming panel count as the structural driver.
- **Tests.** 40/40 on the patched tree. **Predictions** all three held, with the cost sitting honestly at the edge of the pre-registered band.

Why not gold: the kept patch is 1.2% against the 10× bar, deletes nothing, and the "floor" is a bound from three hypotheses, one of which regressed 11%. The gold experiment is the one the measurement points at: a ~10×-coarser band scheme away from the separatrix that keeps gate behaviour — a law decision, now backed by this ceiling.

The one real defect found: the dossier's redirect ("the shape memo is the right lever") is stale against the board — the 5 Oct correction and commit `dbd4add` show the exact memo hits 0% on distinct kicks and the quantized memo is a law change. The author read the taste log's recompile line but missed its correction. Also noted: reverted rounds R1/R3 left no diffs, so half the loop is unverifiable from the folder.
