# Dossier — 20261006-0346-redteam-df81 (premise red-team on docs/representation.md)

## Claim

The design's per-kick mechanism — "a cycle's derivatives are stored with it, so a kick updates the cycle by a multiply-add" (representation.md §3) — has an unbounded, compounding error as written: measured error = C·(accumulated drift)² with C ≈ 1.9 for the angular increment, which crosses the law's own 10⁻⁶ floor after a drift of only 7×10⁻⁴ (730 correlated kicks of 10⁻⁶, 8 of 10⁻⁴, inside B5's 10⁴-cycle horizon); the fix (a re-anchor rule whose cost is 38/n* crossings per kick) is absent from the design and its cost table, it fails outright for the design's own listed monotone kick source (Peters inspiral: 1.1×10⁻² drift per orbit at a = 20M, ν = 0.25 — re-anchor every orbit, jet useless), and **no rung on the ladder tests it**. Two premises survive measurement: the flat-spacetime view gather (2–3 Newton iterations at β up to 0.99) and the ≈0 cost of undisturbed bodies (B9).

## Bottleneck

Board focus #1: "kicks dominate the engine's cost" (fewer/cheaper kicks). The multiply-add is the mechanism behind the cost table's "≈50 ns per kick, <1% of a core" and behind the 600× step down from today's measured 29 µs per kick (HANDOFF, plane bottleneck 3; the plane recompiles on ~99% of kicks). Motion law v2 (briefed to Astra on 9 October) inherits this mechanism verbatim. The gain at stake is not a new speedup but protecting the claimed one: with a re-anchor rule the interior keeps ≈50 ns + 0.05 crossings/kick; without one the error compounds; for inspirals the promised path does not exist and the honest representation is Peters' analytic a(t) as its own generator (a deletion, principle 1).

## Evidence

All commands run from `lab/results/20261006-0346-redteam-df81/`, each ≤ 20 s, float64, 8 vCPU Linux (cloud; orders of magnitude only).

**F1 — the jet under correlated kicks** (`python3 f1_jet.py`, output `f1_out.txt`, 17 s):

Oracle: exact Schwarzschild bound-orbit cycle increments (Δφ total angular advance, Δt radial period) by Darwin-ψ 64-node Gauss–Legendre quadrature. Instrument control: quadrature vs the exact elliptic form 4K(k)/√(2(u₃−u₁)), k² = (u₂−u₁)/(u₃−u₁): worst relative deviation 8.3×10⁻¹⁶ over p ∈ {20, 50}M, e ∈ {0.1…0.995}. (The first run used the precession 2π(1/κ−1) instead of the total advance 2π/κ as the control and was VOIDED by its own pre-registered rule; disclosed here.)

- **Jet error law:** error(n) = C·δ(n)² where δ is the accumulated fractional drift since the anchor. Confirmed in both correlation modes: systematic δ = nε gives n* = √(floor/C)/ε (measured 730 at ε = 10⁻⁶; 8 at ε = 10⁻⁴, C = 1.88, floor 10⁻⁶); random-sign δ ≈ √n·ε gives n* = floor/(Cε²) (measured 56; predicted 53). The mechanism is exactly second order **in drift**, so correlation, not size, is what kills it.
- **C is nearly e-independent** for Δφ (1.88 at e = 0.5, 2.03 at e = 0.995): the near-separatrix orbit is *not* where the jet degrades (my prediction P4 was wrong). For Δt at fixed E, C collapses as e → 1 (0.103 → 1.9×10⁻⁴): Kepler's L-independence of the period protects it.
- **Energy kicks (Peters-like, dE ∝ |1−E|):** Δφ is safe (C_E small), but Δt fails: n* = 755 at ε = 10⁻⁶; at ε = 10⁻⁴ the end error is 1.000 (the period is 100% wrong after 10⁴ cycles).
- **Negative control (frozen increments, no derivatives):** fails in 1–2 cycles at ε = 10⁻⁴, in 2–668 at ε = 10⁻⁶ — the harness detects drift.
- **Grounded kick sizes:** Peters inspiral (the design's own §3 example) gives |Δa/a| per orbit = 1.1×10⁻² at a = 20M, 1.1×10⁻³ at 50M, 2.0×10⁻⁴ at 100M (ν = 0.25) — all in the catastrophic row. Post-averaging belt tides (oscillatory, ~10⁻⁶–10⁻⁸/orbit) are in the safe row; the design's own near-resonance rule (one kick per conjunction, phase-locked) produces correlated sequences in the unsafe row.
- **Implied re-anchor cost:** 38 crossings per n* kicks = 0.052 crossings/kick at ε = 10⁻⁶ (a real overhead the cost table does not carry, ~5–10% of the kick budget if a crossing costs about a kick), and 4.75 crossings/kick at ε = 10⁻⁴ (worse than the 38-crossings-per-cycle compiled cost the design already accepts for unperturbed orbits — but on every kick).

**F2 — the view gather's Newton conditioning** (`python3 f2_view_newton.py`, output `f2_out.txt`, 19 s):

Emitters on circular orbits (β_e ∈ {0, 0.3, 0.6}), observer flying through at β_o ∈ {0, 0.9, 0.99} (the game's 0.9c stream, B15), ~1° of emitter orbit per frame, truth by bisection, Newton seeded from the previous frame's root. Result: median 2–3 iterations, max 3, zero escapes from the causal window, zero non-convergences, max |t_e − truth| = 2.3×10⁻¹³, at every speed combination. g′ = 1 − β_los > 0 keeps Newton tame in flat spacetime. **This premise survives** — my P7 held exactly.

## Predictions

`predictions.md` was written before both runs. Outcomes: P1 failed on first run (wrong control formula — precession vs total advance), fixed, machine-precision agreement after; disclosed above. P2 held (negative control fails fast). P3's functional form held exactly (error = C·δ²) but my arithmetic for n* was wrong (predicted 10⁶ at ε = 10⁻⁶; the correct √(floor/C)/ε = 730, which is what I measured). P4 failed (the separatrix does not worsen the jet; C is e-flat for Δφ and collapses for Δt). P5's form was corrected by the measurement (random-mode error is C·n·ε², i.e. floor/(Cε²) in n*, not a √N rescaling — measured 56 vs predicted-after-the-fact 53). P6 held. P7 and P8 held (the view survives).

## What would make it wrong

- If the law's "exact offset plus stored derivatives" (law.md, the jet clause) is read as *anchoring at the quantized memo key with the body carrying its exact (E,L) offset*, then the jet's error is ~C·(key quantum)² ≈ 10⁻²² for 32-bit keys — bounded forever — and my compounding result applies only to representation.md's bare text. The re-key cadence (quantum/ε kicks) still couples kick size to key width: at ε ≥ 10⁻⁴ with a 32-bit key over E ∈ [0.9, 1] (quantum 2.3×10⁻¹¹) the body re-keys every kick, and the cost returns. Both readings need the missing rule; neither rescues the Peters row.
- If kicked bodies in the real populations never accumulate 7×10⁻⁴ of correlated drift between recomputes (e.g. if every kick already pays a recompile today and always will), the finding is about the design's cost table, not the shipped law.
- My quadrature oracle is exact Schwarzschild (test body); at 1PN-EOB level the C values would differ by O(M/p), not the conclusion.

## Cost of adopting

Small and surgical: add the re-anchor rule and its cost term to representation.md §3/§6 and to motion law v2; replace "inspiral by Peters' formula" as a kick source with Peters' a(t) as a generator (a deletion); add one rung criterion (below). No crate changes.

## Fit with PRINCIPLES

- Principle 13 ("basically we don't want errors that can compound that's the goal"): the multiply-add as written compounds; §2's "Shortcuts reproduce the law exactly, so they add speed, never error" is falsified by F1 for the jet shortcut.
- Principle 1 (less is more; the cheapest compute is compute not done): Peters' inspiral is analytic — evolving it by kicks pays per-kick cost for a closed-form motion.
- Julien's tails rule (board, 29 September: "averages crush tail events"): the kick cost row is an average over a distribution whose tail (correlated sequences: inspirals, resonance-adjacent belts, the player's own repeatedly-kicked transfer orbits) pays 10–100×.
- Principle 10 (measure before claiming): the 50 ns/kick row and the view row are now measured (one falsified in its tails, one supported).

## The lens (what this red-team lens may have missed)

Red-teams overweight exotic cases; I ranked by player visibility, so the photon ring, compound-lens image multiplicity and the Kerr ergosphere went unmeasured — the two unmeasured view risks (cross-doll simultaneity, flagged open in law.md; lensing image-count composition) remain open, and my F2 covers only the flat half. I did not run the integer law; the float result is about the mechanism's error law, not the crate. A lens focused on memory or on the dense order might have found the bit-identity attack sharper than I did.

## The ranked attacks, with the rung that should have caught each

1. **Kicks × cycle derivatives (premise 3) — falsified as written** (F1 above). Catcher: **none exists.** B5 judges the unperturbed cycle (10⁴ cycles, no kicks); B9 judges crossings per cycle; B12 and r10 exercise recompute paths; the memo-hit question was measured (5 Oct) but the jet's validity domain never was. Proposed criterion for the motion-law-v2 rung: *over 10⁴ correlated kicks of size ε at e ∈ {0.3, 0.9, 0.99}, the running increments Δφ, Δt stay within 10⁻⁶ of exact recompute, and re-anchor work ≤ 1 crossing per 10 kicks* — with the frozen-cycle update as the negative control.
2. **The view gather (premise 5) — flat half survives (F2); two halves open by argument.** (a) The cross-doll time map (relativity of simultaneity) is flagged open in law.md and sits under the whole gather at high relative doll speeds — the flagship regime. (b) "Lensing adds crossings, from each doll's memoized deflection(b)" composes deflections but not image counts: a source behind two lenses has up to five images, and the composition of two single-doll maps misses the pair's extra images (binary lenses are in the goal's population). Also **occlusion is absent**: "one sample each… nothing bounces" carries no visibility test, so transits and eclipses — everyday sky events — are missing behaviours. Catcher: **r6 is listed in §7 but not frozen** (no file in lab/rungs); B16 judges single-lens deflection magnitude only.
3. **Dense/sparse bit-identity (premise 4).** Identity requires (i) canonical serialization of concurrent contacts (sequential pairwise resolution is non-commutative), (ii) certificates that reproduce the law exactly — F1 shows one shortcut whose error is not bounded per event, and a certificate built on the jet would inherit it, (iii) symmetric re-anchoring across orders. Measured once: one battle, 10 periods, 0.44% re-anchor drift (H0207). Catcher: **r5 is listed in §7 but not frozen.**
4. **Two bodies as one doll at 1PN (premise 1).** True at 1PN (r3 v3: ν only in the energy map, assists 64/64) and ν-failing by construction at 2PN (a₄ and the D-potential carry ν). Order-of-magnitude [INFERENCE, not measured]: the 2PN/1PN periastron ratio is ~ν·(M/p)·O(1–10), so the law's own 1% precession band fails at p ≈ 60–600M for ν ≈ 0.25 — comparable-mass binaries, which the goal's population includes. r3 v3's seeds used μ = 10⁻³, so no rung covers comparable-mass strong field. Named next experiment: 2PN-EOB periastron quadrature vs the 1PN doll at ν ∈ {0.1, 0.25}, p ∈ {20, 50, 100}M.
5. **Binet cells (premise 2) — survives.** r1's reproduction (m16/m32: precession, periods, deflection, capture, ISO, shape over 10⁴ cycles, exact repetition, ~38 crossings per cycle) stands; nothing here contradicts it.
6. **≈0 cost for undisturbed bodies (premise 6) — survives as stated.** B9 bounds crossings and grants "zero work per orbit until an event"; the caveat is that every kick is an event, which is attack 1, not this premise.

## Files

`predictions.md` (pre-registered), `f1_jet.py` + `f1_out.txt`, `f2_view_newton.py` + `f2_out.txt`. Reproduce with `python3 f1_jet.py` and `python3 f2_view_newton.py` (numpy + scipy, ~17 s and ~19 s).
