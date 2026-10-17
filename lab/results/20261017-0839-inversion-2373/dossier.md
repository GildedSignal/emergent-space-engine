# Dossier — 20261017-0839-inversion-2373 (inversion lens)

## Claim

The phase-neighbour certificate — the adopted cure for the formation regime, and the arm
both encounter anchors route fleets into — is quadratic in fleet size for every fleet with
radial scatter, and the composed 10⁹ ledger ("10.3 M1 cores, encounters closed at
0.03–0.6") carries no term for it: at 10⁹ ships in fleets of 10³–10⁵ the arm alone costs
36–4,500 cores (checked pairs, every-8-interval rebuilds) against the 4-core budget, and
the budget's fleet ceiling is F* ≈ 100 ships at σ_e = 1e-2.

## Bottleneck

Board item 2 (encounter work at 10⁹). Inverted: not "what cuts encounter work" but "what
makes it uncuttable". Answer: the goal's own population. Both anchors priced their gates on
random-phase Dohnanyi rock belts (f0a2, 277d); the goal is "billions of **ships**" —
equal-size, formation-correlated — exactly the population f0a2's own text flags ("the
one-bit floor is unsound … aligned → phase") and taleb-09b5 (gold) measured as the pairwise
tier's ruin. The phase arm both routes them to had its cost stated as "O(n·k)" with k
never priced: the shipped code's own doc warns "k is the actual occupancy of a conservative
phase window, NEVER an assumed rank of four" — this run prices it.

## Evidence

Instrument: `crates/encounters/examples/fleetk.rs` on shipped `emergent-encounters`
(print-only, zero shipped lines touched; `work/patch.diff`). Decisive run seed 20261017,
7 s wall; pilot seed 7 disclosed (`work/pilot-seed7.jsonl`). Reproduce: `bash regen.sh`.

**The law** (from `phase.rs` reach semantics; `pred_pairs/pairs` = 1.000–1.004 on every
uniform arm, three decades of F):

  reach = w₀ + 0.75·da·TAU·H,  w₀ ≈ 4·e_max (angular ≈ ρ/a negligible)
  checked pairs per rebuild = F²·reach/TAU  (uniform λ);  ≈ F²/2  (cluster σ_λ < reach)
  refusal into the tree tier at reach ≥ π:  H* = (π−w₀)/(0.75·TAU·da)

**Measured** (σ_e = 1e-2 Rayleigh, ρ = 1e-4, in-family with the crate's own verify sets):

| population | F | mean_k paid | note |
|---|---|---|---|
| keys (one integer period, uniform λ) | 10³ / 10⁴ / 10⁵ | 50 / 532 / 6,257 | k ∝ F; k/F = reach/TAU grows with e_max |
| train (da = 1e-4), H = 0.0078 → 100 orbits | 10⁵ | 6,308 → 7,808 | drift term adds 0.75·da·TAU·H |
| train (da = 1e-2) | 10³ | refused at H = 100 (reach 4.86) | H* ≈ 63 orbits ≈ P_syn/2 |
| cluster (σ_λ = 0.05) | 10³ / 10⁴ / 3×10⁴ | 975 / 9,830 / 29,670 | 97.6–98.9% of the complete graph |
| ring control (fat ρ) | 10⁴, 10⁵ | 2.0 | linear class: the instrument sees it |
| refused-train fallback (tree tier) | 10³ | cand = 96% of F²/2, 1.9M exact evals, 1.6 s | the ruin returns |

**The contrast:** at F = 400 (keys, H = 10 orbits) there were 60 real contacts and
**rank_max = 0** — every contacting partner is the *closest body in the fleet* at contact
time (taleb-09b5's "rank ≤ 4", strengthened) — while the certificate paid mean_k = 16.6
(55 checked pairs, 115 exact evals per real event). The answer is rank-0; the search pays
k ∝ F. At F = 10⁵ the gap is ~1,500×.

**Composed** (`compose.py`, `work/composed.txt`; c_checked = 3.24 µs/pair measured here,
x86 — orders of magnitude; interval 28,141.5 game-s, rtf 100, BELT_SPLIT 8, φ = 1):

| fleets of F | cores @ every-8-interval rebuilds | cores @ per-member-kick rebuilds |
|---|---|---|
| 10³ | 35.9 | 575 |
| 10⁴ | 382.6 | 6,122 |
| 10⁵ | 4,499 | 71,991 |
| cluster 10³ | 701 | — |

Per-member-event unit at F = 10⁴: 266 checked pairs × 3.24 µs = **0.86 ms per member
event — 17× the stream's own ~50 µs/event anchor**: the certificate rides on the kick
stream and dominates it. Budget fit (4 cores, every-8-interval, checked): **F* ≈ 90–110**
at σ_e = 1e-2 (∝ 1/σ_e: ~900 at σ_e = 1e-3). The visit-only floor (0.17 ns/pair) buys no
soundness — the exact checks are the price of not dropping contacts (taleb: the window
tier dropped 4–6% of real contacts).

## Predictions

`predictions.md` written before the decisive run, fitted only on the seed-7 pilot. Of 9
bands, 6 hit exactly (law ratios, k ∝ F, refusal boundaries, cluster mass, timing, rank).
Three misses, all disclosed: cluster quad_frac 0.9890 vs "≥ 0.99" (0.1% under); events 60
vs band [4, 20] (seed volatility — the pilot had 10; per-event work 55 vs band [250, 450],
lower because more events, same paid pairs); tree leafpair_tests 496 vs "≥ 1e4" (the
quadratic shows up in `cand` = 480k, not leaf tests). No kill criterion fired.

## What would make it wrong

- **The slack**: `main.rs`'s kick experiment names "a stored slack (the relative period
  change a silent certificate absorbs)" — if slack absorbs nearly all belt kicks (impulse
  2⁻²³ of speed per fire, f82a), rebuilds are rarer than every-8-intervals and the low
  edge of my bracket moves down proportionally (F=10³: 36 cores → as low as ~0.02 at the
  visit floor with full slack). The bracket's upper edge (per-kick) stands regardless.
- **φ and F are policy**: if the game's ships live in fleets of ≤ 100 (or σ_e ≤ 1e-3
  circles), the term fits the budget. That is a design constraint the ledger must now
  state, not a number it can assume away — nothing on the wiki records it.
- **Cost per pair**: 3.24 µs is this x86 box; the M1 re-measures. The shape (k ∝ F, k ∝ H,
  refusal) is unit-free.
- **Cheaper pair checks**: if the window pass can pre-filter by radial band before exact
  checks, c falls — but for σ_e ≫ ρ (all the crate's own verify sets) the radial filter
  cuts nothing: bands [a(1−e), a(1+e)] all overlap.
- The fix is already in the crate: keys-fleet contact capability is a **birth constant**
  (fixed relative phase ⇒ fixed min-distance), and a train pair's next close conjunction
  is `dioph.rs`'s exact first-hit (O(log m)). The conjunction calendar (r8-v2's lead,
  "a pair's next close conjunction is a Diophantine approximation") is *required* for
  fleet populations, not an optimization — PRINCIPLES #18: the right representation (the
  calendar) makes the math trivial; the window sweep is the listicle.

## Cost of adopting / fit with PRINCIPLES

Nothing to adopt: this kills a comfort, not a component. The composed 10⁹ CPU ledger
(kick-cadence 4e2d: 10.3 M1 cores) must regain an encounter row of 36–4,500 cores at the
goal's fleet sizes, and the encounters page's conflict (f0a2 vs 277d) is moot *for fleets*:
both anchors priced rock belts. "Compute only surprises" (#3): every rebuild re-sweeps a
window whose contacts are rank-0 — the surprise set is empty and paid for anyway, the
opposite of the principle. "A fix signals the wrong representation" (#19): the window is
the drowning car; the calendar is the boat.

## The lens

Inversion found the failure by reading the *composed success* backwards and asking what
population it silently assumed. What it may have made me miss: everything upstream of the
phase arm (the gates themselves — I take f0a2/277d's numbers as given), the M1's real
per-pair cost, and whether the integrator's plane even wires this crate's arm as-is.
