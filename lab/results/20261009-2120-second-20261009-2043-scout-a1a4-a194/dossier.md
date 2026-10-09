# Dossier — 20261009-2120-second-20261009-2043-scout-a1a4-a194 (second-author lens on 20261009-2043-scout-a1a4)

**Claim.** The first run's claim — the law's whole `NoBoundOrbit` gap compiles into the
ψ-panel tube, exact to ~10⁻¹⁰ with O(1) readout — **now holds on the shipped record
with the checker's named experiment done**: the honest readout (bracket + Newton-in-ψ,
the mechanism P4 predicted, not the linear interpolation that was timed) sits at the
compiled table's own error floor in every case and across the winding sweep
|1−L/L_c| = 10⁻³…10⁻⁷, at 27 µs/sample in pure Python and **0.53 µs/sample compiled**
(C, `-O2`), winding-independent (sweep max/min = 1.014). The "3 µs" headline number is
retired: it measured a linear readout whose accuracy is 10⁻⁵…10⁻⁷ (10⁵–10⁹× above the
table floor). The near-critical column is restated against a reference now confirmed
**three independent ways**, which also closes the first run's last open flag (the
mp40 kink) non-circularly.

**Bottleneck.** Same as the first run (`b-plunge-tubes`, queue item 3): capture orbits
stop being stepping physics and become one compiled object. The named gap between
silver and gold was the record, not the physics; this run closes it and measures what
the readout mechanism actually costs and delivers per sample.

**Evidence** (commands, each ≤ 5 s on this 8-vCPU runner, load 0.1–0.4; all in
`work/`; first run's `plunge_falsifier.py`/`plunge_cost.py` imported unmodified and
still regenerate their record):
```
cd lab/results/20261009-2120-second-20261009-2043-scout-a1a4-a194/work
python3 plunge_record.py   # P3 + restated column + 3-way adjudication, 2.1 s
python3 plunge_readout.py  # honest readout: accuracy+cost, cases+sweep, 3.1 s
cc -O2 -o plunge_readout_c plunge_readout_c.c -lm && ./plunge_readout_c  # 2.6 s
```

1. **Honest readout accuracy — at the table floor everywhere** (`readout-output.txt`).
   Newton-in-ψ (bisect bracket, linear start, 3 safeguarded iterations, local GL4)
   vs the independent backward-from-horizon DOP853 oracle, 512 random τ targets per
   case, floor = the tube's own edge values vs the same oracle (128 edges):
   case C r/φ/v = 1.1e-13/2.2e-11/3.5e-13 vs floor 1.1e-13/2.3e-11/3.6e-13; the same
   equality holds for A, B, D (1.3e-10 φ), E (γ=2000), F (L=0), G (photon, by φ), and
   sweep k=3…7 — at k=6/7 the readout *inherits* the table's degradation exactly
   (4.8e-4/4.2e-1 vs floor 4.8e-4/4.4e-1 in φ). Summary line: all cases at floor
   (≤5×): **YES**. The shipped linear readout on the same targets: 5.5e-7 (A) …
   2.3e-2 (k=7), 10⁵–10⁹× above floor — that is what 3.08 µs bought.
2. **Honest readout cost.** Pure Python: 25.3–28.1 µs (L>0), 10.5 (L=0), 18.0
   (photon); sweep k=3…7: 27.55–27.93 µs (max/min **1.014** — winding-independent).
   Compiled C, same algorithm translated mechanically, semantics bit-identical to the
   Python reader (probe abs diffs 0.0): **530 ns** (case C) / **534 ns** (k=7) per
   sample over 2×10⁶ readouts — ~13,000× under DOP853 re-integration (7.3 ms,
   nfev 782). P4's "< 20 µs" misses by 1.3× in pure Python and passes by 34×
   compiled. Three Newton iterations converge to machine level at k≤5
   (|u₃−u₅| ≤ 4e-16); at k=6/7 the residual (4.6e-10/4.8e-6) sits ≥4 orders below
   the table's own error there; a 4th iteration costs +5 µs Python.
3. **P3 record shipped** (`plunge_record.py`): the missing script for run-output.txt
   lines 23–29. Pair-b column (the claim-bearing conditioning law) regenerates ≤1%
   at every k (exact to the printed digits at k=4–8; 0.2–0.4% at k=2–3). Pair-a
   regenerates to ~1 ulp (diffs 4.3e-17…1.1e-18); the recorded ulps are not
   recoverable on this runner — plain mp.polyroots at dps 40/50, monic form, and a
   deflated-cubic truth were all tried (deflation breaks the b match, pinning the
   author's method); the residual is cross-machine LAPACK dispatch noise in
   np.roots, disclosed.
4. **Prose numbers fixed.** Pair coalescence is b ∝ **√δ** (fitted log₁₀b-vs-k slope
   −0.5001, k=3…7; the dossier said δ). Lcrit(2000)/(3√3·2000) deviates by
   **3.947e-8** (the checker's 3.95e-8; the dossier's "2×10⁻⁹" was wrong by 20×).
5. **Near-critical column restated, and the reference triple-verified.** Restated
   512-panel Δφ errors: 5.8e-15, 6.6e-15, 5.5e-15, **1.5e-12**, 4.16e-7, 1.79e-4,
   7.45e-3 (k=1…7). Two upgrades over both the first run and the checker: (i) the
   shipped k=4 entry (1.665e-8) was also mp40 artifact — the true k=4 error is
   1.5e-12, which is root-precision-limited (P3's pair-b relerr there is 9.65e-13:
   cross-consistent); (ii) the k=7 Δφ dispute is adjudicated by a **third,
   structurally independent form** — u = a + b·tanθ removes the coalescence peak
   entirely (no endpoint-peaked integrand, unlike both split schemes) — giving
   23.841746, agreeing with the ψ-split and the ODE-oracle total to 6 decimals at
   every k, against the tube's 24.019348 (error 7.45e-3, as restated). The +3.2563
   (√2·ln10) per-decade law holds through k=7. The checker's resolution had leaned
   on split + asymptotic (circular); now it is closed without circularity.
6. **New measured fine print near critical:** per-sample table accuracy degrades
   faster than end-value accuracy — at k=5 the end error is 4.2e-7 but the worst
   per-sample φ error is 6.0e-4 (1400×); at k=6, 1.8e-4 vs 0.44. Panel growth
   ∝ ln(1/δ) (log-cheap) must be sized per sample, not from end values. The
   tube's τ-cumulative also mislabels ψ across the spike (all three table integrals
   inherit the under-resolution).

**Predictions.** [predictions.md](predictions.md) written before both scripts ran.
PR1 (readout at floor): **held** (all cases). PR2 (<20 µs pure Python): **missed by
1.3×** (25.3–28.1 µs); winding-flatness held (1.014); 3-iteration convergence held at
k≤5, not machine-level at k=6/7 but consequence-free there; compiled 0.53 µs. PR3
(linear readout ≥100× floor, growing with winding): **held** (up to 10⁹×; 390×
growth k=3→7). PR4: P3 b-column, slope, and checker agreement **held**; "shipped
column correct at k≤4" was **wrong at k=4** — in the interesting direction (the
shipped entry was reference artifact; the truth is 4 orders lower and
root-limited). PR5 (both prose numbers): **held**.

**What would make it wrong.** The float shape is still verified, not the integer
law: the proven B₈ quadrature bound must be re-derived for the new integrands, and
per-sample panel sizing near the coalescence (finding 6) is now a measured
requirement on the build. The readout was measured in ψ-uniform panels; whether the
law's geometric u-bands hold the bound at the spike without panel growth remains
untested (unchanged from the first run). Kicks mid-plunge force recompiles (0.55 ms
float, integer path unknown); absorption at a star surface (u_stop < 1/2) untested.
Cost of adopting: unchanged — one new substitution + anchor form in `crates/space`'s
compiler, i.e. the `b-plunge-tubes` step with the representation now chosen and the
readout contract now honest (floor-limited, sub-µs compiled).

**Fit with PRINCIPLES.** "Exact means deterministic and reproducible" — the readout
error is the table's own error, the same shape every sample, no compounding;
"Store the generator, not the generated" — one (E, L) compiles to a table, readouts
are derived; "Measure before claiming" — the 3 µs claim is replaced by measured
numbers for both mechanisms; "agreement is not independence" (lab lesson) — the k=7
reference needed a third form, and two shared-flawed schemes agreeing was exactly
the trap.

**The lens.** The second-author lens optimized for closing the checker's list; what
it may have missed: no adversarial *readout* cases beyond the sweep (e.g. targets
packed inside single spike panels), no measurement of compile cost at panel counts
that fix k=6/7 per-sample accuracy (n ∝ winding was inferred from end values in the
first run and from per-sample floors here, not measured at the larger n), and the
C harness times the algorithm, not the engine's memory layout (table access
locality, 513-entry bisect in cache).

Wall time: 0.06 s
