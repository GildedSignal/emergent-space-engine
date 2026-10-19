Working...
Check complete. `check.md` written: **Grade: gold**.

**Reproduction (independent, clean tree at base 9b0fdb9b + patch.diff, fresh build):**
- Belt digests bit-for-bit: C0 `e8a69ff7…`, A1 Pass `b73b06dc…` (contacts 3 072 187), A2 `db751898…`, A4 cadence `e98306bb…` with onset 12236 — the recovered variant (MU pre-scaled ×4 before rounding, cap ×4, t%4==0) is real.
- Ladder arms integer-identical: e=0.97 (rmax 138q, maxk 526 815, clamps 0) and e=0.975 (ejected t=7045, 3 clamps, maxk 577 391).
- Frozen-since, season ratios, grinder bracket (686 460–739 345) all verified from TSVs.

**Adversarial (two outside the author's range, both confirm):**
1. a=36q, e>0.5 (admittedly unflown): e=0.94 (r_p=2.16q) bounded 42 orbits at 0.02% drift; e=0.95 (r_p=1.8q) ejected t=9458 — the boundary is a pericenter law at a second semi-major axis, and the gate constant e<1−2q/a (0.9444 there) lands between the arms.
2. e=0.97 at 2× horizon (196 608): bit-stable, rmax 138.0q every orbit.
3. Between the author's arms, e=0.972 (r_p=1.96q): one-time pump (e→0.982, rmax 138→224q, 7 clamps) then **bounded ≥ 28 orbits** — "ejects any orbit whose pericenter enters the zone" is false in the marginal band; the gate is unaffected (that arm violates it and is damaged).

**Page corrections (in place):** "Keplerian maxk to 0.1%" → ≤ 1%; clamp zone "1.5–2.1q" → 1.76q diagonal – 2.09q aligned (geometry + observed clamp radii); marginal-band caveat and my probe results added as a checker block; unflown list updated.

**Honesty notes in check.md:** P3's <2% maxk-drift bound failed (+9.3%) though disclosed with a verified frozen tail; predictions.md predates all decisive flights; boundary arms post-hoc but disclosed. Gold: the prior silver's named experiment folded in as a regenerating record, plus the ladder that locates the pump — adoptable in one step, no crate change. Worktree cleaned; nothing else touched; no git operations run.
