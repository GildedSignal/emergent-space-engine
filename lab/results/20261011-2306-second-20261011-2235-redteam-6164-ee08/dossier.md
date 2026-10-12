# Dossier — 20261011-2306-second-20261011-2235-redteam-6164-ee08 (lens: second author)

## Claim

The parent's claim survives its checker's named experiments and is now stronger on a fully
regenerating record: the kick jet's ("a kick updates the cycle by a multiply-add",
`docs/representation.md` §3) validity domain is a corner **for every spin state** (equatorial
Kerr prograde χ ∈ {0.5, 0.9, 0.998} shows the same logarithmic separatrix divergence and the
same categorical encounter-kick failure as Schwarzschild, with whirls up to 7× longer), the
parent's channel decomposition was **inverted** (the period's Kepler binding-energy
curvature (15/8)·(δE/(1−E))² dominates the belt grid; the precession-phase channel it blamed
is flat at ~3.5·10⁻¹²), and premise 4's gap is narrower than reported (the r5 substance — CW
frame + contacts + sparse/dense bit-identity — passes as existing crate tests; only the
frozen rung is missing).

## Bottleneck

Same as the parent (board focus "fewer kicks per orbit" / smoothness p99): the jet's
recompile rate must be scheduled by certificate, not paid as surprise. What this run adds:
the certificate must be a root-distance check at **both ends of the bound band** — the
plunge double-root (now measured for χ ≠ 0) and the E = 1 (escape) edge, because the
corrected decomposition shows the belt-scale failure IS the near-escape divergence of the
same period curvature (1−E ≈ 1/r_apo), not a separate precession mechanism. In u-space the
check is one rule: distance from the kick's landing point to the nearest root of R
(u_a → 0 is the escape edge), all roots darwin16 already factors.

## Evidence

All numbers regenerate from the run folder (`python3 probe.py` first: 4 s, byte-identical
to the parent's `probe_out.json`; then six parts, each a separate command so no part
exceeds the machine's patience; merge last):
```
python3 probe.py                                   # 4 s, parent record, bit-identical
python3 probe2.py A                                # ~60 s
python3 probe2.py a0    && python3 probe2.py a05  \ # ~90 s / ~3 min
python3 probe2.py a09   && python3 probe2.py hcheck # ~4 min / 6 s
python3 probe2.py a0998lite                        # 143 s (see below)
python3 probe2.py merge                            # writes probe2_out.json
cargo test -p emergent-lattice-event --test equality   # 173 s, 10/10 pass
cargo test -p emergent-engine --test identity          # 472 s, 9/9 pass
```

The five probe2 parts are separate commands because the a = 0.998 whirls are long (its
full sweep ran past 12 min single-threaded and was killed by the run budget twice; the
committed `a0998t` command is that full sweep, for the next run). `a0998lite` is the
decisive minimum at χ = 0.998: the full ε = 10⁻³ row, the whirl at ε = 10⁻⁶, and the
E-kick band.

Oracle: equatorial Kerr timelike geodesics, M = 1, prograde, from the exact first-order
form (du/dφ)² = u⁴Δ²R/Dφ² differentiated once (u″ = F′(u)/2, F built in sympy, lambdified);
same RK4-in-φ cycle, derivative and jet machinery as the parent's Schwarzschild probe.
**Control (P7):** at a = 0, r_c = 5 the machinery reproduces the parent's P3 sweep to ≤
1.0·10⁻¹² (dphi, T) and ≤ 1.1·10⁻¹⁰ (|∂T/∂E|); the circular solver returns exactly
√(9/10), √(25/2). Kerr h-refinement (h = 10⁻³ vs 5·10⁻⁴, ε = 10⁻³): Δφ/T agree to
9.5·10⁻¹³ / 7.2·10⁻¹³ (a = 0.9) and 3.3·10⁻¹³ / 2.3·10⁻¹³ (a = 0.5) — five orders below
the smallest measured effect at that ε.

1. **Record regeneration (the checker's first miss).** Precession ratios (Δφ−2π)/(6π/p),
   e = 0.5: **1.048104 / 1.009220 / 1.004586** at p = 100/500/1000 — the dossier's cited
   1.0481/1.0092/1.0046 and the checker's 1.00922/1.00459, now in `probe2_out.json`.
   Saturation at r_apo = 2000, α = 10⁻⁶: **N_floor = 1 measured** (first kick already
   7.57·10⁻⁶ > floor), compiles/kick = **1.0**; the dossier's "2.8" is the uncapped formula
   1.4·10³·r_apo·α, which caps at 1 — the physical statement "every kick recompiles" is what
   the record now carries. L-channel: 7.54·10⁻¹² against the oracle's own h-refinement
   noise 2.0·10⁻¹² at the same point — "harmless, at the noise floor", as the checker put
   it.
2. **The decomposition correction (P8; held).** Per-channel jet errors for the parent's
   P1 grid, α = 10⁻⁶ on E: the **T-channel is the parent's headline number at every point**
   (r_apo = 10⁴: T = 1.887·10⁻⁴, dφ = 7.3·10⁻¹⁴; r_apo = 2000: 7.57·10⁻⁶ vs 3.6·10⁻¹²;
   r_apo = 22: 2.95·10⁻⁹ vs 3.5·10⁻¹²), and it tracks the Kepler binding-energy curvature
   **(15/8)·(δE/(1−E))²** within 1–9% at all ten points. The parent's claimed mechanism
   ("the corruption is the precession phase", 4·(α·a)²) is the *small* channel — flat at
   ~3.5·10⁻¹² across r_apo = 22 → 2000 at p = 20 — and its "T-channel remainder is
   r_apo-free (Kepler gives 15/4·α²)" is backwards: the T-channel is the one carrying the
   (α·r_apo)² growth, through 1−E ≈ 1/r_apo. The checker's 15/8 coefficient was right but
   inherited the conflation (1.875·10⁻¹² is 15/8·α² evaluated, not a measured channel).
   **The headline is unchanged** — err ≈ (15/8)·(α·E/(1−E))² ≈ 1.9·(r_apo·α)², so the
   validity condition r_apo·α < 4·10⁻⁴ stands — but the mechanism is now identified, and
   it unifies the two failure families: the belt failure is the near-escape edge of the
   same period-curvature divergence that blows up at the plunge separatrix.
3. **Kerr separatrix (P5, P6; the named experiment).** Fixed L = L_c of the unstable
   circular at r_c, E = E_c(1−ε), prograde:

   | spin | r_c | Δφ(ε=10⁻³→10⁻⁶) rad | \|∂T/∂E\| at ε=10⁻³ | kick α=10⁻⁶ at ε=10⁻⁴ / 10⁻⁶ | α=10⁻³ at ε=10⁻³ | α=3·10⁻³ |
   |---|---|---|---|---|---|---|
   | 0 (parent) | 5 | 15.5 → 30.6 | 2.8·10⁴ | 5.5·10⁻⁶ / 0.47 | 43% | plunge |
   | 0.5 | 3.5 | 17.6 → 34.5 | 1.9·10⁴ | 5.3·10⁻⁶ / 0.46 | 42% | plunge |
   | 0.9 | 2.0 | 26.1 → 53.7 | 1.7·10⁴ | 5.7·10⁻⁶ / 0.47 | 44% | plunge |
   | 0.998 | 1.15 | 84.2 → 215.3 | 5.8·10⁴ | — / — (lite) | 52% | plunge |

   At χ ∈ {0.5, 0.9} (and the parent's χ = 0) the full sweep holds: |∂T/∂E| grows 10× per
   decade of ε (logarithmic divergence: e.g. a = 0.9, 1.7·10⁴ → 1.7·10⁷ from ε = 10⁻³ to
   10⁻⁶); a quantum kick breaches the 10⁻⁶ floor by ε = 10⁻⁴ (5.3–5.7·10⁻⁶) and errs ~50%
   at ε = 10⁻⁶; encounter-grade E-kicks (α = 10⁻³, the mild end of B13's assist band) err
   42–52% at ε = 10⁻³, and α = 3·10⁻³ exits the bound family at every spin
   (plunge-after-kick): the multiply-add updates a cycle that no longer exists. At
   χ = 0.998 the lite part carries the decisive content (full ε = 10⁻³ row incl. |∂T/∂E|
   = 5.8·10⁴, already 2× the Schwarzschild value at the same ε; quantum kick 1.05·10⁻⁷
   there; encounter band 52% / plunge / plunge; whirl growth 84.2 → 215.3 rad); its
   deep-ε rows are the named open case (the committed `a0998t` command runs them).
   **High spin does not shrink the failure band** — the whirl is longer at every ε, by 7×
   at χ = 0.998 (P6). B19 gates Kerr *behaviours* (precession, classification, frame
   dragging); no gate mentions recompile, jet, separatrix or root-distance (regenerated:
   21 gates checked, zero hits), so the jet's domain is unguarded at every spin.
4. **Premise 4, probed (the checker's "a probe was owed").** The parent called dense/sparse
   bit-identity "UNGUARDED" on a doc-level finding (r5 absent). The probe: the r5
   *substance* already exists as crate tests and passes on this machine —
   `lattice-event/tests/equality.rs` (sparse `EventCore` vs dense `Chronon` reference:
   identical world/log digests and sorted events, with contacts, across generators, sizes,
   horizons, budget slicing, snapshots; **10/10**) and `engine/tests/identity.rs` (the same
   battle in a free-fall/CW frame with contacts, lockstep vs sparse, world/log/tide
   digests, eight scenes up to a 1-chronon-epoch storm, plus a planted-late-kick negative
   control; **9/9**). What remains missing is the frozen rung (r5 is still absent from
   `lab/rungs/` — regenerated) and the GPU leg (`metal_identity.rs` is macOS-only; this
   Linux box has no Metal device, so the third order is untested here). The gap is a
   ladder formality plus GPU coverage, not a missing check — the parent's wording ("B8
   gates bit-identity at law level, but r5 does not exist") was accurate; its lens section
   ("got a doc-level finding where a probe was owed") is now paid.
5. **Doc-level findings regenerate from the tree** (scripted in `doc_check`, all true):
   Minsky's map is still named "the primary in-cell solution" in `representation.md` while
   `law.md` records its replacement by `space-darwin16-v1`; r5/r6 are still named in §7's
   ladder and still absent from `lab/rungs/` (frozen: r1–r4, r7–r10); the re-anchor
   trigger still reads drift-only ("accumulated offset reaches √(floor/C)") with no
   separatrix term. The two one-paragraph fixes remain the integrator's.

## Predictions
`predictions.md` was written before the decisive run. **P5 held** at χ ∈ {0.5, 0.9} in
full (10×-per-decade divergence, floor breach by ε = 10⁻⁴ at 5.3–5.7·10⁻⁶ vs the predicted
"by ε ≈ 10⁻⁴", ~50% at ε = 10⁻⁶, 42–44% at α = 10⁻³, plunge at α = 3·10⁻³) and at
χ = 0.998 in its decisive part (52% at α = 10⁻³, plunge at 3·10⁻³, |∂T/∂E| = 5.8·10⁴ at
ε = 10⁻³); its deep-ε rows are named open. **P6 held** (whirl monotone in spin at both ε:
15.5 → 17.6 → 26.1 → 84.2 rad at ε = 10⁻³, 30.6 → 34.5 → 53.7 → 215.3 at ε = 10⁻⁶; the
failure band does not shrink). **P7 held with margin** (≤ 1.1·10⁻¹⁰ vs the predicted
10⁻⁹). **P8 held** — the parent's decomposition is inverted exactly as predicted: the
T-channel dominates every grid point and tracks (15/8)·(δE/(1−E))² within 1–9%; the
"r_apo-free" claim fails on the T-channel (it is the precession channel that is flat,
~3.5·10⁻¹² across r_apo = 22 → 2000 at p = 20). Two of the parent's own four predictions
had failed in the informative direction; this run's correction of its derivation is the
same pattern — reported as a correction, not a confirmation. **P9 held** (ratios, saturation
N_floor = 1, doc checks all regenerate). Not run, costed in `predictions.md`: the
integer-law rerun (a rung on `space-darwin16-v1`, the integrator's call), the GPU leg of
premise 4 (no Metal device on Linux), and the deep-ε rows at χ = 0.998 (`a0998t`).

## What would make it wrong, adoption cost, PRINCIPLES fit

Wrong if: the law's kicks were L-dominant in practice (measured L-channel at the belt is at
the oracle's own noise floor, and the L-kick separatrix errors are 2–80× smaller than the
E-kick at every spin and ε — the E-channel is the envelope); if the float α-mapping is
inapplicable to the integer law (unchanged from the parent — floats explore here, the rung
decides); if the Kerr whirl structure had a second separatrix family the sweep missed
(retrograde and χ < 0 are untested; B19 tests both senses, the certificate derivation should repeat for
retrograde). Adoption cost: unchanged from the parent and slightly sharpened — one
root-distance rule at both ends of the bound band (roots darwin16 already factors;
u_a → 0 is the escape edge), plus one criterion in the kick rung, plus B19 gaining a
recompile-rate criterion now that Kerr's jet domain is measured. Fit — principle 13:
"basically we don't want errors that can compound that's the goal": the jet honours it
only inside a domain whose border is now measured at every spin; principle 21: "rough
first, refine when a certificate could break… simple and powerful": the both-ends
root-distance check is that certificate, and it is *simpler* than the parent's proposal
because both failure families are one mechanism; principle 19: the corrected decomposition
is the wrong-representation signal working — the parent's precession-phase story was a
bandaid explanation for a number whose real cause (period curvature in binding energy)
was hiding in plain sight.

## The lens

A second author inherits the parent's frame; what I checked beyond it: the decomposition
(P8) because the checker's 15/8 correction smelled like a formula evaluation rather than a
measurement — it was, and the parent's mechanism attribution was inverted. What this lens
may have missed: retrograde Kerr (the prograde-only sweep follows B19's prograde rows;
retrograde separatrices sit farther out and whirl differently); the ISCO-seed analogue for
Kerr (r1's seed is Schwarzschild; where B19's 256 seeds sit relative to the Kerr separatrix
band is unmeasured); Kerr T-channel belt grid (the (15/8)(δE/(1−E))² law was verified on
the Schwarzschild grid only — frame dragging adds an a-dependent period term at small
p that could matter below p ≈ 10); and the integer-law rerun remains the integrator's to
freeze.

## Files

`probe.py` (parent, untouched — byte-identical reproduction), `probe2.py` (parts A/a0/a09/
a05/a0998lite/a0998t/hcheck/merge), `probe_out.json`, `probe2_part_*.json`,
`probe2_out.json` (merged record), `predictions.md` (pre-registered),
`predictions-original.md`, this dossier. Machine: shared cloud Linux runner, 8 vCPU,
15 GB, loadavg 0.9–1.4 during the runs (four sibling probe2 parts shared it at times;
every process ≤ 200 MB). Cloud timings are Linux/x86: orders of magnitude only.
