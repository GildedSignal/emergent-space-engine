# Predictions — 20261011-1456-second-...-c4ce (second author on 20261011-1332-fermi-e3bc)

Written 2026-10-11 before the decisive run (`jet_anchor`). The checker's named experiment:
anchor the budget identity on the shipped plane's real kick path — bodies kicked per parent
orbit, the cycle-cache miss (re-anchor) rate at belt scale, the per-kick readout the jet pays
(`crossing_state` vs `state`), the realized re-anchor rate. These predictions are derived from
the record (H0190's 32.5 kicks/orbit and the 114× averaging, law.md's jet at ~0.05
compiles/kick, the 5 October correction's exact-memo 0% / quantized 94.5% hit, H0210's 29 µs
kick), not tuned on any run of the new bench.

- **P1 kicks per parent orbit.** The step is 1/2⁷ of the radial period (`step_log2: 7`), so
  128 kicks per orbit are planned and sub-quantum carries suppress some. Predicted: rebinds
  per parent orbit (observed key changes per orbit elapsed) in **[25, 130]** for the LEO
  class (orbiters, player, moon); belt haulers the same constant per orbit.
- **P2 r_kick per body per universe-second.** LEO class (period ~1.4–7.7 h): **0.01–0.03 /s**
  (H0190's unaveraged 1.2×10⁻² vs the planned 128/5840 s ≈ 2.2×10⁻²). Belt haulers at
  0.5–1 AU: **5×10⁻⁶–1.5×10⁻⁵ /s**; at ≥4 AU ≲10⁻⁶ /s. This lands the H0190 factor-2
  ambiguity (checker point 4) on a measured number.
- **P3 readout tiers on the plane's own keys.** `crossing_state` **0.2–0.9 µs**;
  `Orbit::state` **2–8 µs**; the full `Binding::readout` (state + turn + residual)
  **3–12 µs**. So the jet's ε is ~10× below the current per-kick readout, not ~1×.
- **P4 realized per-item wall cost** (the universe's own `cost_ns/items`): ships
  **20–80 µs/item**, player ≤ 400 µs (thrust and encounter work ride on it), fleet ≤ 40 µs.
  The ship number brackets H0210's 29 µs kick.
- **P5 re-anchor rate** (quantized `MemoCode` cell changes per rebind, per body): LEO class
  **0.02–0.15** (the 5 October quantized hit was 94.5% → 0.055; law.md says ~0.05); belt
  haulers **≤ the LEO rate** (weaker tides, slower key drift), 0.001–0.06. Passages (flybys,
  handoffs) count as re-anchors (they always recompile).
- **P6 cache sharing on the real rebind stream.** Exact-key self-repeats on distinct kicks
  ≈ **0** (the 5 October correction); cross-body quantized-cell collapse on the hauler stream
  ≈ **1.0×** (sparse belt, no sharing) and overall ≤ 2×.
- **P7 cold integer floor.** Random `(E, L) += Δ` updates on a 256 MB store (16 M entries):
  **60–300 ns each**, against ~3 ns for the 64 KB L2-resident control — the "rtf 27,000"
  floor tier is ~30–100× optimistic at sparse-active scale (checker's un-run critique).
- **P8 the identity, re-anchored.** With ε = `crossing_state` and the measured ρ:
  jet per-kick cost ≈ 0.4 µs + ρ·(8.5–25 µs) ≈ **0.6–3.4 µs**. At 10⁹ all-active and the
  averaged rate 10⁻⁴/s the jet affords **rtf ≈ 25–130** — i.e. it closes to within ~2× of
  the plane's rtf 100 rather than being cleanly 1.6× or 7× short; the compile-per-kick path
  stays ~25–40× short (rtf ≈ 3, the claim's number, reproduced). At the measured LEO rate
  (~2×10⁻²/s) **no tier closes at 10⁹** (even the cold floor gives rtf ≲ 1); the rtf-100
  active ceiling for the jet at the LEO rate is ~10⁶–10⁷ bodies, and for belt-class rates
  ≳10⁸–10⁹. The claim's structure (per-event compute binds at high rtf; cycle memory caps
  the sparse active set) is predicted to **hold**, with the jet's margin now measured on both
  sides.

What would falsify the claim instead: a measured ρ ≥ 0.3 (the jet degenerates toward
compile-per-kick), or a crossing-indexed readout ≥ 2 µs (the jet's ε advantage vanishes), or
a belt-class re-anchor rate above the LEO class (tides not the driver).
