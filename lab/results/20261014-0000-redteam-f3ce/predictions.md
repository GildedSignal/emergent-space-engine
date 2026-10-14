# predictions.md — 20261014-0000-redteam-f3ce

Written before the decisive run. Target: representation.md §2 line 60 — "There is one error
budget: at most one floor unit per event, carried forward so that it never compounds" —
and its shipped mechanism, the contact carry of `es-lattice-relativistic-v1`
(`crates/lattice/src/relativity.rs::resolve_law`): the pair's owed carry is
`owe[a]+owe[b]`, the chosen candidate pair minimises |owed+e|², the whole error joins the
*lower index* body, and the higher-index body's carry is never rewritten in that contact
(the highest-id body can never change its carry at all).

## The falsifier

`cargo run --release -p emergent-lattice --example rt_carry -- <arm>` (≤ 60 s total):

- `gas-cold` / `gas-hot` / `gas-mixed`: 200-body gas in a box, law v1, T = 6·10⁴ chronons,
  5 seeds each (cold: β ≤ 0.01; hot: β ≤ 0.7, equal masses; mixed: β ≤ 0.9, masses
  1..1000 log-spaced). Checkpoints at t = 10^(2..4.78) in ⅓-decade steps.
- `label`: a 1000:1 mass pair colliding repeatedly in a box, 10 seeds × 2 id assignments
  (identical physics, ids swapped), T = 4·10⁴.
- `perm`: a 32-body gas, 5 seeds × 2 (ids pseudo-randomly permuted), T = 2·10⁴.

Instrument self-tests printed first: the exponent estimator reads α ≈ 0.5 on a planted
√t sequence and ≈ 0 on a saturating sequence (the negative/positive control pair).

## Frozen kill bars (the premise "never compounds" fails if)

- the median-seed running max of per-body |residual| grows with exponent α ≥ 0.2 over the
  last decade in any gas arm (the lab's frozen b12 α bar), or
- |Σ residual| / kinetic energy > 1% at the end of any arm.

## Predictions (the cases I have not tuned on)

1. **Ledger control (must hold exactly):** total 4-momentum energy E(t) − E(0) = Σ residual
   at every checkpoint, every arm, every seed. If false: a real engine bug, reportable.
2. **Cold gas:** per-body |residual| saturates (α < 0.1); |Σres|/E_kin < 10⁻⁴.
3. **Hot equal-mass gas:** still bounded, α < 0.2, larger band than cold.
4. **Mass-mixed hot gas (my genuine uncertainty — the run decides):** I commit to
   α ≥ 0.2 at the median seed in this arm: the carry diffuses across the contact graph
   (each contact rewrites the lower body's carry to ≈ −partner's carry + e, and e can only
   correct a couple of quanta), so some body's |residual| should walk past the per-event
   band. If all three arms saturate instead, the premise **survives** and I report that
   with numbers.
5. **Label, first contact:** identical outgoing velocities under both id assignments
   (control — the exact reflection and the per-body candidates are label-symmetric at
   zero carry).
6. **Label, later contacts:** the two labelings diverge in ≥ 1 of 10 seeds (the carry parks
   on a different physical body), first |Δk| ≤ 4 velocity quanta, digests differ by T;
   both labelings' Σresidual stay within the same band as each other (the ledger's *home*
   differs, not its size).
7. **Permutation:** digests differ; first velocity divergence ≤ 2 quanta.
8. **Held-out seeds 11–15 (gas-mixed, never used for tuning or calibration):** same α
   class (both sides of 0.2, if split, counts against prediction 4).
