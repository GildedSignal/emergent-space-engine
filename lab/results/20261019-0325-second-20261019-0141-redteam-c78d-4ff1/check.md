Grade: gold

**Abstract.** r11 exists, frozen before its run (sha256 de53f498…0506 verified) and
executed: PASS — the silver's named experiment done. I reproduced everything
bit-identically in a clean tree: the four decisive configs (26 s), the independent
bisection check path (2 m 40 s), diagnostics, and c78d's base record (byte-identical,
13 s); the verdict replays PASS from my own metrics. The one-sample negative fails three
bars (p99 0.84, fmin dev 0.80, false blink 0.058); per-pixel readout holds 5% at both
pitches (1.6% at 113 samples, 4.1% at 29); c78d's doppler typo is real in its code and
moves the β minima ~1pp only. Gain: the L59 refutation becomes a one-commit guard. My
probes extend the cure (β 0.99, grazing) and find its missing axis — density (Gaussian
core errs 0.23; page corrected in place).

## Reasons

1. **Reproduction: exact, both paths.** Clean tree at /tmp, empty patch, rung hash OK.
   Author path: all four configs bit-identical to `metrics.json` (26.4 s vs the author's
   27 s). Check path (my rerun): bit-identical to `metrics-check.json`. Diagnostics:
   identical. `verdict.py r11 … my-metrics.json` → PASS; pixel-h2/pixel-h1 pass every
   criterion, the negative fails p99+fmin+blink, the positive passes — no VOID or DISPUTED
   condition is reachable (negative fails by 16×/16×/5.8×, positive passes by 2.8×). c78d's
   `orig-occlusion.py` regenerates its stored output byte-identically under my own rerun.
2. **Freeze and pre-registration.** mtime order: rung 03:31:29 → `rung.sha256` 03:33:19 →
   `predictions.md` 03:37:53 → dossier 03:45:49; the hash still matches. Every frozen-case
   prediction held, five numbers for pixel-h2 included; the two misses (pixel-h1 passes;
   arc at h = 0.15 above 5%) are diagnostics-scale, disclosed with mechanisms, and
   pixel-h1's miss is *against* the author's own kill expectation — you do not pre-register
   your candidate failing and then report it passing. Caveat, disclosed here: run.log is
   empty and `eclipse_rung.py`'s last edit (03:43:32) postdates predictions by 6 minutes,
   so run-vs-predict ordering rests on mtimes and substance; the substance is decisive.
3. **The instrument correction is real.** `orig-occlusion.py` L235-236: `cosang` is
   already v·n̂, then used as `1/(γ(1−β·cosang))` — the doppler's β counted twice; the
   correction 1/(γ(1+β·px/q)) is exact SR and moves the minima 0.535→0.5227,
   0.815→0.7999, exactly as the dossier says. Both checkers of c78d had reproduced the
   typo from its description — the author's two deliberately-different paths are the right
   structural answer to the 5-October lesson.
4. **Attack (four fresh arms, seeds 777/888, none of the author's configs).**
   - *β 0.99* (γ 7.1, the decade above the author's 0.9): pixel-h2 p99 0.024/0.017, zero
     false blink, fmin dev ≤ 0.029 — the cure extends; no pitch shrink with β needed.
   - *Grazing impact 2.8 = 0.7(R_p+R_f)*: p99 0.015 — the cure tracks the missed-eclipse
     regime where the one-sample rule reads nothing.
   - *Density — the axis the rung never varies*: a Gaussian-core fleet (σ = R_f/2, one
     aggregate, 253 uniform pixels at the frozen pitch) errs p99 0.229/0.210, fmin dev
     0.21/0.19; a two-clump fleet errs 0.14/0.36. Uniform pixel weights misprice a core
     4–5× past the 5% bar. The frozen rung is honest (its truth fleet is uniform by
     definition) but the page licensed "per-pixel occlusion" without the condition —
     corrected in place; density-weighted pixels are the same cost (direction 3's profile)
     and are the next freeze's one arm.
   - *Sub-planet R_f = 0.5·R_p*: h = R_p/2 pays 5 samples at p99 0.22, h = R_p/4 pays 13
     at 0.11 — the 5% bar needs ~80 pixels ≈ N per-ship predicates, i.e. the
     min(N, pixels) crossover the domain line claims, measured at the small end.
5. **Novelty.** lab/rungs/ holds r1–r10, no occlusion/eclipse rung; no HISTORY entry
   covers it. This is checker2 of c78d's named gold experiment verbatim (freeze the
   corrected aggregate arm — both its freeze fixes implemented: the fmin bar as
   within-5%-of-exact, the cap as the measured π(R_f/h)²·1.1, validated 0.998–1.000 to
   R_f = 30), executed with controls on both sides. Not a repetition: c78d refuted, 4ff1
   armored.
6. **Page.** Every number in the NEW(4ff1) block matches the record (checked one by one
   against metrics/diagnostics). Two corrections applied in place: the uniform-density
   domain condition at the license sentence, and a Checker3 block with my four arms. The
   Runs-list duplication is inherited from the published page, not this author's doing.
7. **Goal fit.** Not a board bottleneck (occlusion unwired today, e59e) — but it is
   principle 34's guard built the way the lab prescribes: the refutation ("an instrument
   that blinks out whole fleets carries no information", principle 28) becomes a frozen,
   mechanically-judged rung adoptable in one commit, before the view's natural first
   implementation ships. Principle 3 (the occluded fraction derivable at pixel
   resolution), principle 21 (rough first, refine at the certificate). The p99-vs-peak
   choice at h = R_p is disclosed with its license implication and the peak-bar
   alternative spelled out for the integrator.

## What the author missed

- **Density is the nearest unmeasured axis, not the exotic tails.** The dossier's
  "what would make it wrong" names photon-sphere occluders and comoving observers but
  not the game's own core-heavy formations; uniform pixel weights err 20%+ there. The
  page carried the overstatement; now corrected. One arm (density-weighted pixels) for
  the next freeze.
- The freeze-order evidence rests on mtimes (run.log empty) and the instrument's last
  edit postdates predictions.md by 6 minutes — probably a post-validation fix, but
  unverifiable from the record; future runs should tee their decisive runs into run.log.
- The "at BOTH pitches" license reads better than the fine print: at h = R_p a single
  frame can spike ~8% (peak semantics, disclosed in the dossier but worth the number on
  the page if the integrator wants per-frame worst case).

Gold stands if the second blind checker agrees: the frozen set reproduced exactly, the
held-out predictions held on every frozen number, and adoption is one commit
(lab/rungs/r11-eclipse-aggregate.md) plus the page's density clause.
