# predictions.md (written before the decisive sweep; not tuned on it)

Question: what must a gravity-news version carry so a consumer orbiting a *thrusting*
source holds its error quantum — (x, v), (x, v, a), or (x, v, a, j)?

Setup (falsifier.py, pure Python): Carlip's Lorentz-invariant scalar retarded force
(gr-qc/9909087 §3, eq. 3.1) as the toy field; source on an analytic thrust program
x(t) = ½a₀t² + (1/6)jt³ (constant burn, optional jerk ramp); consumer on a circular
orbit at β_c ∈ {0.003, 0.03, 0.3}; versions broadcast every T (window); the consumer
reconstructs the source's retarded state from the newest version by Taylor order
1/2/3; oracle arm = the exact retarded state. Scar = |ΔE| between payload arm and
oracle arm, per rebind (per window), over 2 orbits, RK4 h = P/1024.

Held-out predictions (cases I did not tune on — the T-sweep and jerk sweep are the
decisive ones; β_c = 0.03 is the tuning anchor only):

1. **Positive control (7ab4's law, reproduced):** payload (x,v) under a constant burn
   (j = 0): scar per rebind ∝ a₀, T-exponent ≈ 2 (mixed δv a·Δ and tidal ½aΔ²
   channels; I predict the measured slope lands in [1.9, 2.6] at β_c ≤ 0.03).
2. **The a-slot kills it:** payload (x,v,a) with j = 0 sits at the integrator floor
   (≤ 10⁻¹² relative), ≥ 5 orders below the (x,v) arm at T = P/64.
3. **The jerk residual is real and one order higher:** with j ≠ 0, the (x,v,a) scar
   ∝ j (slope 1.0 ± 0.1 in |j|) with T-exponent in [2.9, 4.1] (δv channel predicts 3,
   tidal channel 4; the mixture is measurable, and whichever dominates is itself the
   answer for the readout). The (x,v) arm's exponent is at least one full order below
   the (x,v,a) arm's.
4. **β_c scaling:** scar ≈ C·(β_c²/2)·(δv/v_c) with C ∈ [0.3, 2] across the three β_c
   (7ab4 measured 0.7 for the rebind channel on the plane; if the toy's C is in that
   band the mechanism is the same).
5. **Cadence invariance of the shipped-style readout:** an "as-if-now" readout (treat
   the delivered version as current, which is what a tube without retardation does)
   shows a scar independent of T (slope |d log scar / d log T| ≤ 0.2) — reproducing
   7ab4's "rekeying faster buys nothing" and predicting that the retarded readout is
   the *other* half of the fix (its T-slope is the mirror image, ≥ 1).
6. **Sign:** the jerk-term scar flips sign with j; no |·| saturation.

What would make me wrong: if the (x,v,a) arm with j ≠ 0 sits at the floor too, the
payload question is undecidable at these amplitudes (negative control failing); if
the (x,v) arm shows T-slope ≤ 1, the δv channel dominates by more than I modeled and
the T* window estimate below is conservative by that factor.
