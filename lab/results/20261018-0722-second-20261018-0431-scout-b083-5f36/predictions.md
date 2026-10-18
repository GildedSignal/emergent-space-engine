# Predictions (written before the decisive runs)

Run: 20261018-0722-second-20261018-0431-scout-b083-5f36 (second author on scout-b083).
The checker's named experiment, in three parts: (a) selector soundness `law::hit ⊆ widened
phase window` across e ≤ 0.5, σ_a ≤ 1e-3, both horizons; (b) the shipped answer on a rigid
keys fleet, flown on the shipped binary (empty or residual → the exact tier's read price);
(c) the offset read's cost grounded on the compact store (searchsorted / packed sweep /
binding_at class), replacing the 19.2 ns numpy figure.

Instruments: `tier2.py` (float replica with the **exact branch structure of `law::hit`,
approaching conjunct included** — the original replica's omission, the checker's decisive
adversarial case) and `crates/universe/examples/rigidring.rs` (a rigid ring of K ships,
one compiled key, e = 2^-48, uniform phases, in Home's doll beside the shipped plane;
flown one frame so the radial store registers, then the shipped `capture`+`answer` path).

## Held-out cases (not tuned on)

- **B1 — the shipped answer on the rigid ring** (the coin the checker left standing).
  In-window members (dd ≤ rr, i.e. chord ≤ near): ≈ K·near_arc/π = K·3.26e-3 at ρ = 1e-5
  (~33 at K = 10,000). Prediction: the shipped decode is **not** rotation-exact (position
  and velocity are decoded through independent quantization), so `d·w` is quantization
  noise, its sign a deterministic coin per member: the answer is **residual, ≈ half the
  in-window set (30–70%), zero contacts**, not empty. The alternative (answer = 0) would
  confirm the checker's idealized rotation-exact ring; either outcome is a result, and
  the flight decides it. Kill criterion: if the answer is ~ALL of the in-window set, my
  reading of `hit` is wrong and the re-derivation is void.
- **B2 — h-independence.** The answer count at interval = 2 and interval = 2^12 agree
  within the boundary band (dw's sign does not scale with h; the dd > rr cross-branch
  band shrinks as |w| grows): |answers(h=2) − answers(h=2^12)| ≤ ~20% of in-window.
- **B3 — noise, not physics.** The near set is time-constant on a shared orbit (same
  period: nobody passes anybody). If the ANSWER membership differs across three ticks a
  quarter-period apart (same near-set size), the sign is decode noise; if it is exactly
  the same members, it is a systematic residual. Prediction: membership differs (pure
  noise regime), sizes within ±25% of each other.
- **A1 — selector soundness.** Widened selector = chord(δ) ≤ near + 1.5·h·|Δa| at e = 0;
  the 2^14 per-orbit-class curve widened by one grid cell and the shear drift at e > 0.
  Prediction: **0 misses** (truth ∧ ¬selector) over the full sweep e ∈ {0…0.5},
  σ_a ∈ {0, 1e-5, 1e-4, 1e-3}, h ∈ {P/10, 9}, clustered phases (σ_φ = 0.02). Held-out
  risk: the corner e = 0.5 ∧ σ_a = 1e-3 (epicyclic cross-terms); if misses appear there,
  report them and the widening that covers them.
- **A2 — the price of soundness at the corner.** At h = 9, σ_a = 1e-3 the widening
  (1.35e-2 rad) dominates near (1e-3 rad): reads ≈ 10–15× the near set. At σ_a ≤ 1e-4
  reads ≤ ~3× the near set at both horizons.
- **A3 — the unwidened curve's miss rate among hits** (the checker's currency): ~10–20%
  of true hits missed by the unwidened 2^14 curve at e = 0.5 under clustering (the
  original's population-disagreement metric understated this); the widened selector
  misses 0.
- **C1 — store-grounded selector cost.** δ-sorted class-major store: the whole window
  lookup on K = 10^6 is a binary search, < 20 µs total (not per member); packed unsorted
  sweep < 3 ms for 10^6. Both ≪ the 4.4 s shipped answer.
- **C2 — exact-tier read cost.** The flown ring's per-answer cost lands in the 4.4 µs
  per-candidate class (604c) within 2×; the near set's reads at 7.1 µs each price the
  ρ = 1e-6 uniform closure at ≈ 353 × 7.1 µs ≈ 2.5 ms per scan at K = 10^6, ≈1,700× under
  the shipped 4.4 s.

## Kill criteria for the run

- Any selector miss (A1) at σ_a ≤ 1e-3, e ≤ 0.5, either horizon: the widened window as
  defined is dead; the dossier reports the miss and what term covers it.
- The flight answering ~all in-window members (B1): my `hit` reading is wrong — void.
