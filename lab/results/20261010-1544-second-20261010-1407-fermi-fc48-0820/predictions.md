# Predictions (second author, written before floor9.py)

Scope: the checker's named experiment — the sorted-microstate floor at the 10⁹
scaling — plus the encoding-class question it flagged as unexamined (which
fields an exact encoding must carry; identity as gauge).

Model and quanta: identical to the shipped run (its hlive.py/floor.py): belt
a ~ U[1, 1.5] AU, ex, ey ~ N(0, 0.01²), M₀ ~ U[0, 2π); quanta E 32-bit over
the a-range (Q_A), L 32-bit (Q_L), ϖ 32-bit, t_p 64-bit per radial cycle.

- **P1 (record regenerates).** `python3 hlive.py` (seed 20261010) reproduces
  the shipped `hlive.json` byte-identically and a `final_state.npz` on which
  `floor.py` gives the shipped 75.5 / 76.1 bits/body.
- **P2 (the checker's correction holds).** The 3-field sorted floor
  ((a, e_vec); the shipped floor.py scope) obeys
  floor(N) = H₁ − log₂N + log₂e with one H₁ per state across
  N = 2¹²…2²⁰ (subsamples of the shipped state + a fresh 2²⁰ birth state):
  slope −1.00 ± 0.02 in log₂N, H₁(birth) = 90.0 ± 0.4, H₁(final) = 90.6 ± 0.4.
  At N = 10⁹: 61.5 ± 0.5 (birth) / 62.1 ± 0.5 (heated) bits/body
  = 7.69 / 7.76 GB — under the 64-bit budget by ~2.5 bits, as the checker said.
- **P3 (the missing degree of freedom).** The tube's stored state carries the
  phase (t_p, 64 bits per radial cycle; law.md: "position and velocity are
  derived when asked"), and floor.py omits it. At the tube's own quantum the
  phase is uniform by construction (M₀ ~ U[0, 2π)), worth 64.0 bits/sample
  (the shipped H_tp_mod saturating at 63.9 is the cross-check). So the
  4-field sorted floor at 10⁹ = P2 + 64 ± 1 ≈ 125.5 / 126.1 bits/body
  ≈ 15.7 / 15.8 GB — over 8 GB by ≈ 2×, and the margin never opens (the
  phase term does not shrink with N beyond the single −log₂N already counted).
- **P4 (robust to the other spec reading).** If (E, L) share 32 bits total
  (the strict 16-byte tube reading) the orbit-shape term drops (the belt's
  (E, L) support is a thin band, ~2²⁵ of 2³² cells) but ϖ (32, uniform) and
  t_p (64) remain: floor ≈ 92 ± 3 bits/body at 10⁹ ≈ 11.5 GB — still over.
- **P5 (no operational encoder rescues it).** A faithful port of shipmem's
  Elias–Fano (`program.rs::Ef`) on the real quantized a-cells lands within
  ≤ 3 bits/key of the uniform multiset bound log₂(u/k) + log₂e; on full tube
  keys at 10⁹ any EF/gap coder costs ≥ floor₄ + O(1) ≈ 128–133 bits/body.
  The 2× gap to 64 bits/body is encoder-independent.
- **P6 (scar form vs floor at 10⁹).** The shipped scar form (identity kept)
  costs 126.4 bits/body at orbit 1 and 149.3 at 1024 orbits, while floor₄
  stays ≈ 125.5–126.2: the scar form is near-optimal right after the first
  pass and loses ≈ +23 bits/body by 10³ orbits. Both classes sit ≥ 1.95×
  over budget.

**Kill criterion.** If the 4-field floor at 10⁹ measures < 64 bits/body, the
original headline is dead for good and the checker's restatement ("under
budget, ≤ 3% margin") is the final word. Within the tube's own quanta this
cannot happen (the phase alone is 64 − log₂(10⁹) + log₂e ≈ 35.5 bits/body),
so the falsifiable content sits in P2 and P5's numbers; if H₁ is not stable
in N (P2 fails by > 1 bit of slope), the whole extrapolation method dies and
with it both the checker's correction and mine.
