Grade: gold

**Abstract.** Claim: scout-8dfb's named experiment is done — all six inclined-Kerr
constants port to pure float Carlson kernels: 8 distinct kernels per (E, L_z, Q) key
(2RF+2RD+4RJ = 0.86 µs at de99's ns; raw 28 = 2.40 µs), the J = Π+n∂ₙΠ closed form
verified 1.9e-15, port ≤ 4.4e-14 vs the original arm, ≤ 3.67e-12 vs quadrature (same
worst row), the root case measured as a spurious solve (3.7%, refuses loudly), LT
0.975–0.986×, B19Q freeze written. Reproduced bit-for-bit; my independent 50-dps arm
gives 2.7e-13 worst over ten rows, five outside range (a=0.9999, e=0.95, θ=5°/175°,
extremes combined); J identity 1.6e-13 in exact arithmetic; kernel count holds outside
range. One correction: the census confinement leaks at a=0.45, fixed on the page. Cost
to adopt: one build step beside the equatorial compiler.

## Reasons

**1. Reproduction (clean).** Reran `regen.sh`: exit 0, output bit-identical to
`regen.log` except the machine timing line (257.93 vs 264 µs/key — disclosed as
order-of-magnitude only). Every dossier number matches the log: worst |PURE−ORIG|
4.38e-14; worst |PURE−QD| 3.67e-12 at the same worst row as the original record
(e=0.9 th45, dPhi_r); selftest {K 1.5e-16, E 8.4e-16, Π 3.3e-16, J 1.9e-15}; raw
16×RF+3×RD+9×RJ = 28 = 2.40 µs and memoized 2/2/4 = 8 = 0.86 µs (arithmetic checks:
800+234+1368 ns, 100+156+608 ns); census 630 rows = 527/80/23 with all 23 rows
carrying exactly one in-band root and sign(R(rp+ε)) = −1; max Λ_r 7.262; LT ratios
0.981/0.975/0.986. `orig-falsifier.py` is byte-identical to
`origin/claude/lab-20261017-2038-scout-8dfb`'s `falsifier.py` (git diff empty), so
the fidelity arm is the shipped record's code, as claimed.

**2. Predictions.** `predictions.md` predates the decisive run (file-time order;
content covers the end-to-end instrument, with the J derivation's pre-verification
disclosed). P1/P2/P3/P6 held; P4 partially missed (raw 28 vs the predicted 10–16)
and reported as a miss; P5's prevalence held and its mechanism clause (m→1 blow-up)
was refuted by its own measurement and reported as refuted — pre-registration doing
its job, the opposite of the first run's P2 "held" wart. Honest reporting throughout.

**3. Attacks (six, several beyond the author's range).**
- *Independent 50-dps quadrature* — my own code, own nodes, own Newton-polished
  (E, L_z, Q) solve (the solve equations were already validated against the raw
  Hamiltonian by the first checker): worst |PURE − mine| = **2.7e-13 over 10 rows**
  — 10× tighter than the record's own 30-dps bound. The record's 3.67e-12 is its
  quadrature's precision, not the port's error; the port is more faithful than
  claimed.
- *Outside range (5 rows)*: a=0.998 with e=0.9 AND θ=85 combined (never together in
  any grid), a=0.9999 (beyond 0.998), θ=5° near-polar, e=0.95 (beyond 0.9), retro
  θ=175° — all ≤ 2.7e-13; the memoized 8-kernel count holds on every one. The
  claim's domain is larger than shown.
- *J identity in exact arithmetic* (50 dps, my own quadrature) on 13 adversarial
  (n, m) — n<0, n>m, n→1⁻, m→1, m→0, n=−50, near-degenerate m≈n: worst 1.55e-13
  (n=0.999/m=0.998); the m=0 limit reduces analytically to the textbook
  π(2−n)/(4(1−n)^{3/2}). The closed form is correct as mathematics, well beyond the
  selftest grid.
- *Refusal entered, not just counted*: a=0.2/p=6.5/e=0.5/θ=30 makes the port raise
  RuntimeError with roots and case — never a silent NaN.
- *LT beyond p=30* (the author tested only p=30): ratios 0.962–0.993 at p=60/120/200
  and a∈{0.1, 0.4}, all inside the freeze band [0.95, 1.15] and converging
  monotonically to 1 with p. The port's readout convention is self-consistent; the
  0.98-vs-1.10 offset against the Hamiltonian arm behaves as a fixed convention gap,
  exactly the open edge the dossier names.
- *Census confinement attacked at the bracket*: **a=0.45, p=6.5, e=0.9, θ=30 is in
  the 4real/1below class** (in-band root, R(rp+ε) < 0) — outside the stated
  "a ≤ 0.3 ∧ e ≥ 0.5 ∧ p ≤ 7.5" confinement. The census grid never sampled
  0.3 < a < 0.6; the bracket is a grid artifact, not a boundary. The dossier's
  "only bracketed" hedge is right in spirit but the stated bracket is not an upper
  bound. Corrected on the page. The operative refusal criterion (root-case-driven,
  parameter-independent) is unaffected.

**4. Novelty.** The handoff page's direction 8 and the first checker's named
experiment define this work; nothing in docs/HISTORY.md. Prior art inside the lab:
cd6e (kick-jet page) closed the *incomplete equatorial* squared-pole integrand by
Hermite reduction and priced kernels — this run's J is the *complete-integral* form
assembled from complete K/E/Π, the case the inclined compile needs, and the named
experiment explicitly requested the ∂ₙΠ recurrence. Not a repetition; cross-link
added to the page. de99's kernel prices (rf 50/rd 78/rj 152 ns) confirmed verbatim
from the kick-jet page.

**5. The page.** Every number in the fold matches regen.log (checked line by line).
Two corrections applied in place: the confinement bracket (above) and the cd6e
cross-reference on the J closure.

**6. Goal fit.** Fills the scoreboard's GR-completeness row and the handoff page's
direction 8; deletes the last non-float dependency (the 40-dps mpmath ∂ₙΠ) and kills
the "missing reduction" premise by measurement. PRINCIPLES #18 "we just need to have
the right representation so that math is trivial" (one kernel family, one closed
form); #1/#17 "the cheapest compute is compute not done" (8 kernels per key, zero
per read); #10 "measure before claiming" (P5's mechanism measured wrong and reported
wrong). Not a focus-list bottleneck, and the dossier says so honestly.

**Why gold.** Reproduced bit-for-bit; independently confirmed tighter than claimed;
predictions pre-registered with honest misses; every named deliverable of the
previous checker's "one experiment" landed (pure-float port, counted and priced
kernels, refusal criterion measured, B19-shaped freeze written); it deletes a
component and corrects a premise, and the adoption cost is now a number the
integrator can rule on (0.86 µs/key against the 4.4 µs shipped belt compile and the
~6 µs rebind floor). Adoptable within one step at float level, with the integer port
named as the build's step.

## What the author missed

- The census's a-grid gap (0.3–0.6) let a grid property read as a boundary; one
  denser a-sweep would have caught a=0.45.
- The freeze's criterion 5 (a = 0 degeneration) is currently unsatisfiable by the
  port itself: at a = 0 the polar constants come out NaN in both arms (the port
  requires a ≠ 0 for the polar branch), while the criterion expects the harmonic
  limit Λ_θ → 2π/√(Q+L_z²+a²(1−E²)). The gate would catch it; the port cannot yet
  express that row.
- `fsolve` fragility beyond the run's grids: my sweep hits 101/270 solve failures at
  p up to 120 (weak field, where the Kepler seed degrades). The (E, L_z, Q) solver,
  not the port, is the adoption's fragile edge; the freeze's refusal class covers
  it, but the build should ship the high-precision polish, not fsolve.
- The 0.86 µs counts Carlson kernels only; the float assembly around them (Möbius
  algebra, 3×3 solve, Newton) is untimed natively — disclosed, but the freeze's
  cost criterion inherits "assembly is free".
- Minor: "e-flat 1.1%" is the worst-corner spread of three sampled points; the
  clean e-comparison at θ=45° is 0.4%. Conservative direction; no claim rests on it.
