# Dossier — 20261021-0213-redteam-901c (lens: premise red-team)

## Claim

The design's kink law (`docs/representation.md` L50: "Thrust grows the rapidity linearly
in proper time; in a field, E and L change by the work done") is half wrong and half
under-determined: the work-rule clause is dead as written (it under-reads a burn's ΔE/ΔL
by 38–57% at relativistic speed and over-calls the burn-to-escape 3.0× at r = 6 M), the
shipped `thrust.rs` does **not** implement it (it is exact: 0.0–1.3e-13 against the GR
invariants, and its boost is the exact constant-felt-acceleration law), and no rung in
`lab/rungs/` has any thrust arm — the player's most-used law has never been judged by an
oracle.

## Bottleneck

Not a cost row: a correctness premise of `docs/representation.md` §2 ("Decisions are the
only kinks"), load-bearing for every player and AI maneuver. Julien: "what really matters
is navigation, knowledge and dynamics those need to be perfect" (OC#16). Expected gain:
deletion of a wrong sentence before builders implement it (the code comment in
`thrust.rs` L7 already repeats it verbatim and misstates its own law). The exact
replacement is one multiply-add per burn in the frame the boost already lives in.

## Evidence

All numbers regenerate with `regen.sh` (≈1 s, float64, `kink_law.py`; oracle = exact
Schwarzschild invariants E = √f·γ, L = r·p_φ and a DOP853 powered-geodesic integration at
rtol 1e-12; controls below). Scene: prograde impulse at a circular orbit, one event,
same boost for every arm.

**1. The letter's work rule vs exact GR (ΔE_letter/ΔE_exact, ΔL same to 3 digits):**

| start | η=0.05 | η=0.25 |
|---|---|---|
| flat (w₀=0.5, SR channel only) | 0.625 | 0.523 |
| r = 6 M | 0.510 | 0.427 |
| r = 10 M | 0.712 | 0.618 |
| r = 20 M | 0.854 | 0.765 |
| r = 100 M | 0.966 | 0.898 |
| r = 10⁴ M | 0.997 | 0.951 |

Two error channels stack: the SR kinetic one (Newtonian ½v² under-reads dγ at ~1/γ³
longitudinally — present at any r, 38–48% at w ≈ 0.5–0.66) and the GR one (√f and the γ
in L = r·p_φ). Escape threshold (prograde rapidity from circular to E = 1): the letter
over-calls the burn 3.04× at r = 6 M, 1.61× at 10 M, 1.22× at 20 M, 1.04× at 100 M.

**2. The shipped `thrust.rs::burn` is exact and is not the sentence.** Float replica of
the shipped path (coordinate v → static frame → boost → back → rebind): post-burn E, L
match the exact invariants to 0.0–3.6e-16 (worst 1.3e-13 at 10⁴ M, η=0.25). Algebraic
identity: its `along = n + u·(u·n)/(γ+1)` satisfies |along|² − s² = 1, hence |dU/dτ| = α
exactly at any attitude — clause 1 holds in the engine's convention, and the map is the
exact Fermi–Walker nose-carried rocket u(η) = u·cosh η + (n + u·s/(γ+1))·sinh η (flat
prograde lump composes to 1.3e-15 at any cadence, `flat_speed_err`).

**3. The sentence under-determines the law.** At a radial impulse (r = 6 M, η = 0.25):
ΔL/L₀ = 0 (exact Lorentz boost along the heading — transverse proper velocity is
invariant) vs **+3.14%** (the shipped/FW map: p_φ → p_φ·cosh η; ΔL = +0.1088 against
L₀ = 3.464) vs 0 (the letter's torque rule, right by accident). The impulsive reading
also violates clause 1 (felt acceleration = α√(γ²+s²) > α at γ > 1). Over a held-heading
burn (r = 6 M, Δτ = 5 M, Δη = 0.25): impulsive-lump E = 0.9457 vs continuous FW/compass
E = 0.94138, dL/L −0.116 vs −0.1034; the two clause-1-consistent readings (nozzle
FW-carried vs gimbal-held on the compass) coincide to ~1e-5 there.

**4. Flush deferral is first order in the flush quantum** (engine lump vs its own
continuous law, gravity exact both arms): r = 6 M relerr_E −0.184% at q = 2⁻⁶ → −0.047%
at q = 2⁻⁸ (×3.95); r = 20 M −0.0016% → −0.0004% (×3.98); flat prograde exact at both
cadences. The composition error is gravity × obliquity only; position lag is also first
order in q (dr −8.6e-3 M at r = 6 M).

**Controls (instrument green):** flat geodesic conservation drift 0.0; weak-field
shipped replica 0.0/3.6e-16; flat lump composition 1.3e-15 at both cadences; torque-free
radial arm consistent (letter 0, axis 0). The exact escape speed is the textbook
√(2M/r) local (my first draft had √(1−f²); corrected by the control, see Predictions).

## Predictions

`predictions.md` was written before the decisive run. Outcome: **P3 held decisively**
(shipped replica 0.0–1.3e-13 vs predicted <1e-12). **P2 held** at r = 6 M (0.427–0.431
vs predicted 0.4–0.6) but its escape sub-claim failed in direction: the letter
**over**-calls the escape burn (3.0× at 6 M), it does not under-call — my pre-registered
Fermi used E = f·γ instead of E = √f·γ; the code caught me, the textbook identity
(w_esc = √(2M/r) local) confirmed it. **P1 partially failed**: the weak-field letter
ratio is 0.951, not 1±0.01 — because the letter's error has a flat-space SR channel my
Fermi missed; the kill is stronger, not weaker. **P4 held**: 0.18% at q = 2⁻⁶ (predicted
0.1–3%), refinement 3.95× per 4× (predicted ≥4×: marginal, honestly first order).

## What would make it wrong

- My `boost_thrust_rs` replica diverging from the shipped integer code (mitigated: the
  algebra is quoted line-by-line from `thrust.rs` and verified two independent ways —
  invariants at an event, and closed-form flat composition).
- "The work done" having a canonical relativistic reading I did not test. I tested the
  Newtonian reading (the sentence's frame) and the letter's own L-analogue; any reading
  that reproduces ΔE = √f·Δγ exactly is no longer "the work done" but the invariant map.
- Cost of adopting: one sentence in `representation.md` (L50) and one doc comment in
  `thrust.rs` (L7) — replace with the exact closed form ΔE = √f·Δγ, ΔL = r·Δp_φ (an
  addition in the local frame, principle 3's own rule), plus naming the nose convention
  (FW-carried, the shipped choice). No engine change: the code is already exact.

Fit with PRINCIPLES: the letter violates its own principle 3 ("Every quantity is kept in
the form in which its change is an addition") — E and L in the doll are exactly that
form and the work integral destroys it; principle 30 ("navigation … needs to be
perfect") is the behaviour at stake; principle 2 (the oracle judges behaviours) is what
no rung ever did to this clause.

## The lens

A premise red-team overweighting the letter's *phrasing* could miss that the shipped
code is already exact: the finding is a doc/code divergence and a rung gap, not an
engine bug. I did not re-attack the surviving census premises (doll 1PN, dense≡sparse,
undisturbed≈0) and did not test the plane's Newtonian doll rebind after burn (main-side
transitional code, out of the design's scope).

## Grade suggestion

Silver-to-gold: real, reproduced by controls, one rung-shaped hole named (no thrust arm
exists anywhere), adoptable in one sentence — but it moves correctness, not a measured
10× cost row.
