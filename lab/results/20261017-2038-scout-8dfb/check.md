Grade: silver

**Abstract.** Claim: the doll inventory's one named hole (inclined Kerr, `kerr.rs`
equatorial-only, "nothing tests it") has a complete float candidate — every bound
inclined Kerr orbit compiles to a two-frequency Mino-time torus whose six
per-(E, L_z, Q) constants close in the shipped Carlson kernel family (Π = RF+(n/3)RJ
verified 2e-16), agreeing with 30-dps quadrature to ≤ 3.7e-12 (120/120; a to 0.998,
e to 0.9, retro, near-separatrix). Reproduced: regen.sh bit-for-bit. Checker added an
independent raw-metric Hamiltonian arm (no Carter separation): periods ~1e-12,
separated integrands pointwise equal to the metric at ~5e-16, mean torus rates ≤ 2e-3,
Lense–Thirning sign/magnitude/inclination-independence at p=30, and it holds on
outside-range rows (a=0.998 with e=0.9; near-polar 5°). Cost to adopt: unpriced —
float-only, dt_r still uses an mpmath derivative, no gate. Silver: port and price it.

## Reasons

**1. Reproduction (clean).** I reran `regen.sh` in the delivered tree: output
bit-identical to `run-output.txt` except the machine-dependent timing line. 120/120
CF-vs-QD comparisons, worst 3.67e-12 (the e=0.9 row's dPhi_r). Π = RF+(n/3)RJ
re-verified against mpmath.ellippi at 1.95e-16 including negative n. Summary script's
own numbers match the dossier.

**2. Predictions.** Timing is consistent with pre-registration (predictions.md 20:45;
falsifier.py last edit 21:06; decisive run ~21:08; dossier 21:12). P1 (RK ≤ 1e-8)
missed and honestly reported — the RK4-with-turning-restarts arm's own resolution is
1e-4-class. **P2 is generously worded**: the registered bound was ≤ 1e-13 (tightened
to "≤ 1e-12, flagged if > 1e-9") and the result is 3.7e-12 — fine at the flag level,
but "held" is not the honest word for a 4× miss of the stated number; the cause
(float64 assembly of the Möbius/partial-fraction algebra) is disclosed and benign.
P4's Λ_θ clause was wrong and the author diagnosed why (finite harmonic limit,
measured exactly). P5 (10 µs) not demonstrated — disclosed. Held-out rows (a=0.998,
e=0.9, retro, p=6.8) all behaved as the in-grid rows.

**3. Attacks (four, one beyond the author's range).**
- **Independent formulation.** The author's three arms are not independent where it
  matters: the RK arm integrates the *same separated potentials* R and P4 as QD and
  CF, so a formulation error (wrong potential, wrong accumulator) was invisible to
  all three. I integrated the raw Kerr Hamiltonian in Boyer–Lindquist coordinates
  (sympy-derived, DOP853 rtol 1e-12, H conserved ≤ 1e-12, start-point H+1/2 = 0
  validating (E, L_z, Q) against the metric): Λ_r, Λ_θ match to ~1e-12 on every row
  — 8 orders better than the author's RK; the separated integrands
  dphi_r+dphi_u and dt_r+dt_u equal the metric's dφ/dλ, dt/dλ **pointwise to ~5e-16**
  on a (r,u) grid; the torus mean rates Ω_φ = ΔΦ_r/Λ_r + ΔΦ_θ/Λ_θ and Ω_t agree to
  3e-5…2e-3 (finite-window truncation class, not a discrepancy — a wrong split or
  potential gives O(1)). The formulation now stands confirmed by a path sharing no
  code or algebra with the instrument.
- **Outside range.** a=0.998 with e=0.9 at p=8 (combining the author's extremes,
  never run together) and a near-polar θ_turn = 5° (author swept 30°–150°): same
  1e-12/5e-16 agreement. The claim's domain is larger than shown.
- **External physics anchor.** At p=30, a=0.2 my Hamiltonian-measured nodal
  regression is −1.69e-2/orbit vs leading-order Lense–Thirring −4πa/p^1.5 = −1.53e-2
  (ratio 1.10, consistent with 1PN corrections at p=30), inclination-independent to
  1% (θ 45° vs 75°: 1.105 vs 1.094) — sign and magnitude of the frame-dragging
  readout anchored to textbook knowledge, guarding my own instrument in turn.
- **Root-case census.** 60 low-a/high-e/near-margin probes: the case `4real/0below`
  exists (5 rows, e.g. a=0.1–0.3, p=6.5–6.8, e ≥ 0.5) and there `cf_arm` **silently
  returns NaN** for the radial constants — it does not assert, contrary to the
  dossier's "this instrument asserts rather than handles them". None of the 21
  reported rows is affected (all 4real/2below), and the dossier discloses that other
  root cases are unhandled, but the wording is wrong.

**4. Novelty.** `crates/space/src/kerr.rs` line 1: "Equatorial Kerr". The handoff wiki
page's open direction 8: "Inclined Kerr — the one named hole in the doll inventory;
nothing tests it". No Mino/Fujita/Carter hit anywhere in docs/ or lab/wiki/. Known to
science (Fujita–Hikida 2009, Schmidt 2002, Drasco–Hughes 2003 — cited), lab-new, and
the derivation is asserted in-instrument rather than transcribed; my independent arm
corroborates the physics.

**5. The page.** The proposed `wiki/handoff.md` fold was checked line by line against
`run-output.txt` (120 comparisons, 3.7e-12, 7.7e-5, 4.9e-10, 1e-11 degeneration,
Λ_θ = 2π/√B, the named port edges): faithful; no correction needed.

**6. Goal fit.** PRINCIPLES #18 ("the right representation so that the math is
trivial": one more invariant, one more clock — the same object as the shipped
Schwarzschild doll), #32 (the separation symmetry appears only in Mino time), #26
(the LISA community industrialised exactly this decomposition). Not a focus-list
bottleneck and the author says so; it fills the scoreboard's GR-completeness row and
unblocks the handoff page's direction 8.

## Why silver, not gold

Real, reproduced, novel to the lab, and the formulation now independently confirmed —
but it deletes a *candidate assumption* ("inclined strong-field orbits need a new
mechanism") at float level only, and the engine cannot adopt it within one step as it
stands: the integer port is unpriced, dt_r still depends on a 40-dps mpmath derivative
(no float ∂ₙΠ recurrence), there is no gate or freeze design, and P5's cost claim was
never measured even by kernel count in code. Two prediction-reporting warts (P1's
magnitude, P2's "held") are disclosed but keep the run below the "held-out
predictions held" gold bar.

**The one experiment:** port all six constants to pure float Carlson kernels (the
∂ₙΠ recurrence; it becomes a fixed, countable kernel set), count the kernels, price
the six-constant readout against the plane's shipped read class on the cd6e/de99
numbers, and write the B19-shaped freeze for Q ≠ 0 (cycles, advances incl. nodal,
fates, Lense–Thirning rate as the weak-field control). That closes P5, makes the
adoption cost a number the integrator can rule on, and is one step.

## What the author missed

- The RK arm is not an independent formulation (same separated potentials): the
  "independent third arm" phrasing overstated the evidence; only an external-form
  check (this one) could catch a potential/accumulator error.
- P2 "held" despite exceeding its registered bound ~4×.
- The 4real/0below root case silently NaNs; "asserts" is wrong, and its prevalence
  (low a, high e, near-margin p) was not measured.
- The timing claim stayed a kernel-count argument never counted in the code.
