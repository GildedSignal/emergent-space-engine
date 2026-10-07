# Dossier — 20261007-0621-components-8306 (components lens): the kick's rebind, the jet measured on the integer law

## Claim

The kick's rebind path on the integer law pays a fresh 4.9 µs quadrature compile on **every eccentricity-moving kick** (p-moving kicks already hit the shape memo at 0.49 µs: the key's p is the semi-latus rectum and the weak-field shape ignores it), and the law's jet (law.md, "exact offset plus stored derivatives, re-anchored" — gold-graded once, never checked on the crate) **holds on the integer compiler with one correction: C is a property of the anchor, not a constant** — error = C·drift² with C spanning 0.33 (p=20M, e=0.3) to 140 (e=0.9 at fixed p; the elliptic curvature grows toward the separatrix), so a global C either breaks the 10⁻⁶ floor by 89× or wastes 9× the compiles; with C measured free at each anchor (second differences of the same arming compiles) and a 1.5 safety factor, belt-size kicks (ε ≤ 10⁻⁶, coherent) cost **0.005–0.08 compiles/kick (13–200× fewer), max error ≤ 10⁻⁶ everywhere tested**, while ε = 10⁻⁴ collapses to 0.46–0.63 compiles/kick (marginal) and the Peters inspiral row is strictly harmful (5.0 compiles/kick) — the law's replacement of it by Peters' a(t) generator is confirmed, not just plausible.

## Bottleneck

Board focus #1, "fewer kicks per orbit … kicks dominate the engine's cost." The plane recompiles a cycle on ~99% of kicks (taste log, 5 October); HANDOFF's measured 29 µs/kick. The lens's four questions for this component (the rebind):

- **Owner:** P14 "No work for no reason" (a kick adds two integers; a fresh quadrature is work for no reason), P3 "Compute only surprises", P13 "Errors never compound" (the jet's error is bounded by construction, re-anchored).
- **Floor:** a kick delivers (ΔE, ΔL); the tube's update is 6 fixed-point multiply-adds on stored derivatives plus a drift check — O(10 ns), zero compiles while drift < δ*. The compile is only re-entered at δ*.
- **Idiot index on compiles:** shipped 1.0 compile/kick on e-kicks vs 0.0065 at belt sizes = **~150×**; on the whole rebind tail the compile is 4.9 of 13.7 µs (36%), so the tail drops to ~8.9 µs (**1.5×**) and the whole 29 µs kick to ~1.2×: **the jet is necessary but not sufficient — the remaining 8.8 µs is fit_key + at_radius + decoded_event, readout-shaped** (see "What would make it wrong").
- **Within 10× of floor:** at ε ≤ 10⁻⁶, compile amortized = 0.0065 × 4.9 µs = 32 ns/kick + O(10 ns) jet arithmetic: **~4–5× of the ~10 ns floor**, on the same order as the queue's timing-wheel result for its component.

## Evidence

Linux x86 shared runner (orders of magnitude only; integrator re-measures on the M1). All numbers regenerate from the repo:

```
cd lab/results/20261007-0621-components-8306/work
CARGO_TARGET_DIR=/home/glmlab/lab-target-0 cargo build --release --offline
B=/home/glmlab/lab-target-0/release/jet-bench
$B cost        # compile 4876 ns, memo hit 487 ns, memo miss 5364 ns, state 731 ns, rebind 13720 ns
$B scan        # error = C·drift² per (p, e); jump floor; C per row (scan.txt)
$B stream corr 1e-6 5.27e8 0.5 10000 2    # 0.0075 compiles/kick, max err 9.2e-7
$B stream corr 1e-6 5.27e8 0.9 10000 9    # 0.077/kick, 6.1e-7 (was 8.9e-5 with global C=2)
$B stream corr 1e-6 20 0.3 10000 13       # strong field, 0.007/kick, 2.0e-7
$B stream rand 1e-6 5.27e8 0.9 10000 12   # 0.002/kick, 8.1e-7
$B stream corr 1e-4 5.27e8 0.1 10000 4    # 0.455–0.63/kick: marginal
$B stream peters 1.1e-3 50 0.5 300 7      # 5.0/kick: strictly harmful
$B negctl corr 1e-6 5.27e8 0.1 10000 10   # frozen anchor: 2.2e-5, detects drift
```

**Cost split** (p = 5.27×10⁸ M, e = 0.1, B17's scaled scene): `Orbit::compile` at a kicked key 4.88 µs; `ShapeMemo` hit (p-only kick; the shape key is (k, q→0), k unchanged) 0.49 µs; miss (e-kick) 5.36 µs; one `state()` readout 0.73 µs; `Rebinding::from_state` (the shipped rebind tail: fit_key + compile + at_radius + residual) 13.7 µs. So the compile is 36% of the tail; the other 8.8 µs is fit and readout work (each `state()` probe 0.73 µs).

**Scan** (single kick of drift δ from a 5-compile anchor, log-parametric central differences at h = 10⁻³): error is quadratic in δ above a discreteness floor: weak field floor ~10⁻¹⁵ (invisible), strong field (p = 50, 20) 10⁻¹²–10⁻¹⁰ — five orders below the 10⁻⁶ rule, so the compiler's re-paneling never binds the jet. C(period, e-axis): 1.8 at (5.27e8, 0.5) — matching redteam-df81's float 1.9 for the same quantity class — 0.33 at (20, 0.3), **135–147 at (5.27e8, 0.9)**. The apsidal advance is e-independent to 10⁻¹¹ in the weak field (p is the semi-latus rectum; Δφ ≈ 6π/p there): e-kicks in the belt move only the period and proper period. df81's "C is nearly e-independent" was measured for Δφ at fixed E; at fixed p the period's curvature is what matters and it is not flat.

**Streams** (n = 10⁴ kicks, rule δ* = √(floor/(1.5·C_anchor)), re-anchor = 1 exact + 4 derivative compiles; truth = exact recompile every kick):

| stream | compiles/kick | max err | vs shipped |
|---|---|---|---|
| corr ε=10⁻⁸ (5.27e8, 0.1) | 0.0005 | 3.1e-10 | 2000× |
| corr ε=10⁻⁷ (0.5) | 0.0010 | 1.4e-6→8.9e-7 w/ safety | 1000× |
| corr ε=10⁻⁶ (0.1 / 0.5 / 0.9) | 0.0065 / 0.0075 / 0.077 | 2.1e-8 / 9.2e-7 / 6.1e-7 | 150× / 130× / 13× |
| corr ε=10⁻⁶ (p=20, strong) | 0.0070 | 2.0e-7 | 140× |
| rand ε=10⁻⁶ (0.9) | 0.0020 | 8.1e-7 | 500× |
| corr ε=10⁻⁴ (0.1) | 0.455–0.63 | 3.5e-7 | 1.6–2.2× |
| Peters ε=1.1×10⁻³ growing (p=50) | 5.02 | 1.1e-4 | harmful |

The global-C failure (my first stream run, disclosed): with C = 2 everywhere, (5.27e8, 0.9) hit max err 8.9×10⁻⁵ — 89× the floor — at the same 0.0075 compiles/kick; the per-anchor C costs nothing (the arming compiles already contain it) and re-anchors every ~79 kicks there. A 1.5 safety factor on δ* (third-order term) brings the worst rows from 1.38× floor to ≤ 0.92× floor at ≤ 1.2× the compile cost. Negative control (frozen anchor increments, same rule): 2.2×10⁻⁵ at ε = 10⁻⁶ — the harness detects drift; the derivative term is what buys the two orders. The Peters row's honest extra: the unbounded version of that stream drives p below the ISCO and the compiler correctly returns `NoBoundOrbit` (a plunge, not a bug).

## Predictions (predictions.md, written before scan and streams)

- P1 (calibration, cost): held.
- P2 (jump floor visible): held — plateau 10⁻¹²–10⁻¹⁰ strong field, 10⁻¹⁵ weak (below my 10⁻⁹–10⁻⁷ guess; five orders under the rule, so it never binds).
- P3 (belt row, 0.007 compiles/kick, err ≤ floor): held (0.0075; 9.2e-7).
- P4 (ε=10⁻⁴, ~0.7 compiles/kick, no win): held (0.455–0.63).
- P5 (Peters row harmful): held (5.0/kick; plus the plunge refusal).
- P6 (negative control exceeds floor within ~10 kicks at 10⁻⁶): held (p50 1.1×10⁻⁵).
- P7 (C grows ≥10× at e=0.9, n* shrinks ~3×): held, stronger — C grows 75×, n* shrinks 9×. My first reading of the scan falsified it (floor-contaminated rows read as C=1.3); the stream corrected me. Disclosed.
- P8 (strong field, both axes): held (0.007/kick, 2.0e-7).

## What would make it wrong, cost of adoption, fit

- **Wrong if** the crossing table (not measured here; the increments are the cycle contract of law.md line 14) carries curvature beyond the increments' C — unlikely at e ≤ 0.9 (same Taylor remainder, same panels) but unverified; or if positions read mid-cycle between anchors amplify the drift (the ramp rule of law.md line 33 governs that read, untested here).
- **The wall claim is bounded:** the jet deletes the compile term (36% of the rebind tail, ~17% of the whole 29 µs kick). The neighbour it exposes is bigger: `kicks::apply` reconstructs Cartesian state, then `fit_key` inverts it back to a key, when the kicked (E, L) are already exact integers in hand — an (E, L)-native rebind skips the round-trip and most of the 8.8 µs. That is the next run on this component (it touches Sol's kicks.rs/binding.rs, so it is proposed, not built here).
- **Cost of adopting:** small and surgical — the jet with per-anchor C (second differences at arm time; in production, derivatives stored in the shape per law.md line 14 make arming 1 compile, not 5) plus the 1.5 safety factor, wired where `Rebinding::from_state` compiles. Not a crate edit from this run: the bench is measurement, the patch is the design + numbers.
- **PRINCIPLES:** P13 "basically we don't want errors that can compound" — bounded by construction, re-anchored, and the bound is self-calibrated at the anchor; P14 "No work for no reason, so no ticks" — the compile was the reason-free work; P1 "the cheapest compute is compute not done" — 150× fewer compiles at belt sizes; P9 — the ε ≥ 10⁻⁴ and Peters configurations are killed, never the method.

## The lens (what it may have missed)

I measured the cycle contract, not positions (above), and my jet is armed by 5 compiles rather than stored derivatives — the adoption cost is overstated by up to 5×. A memory-lens run might ask where the anchor pool lives at 10⁹ bodies (one shared shape per distinct anchor: the memo again); a dynamics-lens run would test the near-separatrix (e > 0.995, where C may grow past any rule) and the resonant per-conjunction kick stream, which is correlated at ε near 10⁻⁴ — the row where the jet already fails here.
