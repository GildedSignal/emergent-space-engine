Grade: gold

**Abstract.** Claim: with the twin rebuilt as the exact continuum limit of the shipped
rule (receding-skip mirrored, the law's own Householder reflection, per-contact
≤ 2.5e-6 rad at every impact parameter, β ≤ 0.999), the shipped dense-order engine equals
its own continuum limit on every class metric, scene and seed — the first run's
15–45%/5× deviations were instrument error — and 87.5% of detected contacts are
no-impulse bin-crossing pass-throughs. Reproduced bit-identically. My held-out cases —
8× density, β 0.99 (γ≈3000), Q=2¹², T=2²², fresh neg seeds — all in band. Cost: nothing
in the engine; adopt the exact arm as the trapping-rung positive control (float twin the
negative) and price the pass-through rule at game scale.

**Reasons.**

1. **Reproduction.** `regen.sh` exit 0; `out/table.txt` matches every dossier number I
   checked. My own rerun of pump s3 (engine and exact) is bit-identical to the stored
   JSON on every physics field (only wall-clock differs). Raw neg arms read exactly the
   dossier's 151/34/187/247 final-γ, 251.0/246.6/250.6/250.5 max-γ, 499/562/542/530
   contacts; the `srskip` arm lands on 247.3. Pre-contact identity (neg, T=2⁹/2¹⁰)
   verified identical to the digit. Every engine residual finite (checked across all 14
   stored engine arms). The structural claim "the exact twin is Q-free" verified:
   q16/q18/q20 outputs bit-identical after removing q_log2/wall_s.

2. **The twin is faithful to the shipped rule** (code read at base 234d0182): detection
   at t−1 positions with the consumed-revision gate; advance; wall-eligible set from
   pre-respond velocities; sequential pair response in id order with in-progress
   velocities; the receding-skip `dot(d,w) ≥ 0 → no impulse` exactly as
   `relativity::resolve_law:236`; the reflection is the f64 form of `targets`' Householder
   about N=(d·P_s, E_tot·d); walls flip only eligible bodies on post-impulse velocity;
   consume at new revisions. The engine's consumed-map prune (`chronon.rs:136-141`) is
   semantically equivalent (dot(d+n·w,w) is non-decreasing while k is fixed, and any
   velocity change moves a rev, voiding the gate). The patch touches no library file —
   confirmed by `git apply` on a clean tree: one new example only. Micro reproduces:
   engine↔law_reflect ≤ 2.5e-6 rad at u=0.54, β=0.999; tilt 0.144–0.156 rad vs `sr_disc`.

3. **Held-out cases of my own, all outside the author's stated domain:**
   - `dense` (512×4→64×4, 8× density, 2.2M contacts — the multi-body-bin case the author
     flagged as only statistically validated): trapped 53v50, dwell 1.002×, max-dwell
     1.097×, contacts 0.99984×, pass-through 87.5%. In band.
   - `hot` (β 0.99 heavy; lights pumped to γ 2750/3347 — the "ultra-relativistic
     untested" edge): trapped 63v61, dwell 0.997×, max-dwell 1.004×, contacts 0.9993×,
     pass 88.8%. In band.
   - Q=2¹² (16× below the author's tested floor 2¹⁶): trapped 52v49, dwell 1.004×,
     max-dwell 0.824×, contacts 0.998×. Q-flat extends at least to 2¹².
   - T=2²² (4× horizon): dwell 0.9994×, max-dwell 0.830×, contacts 0.9987×, pass 87.5%;
     trapped-at-end 43v50 — see "missed" below.
   - neg seeds 2–3 (phase snapshot): final γ flips direction (5.4 v 248.0; 97.4 v 1.6)
     while max γ (200.8v249.8; 248.5v249.0) and dwell (0.965×; 1.03×) stay one class at
     the ceiling. The attribution stands on fresh seeds.
   Disclosure: the run folder's wiki page (which the checker reads) already carried the
   first checker's held-out block; my cases are distinct from theirs except the neg-seed
   probe, which overlapped and returned identical numbers — a determinism cross-check,
   not independent evidence. The dense/hot/Q¹²/T²² probes are my own selection.

4. **Predictions.** `predictions.md` predates the decisive output (mtime order:
   predictions 42 m → dossier 28 m → patch saved 23 m; the harness saves the patch at
   author end). The decisive arm held tighter than pre-registered (trapped ±8% v ±20%,
   dwell ≤1.3% v 10%, max-dwell ≤1.26× v 1.5×, contacts ≤0.6% v 5%). Two misses, both
   disclosed and correctly diagnosed: the neg final-γ band (4.42× v 1.15× — the metric
   is a phase snapshot; max γ 1.018×, dwell 1.014×) and the pass-through ranking across
   scenes. Honest reporting.

5. **Novelty.** The main wiki page (conflicted three-way) records run 1's checking as
   silver with a *partial* twin (skip mirrored, SR mirror kept) on 4 seeds, one scene,
   and names exactly this experiment as open direction 1. This run's increments are
   real: the complete instrument validated per-contact at every impact parameter (the
   tilt is the law's own continuum plane, not rounding), five seeds × five scenes, Q-flat
   against the correct reference, the neg residual attributed, the tilt's ensemble effect
   bounded, and the positive/negative control pair delivered for the rung freeze.
   docs/HISTORY.md has no overlapping entry (its "inversion" hits are the unrelated
   compiler topics). Not a repetition.

6. **Page.** Corrected three overstatements in place: the equal-mass slow control reads
   9.7e-6 rad (the ≤2.5e-6 band is the heavy table's); trapped |Δ| reaches 8.2%
   (53v49), now "≤ 9%"; the two-body pass-through range is 55–62% on held-out seeds,
   not 57–61%. Everything else on the page is faithful to the evidence.

7. **Goal fit.** Truth risk ("a law that mints false behaviour classes") is the
   inversion lens's mandate; this closes the page's open direction 1 and makes the
   trapping-statistics rung freezable in one step (5cad's missing rung). PRINCIPLES:
   "we want determinism ≠ realistic trajectories" (#20) — held in the strongest form
   (trajectories decorrelate, contacts ±12% in neg, while every class statistic tracks
   the continuum); "A failed expectation is not automatically a failed method: diagnose
   which one broke" (H0183) — the first run's expectation died on the instrument, and
   the method now stands validated; "A test that cannot fail is a control" (#10) — the
   micro table failed on the author's own print bug before any ensemble number was
   taken. It deletes the "raise Q to heal dense-order classes" adoption path against
   the correct reference. Gold: reproduced, held-out held beyond the stated domain,
   premise kill completed with a valid instrument, adoptable within one step.

**What the author missed.**

- Trapped-at-end is the weakest metric: −17/−19% in `soft`, and at T=2²² it reads
  43v50 (−14%, outside the pump ≤8% band) while every dwell/contact metric stays dead
  flat. The frozen rung should weight dwell and contacts, not trapped-at-end, or widen
  its band explicitly.
- The pass-through rate's geometric decomposition (which closing speeds cross the bin)
  is unmeasured — acknowledged, but it is what the game-scale pricing needs.
- The tilt is bounded only by trajectory scatter here (a systematic shift below ~20%
  would be invisible, as the dossier admits); a fixed-seed tilt on/off sweep is the
  cheap tightener if the integrator intends to correct the reflection plane.
- Multi-body bins are still validated only statistically (my dense probe strengthens
  that to 8× density but is not a per-event audit of simultaneous >2-body bins).
- Minor: the dossier's micro claim "≤ 2.5e-6 at every impact parameter" silently
  scopes to the mh=1000 table; the equal-mass control exceeds it (corrected on the
  page). Immaterial against the 0.155 rad tilt, but a claim should name its table.
