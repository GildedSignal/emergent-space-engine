# Predictions (second author, written before the decisive runs)

Task from the checker: (1) make the record regenerate (the weak-field control), (2) run the
named missing experiment — the visibility ladder (per-winding magnification vs observer
radius), (3) the jet probe's "complex root" was a coding slip (x = 1/L instead of 1/L², wrong
root picked); fix and rerun it. Nothing below is tuned; the ladder instrument does not exist
yet at the time of writing.

## Already measured while repairing the control (disclosed, not held out)

The shipped 0.018 does not regenerate (shipped code: 0.0, ray born below its own escape
cut). Diagnosis, already verified by running: 0.018 = 6×h — `total_phi` is step-quantized;
and the M=0 comparison ray is launched at a different b (b·√(1−2M/r_o) vs b), contaminating
the bend by ~2Mb/r_o² ≈ 4×10⁻⁴. The repaired control (launch r_o=998M inward at b=200M,
record the instrument's own interpolated outbound crossing of r=999M, both rays at the same
b) gives 0.020304, h- and R-converged, which is the Schwarzschild series
4M/b + (15π/4)(M/b)² + (128/3)(M/b)³ = 0.0200299 to 2×10⁻⁴ relative. Plain 4M/b is off by
+1.5% at b=200M — that is the real 2PN term, not error.

## The ladder (decisive): magnification per winding, static emitters, M=1

Instrument: same `trace` as view_images.py; images of emitter (r_e, φ_e) = crossings of the
exit-azimuth curve Φ(ψ) with levels φ_e+2πk (same side) and 2π−φ_e+2πk (mirror side);
magnification μ = |dψ/dφ_e| = 1/|dΦ/dψ| at the crossing; rel = μ/μ_brightest(φ_e).
Player-visibility threshold 1/50 (a 50×-demagnified image is sub-pixel for typical sprites).

- V1 (validation, r_o=10M, φ_e=π): same-k0 image at ψ ≈ 141.1° with μ ≈ 12.1; same-k1 at
  ψ ≈ 152.3° with μ ≈ 0.016 (checker's independent RK4); rel(k1) ≈ 1/740.
- V2 (validation, flat M=0): same-k0 μ equals the straight-line projection dψ/dφ_e to < 1%.
- L1: the brightest image at every (r_o, φ_e) is a k=0 crossing; windings k≥1 never dominate.
- L2 (r_o=100M): mirror-k0 (the Einstein partner) median rel 0.01–0.05, visible (>1/50) on a
  behind-the-hole band covering 15–50% of emitter azimuths; same-k1 median rel 1/300–1/2000,
  visible only within ~0.1–0.3 rad of alignment; k≥2 effectively invisible.
- L3 (r_o=10M): mirror-k0 median rel 0.3–0.9 (visible everywhere); same-k1 and mirror-k1
  median rel 0.005–0.05, visible on bands covering 5–50% of azimuths; same-k2 mostly below
  1/50 except near alignment.
- L4 (r_o=5M, 3.5M): k=1 families median rel 0.05–0.3; k=2 visible on bands ≥ 10% of azimuths.
- L5 (r_o=3.2M): k=1 median rel 0.1–0.6; k=2 median rel 0.02–0.2; k=3 visible somewhere;
  visible multiplicity ≥ 3 for ≥ 80% of azimuths at threshold 1/50.
- L6 (winding decay): median μ_{k+1}/μ_k per family between e^{−2π} ≈ 0.0019 and e^{−π} ≈
  0.043, with the ratio growing (slower decay) as r_o → 3M.
- L7 (the cutoff the memo needs, thr = 1/50): 100M → k=0 both sides only; 10M → k ≤ 1 both
  sides; 5–3.5M → k ≤ 2; 3.2M → k ≤ 3. Sheet count ≤ 2(K+1) with K ≤ 3 at every r_o ≥ 3.2M.
- Verdict: the claim survives with the cutoff quantified — at 100M the player-visible
  statement is "2 images on a behind-band, 1 off it" (exactly-once still visibly broken);
  at r_o ≤ 10M ≥ 2 images are visible ~everywhere and ≥ 3 on wide bands; a single-sheet
  deflection memo cannot express any of this.

## The jet probe (bands.py, fixed construction)

- J1: with x = 1/L² and the root nearest 1/p, all four p−p_sep ∈ {1.0, 0.5, 0.2, 0.1} at
  e = 0.9 give bound orbits (no complex roots). hL must adapt near the separatrix
  (L−L_sep ≈ 0.0014 at dp=0.1 < 1e-3·L): use hL = min(1e-3·L, 0.25·(L−L_sep)).
- J2: |d(Δφ)/dL| grows monotonically as dp → 0.1; ratio(dp=0.1/dp=1.0) ≥ 10
  (prediction D's jet holds; the VOID was the slip). Expected ~20–40 ((L−L_sep) ratio ≈ 24).
- J3: direct p-variation at fixed e (hp = 0.01): |d(Δφ)/dp| ratio(dp=0.1/dp=1.0) ≈ 8–12
  (1/ε scaling).

## What would make the claim wrong

If at 100M the partner band is empty (rel < 1/50 everywhere off exact alignment) AND k≥1 is
invisible at every r_o, then "once" would be player-visible-correct everywhere except a
measure-zero alignment set, and the finding demotes to "the invariant is wrong on a set of
measure ~0" — the memo would need only a k=0 partner sheet. If μ(k+1)/μ_k decays faster than
e^{−2π} uniformly, the tail is even cheaper than predicted and K shrinks by one everywhere.
