# Dossier — 20261008-1419-second-20261008-1337-redteam-2040-9a04 (second author)

**Claim.** With the checker's named experiment done, the original run's claim holds on
the shipped record in completed form: the §3 multiply-add kick update fails by type on
the E axis too and on **both sides** of the bound region — E-kick plunge (the separatrix
tilts, dL_sep/dE ≈ 18) and escape past E = 1 — with a measured E-axis law
relerr(T_t) ≈ C·(dE/(1−E))², C = 1.85→1.66 (Newtonian limit 15/8), slope 1.979,
scale-free to 1% when 1−E halves, and 1.2×10⁸ stiffer in T_t than the matched dL kick;
and the completed exact tri-predicate — **bound ⇔ E<1 ∧ three real roots ∧ middle root
>2M; escape ⇔ E≥1 ∧ three real roots; plunge otherwise** — agrees with an independent
grid truth 3600/3600 and with 11/11 directly integrated orbits, which makes the proposed
rung criterion complete and freeze-ready for `b-plunge-tubes`.

**Bottleneck.** Unchanged from the original run (kick cost, board focus #1;
`b-plunge-tubes` in flight, the plane currently refuses these orbits). What this run
adds: the refusal boundary of the only cheap kick path is now measured on **both**
invariant axes, and every number in the chain — oracle, validation, predicate —
regenerates from shipped code.

**Evidence** (each command ≤ 60 s, one process; host: 8-vCPU shared runner, load 0.31,
13.9 GB available; timings not load-bearing):

```
cd lab/results/20261008-1419-second-20261008-1337-redteam-2040-9a04
python3 falsifier.py        # 22.9 s — original record reproduces bit-for-bit (JSON diff clean)
python3 falsifier2.py       #  1.5 s, 38 MB — the E axis (this run)
python3 validate_oracle.py  # 10.4 s, 67 MB — shipped RK4-Binet + DOP853 + predicate ground truth
```
All outputs deterministic (md5-identical on rerun; no RNG).

- **E1** weak field (peri 50, apo 200), dE/E = 1e-4: relerr(T_t) = **1.154×10⁻³**,
  relerr(Δφ) = 1.05×10⁻⁹ — reproduces the checker's D1; axis stiffness
  err_E(T_t)/err_L(T_t) = **1.19×10⁸** at matched fractional kick (P1's dL/L = 1e-4
  gives 9.7×10⁻¹²). The T_t certificate must be in the error map; Δφ is E-flat.
- **E2** strong field p = 12, dE/E = 1e-4: relerr(T_t) = 2.56×10⁻⁵.
- **E3** E-scan, f = dE/(1−E) ∈ 3×10⁻³…0.3 (weak field): relerr(T_t) = C·f², fitted
  slope **1.979** (Δφ slope 2.000 but 5–7 orders smaller); C drifts 1.85→1.66; the 1%
  T_t band breaks at **f ≈ 0.075**, i.e. |dE| ≈ 0.075·(1−E).
- **E4** scale-free: same f at 1−E halved (peri 100, apo 400) → errors agree to
  **1.0–1.1%**. The dimensionless reading (principle 4) holds on the E axis.
- **E5** plunge-via-E (E = 0.97, L = L_sep·1.001, dE = +10⁻³): truth PLUNGE — confirmed
  by direct proper-time integration (r → 2.05, no turn) — while the multiply-add
  fabricates Δφ = 19.49, T_t = 613 (= the checker's D2). Predicate3: plunge, correct.
- **E6a** escape (weak-field orbit kicked to E = 1.02, L ≫ L_crit): truth ESCAPE;
  fabricated Δφ = 6.55, T_t = 89,621 (= the checker's D3); the **original `is_bound`
  returns True** for this hyperbolic orbit — its crash path, exercised safely here;
  predicate3: escape, correct.
- **E6b** E = 1.005 with L = 3.996 < L_crit(1.005) = 4.04: truth **PLUNGE, not
  escape** — E ≥ 1 does not imply escape; fabricated T_t = 7.04×10⁵. Both predicates
  say plunge (the original's failure mode is only the escape side).
- **E6c** E = 1.005 with L = 4.2 > L_crit: escape just above the barrier; original
  predicate wrong again; predicate3 correct. (E6b/E6c fabricated T_t ≈ 7×10⁵ both:
  near E→1 the stored ∂T_t/∂E ∝ (1−E²)^(−5/2) saturates any fixed-width store — the
  original's saturation note, now measured.)
- **V1** RK4-Binet shipped (p ≈ 80): relerr(Δφ) = **3.95×10⁻¹²**, relerr(T_t) =
  **6.31×10⁻⁷** at 400k steps, Richardson step consistent with 4th order. The
  dossier's unregenerable "2×10⁻⁴" claim regenerates as an upper bound.
- **V2** DOP853 proper time, apo→peri→apo: relerr ≤ 6×10⁻¹³ on weak, strong and
  near-separatrix seeds — the quadrature oracle confirmed far tighter than the
  checker's 2.5–5.3×10⁻⁶. Exact Δφ at p = 80 = 6.533267 → advance 0.25013 vs 1PN
  0.2356 (6%): the author's quoted pair regenerates.
- **V3** tri-predicate vs independent grid truth (sign scan of E²−V² on 120k points,
  no cubic solver; 3660 samples): **3600/3600 agree**, 60 margin-excluded (1.6%:
  near-double roots, |1−E| < 5×10⁻⁶, band pericentre within 10⁻⁴ of 2M).
- **V4** eleven orbits integrated with terminal events: **11/11** — 4 bound turn at
  the predicted band (r_end 200/30/991.6), 4 escape past 10⁴, 3 plunge through r =
  2.05, including E5's kicked invariants.

**Predictions.** [predictions.md](predictions.md), written before both decisive runs.
**All twelve held** (E1–E6c, V1–V4), including the genuinely blind ones: the E2 value
(predicted [10⁻⁶, 2×10⁻⁴], measured 2.6×10⁻⁵), the exponent 2.0 ± 0.1 and break at
f ∈ [0.04, 0.12], the scale-free agreement, E6b's plunge-not-escape, and V3's zero
disagreements. The original run failed 2 of 5; the physics anchors written into the
predictions ((15/8)·(dE/(1−E))², dL_sep/dE ≈ 18, L_crit(1.005) = 4.037) all measured
out. Two mechanical script bugs were fixed mid-run, both **before** any held-out number
existed: a print-key KeyError that crashed E5 after E4, and the Binet loop capturing
`w_prev` after the state update (plus its crossing-direction sign). Neither touched a
measurement; reruns are bit-identical.

**What would make it wrong.** If every kick were classified first by the tri-predicate
on the kicked invariants, no fabrication can occur and both runs reduce to a cost note:
the multiply-add stays valid only inside its stored cycle's certificate, whose widths
are per-axis and measured — |dE| ≲ 0.075·(1−E), |dL| ≲ 0.4·δ_L at the 1% band (E-axis
scan here; L-axis from the original). The predicate is a sign test on the cubic's root
structure — exactly decidable in integers (Sturm/Descartes), one cubic per kick, no
solve. What falsifies this dossier: a predicate disagreement with the grid truth or an
integrated orbit (none in 3611 trials), or the fabricated cycles being benign (V4 says
they mislead on both sides of the bound region). 2D equatorial Schwarzschild, ideal
float derivatives of the exact map, instantaneous (E, L) kicks — §3's own model; the
shipped integer store can only be worse (derivatives diverge at both boundaries).

**Cost of adopting.** Same as the original plus the completion: one exact tri-predicate
per kick near the edges replaces the recompile there (a handoff to the plunge tube or
the escape path), per-axis certificate widths ride along with the stored derivatives,
and the T_t derivative needs width headroom near E → 1 ((1−E²)^(−5/2), the E6b/E6c
7×10⁵ fabrications). Deletes the per-kick recompile everywhere else.

**Fit with PRINCIPLES.** Principle 2, "error type over error size": the kill is a type
error, now on both invariant axes and both sides of the bound region. Principle 13,
"errors never compound… divergence is not a joke": a fabricated cycle (or a fabricated
escape for a plunging orbit) is divergence handed to the player as an orbit. Principle
19, "a fix signals the wrong representation": the fix is not a patch on the derivative
but the exact classification the invariants already carry — measured complete here.

**The lens: what this lens may have missed.** The second-author lens inherits the
original's frame and the checker's axes, so it cannot see what neither named: the
coupled regime near the separatrix, where an E kick acts on δ_L through the tilt
(dL_sep/dE ≈ 18) and the clean f² law is only the far-field limit (E2's error is a mix;
no scan of that coupling was run); the response of the *shipped* integer derivative
store (I tested the ideal float map, the optimistic bound); and moving lenses (B16) —
no kick was ever applied to an orbit while the source moved. Machine: shared runner,
load 0.31; orders of magnitude only, per the lab rules.
