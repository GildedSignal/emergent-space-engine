# Predictions (written before the decisive run)

Question: can the contact skip (a detected crossed-in-bin pair exchanges nothing, 8144/1648)
be fixed by one closed-form rule on the lattice's own integer data — no sub-chronon stepping,
no carried irrational state? Mechanism claim: the contact normal decomposes as
n·R = P − s·w with P = (d·|w|² − w·(d·w))/|w|² rational in the integer lattice data,
w·P = 0 EXACTLY in integer arithmetic, and s = √D/|w|² the only irrational (D = (d·w)² − |w|²(|d|²−R²),
an integer). The exchange impulse is then a closed form in (P, w, √D, R) needing ONE integer
square root and ONE divide per component.

Held-out cases (not tuned on; the arms sweep them): grazing b = 39R/40, β = 0.9 (ρ = 512),
head-on b = 0, oblique b = R/4, R/2, 3R/4, crossing depths ρ ∈ {3, 30, 300, 512}, R = 2048
quanta (1648's gas reach), Q = 2²⁰ quanta per c·chronon. k = 20 fractional bits on the isqrt.

- **P1 (identity):** w·P_num = 0 exactly in int64/int arithmetic on every arm, and D ≥ 0
  exactly on every crossing arm, D < 0 on the miss control (b = 1.5R). If the integer
  identity fails anywhere the design is dead.
- **P2 (the hole, reproduced):** the shipped rule (receding gate) applies 0.0 of the exact
  impulse on every crossing arm — recovery fraction 0, matching 8144's closed form
  skip ⟺ τ* inside the bin.
- **P3 (the fix, quantized):** the integer rule (isqrt at k = 20 bits + one rounded divide
  per component) recovers ≥ 99% of |Δw| with outgoing-impulse angle error ≤ 5×10⁻³ rad on
  EVERY arm including the grazing tail. Risk case I expect to be worst: b = 39R/40 at ρ = 3
  (small √D, isqrt relative error largest) — I predict it still clears 99% because the
  normal there is dominated by the rational part (0, b).
- **P4 (timing):** applying the impulse at the bin end (detection) costs a position error
  up to (1−τ−)·|Δw| ≈ R·ρ quanta (I predict ~10³–10⁵ quanta at ρ = 300–512 — metres at
  ship scale), while the root-tick schedule (ceil(τ−·2^k) sub-ticks, the engine's own tick
  grid) costs ≤ |w|·2⁻ᵏ·2 quanta — so the schedule form, not the rule, is what the
  adoption must choose; both share the same exact impulse.
- **Kill criteria:** any arm where (a) the integer recovery < 90%, or (b) the angle error
  > 0.05 rad, or (c) the rule fires on the miss control. Also killed if the rule needs
  more than one isqrt + one divide per crossing (carried irrational state).

Controls both sides: miss (b = 1.5R) must not fire; the already-inside-at-boundary class
(|d| ≤ R, the shipped exchanging regime) is out of scope and untouched — the rule addresses
only the crossed-in-bin class, where the shipped negative control (0 impulse) is the floor.
