# Dossier — run 20261010-0814-second-20261010-0656-autoresearch-cc88-8ce2 (lens: second author on 20261010-0656-autoresearch-cc88)

## Claim

cc88's record regenerates from shipped code (cos4: −16.5% on the kick median, digests
bit-identical, `refused` 0), and the checker's named gold experiment — **deleting the
rebind compile via the re-anchored jet** — is implemented in the shipped compiler and
measured: the cycle's **advance** increment holds 7×10⁻¹⁵ at df81's drift budget
θ = 7.3×10⁻⁴ (eight orders inside the 10⁻⁶ floor), but the **period** (3.2×10⁻⁴) and the
**position readout** (9.0×10⁻⁴) break that floor at θ; holding every consumer needs a
budget of ≈7.5×10⁻⁶ (≈7 kicks per anchor at ε = 10⁻⁶). On the plane's own kicks the
per-kick drift never exceeds 1.3×10⁻⁷ (58× inside even that budget), so the compile
component falls to **0.073 compiles/kick** (churn-limited, not drift-limited) — the
deletion stands for the plane's real workload, but the jet as implemented is **not** a
whole-rebind replacement at df81's θ, and its derivative alignment refuses (re-anchors)
per kick at e ≥ 0.9.

## Bottleneck

Board focus line 1 (kicks dominate) via the checker's own route: "Gold on this bottleneck
is deleting the rebind compile itself (the re-anchored jet … Next run should take the
jet)". law.md's jet clause ("a kick updates the cycle by a multiply-add") was graded gold
once (df81, float oracle, increments only); law.md notes "the second never ran". This run
is that second check, upgraded to the shipped integer compiler and to the readout.

## Evidence (runner: 8 vCPU i7-4790 @ 3.6 GHz, shared, light load; each command ≤ 60 s except builds)

**E1 — cc88 regenerates.** Clean worktree at HEAD + `keep.patch`: seed 1 kick_us all
median **88.0 → 73.5 µs (−16.5%)**, replay digest `59ea9969…`, universe digest
`13cfe88b…`, `refused` 0 — equal to the baseline and to cc88's table. Baseline itself
(shipped tree, seed 1): 88.0 µs median, same digests; the memo negative reproduces
(663 distinct shapes in 663 cycle rebinds, exact hit rate 0.0).

**E2 — the plane's real kick drift (no law change; `e2_seed1.json`).** Instrumented
`--kick-bench` (seed 1): 618 weak-path kicks between rebinds, 45 anchors ⇒
**0.073 compiles/kick** at θ = 7.3×10⁻⁴. Per-kick |Δk|/k: median 1.2×10⁻¹⁰, p99
1.0×10⁻⁷, max 1.3×10⁻⁷; **zero kicks above 10⁻⁶**. The anchors are population churn
(first binds, strong-shape rebinds), never drift: the plane's belt tides are seven orders
below the budget. So on the plane the jet's cadence is churn-limited and the compile
component would fall 63 µs → 63·0.073 ≈ 4.6 µs per kick (decomposed prediction: every
factor measured on shipped code; end-to-end wiring not built in this run's budget).

**E3 — the jet on the shipped compiler (`e3_jet_tests_output.txt`, tests in-tree).**
`OrbitShape::jet_table` (analytic integer k-derivatives of the weak panel quadrature,
aligned per knot) + `jet_update` (one exact-rounded i128 multiply-add per knot
component, constants re-derived exactly). df81's named criterion, truth = the shipped
`Orbit::compile` (not a float oracle), 10⁴ systematic kicks:

| e | ε | advance err | period err | radius err | anchors | jet µs | compile µs |
|---|---|---|---|---|---|---|---|
| 0.3 | 10⁻⁶ | **7.1×10⁻¹⁵** | 3.2×10⁻⁴ | 9.0×10⁻⁴ | 14 | 1.6 | 11.3 |
| 0.3 | 10⁻⁴ | 1.0×10⁻¹² | 3.5×10⁻⁴ | 9.8×10⁻⁴ | 329 | 0.3 | 1.7 |
| 0.9/0.99 | any | ~10⁻¹⁶ | 9–99×10⁻⁶ | ≤0.55 | ≈kicks (refusals) | 3.4–4.9 | 46–75 |

- Quadratic check: err(ε)/err(ε/2) = 2.7 at one anchor cycle (bounds 2–8 asserted).
- Negative control (frozen table, re-keyed): advance error 7.3×10⁻⁴ — fails the floor,
  as df81's control did.
- Readout calibration: C_r = 1.7×10³ (e = 0.3) to 2.9×10⁸ (e = 0.99); the period at
  θ_r = 2.4×10⁻⁵ still reads 1.1×10⁻⁵ — the every-consumer budget is ≈7.5×10⁻⁶.
- At e ≥ 0.9 the aligned derivative overflows i64 and `jet_update` refuses each kick —
  the re-anchor rule fires (correct behaviour, recorded limitation: the derivative should
  be stored at its own normalized exponent).
- Both suites green with the jet in-tree: `emergent-space` 14 passed (4 jet tests),
  `emergent-universe` 10 + 6 passed — the shipped law is untouched by the additions.

Commands (target dir `$CARGO_TARGET_DIR`; build ~40 s once):

    CARGO_TARGET_DIR=/tmp/lab-target-2 cargo test --release -p emergent-space jet -- --nocapture
    CARGO_TARGET_DIR=/tmp/lab-target-2 cargo test --release -p emergent-space
    CARGO_TARGET_DIR=/tmp/lab-target-2 cargo build --release -p xtask   # instrumented bench
    $CARGO_TARGET_DIR/release/xtask universe --kick-bench --seconds 10 --rtf 100 --seed 1
    # E1: clean worktree at HEAD, git apply keep.patch, same bench command, diff digests.

## Predictions

`predictions.md` was written before all decisive runs. Outcomes: P1 **held** (−16.5%,
digests identical, refused 0). P2 **wrong in its number, right in direction** — predicted
≥ 50 kicks/anchor drift-limited and ≤ 0.02 compiles/kick; measured 0.073, churn-limited,
because per-kick drift is 10⁻¹⁰–10⁻⁷ (I predicted ≤ 10⁻⁵, true but far looser than
reality). P3 **half-held, and the miss is the finding**: advance holds with eight orders
of margin (predicted), but the period and radius break the 10⁻⁶ floor at df81's θ
(predicted to hold) — and the radius error is not cleanly quadratic (floors ≈3×10⁻⁵).
P4 **held** (update 1.6 µs ≤ 8 µs predicted; compile 11–75 µs here, 63 µs on the plane
per cc88's profile).

## What would make it wrong, adoption cost, fit

- The end-to-end kick-median claim for the plane is a **decomposed** prediction (compile
  fraction from cc88's profile, cadence and update cost measured here); it is not wired
  into `bind`. If the churn anchors (first binds, strong rebinds) turn out to share
  shapes across bodies under a catalogue, the amortized compile falls further, not less.
- The jet is weak-path only; strong shapes (fast_quad) anchor, which the plane's mix
  makes cheap (E2: 45 of 663 rebinds).
- df81's θ is falsified **for the period and readout on the shipped compiler**: adopting
  the jet requires the ≈7.5×10⁻⁶ budget (≈0.13 compiles/kick at ε = 10⁻⁶) or a
  second-order term; on the plane it changes nothing (churn-limited either way).
- PRINCIPLES: "a kick updates the cycle by a multiply-add" is representation.md's own
  clause, here measured rather than assumed (10, "Measure before claiming"); the
  falsified part of df81's rule is reported, not patched around (9, 13: no compounding
  error is accepted — the budget is tightened to what holds); "Compute only surprises"
  (3): 92.7% of the plane's rebinds carry no surprise a compile would discover.

## The lens

A second author inherits the first run's frame: I took "take the jet" as the increments
criterion and nearly shipped the readout failure as an instrumentation bug (a dropped
accumulation printed 0.000e0 and briefly "confirmed" the jet — the honest record above is
from the fixed harness; the intermediate misreading is disclosed here). What this lens
missed: the root cause of the radius error's non-quadratic floor (anchor psi-grid vs the
fresh compile's adaptive bands is the prime suspect, unproven), the e ≥ 0.9 alignment
fix, ARM/NEON numbers, and any wiring into `bind`. The checker's "cos4 rides along
either way" stands: the jet deletes the compile cos4 was optimizing, and on the 7% of
kicks that still anchor, cos4 still pays.

## Files

`predictions.md` (pre-registered), `e2_seed1.json` (instrumented bench, seed 1),
`e3_jet_tests_output.txt` (criterion run), `work/patch.diff` (bench instrumentation +
`jet_table`/`jet_update`/`weak_quad_jet` + `Scalar::plus_significand` + the four jet
tests, 260 lines).
