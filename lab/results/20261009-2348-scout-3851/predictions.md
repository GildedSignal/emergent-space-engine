# Predictions — scout run 20261009-2348-scout-3851

Written BEFORE the decisive sweep. Tuned on (calibration, results-cal*.json):
rp=100, e ∈ {0, 0.3}, α ∈ {+1, −1}. Held out (never run before this file):
rp ∈ {10, 30, 1000, 10⁴} × e ∈ {0, 0.3, 0.6} × α ∈ {+1, −1}.

Model: member x'' + (Ω_m² − α·λ(τ))x = 0, λ(τ) = u³(3γ²−1) along the exact
eccentric tube (the phase-2 closed form). Laws: truth (RK4, cross-checked
against scipy solve_ivp), avg (orbit-averaged λ̄), holdK (λ held at K uniform
epochs, exact per-segment propagation), kickK (tide as velocity impulses at
K epochs, exact own-oscillator drift between). Certificate: Floquet over one
radial period; μ per orbit.

P1 (the band map is the tide's own moments). In every eccentric case, each
truth band with peak ≥ 0.1/orbit has a center within 0.10 (in Ω_r units) of
a predicted center 2ω_eff = k·Ω_r, ω_eff² = Ω_m² − α·λ̄ (k = 1..8). Claim:
≥ 85% of bands matched within 0.10; no truth band orphaned beyond 0.15.

P2 (averaging is blind to pumping, keeps the static edge). The avg law
reports zero parametric bands in every case (100% missed where truth has
any), and its static edge (α=+1: Ω_m² < λ̄) matches truth's unstable region
edge within 5%.

P3 (cadence). hold32 matches every ≥0.1/orbit truth band center within 0.10
and peak within 25%. kick32 does the same (it was calibrated once and fixed
one sign; its band peaks are within 5% at calibration). hold4 misses at
least one peak by ≥ 30% in the e=0.6 cases. hold1 fails qualitatively in
≥ 2/3 of eccentric cases: a spurious ≥ 0.5/orbit band where truth is
stable, or a missing ≥ 1/orbit band.

P4 (e = 0). No truth bands anywhere (λ constant); every law agrees with
truth to < 0.02/orbit.

P5 (the compressive channel turns unsafe at e = 0.6). At e=0.3, α=−1 there
are no truth bands ≥ 0.02/orbit (calibration). At e=0.6, α=−1 at least half
the radii have a truth band with peak ≥ 0.05/orbit.

P6 (bands reach the outermost moons). Moons of a 10⁻³ mass-ratio doll live
at Ω_m ≈ 3–20 × Ω_az (0.9 → 0.2 Hill radii). Claim: in ≥ half the α=+1
eccentric cases, at least one truth band center or the static edge lies
inside [2.2, 3.6] × Ω_az (the outermost-moon range).

P7 (relativistic widening). The driving strength λ̂₁/Ω_r² at rp=10, e=0.6 is
≥ 1.4× its rp=10⁴ value; the static edge in Ω_az units at rp=10 is ≥ 1.2×
the rp=10⁴ value. (Cause: periapsis boost 3γ_p²−1 and apsidal precession
lowering Ω_r.)

Machine state at run start: load 0.90/0.63/0.67, 8 vCPU, 15 GB Linux cloud
box (orders of magnitude only; the integrator re-measures on the M1).
