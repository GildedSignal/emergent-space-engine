# dossier — 20261017-2142-second-20261017-2038-scout-8dfb-e1a4 (second author)

## Claim

The checker's named experiment for scout-8dfb is done: all six inclined-Kerr
constants now port to **pure float Carlson kernels** — the ∂ₙΠ hole is closed
by a machine-derived closed form (J = Π + n∂ₙΠ = [Π(2mn−3m−n²+2n) +
K(m−n) + nE]/(2(n−1)(m−n)), sympy partial fraction of the total-derivative
identity, held to 1.9e-15 vs 40-dps quadrature) — the port changes nothing in
the answer (**≤ 4.4e-14 vs the original arm, ≤ 3.67e-12 vs 30-dps quadrature
on all 21 rows + held-out, the same worst row as the original**), the kernel
set is counted and priced (**8 distinct kernels per key = 0.86 µs at de99's
measured rf 50 / rd 78 / rj 152 ns**; raw unshared 28 = 2.40 µs), the
"4real/0below" root case is measured and is **not a missing reduction but a
spurious (E, L_z, Q) solve** (3.7% of a 630-row sweep, every instance an
extra quartic root inside the intended band with R(rp+ε) < 0 — refuse loudly
upstream), the weak-field Lense–Thirring control holds on the port itself
(|Ω_φ−Ω_θ| = 0.975–0.986 × 4πa/p^{3/2} at p = 30, inclination-flat 0.6%,
e-flat 1.1%), and the B19-shaped freeze for Q ≠ 0 is written
([freeze-b19q.md](freeze-b19q.md)).

## Bottleneck

Not a 10⁹-ladder item: the GR-completeness row and handoff direction 8. What
this deletes: the last reason inclined Kerr could be called "not adoptable
within one step" — the port's cost is now a number the integrator can rule on
(0.86 µs/key against the shipped belt compile 4.4 µs, the plane mix 5–256 µs
p50 76, and the a765 rebind floor ~6 µs), and the adoption's edges are named
(refusal criterion, freeze criteria) instead of open.

## Evidence (`python3 port.py`, ~10 s; `regen.sh` wraps it)

Baseline verbatim: the original run's instrument is imported by path
(`orig-falsifier.py`, unmodified from
`origin/claude/lab-20261017-2038-scout-8dfb`) — the fidelity arm IS the
shipped record's code. Per row (21-row grid + controls + 4 held-out): QD
(30-dps quadrature), ORIG (the original arm, ellipk/ellipe + 40-dps mpmath
∂ₙΠ), PURE (this port; every elliptic element a counted
RF/RD/RJ call; no mpmath anywhere on the closed-form path).

1. **Port fidelity**: worst |PURE − ORIG| = **4.4e-14** over 21×6 constants
   (predicted ≤ 5e-13). The port is the same answer.
2. **Exactness preserved**: worst |PURE − QD| = **3.67e-12** — the same worst
   value and same row (e = 0.9, ΔΦ_r) as the original record. The J closed
   form's 1/(2(n−1)(m−n)) assembly adds no visible residue.
3. **Kernel identity**: K = RF; E = RF − (m/3)RD; Π = RF + (n/3)RJ; J via the
   closed form — selftest vs 40-dps mpmath worst {K 1.5e-16, E 8.4e-16,
   Π 3.3e-16, J 1.9e-15}.
4. **Kernel count and price**: raw per key 16×RF + 3×RD + 9×RJ = 28 calls =
   2.40 µs; memoized distinct per key (worst key) **2×RF + 2×RD + 4×RJ = 8 =
   0.86 µs**. Per-frame reads carry zero kernels (compile once per
   (E, L_z, Q); the read is arithmetic + the amplitude Newton — the freeze
   prices the read class by the shipped ~4 µs lean anchor).
5. **Root-case census** (630 rows: a ∈ {0.1…0.998} × p ∈ {6.5…20} × e ∈
   {0.1…0.9} × θ ∈ {30°,60°,85°}): 83.7% clean 4real/2below, 12.7% refused
   at solve (no convergence — plunge region), **3.7% (23 rows) the
   "0below/1below" class, and every one of them has exactly one extra quartic
   root strictly inside the intended band with sign(R(rp+ε)) = −1** — the
   (p, e, θ) key has no adjacent-turning-point bound orbit there; fsolve
   satisfied the two turning-point equations on non-adjacent roots. All 23
   sit at a ≤ 0.3 ∧ e ≥ 0.5 ∧ p ≤ 7.5. The correct fix is a band-integrity
   assert in the solve (refuse), not a new algebra case; max Λ_r over handled
   rows is 7.26 (no blow-up — the m→1 separatrix edge is not what these
   rows are). The port raises loudly (RuntimeError with roots and case) where
   the original returned silent NaN.
6. **Lense–Thirring control on the port** (p = 30, a = 0.2):
   |Ω_φ − Ω_θ| per azimuthal revolution = 1.4915e-2…1.5076e-2 vs
   4πa/p^{3/2} = 1.5295e-2 → ratio 0.975–0.986, flat in θ (45° vs 75°:
   0.6%) and e (0.1 vs 0.3: 1.1%). The checker's independent Hamiltonian arm
   put it at 1.10; both inside the 1PN-at-p=30 band. My first readout
   formula ((ΔΦ_θ−2π)·Λ_r/Λ_θ, the polar-channel deviation) was wrong by
   15.6× and is recorded as wrong: it measures inclination geometry, not
   node regression; the frequency readout is the correct one.
7. **Timing (instrument only)**: 264 µs/key in Python (np.roots + 3×3
   solves dominate); the native number is the kernel price above. Disclosed,
   not part of the claim.


- P1 (J ≤ 2e-14): **held** (1.9e-15).
- P2 (fidelity ≤ 5e-13): **held** (4.4e-14).
- P3 (exactness ≤ 1e-11): **held** (3.67e-12).
- P4 (10–16 kernels, 1.0–2.5 µs): **partially missed**. Raw count 28 (the
  port recomputes K/E/Π inside Jc and re-evaluates Π(nh) in dt_r) — outside
  the kernel range; the price bracket held on the raw side (2.40 µs) and the
  memoized side landed BELOW my range (8 kernels, 0.86 µs — I over-predicted
  the pole Π's as distinct; dt_r's poles share n₀ with ΔΦ_r's).
- P5 (< 5% prevalence, near-separatrix low-spin high-e confinement):
  prevalence **held** (3.7%), confinement **held** (a ≤ 0.3, e ≥ 0.5,
  p ≤ 7.5); the mechanism clause (m→1 blow-up, sub-1e-4 gap) **refuted by the
  measurement** — it is an in-band root from a spurious solve, gaps O(1),
  Λ_r nowhere near blow-up. Pre-registration doing its job.
- P6 (read class arithmetic-only; compile at/below the ~6 µs floor):
  **held and stronger** — 0.86 µs/key memoized, 2.40 µs raw.

Disclosed: the J identity was machine-derived and standalone-grid-verified
(8e-15 at 40 dps) before predictions.md was written; predictions cover the
end-to-end instrument, which had not been run.

## What would make it wrong

The port inherits the original's float-only status: the **integer port** (Q's
word width, exact integer advances) remains unpriced and is where rounding
choices live; **resonant tori** make coordinate-time readout inversion
ill-conditioned (Mino-time torus exact — freeze excludes it deliberately);
the census covers a grid, not the parameter continuum (the 3.7% class's exact
boundary in (a, p, e, θ) is not mapped, only bracketed); the LT control's
deviation from the checker's Hamiltonian value (0.98 vs 1.10 × LT) is
unresolved — both are "≈1PN at p = 30" but are not the same number, and
nailing which readout convention reconciles them is an open edge named in the
freeze; nothing here touches a doll boundary, key, or tide certificate.

## Cost of adopting

One build step beside the equatorial compiler: a third key (Q) in the doll's
key tuple, six compiled constants per key at **8 Carlson kernels (~0.86 µs
native, the same kernel family the engine already ships from de99)**, a
band-integrity assert in the (E, L_z, Q) solve (the refusal path, criterion
measured), and the B19Q gate as specified in freeze-b19q.md. Kicks: (E, L_z,
Q) drift re-anchors exactly as the galaxy doll's (E, L) drift does.

## Fit with PRINCIPLES

#18 "the right representation so that the math is trivial": the squared-pole
basis element collapses into the same kernel family as everything else — no
new mechanism, one closed form. #1/#17 "the cheapest compute is compute not
done" / "the best part is no part": 8 kernels per key, zero kernels per read.
#10 "measure before claiming": P5's mechanism was measured to be wrong and is
reported as wrong. #2: exact physics stays the oracle; the freeze judges
behaviours, not trajectories.

## The lens (what the second-author lens may have missed)

The port was priced by kernel count at de99's measured ns, not timed natively
(no Rust build here); the SIMD/vectorisation question de99's record leaves
open applies unchanged. The LT readout took two attempts (first formula wrong
by 15.6×, caught against the checker's anchored number — an external anchor
is what made the catch possible, and a solo run would have shipped the wrong
formula). The census grid is coarse at the 3.7% class's boundary.
