Grade: gold

**Abstract.** Claim: the W2/W2p onset instrument is fixed in the run's own script and
every corrected number regenerates, certified per row by closed forms. Reproduced:
`regen.sh` exit 0 twice, run-log byte-identical modulo the price line; the six corrected
onsets to their closed forms ≤ 3.6e-12 s; 0 mismatched rows in all 11 arc cells; the
tell (original W2/W2p converging at +125.1344/+125.1206) resolves to distinct
+0.3855/+0.3809 s; the recomputed artifact column equals the original run's published
onsets to 0.0000 s in all 12 cells; PG zero violations. My attacks outside the tested
domain (β 0.99, d 1000R, oblique 20–135°, oblique onsets) all hold to ≤ 1e-13 s. Gain:
22d1's kill of both cheap occlusion wirings stands on exact, freezable bars; adopt at
one quadratic per row per occluder (~68–140 ns/row across machines).

**Reasons.**

1. **Reproduction.** I ran `bash regen.sh` myself (18 s, exit 0) after the runner's
   pass: my output reproduces `run-log.txt` byte-identically except the timing line
   (68 ns/row this pass vs 109 in the log — shared box, order of magnitude only, as
   declared), and the JSON matches the prior regen copy modulo the price arm. The
   `-orig` reference copies are md5-identical to `origin/claude/lab-20261018-0035-redteam-22d1`'s
   files, so the PG comparison is against the true original. Every dossier headline
   regenerates: onsets +0.4729/+0.2862/+0.2423 (β0.5) and +0.6194/+0.4341/+0.3855 (β0.9);
   closed forms W1 = −R/β, W3 = d − R√(1+β²)/β, W2 = √(d²+R²) − R/β, W2p = d − R/β
   (max refined-onset residual 3.6e-12 s); C1 quad-vs-bisection 1.1e-11 s, brackets
   valid; arc per-row mismatches 0/0/0 in all 11 cells; rim +0.4363 → +0.2751 s bounded
   and shrinking; W2p killed under both letter readings (+0.236/+0.238 s constant vs
   +15.05/+125.12 s; arc Jaccard 0.3065 at 10R, 0.0000 at 100R β≥0.5); PG violations [].
   I re-derived all four onset closed forms and both arc predicates independently
   (algebra in my notes; the W3 root formula and the oblique predicate
   d²(sinψ+v_y)² < R²(1+β²+2v·Ê) both check out) — the certificates are real math, not
   fitted to the code.

2. **Predictions and timeline.** `predictions.md` (01:56) precedes the decisive run
   (`run-log.txt` 02:07); the final script edit (02:14) is after the log, but my rerun
   of the final script reproduces the log exactly, so it changed no measured value.
   PA/PD/PE/PF/PG held; PC held (rim bounded, shrinking — P2 correctly re-graded
   held-in-form). PB held on the artifact column and the tell, and was refuted on one
   sub-clause (planet-β invisibility) — honestly reported with numbers I verified in
   the log (+1.1576/+0.3743/+0.6276 s at β 1e-4). That refutation strengthens the
   kill: the original instrument was biased at every β, not only at game velocities.
   Honest misses, disclosed at the top of the Predictions section, do not block gold
   (H0183); concealment would.

3. **Attack, outside the author's domain.** (a) β = 0.99 (author max 0.9): all four
   refined onsets match the closed forms to ≤ 1.4e-14 s, arc mismatches 0,
   Jaccard(W2,W3) = 0.1411 = √(1−β²) exactly. (b) d = 1000R (next decade): onset error
   +0.23657/+0.38424 s, matching the closed form to 0.0e+00 and converging to the
   claimed d→∞ limit (R/β)(√(1+β²)−1). (c) Oblique 20/30/60/135° at β 0.5/0.9 (author:
   one 45° cell, β ≤ 0.5): per-row predicates exact everywhere (0 mismatches);
   Jaccards 0.46–0.99, dipping to the transverse √(1−β²) exactly at 90° — continuous
   geometry. (d) Oblique **onsets**, which no certificate of the author's covered: my
   independently derived closed form t_O = √((d − v_x R/v_y)² + R²) − R/vy matches the
   fixed instrument to ≤ 2.2e-15 s at four geometries including β 0.99 — FIX 1's
   general quadratic is right where the run's own tests never looked. (e) 200 random
   lookback solves (random β ≤ 0.999, directions, positions): defining-equation
   residual 2.3e-13, quad-vs-bisection ≤ 3.4e-9 (bisection-limited). (f) Negative
   control: the recomputed buggy column reproduces the original published onsets to
   0.0000 s in all 12 cells — C4 is the artifact, faithfully.

4. **Novelty.** Not a repetition. The page at base already held 22d1's corrected
   numbers, but as checker-supplied and non-regenerable — the exact record defect that
   held the line at silver. This run adds: regeneration from the run's own script,
   per-row exact certificates (W3 root formula, W2 arc predicate |sin(ψ+asin β)| <
   R/(γd), oblique predicate anchored at frame-time distance), the oblique sprite
   identity (distance = light time), the artifact column with the tell's resolution,
   the W2p dual-reading kill, and the planet-β visibility of the bug. docs/HISTORY.md
   has no eclipse-parity entry (H0013/H0014 are the relay's family occlusion, other
   work); e59e measured static opacity only.

5. **The page.** The fold-in is faithful: every new line traces to regenerated
   evidence, the frozen form's bars are the closed forms, the Runs line is
   append-only. One overstatement corrected in place: the oblique qualifier's range
   "0.53–0.99 at 20–135°" — my sweep gives 0.46–0.99, meeting the transverse √(1−β²)
   at 90°; the page now says that. Not three gold runs agreeing on this topic's
   current best: the page stays open.

6. **Goal fit.** Deletes both cheap occlusion wirings from the design and freezes the
   rung bars exactly, before the lensing memo lands — the view's correctness half.
   Principle 19 ("a fix signals the wrong representation"): the corrected story is
   stronger — every cheap wiring breaks parity by geometry, which no cadence or budget
   fixes, and the exact test is the same quadratic the contact resolver already is.
   Principle 26 applied to the tell ("agreement is not independence when the harness
   is shared"): the run's answer is three independent methods agreeing. Cost: none
   beyond 22d1's.

**What the author missed.**
- The oblique regime it flagged as "worth one dedicated cell" is measurably closed by
  this check (predicates exact at 20–135°, β ≤ 0.9; the Jaccard minimum sits at the
  transverse angle, not below it) — the rung's oblique qualifier is now grounded.
- PD's parenthetical "≈ −22° at 2R" is the sin-space centre (−β(1−R²/d²)); the
  ψ-space centre the script measures is −25.67°. A convention slip inside a held
  prediction, unflagged; the dossier's reported number is the measured one.
- Arm B's diff_limb is independent of the r_E, r_O choice (they cancel in the
  difference) — still not stated; one line would harden the 0.782 s bar.
- Timeline nit: the script's mtime postdates run-log.txt; proven harmless here (my
  rerun is byte-identical), but the final edit should have been followed by the
  saved log.
