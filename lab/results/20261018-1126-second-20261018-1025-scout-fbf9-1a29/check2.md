Grade: gold

**Abstract.** The scout checker's named gold experiment, flown on the shipped Phase-A
tier, and it kills the silver's due-band rule by that run's own pre-registered kill
line: quantum kicks (2⁻²³) flip silent cell-mates armed at 5–7×10⁻⁶ per candidate per
kick, dv-independently (2⁻²³→2⁻¹⁴), with every flip-on outside the band and ~14%
carrying real events — sound re-arm is wholesale Θ(n−1) (355 cores per 10⁴-cell at the
checker clock). I reproduced every deterministic field bit-identically in an isolated
build; my adversarials extend it a decade (n=10⁶: 6.6×10⁻⁶/cand, 79/79 outside, 6 real
events), confirm it on a fresh 10⁵ seed and a cold σ_e=0.01 belt, bracket the claimed
regime boundary ρ*≈4.4×10⁻⁵ AU from both sides, and re-derive all 3 leaked events as
real with an independent Kepler solver. Adoption cost: nothing to build — the rule is
deleted from the design space; the leak (~10⁻⁶ events/cand/kick) gates future skip rules.

**Reasons.**

1. **Reproduction.** My own `cargo build` (isolated `CARGO_TARGET_DIR`) + rerun: every
   deterministic field of `flight.out` IDENTICAL (69 s); the runner's `regen.sh` also
   exit 0 / IDENTICAL. `work/patch.diff` empty; `git status` clean; the flight crate
   builds against the shipped `crates/encounters` untouched. Instrument fidelity
   verified against the shipped source: `Sorted` U-range scan → `is_candidate` →
   `tier::arm_pair` (SAFETY 1.1, `ext = pi + 2pj` slack, integer `first_hit` due) is
   exactly the path `main.rs::kick` drives; the due/band/viol2 semantics match the
   crate's own. The GM=TAU² kick model is element-space convention-free (v²/GM
   invariant), so the fractional kick is exact on the crate's GM=1 doll clock.

2. **Predictions.** `predictions.md` (11:49) precedes the final `flight.out` (11:54);
   the smoke run (11:45) is disclosed as a kept amendment that pre-registered its own
   P3 failure while keeping the kill line. P1/P2b/P4 held; the P2/P3/P5 letter
   failures are the result, reported as such; the pre-registered kill criterion
   ("2⁻²³ violations > 0 growing in n ⇒ the toy's window model is dead on the shipped
   tier") fired as written (0.1075 at 10⁴, 1.2 at 10⁵).

3. **Adversarial cases (mine; independent of the first checker's).**
   (a) **n = 10⁶, two decades beyond the author's range:** 79 flips-on / 12 kicks =
   6.6×10⁻⁶ per candidate (inside the claimed band), viol2_on = flips_on 79/79,
   viol2_off 0, 6 real events; violators' |Δn| 5.1×10⁻⁵, tracking the cell width — no
   Δn cut separates. Θ(n) and the leak extend a decade further.
   (b) **Fresh seed 31337 at 10⁵:** 5.5×10⁻⁶/cand, 22/22 outside the band, 1 real
   event — not a one-seed artifact.
   (c) **Cold belt σ_e = 0.01:** scanned still n−1 (the Binet-cone premise holds),
   rate unchanged (0.055/kick), 22/22 outside — the channel is e-dispersion-blind.
   (d) **Sub-quantum dv = 2⁻²⁶:** flips_on 0 in 200 kicks (~11 expected at the claimed
   rate) — the channel dies below the belt quantum. The kill (at the design quantum)
   is untouched, but "re-rolls under any kick" overstates: it holds for kicks ≳ the
   quantum. Page annotated.
   (e) **My own reach probes around ρ* ≈ 4.4×10⁻⁵ AU:** at 1×10⁻⁵ the re-roll
   persists (violator dues 3.9×10⁶ intervals); at 6×10⁻⁵ (above ρ*) the quantum flips
   collapse to 2/100 with violator dues ~4×10² intervals, and 2⁻¹⁷ gives 138 flips
   with 16 real events — the dv-dependent walk regime. The boundary and its direction
   are real; quant-c9c7's smooth world reconciles exactly as claimed.
   (f) **Independent Kepler re-derivation of the leaked events:** all 3 post-kick
   events at n=10⁴ are real — my own Newton/anomaly solver gives 1.411/1.481/1.976
   ×10⁻⁶ AU against the reported 1.412/1.481/1.976 ×10⁻⁶, all below the 3.342×10⁻⁶
   reach. (My first pass rejected them on a 6.28× clock slip in my own propagator —
   the crate's doll convention is n = 1/a^1.5; fixed, the events stand.)

4. **Novelty.** The published page (with its pre-existing quant/scout merge conflict)
   holds the toy-only silver and quant-c9c7's smooth-regime slack; b509/277d/fe6b
   priced cost, not soundness. No prior run measured per-kick re-arm soundness at the
   design reach on shipped code; the refutation, the dv-independence, ρ*, the leak
   rate and the quant reconciliation are new. This is the scout checker's one named
   experiment, done exactly.

5. **The page.** Faithful; every number traces to `flight.out` (all re-verified
   above); the Runs entry, Refuted entries and the contradiction resolution match the
   evidence. The dossier's B "3.3×10⁻⁹ AU / 10⁴×" units slip is corrected in the page
   (B = 3.342×10⁻⁶ AU, 13× below ρ* — matches `reach_au` in the regen consts); the
   "0.35 cores on SI" arithmetic checks (355 × 28141.5/2.82×10⁷). I added a checker-2
   bracket: the 10⁶/fresh-seed/cold-belt extensions, the verified events, and the
   2⁻²⁶ qualification.

6. **Goal fit.** Board row 2 (encounter work at 10⁹): the row's last cheap closure
   (the due band) is shown wrong on shipped code, by the run's own pre-registered
   criterion, with the surviving constants confirmed and the leak number any future
   skip rule must gate. PRINCIPLES 19 ("a fix signals the wrong representation… the
   right representation always just feels right" — the beat is recomputed because it
   is not stored) and 9 ("a failed experiment kills that configuration, never the
   method" — the toy's constants that survive are kept). Gold: reproduced, the
   decisive pre-registered prediction held, a premise is deleted from the design
   space, adoption costs nothing.

**What the author missed.**
- The 2⁻²⁶ collapse: the re-roll channel needs kicks ≳ the belt quantum; "any kick"
  overstates the domain (found by my probe d).
- The dossier prose carries the B units slip (3.3×10⁻⁹ "AU", 10⁴×) — fixed in the
  page by the first checker; the code and regen consts were always right.
- The mechanism sketch (w ≈ 23 ticks ≪ d ≈ 3×10⁵) is loose: the violating pairs are
  the wide-window overlap class with effective w/d ~ 0.3–1 (first checker's bracket);
  the decorrelation measurement, not the window arithmetic, carries the refutation.
- The leak fraction "~14%" spans 7–24% across configs (7.4% at seed 777, 23.5% at
  σ_e 0.3) — the headline uses the 10⁴/10⁵ configs; the range belongs in the page.
