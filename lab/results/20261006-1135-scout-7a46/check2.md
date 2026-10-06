# check2.md — 20261006-1135-scout-7a46 (second checker, blind to check.md)

Grade: gold

**Abstract for the integrator.** Claim: a Levi-Civita drift (`z=u²`, `dt=|u|²dτ`, `u''=(E/2)u`) serves the conic representation's singular set (L=0, plunge, near-radial — the live `NoBoundOrbit` freeze) exactly, at K kicks per encounter independent of depth. Reproduced bit-for-bit (all 14 rows, calibration, locked constants; 8 s, <50 MB). My eight adversarial cases (retrograde, 2 v_H, q=0.001 r_H and q=1e-5 r_H, near-parabolic, hits at two speeds, α-sweeps) all support it: no-tide LC error 6e-9…1e-12 at every depth; with-tide error flat (2.0e-3/5.1e-4 at K=8/16) from q=0.1 to q=0.001; A-rt on the L=0 set is non-monotone (err 187 at α=0.2, step-caps at α=0.05/0.0125, err 0.1 at 12,700 evals). It kills the opus-math memo's line-291 rejection of LC-as-drift (its reasons cover only the bound branch) and fills the certified bank's unsupplied list. Adoption: one additive unbound/radial drift branch in the doll, reusing v2 kicks.

## Reproduction

- Copied `falsifier.py` to a clean temp dir (author's folder untouched; `work/patch.diff` is empty — no tree edits). `python3 falsifier.py` → `results.json` identical to the stored one: `calibration` equal, `locked` equal, 14/14 rows, 0 diffs. The 5-October failure mode (numbers the shipped code cannot regenerate) does not apply.
- Engine citations real: `certified_bank.rs` "not supplied by the law… radial paths (L = 0), plunge and horizon times, outgoing escapes with no turning point"; `binding.rs` refuses on `vt.is_zero()` and non-positive discriminant. HANDOFF 24: "plunge and radial orbits have no tube"; HANDOFF 25: Julien's actual freeze ("near-radial fall… kicks refuse with `NoBoundOrbit` and the state freezes"). The bottleneck is real and live.
- Order of work: `predictions.md` 11:51:46, grid `results.json` 12:07:09 (script last touched 12:07:03, 8-second run). Predictions preceded the decisive grid by 15 min; the addendum's amendments are timestamped before it and disclosed.

## Predictions

Held: (1) no-tide control ≤ 1e-12 (3.5e-16…7.4e-12; and mine below); (3) A-rt error growth 70×; (4) cost-to-match 18–93×; (5) C through r=0 at ~1e-15 with zero force evals, A-rt err ~190. Boundary misses (K8 3.04× vs "~3×"; exponent −0.36 vs amended [−1,−0.4]) are reported by the author against his own pre-registered numbers. The original prediction 5 (A-rt stalls) was amended pre-grid and still turned out wrong in an informative direction — disclosed.

## My adversarial cases (beyond the grid)

1. **Retrograde flyby** (tide geometry reversed, q=0.03 r_H): C_K8 2.2e-3, no-tide 9.6e-13. Unchanged.
2. **Fast flyby, v∞ = 2 v_H**: C_K8 2.2e-3, no-tide 8.1e-13. Unchanged.
3. **q = 0.001 r_H** (below the grid's deepest): C_K8 2.0e-3, C_K16 5.06e-4 — identical to q=0.003; A needs ~1,400 evals (≈90×). Flat in depth, extended one decade.
4. **q = 1e-5 r_H** (1,000× deeper): no-tide 6.0e-9 — LC degrades gracefully at absurd depth; A hopeless there by the grid's trend.
5. **Near-parabolic, v∞ = 0.05 v_H** (longest residence, t=0.177): C_K8 1.6e-3, same as the grid row. Residence alone does not hurt at K=8.
6. **Hit at v∞ = 0.7 v_H**: A terminates here (unlike v0.3, which caps — the dossier's "never terminates" is v0.3-specific) but needs ≥1,394 evals vs 8 kicks (~90×).
7. **Thru (L=0) α-sweep**: A-rt err 187 (α=0.2) → **step-cap** at α=0.05 and 0.0125 → err 0.109 only at α=0.003 (12,700 evals, 67× smaller α). A is not merely slow there; it is unreliable (non-monotone in α).
8. Truth quality spot-checked at rtol 1e-14: agreement 1e-13…1.5e-10, always below C's with-tide errors.

## Novelty

Classical mechanism (Bohlin 1911/Levi-Civita 1920), and the author says so. What is new and measured: the repo's own `opus-math` memo (line 291) explicitly rejected LC-as-drift ("fictitious time must be mapped back by Kepler's equation anyway, which R1 already gives" / "the planet's doll is already the regularized frame"); this run shows both reasons cover only the bound branch and the origin — not the conic's discriminant — and that the residue is exactly the certified bank's unsupplied list. No HISTORY entry or prior run tests LC as the unbound/radial drift; `docs/HISTORY.md` has only an unrelated `acosh` quadrature regularization. Prior-art mentions of LC are in `docs/reference/` conversations only.

## Goal fit

Fills the motion-law v2 completeness hole that froze Julien's ship; on that set the gain is unbounded (refusal → served), 18–93× at matched error elsewhere, and it deletes the stepping fallback there. PRINCIPLES: "if you find yourself fixing things that's oftentimes a signal that it is the wrong representation" (#19 — the refusals were the signal); "compute only surprises" (#3 — zero events between tide kicks); "errors never compound" (#13 — drift exact at any depth; error only in second-order kicks).

## What the author missed

- **Event ≠ flop.** One C "event" is a closed-form segment plus kick (the script's own counter charges ~200 arithmetic ops per segment) against ~30 flops for a Verlet step; at q=0.3 the 18× event ratio is near wall-clock parity. The absolute win is at depth and on the singular set, and in the integer design the segment is meant to be table lookups (designed, not measured). State this when quoting 18–93×.
- **The ratio is one-sided.** Matching the other way (C's kicks to reach A's α=0.2 error) gives ~5× at q=0.3; double-digit ratios survive only at depth. Direction robust, convention-dependent magnitude.
- **">62,500×" is extrapolated** from calibration err∝α² scaling. My sweep bounds it at >10⁴× with non-monotone A behavior; the honest phrasing is "no α in any sweep works reliably; >10⁴×".
- **Captures:** `lc_run`'s pre-pass needs a drift-only exit, so bound residents return None — C as shipped refuses captures too, for window reasons, not only tide-smoothness. Disclosed as untested but worth naming as a second refusal.
- The control is one step-rule family (dt=min(cap, αr), fixed dt); a geometry-aware cheap rule (α from q or L) is untested — though on L=0 no r-based rule can help, which is the point.
- Newtonian only; the strong-field ψ form is a pointer to Astra's machinery, unmeasured.

None of these overturn the claim as scoped. Reproduced, predictions held, a premise (the memo's LC rejection on the unbound branch) shown wrong, and the fill for a live freeze adoptable in one additive step: gold.
