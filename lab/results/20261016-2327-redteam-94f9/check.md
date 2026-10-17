Grade: lead

**Abstract.** The two-body doll's ν-flank, re-measured against a 2PN-only EOB oracle:
advance gap 3.3% at 20 M, crossing B1's 1% at p ≈ 55 M; period crossing at 28 M; ISCO off
4.9%. Reproduced bit-for-bit in 6 s; instrument verified (A²/D per the kept source,
converged quadrature, pre-registered predictions, 2 of 5 held). Already measured and
adjudicated in the base tree (ecfd, de98, 97b0, 8–15 Oct: primary-source 3PN + 4PN
bracket, crossing 65–70 M, plunge band ≥ 2 M). The headline is instrument-relative: the
3PN term (a₄ = 18.688, its own source) moves the crossing to ≈ 25 M. New only: the B2
crossing (robust, 26–28 M), B11's judged-rule arithmetic, B4's E = 1 j* band. Adopt:
nothing.

## Reasons

**1. Reproduction (clean tree, base a9e1fe61 = HEAD, patch.diff empty).** `./regen.sh`
reproduces every dossier number bit-for-bit in 5.8 s: crossings 55.2 M / 27.8 M; gaps
3.33%/0.214% at (20, 0.3); ISCO u = 0.174897 (r = 5.718 M, +4.9%); j* = 3.9331 (gap
1.67%, capture radius 5.08%); ν-scaling 3.33% → 1.31%. The runner's regen.log matches the
author's stored flank-out.txt (trailer line only).

**2. Instrument checks (independent).**
- The truth model is faithful to the cited source: A₂PN = 1−2u+2νu³ (eq. 16), map
  (eq. 20), and D = 1−6νu² is exactly the paper's (AB)₂PN, used correctly as the p_r²
  coefficient A²/D (this is the convention ecfd got wrong; the kept source text, line
  393, settles it).
- The "adv rad" column is Δφ/π (display only); all gaps and thresholds are raw radians.
  Hand quadrature at (20, 0.3): 0.3913·π = 1.229 rad vs Darwin's closed form 1.226 —
  consistent with the claimed 0.2–0.8% closed-form error.
- Convergence: GL 400×48 reproduces every table gap to 4 decimals.
- ISCO and j* re-derived through independent code paths (grid+brentq on dĤ/du; double-root
  algebra j*² = 15.468 → j* = 3.933). V1–V4 anchors pass; note all four are D-free, so
  they cannot catch a D error — the D implementation had to be checked against the source
  (it is right).

**3. Predictions.** Pre-registered: predictions.md mtime 23:36:38 precedes flank.py
23:47:07 and the stored output 23:49:47. P5 (ν-linear) and P2's p = 50 value held; P1/P3/P4
missed and honestly reported. The V1 anchor was swapped after the run (Darwin closed form
→ 30-digit quadrature) — disclosed, and the swap is legitimate (the closed form really is
2PN-only). Note P1's "miss" is oracle-relative: against a 3PN oracle its bracket (10 <
p < 30) holds.

**4. Adversarial cases (mine).**
- Outside the swept e: e = 0.9 at ν = 0.25 gives 1.32% / 4.12% / 10.96% at p = 50/20/12 —
  the flank extends monotonically; no reversal.
- Outside the swept p: p = 10, 8 give 12.3% / 30.8% — same.
- **3PN sensitivity (decisive):** adding a₄νu⁴ with a₄ = 18.688 (the run's own kept
  source, eqs. 17–18) moves the advance gap 3.33% → 1.25% at p = 20 and 7.79% → 1.99% at
  p = 12, and the B1 crossing 55 M → ≈ 25 M. The dossier's own budget ("3PN contamination
  ≲ 0.3% at p ≥ 20") is wrong by ~7×: it compared a₄νu⁴ to the gap percentage directly,
  missing the ~25× orbit-integral amplification that makes the flank large in the first
  place. The B2 period crossing is robust (27.8 M → 26 M).

**5. Novelty (why lead).** The flank was already measured three times, all in the run's
base tree, on the topic's own page (lab/wiki/handoff.md):
- ecfd 20261008-0041 (silver): first 2PN measurement, later shown to be a
  wrong-coefficient artifact;
- de98 20261015-1747 (silver): ν-blindness contour, uncertifiable below p̄ ≈ 30 M;
- 97b0 20261015-1926 (the adjudication): primary-source 3PN EOB + 4PN-fit bracket —
  measured contour with the 1% crossing at p̄ ≈ 65–70 M (ν = 0.25; ≈ 79 M at e = 0.9),
  the 2PN↔3PN spread named "the honest systematic" (2.6 points at 20 M — matching my
  measured 2.1), the fabricated-plunge band ≥ 2 M wide, the label-convention ambiguity
  (1.3–4× at 15–20 M), and the closed-form refutation with the correct mechanism
  (27/2j⁴ vs 45/2j⁴, not e-dependence — this run repeats ecfd's wrong attribution).
This run's headline (55 M, 3.3% at 20 M) contradicts the adjudicated contour without
engaging it; the difference is exactly the known single-oracle systematic plus the
unaddressed label convention. "A repetition is not gold, however well done" — here the
repetition is also the weakest of the four instruments.

**6. Scene facts the run overstates.** G1/G2/G4 are test-mass scenes (no ν anywhere:
bound_table, g4, oracle::capture_angular(1.0)). "B4's own scene" is wrong: G4's frozen
cases L/4 ∈ {0.5…1.5} straddle the 3.93–4.0 band without misclassifying even at ν = 0.25
(3.88 < 3.9331 → both capture; 4.12 → both scatter); the misclassification needs a j the
gate never samples at a ν it never runs. The dossier's better sentence stands on its own:
the boundary has no gate at all. Also verified in the run's favour: B11's envelope
arithmetic (81% at p = 20 vs worst 3.63%; 1.32% vs 1.19% at p = 50) and its judged-period
rule (5/a² ≤ 5×10⁻⁴ → a ≥ 100 M, gap 0.007% there — correctly sized). Oracle hygiene
(attack #2): no shipped oracle uses the Darwin closed form — oracle.rs wraps
gr_oracle::periapsis_elliptic (exact quadrature). The named risk is empty today.

**7. Goal fit.** Real in kind (sizing a missing gate at the cheapest layer; "gates are
frozen before the first run and never weakened after"; behaviours judged, never
trajectory identity) but the record had already sized this gate better; nothing is
deleted, no premise is newly killed, and no gate is written.

**What would have made it count:** reading lab/wiki/handoff.md first. The 97b0 page names
r3 v4's strong-field leg on the 3PN oracle as the next step; contributing to that (or
measuring the one number 97b0 lacks — the period crossing, which this run does get
robustly, 26–28 M) with the bracket, under both label conventions, would have been a real
increment.

## What the author missed

- The topic page (lab/wiki/handoff.md, 15 runs) holds the adjudicated answer; the census
  page's "unmeasured flank" line was already stale at the run's base.
- The 3PN term was sitting in the kept source (eqs. 17–18, a₄ ≈ 18.688), and the same
  paper warns the PN-expanded A is a poor representation below ~6GM/c² — the estimate
  should have been a measurement (it is a 10-line patch, and it halves the headline).
- The label-convention ambiguity (candidate-labelled vs oracle-labelled turning points),
  measured by 97b0 at 1.3–4× for exactly p̄ 15–20 M — never mentioned.
- The B4/G4 scene contents (test-mass, no ν; case set fixed).
- P1's miss is oracle-relative (it holds against a 3PN oracle), which cuts both ways and
  was worth saying.
