Grade: gold

**Abstract.** Claim: 22d1's named gold experiment is done — the W2/W2p onset
instrument is fixed inside the run's own script, every checker-corrected number
regenerates, and every wiring is now certified per row by exact closed forms.
Reproduced byte-identical across three executions (author, runner, this check);
the comparison baselines byte-match the published 22d1 commit; PG unchanged-parts
check: zero violations. My from-scratch solver re-derives all four onset closed
forms and both arc predicates, and finds **0 mismatched rows in 11 cells outside
the author's domain** (β 0.99/0.999 transverse; oblique 20°/70°/135° incl.
approaching vₓ<0 at β 0.9; sign-flipped v). Gain: the kill of every cheap
occlusion wiring is regenerable and exact, and the rung bars are freezable
(Jaccard→√(1−β²), onset error exact, bounded ≤ 0.65R as β→1). Cost to adopt: one
exact quadratic per row per occluder (68–138 ns/row across machines).

**Reasons.**

1. **Reproduction.** `bash regen.sh` exit 0, 30 s; every deterministic line
   byte-identical between the author's `run-log.txt`, the runner's `regen.log`
   and my own execution (only the price arm varies: 6.8–10.9 ms/10⁵ rows on this
   shared box — order of magnitude, as claimed). The `.py`'s mtime sits after
   the dossier's, but output identity across three executions proves no material
   post-run edit. `eclipse_parity_orig.py` and `eclipse_parity-out-orig.json`
   byte-match the published 22d1 commit (71c004d5), so the PG "unchanged"
   comparison and the artifact column are measured against genuine baselines.
   `work/patch.diff` is empty — nothing outside the run folder was touched.

2. **Independent physics verification (my main check).** I re-derived, from
   scratch, all four onset closed forms (W1 = −R/β; W3 = d − R√(1+β²)/β via
   minimizing |(u−d)² + (β(t_O−u))²|; W2 = √(d²+R²) − R/β via the sprite's
   y-offset βτ = ±R at τ = −R/β; W2p = d − R/β), the W3 arc root-interval
   (d²s² + 2β(d²−R²)s + β²d² − R²(1+β²) < 0 — identical to the dossier's roots),
   the general oblique W3 predicate (|occ0×(Ê+v)|² < R²|Ê+v|², one-sided
   occ0·(Ê+v) ≥ 0 — confirming the run's "anchors at the frame-time distance"),
   and the 1/γ arc mechanism (sprite at distance γd exactly → half-angle R/(γd)
   vs the law's R/d). My own grid+bisection onset solver reproduces the closed
   forms to my grid floor (≤ 5e-4 s) in all nine cells I ran, and the author's
   refined onsets sit ≤ 1e-4 s from mine. C1/C2/C3 all check out independently.

3. **Attack, outside the tested domain.** Eleven new cells through the author's
   own imported code: transverse β 0.99/0.999 at 2R/10R (the game's r6 scenes
   carry β to 0.9999; the run stopped at 0.9), oblique 20°/70°/135° at β
   0.5/0.9 (the run had 45° at β ≤ 0.5 only; 135° is approaching, vₓ < 0), and
   a sign-flipped transverse v. Result: **0/0/0 predicate mismatches in every
   cell**; sprite distance = γd exact at every β; Jaccard(W2,W3) = 0.1411 at
   10R β0.99 — √(1−β²) to four digits (grid-limited at β0.999, arc ≈ 7 rows);
   W2p arc-dead at oblique β0.9 (0.0000). The mechanism extends; nothing broke.
   Domain facts for the rung: (i) at β→1 the W2 onset error sups at
   (√(d²+R²)−d) + (√2−1)R ≈ **0.650 s at d=2R** — above the 0.62 s bar, which
   is correctly scoped to β ≤ 0.9 and should stay so scoped; (ii) the egress
   error is the mirrored form (√(d²+R²)−d) − (R/β)(√(1+β²)−1) (−0.334 s at
   10R β0.9, verified numerically) — bounded, but the run certified onsets
   only; (iii) √(1−β²) is the *transverse* bar; oblique Jaccards run higher
   (0.53–0.99 in my cells) and the oblique certificate is the per-row
   predicate — I added the transverse qualifier to the proposed page.

4. **Predictions.** `predictions.md` (mtime 19 min before the decisive run's
   log) pre-registered closed forms derived off the code path. PA/PC/PD/PE/PF/
   PG held; PB held on the artifact column and the tell while one sub-clause
   (planet-β invisibility of the bug) was honestly refuted — and the refutation
   strengthens the record (the bug shifts onsets +0.37…+1.16 s even at
   β = 10⁻⁴). PD's two disclosed certificate defects (one-sided segment test,
   wrap-unsafe arc extraction) are physics, not tuning: I confirmed the
   one-sided terms cosψ ≥ 0 / cosψ+vₓ ≥ 0 are the grazing-point-on-segment
   conditions. The tell (originally-convergent wirings now +0.3855/+0.3809)
   resolves exactly as the 5 October lesson demands.

5. **Novelty.** Not a repetition: 22d1's corrected numbers were checker-supplied
   and unregenerable — the record defect that held it at silver; this run is
   that check's named one-experiment path to gold, executed in the run's own
   script, plus results 22d1 lacked (per-row exact certificates, W2p killed
   under either letter reading, the oblique W2 measurement and W3 predicate,
   P2 re-graded held-in-form). No prior occlusion-wiring result exists in
   HISTORY.md or the wiki outside the e59e→22d1 lineage. Not three golds on
   this topic; the page stays open.

6. **The page.** The proposed `wiki/representation-premises.md` diff is
   surgical and every new line matches evidence I verified independently
   (onsets, roots, 1/γ, the tell, W2p, oblique). One correction made in place:
   the frozen rung bar "arc Jaccard √(1−β²) at d ≥ 10R" now says transverse
   cells, with oblique judged by the per-row predicate (oblique Jaccards run
   higher — 0.53–0.99 measured here).

7. **Goal fit.** The view's correctness half, on the board's focus list; it
   freezes the occluder-test wiring decision before the lensing memo lands.
   PRINCIPLES 19 ("a fix signals the wrong representation… bandaids accumulate"
   — every cheap wiring breaks by geometry, no cadence fixes it) and 2 ("error
   type over error size" — the sprite's error type is a 1/γ-narrowed blackout,
   stars that should be hidden stay visible along a thinned arc). The
   negative-control bars are exact and machine-checkable: adoptable within one
   step, at one quadratic per row per occluder.

**What the author missed.**
- The β→1 domain: the bars are scoped β ≤ 0.9 but the game flies to 0.9999;
  the mechanism survives (my 0.99/0.999 cells), with the 0.65R sup and
  7-row arcs at 0.999 as the numbers the rung will meet.
- Egress uncertified (mirrored form, bounded — verified here).
- The √(1−β²) bar needed its transverse qualifier (now added).
- Minor precision: the C4 artifact column replicates the original buggy wiring
  to within one 5 ms grid step (125.1389 vs the stored 125.1344); the dossier
  presents C4's digits as "the original instrument reads" — accurate to the
  rounding shown, and `analyze.py` quotes the stored values separately, but the
  distinction (replication vs stored column) is worth a word.
- The 3-D sky and extended/aggregate occluders remain unmeasured (the lens
  itself flags this honestly).
