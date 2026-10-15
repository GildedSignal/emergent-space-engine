# Dossier — 20261015-1926-second-…-de98-97b0 (second author on de98)

## Claim

**The ecfd-vs-de98 36× contradiction is adjudicated, and both instruments lose: with a
primary-source 3PN EOB (ν→0-exact, RK-checked to 8·10⁻⁹, 2PN-consistent with DJS to a
3PN residual at p̄=400M) evaluated at matched real invariants on p̄∈[8,50]M, ecfd's
+0.36% is a wrong-coefficient artifact — their EOB's p_r² term F = A²·D̄ (D̄=1−6νu²)
cancels the ν-effect (per-unit-ν advance effect at p̄=400M: their form +0.005%
against DJS's −0.504%; the primary-source form A²/D gives −0.514%, 2% = the 3PN
residual) — and de98's DJS-corrected contour undershoots 1.5–13× with the wrong sign
at p̄≤30M (at p̄=30M, e=0.6, ν=0.25: corrected +0.24% vs EOB +3.10% [2PN +2.04,
4PN-fit +3.07]; at 20M: −2.7% vs +6.03%). The measured ν-blindness error is
ν-linear, e-mild, crosses 1% at p̄≈65M at ν=0.25 (at ν=0.1 ≈35M, at ν=0.01 ≈10M) —
roughly twice as far out as de98 projected — and at ν=0.25 the doll fabricates plunge
over a ≥2M-wide band in p̄ (21/21 labels at e=0.3, p̄∈[6.5,8.5]M: doll plunges, oracle
bound; at ν=0.01: 0/21, confirming de98's ν=0-artifact withdrawal). The premise's
certified domain moves out to p̄≳65M, and a resummed ν→0-exact oracle — itself
PN-truncated — does certify down to p̄≈12M (bracket 2PN↔3PN), refuting de98's
"uncertifiable by any PN-truncated oracle" in its strong form (the checker's caution,
now measured).**

## Bottleneck

The one de98 left: the adjudicating oracle. Not a compute bottleneck; it deletes two
wrong numbers (+0.36%, and the corrected column as a contour), converts the
ν-blindness contour from a baseline-subtracted projection into a measured quantity
over p̄∈[8,50]M, and gives r3 v4 its oracle prescription (one 8 s script, already
validated three ways).

## Evidence

Everything below regenerates by `bash regen.sh` (~15 s: `python3 oracle.py` →
`run-record.txt` + `oracle_data.json`; de98's own scripts were the starting point and
its doll/ADM halves are reused verbatim). Oracle: 3PN EOB transcribed from primary
sources fetched this run — Damour, arXiv:1212.3169 (lectures): A(u)=1−2u+2νu³+a₄νu⁴
(a₄=94/3−41π²/32), D≡AB=1−6νu²+2(3ν−26)νu³, tortoise P_{R*}=(A/B)^{1/2}P_R so the
canonical p_r² coefficient is A²/D, Q=z₃u²p_{r*}⁴ with z₃=2ν(4−3ν), z₁=z₂=0; 4PN-fit
bracket +ν(a₅c+a₅log·ln u)u⁵ with a₅c=23.5, a₅log=64/5 (Damour–Nagar
arXiv:1406.6913 eqs. 28–29). The EOB energy map is *identically* the design's map
(E_eff = 1+ĥ+(ν/2)ĥ²), so at matched real invariants doll and oracle share (E, j)
and the comparison carries **no baseline subtraction anywhere** (V1: the ν→0 error is
the O(ν) effect itself at ν=10⁻⁹, ~10⁻¹⁰, not a truncation floor).

**Instrument (all in run-record.txt):**
- V3: EOB quadrature vs an independent RK integration of its own canonical Hamilton
  equations, periastron to periastron: 7.7·10⁻⁹–1.4·10⁻⁸ at three strong labels
  (the EOB half had never been independently validated before — de98's checker had
  to do it for their ADM half).
- V7 (decisive structure test, p̄=400M, perturbative): per-unit-ν advance effect —
  DJS −0.5037%, A²/D −0.5139% (gap 2.0% = 3PN residual, scales as u), ecfd's A²·D̄
  **+0.0052%** (≈zero: the sign of the 6νu² term in the p_r² coefficient cancels the
  ν-effect), no-D A² −0.2543% (half). Through 2PN, gauge-invariant quantities at
  matched invariants must agree — only A²/D does.
- V2: at p̄=80–120M the EOB bracket [2PN, 3PN] sits above de98's corrected column by
  the 3PN share (relative gap 26%→15%, scaling as u; at 80M: corrDJS +0.56% vs
  EOB-2PN +0.71%/3PN +0.84%).
- V4: de98's DJS half reproduced exactly (+13.0920% at 20M/0.6/0.25 vs their stored
  +13.09%).
- V5: the doll against the true series k=3/p̄+27/2p̄²: 2.3·10⁻³ at p̄=100M,
  2.7·10⁻⁴ at 300M (ratio 8.3 ≈ 3³: exactly the 3PN residual). Corollary: the
  famous 1/√(1−6/j²)−1 used by ecfd (and quoted in de98) is **not** exact — its
  j²-expansion carries 27/2j⁴ where the true series has 45/2j⁴; ecfd's "closed-form
  e-dependence" (0.2–0.85%) was this 2PN error.
- V6 (de98's three non-regenerated controls, now regenerated): Newtonian closure
  k=6.3·10⁻¹⁴; weak-field k=0.031429 vs series 0.031350 (3 digits — de98's "4" was a
  digit wrong, exactly as the checker said, and the residual is the 3PN term);
  iso→areal map 11.75→12.77 / 48.99→50.00 against the doll's areal 12.5/50.0
  (transcription confirmed).

**Adjudication (the checker's named experiment, held out in predictions.md):**
- ecfd's convention (matched turning points), their F: +0.3575% — their +0.36%
  reproduced to 0.02 points. Same convention, primary-source F: **+3.21% (2PN) /
  +5.93% (3PN)**. The contradiction was not a matching-convention artifact: it is the
  p_r² coefficient sign (their own measured D̄-sign spread, 2.75% at 20M, exceeds
  their headline; V7 shows which sign is right).
- de98's convention (matched real invariants), their instrument vs mine, e=0.6,
  ν=0.25: p̄=20M: DJS-corrected −2.7% vs EOB +6.03% [+3.37 2PN, +5.96 4PN];
  p̄=30M: +0.24% vs +3.10% [+2.04, +3.07]; p̄=50M: +0.70% vs +1.52% [+1.16, +1.51].
  The corrected column converges to the oracle only at p̄≳80M: subtracting a ν→0
  baseline from a truncated reference does not isolate the ν-effect below that.
- The measured contour (EOB-3PN; 3PN≈4PN-fit to ≤0.5 points everywhere): ν=0.25:
  +1.4–1.8% at 50M, +2.8–3.9% at 30M, +5.6–9.9% at 20M, +10–38% at 15M, +16–74% at
  12–10M (both label conventions, agreeing within ~1.3× at p̄≥15M); crossing 1% at
  p̄≈65M. ν=0.1: crossing ≈35M; ν=0.01: ≈10M. ν-linear (ratio 25.5 at 30M/0.6),
  e-mild within ~2× at p̄≥20M (grows to ~3× at 15M). Period error same order,
  opposite sign (−1.7% at 20M/0.6/0.25). Below p̄≈12M the 2PN↔3PN bracket opens past
  8 points — no analytic oracle vouches there (better than de98's "below 30M": the
  resummed family buys a factor 2.5 in radius).
- P7 (fabricated plunge, adjudicated): at ν=0.25, e=0.3, all 21 labels in p̄∈[6.5,8.5]M
  have doll-plunge vs EOB-bound (band ≥2M wide — wider than de98's withdrawn
  estimate); at ν=0.01, 0/21 (their ν=0-artifact withdrawal confirmed; the effect is
  real and large at comparable mass).

**Predictions (predictions.md, written before the decisive run):** P1 **failed on
sign** (predicted [−4%,−0.5%]; measured +3.4% to +6.6% — at fixed (E,j) the deeper
EOB potential *reduces* the advance against the doll; my physical prior was wrong and
the sign is now measured twice, quadrature and RK). P2 held (+0.36% reproduced within
0.02 points; correct structure outside ±1%). P3 held in structure, failed in margin
(gap 0.089–0.15% at p̄=100–120M vs my 0.05% bar; scaling as u ⇒ 3PN, and V7 at 400M
closes it at 2%). P4 failed (crossing ≈65M, outside my [22,40] and de98's ≈40M).
P5 held (25.5 ∈ [18,35]). P6 failed favorably (2PN↔3PN bracket 2.6 points at 20M,
6+ below 15M — wider than my 0.8% bar; 3PN↔4PN tight everywhere). P7 held (band
non-empty at ν=0.25 and empty at ν=0.01, premature-plunge sense) with the band wider
than my upper edge (≥2M, not ≤2M).

## What would make it wrong

The 3PN EOB is not numerical GR: at ν=0.25, p̄≤15M the 2PN↔3PN bracket is the honest
systematic and it is large; near the merger band (p̄≲8M) even the resummed family is
qualitative. The a₅c=23.5 4PN term is a fiducial fit value (bracket only, and the
3PN↔4PN agreement everywhere says nothing rides on it). The period row carries a
time-convention slop (EOB real time vs Schwarzschild coordinate time), inherited from
de98; the advance k does not. An NR-calibrated EOB (TEOBResumS-class) or true NR
would refine the last digit of the contour, not its shape; the adjudication (a
36× contradiction resolved into two named instrument errors) is robust to that.

## Cost and fit

Adoption cost for r3 v4: point its strong-field leg at this oracle (the script, 8 s,
already validates itself); or state the doll's certified domain as p̄≳65M at ν≤0.25
in representation.md §1 — the number de98 wanted to write is now measured and is
twice their projection. PRINCIPLES: "Certificates need independent, adversarial
checks" (three independent instruments now cross-check; agreement is not independence
— ecfd and de98 shared the *absence* of a structure test); "a failed expectation is
not automatically a failed method" (H0183): the doll did not get worse — the two
oracles that judged it were wrong in opposite directions; "measure before claiming".

## Record fixes (the checker's remaining flags on de98)

- The EOB→ADM instrument switch after predictions.md is now disclosed in the record
  (this dossier and oracle.py's header); both instruments live in one regenerating
  script.
- All three non-regenerated controls regenerate (V6), with the weak-field digit
  corrected.
- The e≲0.94 false-PLUNGE cap (r≤2000M grid in `doll_turning`, inherited verbatim)
  is disclosed: nothing in the shipped rows crosses it (max r_a = 90M at p̄=50, e=0.9
  in my grid; de98's checker already verified their rows too).

## The lens

Second-author lens: it confirms priors (the ν-effect should be small and clean) and
nearly missed the sign inversion — P1's failure is the run's most useful event. What
it may have missed: no numerical-GR anchor (the "1.5 s class reference" ecfd
prescribed for B11 would close the last systematic); the plunge census uses the
EOB separatrix as truth, which near p̄≈7M is itself only qualitative.
