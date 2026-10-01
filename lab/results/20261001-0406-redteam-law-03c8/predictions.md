# Predictions (written before the decisive experiments)

Run: 20261001-0406-redteam-law-03c8. Attacks ranked in `dossier.md`; here are the
cases I have NOT tuned on, and what I expect before running them.

## E1 — Moving-lens observation gap (strongest attack)

The law's observation layer composes static per-doll `deflection(b)` from the memo
(law.md "Observation"; representation.md "Lensing adds crossings, from each doll's
memoized deflection(b)"). No boost of the deflection by the doll's velocity relative
to the observer is specified anywhere; B3 judges static deflection only.

Truth = the lens's rest-frame Schwarzschild deflection, exactly Lorentz-transformed
to the observer frame (a uniformly moving lens is the static solution boosted).

Held-out cases and predictions:
- head-on geometry (photon retrograde to the lens's motion), β = 0.9:
  observed bend ≠ static memo bend; I expect a relative error of order
  2γβ ≈ 4, i.e. hundreds of percent, not a small correction.
- transverse geometry (lens velocity ⊥ photon path), β = 0.9 (held out):
  error still first order in β; I expect ≥ 30%.
- β = 0.1 (held out): error ≈ 10–20% (linear in β), already above B3's 1% bar.
- Shapiro-type arrival-time shift through a moving doll: also first order in β.

If instead the errors come out second order (β²), the attack dies and I report the
observation premise as a survivor with the measured numbers.

## E2 — B9's ≤ 64 crossings per cycle is e ≤ 0.6 in disguise

Crossings per cycle = 32·log₂((1+e)/(1−e)) at m = 16. Predictions, not tuned:
- e = 0.6 → exactly 64 (the gate's own number, consistency check);
- e = 0.9 (held out) → ≈ 136 > 64;
- e = 0.99 (held out) → ≈ 244 > 64.
So the frozen gate text fails the law on any scene with e > 0.6 (comets,
flybys, interceptors) unless the judged scenes silently cap eccentricity,
which the frozen text does not state.

## E3 — Memory: the 16-byte tube vs the charged remainder

From the code (`tube.rs`, `binding.rs`): Tube = 16 B, but every event-active body
carries `TubeEvent` = tube + Residual(4×i128 = 64 B) + event_time + exponents
≈ 88–96 B. Predictions:
- no B-gate in law.md's frozen table judges bytes per body (B10/B15 are CPU only);
- 8 GB therefore fits ≤ ~9×10⁷ event-active bodies, under 10% of 10⁹, before any
  geometry, programmes or contact structures are resident.

## E4 — Averaged tide just below τ₀ (premise-2 robustness probe, run only if time)

Truth (full circular restricted three-body) vs the law's layer (parent direction
frozen at each periapsis = the orbit-averaged kick), moons with apoapsis at 0.45
and 0.49 R_H (τ_apo < 0.08), e₀ = 0.05, 300 parent orbits. Prediction: the layer
SURVIVES at leading order — max |Δe| < 0.02, mismatch growing toward the boundary.
If |Δe| > 0.1 anywhere below τ₀, premise 2 is falsified in-regime and I report that.
