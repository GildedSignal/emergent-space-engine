Grade: silver

**Abstract.** Post-merge (f7f6d87, shipped at 17ace3e6), the ship's clock is exact in every
regime the record had never flown, and the two new walls are real and correctly sized: a held
retro key brakes to a crossing (γ 30.7→1.208) then pumps back (γ 186.7+) — brake-to-rest needs
attitude control, killing HANDOFF item 3's held-key plan; and the far `Range` refusals are the
state→key fit's arithmetic, not the key (`from_invariants` rebuilds the same key at every
refusal point). All dossier numbers regenerated (sweep bit-identical, 81/484 refusals; pump,
69,660-refusal turnburn, silent leave death of fwd2_farstar). Checker extensions, all outside
the author's range: pump reproduced from γ 5 and γ 300 starts; refusal points pushed to
periapsis 1.6e10 M (8× deeper); fwd15 flown to the 2^40 window end — **alive at γ 2,056, k flat
at 1.09e-8, zero refusals: the old γ≈1,800 wall is gone on shipped code.** Adoption cost: none
(measurements); the fix it points to is one fit-path change. Not gold: `predictions.md` was
written after the runs (self-disclosed), so nothing was held out.

**Reproduction.** The runner's `regen.sh` exited 0 (234 s) and I re-ran every piece from the
patched tree: `clock_domain` re-run is bit-identical to `domain_sweep.txt` (ok 403, refused 81,
17.9 ms); `flights.txt` matches the dossier line for line (brake_g30 min γ 1.2082 at t=3.26e10,
pump through 186.7; turnburn γ 1.1856, peri 2.1145e10, refusals 69,660; fwd2_farstar
`LOST t=98515415 fault=None refusals=0` after a k=0.5259, E=1.000000 cycle; E→1⁺ compiles at all
22 periapsis values; k·peri ∈ [1, 1.0001] at E ≥ 100; `NoBoundOrbit` only at small peri × huge
E — 6 rows). Numbers that differ from the dossier, all from the regen's one extra checkpoint
past the author's 55 s cap: clock_relerr reaches 1.96e-6 in brake_g30 (dossier: ≤ 1.7e-6) and
3.6e-6 at γ 259 in fwd15 (dossier: 1.0e-6 at γ 334 — point value, not a bound). The engine is
deterministic per checkpoint: my probes reproduce the author's k/peri/γ exactly at matching t.

**Predictions.** `predictions.md` opens "# Predictions — verdict (written after the runs)" —
no held-out predictions exist; the misses it reports (turnburn's wrong dive sign, fwd2_farstar's
leave) read as genuine but cannot be verified as pre-registration (the original flight outputs
were overwritten by regen; run.log is empty). Same bar as r3 v3: this alone caps the grade.

**Attacks (mine, beyond the author's domain).**
1. *Deeper into the refusal region* (`check_farkey`): at E=1.1 with periapsis 3e9/6.32e9/1e10/
   1.6e10 (author's deepest refusal: 2e9) and E=3 at 6.32e9/1.6e10, `from_state` refuses
   `Range` everywhere while `from_invariants` builds the key cleanly (peri exact, k to 4–5
   digits). The `Topology` hits on my `Passage::compile` reconstruction also occur on the row
   where `from_state` succeeds — the author's disclosed reconstruction artifact, not the key.
2. *The pump at both ends* (`check_flight`): switch at γ 5 (below their 30): brakes to γ 1.0177
   then pumps through 21.87, clock ≤ 4.5e-12, zero refusals. Switch at γ 300: brakes 315 →
   sampled min 12.5 → pumps through 393.4, clock ≤ 5.6e-6. The pump is start-γ universal; note
   the author's own window held **zero** post-switch checkpoints for brake_g300 (SWITCH at
   t=1.6476e11 then TIMEOUT) — their "after braking and repump start" was extrapolation, now
   measured.
3. *The old wall, re-measured on shipped code* (`check_flight fwd15deep`, tmax 2^40): γ 841 →
   1,099 → 1,718.5 → **2,055.9 at the window end, alive, zero refusals, k flat at 1.0915e-8**
   (≫ 2⁻²⁹ — the old wall's signature is absent), worst clock_relerr 1.3e-5 at γ 1,879. This is
   open direction 4 of the pre-merge page, measured in the lab for the first time (C1's
   `--ignored c1_to_the_leave` had shown it on the integrator's own run).
4. *The leave vs a crash*: `fault=None` is set by both death paths in `boundary_clock`
   (step.rs:663–670); fwd2_farstar died at r ≈ 1.1e9 with the star's surface orders below —
   the leave, as claimed.

**Novelty.** The topic page's four prior runs are pre-merge (e128, a1a4) or view-side (efb2 ×2);
HANDOFF 7f660071 already recorded the far-`Range` limit's *existence* (~2.7e8 M) and C1's leave
flight. New here: the mechanism discrimination (fit arithmetic, not the key), the acceptance map
with k ≈ 1/peri E-independence (the merged design's premise, measured), the pump, the leave as
the slow-far-flight end, and the 69,660-refusal survival (refusal counts cannot certify a lost
flight). Not a repetition; nothing in docs/HISTORY.md covers the post-merge regimes.

**Goal fit.** The board's first live question (`high-gamma-clock`, "the regimes it has not
measured"). PRINCIPLES: "It is a game" — the pump is a playability fact, error type over error
size; "A fix signals the wrong representation" — the evidence says the *representation* (key +
gap) is right and the *fit arithmetic* is the fix's target, which is exactly the discrimination
that principle demands before paying for a rebuild.

**Page corrections made** (in `wiki/high-gamma-clock.md`): the γ-300 reversal is now attributed
to the checker (the author's window had no data for it); the clock error band widened to what
the regenerated and extended flights show (≤ 2e-6 at γ 30, ≤ 5.6e-6 at γ 300, worst 1.3e-5 at
γ 1,879); "and it compiles" softened to the measured 5-of-8 with the reconstruction caveat; the
E_key figure corrected to the regenerable 0.62% at γ 307; the forward-flight extension to γ 2,056
folded into the Domain bullet.

**The one experiment for gold.** Pre-register `predictions.md`, then fly on the prograde-nose
build (`wt/play`, HANDOFF item 3): (a) the pump's threshold under a prograde nose and what
brake-to-rest actually requires; (b) the in-flight E→1 crossing (the sweep covers it only at
exact periapsis); and (c) re-derive L from the flight's own tube words at a refusal point,
closing the discriminator's reconstruction caveat. Same dossier plus held-out predictions that
hold is gold.

**What the author missed.** (i) brake_g300's "same shape" was asserted with zero post-switch
checkpoints in the window — half of the γ-300 claim was unmeasured at publication; (ii)
`regen.sh`'s turnburn headline awk is broken (matches only the `# turnburn15` header line,
prints "turnburn max refusals:" empty — the 69,660 is real but not regenerated by the script);
(iii) the clock error band was quoted from point values, understating the tail by ~3–10×
(1.96e-6 regenerated at γ 190; 1.3e-5 at γ 1,879 in my extension); (iv) the E_key "1.6% at
γ 334" checkpoint is not regenerable from the shipped window (regen cut at γ 307: 0.62%);
(v) the lens's own flag is correct and worth repeating: a scheduler reading `refusals` as
distress would kill a healthy 69,660-refusal flight — that semantic should reach the frame-cost
work.
