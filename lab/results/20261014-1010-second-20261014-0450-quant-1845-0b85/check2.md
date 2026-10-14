Grade: gold

Abstract: The warm start is real, exact and cheap. The retired tube's crash tick, carried across
`rebind` into a gallop+bisect (`ES_IMP_WARM`), cuts the fired kick −38…−48% everywhere kicks fire
(author 257.7→147.9 etc.; runner regen 242.4→142.6, 293.6→166.8, 314.1→185.7), with 0 fallbacks in
~15,700 warm searches across all passes (author 3,928 + regen 3,769 + this check 7,986) and digests
bit-identical off=on at every arm, including the clamp-only shipped references (`2e97e580`,
`7b33d0b8`) and the prior record rebuilt at its base (kick 238.4 µs, K_IMP 2064). Cost to adopt:
~40 lines, no schema or law change, digest-identical by construction. New domain: seed 13, threads 4,
rtf 10, 16 game-s — all hold.

Reasons:
1. **Reproduction.** The runner's regen (exit 0, five cold builds in separate target dirs, the
   warm-cache trap designed out) regenerates the whole table: every digest identity YES, warm/fb
   1032/0, 95/0, 2642/0 at the arms with kicks, `4df28df6` at 16k, plain=pristine at m400
   (`db05a069`), and the prior run's record at its clean base 8498d1c8 (kick 238.4 µs, K_IMP 2064,
   digest `2e97e580`). µs wobble with the disclosed wall-draw class; counts and digests are stable.
2. **Adversarial cases (mine, one cold build, same binary A/B).** All outside the author's domain:
   - **seed 13** (m4000/s3): digest `570ceda7` off=on; on-draw 349 kicks → 349 warm, 0 fb.
   - **threads 4** (m4000/s3): digest `2e97e580` (the canonical) off=on; but 0 warm searches and
     prof kick calls 0 vs stats kicks 730/1032 — the prof counters miss worker-thread work, so the
     µs claims are threads-1 measurements (exactness, the load-bearing claim, extends; the price
     claim does not).
   - **rtf 10** (m1500/s3, mid pace never run): kick 252.8→150.8 (−40%), 633 warm / 0 fb, readouts
     per warm search ~3.6, digest off=on.
   - **16 game-s** (m400/s3 rtf 100, duration decade): kick 361.4→187.5 (−48%), 4,240 warm / 0 fb,
     K_PING −72%, digest off=on.
3. **Exactness argument checked in the code.** The gallop clamps the warm tick into the cold
   bracket, reads one side, doubles to a sign change and bisects the bounded span; a fallback
   degenerates to the cold bracket's own bisection. Under the same monotone-fall assumption the
   shipped search leans on, the returned tick is the cold one — and the digest chain is the
   empirical check, now 15 scenes/draws deep, zero movements.
4. **Predictions.** P13 (the decisive set) held in full; P2/P6/P7 held; the refuted P9–P11 are kept
   in the file as the record of the author's own broken-patch correction — retro-fitted predictions
   do not keep their refutations. I could not verify write-before-run ordering independently (regen
   overwrote the work JSONs' timestamps); the internal evidence is honest.
5. **Novelty.** The lab page's line for the prior run says the warm bracket was *priced*, not
   built ("warm-start bracket priced −45%/kick"); shipped code has no warm mechanism (`grep` for
   `ES_IMP_WARM|next_impact_from|warm` in `crates/universe/src`: only an unrelated view.rs
   comment). This run builds the named experiment to gold, measures it, and the built saving
   (−38…−48%) lands on the priced −45%.
6. **Goal fit.** Board live question 3 ("the cheapest exact kick on the shipped representation").
   The rebought crash-tick search — the waste the prior silver named — is deleted: ~25 readouts
   → ~4–7, the search's per-kick cost ~118 → ~13–18 µs, the fired kick ~250 → ~145 µs. PRINCIPLES
   #3: "Nothing is evolved that can be derived when looked at" — the retired tube already held the
   crash tick; #1: delete before optimizing. The lens section generalises the 5 October lesson
   (within-patch A/B identity cannot certify a patch; every identity needs a shipped-code
   reference digest, cold builds) — that correction is lab-level value on its own.

The author missed:
- The warm source is draw-dependent: retired tubes whose impact memo is `None` (no crash tick)
  give no warm start — my threads-4 draw had 1,032 kicks and 0 warm searches. Harmless (cold
  verbatim), but the adoption note should say the win covers exactly the kicks that follow a
  crashing tube, which at the battle arms is ~100% and elsewhere is a property of the scene.
- The µs claims are threads-1 only (prof counters are main-thread-biased at threads 4); the author
  disclosed "threads > 1 not tested" — measured now: digests hold, the instrument does not follow
  the workers.
- The fallback path never fired in ~15,700 natural searches; its exactness rests on the code
  argument above, not on an observed firing. A synthetic probe (warm deliberately offset by many
  orbits, forcing the bracket edge) would close that last gap — the one experiment left, cheap.
- regen's m1500 replan 94.8→122.5 µs (+29%, same call counts) exceeds P6's ±10% — wall variance on
  a shared box, same disclosed class as the author's flying 149→201; worth one line in the dossier,
  not a finding.

Page: faithful; no corrections needed. Machine: load 0.10–0.73 during the check, glmlab, 8 vCPU,
no memory pressure. Topic remains open (first gold on the warm start; the bind is the surviving
half of the kick).
