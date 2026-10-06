# dossier.md

**Claim.** The doll's spin χ is in the compiler: `crates/space/src/kerr.rs` compiles equatorial
Kerr tubes in the crate's own representation (Darwin ψ, the radial cubic factored by its roots,
Gauss–Legendre in u = u₀(1 − t²) for light, all arithmetic `Scalar` — a normalized i64
significand and binary exponent, truncating integer ops), bound/unbound/plunging/photons
through one phase with no orbit category, and gate **B19 passes** on `--law space` with
G1–G6 and B16 unchanged.

**Bottleneck.** law.md "Rotating holes" (Julien: "especially rotating black holes"; the board's
"GR's weird effects, in Julien's order", first item). This deletes the last representation gap
between the Schwarzschild core and rotating holes: χ is one constant per doll, and χ = 0 routes
to the Schwarzschild core bit for bit (digest `59d54de0f9ead66f` on all three sides of
criterion 6). No second law, second memo format or category boundary exists to maintain.

**Evidence** (this Linux runner, 8 vCPU; each command ≪ 60 s; `lab/results/<run>/` holds the
raw lines):

- Before: `cargo run --release -p xtask -- behave --law space --gates G1,G2,G3,G4,G5,G6,B16,B19`
  → G1 256/256 (worst 6.60e-4), G2 256/256 (5.50e-4), G3 64/64 (6.40e-12), G4 0/10 wrong,
  G5 32/32, G6 256/256, B16 256/256 (6.93e-8) — **B19 FAIL, 0/6 cells, 0/1680 fates**
  (`gates-before.txt`).
- After: same command → same seven gates PASS with **identical detail lines**, and
  **B19 PASS, all six criteria** (`gates-after.txt`, `b19-after2.txt`):
  [1] cycles 6/6 cells, 256/256 each, advance worst **2.0e-13** (tol 1e-2), periods worst
  **5.3e-13** (tol 1e-3); [2] fates **1680/1680** exact (circular, E=1 capture, bound/plunge,
  photons, dense capture over the critical band); [3] frame dragging 379/379 tubes inside the
  ergosphere answered, dφ/dt > 0 in all (including L < 0), rates worst 1.4e-14 (tol 1e-6);
  static/ZAMO clocks worst 1.9e-16 (tol 1e-12); no static clock inside 48/48; [4] Penrose:
  85/85 negative-energy tubes answered, 73/73 forged refused, 27/27 splits conserved and
  energy-gaining (canonical: χ = 0.5, E_out +0.4196 for E_in +0.3989), 27/27 outside gain
  nothing; [5] light 6/6 cells worst 4.4e-13; [6] χ = 0 digests identical, 170/170 answered.
  Phase wall time 0.26 s.
- Controls: `--law echo` passes B19; `planted-proonly` and `planted-penrose` still fail it.
- Module tests (`cargo test --release -p emergent-space --test kerr`): 10/10 — ISCO and
  photon orbits vs BPT closed forms at 50 digits (1e-9) for χ ∈ {0.5, 0.9, 0.998} both senses;
  cycles and deflections vs independent mpmath golden geodesics (≤ 5e-6); the weak-field
  odd-in-sense advance → −8πχ(M/p)^{3/2} within 2%; fate/root-structure physics; frame
  dragging turning a retrograde tube forward; split conservation; clocks.
- Whole `emergent-space` suite green (all 8 test binaries). `cargo test -p xtask`: 198 pass;
  7 failures (`echo` events, handoff, plane) **pre-exist on pristine main** — verified by
  stashing this patch and rerunning (`echo_passes_the_four_events_gates` fails identically
  without it; those judges do not touch the kerr path).

**Predictions** (predictions.md, written before the decisive run): P1 cycles ≤ 1e-5 worst —
held with margin (2.0e-13; no cell below 256/256). P2 fates 1680/1680 — held, but only after
the run's diagnosis: the first B19 run failed every retrograde fate because the *adapter's*
`scalar()` refuses negative values (it was written for radii); the fix (`signed_scalar`) is a
boundary fix, not a law change, and is disclosed here (`b19-after.txt` → `b19-after2.txt`).
P3, P4, P5 held as written. P7 cost: predicted < 10 s, measured 0.26 s (convergence lands at
n = 32–256 panels for almost all seeds). Two self-caught algebra defects during unit testing,
both recorded: a missing factor 2 in the cubic's `2aWE` coefficient (found by the module's own
integrand probe; the same slip existed in the Newton residual), and a swapped quadratic
formula in the degenerate E = 1 branch.

**Bonus result (settles an open question from the reference run).** The exact odd-in-sense
weak-field periapsis coefficient is **−8πχ(M/p)^{3/2}**: measured −8.045π at p = 1600
converging to −8π (mpmath, this run's `gen_tables.py`), and the module reproduces it. Run
`20261006-0030` measured −8.05 ± 0.1 π, guessed −12π analytically, and left the coefficient
open ("the checker should fix it analytically"); the naive Lense–Thirring node rate gives −4π,
so the equatorial periapsis LT term is twice that at leading order. The crate test pins it.

**What would make it wrong.** The verification stack is three independent layers — BPT closed
forms (ISCO, photon orbits), mpmath golden geodesics written from the metric, and the frozen
gate against its own float64 oracle — so a shared algebra error is unlikely; shared-*author*
error is not (all three were checked by one session; the checker should rerun
`python3 gen_tables.py` and the gate). The χ = 0 digest identity is structural (routing), not
measured equality of two code paths. Known limits, none touched by B19: this module compiles
cycle *numbers*, not yet the band/crossing table (B9 cost structure) or the memo key — Astra's
integer-realization step; horizon arrival times and the logarithmic BL divergence remain
outside, as in the Schwarzschild core.

**Cost of adopting.** One new file in `crates/space` (~700 lines with derivations), a 10-test
file, one line in `lib.rs`, and the adapter's `kerr`/`spin_answer` + `signed_scalar` in
`xtask/src/behave/space.rs`. Nothing existing is modified except that adapter; every
Schwarzschild gate bit is unchanged (measured above).

**Fit with PRINCIPLES.** "χ = 0 is the Schwarzschild law, bit for bit" (measured, criterion 6);
"a tube is still compiled from (E, L), now with the doll's χ: one more constant per doll, not
per body" (the spin enters as one `Scalar` argument; no per-body state was added); "no orbit
categories" (bound, plunge, capture and light are one cubic's root structure plus the horizon;
frame dragging, the ergosphere, negative energy and the Penrose gain are outputs, not cases);
"floats never decide an outcome" (the law runs on `Scalar` and `num::cos`/GL integer tables;
floats appear only at the judge boundary and in tests).

**The lens may have missed:** cost and the integer realization depth — the module uses
`Scalar`'s i64 significand with checked exponents rather than the crate's Q62-band machinery,
so B9's crossing-count budget has no Kerr counterpart yet; non-equatorial orbits (Carter's Q,
a fourth root pair in Θ — likely the same machinery, per the reference run); the fifth/sixth
integral columns (Marck's tidal angle) that the Fermi-frame phase 2 will need; and adoption on
the M1, where the integrator re-measures (all timings here are Linux/x86 orders of magnitude).
