Grade: gold

**Abstract.** Claim: scout-fbf9's due-band re-check rule is dead on the shipped
tier — after a 2⁻²³ kick, silent cell-mates flip armed at 5–7×10⁻⁶ per candidate per
kick (Θ(n) per body: 0.0017/0.055/0.72 at 10³/10⁴/10⁵), dv-independently, every
flip-on outside the band, ~14% carrying real events, so sound per-kick re-arm is
wholesale Θ(n−1) ≈ 355 cores per 10⁴-cell occupancy. Reproduced: regen IDENTICAL
twice; an independent rebuild matches field-for-field. Adversarials: n=3×10⁵
extends the law (3.5 flips/kick, 4 more real events); a reach sweep brackets ρ\*
(dues collapse 1.3×10⁶ → 23 intervals between 10⁻⁵ and 4.4×10⁻⁵ AU — quant-c9c7's
smooth world confirmed); 7/7 leaked events re-derived as within-reach minima by an
independent Kepler solve. Gain: deletes the due-band route; every future skip rule
is gated by the measured ~10⁻⁶ leak. Adopt: nothing to build.

**Reasons.**

1. **Reproduction.** `sh regen.sh` exit 0 twice (runner; my own rerun, 68 s) — every deterministic field IDENTICAL to `flight.out`. I also rebuilt the cell experiment from scratch in `/tmp` against the same shipped crate: n=10⁴, 400 kicks reproduces 22/21 flips, viol2_on 22/22, viol2_off 0, 3 post-events, pre-events 0, viol-due median 4.3225×10⁶ intervals — field-for-field. The flight drives exactly the shipped Phase-A path (`main.rs::kick`/`tiered_arm`: `Sorted::range` → `is_candidate` → `arm_pair` at SAFETY 1.1, verified in crates/encounters/src). The toy's GM=TAU² vs crate GM=1 mismatch resolves exactly: (r, v/√GM) maps element sets identically, so each kick is a true relative impulse of exactly dv/v in the crate's dynamics.

2. **Predictions.** `predictions.md` (mtime 15 m before `flight.out`), one disclosed amendment tied to the kept smoke log (`work/flight-smoke.txt`: same flip counts, only scoring added — the amendment is honest). P1, P2b, P4 held; P2 failed in the letter and is reported as failed; P3 failed and fired the pre-registered kill line. That line is the toy's own, verified verbatim on the parent branch (`origin/claude/lab-20261018-1025-scout-fbf9`: "Kill: flips/kick > 0.1 or band(1e4) > 1") — crossed at 0.1075, blown at 1.2 (3.5 at 3×10⁵). The run brief names this exact experiment as the gold gate ("or a clean refutation of it").

3. **Adversarial cases (mine).** (a) **n = 3×10⁵, one decade past the author's range:** 105 flips/30 kicks = 3.5 per body per kick (Θ(n) extends; per-candidate rate 1.2×10⁻⁵, same class), viol2_on = flips_on 65/65, viol2_off 0, 4 real leaked events, pre-events 0. (b) **Reach sweep across the claimed ρ\*:** violator dues 4.3×10⁶ intervals at B, 3.1×10⁶ at 10⁻⁶, 1.3×10⁶ at 10⁻⁵, then collapse to 23 intervals at 4.4×10⁻⁵ and 26 at 10⁻⁴ (quant-c9c7's ρ — smooth regime, post-event leaks vanish): the boundary is real and sits where claimed, and the reconciliation with quant-c9c7 holds. (c) **|Δn| separability:** violators at 1.3–1.7× the candidate-population median |Δn| (6.95×10⁻⁷ vs 4.32×10⁻⁷ at 10⁴; 1.27 vs 1.29×10⁻⁵ at 3×10⁵) — "no Δn cut separates them" confirmed. (d) **Independent truth check:** 7/7 dumped leak events re-solved with my own Kepler code (no crate) reproduce the reported dm to 5 digits, all strictly below reach B — the band rule provably loses real encounters.

4. **Novelty.** The parent checker's named gold experiment; neither side of the wiki conflict nor HISTORY holds the re-roll channel or the design-reach leak. Nearest prior art (library-9834/5c16, the frozen-pair strobe record; library-189e, the calendar kill) is a different claim. Two premises fall: scout-fbf9's central rule, and quant-c9c7's implicit transfer of 0-violation slack from ρ=10⁻⁴ to the design reach.

5. **The page.** Faithful on every headline number (all re-verified). Two corrections made in place: the units slip "B = 3.3×10⁻⁹ / 10⁴× below ρ\*" (5×10⁵ m = 3.34×10⁻⁶ AU; ~13× below — conclusions unaffected, both sides of the boundary still correct, confirmed by the sweep), and a checker note adding my extensions plus the window-class caveat: the violating pairs' dues (~10⁶ passages) imply ~10⁵-tick Wide windows (w/d ≈ 0.3–1), not the 23-tick cross window — the re-roll stands on the measured decorrelation (due moves ~ the dues themselves), but the margin to ρ\* is thin, which matters for the leak-gated-slack direction. The author's compressions of quant-c9c7's entry delete parentheticals but keep every number and reword nothing; the added annotation is dated and marked.

6. **Goal fit.** Board focus row 2 (encounter work at 10⁹). The refutation deletes the due-band closure route, prices the sound alternative (355 cores per 10⁴-cell occupancy — arithmetic verified: 10⁹ × 10⁴ µs / 28141.5 s), and hands every future skip rule a measured gate (~10⁻⁶ events/candidate/kick at the design reach). PRINCIPLES 9 ("A failed experiment kills that configuration, never the method") and 19 ("a fix signals the wrong representation… the right representation always just feels right": the beat is recomputed because it is not stored). Honest domain statement (2-body Kepler cells, e ≤ 0.4, cells alone; the anchor's walk channel measured separately).

**What the author missed.**
- The units slip: B in AU is 3.34×10⁻⁶, not 3.3×10⁻⁹ (off by 10³); "10⁴× below ρ\*" is ~13×. Direction and conclusions survive (sweep-verified), but the stated margin was wrong by three orders.
- The "w ≈ 23 ticks" mechanism constant is the wrong window class for the violating pairs: their dues imply ~10⁵-tick Wide windows, w/d ≈ 0.3–1. The dv-independence and due-re-draw are measured facts; the ρ\* formula built on the 23-tick window should not be reused for design work without re-derivation.
- The per-candidate flip rate is not constant in n (1.7×10⁻⁶ → 5.5×10⁻⁶ → 1.2×10⁻⁵ across 10³→3×10⁵); the "5–7×10⁻⁶" band is the 10⁴–10⁵ slice only.
- Leak-event forensics (times, distances, elements) were computed but not recorded; I had to re-dump them to verify. Cheap to keep, and they are the evidence for the strongest claim.
- The page's leak-gated-slack direction should carry the thin-margin caveat: any slack scheme that inflates the effective arming reach toward ~4×10⁻⁵ AU crosses into the smooth regime — that dial is a design lever the refutation exposes but does not price.
