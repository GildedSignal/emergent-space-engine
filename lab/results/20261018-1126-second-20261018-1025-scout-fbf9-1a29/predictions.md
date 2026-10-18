# Predictions (written before the decisive experiment)

Topic: encounters — the checker-named gold experiment for 20261018-1025-scout-fbf9
(silver): "fly the due-band per-kick rule on the shipped tier (`tier::arm_pair`'s
callers) at 10⁴-occupancy cells and measure re-arms/kick — Θ(n) kills the toy's window
model (the standing/dwell class is where to look)."

Instrument: a Rust crate (`flight/`) built against the shipped `emergent-encounters`
lib, using the shipped Phase-A path exactly as `main.rs::kick` drives it (Sorted
U-range scan → `is_candidate` → `tier::arm_pair` at safety 1.1), on the toy's scene
constants: 10⁹-density annulus cells (ρ = 1e9/(π·(3²−2²)) AU⁻², W = n/(ρ·2π·2.5)),
a = 2.5 AU, e Rayleigh 0.07 capped 0.4, reach B = 5×10⁵ m = 3.34×10⁻⁹ AU (cd3b),
horizon H = 8 intervals (interval = P(2.5 AU)/4.43), band = first due < (H+2)
intervals, kick = dv/v·|v| at a random anomaly in a random direction (the toy's
`kick_at` math, ported; pre/post compared at the same anomaly). Two due definitions
are measured on the same bodies: the SHIPPED due (first in-window passage from
`arm_pair`) and the ANALYTIC first-conjunction due (Δλ/Δn, the toy's constant).

- **P1 (wholesale structure, fe6b shape):** scanned and candidate pairs per kick
  = n−1 at every n (all cell-mates pass the Binet cone at this e-spread); slope 1.
- **P2 (the rule's cost, shipped dues):** shipped-due band < 0.01 re-arms per body
  per kick at n = 10⁴ — in-window dues for near-co-orbital cell-mates sit ≥ 10⁴
  intervals out (window width ~ ρ/v_⊙ ≈ tens of ticks vs rotation step ~ 10⁵ ticks),
  so almost nothing is in-band. NOT Θ(n) at any n tested.
- **P2b (the toy's constant bridges):** the analytic conjunction-band on the same
  bodies reproduces the toy's n² law within ×2: ~3.4×10⁻⁴ / 0.034 / ~3.4 per body
  per kick at n = 10³/10⁴/10⁵.
- **P3 (soundness + negative control):** armed flips per kick = 0 at dv = 2⁻²³ at
  every n; flips outside the (H+2)-interval band (violations) = 0 at 2⁻²³; at
  dv = 2⁻¹⁴ violations > 0 somewhere (the +2 margin assumes quantum kicks — the
  instrument must be able to fail).
- **P4 (dwell/standing audit, the kill test's named suspect):** standing pairs
  (equal integer period in ticks) ~ 30–300 at n = 10⁴ (birthday over a ~6×10⁵-tick
  period spread), standing-armed = 0, and the dwell class does not make the band
  Θ(n).
- **P5 (live anchor on shipped windows, arming live):** armed per focal body per
  8-interval horizon over 3×10⁴ true-density partners sampled in ±0.35 AU:
  extrapolates to 10²–10³ per body per horizon (toy: 525–1050); flips 0.1–1× armed
  at dv = 2⁻²³ (miss churn on shipped safety-1.1 windows); violations 0 (churn
  lives inside due < H, i.e. inside the band).
- **E3 control (instrument sanity at amplified reach 0.02 AU, n = 80):** the armed
  set covers every `pair_events` hit (0 missed); dv = 2⁻¹⁴ produces band violations
  there.


## Amendment (after a smoke run, before the final record run)

The first build ran once as an instrument shakeout (68 s; `work/flight-smoke.txt`,
kept). It exposed two instrument defects and one mechanism signal, all addressed in
the final run: (a) shipped `arm_pair` dues carry the `ext = pi + 2pj` arc-traversal
slack, so an armed pair's min-section due can exceed the (H+2) band — the final run
also scores the rule "re-check iff armed OR due < band"; (b) violations must split
silent→armed (event-loss risk) from armed→silent (wasted work); (c) the smoke saw
nonzero quantum-kick flips on the shipped tier (~0.1/kick at n = 10⁴, ~80% outside
the band, dv-independent across 2⁻²³/2⁻¹⁷/2⁻¹⁴) — my P3 "flips = 0, violations = 0"
is therefore expected to FAIL in the letter, and the final run adds per-violation
forensics (pre-due, |Δn|, and the exact `pair_events` verdict on every silent→armed
violation) to decide whether the channel is the beat re-lottery (dv-independent,
deep-beat pairs) or a walk (dv-linear). The kill line stays as pre-registered.
**Kill (pre-registered):** shipped-due band > 1 per kick per body at n = 10⁴, or
2⁻²³ violations > 0 with a count growing in n ⇒ the toy's window model is dead on
the shipped tier, and this dossier reports the refutation (still a gold-shaped
outcome per the brief: "or a clean refutation of it").

Budget: ~60 s single-threaded; n ≤ 10⁵ bodies (< 20 MB), no thread pools.
