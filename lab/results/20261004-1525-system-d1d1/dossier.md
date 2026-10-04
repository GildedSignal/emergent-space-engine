# Dossier — the kick's rebind and the cycle memo are one mechanism

## Claim

The plane pays a fresh exact orbit compile on **every kick** (`Work::kick` → `Rebinding::from_state` → `Orbit::compile(key)`, exact 48-bit key) for work the law's own declared state — tubes keyed by the **quantized** (E, L) memo (`law.md` State; `QuantizedMemo`/`MemoCode`/`ShapeMemo`, already in `crates/space`, **wired to nothing**) — shares: wiring the memo in cuts the rebind 3.7× on quadrature orbits, bit-exact at the event, and the measured quantized-key change rate per tide-like kick is ≈0, which makes that key the rebind's certificate (recompile when the key moves, not when a kick lands).

## Bottleneck

Board focus 1 ("fewer kicks per orbit"; kicks dominate the engine's cost) and HANDOFF bottleneck 3 (a kick costs 29 µs on the M1, 15 of them in "rebinding fit and compile"). This run says the premise is half wrong: the lever is not (only) kick *count* but kick *cost* — the memo already exists and is unused; expected gain ≈ 4× per rebind now, an unbounded multiple once the fit itself is deleted (below). It lets us delete the per-kick compile path outright and de-prioritise `q-correctors`.

## Evidence

Machine: cloud container (Linux x86, 2 vCPU, shared) — orders of magnitude only.

- Baseline, the plane's own deterministic kick replay (pure resolver, no allocator):
  `cargo run --release -p xtask -- universe --kick-bench --seed 7 --seconds 4`
  → kick median **40.4 µs**, p99 66.9 µs, 23 samples, 0 refusals.
- The decisive experiment — `cargo run --release -p emergent-space --example memo_bench`
  (tide-like kick streams, 64 kicks/radial cycle, zero-mean + 1% secular; every kick checked
  against the exact left inverse `reconstruct() == input`, both paths, all streams):

| stream (key) | exact rebind med/p99 µs | memoized med/p99 µs | readout med µs | MemoCode change/kick | memo hit | residual h1/h2 (60-bit word quanta) |
|---|---|---|---|---|---|---|
| weak planet e=0.05, kicks 2⁻²⁴ | 11.4 / 19.4 | **7.8** / 10.8 | 3.3 | **0.000** | 1.000 | flat (323861692 / 323861670) |
| weak planet, kicks 2⁻²⁰ | 11.5 / 19.3 | 7.8 / 11.6 | 3.3 | 0.190 | 0.999 | flat |
| ecc planet e=0.6, kicks 2⁻²⁴ | 29.2 / 38.5 | **7.8** / 10.5 | 3.3 | **0.000** | 1.000 | identical |
| ecc planet, kicks 2⁻¹⁶ | 29.3 / 38.9 | 8.0 / 29.5 | 3.4 | 0.667 | 0.988 | flat |
| strong ship e=0.6 (quadrature), 2⁻²⁴ | 31.1 / 52.3 | **8.3** / 16.2 | 3.3 | **0.000** | 1.000 | flat |
| flyby e=2 (passage) | 19.2 / 28.6 | 18.8 / 27.8 | 2.3 | n/a (refused) | **0.000** | flat |

  Reads: (a) the compile is 73% of a quadrature rebind (29 → 7.8 µs) and 32% of a weak-branch
  rebind (11.4 → 7.8); (b) at tide-like kick sizes the quantized key **never changes** (4,000
  kicks, one memo cell, one shape held in memory) — the orbit's information production per kick
  is zero at 12+12-bit resolution; (c) the residual is **bounded**, not drifting: first half vs
  second half max identical or flat on every stream (P4's error-type check); (d) both paths
  reproduce the bound state **bit for bit** on every one of the 22,000 kicks (asserted, would
  have panicked); (e) passages get nothing (hit 0.000): `MemoCode::encode` refuses non-periodic
  keys, so flybys always compile — the memo cutover's hard case, measured.
- Patch footprint: `crates/space/src/binding.rs` adds `Rebinding::from_state_memoized` (+ shared
  `finish`), the declared-law path only; nothing existing changed. `cargo test --release -p
  emergent-space` passes unchanged (the patch is additive).

## Predictions

`predictions.md`, written before the decisive run. P1 held (100% ≥ the 90% asked; eccentric
strong-field 100% ≥ 50%). P2 held on the quadrature branch (73% ≥ 50%), weaker than claimed on
the weak branch (32%). **P3 held-failed**: the cutover is 3.7×, not 10× — the fit (algebraic
inversion + bisection + `at_radius` panel search + `atan`) now dominates at 7.8 µs; the 10×
needs the fit gone, which is the certificate step below. P4 held (residual flat). P5 held
(flybys unhelped, by construction and by measurement).

## What would make it wrong

- The cutover changes the law's bits by design (worldlines follow the quantized orbit between
  events — `law.md`'s own State says the tube keys the quantized memo; today's plane is the
  deviation). **The behaviour gates must re-freeze on it**: B5 (shape over 10⁴ cycles), B12
  (Jacobi), B14 (Hill), and the universe digests. If any degrades, this is a bandaid, not a
  unification, and I kill it myself.
- The certificate step (recompile only when the quantized key moves; the kick becomes readout +
  integer residual add ≈ 3.3 µs now, less when `decoded_event` is specialised) has one named
  risk: phase staleness over a held window (the held tube's period is the old orbit's). The
  case that could break it: high-eccentricity orbits kicked hard (codeΔ 0.667 at 2⁻¹⁶ says the
  window collapses) and mean-motion resonance, where conjunction phase must be kept
  (`law.md` Events) — there the rebind must stay per-conjunction, which is fine: it is the key
  change that pays, and the key changes exactly then.
- Adoption cost: one wire (`QuantizedMemo` into `crates/universe`'s bind path, thread-local or
  in `Ctx`), digest re-freeze, gate re-run. Within one step.

Fit with PRINCIPLES: principle 3 — "Nothing is evolved that can be derived when looked at"; the
memo derives the orbit from a key the kick almost never moves. Principle 6 — "Store the
generator, not the generated": the compile regenerates what 12+12 bits already identify.
Principle 19 — the plane reimplementing its law's declared state while the memo sits unwired in
the same crate is the "fix signals the wrong representation" smell, in the other direction: the
representation was right and was not used.

## The lens

The whole-system lens looked at structure and arithmetic, not behaviour: no B-gate was re-run
with the cutover (the plane's own gates judge it). Cloud timings are one machine, orders of
magnitude only (principle: the integrator re-measures on the M1). What it may have missed by
staring at the kick: whether `q-correctors` (fewer kicks) and this (cheaper kicks) multiply or
collide — if a kick costs ~3 µs, 64/orbit is already ~0.2 ms per body per orbit and correctors
lose their top ranking; that reorder is the integrator's call, not mine. One substantive result:
the memo exists, is exact, and is unwired; the cheapest next experiment is the wire plus B-gates,
not a new mechanism.
