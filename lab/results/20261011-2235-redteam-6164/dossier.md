# Dossier — 20261011-2235-redteam-6164 (lens: premise red-team)

## Claim

The design's kick premise — "a cycle's derivatives are stored with it, so a kick updates the
cycle by a multiply-add" (`docs/representation.md` §3) — is measured false in three domains
(wide/eccentric orbits, encounter-size kicks, and a band around the plunge separatrix), no rung
or gate guards its validity domain, and `docs/representation.md` is stale against `docs/law.md`
on two of the lens's six premises (the integer Binet mechanism is dead; rungs r5/r6 named in
its own falsifier ladder were never frozen).

## Bottleneck

Board focus items "fewer kicks per orbit" / "fitting 10⁹ in 8 GB" both route through the jet
(law.md's adopted "exact offset plus stored derivatives, re-anchored", ~0.05 compiles per
kick). This run measures that mechanism's validity domain and finds the 0.05 figure holds only
in a corner: recompiles per kick ≈ 1.4·10³·r_apo·α (r_apo in M, α = relative E-kick). Getting
this into the law's certificate (a root-distance check against roots darwin16 already
computes) is the difference between the allocator scheduling recompiles by slack and paying
them as a surprise in the p99 — exactly the smoothness bottleneck (principle 12).

## Evidence

Oracle: float64 Schwarzschild timelike geodesics, Binet ODE (M = 1), RK4 h = 1e-3 with
h-refinement agreement 1.3e-11; precession converges to the 1PN 6π/p with a clean O(1/p)
2PN excess (ratios 1.0481 / 1.0092 / 1.0046 at p = 100/500/1000). All commands run in the
run folder, each ≪ 60 s:

```
python3 probe.py          # 4 s; writes probe_out.json, prints it
```

Held-out cases (details in `predictions.md`, scorecard below):

1. **Single quantum kick (α = 1e-6 relative on E), belt-like grid** — jet error ≈
   **2·(r_apo·α)²**, r_apo in geometric units: C/r_apo² ∈ [1.9, 6.1] across r_apo = 22 → 10⁴
   (p ∈ {20, 100}, e ∈ {0.1…0.99}). Derivation matches: the T-channel remainder is
   r_apo-free (Kepler gives 15/4·α²); the corruption is the **precession phase**, whose
   relative remainder is (α·a)²·4, a = r_apo/2. The L-channel is harmless (≤ 7.5e-12).
   Against the 1e-6 floor (df81's): passes at p = 20 to e ≤ 0.9 (e = 0.99 there is 7.6e-6,
   7.6× floor), **fails at p = 100 from e ≥ 0.9 (2.1e-6) through e = 0.99 (1.9e-4, 190×
   floor)**. The jet's one-kick validity condition is r_apo·α < 4·10⁻⁴.
2. **Correlated-kick walks** (base p = 20, e = 0.5): error exponent vs kick count N =
   **1.9962** (quadratic, as df81 found); N_floor ∝ 1/α exactly (178 / 18 / 2 at α =
   1e-7 / 1e-6 / 1e-5). Recompile trigger = accumulated drift 1.8e-5 relative in E =
   √(floor/C) ✓. Cost: **0.056 compiles/kick at α = 1e-6, r_apo = 40** — reproducing
   law.md's "about 0.05" — but scaling as r_apo·α: at r_apo = 2000 (e = 0.99, p = 20) the
   same α gives ~2.8 compiles/kick (every kick), and at encounter α = 1e-3 even r_apo = 40
   gives ~56. The 0.05 figure is a corner of the plane, not the plane.
3. **Plunge separatrix** (L = L_s, unstable circular at r_c = 5M; E → E_s from below):
   |∂T/∂E| grows 10× per decade of approach (2.8e4 → 2.6e7, logarithmic divergence); whirl
   cycles Δφ = 15.5 → 30.6 rad. A single 1e-6 quantum kick errs by 6.9e-8 (ε = 1e-3),
   5.5e-6 (1e-4), 4.7e-4 (1e-5), **0.47 at ε = 1e-6**. Encounter-grade kicks (α = 1e-3,
   B13's regime) at ε = 1e-3: **43–79% error, and α ≥ 3e-3 exits the bound family
   outright** — the multiply-add updates a cycle that no longer exists.
4. **r1's own ISCO seed** (tangential launch at r = 7M, L = 1.01·L_circ(7)): bound, r ∈
   [7, 8]M, already a 2.25-revolution whirl (Δφ = 14.18 rad/cycle), sitting **1.93e-3 (0.19%)
   below its plunge separatrix in E** and 1.5e-4 below the critical L. Quantum kicks are fine
   there (2e-8); one encounter flyby (α ~ 1e-3–1e-2) crosses the gap: the near-ISCO
   population lives one flyby from where the jet is categorical.

Premise scorecard for the lens's six targets (survivors reported too):

- **1. Two-body doll, ν in the energy map only (1PN): SURVIVES on record** — r3 v3
  (precession 1024/1024, periods 632/632, ν effect 500/504, assists 64/64) and B11; domain
  1PN, ν ≤ 0.25. No new attack; going past 1PN or comparable-mass spin is exotic for the
  player.
- **2. Binet cells as a rotation: SURVIVES at ODE level, DEAD at the integer level as
  written.** H0205 passed every r1 criterion with the band ODE (m = 16/32, ~38
  crossings/cycle); the banded force residual is −3M(u−u_k)² (exact algebra), a one-sided
  precession bias of order (2^(1/32))² ≈ 4e-4·Δϖ — below B1's 1%. But `representation.md`
  still names **Minsky's two-addition map as the integer mechanism**, and law.md line 20
  records that mechanism was killed (first-order slope error in every cell holding a turning
  point) and replaced by `space-darwin16-v1`. The design doc teaches a dead mechanism as "the
  primary in-cell solution".
- **3. Kicks absorbed by cycle derivatives: FALSE in the measured domains above.** Guarded
  nowhere: B5 gates E,L growth exponents; B9 counts crossings; B12 Jacobi growth; r2 carry
  width; r4 v3's frozen cases are near-circular (e₀ = 0.02) — the high-e corner where the jet
  weakens is untested by any rung.
- **4. Dense order bit-identical to sparse: UNGUARDED at the ladder.** B8 gates bit-identity
  at law level, but r5 (the Clohessy–Wiltshire + lattice-contacts scene) named in
  `representation.md` §7 **does not exist in lab/rungs/** (verified: only r1–r4, r7–r10 are
  frozen). Not attacked further here.
- **5. View gathered at the past light cone: UNGUARDED.** r6 also absent from lab/rungs/.
  B7 (clocks) and B16 (deflection) exist; nothing judges the moving observer's Doppler,
  aberration or image-branch continuity under acceleration — the core player fantasy. Lead,
  not run: Newton-from-previous-frame can jump image branches when a lensed image pair
  appears/disappears during a hard burn; a rung should plant that case.
- **6. ≈0 cost for undisturbed bodies: SURVIVES** (B9's "zero work per orbit until an
  event"), but §6's cost table must carry finding 2: the kick row's "<1% of a core" assumes
  the jet's corner (α small, r_apo small). Secondary text bug found: "cells hold integer
  mass moments of everything" vs "crossing a spoke carries no gravity event" — a body
  crossing 2πm/ln 2 ≈ 145 spokes per orbit would generate ~8.7e6 cell-moment events/s at
  10⁹ bodies and the doc's 6e4 kicks/s, unless moments are per-ring or derived on demand
  (principle 6: store the generator). B15 would catch it if it bites.

## Predictions

`predictions.md` was written before the run. Scorecard: **P1 partially failed as predicted
to pass** (held for e ≤ 0.9 at p = 20 but failed at p = 100, e ≥ 0.9 — the finding); **P2's
shape held** (exponent 1.9962, N ∝ 1/α) but the absolute N at α = 1e-6 was 18, not "a few
hundred" — 40× weaker than my prior, i.e. df81's 730 implies their quantum was ~2.5e-8, no
contradiction, but the docs' "0.05 compiles/kick" is α- and r_apo-dependent; **P3 held in
mechanism and in the encounter-kick reading** (0.19% gap vs 1e-3–1e-2 encounter kicks) but
the >1% quantum-kick band is narrower than predicted (ε ≲ 3e-6, not 1e-4–1e-2); **P4
failed**: at fixed p the error grows 2570× from e = 0.1 to 0.99 (through r_apo), not <10×.
Two of four held, two failed in the informative direction.

## What would make it wrong, adoption cost, PRINCIPLES fit

Wrong if: the law's kicks are L-dominant in practice (measured L-channel ≤ 7.5e-12 —
encounter kicks are mixed, so the E-channel bound is the envelope, not the typical case); if
df81's re-anchor already triggers on a norm that includes separatrix distance (law.md states
offset vs floor only — it does not); if the integer law's quantization makes the float
α-mapping inapplicable (floats explored here; only integers decide — the rung must re-run
this on the law). Adoption cost: small and local — the certificate "kick lands within the
root-distance band ⇒ exact recompile" uses the R-roots darwin16 already factors at compile
time (law.md §Motion, item 2); plus one criterion in the kick rung (e.g. "recompile rate ≤
0.1/kick on the belt's (p, e) tails at the encounter kick distribution", negative control:
jet without re-anchor, which df81 already showed fails). Fit — principle 13: "errors never
compound… basically we don't want errors that can compound that's the goal": the jet honors
this only inside its domain, and the domain has a cheap border; principle 21: "rough first,
refine when a certificate could break… simple and powerful" — the root-distance check is
that certificate; principle 19: "if you find yourself fixing things that's oftentimes a
signal that it is the wrong representation" — law.md's darwin16 was the fix, and
`representation.md` still carrying the dead Minsky text is exactly the drift that signal
exists to prevent.

## The lens

A red-team overweighted the strong-field corner: the belt-scale line (p = 100, e = 0.99:
1.9e-4 per quantum kick) is the more player-adjacent failure since belts are where the
bodies are. Missed here: Kerr (χ ≠ 0), where the separatrix structure is richer and the
same certificate must be re-derived; the integer-law rerun of the same sweep (floats only,
as the rules direct); and premise 4 got a doc-level finding where a probe was owed. The
two doc-staleness findings are one-paragraph fixes for the integrator, not physics.

## Files

`probe.py` (oracle + jets + walks + separatrix sweep), `probe_out.json` (all numbers),
`probe_stdout.txt`, `predictions.md`. Machine: shared cloud runner, 8 vCPU, no other load
observed at start; 4 s total; timings not evidence.
