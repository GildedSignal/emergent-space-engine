# B19Q — the B19-shaped freeze for inclined Kerr (Q ≠ 0)

Frozen BEFORE any gate run; design text only (the lab never touches gates).
Shape follows B19 (equatorial Kerr: cycles, advance, fates, frame dragging,
Penrose, light, χ=0 digest), extended by the third key Q. All criteria are
behaviours/statistics — no trajectory identity with any float truth.

## The object under test

The compiled 2-torus: six per-(E, L_z, Q) constants (Λ_r, Λ_θ, ΔΦ_r, ΔΦ_θ,
Δt_r, Δt_θ) as pure Carlson kernels (this run: 2×RF + 4×RJ + 2×RD distinct per
key, 0.86 µs at de99's measured ns). Oracle: 30-dps separated quadrature
(the run's QD arm), plus the independent raw-metric Hamiltonian arm the
checker added (no Carter separation) for formulation-level attacks.

## Criteria (frozen)

1. **cycles** — On the frozen 25-row grid (a ∈ {0.2, 0.6, 0.9, 0.998} ×
   (p, e) ∈ {(12, 0.1), (8, 0.5)} × θ ∈ {30°, 60°} + retro θ150° + controls
   + held-out e = 0.9 / p = 6.8): compiled Λ_r, Λ_θ vs oracle, float ≤ 1e-11
   (measured: 3.67e-12), zero integer-advance disagreements at the law's
   quantum. Positive control: the oracle vs its own 40-dps refinement.
   Negative control: the J basis element replaced by Π alone (must fail dt_r
   by O(1)).
2. **advances** — ΔΦ_r and ΔΦ_θ (nodal included) vs oracle ≤ 1e-11; retrograde
   sign structure preserved (ΔΦ_θ < 0 at L_z < 0). Negative control:
   sign-flipped spin a → −a (frame dragging must flip).
3. **fates / refusal path** — Every key with no adjacent-turning-point bound
   solution must be REFUSED loudly, never NaN: the census class (an extra
   quartic root inside the intended band, R(rp + ε) < 0; 3.7% of the sweep,
   a ≤ 0.3 ∧ e ≥ 0.5 ∧ p ≤ 7.5), the fsolve-non-convergent class (12.7%),
   E ≥ 1, and Λ_r → ∞ at the plunge separatrix. Positive control: all 527
   handled census rows compile.
4. **frame dragging** — At p = 30, a = 0.2 (weak field):
   |Ω_φ − Ω_θ|·p^{3/2}/(4πa) ∈ [0.95, 1.15] per azimuthal revolution
   (measured on the port: 0.975–0.986 at e 0.1–0.3, θ 45°–75°; the checker's
   independent Hamiltonian arm: 1.10), inclination-flat to 2% (measured
   0.6%), e-flat to 2% (measured 1.1%). a = 0: ΔΦ_r ≡ 0 identically,
   ΔΦ_θ = 2π exactly, radial constants inclination-independent.
5. **degenerations (the χ=0-digest analogue)** — Q → 0: radial constants match
   the SHIPPED equatorial compile (kerr.rs conventions) to ≤ 1e-10, Λ_θ →
   2π/√(Q + L_z² + a²(1−E²)) (the harmonic limit; measured digit-exact);
   a = 0: 2π·Λ_r/Λ_θ = 2π/√(1 − 6/p).
6. **cost** — ≤ 8 distinct Carlson kernels per six-constant key (measured:
   RF×2, RJ×4, RD×2), priced ≤ 1 µs at de99's kernel ns; the per-frame read
   carries zero kernels (compile once per key; reads are arithmetic plus the
   amplitude Newton).

## Edges deliberately OUT of this freeze

Resonant tori (Λ_r/Λ_θ rational): the coordinate-time readout's inversion —
the Mino-time torus itself stays exact; the readout conditioning is the known
LISA problem and needs its own criterion if the engine reads in coordinate
time. Photon Q ≠ 0 (Teo's spherical family): not attempted. The integer port
(Q's word width, exact integer advances): the build step after this freeze.
