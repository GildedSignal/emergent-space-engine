Grade: gold

**Abstract.** Every root-doll belt ship steps on the doll's clock — 2^step_log2 per P_D (77.24 d, not the record's 88 d), interval 2.814×10⁴ s p50, flat in a across 2–3 AU — not the own-period law; effb's published 10⁹ kick-rate law (2⁷/P_own, "code-verified") is the secondary-doll law read onto the root doll, wrong 15–31× at the plane's belt. Reproduced bit-identically (fresh seed-1 N=4000 run; runner regen). My adversarial cases: N=20000 seed 5 identical; step_log2=5 gives exactly 4× the interval (1.126×10⁵ s), verifying the dial anchor on shipped code; belt first events land 13.3–15.3 ks (events/body 0.01→1.00), matching interval/2 and taleb-6138's wave. Recomposition: 148× the flying-pace budget at 30 µs; birth-wave staggering mandatory. Adoption: zero code — re-anchor the step_log2 decision and the 10⁹ ledger on P_D.

**Reasons.**

1. **Reproduction.** `git apply work/patch.diff` on a clean tree, `cargo run --release -p emergent-universe --example cadence -- 4000`: every physics number identical to `cadence-4000.txt` (kicks +101,624, events +205,339, belt events mean 4.00, all percentiles); only wall-time digits differ (13.9 vs 14.0 s). All dossier numbers traced to the outputs; compose.py's products re-derived by hand (8.207/1.066/0.103/0.0039 cores; 148×/242×/14×/0.54× overruns; wave 9.09×10⁵ = 26×).

2. **The mechanism is code-grounded, not just measured.** `step.rs:601` `on_clock() == doll 0 && Ship|Player`; belt ships are `Kind::Ship`, `doll: 0` (`scenario.rs:261-262, 343`), so `step.rs:554` routes them to `plan_clock` → `ext::constants`, whose documented law (`ext.rs:26`) is exactly Δs = 2^−k·P_D/f′. `step_for` is unreachable for them. P_D is Kepler-consistent (Cinder periapsis 0.3515 AU, e = 0.1, star ≈ 1.28 M☉ → 77–79 d): ladder.txt's 88 d was the wrong constant, and this run's 77.24 d is the right one.

3. **Adversarial cases (four, one outside the author's domain on two axes).**
   - *N=20000, seed 5* (5× the author's largest N, fresh seed): interval p50 2.814×10⁴ s, quartiles 2.8177→2.8056×10⁴, rate 3.553×10⁻⁵, counterfactual 6.770×10⁵ (24.1×), events/body 4.00 — all constants stable at the next decade.
   - *step_log2 = 5* (a configuration the author extrapolated in compose.py but never ran — the actionable claim): interval 1.126×10⁵ s = exactly 4× the shipped one, rate ÷4, kicks/orbit ÷4. The dial anchor is P_D, verified, not assumed.
   - *First-event timing probe* (advance to 13,000 vs 15,000 game-s): belt events/body 0.01 → 1.00 — first kicks land between them, i.e. at interval/2 ≈ 1.41×10⁴ s, inside taleb-6138's independently measured wave window (13,377–14,473 p01–p99 on 199,700 bodies). The instrument reads the executed cadence, not a plan artifact.
   - *Novelty arithmetic*: 1738's cube cadence axis (457× averaged-vs-shipped) sits inside the own-period law's 427–853× at 1–2 AU, i.e. it was built on effb's law; at the plane's measured belt it is ~13,000×. The "inherits the correction" claim is right, conservatively.

4. **Novelty.** The bare mechanism was on record (ladder.txt 123-124: "2⁷ per period of Cinder… whatever its own period"; kick-cadence page: "one doll-wide Δs tied to the fastest secondary"), but the live wiki record said the opposite: effb's nladder entry, "code-verified… a pure birth constant", feeding the 10⁹ ledger, the checker's 5.3-core line and 1738's cube. This run measures the law on shipped code, arbitrates the contradiction (both records right in their own dolls), corrects the constant (77.24 d, +14% on ladder.txt's own 10⁷ composition) and recomposes. A premise correction of a load-bearing number, not a repetition.

5. **Predictions.** Genuinely pre-registered (17:31, before any output file; the misses prove it — a post-hoc "prediction" would have matched). The discriminators that separate the two laws all held: P2 (interval in window; wave anchor), P3 (flatness: slope ≈ −0.01 vs +1.5 demanded), P6 (steady state to the sixth digit), P7 (instruments within 7%). P4's p50 missed its band by +39% (one rounding octave; disclosed, mechanism held); P1's 88 d miss *is* the finding; P5 (locals) was dropped with a disclosed instrument bug and no claim made. Honest reporting throughout.

6. **Page.** Faithful to the evidence; one overstatement corrected in place (the 3071/7497 roster reproductions are a code-path reading, not a measurement — now marked as such). The inherited 7f99/6138 conflict markers are kept, correctly left for adjudication (both runs awaiting grade). Not three agreeing gold runs — the topic stays open.

7. **Goal fit.** Board #1/#5: the steady-state event rate is the belt's whole CPU bill at 10⁹, and its central constant was composed from the wrong clock. PRINCIPLES #22 "the simulation tells us what's next not us" — the anchor is the doll's clock, a property of the state, not a choice; the run deletes a wrong dial anchor at zero code cost and hands the integrator the coarsening certificate question (2,674–5,484 kicks/orbit vs the old 512 bar) as the named follow-up.

**What the author missed.**

- The one-command dial falsifier (step_log2 = 5 → exactly 4× interval) was left unrun; compose.py's table was extrapolation until I ran it. It holds to four digits — the gold-making lever was one command away.
- A prose slip in the dossier: "26× the steady stream… 14× the whole 4-core box" — 10 s/s is 14× the *flying-pace budget* (0.72 core-s/wall-s), i.e. 2.5× a 4-core box. compose-out.txt itself is correct; only the dossier's parenthesis mislabels the reference.
- The correction factor is period-dependent: 24× at the plane's 2–3 AU belt, ~8× at 1.5 AU (P_own/P_D). The dossier states the domain; the Runs line's "corrected 24×" should be read at the plane's belt.
- The two-clocks picture's secondary-doll half is still code-path-only (the locals' instrument bug was disclosed, not fixed); one run of a corrected readout, plus the dynamic-P_D probe (a source rebind moving the doll's clock), would close the picture.
- The wave-staggering conclusion at 10⁹ (26× the steady stream for ~1.1×10³ game-s) is composed, not simulated; a 10⁶-body birth-wave run would measure the drain's absorption directly.
