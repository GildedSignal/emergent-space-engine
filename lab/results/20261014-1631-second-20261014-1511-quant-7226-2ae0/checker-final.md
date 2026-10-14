Working...
Check complete. **Grade: silver** — written to `check.md`, with three corrections applied to the author's proposed `wiki/frame-cost.md`.

**What I did:**

1. **Reproduced from my own build**: applied `work/patch.diff` to a clean tree, rebuilt — every count and digest in the dossier matches (s3 fly 23,552→8,589 probes, worst 32→14, digest `36637e67`; secant kill row 35,621/57 exact; suite 11/11). Counts are deterministic; wall columns within stated wobble.

2. **Verified OFF = shipped against a pristine build myself** — the patch carries one unconditional edit (0b85's Crash-retain removal) and the m4000 battle scene is only reachable through the patch's bench unlock (shipped clamps members to 400). Pristine digests identical at flying s3/7/11/42 and battle m400; the m4000 OFF reference is patch-internal, which the dossier could have said.

3. **Seven adversarial cases outside the author's domain, all held**: new seeds 42/99 at both paces (−62…−64 % probes, worst ≤ 15, digests identical), a 16 s horizon (tail does not grow), the untested rtf 10 pace, composition at new seeds (warm+P3 < warm < P3 < shipped), and `ES_FP` edge values (found a new footgun: unparseable values silently mean secant, the killed row — harmless to correctness).

4. **Why silver, not gold**: the pre-registered P2 battle-median cut (≥ 15 %) measured ~0 % — a miss by the author's own counting rule, honestly reported with a credible but untraced mechanism — and the end-to-end gain is ~1.9× on the flying kick (199→105 µs), under the 10× bar. Named gold experiment: per-kick probe attribution at battle pace, turning the criterion-artifact reading into a measurement. Everything else — tail rule, identity, kill-table regeneration, composition — held at every arm, including all of mine.
