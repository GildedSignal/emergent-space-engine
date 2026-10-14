# Predictions — 20261014-0727 (second author on 20261014-0450-scout-b29a)

Written before the decisive run. The experiment: compose c7eb's validated contact impulse
(Δv_i = 2 m_j b/(|b|² v_rel), geometry drawn from the 482 measured game-density truth
encounters) as the ΔE/ΔL source through both arms (arm A exact refit via cartesian +
`Rebinding::from_state`; arm B key-space integer ΔE/ΔL from conjunction geometry alone:
polar readout (r, v_r, v_t) + (d/a, v_rel/v_circ, cosψ, side, m_j), closed-form metric
algebra, floored to the key's Q48/Q32 quanta), on a cold belt (σ0.07, e≤0.6) and an
eccentric belt (σ0.3, e≤0.9), plus the Darwin-domain statement on a far band
(p ∈ [16384, 18432) M, beyond `Key::darwin`'s 8192 M cap, via the uncapped v3
`OrbitKey::bound`).

Mass ladder in units of the central mass (radii at 2.5 g/cm³; m_crit = 1.3e-17 ≈ 1.35 km
from the c7eb gold run at game density): 6.6e-21 (50 m), 5e-19 (1-Mt ship), 1.3e-18 (600 m),
1.3e-17 (m_crit), 6.6e-16 (5 km), 1.3e-14 (28 km), 4.7e-10 (Ceres).

- **P1 (arm-vs-arm, the shape grid).** Arm B vs arm A in OrbitKey space (k Q48 / periapsis
  quanta at Q40): median ≤ 3e5 quanta (≈1e-9 relative in k), p95 ≤ 3e6, at every mass and on
  both belts — impulse-independent, the double-quantization floor, not error that grows with
  the kick. The real distribution's cosψ ≈ ±1 structure changes nothing here.
- **P2 (arm-vs-truth, the invariant grid).** Arm B's key vs the kicked state's f64 invariants:
  median ≤ 8 quanta of max(E Q48, L Q32) at every mass on both belts — the birth floor
  (3.0/7.6 in b29a) holds with the real impulse distribution.
- **P3 (refusals).** Arm A refit refusals: 0 at masses ≤ 28 km; Ceres ≥ 0 but ≤ 10%
  (the real tail reaches Δv/v ~ 0.1–0.4 only at the closest-d × slowest-v_rel corner);
  `Key::new` refusals ≤ Ceres-level. No plunge at any mass ≤ 28 km.
- **P4 (σ-dependence of the composed cost, cold vs eccentric).** Cold: composed refit arm
  ≈ 30–50 µs p50; eccentric ≈ 60–110 µs p50 (compile and refit each ~2× at σ0.3, per the
  checker's own 76 µs measurement); the key-space arm stays ≤ compile+read+~2 µs on both
  (the kick is not the tail). So the 13×-under-sticky headline is cold-only and the
  eccentric ratio is ~6–7× — priced, not assumed.
- **P5 (the store's own grid absorbs the real distribution).** At masses ≤ m_crit, ≥ 90% of
  events leave the p and e columns unchanged (|Δp| and |Δe| below one store quantum: the
  b29a synthetic ladder's "0/4096 identical" was glue-bound; the real ladder sits *below*
  the column grid almost everywhere). 28 km: p/e deltas of order 1–10 quanta. Ceres: > 80%
  wide records.
- **P6 (far band, the domain statement).** `Key::darwin` refuses 100% of the far band
  (clean Err). The invariants-direct row→(E,L) closed form lands L ≈ 1.6e4·2³² > 4096·2³²,
  so `Key::new` refuses ~100% — the key-space arm's true boundary is the legacy L cap, not
  Darwin's p cap. The v3 path (`OrbitKey::bound` → compile → readout → kick → refit → scar)
  composes with ≥ 95% success at m_crit, ≥ 80% at Ceres, at costs within ~2× of the cold
  belt's.
- **P7 (bytes).** Scar bytes per event at m_crit ≤ 12.05 B/event on both belts (near-all
  12-B narrow records; the real rock distribution rarely forces Wide).

Kill criteria: P1 median > 1e6 quanta at any mass ≤ 28 km, or arm error growing with the
kick (correlation across the mass ladder) — the key-space arm then fails on the real
distribution and the refit arm is the floor. P2 median > 20 quanta — the closed-form ΔE/ΔL
does not reproduce the birth floor. P6 v3 composition < 50% success — the far-band
statement fails and the store's outer bands have no promotion.
