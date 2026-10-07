# Dossier — run 20261007-0621-scout-6e10 (lens: scout)

## Claim

H_live is a **stock** of three terms, not a flow of "+62 bits per kick": a
chaotic event scars a body once for ≈ 2·log₂(σ_kick/quantum)+4 bits (measured
40.2 at q24, vs 1488 bits for the flow model after 24 kicks — 33× overcount),
a smooth (birth-state-derived) event scars it **0 bits beyond its membership
list**, and the secular carry walk is diffusive (4.5 bits/body total after 12
epochs, 1 bit per resolution doubling); under this ledger 10⁹ belt bodies cost
≤ 0.6 GB of secular stock + 37 MB per chaotic-churn epoch, and the only term
that can fill 8 GB is war, at 6–16 B per simultaneously distinguished body
(3–8×10⁸ bodies at 5 GB).

## Bottleneck

"Distinctions created per game-second (H_live): they, not the body count,
decide whether 10⁹ fit in 8 GB; **not measured yet**" (HANDOFF, risks; board
focus list). law.md's allocator line assumes "+62 bits per kick, −60 per
reabsorption". Expected gain: replaces a wrong-unit budget line with measured
terms, deleting the risk of sizing shipmem (and B18/B18b's floor rule) against
a 33×+ overcount. It also types B18b's "churn of 10⁻² per epoch": the churn's
*kind* (smooth-field vs encounter-chaotic) decides 0 vs 40 bits per scarred
body — more than the churn rate does.

## Evidence (all commands ≤ 60 s; deterministic, seeded; ≤ 590 MB RSS)

```
cd lab/results/20261007-0621-scout-6e10
python3 h_live_ledger.py      # 11 s -> h_live_ledger.json (+ run_log.txt)
python3 stock_vs_flow.py      # 2.4 s
```

Belt = B18b's scene (2²⁰ bodies, banded a, Rayleigh e, uniform angles) under
Laplace–Lagrange secular flow from a Jupiter, integer quanta at measurement
boundaries; 12 epochs × 10 orbits; churn 10⁻²/epoch. Entropies are
differential at the quantum (validated: chaotic kick measure 40.2 bits =
analytic 2·log₂(σ/q)+4.1; empirical estimator ceilings at log₂ n were caught
and avoided). Battle = 2¹⁴ fleet born on one orbit (0 bits/member), Poisson
contact kicks (shared drift + slot-linear + per-member chaos).

| Quantity | Measured |
|---|---|
| Control: belt, no perturber | 0.0 bits, exact |
| Control: battle, zero kicks (generator coords h,k) | 0.0 bits |
| Secular carry walk (program-with-t, integer increments) | 0.75 → 2.11 bits/col over 12 epochs; 4.46 bits/body total; 0.0 / 2.1 / 10.1 bits at q16/q24/q32 |
| Churn kick, smooth in birth state (event program + membership) | **0.0 bits** beyond membership f·log₂(1/f)+2f |
| Churn kick, chaotic (encounter-phase-dependent) | **40.2 bits/kicked body** (irreducible; = analytic bound) |
| Churn stock accumulation | 0.29 bits/member/epoch → 37 MB per 10⁹ per epoch; scarred fraction → 1 as 1−(1−f)^E (asymptote: the materialized belt, 45.5 bits/body = 5.7 GB at q24, 2.7 GB at q16) |
| Static birth program (no repack, no t) — wrong form | 45.5 bits/body at 12 epochs |
| Battle residual after best-fit program | 47.3 / 48.9 / 50.6 bits/member at λ=2/6/20 kicks (6.1 B) vs 16 B tube |
| Same state stored as (e, ϖ) instead of (h, k) | 44.2 bits/member **for an unscattered formation** (coordinate lesson) |
| Repeated kicks on the same body (stock vs flow) | 40.2 → 44.8 bits over 24 kicks; flow model says 62×24 = 1488 (33× overcount, unbounded) |

## Predictions

`predictions.md` was written before the decisive run. What happened:
- **P1 ✓** (carry ≤ 2 bits/epoch: 2.1 bits *total* after 12 epochs, diffusive, program-with-t works).
- **P2 ✗ in its literal form**: < 0.5 bits/body after 1000 orbits fails — chaotic churn accumulates as 0.29 bits/member/**epoch** (10-orbit epochs) because scarred bodies never exactly return (law.md's reabsorption fires only on exact return); after ~100 epochs ≈ 40% of a 10⁹ belt is scarred ≈ 2.2 GB at q24. The belt is free **only** with a per-population scar quantum (q16: 21-bit scars) or body recycling.
- **P3 ✗ (my kill criterion fired)**: battle residual 48.9 < 50 bits → war recapture works; no strict tube cap. War members cost min(program+scars, tube) = 6–16 B; cap ≈ 3–8×10⁸ simultaneous war-distinguished bodies at 5 GB. I delete the pre-registered "war cap ≈ tubes at 16 B" claim.
- **P4 ✓** (33× at 24 kicks, growing).

## What would make it wrong

- The replica is 2-body secular + invented kick distributions. Real encounter
  kicks sit **between the two measured poles**: planet flybys are largely
  event-programmable (their strength depends on arrival phase, which the birth
  program + t derive), ship-combat encounters are the chaotic pole. The poles
  are measured; the mix per workload is not.
- The secular model is non-resonant by construction (Laplace–Lagrange);
  resonant pumping (which killed averaging, r4/r9) can scarify belts faster
  than the 0.5%/epoch chaotic pole here.
- Differential entropy assumes near-Gaussian residuals (validated on the
  analytic kick bound); heavy-tailed kicks would be underestimated.
- One rounding per epoch; the law's real cadence changes the carry walk only
  by its √(roundings) count — same order.
- The plane's own numbers (the b-h-live build, B18b's typed churn cases) are
  the gold-standard version of this ledger; this replica is the falsifier.

## Cost of adoption, fit with PRINCIPLES

Adoption: rewrite law.md's allocator line from "+62 bits per kick and −60 per
reabsorption" to the stock ledger above; type B18b's churn case (one
smooth-field churn, one chaotic churn — today "churn" is untyped and the type
decides 0 vs 40 bits per scarred body); shipmem already has the mechanism
(hot map + seal + compact with repack-at-half-blocks), so no new store code is
implied by the measurement. PRINCIPLES 24 ("the memory floor is information"),
3 ("compute only surprises" — store only surprises: the smooth pole costs
membership only), 19 (the flow line was the wrong representation for a stock
question), 16 (the scar quantum per population is a quantization choice, and
it sets the belt's asymptote: 5.7 GB at q24 vs 2.7 GB at q16).

## Best candidate from other fields (the lens's deliverable)

The store shape shipmem already has **is** the cross-field best answer; what
the scan adds is each field's missing rule, now measured:
1. **Delta-snapshot netcode** (Quake 3 delta compression; Source/Overwatch
   snapshot-vs-baseline): unchanged entities cost ~0; changed entities cost a
   delta against their baseline; baselines re-key lazily. = program + hot map
   + scars; the re-key rule is compact()'s repack-at-half-blocks. (Mechanism
   widely documented; specific per-title numbers UNVERIFIED.)
2. **Gorilla/Prometheus TSDB** (verified via search, 7 Oct): delta-of-delta +
   XOR compresses smooth per-stream state toward its innovation entropy — the
   carry walk measured here is exactly its regime (≈0 bits until a value
   crosses a quantum).
3. **Video-codec mode decision** (I-frame vs P-frame by rate-distortion cost):
   shipmem's exact-byte-count OR between program+scars and packed blocks is
   the same rule; adds the rekey trigger, already present.
4. **LSM compaction in idle time**: the write path stays O(1) append (hot
   map), folding happens in background (seal/compact) — maps to the frame
   budget's idle frames (principle 17).
5. **MVCC vacuum**: retention decided by consumers — the analogue (innovations
   outside every live light cone are replay-only) is not needed for the live
   stock but bounds the replay log. UNVERIFIED as a direct mapping.
No field stores a billion *individually-evolving* bodies (games aggregate;
MD accepts loss); the poles/ledger above are the transferable core, not a
ready-made store.

## The lens: what it may have missed

The scout's instinct was to find a better mechanism elsewhere; the run says
the mechanism is already right and the *ledger* was missing. Blind spots that
remain: dense-regime workloads (a real Fermi-frame battle at contact density,
not Poisson kicks); the three-body/resonant regimes this secular replica
cannot express; and GPU-side costs of Elias–Fano membership reads, which this
CPU replica never touches. Incidental engineering lesson recorded: the
quantized state must live in quanta end-to-end — a float rescale mixed units
and wrapped int64 after two epochs, and only the zero control caught it.
