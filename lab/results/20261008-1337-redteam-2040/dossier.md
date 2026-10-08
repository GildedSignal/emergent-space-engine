# Dossier — 20261008-1337-redteam-2040 (premise red-team)

**Claim.** representation.md §3's "a kick updates the cycle by a multiply-add" survives
far better than expected in the regular regime (error ≈ 0.05·(kick/distance-to-separatrix)^1.85,
1% band broken only when the kick exceeds ~0.4× the distance to the separatrix; along a
secular inspiral it holds until 2 kicks before the plunge), but it **fails by type at the
separatrix: a kick that crosses it returns a finite cycle for an orbit that plunges** —
misclassification, not error size — and no frozen rung or gate tests kick response at all.

**Bottleneck.** Not on the board list directly; it lands on two live items: the in-flight
`b-plunge-tubes` build (the plane currently *refuses* these orbits, `NoBoundOrbit`) and the
kick path's cost (board focus: "kicks dominate the engine's cost"; the exact cycle memo hits
0% on distinct kicks, taste log 5 Oct, so the multiply-add is the only cheap kick path the
design has). Gain: deletes the recompile on ~every kick outside the separatrix window and
names the one exact predicate (root structure of the turning-point cubic on the integer
invariants — a sign test) that must gate the cheap path. Orders of magnitude: a recompile
costs "tens of crossings" per new invariant pair (§3); the multiply-add is one; my run says
the recompile is needed only inside a window of width ≈ the kick size around the separatrix.

**Evidence** (all commands ≤ 60 s; `falsifier.py`, output `falsifier-out.json`; one core,
22 s, ~30 MB; host load 2.0, 15 GB RAM with 11.7 GB free, 8 vCPU shared runner):

```
cd lab/results/20261008-1337-redteam-2040 && python3 falsifier.py
```

Oracle: exact Schwarzschild timelike geodesics (M=1), per-radial-cycle (Δφ, T_t, T_τ) by
Chebyshev quadrature over the turning-point band (the `bound_period_quad` family, H0183),
validated two ways: an independent RK4 integration of the Binet ODE agrees to 2×10⁻⁴ at
p≈80, and the 1PN series 6π/p = 0.2356 sits 6% below the exact 0.2501 (the exact-vs-1PN
gap H0203 used to freeze r3 v2's exclusions). Derivatives of the *exact* map by central
differences — the ideal version of the stored "cycle derivatives"; the shipped integer
version can only be worse (the derivatives diverge as the separatrix is approached, so a
fixed-width store also saturates there).

- P1 weak field (peri 50, apo 200): kick ΔL/L = 10⁻⁴ → relerr(Δφ) = 1.5×10⁻⁹.
- P2 strong field (p = 12, e = 0.6 — δ_L/L_sep = 7.7×10⁻²): same kick → 1.6×10⁻⁷.
  Note the standard strong-field eccentric orbit already sits 8% from the separatrix.
- Scan at E = 0.97, kick 10⁻⁴·L: δ_L/L_sep = 3×10⁻²…3×10⁻⁴ (kick/δ = 3.4×10⁻³…0.33) →
  relerr(Δφ) = 9.0×10⁻⁷…4.3×10⁻³, i.e. err ≈ 0.05·(kick/δ)^1.85; the 1% band breaks at
  kick/δ ≈ 0.4. Matched δ at E = 0.999 (peri 4.2, apo 992) gives the same error to 7%
  (scale-free in δ, as the dimensionless reading of principle 4 would want).
- P4 the kill: E = 0.97, δ_L/L_sep = 10⁻³, kick ΔL = −2×10⁻³·L_sep (crosses it). Truth:
  plunge — no cycle exists. The multiply-add returns Δφ = 18.86 rad, T_t = 585 for the
  pre-kick truth of Δφ = 15.64, T_t = 557: **a finite, plausible-looking cycle for an orbit
  that falls in.** 1/1 misclassified.
- Inspiral walk (E = 0.97, dL = −10⁻⁶·L per kick from δ₀ = 3×10⁻²): 29,127 kicks to the
  separatrix; the 1% band breaks at kick 29,125 — two kicks (7×10⁻³ % of the walk) before
  death. Every inspiral ends inside the bad window, but only at the end.

**Predictions.** [predictions.md](predictions.md), written before the run. Held: P1, P2
(orders below the bands), P4 (the misclassification). Failed, honestly: P3 (predicted
relerr > 10⁻² at kick/δ = 0.1; measured 4.9×10⁻⁴, 20× below the band) and P5 (predicted
the 1% threshold at kick ≈ 0.01·δ; measured ≈ 0.4·δ, 40× more forgiving). The premise is
more robust than this red-team expected; the kill is qualitative, at the boundary, exactly
where the design's own certificate definition ("the interval over which a description
reproduces the law", §3) already forbids using it — the doc just never says that interval
shrinks to zero at the separatrix and must be *certified per kick*.

**What would make it wrong.** If shipped plunges were decided by an exact integer root-
structure test before any cycle update (the cubic (E²−1)r³+2r²−L²r+2L² = 0 on the kicked
invariants — three real roots with the middle one outside the horizon ⇔ bound), the
misclassification cannot occur and my kill reduces to a cost note (recompile inside a
window of one kick width). My derivatives are of the exact map, so the real integer
implementation's errors are worse, not better; and I model kicks as instantaneous (E, L)
jumps, which is §3's own model. 2D equatorial only — the game is 2D.

**Cost of adopting.** One exact predicate per kick near the edge (the plane already pays a
refusal there today), plus the rule "the multiply-add is valid only inside the stored
cycle's certificate; crossing the certificate boundary hands off to the plunge tube".
Deletes the per-kick recompile everywhere else — the opposite of a bandaid: it is the
design's own certificate principle applied to the kick path.

**Fit with PRINCIPLES.** Principle 2: "error type over error size" — the kill is a type
error (a cycle fabricated for a plunging orbit). Principle 13: "errors never compound…
divergence is not a joke" — a fabricated cycle is divergence handed to the player as an
orbit. Principle 19: "a fix signals the wrong representation" — the fix is not a patch on
the derivative but the exact classification the invariants already carry for free.

**The ranked attacks** (each with the rung criterion that should have caught it):
1. Kick response at the plunge separatrix — **falsified here at the boundary; survives
   elsewhere, better than predicted.** No frozen criterion exists. r1 has no kicks; the
   closest was r3 v3's handoff exponent (0.233 vs 0.2), adjudicated an artifact of a
   chaotic float reference — that adjudication deserves reopening: a handoff is a kick-like
   jump, and the response map is genuinely non-smooth at regime edges. Proposed criterion
   (type, for the motion-law gates / the B12 redesign): *a kick that changes the
   turning-point root structure must flip the body to the plunge path, never return a
   finite cycle; derivative-updated cycles stay within their behaviour band while the
   kicked invariants remain inside the stored certificate.*
2. The view gather's Newton-from-previous-frame (§2) — **unfalsified here (time), and
   unguarded anywhere**: r6 was never frozen (only r1–r4, r7–r10 exist as files; §7's r5
   was covered by H0207's battle test, r6 by nothing). In flat spacetime the crossing
   equation is monotone (|F′| ≥ 1−β_emitter), so the hazard is curved spacetime only:
   crossings are born/die at caustics as the observer moves, and the stale seed swaps
   branches precisely when the player — the only wildcard, thrust to 10⁴ g — accelerates
   near a lens. The player sees sprites pop or swap colour. Needed: a branch-identity
   criterion in r6 (count of crossing-set membership changes per minute under an
   acceleration profile, zero tolerance for the primary branch).
3. EOB "ν only in the energy map" — **survives at 1PN** (r3 v3: assists 64/64), conditional
   on: comparable-mass strong-field binaries (2PN terms are ν-dependent, textbook) and deep
   flybys (m-meso-motion, silver, conditional). Covered by r3's `nu` criterion at 1PN;
   nothing covers 2PN, which is fine iff the doc states the Fermi line (at r = 20M, the
   2PN ν-term is ~ν(M/r)² ≈ 6×10⁻⁴, below every behaviour band).
4. Binet cells — **survive** (H0205, checker-reproduced: every r1 criterion at m16/m32,
   ~38 crossings/cycle; river and m8 killed). Caveats on record: r1 stands DISPUTED (author
   timeout; no clean re-run logged) and e > 0.7 is excluded from its seeds.
5. Dense/sparse bit-identity — **held in the one built test** (H0207: bit-identical
   lockstep vs sparse on a battle, re-anchoring 0.44%). Untested edges: multi-contact
   ordering inside one window (the tie rule, redteam-6254, adopted into law.md) and
   hysteresis of the sparse↔dense trigger (a body flapping between orders frame to frame
   re-introduces synchronization work — the principle-14 hazard below). r5 was never
   frozen as a rung.
6. "Cost ≈ 0 for undisturbed bodies" — **already corrected by measurement** (taste log,
   5 Oct: the exact memo hits 0% on distinct kicks; the plane recompiles ~99% of kicks;
   the quantized-cell memo hits 94.5% but changes orbits). This run adds the positive
   converse: the multiply-add is the cheap path that survives that correction, with the
   separatrix gate as its only refusal.

**Principle violations found in the text** (not measured): the dense order's lockstep is
ticks (principle 14) — defended in-doc by "a tick wastes nothing when everything changes
every tick", which holds only if the sparse↔dense trigger has hysteresis; §2's "carried
forward so that it never compounds" is an amplitude claim wearing a compounding badge (a
fabricated cycle compounds nothing only if something classifies it first — attack 1's
predicate); §6's largest cost row ("AI decisions… likely the largest total") is off the
plan by Julien's 30 September ruling and should be marked as such.

**The lens: what it may have missed.** Red-teams overweight exotic cases; I ranked by
player visibility but still falsified the strong-field separatrix rather than the view,
which every player sees every frame — chosen for decisiveness in 60 s and because
`b-plunge-tubes` is in flight now; the view's branch identity (attack 2) is the one I
would run next. I also tested the ideal float map, not the shipped integer one, and no
moving lens (B16) interaction with kicks. Machine: shared 8-vCPU runner at load 2.0,
timings not load-bearing (orders of magnitude only, per the lab rules).
