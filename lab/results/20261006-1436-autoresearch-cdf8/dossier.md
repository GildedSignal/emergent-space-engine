# Dossier — run 20261006-1436-autoresearch-cdf8 (lens: autoresearch)

## Claim

An exact radius-band pre-filter before the tube decode would cut the player's encounter check on
a sparse belt by 3.4× at zero output change — but it is **unsound on the plane as the data model
stands**, because a secondary's tube is the pair's relative orbit (its readout can sit below its
key's periapsis), so the change is reverted and the run delivers the falsified premise, its exact
boundary, and a bit-identity bench for the finder instead.

## Bottleneck

The plane's measured bottleneck #4 ("the player's encounter check costs 190 µs per item"; the
Binet-cone seam is the intended successor). Profiled here: 91–94% of an item is the tube decode
(`other.cartesian(t)`, the Kepler solve in exact `Scalar`), 20–34 ns is `binding_at`, the rest is
the integer predicate. Expected gain order: 3–10× on sparse scenes; what it would delete is most
decodes per frame for far bodies — the same "compute only surprises" the Binet cone buys
globally.

## Evidence

All commands ≤ 60 s, Linux x86 (orders of magnitude only; the integrator re-measures on the M1):

```
cargo run --release -p emergent-universe --example enc_bench -- A 48   # and B, P, HO1, HO2, HO3
```

- Baseline (reverted config = shipped code), this run's files:
  - `baseline.txt`, `heldout-final.txt`: A 1483–1515, B 3524–4284, P 1242–1249 ns/item (median);
    decode share 91–94%. HO1 (4001 bodies) 1515 ns/item — flat in N.
  - Every line carries `outputs_identical=true` (the bench's replica of the original loop vs the
    shipped one; 18,585 encounters on B match bit for bit, digest `2adf5e51…`).
- With the filter (code saved in `round1-filter-encounter.rs`; rebuilt from it to re-measure):
  - A: 445 vs 1495 ns/item (3.4×), 98% of items rejected before decode, outputs bit-identical.
  - B: 3880 vs 3450 (+12%), HO3: 3807 vs 3384 (+8%) — nothing rejected when eccentric bands
    overlap; the band arithmetic (~10 `Scalar` ops ≈ 400 ns/item) is pure overhead there.
  - P: `outputs_identical=false` — 47 vs 69 encounters, 0 vs 19 contacts. The in-loop self-check
    printed the violating item: `j=16 r_lo=1.4126e9 x_hi=1.2426e9 margin=1.0765e8
    actual_hit=true` — the readout sits ~1.7e8 *inside* the key's periapsis.
- Machine state during the runs: loadavg 1.4–2.5 (shared 8-vCPU runner), no thermal events
  logged; timings are medians over 48 sweeps with alternating call order (the first caller warms
  the cycle memo — a one-sided A/B inflated the second caller ~3×; both orders are interleaved).

## Predictions

`predictions.md` was written before the decisive run. What happened:

- P1 (≥80% rejected on A, ≥5× ns/item): 98% rejected; 3.4× — direction right, magnitude short
  (the per-rejection `Scalar` arithmetic sets the floor, ~400 ns).
- P2 (clustered B within +15%): +12.3% — held.
- HO1 (flat in N): 1515 vs 1483 — held. HO2/HO3: measured but moot after the kill.
- The kill criterion ("any output bit changes ⇒ revert") fired on P. Held out honestly: the
  failure was on the tuning-adjacent plane scene, not a held-out one; the held-out scenes all
  stayed bit-identical, which is exactly why the plane had to be in the loop.

## What would make it wrong

The unsoundness rests on one measured item class (secondaries). If those bindings are instead
misbound (a real engine bug — a readout below periapsis should be impossible for a tube about the
doll's origin), the filter's premise is fine and the bug is the finding. Either way the cost
claims stand only for test-particle tubes. The 3.4× ceiling could be beaten by an integer-only
band test (no `Scalar` division/sqrt per item) or by caching bands per binding — untested.

## Cost of adopting, and fit with PRINCIPLES

Nothing to adopt in the engine (reverted; the tree keeps only the bench). The next step for
bottleneck #4 is cheap: mark which bindings are centred on their doll's origin (test particles,
not secondaries), gate the filter on it, and re-run this bench — the pre-registered kill then
cannot fire on P again. That is "compute only surprises" (PRINCIPLES 3: "Nothing is evolved that
can be derived when looked at") applied to the finder, one flag away. Fit check against the
board: encounters work is active (r8 v4, the phase-neighbour certificate); this is the per-item
constant on the plane's own seam, not a competing discovery method.

## The lens

Autoresearch's blind spot showed up as promised: a local search tuned the filter on belt-like
scenes and the plane broke it — the structural change that beats my best is the one the board
already chose (the Binet cone / phase-neighbour certificates find *which* pairs to check; a band
filter only makes the checked pairs cheaper). This run's value is the instrument and the
falsified invariant, not a speedup.
