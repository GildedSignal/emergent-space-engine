# Predictions (written before the anchor run and the ledger script's outputs were seen)

Model: 2-D Poisson sweep on the shipped belt geometry (scenario.rs: `a` uniform [2,3) AU,
`e` Rayleigh 0.07 redrawn above 0.4, planar, radius 34·2⁻¹⁰ ru ≈ 49 m; 1 ru ≈ 1.48e3 m from
the Moon's 1,176-ru radius; game AU = 1.013e8 ru ≈ SI AU). Conjunction rate per body:
n₂D · 2b · v_rel, n₂D = N/A_eff, A_eff ≈ 25 AU², v_rel ≈ 1.8 km/s (shear + epicyclic at
conjunction). Belt own period at 2.5 AU ≈ 12,480 kick intervals ≈ 3.51e8 game-s (grid
anchor: first kick p50 = interval/2, interval = P_D/2⁷).

- **P1 (anchor, must hold or the run is VOID):** shipped `belt_first 10000` prints belt
  first-item p50 ≈ 14,000–14,150 game-s (interval/2 of 28,141.5; 3294's record), locals
  p50 < 1,000 game-s. If not, my rate identity is built on the wrong grid and everything dies.
- **P2:** contacts (b ≤ 98 m) at N=10⁹ land in **0.1–1.5 per game-second** (point estimate
  ~0.35). NOT zero: at 10⁹ real bodies the shipped belt grinds ~8e7 contacts per own-orbit.
- **P3:** Dohnanyi-class conjunctions (b ≤ 5×10⁵ m, 2b89's key-mint scale) at 10⁹ land in
  **5×10²–5×10³ per game-second**; at shipped per-event costs (16.4 µs mint, 0.6 µs exact
  eval) the whole event flow is **≤ 0.1 cores** at rtf 100.
- **P4:** 1b1f's measured 0.105–0.247 encounters/body/orbit at N=800 is reproduced by the
  model only if their encounter radius was ~10⁸–10⁹ m (I infer b ≈ 1.6–3.9×10⁸ m). If their
  b was contact-scale the model over-predicts by >10⁵ and P5 fires.
- **P5 (kill criterion):** if any gold-anchored flow number (ec74's λ ∝ density^0.95; 09a1's
  contacts ≈ 0.9 bits/s at 10⁹) disagrees with the model by more than 10×, the "event flow is
  cheap" claim is dead and the encounter row stands as genuinely expensive.
- **P6 (composition, arithmetic):** the belt stream at 10⁹ rtf 100 with every measured lever
  composed (split 8 ×0.125, secular survival 0.615, boundary fast path ~free) lands at
  **5–9 M1 cores** (4e2d's 10.3 uses the pre-fast-path +25% boundary); required cadence cut
  for 4 cores: S* ≈ 18–32. The kick-cost scoreboard row (10³·³) stays retired as a 10⁹ lever.

Held-out arms the checker may add: N=10⁵ belt_first (locals cap 300 → belt fraction rises;
p50 must stay ≈ 14,071 ± 3%), seed 2, and the model's b-scaling (∝ b¹, count ∝ b) at
b = 10⁶, 10⁷ m.
