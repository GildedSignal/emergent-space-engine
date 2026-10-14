Grade: silver

**Abstract.** Claim verified: the frozen r5 rung at engine Q VOIDs — shipped median
|Σres|/KE 7.4×10⁻³ (worst seed 1.3×10⁻²) passes the 1% bar; the pair-carry candidate
fails it (1.4×10⁻²). All six cells reproduce byte-identically from `work/patch.diff`,
and the "shipped" arm is bit-identical to the pristine HEAD law (stash-verified). But
the pass is a window, not an engine-Q property: at 10⁴:1 (engine Q) end |Σres|/KE is
2.77 median / 16.2 worst; at β 0.9 it is 0.43 / 1.14; the candidate repairs neither
(checker2 arms). Mechanism confirmed directly at 2²⁰ (γ > 20 by contacts 3–5). Adoptable
now: the mass-contrast certificate gate; dead: the three-form pair-scaled carry. Not
gold: the decisive predictions failed and the separating bar (10⁴:1 re-freeze) is
measured by checkers but not yet frozen and run.

## Reasons

1. **Reproduction.** Applied `work/patch.diff` in a clean tree, built, ran all six
   decisive cells (shipped/pair-carry × pair1000/pairequal × seeds 0–4 and 11–15):
   byte-identical to the stored logs (also re-proves prediction 6, determinism).
   `git stash` of the patched `relativity.rs` → rebuild → the shipped arm's output is
   unchanged: the "shipped" numbers measure the real shipped law, and flag-off is
   bit-identical as claimed. Tests: 21/21 green with the flag off; one fails with it on.
2. **The verdict is genuine.** `metrics.json`'s abs-median matches the frozen rung
   definition; `lab/verdict.py`'s VOID-on-passing-negative fired as recorded. One
   load-bearing subtlety the dossier does not name: the probe's own `METRIC` line
   prints the median of *signed* fractions (5.2×10⁻³), and had that value fed
   `verdict.py`, the candidate's −1.4×10⁻² would numerically satisfy `<= 0.01`. The
   `abs()` in `regen.sh` is what makes the candidate fail correctly; it is right per
   the freeze, but the instrument should print the metric it freezes.
3. **Predictions.** 1 failed as disclosed (the pre-registered coin-flip: 7.4×10⁻³ pass
   vs predicted ~2×10⁻² fail, with the honest-reporting branch pre-written); 3 failed
   (no fix form clears the bar — itself the finding); 2, 4, 5, 6, 7, 9 held; 8 partial;
   10 now direct at 2²⁰, not inferred. By the lab's gold letter (held-out predictions
   held) gold is unavailable; the failures were disclosed, not hidden.
4. **Adversarial, outside the author's domain** (my probe, engine Q, 200 contacts,
   rung normalization, ledger exact and subluminal throughout):
   - **10⁴:1, β 0.6** (the author's own named-next probe): end |Σres|/KE abs-median
     **2.77**, worst **16.2**; light body γ to 1103–1936. The 1% bar fails by
     280–1600×. Same numbers independently appear in the first checker's page note.
   - **β 0.9, 1000:1**: abs-median **0.43**, worst 1.14 — the bar fails ×40.
   - **pair-carry on both**: −11.6/−5.6/−0.04 at 10⁴:1; −0.76/−0.51/−1.9 at β 0.9 —
     same catastrophic class as shipped, no repair. The "fix is dead" conclusion holds
     outside the tested range.
   - **Mechanism**: γ crosses 20 at contacts 3–5 (β 0.6), contact 1 (β 0.9); end γ
     62–179 (β 0.6), 594–626 (β 0.9). Prediction 10 holds with margin.
   Consequence: the headline "refutes the rung's severity premise" is true **at the
   frozen scene only**; one contrast decade up, the same bar separates hard. The claim
   must be read scene-local (the dossier's "What would make it wrong" says so; the
   claim paragraph does not).
5. **Novelty.** Against `lab/wiki/contact-carry.md` and HISTORY: the parent measured
   the walk and its checker the Q-ladder; new here are the frozen rung actually run at
   engine Q (VOID), the γ-history saturation reading, three implemented fix forms with
   two named root causes (the score's unit mismatch is visible in `resolve_law`'s
   `r[0]²+r[1]²+r[2]²` over incommensurate E/p units), and two instrument bugs. The
   LCG low-bit artifact is real: replicating the sampler, the 5 rung seeds span 3
   y-offset classes ({0,12,15}, {1,3,11,13}, {2,4,14}) — exactly the observed
   t-collisions.
6. **Page.** Faithful once the first checker's corrections are in; I corrected the
   held-out median (7.4×10⁻³ abs-median, not the signed 5.2×10⁻³) and folded my β 0.9
   and 10⁴:1 γ measurements into the Domain line.
7. **Fit.** Principle 2 (error *type*: saturation of the γ³ quantum, not compounding
   drift) and 13 ("errors never compound" — saved at engine Q by margins, not
   mechanism; at 10⁴:1 not saved at all, 16× KE); H0183's discipline (a failed
   expectation diagnosed, not a failed method) is what this run did to its own rung.

## The one experiment that would make it gold

Freeze r5's bar at **10⁴:1, β 0.6, engine Q** (or worst-seed over the 1000:1 set) and
run the verdict: it separates by >6 orders against the 1.4×10⁻⁶ equal-mass control,
the probe exists, one run. That converts "the bar was mis-calibrated at one scene"
into a standing gate, and decides the certificate-gate disposition the dossier
proposes.

## What the author missed

- The 10⁴:1 arm costs seconds (my 15-run sweep: 4.2 s total); naming it "the obvious
  next probe" and not running it left the headline claim scene-local when one arm
  would have shown the defect is *larger* than ever one decade up.
- The end-metric is a snapshot of a swinging walk: every seed crosses 1% of
  instantaneous Σm|k|² by contacts 6–10, and mid-run |Σres| reaches 1.4–4.4× Σm|k|² at
  β 0.6 (250–620× at 10⁴:1). A median-at-200-contacts bar is snapshot-lucky in
  principle; the horizon/quantile bar the dossier gestures at is the right shape, and
  these numbers argue for it.
- "One digest test differs": the failing test is `low_speeds_reduce_to_the_newtonian_bounce`
  — the Newtonian-reduction contract (>1.1 quanta from the exact Newtonian outcome at
  v ≤ c/64), a substantive low-speed behaviour change of the candidate, not digest
  pinning.
- Held-out seeds 11–15 share the same three y-offset classes as 0–4, so prediction 7's
  "same classes" was near-guaranteed; a held-out set needs single-quanta y-offset
  draws (the author's own post-run note says the rule; the prediction still counted).
- `run.log`'s instrument excerpts are pre-sampler-fix scenes; `regen.sh` does not
  regenerate them (the shipped probe reproduces the physics — first-contact γ ≈ 3.4
  vs 3.9 — but not those bytes).
