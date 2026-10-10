# Dossier — 20261010-1947-quant-9c2f (lens: Quant)

**Claim.** B12's bounded-vs-compounding discrimination is solved without the reference by a
return-matched **memory curve** — pairs of the law's own samples matched in the semimajor
axis at increasing encounter separations, |Δe| extrapolated to zero a-separation — : every
state-only error family stays flat (slope ≤ 0.079), every memory family rises (slope ≥ 0.251),
the requirement-level leak (the walk that spends the 1e-4 budget exactly at the horizon,
δ\* = 2.39e-5 per encounter) is caught even through a worst-case state-only error of the same
scale, and the machine-dependent reference (2×16 extra integrations at 1e-12/1e-13 plus the
convergence filter — the part that breaks on Linux) is deleted from the gate.

**Bottleneck.** The instrument (handoff risk list, "Headed next" #2; queue `q-b12-design`):
"B12 cannot yet tell bounded from compounding error on chaotic ships." Not a 10× speed
number: it unblocks the B12-v2 freeze and deletes the reference from the gate entirely.

## Evidence

Grounding, this Linux box (the frozen gate itself):

- `planted-bounded` **fails** B12: median growth exponent 0.353 (limit 0.2), worst err 1.27e-5.
- `planted-compound` **fails**: 0.416, worst err 9.8e-7.
- P2's ranking inversion (bounded 0.493 > compound 0.305 on the integrator's machine) **did
  not reproduce** (here 0.353 < 0.416): the exponent's verdict is itself machine-unstable, and
  envelope size ranks them backwards too (1.27e-5 vs 9.8e-7). No envelope statistic can work:
  on chaotic ships the semimajor axis a diffuses by up to ~0.9 sep over 200 periods, and a
  state-only error reads that diffusion as growth.

The memory curve (16 frozen ships × 1601 samples each, the law's own answers only; M(Δn) =
per-ship median |e(t₂)−e(t₁)| over sample pairs matched in a, intercept at zero a-separation;
`work/memory_curve.json` holds every number):

| stream | slope | verdict | top M |
|---|---|---|---|
| echo | 0.079 | state-only | 2.8e-16 |
| planted-bounded | −0.246 | state-only | ≤4.8e-12 |
| AR(1) φ=0.9, σ=1e-8 (correlated, no memory) | −0.012 | state-only | 2.4e-8 |
| state-only in a **and** planet distance | −0.060 | state-only | 7.4e-6 |
| planted-compound (walk 1e-7/encounter) | 0.281 | **LEAK** | 4.5e-7 |
| leak δ\* = 1e-4/√18 (requirement) | 0.269 | **LEAK** | 9.9e-5 |
| leak 4δ\*, 16δ\*; δ\*/4 on clean echo | 0.418, 0.371, 0.324 | **LEAK** | — |
| state-error floor + leak δ\* | 0.337 | **LEAK** | 1.0e-4 |
| state-error floor + leak δ\*/4 | 0.072 | state-only | 2.5e-5 |
| state-error floor + leak δ\*/16 | 0.077 | state-only | 1.3e-5 |

Null slopes ≤ 0.079, leak slopes ≥ 0.251: an empty gap; the pre-registered verdict rule
(slope ≥ 0.25 and top/bottom ≥ 2) needed no fitting. Including the ships this run's reference
excluded (all 16, not 14 judged) changes no verdict (−0.048 / 0.251): **the statistic needs no
reference, no convergence filter, no machine-dependent selection** — the inputs are t, the
law's states, and the scene constants.

The classic alternative, variance ratio VR(64) on error levels: leaks 0.84–1.00 vs nulls
0.02–0.40 — it separates on this scene (my P5 said it would not; wrong, because a's wandering
is confined, so state-only error mean-reverts at long lags). But VR is scene-calibrated, and
through the state-error floor its bands overlap exactly where it matters: null bounded 0.40 vs
requirement leak 0.49, unseparable, while the memory curve separates (−0.060 vs +0.337). Keep
VR(64) as a free corroborating column; the memory curve is the instrument.

**The detectable leak and its horizon, derived** (the redesign's stated requirement): with a
state-only error floor f and N encounters in the horizon, the gate polices per-encounter walk
rates in [≈4f/√N, 1e-4/√N] — the ratio 1e-4/(4f) is horizon-independent; each ×m of
sensitivity costs m² of horizon. At 200 periods (N median 18, max 30): echo's own floor is
3e-16, so a clean law polices down to ~1e-16; the worst-case planted state error (f = 7.4e-6)
gives [~6.6e-6, 2.4e-5] — and the measured detection boundary (δ\* caught, δ\*/4 buried)
lands exactly there. The freeze's f is set by the integrator's chosen acceptable-state-error
family (the plants define it), not fitted on the leak side.

**Reproduce** (this box, CARGO_TARGET_DIR=/home/glmlab/lab-target-2; each ≤ 60 s after one
40 s build; machine state is logged by the gate runs themselves):

```
cargo build --release -p xtask
$CARGO_TARGET_DIR/release/xtask behave --law planted-bounded --gates B12
$CARGO_TARGET_DIR/release/xtask behave --law planted-compound --gates B12
B12_DUMP=$PWD/lab/results/20261010-1947-quant-9c2f/work/streams \
  cargo test --release -p xtask dump_b12_streams -- --ignored --nocapture   # needs this run's patch
python3 lab/results/20261010-1947-quant-9c2f/work/analyze.py               # prints every number above
```

Files: `work/analyze.py` (deterministic; own SplitMix64 for the synthetic controls),
`work/streams/*.f64` (16 ships × 1601 × 10 f64 per law, the law's own observables),
`work/memory_curve.json`. The tree patch adds one ignored dump test and marks
`laws::star_axis` `pub(crate)`; nothing else changes.

## Predictions (predictions.md, written before the decisive run)

Held: P1 (flat for echo and bounded), P3 (separation ≥ 4×: 4.5e-7 vs ≤4.8e-12, i.e. ~10⁵×),
P4's verdict (the requirement leak flagged through nothing and through the state floor),
P6 (no reference, no filter), P7 both (correlation without memory and a two-coordinate
state-only error stay flat, the latter on a 7.4e-6 floor). Missed, narrowly and disclosed:
P2's slope band [0.3, 0.7] — the plant reads 0.281 (the estimator compresses; growth 5× held);
P4's slope clause ≥ 0.3 — read 0.269 (verdict unaffected); P5 outright wrong — VR(64) does
separate on this scene. The P5 miss is informative: VR's null band depends on the confinement
of the wandering coordinate, which is scene physics, not a guarantee.

## What would make it wrong

A real law whose state-only error lives in a coordinate that wanders without returning (an
accumulating angle, say) raises the floor f without bound and buries real leaks — the freeze
must set f from the declared acceptable-state-error family, and the matching vector may need a
second coordinate (cost grows with dimension). The slope threshold sits inside a 16-ship gap
(0.079 to 0.251); a law near the boundary could wobble across. The synthetic controls are
added to e post hoc, not planted in states (the plants' velocity-shift feedback is not
exercised for them) — a checker can plant one in Rust. And the matching coordinate a is
inherited from P2's plants; a law whose error keys on other elements needs the instrument
re-derived, not re-tuned.

## Cost of adoption, fit

B12-v2 reads the same 1601 samples per ship the judge already reads, computes e, a, n (already
computed today), and pair-matches (20M pairs ≈ <1 s in Rust, 37 s in this numpy); it deletes
the 2×16 reference integrations per law and the convergence filter, and runs anywhere
(Linux included). PRINCIPLES: "basically we don't want errors that can compound that's the
goal" (13) — the gate now measures compounding itself; "error type over error size" (2) — the
instrument is scale-free and magnitude-blind, which is exactly why it survives where the
envelope exponent and VR do not; controls on both sides, and thresholds from the requirement
(the 1e-4 budget and the horizon), none fitted.

## The lens

The quant habit that may have misled: I reached for market-statistics instruments (unit root,
variance ratio) and found one works better than predicted — but its calibration is scene
physics (confined diffusion), not mechanism, and only the return-matching carries the
guarantee. Not done here: the plane law itself is not wired as a behave `Law` in this tree, so
the curve has not been run on the real law's streams — the integrator should do that (and on
the belt or co-orbital scenes) before freezing; and the physics of *why* a is confined (co-orbital
geometry) deserves one paragraph from a physicist, not a footnote from me.
