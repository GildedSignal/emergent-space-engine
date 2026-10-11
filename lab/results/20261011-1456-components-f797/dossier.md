# Dossier — 20261011-1456-components-f797 (lens: first principles, one component at a time)

## Claim

The kick's generator update (the per-fired-kick tube rebind, `Rebinding::from_state` → `Orbit::compile`) runs **9–16× above its measured floor**, and the law's own adopted-but-unbuilt design — the re-anchored jet, law.md "Not adopted: … strong-field reuse is the jet (exact offset plus stored derivatives), re-anchored" — lands within ~2× of that floor; today the plane pays a full Darwin cycle compile on **100% of fired kicks** (measured, fresh harness).

## Bottleneck

Board line 1: "fewer kicks per orbit … kicks dominate the engine's cost". Six runs killed correctors and higher-order splits (the count will not drop); q-cadence and the slack skin work the count from the scheduling side. What nobody had on the record is the **price** of one kick and its floor. This run measures both for the generator component. Expected gain: the generator share of a fired kick drops ~9–16× (belt e 0.6: 52 µs → ~6 µs; e 0.9: 94 µs → ~12 µs); it deletes the per-kick compile and the per-kick `fit_key` root search entirely, and with them the rebind's word-transition double compile (below).

## Evidence

Linux/x86 (8 vCPU i7-4790, load ≈ 1, idle-ish; orders of magnitude only — the integrator re-measures on the M1). Machine state recorded in `bench.txt`'s run log line.

```
cargo run --release -p emergent-universe --example kickbench     # ~8 s total
```

Bench: `kickbench.rs` (copied in this folder; lives at `crates/universe/examples/kickbench.rs`). It uses the plane's own rebind (`emergent_universe::bind::bind`) and the exact compiled readout (`Orbit::state`); scenes from strong field to belt scale. Output in `bench.txt`; both full runs agree within ~10%.

Belt body, periapsis 2^17 M, e 0.6 (33 knots) — the representative case:

| quantity | ns | note |
|---|---|---|
| one readout (`Orbit::state`) | 4 600 | the decode every kick and reader pays |
| `Orbit::compile` alone | 39 600 | 76% of `from_state` |
| `Rebinding::from_state` | 52 200 | what every fired kick pays today |
| `bind` (the plane's rebind) | 115 000 | 2.2×: the word re-expression recompiles, see below |
| kick loop, any dv ≥ 1 quantum | 51 000 | confirms `from_state` is the whole kick's generator cost |
| jet floor, crate `Scalar` arithmetic | 3 340 | (5·knots+3) components × (2 mul + 2 add) |
| jet floor, raw i128 | 380 | hardware floor, ~9× below `Scalar` |

- **Idiot index (this component): 52 200 / 3 340 ≈ 16×** at e 0.6; 13.6× at e 0.9 (94 377 / 6 921); 23× near-circular (15 680 / 667, but absolutely cheap).
- **Design within 10× of the floor:** jet + re-anchor. With the law's 0.05 compiles/kick: 3.34 + 0.05·52.2 ≈ 6.0 µs → **8.8× below today**, i.e. the design sits at 1.8× the crate-arithmetic floor. Conservative bound (anchor every 20 kicks and the derivative tables costing 3× a compile): ≈ 4.7×. At the red-team's measured anchor limit (730 kicks, run 20261006-0346-redteam-df81) the anchor share is negligible: ≈ 15×.
- **100% recompile, fresh harness:** every fired kick at dv = 1, 2^8, 2^16 velocity quanta changes the `OrbitKey` (one scene 99% at dv = 1 quantum) and the exact `ShapeKey` (100%; on all scenes here `ShapeKey` retains the full-precision compactness, so even the radius-free shape key cannot repeat). This independently re-confirms the 5 October memo-artifact correction and extends it to the shape memo.
- **The rebind's word transition doubles compiles:** `bind` = 2.2× `from_state` on every scene, with or without 4× word headroom. Cause: `word_for` (crates/universe/src/bind.rs) sizes the word from `r_max = periapsis/(k−1) = apoapsis/e`, so any fresh binding at a word chosen from the current state re-binds coarser and compiles again; near-circular states inflate `r_max` by up to ~2^46 (k within one Q48 quantum of 1). In steady state the plane's word persists, so this is paid at creations, handoffs and thrust flushes, not every kick — but it is pure waste the jet deletes (no compile, and the table is word-independent). An exactly-circular bind was probed separately: returns `Ok` (no refusal path).
- **Neighbours (the lens's blind-spot check):** a fired kick in the root doll also pays one readout of itself plus one readout per secondary source (`ctx.secondaries` → `state_of` per source per kick, ~4.6 µs each) — for a 5-planet doll that is ~23 µs the jet does not touch. So the **engine-level** gain is the rebind's share of the kick (~65% for that doll) times the component's 9–16× ≈ **2–3× per kick today**, rising to the full 9–16× once sources are read cheaper (a named experiment, below). The readout itself (4.6 µs vs a sub-µs binary-search-plus-Newton floor) is the next component over.

## Predictions

`predictions.md` was written before any timing run. All four held: P1 rebind ≥ 3× readout (11×), P2 100% key change / ≥ 99.9% shape change, P3 compile ≥ 50% of `from_state` (76%; 39% near-circular, where `fit_key`'s exact BigInt path dominates instead — the jet removes that too, being keyed on (E, L) with no root search), P4 jet ≤ 1/10 of `from_state` (1/16).

## What would make it wrong

- The plane's kick count per body is set by cadence and slack; if most kicks on real scenes are sub-quantum and carried (they already cost nothing — the taste log says ~99% fire), the fired-kick price is the whole story. If a future cadence change makes fired kicks rare, this component's weight falls.
- The derivative tables' compile cost at anchor is unmeasured (bounded 1–3× a compile above); if it were ≥ 10×, the design-inclusive gain at 0.05 anchors/kick drops to ~2×.
- The force side (secondary readouts) is unmeasured here; if it dwarfs the rebind, the engine-level gain shrinks toward 1× (the component-level index stands regardless).
- The jet floor assumes eager table update; a **lazy** jet (store (anchor table, ΔE, ΔL), correct at readout) could sit below it, but pays the correction inside every readout's Newton solve — unmeasured, and it is the open design question this run leaves.

## Cost of adoption, and PRINCIPLES

The jet is already the law's adopted design; what adoption costs: (1) per-anchor derivative compilation of the Darwin panels' (E, L)-partials (derivation work, ~1–3× a compile, paid per anchor); (2) memory: ∂/∂E and ∂/∂L per table component ≈ 2× the value table per live kicked body (~5 KB extra at 33 knots) — coarser-precision derivatives (the table's own quantum) would cut this, unmeasured; (3) the exactness story is already adjudicated: error grows C·drift², bounded by re-anchoring (redteam-df81), so principle 13 ("Errors never compound") is kept by construction, and the anchor is the certificate.

Fit: "Compute only surprises. … Nothing is evolved that can be derived when looked at" (P3) — a kick's generator change is two small integers; everything else in today's rebind is re-derivation. "Store the generator, not the generated" (P6). "we just need to have the right representation so that math is trivial" (P18) — the compiled cycle already stores the smooth object; the jet is its tangent transport.

## The lens

The components lens measured one component and its neighbours, but did not run a full plane scenario with the force path instrumented — the rebind's *share* of a real kick is bounded (secondary readouts ≈ 4.6 µs each), not measured end-to-end. It also did not measure the anchor-side derivative compile (no implementation exists to measure). And by design it stayed inside the doll-tube machinery: the Fermi-frame fleet's tide kicks (the lattice core) are a different kick path this run does not cover.

## Grade self-assessment

Silver-shaped as a record (the design was adopted on paper before this run; what is new is the measured idiot index, the floor, the fresh-harness 100%-recompile confirmation, and the word-transition finding), but the measurement is reproducible in one command, all pre-registered predictions held, and the design is adoptable within one well-scoped build step (jet + anchor in `crates/space`/`bind`). The named experiment to gold: instrument a real plane run's kick into (self readout, secondary readouts, force, rebind) and build the jet's derivative compile.
