# Dossier — the rebind after a kick: 270× above its floor, and the jet that closes it

## Claim

The rebind (the state re-expression every kick pays) is ~270× above its information-theoretic
floor — every kick fits a fresh orbit and compiles a fresh shape (0% memo hits, 2000/2000
distinct keys measured) — and the adopted-but-unmeasured jet closes it to within ~10× of the
floor, **provided the period derivative is carried** (without it the jet dies at kick 1–4,
measured); the safe re-anchor interval on the plane's own machinery is 38 kicks (correlated,
δv/v = 10⁻⁶, 10⁻⁶ floor), 510 for a random walk, and the error law is clean C·D² with
C ≈ 0.8 across two kick sizes, two regimes and both directions.

## Bottleneck

Board live question #1: "kicks dominate the engine's cost." The lab's six runs killed
correctors and higher-order splits (fixed cadence, cheaper per kick was said to gain only 8%);
the lever left inside a kick is the rebind. Baseline here (this Linux runner, shared 8 vCPU —
orders of magnitude): a plane kick's resolver step is 58 µs median (plane-made bodies), 366 µs
(fleet members); `Rebinding::from_state` alone is 25–27 µs weak field, 36–40 µs strong.
Expected gain: ≥ 20× on the engine's dominant event; deletes the per-kick fit and the per-kick
compile (both move to re-anchor events, 1/38 to 1/510 of kicks).

## Evidence
- From the repo root: `cargo build --release -p xtask` (target dir `$CARGO_TARGET_DIR`), then
  `$CARGO_TARGET_DIR/release/xtask universe --kick-bench --seconds 30` → `kick-bench-linux.json`:
  kick median 57.9 µs (made), 365.6 µs (leavers), `exact_hit_rate` 0.0, `quantized_hit_rate` 0.037.
- `cd work/jet-probe && cargo build --release --offline && ./…/jet-probe` → `jet-probe-out.jsonl`
  (truth = `Rebinding::from_state` per kick, the plane's exact path; J0 = anchor table only;
  J1 = anchor table + first-order FD correction in key space + exact re-time;
  J1t = J1 without the time anchor correction).

Numbers (weak field r = 2²⁴ M, e ≈ 0.28, cadence 8/orbit, probe at 4 phases 1–1.75 periods
after each kick; error = max relative radius error vs the exact rebind):

| case | e0 (no corr.) crosses 1e-6 | J1 crosses 1e-6 | J1 crosses 1e-5 | J1t crosses 1e-6 |
|---|---|---|---|---|
| correlated δv/v=1e-6 | kick 1 | **38** | 112 | 2 |
| random-walk 1e-6 | kick 1 | **510** | never (e(2000)=3.9e-7) | 1 |
| correlated 1e-7 | kick 3 | **350** (= 38×10) | 1198 | 4 |
| strong field r = 2¹² M, 1e-6 | kick 1 | **38** | 110 | 2 |

- Error law: crossings scale as 1/δ (38 → 350 at δ/10) and walk/corr = 13× ⇒ error ∝ (Σδ)²,
  C ≈ 0.7–0.8 (from C·(n·δ)² = floor). The red-team's "730 quantum kicks" used a smaller
  quantum (mine is δv/v = 1e-6 ⇒ δ(E−1)/(E−1) ≈ 4×10⁻⁷); the transferable number is C, and
  both are consistent with D².
- Cost split (this box): from_state 25–27 µs = compile 16–17 µs (≈ 65%) + fit/anchor ≈ 8–10 µs
  + residual; decode 3.1 µs; the jet's correction arithmetic (5-decode read minus decodes)
  ≈ 0.6 µs. Every one of 2000 kicks produced a distinct shape key (compile is unavoidable per
  kick in the current path).
- Floor: the kick's surprise is (δE, δL), closed-form integers (δE = v·δv, δL = x×δv); the
  fit-free update is ~two dozen integer ops ≈ 0.1 µs. Idiot index = 27 µs / 0.1 µs ≈ **270**
  (M1: 24 µs ⇒ ~240).
- Design within 10×: jet + re-anchor every N*. At the 10⁻⁶ floor N* = 38 (correlated worst
  case): 27 µs/38 + 0.6 µs ≈ 1.3 µs/kick (21× cut). At the 10⁻⁴ floor — the memo's own shape
  quantum is 2⁻¹¹ ≈ 4.9×10⁻⁴, so 10⁻⁴ is defensible against B1/B2/B5 (behaviours at 1%, 0.1%) —
  N* ≈ 350 (D² extrapolation, bracketed by measured crossings at 112/1e-5 and e(2000)=7.7e-4):
  ≈ 0.7 µs/kick (39× cut), within ~7× of the floor. The law text's 0.05 compiles/kick (re-anchor
  every 20) is sound and slightly conservative against the measured 38 at the strictest floor.

## Predictions

`predictions.md` was written before the decisive run. Held: compile ≥ 60% (65%); J0 dead in
1–10 kicks (1–3); J1 D² with walk ≥ 4× correlated (13×); the package within 10× of floor at
the re-anchor interval. Missed: the held-out strong field does **not** shrink N* (38 = 38; I
predicted ≥ 50 and a shrink — the table's curvature C is field-independent here); and I
underestimated how load-bearing the time anchor is: J1t (no period correction) dies at kick
1–4, so the memo's ∂Δt/∂E, ∂Δt/∂L are mandatory, not an optimization.

## What would make it wrong

The jet's error was measured with the exact per-kick re-time (J1); the real jet carries the
period drift from the memo's stored derivatives, which removes the same first-order terms but
leaves cross-terms of the same order as C·D² — so N* is an estimate, not a bound, until the
derivative-corrected jet is measured (one more experiment: the same harness with ∂Δt carried
instead of the oracle fit). Second: my kick stream is one body in one doll, cadence 8, e 0.28;
a resonance or a near-handoff body has larger C. Third: timings are a shared cloud vCPU —
orders of magnitude only; the integrator re-measures on the M1.

## Cost of adopting

`crates/space`'s memo must store ∂/∂E and ∂/∂L of (Δφ, Δt, Δτ) per band (law.md line 14
already specifies them; they are not yet in the tables), and `crates/universe`'s `rebind`
gains a jet path with the re-anchor certificate "accumulated |δE|,|δL| since anchor >
√(floor/C)·scale" decided in integers at the body's own events (fits the tie rule). No gate
changes; B5's exactness is untouched (E, L stay exact in the register; only the derived
readout carries the jet's bounded, re-anchor-reset error — oscillatory, not compounding,
which is the error type the law wants).

## Fit with PRINCIPLES

- "you don't advance a ship tick by tick you just map where it wants to go" (#14): the kick's
  map is two integers; the refit is work for no reason.
- "Compute only surprises… Nothing is evolved that can be derived when looked at" (#3): the
  orbit's response to a small impulse is derived from derivatives already compiled, not
  recomputed.
- "bandaids are basically fixes resulting due to a poor representation" (#19): a per-kick
  compile is the wrong representation — the tube is a compression of a worldline, and
  compressions update differentially.
- "Errors never compound" (#13): the jet's error is bounded per anchor window and resets at
  re-anchor (measured D² within the window, not across windows).

## The lens

The components lens made me measure one component's floor; the neighbour it exposed is the
**decode itself at 3.1 µs** (~30× above a table-read floor) — it is paid by every readout
(view, encounters, judges), not just kicks, and `b-readout-cost` owns it; my jet arithmetic
(0.6 µs of `Scalar` ops) would also drop several-fold in plain fixed-point. I did not measure
a resonant or near-handoff kick stream (C there may be larger), and the checker should treat
N* = 38 as this harness's number, not a law constant.
