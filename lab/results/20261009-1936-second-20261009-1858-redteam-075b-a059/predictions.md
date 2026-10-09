# Predictions (written before the decisive ladder)

Second author on 20261009-1858-redteam-075b. The checker's named experiment: implement
the design's ACTUAL policy — law.md:35's jet, re-anchored ("error grows as C*drift^2;
when the accumulated offset reaches sqrt(floor/C) the cycle is recompiled") — on a
separatrix ladder, floors {1e-6, 1e-3}, 32 kicks/orbit (H0190), seeds swept; measure
anchors/orbit against the 350–700 fixed-step control and the residual phase walk.

Falsifier: `jet_anchor.c` in this folder (author's law and truth machinery verbatim:
1PN Binet, RK4 h=1e-3, kicks at periapsis as element jumps, dC=eps*C0*s, dK=-2*u_p*dC).
The jet: anchor with exact F, first derivatives, clean Hessian (9-point stencil,
fd=1e-3 rel; 1e-4 at s<=0.02 where the wider stencil crosses the separatrix);
trigger 0.5*|q2| > floor/margin -> recompile at the body's state; consumption once
per orbit at the pre-batch state. tmode=1: law.md's literal 1D trigger (FCC*dC^2);
tmode=2: honest 2D (full d^T H d) — kicks move both C and K, so the error the design
must bound is the 2D one. Cost: one compile = one exact radial cycle = cr crossings,
cr = 2*16*log2((1+e)/(1-e))+8 (B9, m=16): 58.7 at e=0.5, 143.9 at e=0.9. Derivative
evals not charged (the integer law differentiates the quadrature).

Tuned on (smoke, before this file): (20,0.5) s=0.65 and (8,0.8) s=0.05 rows only,
plus clean-curvature probes at all rungs (H is an input, not an output). The interior
ladder and all walk/rate numbers below are held out.

Ladder: e in {0.5, 0.9}; s=(p-6-2e)/p in {0.5, 0.3, 0.2, 0.1, 0.05, 0.02, 0.01};
p=(6+2e)/(1-s). eps=1e-4 (the author's hot kick), sign=0, KPO=32, N_orbit: 300
(s>=0.1), 200 (s=0.05), 150 (s=0.02), 100 (s=0.01). Floors {1e-6, 1e-3}, tmodes {1,2},
seeds {1,2}. Extras: eps=1e-5 rows (s in {0.2,0.1,0.05}, e=0.9, floor=1e-6, tmode=1);
systematic sign=1 (s in {0.1,0.05}, e=0.9, floor=1e-6); convergence spot-checks
(h=5e-4; fd 1e-3 vs 3e-3 vs 1e-4).

Navigation tolerance: max |Phi - phi_true| <= 1e-3 rad over the run (r-kick-absorb's
criterion). Cost parity: cr*anchors/orbit <= 700 (probe 2's fixed-step control).

1. **Controls.** Exact-per-orbit <= 1e-8 rad at every rung; stale jet >= 1e-3 rad
   within 300 orbits at every rung (eps=1e-4, KPO=32).
2. **Cold survival, literal trigger.** floor=1e-6, tmode=1: evals/orbit <= 100 and
   maxerr <= 1e-4 over 300 orbits at s >= 0.3, both e. (Smoke: s=0.65 gave 13
   evals/orbit, 2.8e-5 rad.)
3. **Cold failure, honest trigger.** tmode=2 at floor=1e-6: >= 500 evals/orbit at
   every rung incl. s=0.5 — the 2D trigger never beats the 700 control because the
   K-walk (dK = -2*u_p*dC, FKK large) dominates the trigger even where FCC is small.
4. **Hot two-horned kill.** At s <= 0.05, every configuration (floor, tmode, margin)
   fails cost or navigation: floor=1e-6 -> saturation (>= 30 anchors/orbit, >= 1700
   evals/orbit at e=0.5; >= 4300 at e=0.9); floor=1e-3 -> maxerr > 1e-3 rad by 200
   orbits (walk ~ N_orb * floor * c). Skin s* (largest killed s, tmode=1, floor=1e-6):
   0.1 +/- 0.05 — borderline at s=0.1 (predicted 3-12 anchors/orbit from
   rate ~ H*sigma^2/(2*floor) with walk-statistics factor ~1/3), killed at s=0.05.
5. **The squeeze.** floor=1e-3 fails navigation at every rung s <= 0.5 (predicted
   maxerr >= 1e-3 over 300 orbits even cold: the walk accumulates ~floor-scale signed
   error per orbit). So the design cannot escape to the loose floor; at the tight
   floor the skin s* ~ 0.1 pays the full kick rate in compiles.
6. **eps-scaling.** rate ~ eps^2: at eps=1e-5, s=0.05, floor=1e-6, tmode=1:
   <= 3 anchors/orbit (<= 450 evals) and maxerr <= 1e-4 — passes. The kill skin
   shrinks with eps^2 in rate, i.e. s*(eps) moves where H(s) ~ eps^-2: still
   s ~ 0.15-0.2 at eps=1e-5 for parity (borderline), consistent with 4.
7. **Systematic drift.** sign=1, s <= 0.1: plunge or separatrix crossing within
   ~30 orbits (32*1e-4 ~ 3e-3 relative drift per orbit); before death Hmax/Hbase >= 2
   and maxerr at floor=1e-6 exceeds the random-sign row at the same rung by >= 3x
   (anchor curvature under-triggers as the walk climbs the divergence).
8. **Trigger floor is unenforceable near the separatrix.** maxcons > 10*floor at
   s <= 0.1, floor=1e-6: a single full-size kick landing on a fresh anchor already
   costs 0.5*H*sigma^2 ~ 1e-3-scale instantaneous error; per-kick recompiles cannot
   get below it (this bounds ANY re-anchor policy at kick granularity).
9. **Batch-phase luck.** seed-to-seed maxerr spread >= 2x at s=0.05, floor=1e-6
   (consumption samples the post-trigger state once per orbit; a one-seed gate can
   pass by alignment — same class as the author's bucket-phase finding).

**Kill rule (frozen).** The jet mechanism is KILLED at rung (e,s) iff no
configuration (floor in {1e-6,1e-3}, tmode in {1,2}, margin in {1,4}) passes both
(evals/orbit <= 700 AND maxerr <= 1e-3). The cost premise dies within skin
s* = max killed s. Clean refutation of the author's claim: every rung s >= 0.05
passes some configuration at both e (then the premise stands on the design's own
mechanism and the author's separatrix kill was an artifact of attacking the stale
text).
