# Dossier — 20261006-1249-redteam-4978 (premise red-team)

**Claim.** The jet — a kick updating a compiled cycle from its stored ∂/∂E, ∂/∂L derivatives
(`docs/law.md` line 35, adopted 5 October with re-anchoring at "about 0.05 compiles per
kick") — is invalid near the Schwarzschild separatrix: one 0.1%-of-L kick misses the new
cycle's increments by 10³–10⁹× the law's 10⁻⁶ floor (up to 100× the cycle itself), the
error diverges as the orbit approaches the last stable orbit, and no linear update can
represent the bound→plunge flip a kick causes there. No frozen gate measures any of this.

**Bottleneck.** The board's live questions "the changeover near a secondary" and the design's
cost table (`docs/representation.md` §6: "tidal kicks… ~50 ns each, incremental"). For the
black-hole-adjacent population (r_peri ≲ 6 M — the marquee GR content: whirls, ISO, plunges,
"all emerge", §1) the jet degenerates to a full recompile per kick, and without an explicit
per-kick regime test the flip is an error of *type*, not size (principle 2). Player-visible
today: the plane already freezes in near-plunge states (`NoBoundOrbit`, HANDOFF "In flight").

## Evidence (exact Schwarzschild geodesics, float64, quadrature on the root-factored first integral; the jet gets the EXACT derivative — the design's best case)

Reproduce: `cd lab/results/20261006-1249-redteam-4978 && python3 sep_jet.py` (3 s, < 50 MB).
Full output in `sep_jet.out`. Instrument controls: independent RK integration of
u″+u = 1/L²+3u² gives pericenter spacing 11.856 vs quadrature 11.8557; weak-field
Δφ−2π = 0.2677 vs 1PN 6π/p = 0.2513 (the 2PN term at p = 75 M).

Family A (L = 3.7 M, E → E_sep⁻, whirl radius 4.44 M), one torque kick ε = 10⁻³ in L
(floor = 10⁻⁶):

| δ to separatrix | r_peri/M | Δφ/cycle (rad) | orbits/cycle | jet err Δφ | × floor | jet err Δt | × floor |
|---|---|---|---|---|---|---|---|
| 0.01 | 7.27 | 10.85 | 1.73 | 1.4e−3 | 1.4e3 | 1.3e−2 | 1.3e4 |
| 0.001 | 4.90 | 14.47 | 2.30 | 0.112 | 1.1e5 | 1.04 | 1.0e6 |
| 0.0001 | 4.57 | 18.30 | 2.91 | 4.17 | 4.2e6 | 38.9 | 3.9e7 |

Family B (r_peri = 4 M fixed, L → 4⁻): err 0.21 rad (2.1e5×) at δ = 0.05; **2 808 rad
(2.8e9×) at δ = 0.001** — the error exceeds the cycle itself by 100×: the first-order update
is meaningless there. The error scales ≈ (ε/δ)², i.e. with Δφ″, which diverges at the
homoclinic orbit — Δφ per cycle grows logarithmically in δ (10.9 → 18.3 rad over δ 10⁻²→10⁻⁴),
the zoom-whirl divergence.

Controls that pass (kill is bounded to the configuration, not the method): weak field
r_peri = 45 M, e = 0.1: err 2.0e−6 ≈ floor; near-parabolic r_peri = 50 M, e = 0.98:
err 7.4e−7 < floor. The weak-field near-parabolic edge is benign (power law); the kill is
specifically the relativistic separatrix.

**Regime flip (P4):** bound orbit E = 0.9602, L = 3.7 (δ ≈ 0.005), kick −1.4% in L at
constant E, just across L_sep(E) = 3.654. Truth: plunge (the first integral loses its inner
turning points; single real root), horizon reached after 8.85 rad. The jet predicts the next
pericenter at 13.8 rad — a pericenter *inside the horizon*. No derivative-based update of a
bound-cycle record can represent bound↔plunge; it must be an explicit regime test on the new
(E, L).

## Predictions (`predictions.md`, written before the run)

- P1 half-wrong: Δφ diverges (logarithmically, as predicted) but the amplitude is ~4× smaller
  than I guessed — 2.3 orbits/cycle at δ = 0.001, not ≥10. Held-out miss, reported as such.
- P2 held in structure: error exceeds the floor already at δ = 0.05 (family B) and reaches
  0.1–4 rad (10⁵–10⁶×) at δ = 0.001–0.0001; family B exceeded my range (2.8e3 rad at δ=0.001).
- P3, P5 held: both weak-field controls pass.
- P4 held: plunge mispredicted as a bound cycle (13.8 rad phantom pericenter vs horizon at 8.85).

## Ranked attacks (the lens deliverable)

1. **Jet near the separatrix + bound↔plunge flip under kicks** (premise 3 of my brief,
   measured above). Should have been caught by: **none**. B12 is weak-field handoffs
   (Jupiter-like); B19 classifies plunge only at *unperturbed* compilation from (E, L); B5/B9
   measure the unperturbed cycle. Missing criterion: *kicked* strong-field orbits near the
   separatrix — plunge classified exactly, Δφ/Δt update bounded, recompile rate measured.
   The same attack applies a fortiori to Kerr (B19's χ ≠ 0), where the separatrix topology
   is richer.
2. **The view: "each visible tube crosses the past light cone once" + per-doll deflection(b)
   memo** (premise 5). Near a compact mass, image multiplicity is generic (fold caustics:
   pairs of images are born and die as the observer moves); Newton from the previous frame's
   crossing cannot *discover* a new crossing — it needs a caustic-crossing detector. And a
   deflection memoized per doll assumes bending angles add through *nested* dolls — that is
   board bottleneck 1 ("moments add, the flow does not") restated for light. Coverage: r6 is
   cost-only; B16 tests one boosted lens, not nesting or multiplicity. **None.** Not measured
   here; [INFERENCE] from caustic geometry. Principle 30 ("navigation, knowledge and dynamics
   those need to be perfect") and principle 4 (single-image is a category, not a number).
3. **Dense ≡ sparse bit-identity for events across relativistic dolls.** The tie rule
   (redteam-6254, law.md line 47) canonicalizes same-epoch batches on the *root clock*; the
   map of a relativistic doll's events onto the root clock is law.md's own open item, so B8's
   "CPU/GPU, sparse and dense" identity is untestable for cross-doll same-epoch batches until
   that exists. Partially covered (B8); the gap is named, not fatal.
4. **Cost table "≈ 0 for undisturbed" + memo sharing.** Already half-known (5 Oct taste log:
   the exact memo hits 0% on distinct kicks; the quantized memo is a law change). My Fermi at
   the table's own kick rates (recompile ≈ 30 crossings ≈ 1.5 µs; 6×10⁴ kicks/s ≈ 0.1 core)
   says the premise survives in orders of magnitude — except in strong field, where it fuses
   with attack 1. Survives with a caveat.
5. **Premise 1 (EOB, ν only in the energy map): survives** — r3 v3 confirmed it (1024/1024
   precession, 64/64 assists). The extrapolation "dolls all the way down" to
   strongly-gravitating triples is untested, but that is exotic (my blind spot).
6. **Premise 2 (Binet cells): already dead inside the design** — law.md line 20 replaced the
   in-band area-preserving map (first-order slope error at turning points) with Darwin
   compilation on 30 September; `representation.md` §1 still states the dead version. The
   surviving claim — exact per-cycle repetition with constant Δφ, Δt, Δτ — is exact for
   Schwarzschild geodesics (my quadrature *is* that statement; C1 cross-checks it). Survives.

Principles violations found: the jet near the separatrix violates principle 13 ("errors never
compound" — the phase error sits in the description and reaches encounter timing) and the
design's own §2 error budget ("at most one floor unit per event" — exceeded by 6–9 orders);
principle 21 wants the certificate, and the certificate exists but treats C as a constant.

## What would make it wrong

If near-separatrix orbits can be routed wholesale to an always-recompile path (the allocator
choosing by a dimensionless number, e.g. r_peri/r_ISCO) — then the *measurement* stands but
only the cost line changes, and the regime-flip test per kick is still required (a kick can
move an orbit *into* the band from outside; only a post-kick test sees it). If near-BH orbits
never receive kicks in practice — false: encounters and player thrust are O(1) there, and
law.md itself schedules inspiral through this regime.

## Cost of adopting

Small and local: (1) one algebraic separatrix/plunge test on the post-kick (E, L) — the Darwin
cubic's root count, already computed at cycle compile; (2) forced exact recompile inside a
declared band (recompile-per-kick there: honest, and the band is small); (3) a frozen gate
criterion (kick-then-classify in strong field, near-separatrix Δφ/Δt bounded). It converts a
silent wrong-type error into a bounded one. It deletes nothing else.

## The lens

Red-teams overweight exotic cases, so I ranked by player visibility: BH-adjacent scatterings
are the showpiece content and the engine already freezes at this boundary. What I may have
missed: attacks 2 and 3 are argued, not measured (lensing gather simulation was over budget);
Kerr untested; and I attacked the *live* law.md version of the premise, not only the stale
representation.md text, which is where the burden actually sits.
