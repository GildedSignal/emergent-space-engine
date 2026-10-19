Grade: silver

**Abstract.** The wiki's named decisive experiment (encounters od 1, budget-1e9's one
binary risk) is run on the shipped tier and reproduces bit-identically from the base
commit (patch applied, 33 s, 21 MB, one core). Both toys' shapes die by measurement: no
zero-leak epoch at any E ≥ 2; the E-curve is a concave, saturating first passage
(per-kick leak falls in E at the quantum); κ-saturated at operational E (≤ 1.2× over
64×κ at E=2); the protector is near-book depletion (dues ~10⁵ passages deep).
Game-horizon P=1 column: 0 on 3 of 4 seeds; worst seed 777 gives 2.6×10⁻⁶ →
6.5×10⁻⁶ per kick at E = 2–8, 1.6×10⁻⁶ at E = 256, 6.5×10⁻⁷ at E = 1024 — 10⁻⁶-class
from E ≈ 256 up, NOT "at every E" as the dossier letters it. Churn prices at 355/E
cores; the ledger's conditional closes by measurement. Cost to adopt: one first_hit per
pair per E kicks (416 ns, e87d) plus the leak audit at the game horizon.

**Reasons.**

1. **Reproduction: exact.** Clean tree at the base commit (c41a9892), `git apply
   work/patch.diff`, rebuild, rerun every regen command: all six stored outputs
   bit-identical (book, smallh, three κ arms, dv0, seeds 777/5). 33 s wall, 21.4 MB
   peak — inside every claim. The instrument is faithful: `rots()` copies
   `arm_pair`'s integer lines verbatim at t0 = 0 (tier.rs:552–571), `first_hit` called
   with the same (c0, d, pi, 0, w), `make_belt` σ_e 0.07 cap 0.5, safety 1.1 — e87d's
   anchor class. Anchors match e87d's own dossier on origin/claude/lab-…-e87d:
   armed(10⁶) 0.7742 vs 0.774, deep flips 1.69–1.74×10⁻¹ vs 1.695/1.741, w p50
   53,946 vs 53,956 (a population median, e87d mixed a-windows — not a discrepancy).
   The synodic leg of r verifies from geometry: pi²/Δpi ≈ (7.633×10¹⁰)²/(pi·7.5×10⁻⁵)
   ≈ 1.0×10¹⁵ ticks ✓; 5.7×10⁹ ticks/kick is inherited from 0659's 27.6k game-s
   cadence (not independently re-derivable in this crate; cited honestly).
2. **Predictions: held where it mattered, failed in the letter of three.** P1 both
   controls exact (dv0 0/768k kicks — armed-but-constant, structurally incapable of
   leaking; E=1 empty interior 0/~16M intervals). P4, P5 held (flips ≈ armed·0.67 at
   H=128; H=16 flips ≤ 2.5×10⁻⁵). Held-out seeds 5 and 777 ran; seed 777 was the only
   seed that leaks at P=1 at all. P2's pre-registered independent-re-deal law
   1−(1−f)^E is dead (overshoots ×4 at E=1024) — honestly reported and correctly
   diagnosed as the finding. P3 narrowly failed at E=1024 (×3.3 vs the ×3 band).
   P6 failed on its letter by ~4 orders (pre-registered ≤ 10⁻¹⁰/kick at E=1024; the
   r constant slipped 215× — 2.3×10⁻⁸ vs the tier's 5×10⁻⁶ — a unit error,
   disclosed, corrected in the conservative direction). The gold bar's "the held-out
   predictions held" is not met by the letter.
3. **Attack (4 cases, all beyond the author's grid).** Width 1e-5 and 1e-3 (100× span
   around the tested 1e-4): book depletion width-robust (dues q50 4.7–5.3×10⁵;
   near-density ~10⁻⁶-class), no knee, concave saturation, and the P=1 column stays
   exactly 0 on both extremes. κ = 2⁻¹⁷ (512× the quantum, one octave beyond the
   sweep): no knee; E=2 P=256 within 1.3× of the quantum value (saturation genuine);
   but the per-kick curve is flat-to-humped (peak ~1.25×10⁻³/kick at E = 8–64), not
   falling — "falls in E" is quantum-scoped — and the flat P=1 column sits at
   1.6×10⁻⁶/kick. Fresh seed 12345: P=1 all 0, P=16 nonzero at E=2 (4.9×10⁻⁵), laws
   intact; P=16 constants vary ~3× across seeds. Nothing killed the claim; the
   domain statement now carries my probes.
4. **The overstatement that blocks gold.** "The game-horizon miss is bounded … ≤
   2.6×10⁻⁶ per pair per kick … under the record's 10⁻⁶-class budget at every E" is
   contradicted by the run's own table: seed 777's P=1 column per kick is
   6.5×10⁻⁶ at E=8 (20/384,000 — Poisson CI [4.0×10⁻⁶, 1.0×10⁻⁵]), 3.3×10⁻⁶ at
   E=64, 1.6×10⁻⁶ at E=256. The "≤ 2.6×10⁻⁶" is the E=2 point only, and "at every
   E" is false below E ≈ 256 on the only leaking seed. The E=1024 bound (6.5×10⁻⁷)
   rides 2 events in 3,000 intervals. Smaller letter errors: "seed 1" does not exist
   (the quoted E-shape row is seed 20261018 at κ=2⁻²⁰ while the quoted 777
   saturation is at κ=2⁻²³ — mixed dials; "at the quantum" mislabels 2⁻²⁰, the
   quantum is 2⁻²³); "leaks nonzero at E=2 at every P ≥ 16" fails on seed 20261018
   at P=16 (0/1.54M); "armed(≤16) ≤ 8×10⁻⁶" is the s1-set value — 777/5/12345 reach
   3–8×10⁻⁵ under kicking (still 10⁴–10⁵× depleted). All corrected on the author's
   page in place; the dossier keeps its letter.
5. **Novelty: real.** This is the wiki's named od 1 — 9fd1's own "E* must be frozen
   from a pooled shipped-tier boundary-flux measurement, not from the knee". No prior
   run measures the epoch-leak surface on the shipped tier (08d0 = 1-D toy, 9fd1 =
   renewal toy, e87d = decorrelation/flip rates, 1a29 = anchors/churn); docs/HISTORY
   holds nothing equivalent. The proposed page folds the result into the conflicted
   page correctly: the 34be/9fd1/e87d paragraphs are carried verbatim (I diffed
   against the conflicted lab page's sides), the contradiction is marked resolved
   with the resolution being the measured claim, and 08d0 is marked superseded, not
   deleted.
6. **Goal fit.** Board live question 2 (encounter work at 10⁹) and budget-1e9's one
   binary risk: the churn row prices at 355/E with a measured-leak rider, a 64–256×
   cut on that row at E = 64–256. PRINCIPLES: "a failed expectation is not
   automatically a failed method: diagnose which one broke" — both toys broke and
   the diagnosis is the deliverable; "compute only surprises" — one integer decision
   per pair per E kicks; "Floats may explore; only integers decide canonical
   outcomes" — every decision in the surface is integer (first_hit), floats only
   build sections, as shipped. One caution for adoption: 0659's p = 1.0 note stands
   — the epoch rule spreads certificate re-pay, not the kicks themselves.

**The one experiment to gold:** the same surface on the thin-window co-moving class
(1a29's w ≈ 23) with P=1 statistics large enough that the freeze constant is not 2
events — then the leak-unbound claim carries its own constants across both shipped
classes and E* freezes with a CI'd leak row at every E.

**What the author missed.** (a) The "at every E" budget sentence, contradicted by
their own E=8–256 columns — the freeze would have cited a wrong bound. (b) The
Poisson fragility of the 2-event E=1024 anchor. (c) The κ-scoping of "per-kick leak
falls in E" (flat-to-humped at 512×κ). (d) "seed 1" / mixed-κ quoting. (e) The
armed(16) constant quoted from one seed. (f) The predictions' r unit slip — caught
by the author, but only after the pre-registration. The physics finding itself —
depletion, not geometry, is the protector, and neither toy's shape transfers — is
correct and now measured.
