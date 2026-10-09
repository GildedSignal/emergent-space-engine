Working...
Check complete. `check2.md` written; tree restored to pristine (only untracked `lab/results/` remains).

**Grade: gold.**

Reproduction in a clean tree from `work/patch.diff` — every claim leg regenerated bit-exactly:
- Control digest `21c73edc…` (P6); B13 split = shipped (60/64, identical text, PLANE_TRACE byte-identical to the author's trace); B17 PASS with the dossier's exact numbers (34.7 s); B12 text-identical (median ∞ → 0.608, same 44 replaced draws).
- Belts: 78385→16732 (4.68×) and 78094→10032 (7.79×), all four digests matching, split deterministic on rerun; naive uniform-4 reproduces its 3/64 B13 collapse.

Adversarial cases (mine): fresh seed 3 holds (4.59×); planet-crossing belt (e ≤ 0.9) collapses to 1.61× with zero losses — the bound honestly keeps full resolution where encounters are possible; trace identity; uniform-4 control.

Predictions discipline verified by file times (predictions 10 min before first data file); the pre-registered "stop and re-derive" was executed on P2's two falsifications, and the ratchet they forced is the substantive finding: a cadence that modulates with the orbit is a different, worse law — the constraint the queued q-cadence build must carry.

Two record defects found and named (neither touches a claim leg): the split-on bench digest `bb81ae6e…` is stale v2-era — the shipped v3 patch regenerates `fea07ab3…` — and the kick-bench absolute counts (630/611) have no regenerable invocation (identity and the invariant 45 shapes reproduce exactly).

One disclosure, also in check2.md: a repo-wide grep inadvertently surfaced three fragment lines of check.md before I began; every number I cite I measured myself, and the grade rests on that.
