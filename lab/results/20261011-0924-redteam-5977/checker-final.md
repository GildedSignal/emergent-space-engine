Working...
**Grade: gold** — written to `lab/results/20261011-0924-redteam-5977/check.md`.

What I did, and what held:

**Reproduce.** `falsifier.py` regenerates `falsifier-results.json` byte-identical (9.4 s, 64 MB). No patch to apply.

**Independent re-derivation, different method.** Rebuilt both attacks from scratch — first-order radial quadrature on conserved (E, L) with turning-point branches (vs the author's Binet IVP in φ) for the photon side; first-integral/closed-form quadrature for apsidal advance. All 26 delay rows and all 13 apsidal rows agree to ≤ 2e-7. The headline (Δt = 3.14→7.31M, 4.3–10.1° phase error; B11's band 2–4× the exact-vs-1PN gap) is real.

**Adversarial.** Φ=3.0 past the sweep: Δt = 9.15M, 12.6° — the reported range is a *lower bound* toward conjunction. Keyed the memo on the true b instead of the chord's b_flat: still ~50° error where the real bend is 0.09° — the finite-path attack survives its strongest objection. The dropped p=12 eccentric rows genuinely plunge (p < 3(1+e)²/e), so no cherry-picking.

**Letter and guards.** law.md:53 verbatim confirms the flat-cone + direction-only-memo reading; B3/B7/B16 judge deflection and clock rates, nothing judges arrival time; Shapiro exists only in the oracle (H0183, which makes the fix cheap); r5/r6 absent from `lab/rungs/` — and r6 as frozen in §7 judges *cost only*, so even building it wouldn't catch this. B11's allowance `(1% + 2·8/p)` quoted correctly. Predictions predate the final run by 13 min (mtimes), with honest partials (P2 half-held, P4 missed p=25 and says so).

**Why gold, not silver:** premise shown wrong on the surface PRINCIPLES 30 requires perfect, double-verified physics, adoptable in one step (delay(b) memo column + one criterion + one paragraph killing representation.md §1's dead Minsky premise).

**What the author missed** (in check.md): the delay column must also enter the moving-lens memo (β-dependent, B16's original sin one rung later); the worst regime (b → b_crit, diverging delay, extra crossings) lies beyond the 2.7 stop; AI perception inherits the error; r6's frozen letter itself must change; and one rounding slip (far control max is 0.0128°, not ≤ 0.011° — bound still holds 4×).
