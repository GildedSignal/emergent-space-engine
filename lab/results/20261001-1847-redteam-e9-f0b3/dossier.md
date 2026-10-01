# Dossier — red-team of engine-judge E9 (the Schwarzschild tide gate), pre-freeze

**Claim.** E9's independent oracle (nearby Schwarzschild geodesic pairs) is sound at the
first-order physics level — its Killing constants, difference equations, exponential-map
genesis, axis transport and projection are confirmed by an independent absolute-coordinate
construction to ~1e-9 — but the gate as coded certifies wiring, not GR: both planted
defects and the positive weak control run at r/M = 10^6, where the Newtonian tide misses
the GR oracle by 7.0e-6, *below* the oracle's own 1e-5 validity tolerance, and the
engine-extent linearization gap (measured 4.9e-7, both constructions agreeing) plus the
6x margin of the r/M=10 e=0.6 separation control are the only quantitative fragilities
found. Freeze-able after the two premise notes below are recorded, not before.

## Bottleneck

Not a board bottleneck: this is the pre-freeze red-team that AGENTS.md requires of every
gate. Gain: E9 can be frozen without adopting a wrong oracle; the alternative (a wrong GR
tide passing E9) would poison phase 2 (Schwarzschild tide in the Fermi frame).

## Evidence (all numbers reproducible from this folder; cloud x86, orders of magnitude only)

Three-way comparison, identical initial data and sampling grid (dt = period(a,e)/40, 401
samples over ten proper periods):

- **(R)** the judge's oracle, executed as Rust: `cargo test -p xtask schwarzschild`
  (5/5 pass on this box), plus a standalone harness (`rust-truth-harness.rs`, built from
  an unmodified copy of `schwarzschild.rs`) dumping truth samples to `truth.jsonl.gz`.
- **(M)** an independent absolute-coordinate integrator (`control.py`): raw second-order
  geodesic equations, textbook diagonal-metric Christoffels, own Riemann tensor, own
  Fermi-simultaneity Newton solve. No Killing constants in the RHS, no difference
  variables.
- **(A)** independent analytic derivations (turning-point (E,L); circular epicycle and
  geodetic rate; Riemann-projected tidal matrix).

1. **Killing constants** — my turning-point derivation (L² = (f(r_a)−f(1))/(α(f(1)−f(r_a)/r_a²)))
   matches the Darwin forms to dE/E ≤ 1.2e-16, dL/L ≤ 4.7e-16 at α=0.1; ≤ 3.7e-11 at
   α=1e-6 (cancellation in *my* closed form there). Circular: exact to all digits.
2. **Pairs are true geodesics (core premise)** — my absolute members vs the Rust oracle's
   difference-ODE pairs at s=1/16: see `compare-run2.log` (r/M=10 e=0.6, e=0; r/M=10^6
   e=0). Held prediction: < 1e-9 of the offset (E,L conserved to ≤1.2e-13 along my runs).
3. **Fermi simultaneity** — equal-proper-time projection vs orthogonality-solved Fermi
   projection (`control-run2.log`, P2 lines): measured residual and s² scaling. The even
   part of the simultaneity error cancels in the judge's odd (centered) difference; the
   halving check bounds the rest.
4. **Engine-extent gap (no false failure)** — a *perfect* engine at full extent 1e-5·r_p
   vs the judge's linearized (s=1/16) truth: **4.85e-7** (my construction) and **4.88e-7**
   (their own s=1 vs s=16, no code of mine involved) — 20,000x inside the 1% band.
5. **Weak control is wiring-only (premise)** — the oracle-only Newtonian trace at r/M=10^6
   misses the GR oracle by position 7.0e-6 / shape 5.0e-6, *below* the oracle validity
   tolerance 1e-5. At that radius the gate cannot tell GR from Newtonian: `--e9-weak-control`
   and both planted defects (sign-tide, static-tide, run only there) certify that a
   mutation reaches the verdict, not that the physics discriminates. Discrimination lives
   in the near-field cases, which the phase-1 engine cannot inform by construction.
6. **Margin fragility at the strong end** — the r/M=10, e=0.6 separation control measures
   1.614e-6 against the 1e-5 oracle tolerance (6x margin) in a regime where the pair
   separation grows 64x per ten periods and my faithful Python port of the same maths
   reads 3.5e-9 there: second-order controls in the unstable strong-field case are
   chaos-amplified and implementation-sensitive. Fails safe (oracle_ok=false fails the
   case), but any future oracle refinement can flip the r/M=10 rungs to oracle-invalid.
7. **Units and scale mapping** — verified end to end: λ = τ√(M/r_p³) normalization
   (a·g(u,u) = −1) is consistent everywhere; the engine's quantized velocity k = n·rot(x)
   maps to the oracle's offsets.1 = k/(nR) = rot(offsets.0) (the n cancels; rigid
   co-rotation at unit λ-rate); genesis renormalization targets the same norm. Sample
   grids coincide exactly (engine ticks j·stride ↔ oracle λ_j = j·stride·n; drift ≤ 200n
   ≈ 1e-6 relative). At r/M ≥ ~10³ the velocity quantum rounds the members' relative
   velocity to zero (n·|x| = 10.5/√(r/M): 0.01 at 10^6): large-radius cases judge a drop
   cloud, consistently in both implementations.
8. **Runtime** — release oracle ≈ 0.12 s per ten-period case (measured): 63 calls ≈ 8 s.
   Epochs are angle-capped (2⁻⁸ rad ⇒ ~1,600 epochs/orbit at every radius, anchors every
   8 epochs): the 6.6e10-chronon weakest-field case is ~16,000 epoch kicks, not per-
   chronon work. The 55 s watchdog fits with wide margin [INFERENCE: engine side not
   run — E9 fails closed pre-freeze by design].
9. **Fail-closed honored** — `E9_FROZEN=false` returns UNSUPPORTED before any engine
   call; the pre-freeze unit tests construct no Frame/Battle; oracle-invalid ⇒ case
   fails AND engine_valid=false ⇒ gate FAILs; frame misbehaviour (refused anchors,
   recentring, handed-out bodies) ⇒ FAIL. Timeout/panic are not kills (consistent with E6).
10. **Determinism probe** — debug and release test binaries of the same source parse to
    the same control values (see below); the "1.61e-9 vs 1.61e-6" spread in my first
    reading was a transcription error of long fixed-point prints, resolved by parsing.

## Predictions (`predictions.md`, written before the decisive runs)

Held: 1 (constants ≤1e-12), 4 (Fermi residual, small and s²), 5 (extent gap <5e-4;
actual 4.9e-7), 7 (weak-control degeneracy), 8 (oracle <15 s; actual ~8 s).
Pending at write time: 2 (mirror fidelity — see below), 3 (pairs <1e-9), 6 (circular
analytics). **Held-out misses I own:** (a) prediction 2's mirror-fidelity bound failed —
my Python port reads 15x–450x off the Rust on *sub-tolerance second-order controls*
in the amplified e=0.6 regime (first-order behaviour matches; closure test exact);
the authoritative comparisons therefore run against the Rust dump, not my port.
(b) My first absolute integrator had a sign-flipped Γ^r_rr — invisible at ṙ=0, E and L
still conserved, closure broken; found by the closure test, fixed, and recorded here
because "a failed expectation is not a failed method" cuts both ways.

## What would make it wrong

- The r/M=10 e=0.6 separation control (1.6e-6) crossing 1e-5 under any oracle code
  change would void oracle validity at the strong end (fails safe, but the 21-case
  spectrum would collapse to VOID, not KILL).
- The engine-side runtime at r/M=10^6 is inferred from epoch capping, not measured;
  if anchoring does per-epoch work beyond ~µs, the weakest-field case times out.
- The weak control cannot detect a wrong-tide engine; a fourth mutant (Newtonian tide)
  failing a *near-field* rung would close that hole once the engine can pass any.

## Cost of adoption, fit with PRINCIPLES

Adoption cost: none beyond the freeze record — E9 already fails closed. The two premise
notes (wiring-only weak control; unstable-regime margin) belong in `docs/engine-judge.md`
before `E9_FROZEN` is set. Fit: "Certificates need independent, adversarial checks"
(this run); "Gates are frozen before the first run and never weakened after" (the
candidate text is frozen pre-run and fails closed); "a game is an illusion spectacle,
the oracles are guards, not shepherds" (E9 judges the whole public frame, per its own
phase-1 limitation, and does not claim to isolate the tidal coefficient).

## The lens (what red-teaming may have made me miss)

A red-team attacks; it does not explore. I did not test the *engine-side* path at all
(fails closed), did not run E1–E8 (unchanged, out of scope), and did not audit the
Darwin-period quadrature beyond the shipped closure test plus my period() cross-check.
The strongest claim I could not fully close inside the window: *why* my Python port
differs from the Rust on amplified second-order controls — root cause is consistent
with 1-ulp op-order differences under ~10^6 amplification, but I did not isolate the
exact operation.
