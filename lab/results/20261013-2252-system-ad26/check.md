Grade: silver

**Abstract.** One-scene, one-clock census on shipped code (probe patch only: prof counters
printed, `--members` clamp env-gated): the tube rebind is 39–68% of all event-carrying item
work D (80% of a hand-out, ≈45% of a kick, retry 12–39% of the bind, fixed tier 21% of D at
4k), and the record's four unmerged levers compose arithmetically to 21–22% of today's
resolved-battle cost — ceiling ≈9.5×10⁴ members, quiet 10⁹ belt 1.08 cores at Carlson-priced
30 µs/event. Reproduced: m4,000 bit-stable (digest `5c8fe1a8e439221d`, 2,163/1,058 counts),
shares ±3 points, endgame recomputed from fresh numbers gives 21%. Adversarial seed-7-at-4k
reproduces (67.9%). Adoption cost: stack four already-verified patches, run behave + this
census — the integrator's step, not a lab result. Not gold: the composite is arithmetic, not
a build, and the head prediction (≥60% everywhere) failed as stated.

**Reasons.**

1. **Reproduction.** regen.sh exit 0; the runner's fresh census and my own rebuild of the
   author's original m4,000 JSON (inside `work/patch.diff`) agree with the dossier within
   noise (D 1,548.6 author / 1,570.6 fresh vs 1,536.3 quoted; bind/D 66.2% both vs 65.2%
   quoted). The cross-run anchor is bit-stable across three independent runs: digest
   `5c8fe1a8e439221d`, 2,163 hand-outs, 1,058 kicks. The partition D is clean: `process`
   nests the kick/boundary/crash items (verified: 771.40+73.77+1.06 = 846.2 vs process
   845.96 at m400/rtf100), so nothing is double-counted. The patch touches no engine code —
   measurement plumbing and a clamp lift only.
2. **Predictions.** `predictions.md` (22:55) predates the decisive run (author's m4,000
   finished 23:04, per the JSON's own uptime field inside the patch). Prediction 1 failed as
   stated (49–51% at 1,500 members, not ≥60%) and the dossier reports the failure
   prominently and re-derives the claim range; the kill criterion (<40% at 2+ member counts)
   was not triggered — my fresh flying arm measured 39.0%, so that regime genuinely
   straddles the line (I corrected the page's floor from 41% to 39%). Prediction 4 failed
   (0.179 vs 0.03–0.15) and is explained (strict kicks+leavers = 0.101, verified from the
   JSON: (1058+2163)/4000/8). Prediction 2's "rising with members" failed (39%→32%; my
   20,000 rung: 11.6%). Held-out seed 7 within ±10 everywhere (author ±2.5, my regen ±5.9).
3. **Attack (three cases, all outside the author's domain).**
   a. *Seed 7 at 4,000 members* (author held seed 7 out only at 1,500): bind/D **67.9%**,
      retry 39.0%, hand-out bind 80.3% — the structure reproduces at the decisive scale on
      a fresh seed.
   b. *20,000 members, seed 1* (next rung; clamp allows it): bind/D falls to **48.6%**, the
      retry collapses to **11.6%** (below the claimed 18% floor), and the fixed tier grows
      to **31% of D**. Recomputing the endgame on the 20k mix gives 31% of D remaining and
      ceiling ≈4.7×10⁴ — the composite's "22%" is the 4k mix, not an invariant. The
      ordering survives (bind still the largest term, kill line not crossed) and the
      mix drift *strengthens* the fixed-tier lever relatively, but the ranges are
      domain-bound and the dossier does not bound them by N.
   c. *rtf 100 at 1,500 members* (author flew only at 400): bind/D **44.1%**, retry 23.3% —
      above the kill line, consistent with the author's straddle report.
4. **Novelty.** The per-event anatomy was already on the page (367f: hand-out bind 355–421 µs,
   re-fit 52–63%; 7055: the memo; a4ed/de99: the kick prices). New and real: the single-clock
   D partition across item classes with the bind share of D, the fixed tier priced at 21% of
   D (367f had the walk tier "an order behind" in per-body terms, not as a share of event
   work), the composed endgame, and the interlock sentence (bodies gap and kick gap = one
   adoption queue). A synthesis, correctly cited as such; not a repetition.
5. **Goal fit.** Prices the whole adoption queue for the board's furthest gap (28 vs 10⁹
   bodies) and the kick gap with one measurement. PRINCIPLES 19: "a fix signals the wrong
   representation" — the retry is a repair of a wrong word choice, deleted by choosing
   before compiling; the fixed tier is deleted outright ("the best part is no part"). The
   endgame is built up, not subtracted, so no lever is counted twice.

**The one experiment that would make it gold.** Stack the four verified patches (009b word
fix, 7055 memo, 5eb6/8b43 fixed tier, de99 Carlson kernel) on one branch, run the behave
suite, then this same 7-arm census plus my three adversarial arms on the stacked build. If
measured D at m4,000 lands within ~2× of the 42 ms/game-s arithmetic with digests holding,
the 4.5× and the ~10⁵ ceiling become measurements and the run moves the bodies bottleneck
by the gold margin. The 009b×7055 interaction (memo re-priced against the word-fixed bind)
is decided by the same build.

**What the author missed.**

- **The endgame block does not regenerate.** `endgame.py` hardcodes the author's census
  constants (D = 192.0, ho = 1103.6/8) instead of reading the fresh census output, so
  "every number regenerable via regen.sh" is true only because the constants are frozen. I
  recomputed with fresh inputs: 21% and ceiling ≈9.6×10⁴ — the conclusion is robust, the
  regeneration claim is not.
- **Means, not tails.** The ceiling math divides an average slope into a CPU budget, but
  today's break at 10³–10⁴ is an overflow phenomenon: m4,000 spends 192 of 300 ms/s of
  budget yet overflows 291/480 frames (worst 61.8 ms). A 4.5× cut on the mean moves the
  overflow boundary only if bursts shrink proportionally; PRINCIPLES 12 ("i care about the
  p95/99 results") asks for a worst-frame argument the dossier does not make.
- **The mix drift at the next rung** (fixed tier 31%, retry 12% at 20,000) was one arm away
  and bounds every range in the claim; the clamp was already lifted to 20,000.
- **The kick side of the interlock is weak.** The bind is 45% of a kick, so the Carlson
  lever halves the kick at best (≈240 → ≈155 µs); the kick gap (75–160 µs vs 50 ns floor)
  stays open after the whole queue lands. The lens section names this, but the headline
  ("one adoption queue, not four problems") oversells it.
- The rtf-100 hand-out prediction ("~0 hand-outs in 8 game-seconds") measured 375 in 800
  game-s — the *rate* collapsed (0.0012 vs 0.16 ev/m/gs), but the prediction as written
  failed and is not flagged against prediction 5.
