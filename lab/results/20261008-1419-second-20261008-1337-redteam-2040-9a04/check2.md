Grade: gold

**Abstract.** Second author completes the checker's named experiment: the §3 multiply-add
kick fails by type on the E axis too (relerr(T_t) ≈ C·(dE/(1−E))², C 1.85→1.66, slope
1.979, 1.2×10⁸ stiffer than the matched dL kick) and on the escape side (fabricated
cycles; the original `is_bound` wrong there), and the exact tri-predicate agrees with
grid truth 3600/3600 and 11/11 integrated orbits. All three commands regenerate every
output bit-for-bit (22 s, 1.3 s, 10 s; ≤ 67 MB). Adoption: one exact predicate per kick
at the edges, per-axis certificate widths, recompile deleted elsewhere; the
`b-plunge-tubes` criterion is freeze-ready. Two peripheral constants need correcting
(tilt 9.06, not 18; RK4 T_t first-order, not 4th) — not load-bearing.

**Reasons.**

1. **Reproduction, clean and exact.** `work/patch.diff` is empty (no tree edits). All
   three commands rerun: `falsifier.py` 21.9 s / 34 MB, `falsifier2.py` 1.3 s / 38 MB,
   `validate_oracle.py` 10.2 s / 67 MB. Every output is byte-identical to the stored
   JSONs, and `falsifier-out.json` is byte-identical to the original run's published
   branch output (`origin/claude/lab-20261008-1337-redteam-2040`) — the "original record
   reproduces bit-for-bit" claim is verified against the branch, not just the local copy.

2. **Held-out predictions.** File times order correctly: `predictions.md` 14:34:38 →
   falsifier2 run 14:35:00 → validate run 14:36:59 → dossier 14:38:58. The two mid-run
   script fixes are disclosed and precede any output. All twelve items hold on my rerun:
   E2 = 2.56×10⁻⁵ ∈ [10⁻⁶, 2×10⁻⁴]; slope 1.979 ∈ 2.0 ± 0.1; 1% band break at f ≈ 0.075
   ∈ [0.04, 0.12]; scale-free ratios 1.00–1.01; E6b plunge-not-escape (the genuinely blind
   physics call); V3 zero disagreements with 60/3660 = 1.6% margin-excluded; V4 11/11.

3. **My attacks confirm rather than break.**
   - Twenty predicate-vs-integration cases outside the V3 sweep box (E ∈ {0.5, 0.945,
     0.95, √(8/9), 0.99, 0.9999, 0.999999, 1.0001, 1.2, 2.0}; near-ISCO and near-L_crit
     at three energies; past the circular edge; an orbit with apocentre at the grid
     cap): **20/20** classify3 = integrated behaviour. The predicate also survives where
     the author's own grid truth reaches its limit.
   - Off-scan points of the f² law (f = 0.05, 0.15, 0.20): C = 1.82, 1.76, 1.73 — inside
     the claimed drift band; the law interpolates, it is not a fit artifact.
   - Second scale-free halving (peri 200 / apo 800): err ratios 1.008–1.009 at every f.
   - The 15/8 Newtonian limit is right for the raw-linear model (½(T″/T)dE² with
     T ∝ (1−E²)^(−3/2) gives g′² + g″ = 3.75/(1−E)²); finite differences of the exact
     map give C = 1.852 at the E1 seed. L_crit(1.005) = 4.0397 by the unstable-circular
     curve (author: 4.037; E6b/E6c margins unaffected). The two separatrix solvers
     (bisection, curve) agree to 15 digits.

4. **Two stated numbers are wrong; neither is load-bearing.** (a) dL_sep/dE at E = 0.97
   is **9.06**, not ≈ 18 (central, one-sided and curve derivatives agree); the dossier's
   "the physics anchors … all measured out" is false for this one — no measurement of it
   exists in the run. E5's plunge truth never uses the tilt; it is directly integrated.
   (b) V1's "Richardson step consistent with 4th order": the RK4-Binet T_t path
   converges at exactly **order 1** (error = A/n; the Richardson difference equals the
   400k error, the order-1 signature), and Δφ sits on a roundoff floor that grows with
   n. The oracle conclusion stands regardless — DOP853 cross-checks the quadrature to
   ~10⁻¹³, which is the tighter anchor. Also a transcription slip: advance 0.25008, not
   0.25013. These must be corrected before the criterion freezes; they change no
   measured result and no part of the adoption.

5. **Novelty.** Nothing in HISTORY or the docs covers kick response on the E axis, the
   escape side, or the predicate's completeness; H0183's `bound_period_quad` is the
   oracle family, here independently validated for the first time (the original's
   "2×10⁻⁴" was not regenerable). The tri-predicate itself is textbook Schwarzschild
   root-structure classification; the contribution is the measured per-axis certificate
   widths, the completeness evidence (grid + integration, both sides), and the
   freeze-ready criterion for `b-plunge-tubes` (queued in `lab/queue.txt`; the plane's
   `NoBoundOrbit` limit is live in HANDOFF).

6. **Fit.** Principle 2 ("error type over error size"), 13 ("errors never compound") and
   19 ("a fix signals the wrong representation") apply as quoted. The premise falsified
   is §3's single per-cycle certificate: widths are per-axis and the derivatives diverge
   at both boundaries. What is deleted: the per-kick recompile outside the measured
   window, and the plane's crash-path refusal replaced by an exact, integer-decidable
   classification (one cubic sign test per kick). Adoptable within one step.

**What the author missed.** The coupled E–L regime near the separatrix (an E kick acts
on δ_L through the tilt) was named in the lens section but never scanned; the
derivatives tested are ideal floats, not the shipped integer store; no moving lens
(B16) interaction. `L_sep_of`'s 0.25-spaced L grid silently returns None when the bound
window is narrower (E ≲ 0.955), so near-separatrix seeds only exist for E ≥ 0.97, and
V3's rows below E = 0.9428 are trivially plunge (no bound region exists below ISCO
energy) — the sweep's E range overstates its coverage. The ∂T_t/∂E headroom near E → 1
is asserted from (1−E²)^(−5/2) but never fitted as a storable width, which is what the
integer store freeze will need.
