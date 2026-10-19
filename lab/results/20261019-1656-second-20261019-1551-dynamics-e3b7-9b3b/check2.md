Grade: silver

**Abstract.** Claim: Bounce+tide fail the cold-belt gate, the kicks alone hold it
(Pass belt flat through H=49152; both prior digests regenerate bit-for-bit), and the
pump's address is the DK_CAP clamp zone below r≈2.1q: orbits held outside it,
ejected inside, endpoint speeds 577–708k = the grinder's 686–740k. Everything
regenerates from a clean rebuild. My a=100q ladder confirms the pericenter law at a
third semi-major axis (constant 2.1q strict, not 2q); my fleet×Pass flight shows the
season is entirely contact-mediated (esc 800 vs 1379) plus a one-event clamp
slingshot (262144→700993 in 5 ch). Gain: fix list = Pass belt bodies or exact inner
zone; the gate gets its constant. Silver: P3's registered <2% drift failed (+9.3%)
yet labeled "held".

**Reasons.**

1. **Reproduction (clean tree, my own build).** Applied `work/patch.diff` myself;
identical 7.46 s build. A1 rerun: digest `b73b06dc9d725a58…` **bit-for-bit**, contacts
3 072 187; O_a70_e0.5 integers identical to the author's. All expected digests
regenerate (G_s1 `e3462444…`, C_s1 `634d9918…`, GW `79b89629…` walls 14896, G_s2
`420ef2ff…`, C_s2 `e903ff6d…`, C0 `e8a69ff7…`, A4 `e98306bb…` onset 12236). Every
dossier number recomputed with my own script from the TSVs: A1/A2 maxk 91993→92196
frozen t=19362, A3 95298→104180 frozen t=5306 (verified: no maxk change after),
season peak 64-ch window at t=7808 = 173× the cold same-time window (my 102877/595
vs author 102874/592: window-alignment hair), shell 77/21, esc 1379/1371 and
1374/1373, esc50 t=2211 (first esc≥800), C0 discriminator 1352 contacts / maxk
379827 at t=12288, rms 77.7→91.8q, GW walls 14896, the full e-ladder table
integer-for-integer.

2. **Predictions.** `predictions.md` pre-dated the flights (36 m vs 8–9 m file times);
the post-prediction boundary arms (0.975/0.98/0.985) are disclosed as such. P1/P2/P4
held exactly — two bit-for-bit digest predictions, the strongest kind. P5, the
pre-registered mechanism discriminator, resolved to branches (i)+(ii) as predicted;
branch (iii) refuted. **P3 did not hold in its registered letter**: "maxk drift < 2%"
failed at +9.32% (esc=0 and the frozen tail held), yet the dossier's Predictions
section says "P3 held". The number is disclosed, the label ignores the registered
bound. By the integrator's own precedent (taste log, 1 October: the law red-team,
silver, "one held-out prediction failed … and was reported as held"), this caps the
grade at silver.

3. **Adversarial probes (three; two outside the author's and the first checker's
range).** All confirm; one sharpens a constant.
   - **a=100q ladder** (third semi-major axis; T=12014 ch, H=168192): e=0.97
     (r_p=3q) bounded — drift 0.11%, achieved e exact, clamps 0; **e=0.98 (r_p=2.0q,
     exactly the gate line 1−2q/a) EJECTS** (t=70628, 5 clamps); 0.981/0.99 eject
     faster (46870/30270). The held/ejected boundary is a pericenter law at every a
     tested — but the safe constant is **2.1q strict** (the aligned clamp radius),
     not the dossier's 2q: an orbit at the 2q line is already unsafe. The marginal
     band (1.96, 2.1)q that the first checker found pumps-without-ejecting at a=70q
     (≥28 orbits) **ejects at a=100q within 6 orbits** — a horizon-limited caveat,
     not a stable band. Page corrected in place.
   - **e=0.5, a=70q, 4× horizon** (393216 ch, 56 orbits): still bounded; rmax never
     exceeds the 14-orbit value 106.04q; pericenter creep −0.4% over the extra 42
     orbits. No slow mid-e pump; the author's boundedness verdict extends in time.
   - **Fleet×Pass** (H=8192, never flown under Pass by anyone): esc stops at exactly
     800 — the unbound fleet itself; **zero belt-body evictions** (Bounce twin at the
     same horizon: 1379 evicted, n_in 200, maxk 739345). The fleet season is entirely
     contact-mediated, closing the dossier's "inferred, not measured" gap at the belt
     level. Bonus signature: one hyperbolic fleet body is clamp-slingshotted
     262144→700993 in 5 chronons (t=390–394) — inside the grinder band, by a body
     never on a bound orbit: the clamp pump's cleanest one-event proof.

4. **Novelty.** The published page (updated: e3b7) leaves the pump's address unknown
   ("symmetric/rotational rounding … MU ladder" as unflown directions). The isolated
   e-ladder, the clamp-zone boundary, the one-body grinder reproduction and the gate
   constant are new; no HISTORY entry covers them. Folding the prior checkers'
   flights into a regenerating record is the sanctioned second-author structure.

5. **Page.** Faithful, with the first checker's corrections folded; I added a
   Checker2 block and the gate-constant fix (e < 1−2.1q/a strict) in place.

6. **Goal fit.** chaos-shadowing open direction 2 via the board's smoothness line.
   P19: "a fix signals the wrong representation" — the clamp zone is now the
   *measured address* of the wrong representation, and the fix list shrank from
   "redesign the tide" to two items (Pass belt bodies; exact inner zone), cadence and
   outer rounding killed with digests. P2: the boundary is a type boundary
   (held/ejected) read off integer columns. Checkable per body within one step.

**The one experiment that would make it gold:** fly the belt's Bounce
self-destruction with per-body e-histograms (the run's own named gap) and show
contacts walk bodies' e across 0.97 into the clamp zone directly — my fleet×Pass
probe shows contacts are *necessary* (zero evictions without the response), but the
e-walk itself is still inferred from endpoint speeds and the Pass/Bounce contrast.
(And label prediction outcomes against their registered bounds.)

**What the author missed.**
- The gate constant is unsafe at its own line: 2.0q at a=100q ejects (5 clamps);
  the adoptable form is e < 1−2.1q/a, strict, orientation-blind.
- The fleet×Pass control — one 6-second flight — converts half of the inferred
  mechanism into measurement and carries the single cleanest clamp-pump signature.
- The a=36 block period 3619 scales T ∝ a (Kepler: 2595 ch), so "27 orbits" is
  ~38 orbits actually flown; harmless because the rmax columns are running maxima
  (drift verdicts are period-insensitive), but the count is wrong. Likewise "14
  orbits" at a=70q is 13 complete.
- Letter overstatements: "Keplerian maxk to 0.1%" (deviations reach 0.80% at
  e=0.97, −0.58% at e=0.01, +0.73% at e=0.06); "achieved e to 3 digits" (2 digits
  at e=0.06: 0.065); "686–740k ≈ v_esc(1q)" (v_esc(1q)=775k; 0.88–0.95×);
  "P3 held"; esc50's definition (first esc ≥ 800) unstated.
- The three discarded cadence variants (f53fe500/89cd6c20/ed4d26e9) are not
  regenerable from the shipped patch — the onset-invariance claim rests on
  unregenerable flights (the cadence kill itself stands on A4's digest + onset).
- Inherited from e3b7's block: "elastic impulses cannot raise maxk" is false as
  general mechanics (equal-mass elastic collisions can raise one body's speed
  component); the Pass/Bounce contrast carries the argument without it.

Machine: every process ≤ 12 s, well under budget; flights in `/tmp/check2/`
(A1_mine, O_a100_e{0.97,0.98,0.981,0.99}, O_a70_e0.5_h393216, G_s1_h8192_pass),
scripts `/tmp/check2/recompute.py`, `/tmp/check2/analyze_mine.py`. Tree restored
after the rebuild.
