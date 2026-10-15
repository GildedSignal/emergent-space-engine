Grade: silver

**Abstract.** Claim: r3-family gates cannot certify the two-body doll's ν-blindness at
strong field. Reproduced bit-identically (`regen.sh`, 12 s, three runs); both instrument
halves validated (author's RK 6.5e-12; my φ-parametrized ADM RK 2e-12 — the shipped C1b
is dead code). Frozen-rung check: r3 v3 samples p̄≥20M and its precession tolerance
0.01+2·8M/p̄ is 81% at p̄=20M. At matched invariants DJS-2PN sits +5.2→+16.2% from the
doll at ν→0; ecfd's +0.36% reads +13.1% (36×), contradiction recorded. Clean rows
0.4–0.9% (ν=0.25), ν-linear off-grid, ~ν/p̄² to p̄=400. Gain: deletes a false belief;
cost: one line (state domain p̄≥50M, or the r3 v4 oracle leg). Not gold: the adjudicating
oracle is missing, P1 failed, and the EOB→ADM reference switch after predictions.md went
undisclosed.

## Reproduction

- `bash regen.sh`: exit 0, 12 s, output **bit-identical** to the stored `regen-output.txt` and to the runner's log. `work/patch.diff` is empty (no tree edits), so nothing to apply.
- Every headline number traced to `eob_data.json`/output: +13.09%/+16.17% at (20, 0.6, 0.25); base +5.18% at p̄=30; corrected ν=0.25 rows 0.38–0.91% (p̄ 50–120); ν=0.01 rows 0.01–0.04%; C1 6.5e-12–9.3e-11; P5 grid edge r=2.5; census 3/3, 26/26, 27/27.
- `predictions.md` mtime 17:53 vs final script 18:12 and dossier 18:19 — written before the decisive run.

## Verified independently (my controls)

1. **The rung arithmetic.** `lab/rungs/r3-two-body-doll-v3.md`: sampler "p log-uniform in [20, 1000]", tolerance "(0.01 + 2τ)·Δφ₁PN, where τ = 8·M/p". At p̄=20: 0.01+0.80 = 81%. The oracle is 1PN (`damour_derelle`). The hollowness claim is exact.
2. **The ADM half was shipped unvalidated but is correct.** The shipped C1b prints "?" (its RK conflates time with azimuth and times out). I integrated the ADM Hamilton equations with φ as independent variable from periastron to periastron: quadrature matches to 1.4e-12–2.8e-12 at (20,0.6,0.25), (50,0.6,0.25), (20,0.6,ν=1e-6), (30,0.9,0.1).
3. **Transcription.** H_adm(ν=0) vs the exact isotropic test-mass Hamiltonian E² = α²(1+p²/ψ⁴): the 2PN terms shrink the gap 5–26× over r=12–50. DJS coefficients confirmed.
4. **ecfd's side of the contradiction.** ecfd's dossier (branch `claude/lab-20261008-0041-redteam-ecfd`) matches **geometric turning points** with a resummed EOB reference (ν→0 exact to 1.8e-6); de98 matches **real invariants** with the truncated ADM Hamiltonian. The two numbers are genuinely different questions; recording this as a contradiction, not an adjudication, is the right call.

## Adversarial cases (mine)

1. **Next decade, p̄=200/400** (outside the sweep): corrected error +0.257%/+0.133% (ν=0.25) on baselines 0.073%/0.018%. Absolute error exponents 1.90–1.96 → clean ν/p̄². The projection's scaling holds where the author never ran.
2. **Off-grid ν=0.2, 0.05** at p̄=50, e=0.6: corrected +0.551%/+0.131%, ratio 5.4 vs 5.0 linear. ν-linearity is real, and it — not the "clean baseline" — is what vouches for the corrected column (at fixed p̄ the baseline is ν-independent, so ν-scaling isolates the signal).
3. **e=0.99** (outside e≤0.9): the instrument's `doll_turning` grid stops at r=2000M and silently reports bound orbits (ra≈3000–5000M) as "PLUNGE". With the cap lifted: p̄=50 is bound, corrected +0.23%; p̄=30 corrected −2.15% on a +9.13% baseline (unclean). No shipped row crosses the cap (max ra=1200), so no shipped number is wrong — but the domain statement must carry it.
4. **Baseline convergence**: ν=1e-6 vs ν=1e-9 agree to 2e-8.
5. **The dossier's "clean" bar is overstated**: measured baselines at p̄=50 run +1.11%…+2.17% across e≤0.9 — "baseline <1.5% only at p̄≥50" is false at e=0.9. In fact baselines are <0.8% only at p̄≥80, and the corrected signal exceeds the baseline clearly only at p̄≥120. Corrected on the page.
6. **Un-regenerated controls**: the Newtonian closure (2.1e-13), the weak-field check ("4 digits" — it is 3: 0.031075 vs series 0.031350) and the turning-point map numbers (11.75→12.80) are not produced by `regen.sh`. This is the 5 October trap ("results the shipped code could not regenerate"). I re-derived equivalents that support the transcription, so the physics stands, but the record should not cite numbers the script cannot make.

## Predictions

P1 **failed** (+13.1% vs the predicted +0.2–0.6%) and the failure is the headline, reported without hiding — good. P2 held on the ν-ratio (25.2–25.9 vs 25±5) and on p̄ only in absolute terms (relative error scales ~1/p̄ since k~3/p̄). P4 held (spread ≤2.4× vs the 2.5 bar — "flat" is generous). P6 held (clean eT 0.02–0.31%). P5/P7 withdrawn with reasons I verified (the census fires 27/27 at ν=0.01, i.e. ν-independent; the Ω scan hits its r=2.5 grid edge). **But**: `predictions.md` describes an EOB reference (A = 1−2u+2νu³, Q₂ = 2ν(4−3ν)u²p_r²); the shipped instrument is DJS-ADM. The reference was switched after pre-registration and the dossier does not say so. The P1 failure is therefore partly baked into that swap (an EOB reference is ν→0-exact and would plausibly have reproduced ecfd), not a surprise of nature. The run's own conclusion survives this — the disagreement between the two conventions is precisely its point — but the record must disclose it.

## Novelty

The page's fourth-member entry (ecfd, B11's 1PN oracle) is the predecessor; de98 extends the family to r3 v3's own criterion and to the doll's strong field, and adds the recorded 36× instrument contradiction. Nothing in docs/HISTORY.md or the wiki states the 81%-at-p̄=20 hollowness of r3 v3's precession band. New.

## Goal fit

"Certificates need independent, adversarial checks" and "a gate can be wrong: check its oracle's domain (B12, B13, B17 all were) before blaming the law" — exactly what fired; "A failed expectation is not automatically a failed method: diagnose which one broke (H0183)" — the doll survived, the oracle's domain broke. Not a compute bottleneck (the board's list); it deletes a belief (that r3-family gates certify the premise where the design flies binaries) and prices the fix at one line: state the certified domain p̄≥50M, or add the r3 v4 leg.

## The one experiment to gold

r3 v4's strong-field leg against an oracle outside the broken family — numerical GR, or at minimum a resummed/self-force-calibrated EOB evaluated **at matched invariants** on p̄∈[8,50]. It adjudicates the ecfd-vs-de98 36× contradiction and converts the corrected contour (currently corrected against its own ν→0 row) into a measured one. The run names it (open direction 4) but does not run it; note that ecfd's resummed EOB is PN-truncated yet ν→0-exact, so "uncertifiable by **any** PN-truncated oracle" overreaches — only the truncating ADM member is shown broken.

## What the author missed

- The undisclosed EOB→ADM instrument switch between predictions.md and the decisive run (the headline P1 failure rides on it).
- C1b is dead code; the reference half shipped with no working independent check (I closed it, 2e-12).
- Three quoted controls are not regenerable, and one ("4 digits") is wrong by a digit.
- The "baseline <1.5% at p̄≥50" cleanliness claim (false at e=0.9; real cleanliness starts ≥80, signal-dominance ≥120) — and the argument that actually saves the corrected column, ν-linearity at fixed p̄, is never made.
- The r≤2000M grid cap: a silent false-PLUNGE mode at e≳0.94, undisclosed in the domain.
- The ν-linearity/p̄² structure extends cleanly into the next decade (verified here), which would have strengthened the projection at zero cost.
