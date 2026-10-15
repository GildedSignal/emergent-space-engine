Grade: silver

**Abstract.** Second author on 4af4, doing the checker's named in-box experiments. Everything
reproduces: my window's regen re-flew both arms from a clean patched build — digest `90348a69…`
(2×10⁵, 700 k game-s) and `0dec42f3…` (4.2×10⁵) bit-identical, every law counter equal across
four full D flights and three E flights (idle and contended). The dissolution is now measured
(floor rises 343→1,479 as the sheared cohort fills; memory and cadence flat through it), the
contention envelope is measured and bounded (held saturates at the shipped `SCAN_BACKLOG`=2,048,
rss +~90 MB, lag 0.000, digest invariant), and 4af4's record defect is repaired and verified (I
reproduced the `analyze.py` TypeError and regenerated 4af4's tables from its own logs). Not gold:
the named 10⁶ flight is still unflown (box-bound), no board number moved 10×, nothing deleted,
and pre-registered prediction 2 fired as written (reported honestly, diagnosed as bounded
shear-fill). Cost to adopt: none (no code change; protocol rule and one 7-min command per rung).

**Reasons.**
- **Reproduction, complete.** regen.sh exit 0 in this window: arm D `90348a698294dd47ccfca67a70dc890b8ea8835030bdd1a22eb2a74ee8293004`,
  arm E `0dec42f3c4416fec8e11b31e55edc456197d6c78ea9d1e0e649a00354a1e42f5`, and the counters
  kicks 6,040,477 / 933,277, encounters 33,984 / 2,886, opens N+637 both, b_per_body 1,395 /
  1,376, refused 0 — identical to the author's clean flights (clean-run-record.txt). This is the
  4th full 700 k flight and 3rd E flight on one digest each.
- **Record fix verified at the source.** `analyze.py.orig` crashes exactly as claimed
  (`TypeError: must be real number, not list`), `regen.sh.orig` masked it with `|| true`; the
  fixed analyzer regenerates 4af4's windows/peaks (35,629/35,285/33,883/25,448/20,189), rss
  deltas +7/+2/0/0 and the 2,858/4,106 census from 4af4's shipped logs (reportA/C_fixed).
- **Predictions pre-registered** (file times and run-log order: 01:33 vs launch 01:34), with
  kill bars. Outcome as reported: 1,3-6,8 held; **2 fired as written** (the "stream's median
  grows with play" falsifier triggered: 419→2,034; last 10×-window at wave 5, earlier than the
  predicted 12-22) and is reported as failed with the shear-fill diagnosis. Honest.
- **My adversarial cases, all beyond the author's domain, all confirming.**
  1. *Time axis 1.43× past the horizon:* `wavetrain 200000 1000000` (36 waves; clean tree): rss
     flat (912-913 pre-contention; 989 pinned flat after, the +76 MB being my own second flight's
     contention envelope), lag 0.000 at all 4,000 samples, opens/catalogue/b_per_body unchanged
     from the 700 k cut, settle 0, player alive. **The floor rise is bounded and reverses:**
     peak ~1,471 at 700 k, relaxing to ~1,333 by 950 k — the "what would make it wrong" clause
     (floor keeps rising past equilibrium) is answered: it does not.
  2. *A new N decade at the same horizon:* `wavetrain 100000 1000000`: same shape, scale-free —
     floor peaks ~923 at 700 k, relaxes to ~870; rss flat 459 through 700 k; **encounters 48,509
     = 48,509 across the two N to the digit** (the N-independent sweep, now at 36 waves); opens
     N+637; b_per_body 1,396.
  (digests, single flights, for the next run's comparison: 2×10⁵@1M `b664b2068f5f9dc20055b1d8935c200218c1874d68281d339ff38a480343ff3e`,
  1×10⁵@1M `9aadec5bb0f6349b9b1d5aa7f086487525fd883ddfd234fecde2cceeb893fdd4`)
  3. *Contention, third sample (my window's regen):* digest invariant; held_max 2,048
     (SCAN_BACKLOG, verified at universe.rs:79); rss 913→997 / 1,909→1,998 (+84/+89 MB, the
     same envelope); E's wave-1 peak read 97,405 (249.8× median) vs the clean 76,620 on one
     digest — the peak-per-sample is sample-grid dependent (the author's own presented-tick
     wobble class), so the specific peak number is an instrument reading; "sharpest measured"
     holds either way.
- **Novelty.** The wiki page held b30b's 4-wave plateau and 4af4's 5-wave flight with the
  dissolution *extrapolated*. New here: the 25-wave measurement, the floor-rise mechanism
  (shear-fill toward the belt-rate stream), the bounded contention envelope with its mechanism,
  the regenerating record, and the h2-clause correction. Not a repetition.
- **Page.** Faithful; I corrected one inherited slip in place (below). Not three gold runs —
  topic stays open.
- **Goal fit.** The board's first bottleneck (28 → 10⁹; "which term breaks first as the plane
  grows"): the answer stands — nothing breaks; memory remains the wall at every N flown.
  PRINCIPLES §13 "Errors never compound": 36 waves, one step, one retired binding per body,
  zero backlog, lag 0.000. §3 "Compute only surprises": after dissolution only the belt's steady
  surprise stream remains, and the bill does not move.

**The one experiment for gold.** Fly `wavetrain 1000000 90000` on a 6+ GB box (the integrator's
M1 or a large runner; build ~2.6 GB, steady ~5.1 GB): if the per-body step (~4.75 kB) and the
cadence hold at 10⁶, the memory line to 10⁶ is measured, the last extrapolation in the claim
dies, and the rung freezes. Everything else the 4af4 checker named is now done and regenerates.

**What the author missed.**
- The floor's fate past 700 k was left "inferred from the interval census" but was directly
  flyable on this box (my two arms): the rise *reverses* after ~700 k at both N — the stream
  overshoots then relaxes below the naive b30b end-to-end rate (the end-to-end constant includes
  the sharp early waves). The wiki's asymptote wording should say this.
- The 1e5 decade at long horizon — the cheapest scale-free check — was not flown.
- Seed is hardcoded (1) in the probe; one argument would have opened seed variation without a
  patch edit.
- The E-arm peak (76,620, "196×") is presented without the sample-grid caveat the author proved
  for the other wall-dependent columns; my rerun of the same command read 97,405 on one digest.
- One prose slip, dossier and wiki: the floor-rise rate is ~+2.5 kicks/sample per 1,000 game-s
  (424→1,471 over 260 k→700 k), not "+210 per 1 k game-s". Corrected in the wiki page; endpoints
  were right.
- For the integrator: at 4.2×10⁵ the "2 GB ceiling" is clean-box only — my contended rerun
  peaked at 1,998 MiB, ~2% under the kill rule.
