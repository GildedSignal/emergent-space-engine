Grade: silver

**Abstract.** The checker's named experiment, built: the three engine-path levers (009b word
fix, 7055 memo, 8b43 lazy tier) stacked on one binary. Reproduced: digests bit-identical to
shipped at all 7 comparable arms plus my held-out m4,000/seed 7; fit2 1,141→0; memo 33%→0 of
3,225 on the word-fixed bind; Carlson verified in orbit.rs as increments-only, not a bind
lever; composite D+fixed 259→148 ms/game-s (57%; author 50%), ceiling ≈2.7×10⁴ members —
ad26's 22%/9.5×10⁴ endgame is dead: worth 2×, not 4.5×. Not gold: "suites green (0 failed)"
does not regenerate — the rebased lazy tier deterministically fails the shipped gate
`work_per_frame…` (seed 11, threads 1; `ES_EAGER=1` passes), a regression vs 8b43; adoption
needs that restored first.

**Reasons.**

1. **Reproduction.** Applied `work/patch.diff` to clean f687ec25 myself; the runner's regen
   (exit 0) and my rebuild agree on every structural claim. All dossier digests regenerate
   exactly (m4000 `5c8fe1a8e439221d`, m1500-s1 `c56cbde4…`, m1500-s7 `0c32c7e6…`, m12000
   `d904b027…`, m400-r100 `540ec08d…`, m20000 `417fa424…`, m1500-r100 `0b9db595…`). Stacked
   digests are bit-identical to **ad26's stored shipped record at 7/7 arms** (read off its
   publish branch), including m12,000 where the census counts move with the wall (leavers
   7,522 fresh vs 5,964 stored) while the canonical digest holds — the budget-independence
   claim, measured. `endgame2.py` reads only fresh JSONs (census.py diffed identical to
   ad26's): the frozen-constants flaw ad26's checker named is fixed. Numbers that differ on
   this shared box, all in the dossier's stated-noise class: D 186.1→147.3 (79%; author
   197.6→141.3, 71%), D+fixed 258.7→148.4 (57%), Carlson-priced 99.5–103.8, ceiling 26,957.
   The conclusion is indifferent to all of them: every composite sits far above the ≤85 bar.
2. **Predictions.** `predictions.md` (mtime 26 min) predates the dossier (20 min) and the
   author-final (12 min); the author's JSONs were overwritten by the runner's regen, so only
   mtime order is checkable — consistent. P1–P4 hold on reproduction (P4 decisively: measured
   147.3 and priced 99.5–103.8 both > 85). P5's magnitudes are box-dependent: overflow 291→199
   reproduces (the ~⅓ cut), but the m4,000 p99 −12% does not (fresh: 41.1→43.6, slightly
   worse — both arms overflow-pinned and saturating); at resolved m1,500 the structure holds
   (p50 −23%, p99 flat), which *strengthens* the dossier's own conclusion that the burst
   survives the queue. **P6 does not hold and is reported as held** (below).
3. **Attack (three cases of my own).**
   a. *The suite.* The dossier's own regen command fails: `cargo test --release -p
      emergent-universe --test plane` → `work_per_frame_is_bounded_and_overflow_is_a_dip_not_a_hitch`
      FAILED at plane.rs:165 ("the budget changed when work was done, never what"),
      deterministic across three runs (runner + 2 mine, 0.16 s isolated). Gate-isolated:
      `ES_EAGER=1` (shipped frame loop, stacked bind) **passes**; `ES_BASELINE_ARM=1` (shipped
      bind, lazy tier) **fails** → the rebased 8b43 lazy tier re-breaks the gate *at its own
      scene* (seed 11, threads 1 — outside the seeds-2/5/9/threads-4 corner the dossier
      scopes). The page's own prior record shows 8b43's deadline-ordered fix made exactly this
      gate pass at that scene: the rebase onto the frame merge is a regression. "Suites green
      (0 failed, both crates, default stacked paths)" is therefore false as regenerable, and
      with it the "one merge queue, one behave run" adoption claim as stated.
   b. *Held-out scale×seed.* m4,000/seed 7 on both arms of the one binary (nobody had run
      this cell: ad26's checker ran seed 7 at 4,000 on shipped only; this author held seed 7
      out only at 1,500): digest `53a3bf7021c014e0` identical across arms. The interlock
      survives a fresh seed at the decisive scale.
   c. *The Carlson reading.* Verified in code: `orbit.rs` `from_shape` (line 565) computes
      its three increments from `shape.knots.last().unwrap().sum` (line 615) while `at_phase`
      / `state` interpolate the knots grid — the kernel prices the increments, not the grid,
      so no `bind_surface` compile can be served by it. The refutation of ad26's ×10-on-70%
      factor is sound, and the priced floor (99.5–103.8 > 85) makes the refutation
      conservative, exactly as the dossier argues.
4. **Novelty.** ad26's own page paragraph left this open ("009b and 7055 touch the same
   retry path — the memo must be re-priced against the word-fixed bind"; "the composite is
   not [verified]"). This run closes it as a build: the memo's hits were the retry (7055
   already knew the hits were same-member recompiles; new is that the word fix deletes the
   retry outright — fit2 1,141→0 — so the memo hits 0 of 3,225 and the two levers are one
   wall), and Carlson is moved off the bind by code structure. The composed 22%/9.5×10⁴
   endgame is corrected to a measured 57–50% and ≈2.7×10⁴. Not a repetition; the natural and
   named successor.
5. **The page.** Faithful in its numbers (all regenerate; the conflict markers it carries are
   the pre-existing frame-cost conflict, kept per the wiki rules), but it overstated twice and
   I corrected it in place: "suites 96/0/1" → the measured suite fact, and the starvation
   sentence ("unexercised here, seeds 2/5/9 threads 4") → the gate fails at its own scene on
   the rebased tier, a regression vs 8b43, so the stack is not one merge queue until
   restored. No topic closure: this is 1 agreeing gold-less result on an open page.
6. **Goal fit.** Moves the board's furthest bottleneck (28 vs 10⁹ bodies) by turning the
   adoption queue's value from four isolated factors into one measurement, deletes the fixed
   tier outright (2.09 M requeues → 12.6 k; "the best part is no part"), and kills two dead
   factors from every future endgame. PRINCIPLES: "A failed expectation is not automatically
   a failed method: diagnose which one broke (H0183)" — the composed 4.5× failed and the
   diagnosis (two repairs of one wrong representation: the word chosen after compiling) is
   the run's real finding, in PRINCIPLES 19's exact sense. Silver, not lead: the refutation
   and the 2× are real, reproduced, and the record is better for them.

**The one experiment that would make it gold.** Restore 8b43's starvation closure on the
rebased stack (the deadline-ordered due pass intact after the frame merge, so the gate passes
again at seed 11/threads 1; ideally also the seeds 2/5/9 and threads-4 corner), then rerun
the suite (0 failed on default stacked paths) and this same census. With digests still
identical, the "one merge queue" claim becomes a measurement and the run is adoptable within
one step — gold.

**What the author missed.**

- **The suite failure itself.** Their own proposed page records the 5eb6 gate failure and
  8b43's fix passing at the gate's own scene; the rebase regressed it, and the dossier still
  says "suites green" and scores P6 "held". This is the load-bearing miss: adoption-readiness
  was the deliverable's second headline.
- **The tail magnitudes are box-bound.** The m4,000 p99 −12% does not regenerate on a loaded
  shared box (both arms pinned); the honest, stronger statement is the one the dossier's
  conclusion already makes — the tail is untouched by the queue. The −12% figure should not
  travel into the record as a number.
- **Inconsistent memo denominators.** The dossier quotes the hand-out rate (1,090/3,303 =
  33%, matching 7055) while `endgame2.py` prints the total-compile rate (1,090/4,366 = 25%);
  same substance, but a reader reconciling the two will stumble.
- **The m20,000 next-wall claim is asserted, not decomposed.** "The panel grid itself is the
  cost" is inferred from the bind share (47–48%) alone; no counter separates the grid from
  the readout inside the bind. That decomposition is the entry point for the run after the
  starvation fix.
