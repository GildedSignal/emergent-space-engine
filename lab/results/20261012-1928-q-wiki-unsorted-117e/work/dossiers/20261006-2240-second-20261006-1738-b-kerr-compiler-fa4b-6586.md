# dossier.md

**Claim.** Run `20261006-1738-b-kerr-compiler-fa4b` is gold on the physics and silver only by a
record defect: the publisher's grep (`lab/run.sh:99`) looks for a literal `Grade: ` line in
`check2.md`, the second checker put the verdict in `checker2-final.md` instead ("## Verdict:
**Grade: gold**"), and the machine read disagreement where both checkers said gold; the shipped
record regenerates bit for bit, and both latent edges the second checker named are real, now
measured exactly, and closed by a 19-line guard with **every gate line unchanged** — the claim
holds.

**Bottleneck.** Not a board bottleneck: this is the lab's own gate on gold ("gold is checked
twice; gold stands only if both grade it gold"). The named gap was (a) a record that must
regenerate from shipped code, (b) the isco extremal edge and the CYCLE_MAX silent degradation.

**Evidence** (this Linux runner, 8 vCPU; machine-state.txt; every command ≤ 60 s except
gen_tables at 31 s).

*The silver is mechanical.*
```
git show origin/claude/lab-20261006-1738-b-kerr-compiler-fa4b:lab/results/20261006-1738-b-kerr-compiler-fa4b/check.md  | grep -m1 '^Grade: '   # → Grade: gold
git show origin/claude/lab-20261006-1738-b-kerr-compiler-fa4b:lab/results/20261006-1738-b-kerr-compiler-fa4b/check2.md | grep -m1 '^Grade: '   # → no match
```
`run.sh:95-99` then sets `grade="Grade: silver (second checker disagreed)"` — the branch commit
message says exactly that. The second checker's substantive verdict is in `checker2-final.md`:
"## Verdict: **Grade: gold**". One missing line, not a physics disagreement.

*The record regenerates from shipped code* (clean tree at `70f27a9` + the run's `work/patch.diff`).
- `cargo run --release -p xtask -- behave --law space --gates G1,G2,G3,G4,G5,G6,B16,B19`
  (0.7 s): all eight PASS; every gate line identical to the author's `gates-after.txt` — the
  full diff is their first-compile warning block plus the runner's target-dir path, nothing else
  (B19 detail line, counts, worst errors, digest `59d54de0f9ead66f` all byte-equal).
- `cargo test --release -p emergent-space --test kerr`: 10/10. Whole crate suite: green
  (57 tests, 9 binaries).
- `python3 work/gen_tables_redirect.py` (31 s) regenerates `golden.json` **byte-identical**,
  including the LT scan −8.1836π → −8.0909π → −8.0452π. Disclosed boundary fix: the run's
  `gen_tables.py` hard-codes its output path to the author's run folder; the redirect changes
  that one string (`work/gen_tables_redirect.py` is the sed result, kept).

*The named experiment 1 — isco at the extremal limit* (`work/gen_cases.py` →
`crates/space/tests/second_probe.rs`, mpmath truth from Bardeen's closed form at 40 digits).
```
cargo test --release -p emergent-space --test second_probe -- --nocapture
```
- a ∈ {0.5, 0.9, 0.998, 0.999, 0.9999, 1−2⁻³⁰, 1−2⁻⁵²}: both senses correct, worst relative
  error **8.3e-9** (at a = 1−2⁻⁵²; the near-triple-root flatness predicted in predictions.md,
  measured better than the 1e-5 bound).
- **a = 1: prograde returns 6.0, truth 1.0** — the defect exactly as the checker named it. I
  re-derived the cause by hand: at a = 1 the prograde polynomial is (√r−1)³(√r+3) ≥ 0 on the
  bracket [1, 6] with its triple root at the `lo` endpoint, so `bisect` (sign-blind, returns
  `hi`) slides to 6. Retrograde returns 9.0 — correct, the same slide happens to land on the
  root. `photon_orbit` is safe even at a = 1 (its polynomial is −(u−1)²(4u−1): simple root in
  the retrograde bracket, and the prograde slide lands on the true root u = 1) — probed, no
  guard needed.
- Unreachable through the judge, confirmed in code: `xtask/src/behave/space.rs` `kerr()` rejects
  `χ ∉ [0,1)` before any call.

*The named experiment 2 — the CYCLE_MAX cap.* Whirls built directly in (E, L): an unstable
circular orbit at r_s with E_c = 0.95 (bisected between r_ph and r_ISCO), L moved into the
bound window by 2⁻ᵏ. Truth: my own tanh-sinh quadrature **in u** with mpmath polyroots —
different substitution, quadrature and root-finding from the module's ψ-trapezoid and bisection;
the four deepest truths re-converged at dps 60 across three subdivisions (spread ≤ 2.2e-27).
χ = 0.998 prograde (full table in `work/cases.json`, probe output `probe-after-guard.txt`):

| k | u₃−u_peri | advance (truth) | module rel error | exit |
|---|---|---|---|---|
| 8 | 3.7e-2 | 63.3 rad | 9.0e-16 | agreed |
| 20 | 5.7e-4 | 200.9 rad | 6.5e-12 | agreed |
| 32 | 9.0e-6 | 338.9 rad | 7.2e-9 | agreed (biased) |
| 40 | 5.6e-7 | 430.8 rad | 2.2e-6 | agreed (biased) |
| 44 | 1.4e-7 | 476.8 rad | 5.6e-5 | **CYCLE_MAX** |
| 48 | 3.5e-8 | 522.5 rad | 2.3e-4 | **CYCLE_MAX** |
| 52 | 7.3e-9 | 575.1 rad | **1.1e-2** | **CYCLE_MAX** |

χ = 0.5 spot checks: 39.6 rad → 9.0e-9; 58.9 rad → 1.0e-4 (agreed-exit, no cap). Cap binding was
measured directly by a temporary probe print in `cycle` (removed; the mechanism is in the guard
now). Three findings, two of them beyond the checker's one-liner:
1. The cap binds at u₃−u_peri ≲ 1.4e-7 (advance ≳ 477 rad) and the error reaches 1.1e-2 at the
   deepest f64-representable whirl (at k = 56 the step L·2⁻⁵⁶ is 0.1 ulp of L, ulp = 2⁻⁵²,
   and rounds back onto the separatrix, so k ≤ 52 is reachable) — silent, as named.
2. A **bias band precedes the cap**: from u₃−u_peri ≈ 9e-6 upward the doubling loop can "agree"
   (increments below 2⁻³⁴) while the answer is already wrong by 7e-9 → 1e-4 — once the periapsis
   peak is narrower than the panel spacing, refinement barely moves the sum. The guard cannot
   catch this band; disclosed as residual.
3. The **exact separatrix point** (double root) does not error: `real_roots` splits the double
   root at grid scale (2⁻⁵⁰) and `cycle` returned a finite 625.5 rad for an orbit whose cycle
   never completes (homoclinic, Δφ → ∞). My prediction said it would error; it did not.

*The guard* (`work/guard.diff`, 19 lines on top of the run's patch): `isco` refuses a ∉ [0,1)
(`Err(Range)`); `cycle` refuses when the cap is reached without agreement. With the guard
applied: `isco(1, pro)` → `Err(Range)`; k = 44/48/52 whirls and both separatrix points →
`Err(Range)` (no silent numbers); **the eight-gate run is line-identical**
(`GATE_LINES_IDENTICAL_WITH_GUARDS`, `gates-guard.txt`), kerr tests 10/10, whole crate suite
green. The frozen gate domain sits far from all of this: its 1536 cycle seeds measured worst
2.0e-13 (converged at n = 32–256 against a cap of 2¹⁴), and the deepest gate-adjacent whirl
either checker probed (p = 1.001× separatrix, e = 0.9, outside the frozen domain) is ~104 rad
↔ u₃−u_peri ≈ 1e-2 — four orders of magnitude above where degradation starts.

**Predictions** (`predictions.md`, written before the probes). P1 held (≤ 1e-5 predicted,
worst 8.3e-9; a = 1 prograde 6.0 and retrograde 9.0 exactly as predicted). P3 held (grep proof,
no run needed). P2 held in its main bands (cap binds at δ = 2⁻⁴⁴, top of the predicted
[2⁻⁵⁶, 2⁻⁴⁴]; underestimate direction; hundreds of radians) and **missed twice, both
disclosed**: the exact separatrix returns a finite number instead of an error (finding 3), and I
predicted "exact ≤ 1e-9 until the cap binds" while a smooth bias band (up to 1e-4) precedes the
cap (finding 2).

**What would make it wrong.** My whirl truth shares the metric-level potential with the
author's generator (the independence is in quadrature, root-finding and parameterization); a
wrong potential would fool both. The frozen float64 oracle and the checkers' 30-digit BPT
anchors bound that risk to the whirl table, and the dps-60 cross-convergence of that table is
2e-27. The mechanical diagnosis is exact (grep + run.sh source), not inferred. The guard's
no-op-on-the-gate claim is measured, not argued.

**Cost of adopting.** For the integrator: the run's patch plus 19 lines. One protocol fix for
the lab owner (not mine to make): `run.sh` should read the second verdict from wherever it is
(`checker2-final.md`) or the checker prompt should require the literal line in `check2.md` —
otherwise every second checker who writes prose-first repeats this silver.

**Fit with PRINCIPLES.** "A failed expectation is not automatically a failed method: diagnose
which one broke" — the failed gold was one missing line, diagnosed to the exact grep. "Errors
never compound" and "floats never decide them" — the worst band now refuses to answer instead of
returning a degraded number ("the best part is no part"). "Certificates need independent,
adversarial checks" — the two-checker rule worked as designed; only its parser misread where the
verdict lived.

**The lens (second author) may have missed:** I did not re-run the 7 pre-existing xtask failures
(both checkers proved they pre-exist; nothing here touches xtask beyond the run's own adapter);
Carter's Q, the B9 crossing budget and M1 timings stay open as the author disclosed; and my
bias-band finding (2) suggests the deeper fix is a convergence certificate tied to the peak
width, not the cap alone — that is a design question for the motion-law owner, not this run.
