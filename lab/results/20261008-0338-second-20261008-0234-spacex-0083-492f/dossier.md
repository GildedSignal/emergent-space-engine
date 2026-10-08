# Dossier — the jet built and measured: 19.7 µs vs 75.9 µs per rebind (3.85×), 3.0× on the whole kick, errors ~10⁻¹² at C·drift² with on-scene C ≈ 2–3.3

Run: 20261008-0338-second-20261008-0234-spacex-0083-492f, lens: second author on
20261008-0234-spacex-0083. Linux x86 cloud box (8 vCPU, 15 GB, quiet); orders of magnitude only,
per the lab rule.

## Claim (one sentence)

The silver run's named gold experiment is done: the law's minimal jet (per body, the stored
exactly-compiled shape plus a derivative-offset table priced by one extra quadrature sweep, a
first-order correction of the knot tables at each kick, and a re-anchor bound) built additively on
the shipped integer law **cuts the kick's rebind from 75.9 µs to 19.7 µs median (3.85×) and the
whole resolver scope from 96.8 µs to 32.0 µs (3.0×)**, with the jetted trajectory's error against
the exact rebind at 10⁻¹⁴–10⁻¹² (period, proper period, radius a quarter-cycle out), following
**error = C·(Δgap/gap)² with on-scene C ≈ 2.0–3.3 median** (p90 11–26; the red-team's float 1.88
replaced by integer-law measurements), so the 10⁻⁶ floor is crossed only at drift ≈ 5×10⁻⁴ —
about 3×10³–10⁴ correlated kicks at this scene's measured per-kick drift (1–2×10⁻⁷), with the
re-anchor price measured at 29.5 µs and zero re-anchors firing in any ≤ 55 s window — so the
original claim **holds, with the honest end-to-end number now 3.0×, not the 4.4× ceiling** (the
jet's own per-kick work — corrected-shape build, correction multiplies, decode — costs ~10 µs,
not the ceiling's 0.46 µs; trivial reuse stays worthless, 10/663 kicks).

## Bottleneck

The same one the silver run named (board focus 1, cheaper events): 63% of every kick is a fresh
Darwin compile whose quantized content changes by less than one part in 4096 per kick. This run
turns the priced ceiling into a built artifact and a measured number, which is what adoption
needs (the integrator cannot adopt a ceiling).

## Evidence

All commands ≤ 60 s (bench walls 0.4–1.5 s), from the repo root, after `git apply
lab/results/20261008-0338-second-20261008-0234-spacex-0083-492f/work/my-run-patch.diff` (125
lines: new `crates/space/src/orbit/jet.rs`, new `xtask/src/universe/jet2.rs`, additive
`Rebinding::from_state_with`, `mod jet`/`pub use` + the 0234 run's two visibility lines, additive
`--jet2`/`--bound` dispatch — **no shipped line's behaviour changes**; `--kick-bench` stays alive,
unlike the 0234 patch) and `cargo build --release -p xtask` (zero warnings):

- `xtask universe --kick-bench --rtf 100 --seconds 10` → `kick-bench-regen.json`: digest
  `13cfe88b452d…`, 97.68 µs median, 682 samples, 663 cycles, 45 quantized shapes, exact hit 0.0 —
  the silver record regenerates on the patched tree; the universe is provably unfed (same digest
  in every jet2 run).
- `xtask universe --jet2 --rtf 100 --seconds 10 --bound 1.5e-4` twice → `jet2-timed-r1/r2.json`:
  full 96.8/97.2 µs, exact_bind 75.8/75.9, **jet_bind 19.7/19.7**, resolver sum (readout+forces+
  jetted rebind) **32.0/32.0**; counters and every error/C value **bit-identical across the two
  runs** (B8); parity control 42/42 bit-identical (`from_state_with(Orbit::compile)` ≡
  `from_state`); refused 0; 663 jetted reads, 19 passage kicks (compiled, as the law keeps them),
  0 law fallbacks; 45 anchors, all at the bodies' own record shapes (0 fresh compiles), 29.5 µs
  each, amortizing 1.95 µs/kick in-window; period/proper/radius errors median 1.5×10⁻¹⁴,
  1.5×10⁻¹⁴, 1.1×10⁻¹⁵, p99 6.1×10⁻¹² / 6.1×10⁻¹² / 1.4×10⁻¹²; advance error 0.
- `xtask universe --jet2 --rtf 100 --seconds 30 --bound 0` → `jet2-drift-30s.json` (never
  re-anchors): drift p99 3.9×10⁻⁶, period error p99 2.7×10⁻¹¹ — five orders below the floor at
  the scene's own drift; **C median 1.97** (p90 11) over 639+ in-range samples; n* ≈ 2.8×10³
  kicks from the on-scene step distribution.
- Adversarial seeds (`--seed 3`, `--seed 7`, 10 s): rebind 68.7→17.8 (3.86×) and 52.6→16.7
  (3.15×); resolver 3.1×/2.6×; errors p99 ≤ 1.1×10⁻¹²; C median 3.3 on both.

The measured decomposition of the 19.7 µs jetted rebind: the fit/decode/residual rest (~9 µs,
unchanged), the corrected-shape build + first-order correction + `from_shape` (~10 µs — the
per-kick jet work the ceiling priced at 0.46 µs), and the p99 (375.8 µs) sits at the same spikes
as the exact rebind's p99 (388.6). Steady-state amortized anchors at the measured cadence:
(61 µs compile + 29.5 µs pricing)/~3000 kicks ≈ 0.03 µs/kick, invisible next to the 10 µs of jet
work.

## Predictions

`predictions.md` written before the record runs (after debug smokes that fixed a knot/diff
misalignment and a factor-2 in the correction; both disclosed above). Held: P1 (rebind ≥2×:
3.85×), P2 (resolver ≥2.1×: 3.0×), P3 (C in [1, 50]: 2.0–3.3; 30 s errors below the floor:
2.7×10⁻¹¹), P4 (controls: 0 mismatch, 0 refused, digest identical, `--kick-bench` regenerates),
P5 (45 record anchors, 0 fallbacks, passages 2.8%, pricing 20–40 µs, no re-anchor in-window),
P6 (bit-identical reruns). Adversarial held. No kill criterion approached: the jetted rebind is
0.26× of the exact rebind, not ≥0.6×.

## What would make it wrong

- The jet serves only the weak branch (ShapeKey compactness zero — the plane's entire
  population): the strong-field jet needs the q dimension of the derivative table and is
  **unbuilt and unpriced**; passages (2.8%) keep their compile. A strong-field-heavy scene would
  re-rate the speedup toward 1×.
- No re-anchor ever fires in ≤ 55 s windows (the scene's drift is ~10⁻⁷ per kick); the re-anchor
  path's steady-state cost and its fired behaviour are priced by arithmetic from the measured C,
  drift steps and anchor times, not observed as an event. The bound (1.5×10⁻⁴) was set from C's
  p90; a body with C ≫ p90 would breach the floor before re-anchoring, and only a longer run
  (or a driven-drift scene) can measure that tail.
- The replay discipline times parts after `step::process` on the same snapshot, cache-warm
  (inherited from the 0234 harness; its shipped-bench cross-check bounds the bias, and my
  exact_bind median matches the silver record's 75.9).
- The derivative table is a forward difference at δ = gap·2⁻²⁴: its truncation is bounded by the
  observed error floor (~10⁻¹⁴) on this scene, not separately measured.
- Linux/x86 cloud: shares are robust, µs are not; the integrator re-measures on the M1.

## Cost of adopting, and fit with PRINCIPLES

Adoption is now a wiring step, not a design step: land the additive jet module, store per body
its anchor shape and derivative table beside the tube, route `bind`'s periodic branch through the
jet with the bound rule, and judge with the existing gates (B5's error type is what the C·drift²
record bounds; B8's determinism is what the bit-identical reruns show; B9's cost-per-orbit
improves by the same 3× per kick). PRINCIPLES: "The cheapest compute is compute not done" (1) —
the compile deleted; "Cost follows change and entropy. Nothing is evolved that can be derived
when looked at" (3) — the tables are derived from invariants that move ~10⁻⁷ per kick;
"errors never compound" (13) — the error is bounded by construction at C·bound² < the floor and
re-anchored, unlike the quantized memo the law rejected.

## The lens (what this second-author lens may have missed)

It built and measured, but did not wire the jet into the live universe, so the gates' own
harnesses never ran against a jetted engine; the strong-field and passage rows are untouched;
and it inherited the 0234 replay harness (and its cache-warm bias) rather than re-deriving the
kick decomposition independently — the baseline regeneration is the guard. Per-body drift steps
for n* were pooled across bodies (order-of-magnitude only).
