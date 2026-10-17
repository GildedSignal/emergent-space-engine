Working...
Check complete. **Grade: lead** — written to `lab/results/20261016-2327-redteam-94f9/check.md`, with the author's wiki page corrected in place where it overstated.

**What held up:**
- Reproduction bit-for-bit in 5.8 s (clean tree, base = HEAD, empty patch); the runner's log, the author's stored output, and my run all agree.
- Instrument sound: D = 1−6νu² verified as the paper's (AB)₂ᴾᴺ with the correct A²/D convention (settled from the author's own kept source — the exact convention a prior run, ecfd, got wrong); quadrature converged (GL 400×48 identical to 4 decimals); ISCO and j* re-derived through independent code paths; predictions genuinely pre-registered (mtimes 23:36 < 23:47), misses disclosed; B11's envelope and judged-period arithmetic verified.
- Adversarial extensions (e=0.9, p=8/10) confirm the flank grows monotonically inward.

**Why lead, not silver/gold:**
1. **Already known.** The flank was measured three times in the run's own base tree — ecfd (8 Oct), de98 (15 Oct), and the 97b0 adjudication (15 Oct) with a primary-source 3PN EOB + 4PN bracket: 1% crossing at p̄ ≈ 65–70 M, plunge band ≥ 2 M, label-convention ambiguity quantified, and the Darwin-closed-form finding with its *correct* mechanism (27/2j⁴ truncation, not e-dependence — this run repeats ecfd's wrong attribution). The author's topic page was never read.
2. **The headline is instrument-relative.** Adding the 3PN term (a₄ = 18.688, sitting in the run's own kept source, eqs. 17–18) moves the B1 advance gap 3.33% → 1.25% at p = 20 and the crossing 55 M → ≈ 25 M. The dossier's own error budget ("3PN ≲ 0.3%") is ~7× low. Only the B2 period crossing (26–28 M) is robust.
3. **Scene overstatement.** G1/G2/G4 are test-mass (no ν); G4's frozen cases don't misclassify even at ν = 0.25 — "B4's own scene failing" needed a case and a ν the gate never runs.

Genuine increments kept on the page: the robust B2 crossing, B11's judged-rule arithmetic, and the E = 1 j* capture-band framing. Oracle-hygiene attack resolved clean: no shipped oracle uses the closed form.
