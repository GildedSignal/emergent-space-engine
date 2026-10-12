# Predictions (written before the decisive run)

Attack: premise 4 of representation.md §3 — "two evaluation orders of the same event
graph, with identical bits" — as shipped in `crates/engine` (B8's evidence base). The
identity ladder (`crates/engine/tests/identity.rs`) covers only battles whose bodies all
move at fleet speed (q/8..q/32 per component, β ≤ ~0.18, one speed class per scene). The
player's headline action — a relativistic body crossing a battle — is untested.

Falsifier: the shipped battle scene (100 bodies, q = 1024, seed 2, div 8) plus one
interceptor of mass 1, radius q/2, at k = [900, 0] (β = 0.88, γ = 2.1), timed to cross
the engagement zone mid-battle; variants at k = [720, 240] (β = 0.74) and two opposing
interceptors (a near-c pair). Same Frame, both orders (`Chronon` lockstep vs `EventCore`
sparse), horizon 4096. Controls: the shipped s1 scene (positive, must agree), and the
epoch-shift-by-1 plant on my scene (negative, must disagree — proves the instrument
detects differences).

## P1 (identity, the decisive prediction)

Lockstep and sparse give identical world, log and tide digests on every flyby variant.
Rationale: the lattice law is discrete-time by construction (contacts are exact integer
bin meets at ticks), the event graph is shared, and the tie rule keys on (time, body id,
kind). If any variant's digests differ, premise 4 is falsified in the shipped artifacts.

## P2 (cost, the p99 exposure)

The sparse order pays grid re-forms for the fast body (its velocity exceeds the cells'
velocity bound), so sparse's rebuilds ≥ 1 on every variant, and sparse's wall time
relative to lockstep grows compared with the shipped scenes' ratio. If the sparse/lockstep
time ratio on the flyby scenes exceeds ~5× the shipped scenes' ratio, the allocator's p99
premise (representation.md §3, one queue by slack; principle 12) is exposed at exactly
the player's headline action: one fast body churns the sparse structure of a whole
battle.

## P3 (coverage, secondary)

At least one variant produces a contact involving a relativistic-closing-speed pair
(the battle's contacts guarantee > 0 overall; I check the interceptor crosses the zone
during the horizon). If the interceptor never shares a tick-local neighbourhood with a
battle body, the scene is weak evidence and I say so in the dossier.

## Kill criteria

- P1 failing on any variant: premise 4 killed (KILL of the "identical bits" claim as
  shipped; the fix would be a new tie/detection rule, a law change).
- P1 holding: premise 4 survives this attack; report as a strengthening result plus the
  measured P2 numbers.
