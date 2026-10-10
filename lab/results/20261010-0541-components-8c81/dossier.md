# Dossier — the kick event's idiot index (lens: components, one component at a time)

## Claim

The plane pays a full rebind (state → orbit solve → cycle compile → new Entry + retired Segment) on **100% of kicks** and a cold t→ψ solve on every state read, so one kick costs 33.3 µs pure (50.4 µs per item whole-universe) against a floor of about 1.5 µs — an idiot index of **≈ 34×** — and the fix is not new physics: it is the already-adopted jet/re-anchor (law.md "Not adopted: a quantized (E, L) memo for kicks", 0.05 compiles per kick) plus phase-carried readouts, neither of which is wired in this tree.

## The component, its owner and its floor

- **Requirement.** Kicks are the engine's only repeated work ("Events: the only places where work happens"; the board: "kicks dominate the engine's cost"). Owners: P14 "no work for no reason, so no ticks… you don't advance a ship tick by tick" and P33 "a body resolves only the influences that are significant at its own scale, and smaller ones enter as an aggregate". A kick's own information is its Δv quanta and sigma-delta carry: 4 integers, 32 bytes.
- **Floor.** Read the state at the kick phase (a crossing-table read: **0.346 µs**, measured), evaluate tide + secondaries on it (a tensor and a few positions; ~0.1 µs of integer arithmetic), add Δv to the carry, and advance the trajectory by the jet with a re-anchor every ≈ 20 kicks (0.05 × (from_state 12.8 µs + compile 9.3 µs) ≈ 1.1 µs amortized — the adopted design's own rate). **Floor ≈ 1.5 µs per kick.**
- **Distance.** Pure resolve measured **33.3 µs**; whole universe **50.4 µs per kick/open/boundary** (`cost_split`, 49 619 items over 3×10¹⁰ ticks). Ratio ≈ **34×** (22× on the pure path). Memory side: one rebind materializes an Entry (176 B shallow + a knots table) and a retired Segment (184 B) — ≳ 360 B and ≥ 2 orders more words than the kick's 32 B of information.

## Evidence (all on this run's tree; Linux x86 cloud, orders of magnitude only)

Machine state: 8 vCPU, load 1.61, 13.8 GB available. Commands (each ≤ 60 s):

```
cargo build --release -p emergent-universe --examples
./cost_split            # baseline pieces (pre-existing example)
cargo run --release -p emergent-universe --example kick_floor
cargo run --release -p emergent-universe --example kick_weight
```

| Measurement | Value |
|---|---|
| Pure kick resolve (`step::process` on the plane's ship 14) | **33.3 µs**, 3000/3000 kicks rebind (**100%**) |
| of which rebind (33.3 − readout 3.35 − secondaries 3.27 − tide 3.35) | ≈ 23 µs (**69%**) |
| `Rebinding::from_state` + `Orbit::compile` (e = 0.01) | 12.8 + 5.4–9.3 µs (e = 0.7: **32 µs**; e = 0.95: 128 µs) |
| `signed_state` (cold binary search over knots + ≤ 72 Newton iterations, each a Gauss–Legendre panel) | 2.83–4.3 µs per call |
| `crossing_state` (direct table read, same type) | **0.346 µs** (8× below) |
| whole-universe overhead over pure resolve (queue + apply + `root_state` after every event) | 17.6 µs = **34%** per item |
| Knots per compiled cycle: e = 0.01 / 0.30 / 0.70 / 0.95 | 6 / 16 / 42 / 86 (B9's bound holds) |
| Distinction weight per kick (Entry 176 B + Segment 184 B, shallow) | ≳ 360 B vs 32 B of information |

`kick()` in `crates/universe/src/step.rs` shows why the rebind always fires: Δv is quantized against the velocity word chosen by `choose_units` to *hold* the state (~2⁻⁶² of v_max), and the per-kick tide Δv sits ~10 orders above that quantum, so `dvq != [0,0]` on essentially every kick. The sub-quantum carry path exists but never triggers at this cadence.

## Predictions (`predictions.md`, written before the run)

- **P1 held:** ≥ 90% rebinds predicted, **100%** measured.
- **P2 held:** rebind ≥ 50% of the resolve; measured ≈ 69%.
- **P3 held:** crossing_state 0.1–0.6 µs predicted, 0.346 µs measured (8×, at the predicted edge).
- **P4 split:** ≥ 32 knots predicted — **true in the belt's regime** (42 at e = 0.7, 86 at e = 0.95) but **false for the probe's near-circular ship** (6; B9's own bound gives ≈ 9). The per-rebind weight claim stands on the measured Entry/Segment sizes.
- **P5 held:** canonical-path overhead ≥ 30% predicted, 34% measured (`root_state`, a view/deadline heuristic, is 6.8 µs of it — paid eagerly after every event).

## What would make it wrong

The floor assumes the re-anchor's 0.05 compiles/kick keeps B5/B12's exactness at the plane's kick cadence; that was graded gold by one checker ("the second never ran"). If correlated kicks break the re-anchor sooner on real scenes, the floor rises toward 33.3 µs and the index shrinks toward 1. Also: my rebind share is a subtraction, not an instruction-level profile (from_state/compile bound it from cost.rs); and ship 14 is one near-circular Home orbiter — eccentric bodies pay more per rebind, so 34× is a *lower* side for the belt.

## Cost of adoption, and fit

No new law, no gate changes: (1) wire the jet/re-anchor (Sonnet's in-flight task) — deletes ≈ 69% of the kick; (2) carry the kick's ψ between kicks of a binding (times step by constant H, so the Newton warm-starts one panel away) or read states at crossing granularity — another ≈ 3 µs; (3) make `root_state` lazy (deadline resolution does not need per-event positions) — ≈ 14% of per-item. Fit: P1 "the cheapest compute is compute not done"; P3 "nothing is evolved that can be derived when looked at"; P13 "errors never compound" (the re-anchor re-anchors before the drift floor, by design). The neighbours were measured, not just the component: the Calendar queue is already at its floor (inline keys, one slot per body, no stale entries); the overhead lives in `apply`, not the queue.

## The lens's blind spot

One component, one machine, one ship: the decomposition says where the 34× lives but not whether re-anchoring every ~20 kicks shifts cost into the catalogue (Entry churn) or the encounters seam, and cloud x86 orders of magnitude hide the M1's cache profile (the knots table is small; the win is the deleted compile, not locality). H_live (b-h-live, queued) measures the same stream's *retention* side; this run measures its *emission* side — they meet at the rebind.
