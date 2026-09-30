# Dossier: premise red-team on docs/representation.md (run 20260930-2250-redteam-03c8)

## Claim

The Binet-band law survives its strongest cheap falsifier almost everywhere — precession error ≤ 2×10⁻³ out to e = 0.95, r_p = 4.5, plunge classification 0/483 wrong, photon-capture b_crit to 1.5×10⁻⁴ — but it breaks r1's own 1% gate exactly where r1's sampler never looks (near-circular ISCO skimmers, up to 6.7%; the photon-ring sliver b ∈ (5.196, 5.22], up to 1.4%), and two of the six premises I was told to attack (dense/sparse bit-identity, the view gather) have no frozen rung at all, although §7 says all gates are frozen.

## Bottleneck

B0 (the representation) and the falsifier ladder itself. Gain: not a speedup — it prevents adopting a law whose failure region is invisible to its own gate. What it deletes: the belief that r1 PASS (H0204) covers the strong-field near-circular regime, and the §7 sentence "kill criteria are frozen" for r5/r6. Design consequence it points to: band width should be linked to the spacetime gradient (finer bands where ω_k = √(1−6u_k) → 0, i.e. at the ISCO and photon-sphere degeneracies) — precisely Julien's "sheets … whose size is linked to the spacetime gradient" (board, B0).

## Evidence

All float64, M = 1, RK4 in φ at h = 2×10⁻⁴ (halved step changes results at ≤ 1e−9: model error, not solver error). Model = r1's frozen Binet configuration, read literally (u_k = geometric band centre, u and u′ continuous across bands); oracle = exact Schwarzschild Binet u″ + u = 1/L̃² + 3u². Timelike seeds are turning-point pairs (u_p, u_a) — identical ICs and L̃ for both models; light launched from r₀ = 2000 with identical (u, u′).

Commands (cloud, Linux/x86, each ≤ 60 s):

```
cd lab/results/20260930-2250-redteam-03c8
gcc -O2 -o falsifier falsifier.c -lm && ./falsifier      # ~20 s -> run-out-v3.txt
gcc -O2 -o isco-scan isco-scan.c -lm && ./isco-scan      # ~17 s -> isco-out.txt
ls lab/rungs/                                            # r5/r6 absent
```

Numbers (m = 16 unless said):

1. **In-box control (r1's seed box: p ≥ 10, e ≤ 0.7): precession error ≤ 1.7×10⁻³ everywhere** — consistent with r1's PASS (H0204).
2. **High-e exotic corner is clean:** e = 0.95, r_p = 4.5 → 5.6×10⁻⁴; e = 0.9, r_p = 4.5 → 6.5×10⁻⁴.
3. **Near-circular ISCO plateau fails the 1% gate:** e = 0.02, r_p ∈ [5.9, 7.4]: 13/26 grid points > 1%, worst 6.7% (r_p = 5.96: banded 54.26 vs exact 58.13 rad/cycle); e = 0.05, r_p ≤ 5.96: up to 5.0%; e ≥ 0.1: ≤ 1.2%. r1 cannot sample this region: p ≥ 10 with e ≤ 0.05 puts r_p ≳ 9.7. At the separatrix (e = 0.02, r_p = 5.90) the banded orbit fails to complete a radial cycle at all (sticking) while exact captures.
4. **Error is non-monotone in m:** at e = 0.02, r_p = 6.02, m32 (3.0%) is worse than m16 (1.2%). The error is band-edge quantization noise, not smooth O(band²) — "raise m" is not the fix; gradient-linked band width is.
5. **Photon-ring sliver:** deflection error 1.4% at b = 5.205 (2.9 loops), 0.69% at 5.22, ≤ 0.2% for b ≥ 5.3 (m8: 5% at 5.205). r1 gates deflection only at b ≥ 10, where m16 measures 0. Photon-capture b_crit: banded 5.19535 vs 3√3 = 5.19615 (1.5×10⁻⁴) — capture is right, winding is not.
6. **Plunge classification: 0/483 disagreements** (e ∈ {0.05, 0.5, 0.95}, r_p grid 0.05).
7. **Carries vs contacts (bit-identity, premise 4):** sigma-delta on additive kicks is exactly order-independent in the emitted total (verified numerically; r2's "kicks accumulate exactly" generalized) — but same-cell simultaneous contacts give different bits under different resolution orders ((−1,−1,2,−4,8,3) vs (−4,−4,2,3,4,−1) in a 3-body demo). The design states no canonical tie-break for simultaneous same-cell events; the dense order resolves them in lockstep, the sparse order by slack.
8. **Gates:** `lab/rungs/` contains r1–r4, r7–r9. **No r5 (dense order) and no r6 (view)**, although representation.md §7 lists both and says the kill criteria are frozen.

## Predictions

See `predictions.md` (written before the decisive runs). Scorecard: P-A held (in-box ≤ 1.7×10⁻³). P-B failed in direction — I predicted high-e failure and measured a low-e ISCO plateau instead (my blind-spot warning applied to me). P-C partially held: the >1% light region exists but is a 0.3%-wide sliver in b, not a broad cliff, and b = 10 is clean. P-D mostly failed (good news): no misclassifications, b_crit excellent; only one sticking case at the separatrix. P-E held broadly (÷3–4 per m doubling) except near the ISCO, where scaling breaks down (finding 4).

## Ranked attacks (by how likely the player is to see the failure)

1. **Premises 4 and 5 are ungated.** r5/r6 do not exist. The view gather is on Julien's must-be-perfect list ("navigation, knowledge and dynamics those need to be perfect", OC#16); nothing catches a Newton-from-previous-frame wrong-root under burns (star popping). Criterion that should catch it: none — r6 itself must be frozen.
2. **Near-circular ISCO skimmers (premise 2 crack).** The player's natural "orbit as low as possible" around a black hole shows a visibly wrong rosette (loop count per radial cycle 8.6 vs 9.3 at e = 0.02, r_p = 5.96). Should be caught by r1 `prec` — the criterion is right, the sampler cannot reach the region. Fix: r1 v2 adds e ∈ {0, 0.02, 0.05} × r_p ∈ [5.9, 7.6].
3. **Photon-ring winding (premise 2 crack, light).** Multi-image spacing near the ring edge wrong by >1% for m16. Should be caught by r1 `defl` — sampled only at b ≥ 10. Fix: extend the light grid to b ∈ [5.20, 6].
4. **Same-cell simultaneous contacts break bit-identity (premise 4).** Measured different bits per order. r5, when frozen, needs a simultaneous-triple negative control and the design needs a canonical tie-break.
5. **Order-transition thrash (dense ↔ sparse at Knudsen ≈ 1).** Unstated hysteresis; re-packing on every flip is a p99 risk ("i care about the p95/99 results", CL 09-25). No rung measures it.
6. **Kick-by-multiply-add is worst where cycles are wrong (premise 3 aggravation).** At e = 0.02 the exact Δφ moves 58.1 → 28.4 rad as r_p goes 5.96 → 6.2: ∂Δφ/∂E is huge on the plateau, so stored cycle derivatives misprice kicks exactly there. Partially gated by r4 v3/r9 (away from ISCO).
7. **EOB at 1PN (premise 1) survives as gated** (r3 v3: ν only in the energy map, assists 64/64). Residual risk only for strong-field comparable-mass binaries (a merger spectacle). Exotic; leave.
8. **Phase drift of the integer law.** Amplitudes are safe (carries exact, order-free), but bounded per-event quantization still walks longitude ~linearly with event count; r1's `repeat` gates within-orbit identity, not cross-orbit phase. Long-session eclipse timing. Mild; name it in the error model.

**Premises that survive with numbers:** premise 2 in the broad domain (findings 1–2, 6), premise 6 as an estimate (§6's largest line, AI decisions, is off-plan since 30 September — stale, not false).

## What would make it wrong

My banded model is r1's configuration read literally; an implementation that subdivides bands near ω_k → 0 would shrink the plateau (that is the proposed fix, not the current spec). The oracle is the exact Binet equation in the equatorial plane — the same family r1's `periapsis_elliptic` oracle uses; a checker should re-derive with the crate oracle. Floats explore, integers decide: these numbers size the crack, the rung decides it.

## Cost of adoption

r1 v2 seed-grid extension: one file, cheap, frozen before any rerun (a v2 freeze is the integrator's call). Gradient-linked band width near degeneracies: a design decision for the integrator, one step, no new machinery (the ring tree already knows ω_k per band).

## Fit with PRINCIPLES

- "Gates are frozen before the first run and never weakened after" — §7 names r5/r6 as frozen; they do not exist.
- "Behaviours matter, not continuum fidelity: error type over error size" — the ISCO error is a behaviour error (rosette loop count, orbit lifetime at the separatrix), which is why it is worth a rung even at 1%.
- "Measure before claiming, and never strawman" — the law was measured on its own frozen configuration, at turning-point-consistent seeds (the first version of my harness mis-seeded; v2/v3 corrected it before any conclusion was drawn).

## The lens

A premise red-team overweighted exotic cases and was corrected by its own measurements (high-e came back clean; the crack is in the mundane "fly low around a black hole"). What this lens missed: no numeric falsifier was run for the view gather (r6) or the allocator — both named here and cheaper to attack fresh than to half-do late; and everything is equatorial 2D float64, orders of magnitude only, per the lab README.
