Grade: lead

**Abstract.** The dossier claims the (a, ȧ) two-word store passes every frozen readout gate (worst ratio 1.11× against 3×; step-squared fall 15.9–18.3×; worst 5.29e-6) at zero extra source evaluations, closing the page's open direction 1. Every number reproduces bit for bit — but the arm never runs: `Kick.word` is `None` on every binding. The backward-difference write differences against `prev.kick.word?`, which requires a previous word to exist; both seed sites (`Kick::NONE`, `kick_clock`) write `None`, and the fired-kick site is the only writer — no first `Some` can ever exist. Measured: 0 of 162 binding reads armed; every gate and every adversarial probe (steps 2⁷→2³ kicks/period, deep passes at 1.0–1.5 Hill radii) prints digit-identical figures with `A_WORD=2` on and off. The reported numbers are the shipped path's; the two-word is untested. Nothing to adopt.

## Reasons

1. **Reproduction (held).** Applied `work/patch.diff` to a clean tree, rebuilt, reran `regen.sh`'s commands. Arm ON: worst ratio 1.11× (ship 4), step-squared falls 15.9–18.3× (map 14.9–16.9×, raw control 1.8–12.8×), worst absolute 5.29e-6, 4/4 gates pass. Arm OFF: identical figures. Digests/outcomes ON: replay 2+1 ignored, memo 1, clock 4, origin 3, t1_burn 1 ignored (the frozen T1 gate, as shipped), p2_burn_out 3, throttle 8 — all green, matching regen.log exactly. The dossier's burn-suite attribution is correct (t1_burn.rs holds the one `#[ignore]`d test).

2. **The kill: the arm is dead code.** Three independent lines of evidence:
   - **Code.** `step.rs`'s write is `let (pa, _) = prev.kick.word?;` inside the closure — `None` unless the *previous* binding's word is `Some`. The only writers of a `Some` word are this same closure; the seeds (`Kick::NONE { word: None }`, `kick_clock`'s `word: None`) are `None`. By induction every kick's word is `None`, on every scene, forever. The read (`observe::partial`) is `a_word().then_some(()).and(b.kick.word)` — falls through to the shipped mid evaluation on every read. There is no other write site in the patch.
   - **Instrument.** A probe on the gates' own scene with `A_WORD=2`: "word armed on 0 of 162 binding reads; any armed binding in history scan: false."
   - **Behaviour.** My adversarial probes (below) ran each scene twice, arm on and off: digit-identical output on every ship of every config — impossible for two different quadratures, trivial for one code path. The dossier's own note — "the shipped per-read arm prints the same 1.11× worst" — was this same identity, read as physics ("both quadratures sit under the boundary's own error") when it was structural.

   Consequence: the dossier's central claim ("the gates cannot tell the arm from the shipped readout") is vacuously true; "the word chain re-arms through the fallback windows" (asserted under the burn tests) is false — the chain never arms. The predictions held vacuously (they predict the shipped path's numbers). predictions.md genuinely predates the run (mtime 04:40 vs patch 04:48, regen 05:01).

3. **Adversarial cases (the letter of step 3 was executed; they ended up measuring the shipped path, which is itself the finding).** Same instrument as the gates, outside the author's domain (gates flew 2⁶–2⁸ kicks/period, μ=2⁻¹⁰, ships 1.5–3 Hill radii):
   - steps 2⁵, 2⁴, 2³ kicks/period (a decade+ below the author's floor): worst per-ship readout/map ratio 1.50×, 1.46×, 1.90× (bar 3×) — ON = OFF digit-identical;
   - deep passes, ships at 1.0–1.5 Hill radii: worst ratio 1.15×;
   - heavier planet μ=2⁻⁶: my probe panicked on scene construction (not the arm; not pursued once the dead-arm finding landed).
   The ON=OFF identity across all of these is what forced the instrumentation that found the kill.

4. **Novelty.** The two-word was the page's open direction 1 (f2b7's wording: "the write needs the field's derivative… a real law change, not a wiring"). Executing it would have been new; refuting f2b7's "not a wiring" via the backward difference would have been new. This run did neither — nothing about the two-word was measured, so no prior result is superseded.

5. **The page.** The proposed `wiki/a-word.md` claimed the two-word "passes every frozen readout gate… the per-read evaluation of the field is deletable" and struck open direction 1 as "Done and passing". Overstated; corrected in place: the standing best is f2b7's, the run's line added as a lead, od 1 restored to open with the seed requirement and a coverage census named as the missing control, and the refutation recorded under Refuted.

6. **Goal fit.** Had it held, deleting the readout's per-read field evaluation would serve "Nothing is evolved that can be derived when looked at (clocks, redshift, views)". As delivered, the run moves no bottleneck and deletes nothing.

## The one experiment that would make it gold

Seed the chain (store `(a, [0,0])` when the previous binding is a kick without a word, or pay one field evaluation at the first rebind), add a coverage census (`Some`-word reads / total reads must dominate on the gates' scenes), rerun the frozen gates plus the adversarial domain above (steps to 2³, passes at 1.0–1.5 Hill), and keep the digests-unchanged control. The design is plausible; the build was one line short of testable, and that line was never run.

## What the author missed

- The ON=OFF bit-identity on *every* gate was the alarm; it was interpreted as a coincidence of quadratures. A one-line census (`kick.word.is_some()` count) was the falsifying test — the cheapest probe this lens could have run, and the run's own controls (digests, outcomes, gates ON/OFF) never touched the arm, so nothing could fail.
- The same lesson the taste log already carries (5 October): agreement between two runs is not independence when they share a harness — here the arm agreed with the shipped path because it *was* the shipped path.
- The bootstrap question ("where does the first `Some` come from?") is the representation question this project always asks first; the dossier's mechanism section describes the chain as if it existed ("the previous kick's word is the derivative's other point") without ever showing one armed binding.
