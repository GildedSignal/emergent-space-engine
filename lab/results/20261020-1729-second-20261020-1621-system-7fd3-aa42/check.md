Grade: gold

**Abstract.** 7fd3's checker-named experiment flown whole: the 26%-vs-84-87% compile-share
contradiction is dissolved — both numbers reproduce in their own denominator×scene cells
(bench wall 0.367-0.430 regen, fresh seed 0.421; bench from_state stages 0.842-0.866 vs
a765's stored 0.876-0.894; belt wall 0.254-0.266; belt stages 0.438-0.452), digests
bit-identical to a765's independent audit (all three seeds), counters deterministic and
equal to a765's stored calls (1467/1737/1349). The unnamed term is measured: rebind
scaffolding outside `from_state` = 41-57% of the wall on both tested scenes (checker
probes: 35% on a 10⁴ burn belt, 37% at bench rtf 30, 41% at belt 10⁵ — second-largest
term everywhere; compile is the only scene-dependent stage: 7-8/15/53-79 µs/mint
coast/burn/bench). Adoption cost: zero code; every compile-share citation now names
denominator and scene, and the kick's next pricing run aims at the scaffolding.

## Reasons

1. **Reproduction, three ways.** The runner's regen (exit 0) reprints every load-bearing
   ratio inside the disclosed load bands (bench wall 0.428/0.394/0.367/0.430 vs dossier
   0.413/0.387/0.367/0.427; belt wall 0.265/0.254; stages 0.852/0.842/0.851/0.866 and
   0.452/0.438). I applied `work/patch.diff` to the clean tree myself, built, and re-ran:
   counters identical, ratios inside band. Independence, not just repetition: the bench
   `digest`/`replay_digest` are **bit-identical to a765's audit and clean JSONs from 16
   October** (different instrument, different day) for all three seeds, and this run's
   mints equal a765's stored `calls` exactly — the census-plus-stage-timers instrument is
   digest-neutral, and the two source runs' counters cross-match. `work/census.patch` is
   verbatim 7fd3's patch (diffed against its branch); the additions are exactly the two
   `Stage` timers inside `from_state`, the `fit_ms`/`fs_ms` print fields, and the bench's
   census hookup.

2. **The instrument reads both metrics correctly.** `FS_NS` wraps all of `from_state`,
   `FIT_NS` wraps `fit_key`, `compile` wraps `Orbit/Passage::compile`; `REBIND_NS` wraps
   the whole `Work::rebind`. So 7fd3's metric = compile/rebind_ms and a765's =
   compile/(fit+compile+tail), from one binary — verified against the code and both
   source runs' stored numbers. The outside-from_state arithmetic (wall − fs/rebinds) is
   conservative where it can be biased: bench mints exceed rebinds by ~10% (retries or
   setup mints outside any rebind), which can only *understate* the scaffolding.

3. **Predictions.** `predictions.md` (17:33) precedes the dossier (17:39) and the
   regen logs (17:42); the pre-registered fork declared the mixed band (0.35-0.55) as a
   third exit before the runs, and that is what fired — strong evidence of genuine
   pre-registration, since a post-hoc author would have picked a clean branch. The kills
   are reported at their own bands (P1 ≥0.55 and P2 ≤0.35 both died; P5's reads/mint
   35-37 against [0.5, 8] with the mechanism named: the bench's own frame traffic —
   52,217 reads / 600 frames ≈ 87/frame checks out). One generosity: P3's belt stage
   metric read 0.441-0.453 (my regen 0.438-0.452) against the predicted [0.45, 0.75];
   "held, at the edge" is kind to the 0.438-0.441 readings — the numbers are disclosed,
   so this is wording, not concealment.

4. **Adversarial arms (four, three outside every swept axis).** (a) **Bench seed 2026**
   (fresh seed): wall 0.421, stages 0.857, compile 61.3 µs/mint, outside 81.1 µs (50.9%),
   reads/mint 35.1, history 215/215 — the bench cell reproduces on a seed the author
   never ran. (b) **Bench seed 3, rtf 30** (fresh regime): stages 0.881, compile 78.7
   µs/mint, but wall 0.552 — at the P1 fork edge — and outside 37.3%: the mixed band and
   the 41-57% scaffolding band are rtf-100-scoped, not universal. Both source numbers
   were rtf 100/1800, so the adjudication stands; the page now says so. (c) **Belt 10⁵
   coast** (decade up): wall 0.277, stages 0.471, compile 8.3 µs/mint, outside 41.2%,
   history 99.965% — cell holds. (d) **Belt 10⁴ burn** (regime the author named
   unmeasured): wall 0.397, stages 0.613, compile 15.0 µs/mint, outside 35.2% — the
   compile is confirmed as the scene term (burn sits between coast 7-8 and bench 53-79
   exactly as the e-monotone story predicts), and the scaffolding stays the
   second-largest wall term. `fit_key` (4.0-4.7) and the from_state tail (4.9-6.0) are
   flat across all six scenes flown — the "only the compile is scene-dependent" claim
   survives everywhere I probed.

5. **Novelty.** The frame-cost page's open directions (7fd3's merge) held exactly this
   item: "one census run on a765's arm settles it." The run is the designed second-author
   pickup, and it delivers more than the fork asked: the cross-cells (belt-stages
   0.44-0.45, bench-wall 0.37-0.43) and the outside-from_state term are new — no HISTORY
   entry or wiki page names the rebind wall's scaffolding share; a765's audit stopped at
   `from_state`'s edge and 7fd3's "fit 74%" folded 41 points of scaffolding under a
   wrong name. Not a repetition: both standing numbers are *re-scoped*, not re-measured.

6. **Goal fit.** The board's kick row was gated on this adjudication ("gated whether the
   kick's next 10× is the fit or the compile/Carlson replacement"); the answer is
   "neither alone — the scaffolding, then the compile on strong-e scenes," with the
   floor-gap arithmetic corrected in passing (a765's ~10-12×-above-floor used a
   from_state-scoped "rebind"; against the true 146-196 µs wall it is ~25-33×). PRINCIPLES:
   "Measure before claiming" — the contradiction was two true numbers in unlabeled
   denominators; "the right question, then the representation" — "share of *what*, on
   *which population*." Zero adoption cost, print-only (digests prove it).

## The one experiment that would make it more

None for this claim — the adjudication is complete. The next run's first hour is named
by the author: one more timer layer pricing the scaffolding's internals (decode/turn/
residual vs `word_for` retry vs the τ-reads/retirement), on the bench and a burn belt,
where my probes show the band's edges live.

## What the author missed

- The page said "41-57% on every scene"; the burn belt (35.2%) and bench rtf 30 (37.3%)
  sit below it — corrected in place, with the checker arms added to the domain line (and
  the belt wall range fixed to 0.254-0.266; the 3×10⁴ cell's lower readings were
  omitted).
- d4f1's compile/bind 0.85-0.90, cited by 7fd3's checker as agreeing with a765, is
  dropped from the resolved line rather than adjudicated: its "bind" denominator was
  never checked against the two cells (its own seed-2 read 0.57 on 33 kicks; likely
  stage-scoped, unproven).
- The mint-knots page still cites a765's "compile 84-87% of the rebind" without the
  denominator qualifier — out of this run's one-page scope, but the citation rule this
  run establishes ("name denominator and scene") should be propagated there by the next
  run on that topic or the integrator.
- The patch quietly drops `machine_after`/`wall_seconds` from the bench JSON (replaced
  by `census_note`) — harmless (digests and replay digests untouched, and the raw logs
  still carry the census lines), but "print-only" should not delete fields; the stray
  leading space before `pub(super) fn run` is cosmetic.
- P3's "held, at the edge" is generous (see §3).
