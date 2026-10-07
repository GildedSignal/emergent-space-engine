Working...
Check complete. `check2.md` written; nothing else in the run folder touched (all builds and outputs went to `/tmp`).

**Grade: gold.**

What I did, in brief:

- **Reproduced exactly** (bit-for-bit, modulo wall-clock brackets): `--channels` plain, `--fma` (including the centerpiece flip: step 95P plain PASS −1.26 / fma FAIL +6.40), and `--permute` (null sd 0.93–1.03, p95 ≤ 1.67). All dossier numbers regenerate from the shipped code.
- **Integrity verified**: `restricted.rs` is bit-identical to the ungraded candidate `q-b12-design-9242` (its `checker-final.md` is a 429; no check.md exists — the dossier's claim is true), and `main.rs` differs only by additions — the arrow statistic, gate, sampler and constants are untouched. `predictions.md` predates the plant runs by file time.
- **Adversarial cases of my own**:
  1. **Switch-time sweep** (the one experiment the run left open), plain + fma, {10, 50, 99, 150} P: the bounded step control **FAILS at 10/50/150 P on both paths** (z up to +31.8); only near-half-horizon switches pass. The gray zone is broad and switch-time-driven — 95 P's plain PASS was a knife-edge, so "the only control whose verdict depends on the machine" understates it.
  2. **Permutation null on the fma path** (unreported by the author): sd 1.00–1.06, p95 ≤ 1.84 — honest on both paths.
  3. **Per-ship discriminator**: leak 3e-9 reads +3.00e-9 on 15/15 evidence ships with ties 0; step reads scattered negatives — the zero-cost fix works as claimed.
- **Novelty/goal fit**: HISTORY's B12 entries kill the *old* statistic; the measured null, phase-channel coverage map, anti-persistence control, step gray zone, and the header/code mismatch are new. This is the red-team HANDOFF #2 requires before B12's freeze; it shows a premise of the candidate wrong (bounded ⇒ pass fails for time-localized errors) at near-zero adoption cost — the same shape as the integrator's 6 October gold.

Predictions were honest: P4 held; P1–P3 failed exactly as the pre-registered kill criterion anticipated and are reported as a negative result with a verified diagnosis. Noted in "what the author missed": the P5 "held" counts the plain path only, the quoted per-ship ranges silently span both arithmetic paths, and the mid-run permute-harness edit (harmless, verified) is undisclosed.
