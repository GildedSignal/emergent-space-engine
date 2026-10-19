Grade: silver

**Abstract.** The claim verifies and extends: representation.md L59's "aggregates are one
sample each" is refuted on the occlusion channel. Regen is byte-identical (13.7 s); every
dossier number matches results.json — 89.1%/99.0% mid-transit error at R_f = 3/10·R_p
(law 1−(R_p/R_f)²), total blink while ≥ 89% of flux is visible, surviving retardation and
k⁴ beaming at β 0.5. Fresh-code arms beyond the sweep: R_f = 30/100 read 0.9989/0.9999
with the >80%-error window pinned at 2.00 R_p; β 0.9 blinks in both orientations
(0.702/0.861); a 10:1 convoy column peaks 0.925 (no disc radius exists for the closed-form
cure there); 25/33 of the impact band fails 5%. Cure: 145 pixel samples → 3.0%. Adoption:
one doc amendment plus the eclipse-parity aggregate rung (bars need the two fixes below).

**Reasons.**

1. **Reproduction.** `occlusion.py` rerun in a clean folder: byte-identical stdout and
   results.json, 13.7 s, < 1 GB. Every table row, the pixel arms (145/0.0304, 1957/0.0046),
   the β arms (0.592/0.535, 0.835/0.815), the controls (N = 1 → 0.000) and the diagnostics
   (err>80% window 2.00 R_p; random-member 0.109/0.305) all match. patch.diff is empty —
   no tree edits to apply.
2. **The letter and the hole.** The quote is verbatim at docs/representation.md L59 and
   L116 (base 52db369). `grep occlusion|eclipse|transit|occult lab/rungs/` → no matches,
   so no rung sees it. The live page's direction 5 names "aggregate emitters (partial
   dimming, not row drops)" unmeasured; HISTORY and the page record 1885 (dispersion
   channel), 22d1 (per-row law), e59e (opacity absent) — the aggregate spatial-extent
   channel is new, and the orthogonality claim is structural: the failure is measured at
   β = 0, exactly where 1885's belt control read zeros. Novel, not a repetition.
3. **Predictions.** predictions.md (01:50) predates occlusion.py (01:56) and the run
   (runner's results 02:05); the frozen kill criterion fired with 12–198× margin on every
   R_f ≥ R_p config. But 4 of 10 pre-registered predictions missed (P2 peak 28.9% vs <5%;
   P5 60.5% vs 30–50%; P6 random-member 0.109 vs 0.891±0.1; P10 grazing 6.7% vs >60%) —
   each honestly disclosed with its mechanism, but the author's quantitative model of the
   artifact was wrong in four places. The rubric's "held-out predictions held" is not met.
4. **Attack (fresh code, seeds 4242/999, no reuse of the author's functions).**
   - Next decades: R_f = 30 and 100·R_p give 0.9989/0.9999 — the closed form holds — and
     the err>80% window is still 2.00/1.99 R_p: the blink window is the sample's own
     eclipse width at every size.
   - β 0.9, both orientations, independently reimplemented retarded-time + segment-vs-disc
     + k⁴: peaks 0.702 (transit, f_true_min 0.575) and 0.861 (sky, 0.783), f₁ reaches 0 in
     both — the blink survives another relativistic decade.
   - New shape: a convoy column (σ_x = 10 R_p, σ_y = 0.3 R_p, impact 0) peaks 0.925 with
     f_true_mid 0.924 and a 2.19% total-blink path — anisotropic fleets blink too, and no
     disc radius exists for the circle–overlap cure at all.
   - Impact band at R_f = 3: 25/33 impacts from 0 to 4·R_p err >5% (0.89 for every
     impact < 1) — three quarters of the transit band, not a central-transit curiosity.
   - Cure floor: h = R_p pays 45 samples at 7.7% peak; the 5% bar needs h = R_p/2 (145
     samples) — the criterion's cap is met exactly, no slack.
   - Criterion flaws, verified independently: "f_true_min ≥ 0.88" cannot survive "judged
     at player β" (exact minima 0.535/0.815 at β 0.5), and the ≤150-sample cap is
     R_f = 3-specific (h = R_p/2 at R_f = 30 pays ≈ 11,700). Both already fixed in the
     page by the first checker; my numbers agree.
5. **Goal fit.** Shows a design premise wrong on a channel the record explicitly named
   unmeasured, prices the cure on the letter's own second clause, and leaves a freeze-ready
   rung arm — principle 28 ("the view is an instrument… an instrument that blinks out whole
   fleets carries no information"), principle 3 (the overlap fraction is derivable), and
   the artifact is the tail, not the average (principle 20). Not a board bottleneck;
   occlusion is unwired today (e59e), so nothing shipped changes and no 10× cost moves —
   the value is deleting the rule before its natural first implementation ships.

**The one experiment that would make it gold.** Freeze the corrected eclipse-parity
aggregate arm (candidate: per-pixel aggregate occlusion; negative: the one-sample rule;
bars as the page's direction 2 now reads them — 5% p99 vs exact Σk⁴ at player β over both
orientations, sample cap as ~(R_f/h)²·π/4) and execute it for a mechanical verdict. That
is the step 13c6 took for r6: the refutation becomes a guard, adoptable in one move.

**What the author missed.**
- The freeze-ready criterion contradicted itself (the 0.88 bar vs the player-β clause) and
  its sample cap was config-specific.
- The closed-form "cheapest cure" is shape-limited, not just density-limited (the first
  checker found ring/arc/β; the convoy column has no radius at all) — per-pixel exact
  predicates are the only shape-general cure priced.
- The blink window is size-invariant (2 R_p at R_f = 30/100) — stronger than claimed, and
  unclaimed; likewise the impact-band breadth (25/33) versus the dossier's
  "impact < R_p" phrasing.
- The safe-domain limb flash is exactly 0.5 at the bisection instant; 0.289 is grid-limited
  (du = 2.25 R_f) — one finer grid near the limb pins it.
- No sub-pixel statement: the artifact needs the transit resolved on screen; the rung's
  domain should say so in one line.
