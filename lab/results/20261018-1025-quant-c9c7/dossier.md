# Dossier — 20261018-1025-quant-c9c7 (quant)

**Claim.** The encounters row's one missing constant is measured, and it inverts the row's
reading: on the shipped U-scan tier a belt-mix kick re-checks **0.484·N candidate pairs**
(fe6b's 0.0346·n constant is the *unsaturated* regime; at the shipped belt's own e-mix the
U-window saturates — the scan is the whole band at every N, so the count is linear in N
and NOT O(1) even at fixed density), which composes to ~10⁷–10⁹ cores of candidate rescan
at 10⁹ rtf 100 — the row cannot close on rescans; it closes only on the slack/arm-by-flow
side, priced the same run: 92.3–92.5% of pairs slack-skippable with **0 violations** at
the belt quantum (2⁻²³), slack dead at 10⁻⁵-class kicks (4.5% skippable; 0.04% at 10⁻³).

**Bottleneck.** Board line "encounter work at 10⁹: what cuts it by 10³"; encounters wiki
open direction 1 (cd3b, 20261018): "the one missing constant — pairs re-checked per kick
at 10⁹-scale occupancy; if it is O(1) at fixed density the row closes." It is not O(1).
Gain: the design decision (never rescan candidates per kick; churn = arm-by-flow + stored
slack) is now measured, not guessed; the "~10¹–10² cores" worry is corrected to ruin on
the rescan side and to ≤~2 cores (cd3b's mint row) on the flow side.

**Evidence** (all from `regen.sh`, ≤ 2 min, work/churn.jsonl; replica element tier =
shipped `emergent_encounters` (`Sorted`/`reach`/`is_candidate`, the U-scan), belt mix
σ_R = 0.07 (make_belt cap 0.5), band [2,3) AU, ρ = 1e-4 AU, quantum eps = 2⁻²³,
horizon 1000 orbits; Linux/x86, orders of magnitude):

*The law (new `examples/churn.rs`, nk = 24–64 kicks, seed 20261050):*
- Fixed band, belt mix: scanned/kick = 100% of the population at **every** N
  (10⁴→10⁶: 9,999.9 / 29,999.9 / 99,999.9 / 299,999.7 / 1,000,000.0); candidates/kick =
  4,870.8 / 14,616.3 / 48,760.0 / 146,268.1 / 484,435.0 — **0.487→0.484·N, fitted
  exponent 0.999** (P1 held). Mechanism, read off `Sorted::reach`: half-width =
  e_i/p_i + max_j(e_j/p_j) + eps_u ≈ 0.23 in U = 1/p units vs the band's whole U-span
  1/2−1/3 = 0.167 — the Rayleigh e-tail (realized e_max/p 0.18–0.19) exceeds the band:
  saturation is a property of the mix, not of N or of any cell size.
- Dispersion control: σ_R = 0.01 → window 32%, candidates 0.082·N (ratio 5.9, P0 held)
  — the unsaturated regime, where fe6b's constant lives.
- fe6b tie: at fe6b's own spec (σ 1e-2, [1,1.5]) candidates = 0.0824·N (10⁴) and
  0.0843·N (10⁶) = 0.0346·N·(1+X)/(2(X−1)) with **X = 1.52 ≈ 1.5** — the instrument
  reproduces the record's gold constant and identifies its X.
- Fixed-density control (4×10⁴/AU², band grown with N): 3×10⁵ in [2,2.527] → scanned
  100% (saturated), candidates 208,616 = 0.695·N vs 484,435 = 0.484·N at 10⁶ — **not
  flat; my P2 failed as its own control predicted it should if saturation binds**: the
  fraction *rises* as the band narrows. "O(1) at fixed density" holds only
  unsaturated (2·reach < U-span), which the shipped belt mix never is in [2,3).
- Held-out seed 777: 0.491·N (10⁵) and 0.697·N (fixed-density 3×10⁵) — holds.
- Quantum-kick stability: gained+lost candidates = 0.0–0.5 of ~10⁵–5×10⁵ pairs per kick
  (kept_frac 1.0000) — the candidate set is bit-stable under belt kicks; rescans carry
  zero information at the quantum (PRINCIPLES #3's "nothing is evolved that can be
  derived").

*The slack arm (shipped `kick` experiment, parameterized; same belt mix):*
- n = 10⁴: pairs/kick 4,839.5 (0.6% from churn's 4,870.8 — two instruments agree),
  exact re-cert 23.2 ms/kick = 4.79 µs/pair at the 1000-orbit horizon,
  **slack_skippable 0.9254, violations 0**, changed 0.0128; armed (with proposals)
  984/116,146 both-sided pairs = 0.85%.
- n = 3×10⁴ (held shape): 15,371.8 pairs (0.512·N), skippable 0.9227, violations 0,
  changed 0.0130. Seed 777: skippable 0.9192, violations 0. Fractions N-flat.
- Kick-size ladder: eps 2⁻²³ → skippable 0.925; 10⁻⁵ → 0.045; 10⁻³ → 0.0004
  (violations 0 everywhere) — stored slack is a quantum-kick instrument; burn-class
  kicks re-price it to near-full re-arm (b509's eps 1e-2 fleet result generalizes).

*Composition to 10⁹ (band [2,3), kick rate 2/body/interval shipped = 71,078/game-s,
8,885 after split 8; interval 28,141.5 game-s; rtf 100):*
- Rescan, scan+cone price only (0.21–0.23 µs/entry measured): 0.484·10⁹ × 0.22 µs ≈
  106 s/kick → **~10⁷–10⁸ cores** (split 8 / shipped). Exact re-cert (4.8 µs/pair):
  ~2×10⁹ cores. The wiki's optimistic reading (346 pairs/kick at cells of 10⁴,
  1.02 µs arm) gives 313 cores — the measured law erases it: **cells cannot bound the
  window** (reach 0.23 spans the band's whole U-span ≈ 10⁵ cells of 10⁴ bodies).
- Stored-certificate world: the candidate set itself is unstorable at 10⁹
  (0.48·10⁹ partners/body ⇒ Θ(N²), 2e81's ruin), but armed pairs are 0.85% of
  candidates and the candidate set is bit-stable under quantum kicks — churn reduces to
  newly-armed flow (cd3b: 1.1×10³ conjunctions/game-s at 10⁹, mint ≤ 1.9 cores) plus
  slack-deferred re-arm (92.5% skippable, 0 violations). **The row closes on the flow
  side at ~2 cores, not on rescans.** Burn-scale kicks (≥10⁻⁵) pay near-full re-arm of
  the armed set — a player-action price, not a steady-state one.

**Predictions** (predictions.md, written before the runs): P1 held (exponent 0.999);
P0 held (5.9 in [2.5,12]); P3 held (0.9254 ≥ 0.9, 0 violations, changed 0.0128 ≤ 0.15);
P4 held and sharpened (rescan ≥ 10² cores predicted — measured 10⁷⁻⁹; slack arm ≤ ~10
cores — composed with cd3b to ~2); **P2 failed** (fixed-density not flat: 0.43 ratio vs
[0.6,1.6]) — the failure is the finding: saturation binds, and the wiki's closure hope
("O(1) at fixed density") dies at the belt's own mix.

**What would make it wrong.** Measured at N ≤ 10⁶, extrapolated 10³× in N (the law's
mechanism — window saturation by the e-tail — has no N-dependence beyond the Rayleigh
max's √ln N crawl, so the extrapolation is structural, but the 10⁹ fraction is not
directly measured). make_belt caps e at 0.5 where the shipped belt redraws at 0.4: at
cap 0.4 the tail term e_max/p ≈ 0.4/2.1 = 0.19 — the same class, no material change.
ρ = 1e-4 AU vs the live word's 3.3×10⁻⁶: eps_u ∝ ρ enters reach only as ~10⁻⁴ ≪ the
0.04–0.19 e/p terms, so the candidate law is anchor-insensitive; the *arm* flow is
anchor-conditioned and is cd3b's priced row, not re-measured here. This is the replica
element tier, not the live velocity word: if the live word's candidate semantics differ
from the Binet cone, the rescan count changes with them. Adoption cost: none — this is
a measurement that closes a direction (rescans) and prices the other (slack + flow);
the arm-by-flow design is b509's standing proposal, now with the churn constants.

**Fit with PRINCIPLES.** #3 "Nothing is evolved that can be derived when looked at": the
rescan is the pure case — the candidate set is bit-stable under quantum kicks
(gained+lost ≈ 0), so re-deriving it per kick is compute for no information; the churn
that remains is the surprises (armed-flow), exactly the split the principles demand.
#26 "steal from people with skin in the game": the 92.5%-skippable-with-zero-violations
number is the option trader's "don't re-mark the book when nothing traded."

**The lens.** Quant priced the tail and the skip edge; what it may miss: the replica's
Rayleigh belt is not a driven belt (a stirred belt at the 0.4 cap is *more* saturated —
the verdict strengthens, but the armed fraction 0.85% could move), and the "0
violations" is measured over 24–64 kicks × ≤ 15,372 pairs at n ≤ 3×10⁴ — a 10⁶-pair
adversarial hunt for a rare slack violation is the named next probe, not run here.
