# Dossier — 20261016-2327-redteam-94f9 (lens: premise red-team)

**Claim.** The two-body doll's "ν enters only through the energy map" (representation.md
L37, law.md L39) is measured against a 2PN truth at ν = 0.25: inside B11's domain the
gate's own letter holds, but the law's flat budgets break — periastron advance exceeds
B1's 1% for p ≲ 55 M (3.3% at 20 M, 7.8% at 12 M), the radial period exceeds B2's 0.1%
for p ≲ 28 M, and the plunge boundary has no gate at all while being wrong by 4.9%
(r_ISCO 6.0 M against the truth's 5.72 M) with B4's own "no misclassification" standard
failing on its own scene (E = 1 flyby, j* = 3.933 against the law's 4.000).

**Bottleneck.** Not a board bottleneck: this is lens target 1 (the two-body doll), the
one surviving premise of the 20261016-1207 census left with an unmeasured flank. The
gain is not speed but licence: the census's open direction 3 ("a behaviour gate against
a 2PN-or-better oracle is the missing licence for the merger scene") now has numbers,
so the missing gate can be written to size instead of guessed. Nothing is deleted; the
merger scene (equal-mass plunge, the strongest-field scene the game sells) is shown to
sit exactly where every existing gate stops looking.

**Evidence** (all from `python3 work/flank.py`, 6 s, shared Linux x86 — orders of
magnitude only; regenerate with `./regen.sh`):

Candidate = the doc's law: exact-Schwarzschild relative dynamics (A = 1−2u, D = 1) plus
the EOB energy map Ĥ = √(1+2ν(ĥ−1)). Truth = 2PN EOB, A = 1−2u+2νu³, D = 1−6νu²
(Damour, arXiv:0802.4047 eqs. 16, 20, 21, source text kept in `work/eoblec.txt`). Both
share the exact ν = 0 limit, so the gap between them *is* the ν-dependence the premise
denies. Compared at matched real invariants (Ĥ, j) — the tube's own key.

Validation (before any measurement counted):
- V1 candidate at ν→0 vs an independent 30-digit mpmath quadrature of the same
  Schwarzschild problem: max rel err 5.7e-7 (map round-trip noise at ν = 1e-8).
  This anchor replaced the "Darwin closed form" 2π[(1−6/p)^{−1/2}−1], which the run
  showed is only 2PN-accurate (e-dependent discrepancy 0.2–0.8% at p = 20) — a
  red-team finding about its own instrument, not the design.
- V2 circular Ω² = u³ at ν→0: 1.05e-9. V3 truth's circular binding-energy series:
  a1 = −0.77091 vs −0.770833, a2 = −2.7635 vs −2.7839 (fit truncation).
- V4 eccentric path → circular Ω continuously (3.3e-3 at e = 0.05, O(e²)).

The flank at ν = 0.25 (equal mass), gaps (truth−candidate)/truth:

| p/M | e | advance gap | B1 (1%) | period gap | B2 (0.1%) |
|---|---|---|---|---|---|
| 100 | 0.3 | 0.53% | ok | 0.0068% | ok |
| 50 | 0.3 | 1.11% | FAIL | 0.028% | ok |
| 20 | 0.3 | 3.33% | FAIL | 0.214% | FAIL |
| 20 | 0.6 | 3.63% | FAIL | 0.133% | FAIL |
| 12 | 0.3 | 7.79% | FAIL | 0.873% | FAIL |

Crossings (e = 0.3): advance 1% at p ≈ 55 M; period 0.1% at p ≈ 28 M.
ISCO: candidate 6.000 M (exact) vs truth 5.718 M, +4.9% plunge radius; +1.8% at ν = 0.1.
Capture at E = 1 (B4's scene): (u*, j*) candidate (0.2500, 4.0000) vs truth (0.2634,
3.9331): a j = 3.96 marginally-bound flyby is scattered by the truth and captured by
the law — a misclassification band of 1.7% in j*, capture radius off 5.1%. Both flank
effects point the same way: the law over-plunges equal-mass binaries.
B11's envelope (1% + 16/p) covers the worst measured precession gap in its domain
(3.63% at p = 20 against an 81% allowance): its letter holds; its period arm judges
only a ≥ 100 M, and the measured period gap at that boundary is 0.007% — the guard is
correctly sized, so B11 is self-consistent. The failures are against the flat budgets
(B1, B2, B4's standard) in p ≲ 55 M, and at the plunge boundary, where no gate looks.
ν-scaling: gaps scale linearly in ν (3.33% → 1.31% when ν: 0.25 → 0.10).

**Predictions** (predictions.md, written before the run): P5 (linear in ν) held;
P2's p = 50 value held (<0.05%). Missed, all honestly: P1's crossing predicted in
10 < p < 30 M, measured 55 M (my pre-run estimate divided the gap by the full cycle
angle, 2π + advance — the same error I then found and fixed in the script's first
output); P3's ISCO range [0.185, 0.215] against measured 0.1749 (direction held:
inward); P4's j* gap 3–10% against measured 1.67%. The misses run both ways (flank
bigger than guessed for precession, smaller for ISCO/capture), so no direction bias
in what survived.

**What would make it wrong.** The truth is 2PN: at the plunge (u ≈ 0.17–0.26) its own
3PN error is ~0.2–2% (a₄νu⁴ ≈ 18.7·0.25·u⁴), smaller than the measured 5% but not
negligible; the plunge-boundary numbers are order-of-magnitude and their sign is
corroborated by the literature's EOB ISCO trend (inside 6 M for ν > 0). The advance
and period gaps at p ≥ 20 M (u ≤ 0.13) carry 3PN contamination ≲ 0.3% — below the
reported 1–8%. If the integrator adopts a 3PN or NR-calibrated merger law, the flank
shrinks by that remainder and the missing licence becomes a gate-writing task, not a
law change. Adoption cost: none for the law (no change proposed); the adoptable item
is the gate: a 2PN-oracle arm for B11 below p = 20 M and a comparable-mass arm for
B4's capture scene, both sized by these numbers. Fit with PRINCIPLES: "A laboratory
result never counts as integrated qualification" and "gates are frozen before the
first run" — this sizes a gate before it exists, at the cheapest layer (float, 6 s);
"Behaviours matter, not continuum fidelity" — judged on advance, period and
classification, never trajectory identity.

**The lens.** A premise red-team weighs exotic cases by likelihood of being seen; the
equal-mass plunge is the least exotic strong-field scene the game sells, which is why
it ranks first here. What this lens may have missed: everything not two-body — the
view's gather, the dense order in the field, and any cost question (this run measures
physics licence, not compute). The instrument lesson is recorded above (the Darwin
closed form is a 2PN truncation; any future rung using it as an "exact" oracle would
inherit a 0.2–0.8% e-dependent bias at p = 20 — worth a checker's eye on B1's oracle).

Ranked attacks, per the lens brief (only the first is measured; the rest are named
with the rung that should catch each):
1. **Two-body strong-field flank** (above). Rung that should catch it: B11 with a 2PN
   oracle arm at p < 20 M, or B4 extended to comparable masses. None does.
2. **B1's oracle hygiene**: if any behave oracle uses 2π[(1−6/p)^{−1/2}−1] as "exact"
   Schwarzschild precession, it is 0.2–0.8% wrong at p = 20 in an e-dependent way —
   a negative control that fails for the wrong reason. (Named; not inspected in the
   crates this run — the checker can grep it in minutes.)
3. **§6's "AI decisions: likely the largest total, and unknown"** contradicts the
   board's "AI off the plan" — stale letter, no physics. No rung; the integrator's
   one-pass amendment (census, open direction 1) already covers it.
4. **Premise that survives, worth recording**: the dense order's lockstep tick does
   not violate principle 14 ("ticks make no sense" targets synchronization of idle
   regions; where everything changes every light-crossing, a tick is the cheapest
   order). The census's principles audit gap is partially filled by this reading.
