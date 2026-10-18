# Dossier — 20261018-1433-redteam-915d (lens: premise red-team)

## Claim

**The additive-attitude premise is dead at the game's own speeds: representation.md thesis 3
("every quantity is kept in the form in which its change is an addition") and L50 ("thrust
grows the rapidity linearly in proper time"), as shipped in `thrust.rs`'s heading accumulator
(`owed`: "The heading turns by ±turn·Δτ"), cannot represent the non-abelian part of the boost
group — the frame rotates by exactly (γ−1)·ψ for a constant-γ turn through ψ (certified at
every grid point, γ to 7.1), the seen sky and the thrust direction both go with it, and the
error feeds back into the trajectory: 12–74° nose error, up to 0.27 c speed error and 6.6–48%
position error inside single maneuvers at β ≥ 0.866 — while the cure is the doc's own §1
algebra (unit split-quaternions: one multiply per burn, and a held burn is a one-parameter
subgroup, i.e. a generator, cheaper than today's per-flush composition).**

## Bottleneck

Not a board row: a premise of bottleneck 0 (the representation). It deletes the accumulator
law and the page-frame view orientation, and it adds the one component of SO(2,1) the design
cannot store today. Gain: correctness of the game's core loop (the player's own turning
flight, principle 30), not a 10× in cost — though the fix is also cheaper (closed-form held
burns).

## Evidence

All numbers from `python3 falsifier.py` (≈9 s, pure float, c = 1, flat local orthonormal
frame — the doll's; the exact model composes SO(2,1) matrix exponentials, the shipped replica
is `thrust.rs`'s law verbatim in the flat limit: accumulator heading + exact proper-velocity
boost composition along it, so the only difference modeled is where the thrust direction
comes from).

**Instrument certification (controls, both sides):**
- Two perpendicular boosts (φ = ψ = artanh 0.9, γ = 2.294 each): the frame rotation is
  **42.8961988683492° = 2·atan(tanh²(φ/2)) = atan2(sinhφ·sinhψ, coshφ+coshψ)** to 3·10⁻¹⁴
  (block contamination of Bp⁻¹B: 10⁻¹⁴). Order swap flips the sign exactly.
- Collinear flight (nose ∥ v, Δη = 1): sky rotation 0.0 exactly, β error 1.4·10⁻¹⁴.
- Pure turn at β 0.866 (ω·τ = π, no thrust): sky rotation −1.8·10⁻¹³ ≈ 0 (rotation commutes;
  the accumulator is exact when nothing composes).
- Step-halving: sky changes 1.3·10⁻¹¹°; constant-γ holds in the prescribed instrument (γ
  1.2500, 2.0000 … to 4 decimals).

**The law (prescribed constant-γ turns, the physics instrument): sky = −(γ−1)·ψ, exactly,**
at every grid point (the competing form (1−1/γ)·ψ is refuted, 2× off at γ 2):

| β (γ) | ψ = 90° | ψ = 180° | ψ = 360° | (γ−1)ψ |
|---|---|---|---|---|
| 0.1 (1.005) | 0.45° | 0.91° | 1.81° | 0.45/0.91/1.81 ✓ |
| 0.5 (1.155) | 13.92° | 27.85° | 55.69° | ✓ |
| 0.6 (1.250) | 22.50° | 45.00° | 90.00° | ✓ |
| 0.866 (2.000) | 90.00° | 180.00° | 360.00° | ✓ |
| 0.95 (3.203) | 198.23° | 396.46° | 792.92° | ✓ |
| 0.99 (7.089) | 547.99° | 1095.99° | 2191.97° | ✓ |

A 180° course reversal at γ 2 turns the entire seen field by 180°; one holding loop at
β 0.6 turns it by 90°. At the record's own pump speeds (γ 5–63) a single reversal is
hundreds of degrees.

**The game's own flights (same keys, exact vs accumulator):**
- **off45 held burn from γ 2** (nose 45° off v, the record's off45 family, Δη = 1):
  sky −18.0°, nose 12.1° off where the game says, position error **6.6% of path**.
- **off135 brake from γ 2** (the held-brake family): sky −26.2°, nose **55.8°** off,
  final speed off by **0.27 c**, position error **22.3%** of path.
- **wide turn to reversal** (ω = 1.4, T = 3, open-loop, velocity turns 156°):
  sky −74.4°, nose 73.2° off, final velocity direction **133.4°** off, position error
  **48.2%** of path. The feedback loop: once the nose is wrong, thrust compounds it into
  the trajectory.

Shipped grounding: `view.rs` L309 aberrates with velocity only and orients on the page
("the heading axis is the page's", L54); `view.rs` L293 takes the heading from the same
accumulator; `lorentz.rs`'s `Frame` is a pure boost (rotation–boost–rotation). No Thomas
term exists anywhere in the tree. Same disease, different organ, as e8f7's doll keys ("the
re-emit must compose boosts, not sum shears", handoff.md L141) and its noted "Wigner axis
error… owned by the spatial turn machinery if anyone's" (L157) — this run is that owner, and
the machinery is the player's own flight.

## Predictions

`predictions.md` was written before the run. **9/10 held** (P1–P5, P7, P8 held; controls
exact; the two-boost Wigner 42.9° inside the predicted (20°, 60°); the γ 2 reversal's 180°
> 90°; the β 0.6 loop's 90° inside [50°, 130°]; position errors > 5%). **P6 missed, honestly:**
I predicted the off45 burn passes 30° before the velocity turns 90°; measured: the off45 burn
turns the velocity only ~45° in total (it nearly doubles γ instead) and the sky reaches
18.0°; the off135 brake reaches 26.2°. The >30° magnitudes belong to real turns (the sweep
table), not to that brake parameterization.

## What would make it wrong, cost, fit

- **Wrong if** the game declared the doll-frame accumulator to *be* the law (attitude =
  doll-parallel by fiat): deterministic, but then the sky the player sees at β ≥ 0.5 is not
  the sky a human would see — against principle 30 ("I want the player to feel what a human
  would feel in space, it's about immersion"), which is this game's stated core. Or if
  players never exceeded β 0.1 (0.45° per loop) — the record flies γ 2–63 daily.
- **Cost of adopting:** one unit split-quaternion (4 numbers) per live body under thrust; one
  quaternion multiply per burn flush (a decision — the doc's own "multiplications appear only
  at surprises"); the view gains one rotation per frame. Cheaper than what it replaces: a
  held burn at constant keys is a one-parameter subgroup, B(τ) = B₀·exp(Aτ), a closed-form
  flush. `lorentz.rs` already composes boosts by shears; e8f7 sketched the same composition
  for doll keys.
- **Fit with PRINCIPLES:** principle 19 — "if you find yourself fixing things that's oftentimes
  a signal that it is the wrong representation"; the accumulator is the wrong representation
  and the right one (§1 L40: "Rotations and boosts are the unit split-quaternions") is already
  in the doc, contradicted by thesis 3's letter. Principle 6 — "Store the generator, not the
  generated": a held burn *is* a generator. Principle 2/13 — error *type*, not size: the
  missing rotation is a whole component of the Lorentz group; no carry width shrinks it.
- **No rung sees it:** §7's ladder (r1–r7) has no attitude/thrust/turning criterion; B-gates
  judge counts and orbits. The falsifier to freeze: *a turning flight at γ ≥ 1.1 must carry
  the Thomas rotation (γ−1)ψ in the seen sky and the nose; negative control: the accumulator
  (must miss by exactly (γ−1)ψ).* The two closed forms certified here are the bars.

## The lens

The lens's blind spot is exotic cases; this attack is ranked by player visibility and lands
on the player's own turn at β ≥ 0.5 — the core loop, not an edge. What the lens may have
missed: the field half (geodetic precession in Schwarzschild dolls — handoff.md's Fermi-frame
chart already prices that channel for fleets); this run certifies the flat local-frame
composition, which is where the structural term lives. Second blind spot: I did not run the
shipped binary itself; the shipped law is quoted from `thrust.rs` (`owed`'s accumulator,
`burn`'s exact composition) and replicated verbatim in the flat limit — a tree run should
fly one off-axis burn to confirm the wiring reads as the letter says.

## Wiki

Page: `wiki/representation-premises.md` (result folded in as a NEW block, one Refuted entry,
one Runs line).
