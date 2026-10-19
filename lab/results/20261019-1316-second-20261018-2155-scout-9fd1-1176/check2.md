Grade: gold

**Abstract.** The checker-named experiment (leak(E, κ, P) on the shipped tier's own dues,
e87d's replica verbatim — I checked `rots_ticks` against `tier.rs:560–565` line by line)
shows no zero-leak knee: the leak is nonzero at every E ≥ 2 and saturates E-flat at the
event rate — 7.2×10⁻⁶/pair/touch at belt-real P=4 = 7.2×10⁻⁹ per candidate per cell kick,
140× under 1a29's 10⁻⁶ budget, so E* is cost-limited (E_cell ≈ 10⁶ ⇒ the 355-core row →
3.5×10⁻⁴ cores). Mechanism: δc0 = 1.02w per quantum kick (e87d's missing constant); the
flip flux is κ-saturated at 2w/pi over 512×. I reproduced all four outputs **bit-identically**
and pushed six arms beyond the flown dial — non-dyadic E, κ 128× weaker and 8× stronger,
P=64, the thin corner — every one confirms. Cost to adopt: nothing to wire; the E* freeze
completes after the one named run (armed staleness).

**Reasons.**

1. **Reproduction.** Clean tree at the recorded base c41a9892; `git apply work/patch.diff`
   clean; `./regen.sh` equivalent run mode-by-mode: `grid.csv`, `heldout.csv`,
   `anchors.txt`, `flips.txt` all **bit-identical** to the stored files (diff, not spot
   check). Full pipeline ~5 min, within budget. The replica claim holds at code level: the
   instrument's `rots_ticks`/`due_ticks` reproduce `arm_pair`'s integer setup exactly and
   call the shipped `arm_sections`, `first_hit`, `cone_pairs`, `make_belt`.
2. **Controls, both sides.** dv0: 0 misses at every E ≤ 256 (55 events; the one E=1024
   artifact reproduces in my runs too, disclosed in the dossier); E=1: 0 misses at all
   (κ, P); no-arm: 1.000 everywhere; flips dv=0: 0 flips bit-exact. The dv0 control also
   passes on my own non-dyadic E variant (0 misses at E ∈ {3,5,7,12}).
3. **Predictions.** `predictions.md` predates the author's finish (mtime order; priors in
   it match the regenerated anchors/flips tables exactly). P1, P5, P6 held (held-out seed
   424242 reproduced bit-identically); P2 held in its main assertion (no knee; 1−1/E at the
   quantum E=2: 0.48 vs 0.5) and failed in its letter at 2⁻²⁶ — reported as failed, with
   the right reading (quasi-static dip); P3 partial (event rate 1.48× over 512× κ, flat
   5% over 512× at quantum+); P4 failed in letter (P^0.66; the P·1.3×10⁻⁶ + 1.5×10⁻⁶
   decomposition fits 1/4/16). Honest reporting of own failures throughout — the marks of
   genuine pre-registration.
4. **Adversarial (mine, all beyond the author's range).**
   - Non-dyadic E ∈ {3,5,7,12} at the quantum, P=4, 2 seeds (the author tested only
     powers of two, all dividing T=2048 — a cadence-aliasing hole): miss 0.361/0.599/
     0.741/0.789, interpolating the dyadic curve smoothly; no aliasing; leak nonzero at
     every E ≥ 2; saturates at the event rate.
   - κ = 2⁻²⁸ and 2⁻³⁰ (32× and 128× below the author's weakest): leak still nonzero at
     every E ≥ 2 (E=2: 3/117 and 2/127; Wilson lower bounds ~0.5–1%), rising to 0.94 by
     E=1024. The "no zero-leak knee" claim survives a 128× downward extension of κ.
   - κ = 2⁻¹¹ (8× above the author's strongest): miss 0.490 at E=2 and 0.755 at E=4 ≈
     1−1/E exactly — confirming the law is exact under full re-roll and an envelope at
     the quantum; event rate 7.8×10⁻⁶/touch (κ-flatness extends); no knee.
   - P = 64 (4× above the author's max): event rate 9.47×10⁻⁵/touch, leak saturates
     exactly there; per cand per cell kick 9.5×10⁻⁸ — 10.5× under budget even at this
     extreme, so the freeze readout is robust to P's ×2–3 uncertainty.
   - Thin corner (a=1, σ_e 0.3, 10⁻³ band): w p50 38,117, δc0 = 1.684e4 = **0.442w** at
     the quantum (0.055w at 2⁻²⁶) — not 1.02w, yet the leak is still nonzero at every
     E ≥ 2 (0.102 at E=2) and saturates at 1.22–1.27×10⁻⁵. No knee in the thin class.
   - The first checker's in-page note is fully grounded: every number of its arms that I
     re-ran (κ 2⁻¹¹ E=2 range, P=64 9.5e-5, thin 0.44w/0.055w/0.10/0.996/1.2e-5,
     119/125 vs 125/130 events) reproduces exactly.
5. **Novelty.** The published page's open direction 1 (from 9fd1) names this experiment
   verbatim: "e87d's integer replica with an epoch dial and a κ dial, pooled seeds:
   measure leak(E, κ) on the real due structure … the one experiment between the epoch
   rule and a freezeable E*." 08d0 was a toy with φ₀ fixed; 9fd1 a renewal toy (re-dealt
   dues); e87d measured decorrelation, not the epoch leak. Nobody had measured the leak
   on the tier. The run also closes the page's registered contradiction (knee vs no
   knee) with one attribution: both toys were right about their own idealizations.
6. **Goal fit.** Board item 2 (encounter work at 10⁹): the epoch rule is the named
   355-core-row lever, and the run inverts its freeze question — the leak budget never
   binds, so the dial's cost is the only constraint. PRINCIPLES: "compute only
   surprises" (the leak is the surprise rate, now measured E-flat and 140× under
   budget); "the simulation tells us what's next not us" (the toys' knees were
   instruments, not laws — the tier decides); a per-touch flat 7×10⁻⁹ leak is an error
   that cannot compound. Numbers the shipped code regenerates, on the design's own
   representation, integers deciding.

**What the author missed.**
- The "1−1/E law" is the full-re-roll envelope, not the quantum behaviour: at belt-real
  P=4 the measured E=2 miss is 0.16 against the envelope's 0.5 (armed-state persistence),
  converging only by E ≳ 64. The dossier's evidence paragraph quotes the P=1 arm where it
  fits; the in-page checker note corrects this, and my κ=2⁻¹¹ arm (0.49/0.755 ≈ exact)
  pins the correction. The verdict (no knee, E-flat leak) is untouched.
- Only dyadic E values, all dividing T=2048 — closed by my non-dyadic arm (no aliasing).
- Sub-flown κ unexplored — closed to 2⁻³⁰ (leak still nonzero; the quasi-static dip
  deepens but never closes).
- The leak is priced in arm-window units (a sound superset of real contacts) — fine and
  conservative, but the real-contact leak at the thin corner is one more number the
  freeze could use.
- The freeze readout (3.5×10⁻⁴ cores) remains conditional on the unmeasured
  caught-but-late (armed staleness) channel — correctly named as open direction 1; until
  that run, the row-level number is a bound on one channel, not the adoption.
- Trivial: the P=4 quantum E=256 miss is 0.9932, quoted as "1.00" in the dossier's list
  (E=1024 is 1.0000).

Page: faithful; the author's Runs entry self-labels "(gold)" — with this check and the
first's, gold stands. I appended a blind-second-check note to the proposed page; nothing
else needed correction (the first checker's two corrections are grounded — I re-measured
their numbers).
