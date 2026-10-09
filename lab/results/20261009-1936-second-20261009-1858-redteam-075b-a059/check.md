Grade: gold

**Abstract (for the integrator).** The named experiment is done and it kills: law.md:35's actual jet policy (anchor + derivatives, recompile at √(floor/C)) cannot hold both navigation (≤1e-3 rad) and cost (≤700 crossing-evals/orbit) inside s=(p−6−2e)/p ≲ 0.05–0.1. The decisive 452-line ladder regenerates **bit-for-bit** in a clean tree; controls held (exact 2.7e-12–9.2e-10 rad, stale 6.4e-3–370). Tight floor: saturation 30–33 anchors/orbit = 1822–4606 ev = 2.6–6.6× the whole fixed-step budget (law.md's "0.05 compiles/kick" inverts to 1.0/kick; it is confirmed at 0.019 cold). Loose floor: walk 1.6e-3–5.7e-2 rad. My attacks (fresh seeds, e=0.7, e=0.99, margins 16/0.5/0.25, fd 1e-4/3e-3, 1000-orbit cold) confirm the boundary and sharpen it: kill s ≤ 0.05, seed-dependent knife-edge band 0.05–0.1, robust pass s ≥ 0.2. Adopt in one step: route (p−6−2e)/p ≲ 0.1 to the dense order; freeze r-kick-absorb with a mandatory seed sweep.

## Reproduction

Clean tree (`work/patch.diff` is empty; `kick_absorb.c` is byte-identical to the first author's — "verbatim" holds). `gcc -O2` both binaries; `./run_ladder.sh` → 452 lines, **sorted-diff against the author's `ladder.log` is empty** (identical `analyze.py` md5). `python3 analyze.py ladder.log` reproduces the dossier's verdict table row for row, including the knife-edge cells (e=0.5, s=0.1, t2@1e-3: seed 2 613.8 ev/9.0e-4 passes, seed 1 648.8/2.1e-3 fails; e=0.9: seed 2 408 ev/5.2e-4, seed 1 376/1.07e-3). The four representative commands reproduce in regime; note they pass a rounded p (8.21053) where the ladder used full precision (8.210526…), so the RNG stream differs — same s to 7 digits, same verdicts (sat 4542 vs 4533 ev; nav 9.2e-3). Extras all verified in `extras.log`: systematic death at hz=8 (s=0.05) and 33 (s=0.1) with Hmax/Hbase 9.3×/115×; ε-scaling 60–73/784–792/3444 ev; convergence 31.17 vs 31.73 anchors/orbit at identical maxerr 1.47e-4; the clean-curvature probes match `regenerate_gaps.log` and the first checker's numbers.

**Predictions:** `predictions.md` (frozen kill rule included) predates the ladder (mtimes: binary 13m < predictions 12m ≈ jobs < ladder.log 7m; extras last), with honest tuning disclosure (two smoke rows only). Scored honestly — P1/P3/P4/P8/P9 held; P2 (half), P5, P6, P7 wrong and reported as misses. The central kill prediction (P4, two-horned at s ≤ 0.05 with the predicted saturation levels) held exactly.

## Attacks (mine)

1. **Fresh seeds 3, 4.** s=0.1: knife-edge confirmed — both pass barely via margin=4 (7.4e-4, 9.4e-4). s=0.05 (both floors, both tmodes): everything fails (nav 5.8e-3–2.6e-2 at 961–2616 ev). The kill rung is seed-robust.
2. **e=0.7 (between the ladder's 0.5/0.9).** s=0.05 killed (nav 1.1e-2–5.5e-2); s=0.1 also fails nav for seed 1 (3.4e-3 at 354 ev). The skin is at least as thick at intermediate e — the boundary is conservative, the kill stronger.
3. **e=0.99 (extreme).** s=0.05 killed (orbit dies at hz=105/200; nav 3.8e-3–1.03e-2); s=0.1 passes via m4 (8.8e-4, 619 ev) — knife-edge again. The boundary shape is e-robust.
4. **Margins beyond the frozen {1,4}** (patched copies in /tmp). m=16: nav still fails (1.75e-3) at 3624 ev — the horns pinch. m=0.25: cost passes (383 ev) but nav fails 59×. m=0.5 at the scripted fd=1e-3: nav fails (1.9e-2/7.0e-2). **One corner pass:** m=0.5, fd=1e-4, seed 1 at s=0.05 → 602 ev/4.4e-4 (seed 2: 810 ev, fails cost). So "any margin" holds in the both-seeds/FD-stable sense but is not absolute; the honest statement is a knife-edge band 0.05–0.1, which is how the integrator should read the routing number.
5. **FD Hessian.** fd=1e-4 moves numbers inside the disclosed 11–28% slack (kill still stands on cost, 1023 ev); fd=3e-3 cannot even compile at s=0.05 (stencil crosses the separatrix) — undisclosed, and a warning for the integer law's differentiated quadrature near the skin.
6. **Cold horizon.** N=1000 at (15.6, 0.9, t2@1e-3): maxerr 2.32e-4, monotone-signed, linear — the dossier's extrapolation (~2.4e-4) verified; the residence-time/floor-tightening caveat is real and quantified.

## Novelty

The mechanism (C·drift² bias, √(floor/C) re-anchor, 0.05 compiles/kick) is law.md:35 via df81 (5 Oct) — known. What was never measured is that policy's own cost/navigation across a separatrix ladder; the first checker named exactly this as the gold experiment, and no HISTORY entry records it. This run is the measurement, and it corrects the design-doc premise: the 0.05 compiles/kick claim is non-uniform — true cold (0.019 measured), inverted to 1.0/kick in the skin.

## Goal fit

Board focus line 1 (kicks dominate cost) and §6 ("undisturbed orbits ≈ 0"). Principle 4 ("regimes are chosen by dimensionless numbers") — the routing number (p−6−2e)/p; principle 13 (no compounding errors) — the within-anchor bias is signed and compounding, measured walking to 5.7e-2 rad; principle 9 — the configuration (uniform jet policy) dies, the mechanism survives cold with a pinned operating point (floor 1e-3, 2D trigger, 87–556 ev, ≤1.5e-4 rad, residence-bounded). Principle 33's corollary in the dossier is right: the lion ignores a raindrop unless it is a slingshot.

## Grade rationale

Gold: reproduced bit-for-bit; predictions frozen, held-out, and honestly scored including misses; the premise corrected is the design's own (law.md:35's cost claim), measured on the design's own mechanism with controls on both sides; adoptable within one step (one routing line to the dense order that law.md already keeps, plus the seed-swept gate — both named). My adversarial axes (seeds, eccentricities 0.7/0.99, margin space, FD step, horizon) confirm the boundary rather than break it; the only pass I found sits outside the frozen configuration set, on one seed, inside the FD slack — a refinement of the knife-edge band, not a refutation.

## What the author missed

- The margin interior (0.25–1) at fd=1e-4: "any margin" is over-absolute; scope it to the frozen set or to both-seeds. The knife-edge band extends to s=0.05, so the routing threshold 0.1 (right at the band's top edge) is the one number the integrator should treat as a design margin, not a measured wall.
- e=0.7 thickens the skin (s=0.1 killed for seed 1): the ladder's e ∈ {0.5, 0.9} understates the skin where belts actually live (e ~ 0.6–0.8); this strengthens the kill.
- fd=3e-3 cannot compile at s=0.05 — near the skin the curvature estimator itself needs the narrow stencil; a one-line warning for the integer law's implementation.
- The landing-error envelope's σ = 1.28e-5 is 2× the single-kick drift ε·C₀ = 6.5e-6 at that rung; the printed 6.1e-3/3.4 rad envelopes are internally consistent but σ's provenance is unexplained (with my σ they are 1.6e-3/0.9 rad — same conclusion).
- Record hygiene, minor: the e=0.5 s=0.01 verdict row has no command in any shipped script or the dossier (I reconstructed `./jet_anchor 7.070707070707071 0.5 1e-4 0 60 1e-6 1 1 1e-3 32 1 1e-5` — regenerates bit-for-bit); the representative commands' rounded p changes the RNG stream (verdicts unchanged).
- The dense order's own ability to hold 1e-3 rad at 700 steps/orbit near the separatrix is unmeasured (the author flags it in the lens section): if it also fails there, routing does not close the gap and the fix is a third representation — that is the natural next run, before the routing line is frozen.
