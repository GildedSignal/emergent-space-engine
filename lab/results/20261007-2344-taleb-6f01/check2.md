Grade: gold

**Abstract.** The gold co-orbital phase-rank certificate (20261006-0346) is safe only while
S = N·Δ/2π ≲ k: at any statistical formation spread, mean-anomaly rank silently drops 90–97%
of contacting pairs, true-longitude rank survives static orientation but cracks under the
epicyclic wiggle or window drift, and period/phase-density triggers stay blind. All three
sweeps reproduced bit-for-bit in a clean tree (pilot 1.4 s, wscan 73 s, escan ~5 min); every
dossier table matches its JSON. My attacks: fresh seed 73.0% vs 72.0%; the drift term the
author never measured confirmed (λ misses 16.1% at S = 6.75, max rank 12); the truth finder
exact under a directed non-adjacency attack (0 shadowed contacts in 425 extra λ-close pairs).
Cost to adopt: one dimensionless gate, S = N·(Binet extent)/2π ≲ k, λ sort key, cone tier
otherwise — before `b-coorbital-cert` ships.

**Reasons.**

1. **Reproduced exactly.** `work/patch.diff` is empty (no repo edits); reproduction is
   `cert.py` alone. pilot.json, wscan.json and escan.json all compare physics-identical
   (only wall-clock `seconds` differ). Every number in the dossier's tables matches the
   stored JSONs: M-misses 0.6/23/72/87/95% across D; N-scaling 57/72/87% at D = 0.5;
   escan M-misses 90/95/97/97/93/97% with λ-cracks 52/20/38%; ρ-insensitivity 72/72/70%;
   `miss_lam_enc` = 0 everywhere including wide-belt; Binet radius monotone in both
   families; `dn_rel` flat at 1.4977e-04 while miss goes 0.6 → 95%. Controls both behave:
   aligned-gold 149 contacts, 0 miss, max rank 3; wide-belt 100% M-miss.
2. **Predictions.** `predictions.md` (32 m) predates cert.py (26 m), pilot.json (26 m),
   wscan.json (25 m), escan.json (17 m). The author reported two honest failures
   (D-point values low; lamsafe λ 20% vs < 2% predicted) and drew the right conclusion
   (the S_λ parameterization needed e·sin(Δϖ/2), the law itself is stronger).
3. **My attacks (beyond the author's).**
   - Fresh seed (D = 0.5, s = 99): miss_M pairs 73.0% vs 72.0% — the ±5 pp held-out claim
     holds; λ = 0.
   - k-sweep (registered held-out): k = 2 → 88.1% vs model 91.6% (holds); **k = 8 → 43.4%
     vs model 66.5% — the closed-form miss-fraction `1 − 2πk/(N·D)` fails in magnitude
     (23 pp)**. Direction is conservative: the model over-predicts miss (contact selection
     weights small gaps, as the author noted for D-points), so a gate on S errs toward the
     cone tier and never silently drops. The safety law itself (S ≲ k safe, S ≫ k broken)
     held on every axis.
   - Window drift (asserted in the domain formula, never measured by the author): aligned
     e-vectors, da = 5e-4, N = 300 → S = 6.75 > 4; λ-rank cracks at 16.1% (max rank 12),
     brute agrees. The Δn·W term is real.
   - Truth-finder independence in the scattered regime: the author's brute check covered
     only the aligned pilot, and a random 200-pair subsample in the scattered regime is
     vacuous (0 contacts). Directed attack: all pairs ever λ-close within 3 neighbours
     (425 non-adjacent candidate pairs beyond the adjacency truth) — **0 contacts missed
     by λ-adjacency** in both headline cases. The instrument is sound where the
     certificate fails.
4. **Novelty.** HISTORY.md runs through H0215 (6 October) with no entry bounding the
   co-orbital certificate; the gold 20261006-0346 appears only in the board's taste log,
   unbounded. law.md's Binet points (U, V, W) are the cited representation and the gate is
   expressed in them. Nothing prior measures the certificate's domain.
5. **Goal fit.** The board's top scaling risk and the queued build `b-coorbital-cert`: a
   tier that silently drops 90%+ of contacts at the motivating scale (10⁶) corrupts every
   downstream encounter certificate — "errors never compound" (principle 13) is exactly
   what is protected. The gate is a dimensionless number (principle 4), kills the ungated
   configuration rather than the method (principle 9), and the 10⁶ extrapolation is integer
   rank arithmetic (2π·4/10⁶ = 2.51e-5 rad, verified), not float extrapolation (principle
   24). Adoptable within one step; no new component.

The one blemish (k = 8) demotes a side-formula, not the claim, and errs safe. Every
load-bearing element was reproduced and survived four independent adversarial axes, two of
which the author never measured.

**What the author missed.**

- The registered held-out k-formula fails at k = 8 by 23 pp (over-predicts); the author
  saw the same bias at k = 4 (72 vs 83%) and still registered the uncorrected form.
- The scattered-regime brute evidence was vacuous by construction (contacts are ~0.3% of
  pairs; 150–200 random pairs almost surely contain none) — only the directed attack
  actually tests the truth finder where the certificate breaks.
- `contact_pairs` counts (i, j) and (j, i) tuples separately once λ-order swaps between
  grid times (143 tuples vs 75 unordered pairs at D = 0.5): cosmetic inflation, and miss
  fractions are unbiased because the rank gap is symmetric — but "pairs" in the tables is
  not a body-pair count in the scattered cases.
- `phase_density_per_rad` is computed analytically as N/2π, so its blindness is by
  definition; only the dn_rel blindness is measured. The gate should rest on the Binet
  extent (measured, monotone), which the dossier correctly picks.
- The wide-belt λ-miss came in at 50% against the predicted ≈ 97% (predictions table) and
  is not listed among the reported misses; immaterial (the tier is invalid there by both
  keys) but unreported.
- The gold's σ_e = 3×10⁻⁴ is quoted from a run folder absent from this checkout; not
  independently verifiable here (the board's statement of the gold's claim matches the
  aligned control, so the control is not a strawman).
