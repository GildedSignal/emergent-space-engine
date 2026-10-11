# Dossier — 20261011-0517-taleb-3ebf

## Claim

The phase-neighbour certificate's premise — "every real encounter lies within partner rank k
along the orbit" (gold 20261006-0346-taleb-09b5) — is a property of **equal periods**, not of
concentration: inside one period group it holds (controls reproduce it), but in a battle between
fleets it fails silently — 64% of encounters dropped when grouping by element clump (equal-period
crossing fleets), and no along-orbit rank at all catches a different-period interception (cross
partners at median rank n/2, max 0.7·n) — while the only exact fallback materializes n² candidate
pairs (measured exponent 2.00), so the certificate as gated ("the gold run's scenes and a dense
ring") would ship blind to the game's central event.

## Bottleneck

The top scaling risk (board, 5 October): "candidate pairs per body grow with N … candidate work
must track real encounters", and the risk adopted from the gold: co-orbital concentration breaks
the pairwise tier. This run is the pre-freeze red-team of the queued build `b-coorbital-cert`
(AGENTS: "Before any freeze, one GLM red-team and the cheapest falsifying probe must have run").
Gain: it prevents freezing a certificate whose gate cannot fail on battles; it also gives the
build its correct grouping key for free (period, not element clump — measured below), which makes
the equal-period battle a 19× pair-count win instead of a 64% silent miss.

## Evidence

All scenes 2-D, ρ = 1e-3, deterministic seeds; truth = the crate's independent conservative-
advancement truth (Halley states vs the method's Newton); every scene ≤ 15 s wall, full set 35 s
on the shared runner (8 vCPU, load 0.5–1.1, 13 GB avail; recorded in `battle.jsonl`). Orders of
magnitude only (cloud Linux box; the integrator re-measures on the M1).

Reproduce:

```
cd lab/results/20261011-0517-taleb-3ebf/work/encounters   # copy of crates/encounters, unmodified lib
CARGO_TARGET_DIR=/tmp/taleb-battle-target cargo run --release --bin battle     # all 8 scenes, ~35 s
```

Scene builders: a fleet = phase packet of width 0.5 rad on one orbit family (a ∈ [1, 1+1e-4],
Rayleigh e σ = 3e-4); `b1` = two such fleets, periapsis directions π/2 apart, co-located (equal
periods → a standing battle each orbit); `b2` = fleet B on a transfer orbit (a = 1.07, e ≈ 0.0655)
crossing A's packet at perihelion at t = 2 orbits (the interception). Full JSON per scene in
`battle.jsonl`; code in `work/encounters/src/bin/battle.rs`.

| scene | n/fleet | enc | cross | caught by fleet-local rank k≤256 | caught by union rank k≤256 | kmed / kmax union rank of cross partners | cone cross pairs |
|---|---|---|---|---|---|---|---|
| f1-formation (control) | 300 | 9315 | 0 | 1.000 (k=16) | 1.000 | — | 0 |
| ring-dense (control) | 600 | 3496 | 0 | 1.000 (k=8) | 1.000 | — | 0 |
| b1-cross | 75/150/300 | 1989/7995/34832 | 72/61/64% | **0.28/0.39/0.36 plateau** | 1.000 (k=8/16/32) | 1–4 / 7–31 | 5625/22500/90000 = n² |
| b2-intercept | 75/150/300 | 1319/5118/20330 | 12/10/11% | **0.88 plateau** | **0.93 at k=256** | **67/166/284 / 100/217/423** | 5625/22500/90000 = n² |

Key measured facts:

1. **Controls reproduce the gold's regime** (known side): formation kmed rank 2, dense ring kmax 5;
   window tier 0 misses; `outside_cone` = 0 in every scene (the cone candidate set is sound, so
   the instrument is not leaking).
2. **Equal-period battle (b1).** Cross-fleet pairs are 61–72% of all encounters. A certificate
   grouped per element clump (each fleet its own group — the natural reading of "co-orbital
   group", the fleets are two clumps in (V, W)) plateaus at 0.28–0.39 for every k: **the majority
   of the battle is dropped, silently** (no error; only the independent truth sees it). The
   *union* phase sort — legitimate because the periods are near-equal, so the sort is
   quasi-eternal — catches 100% with k growing ∝ n (kmax 7/14/31 for 150/300/600 bodies), and the
   window tier it replaces costs 179,700 sections for the same encounters: **group by period, not
   by element clump** (19× fewer pairs, zero misses).
3. **Interception (b2).** The fleets differ in period, so no phase sort is eternal: cross partners
   sit at **median rank ≈ n_total/2, max 0.70·n_total** (67/166/284 median at 150/300/600 bodies);
   even k = 256 leaves 7% of all encounters uncaught at n = 600. The catching k scales with n, so
   the "O(n·k) certificate" degenerates to the quadratic tier. The only exact path — the Binet
   pair tier — materializes **every** cross pair (cone_cross = n² exactly, exponent 2.00) at ~400
   setup evals per pair (transversal numeric windows): 35.8M evals for 90k pairs at n = 300/fleet.
   Extrapolated to 10⁶ ships per fleet (the goal's fleet scale): 10¹² cross pairs, 4·10¹⁴ setup
   evals ≈ 10³ days on this box, or (b1-style Full sections) ~60 TB of stored certificates — the
   gold's 40 TB class of ruin, now *between* groups, where no certificate exists.
4. **Scaling exponents** (n = 75→300 per fleet, fixed packet width): cone_cross 2.00, cross setup
   evals 1.97–2.02, cross encounters 1.91–1.98. Encounters are themselves quadratic at fixed
   packet width (per-pair meeting probability constant: 2.5% b2, 24% b1), so work per real
   encounter is flat (b1 window tier 286–293 evals/encounter; b2 ~16k setup evals/encounter): the
   quadratic is not waste relative to events, it is ruin in absolute terms at fleet scale — and
   the *silent miss* is ruin at every scale.
5. **The window tier stays exact on battles** (misses 0, one 1-of-22178 event in b1-300): the
   fragility is not in the pair machinery, it is in the group tier above it.

## Predictions

Written and frozen in `predictions.md` before the b1/b2 runs (controls already run). Outcome:
predictions 2, 3, 4, 6, 7, 8, 9, 11 held (8 of 11), most quantitatively (union-rank kmed ~ n/2
predicted as ~n/4–n/5, measured 0.47·n; plateau values as predicted). Three misses, diagnosed:
- #1: cross fraction predicted ~50%, measured 61–72% (b1) — the battle dominates even more than
  guessed.
- #5/#10: setup evals per cross encounter predicted ∝ n (candidates n² vs encounters n); measured
  flat, because encounters are quadratic at fixed packet width (per-pair meeting probability
  constant). The measurement corrected my model; the invariant that survives is work per
  encounter, which is flat everywhere.

## What would make it wrong

- If the build's "dimensionless concentration number" already keys on integer period equality
  (not element clumps), finding 2's silent miss is moot (b1 covered) — but finding 3 stands:
  different-period group pairs have no certificate, and the gate still cannot see it.
- If fleets in the real game are never phase-concentrated when they meet (spread over the whole
  orbit), b1/b2 degrade toward the belt case the two-tier certificate already handles; the
  fragility's constant scales with concentration. But a fleet that is not concentrated is not a
  fleet: the game's own extreme event is the concentrated one.
- The interception geometry tested is one Hohmann-like crossing, 2-D coplanar. The rank argument
  is structural (setup-time phase distance between groups is ~random whenever periods differ), so
  inclinations should not save it, but that is inference, not measurement.

## Cost of adopting, and fit

Adoption is one edit to the `b-coorbital-cert` build spec, before it freezes: (i) the grouping key
is the integer period (belt `keys`), never the element clump; (ii) the gate's scene list adds two
scenes — an equal-period crossing pair of formations, and a different-period interception — with
zero misses required against the truth; (iii) the design names the missing cross-group tier: at a
group-pair crossing epoch, a merge-join of the two groups by predicted along-track position
(each group's participants at the crossing are a contiguous range of its own phase sort), which
is O(participants), not O(n_A·n_B). No engine code changes; the two gate scenes reuse this run's
builders as-is.

PRINCIPLES: "not making mistakes matters more than doing things efficiently, don't multiply by
zero" (#25) — a certificate that silently drops the player's battle multiplies the game by zero
at its moment of maximal interest; "a test that cannot fail is a control" — the planned gate
scenes are single-population, so the certificate cannot fail on the one event it must survive;
"Write the kill criterion before the run" — `predictions.md`, held.

## The lens

Taleb prizes the extreme event and may over-weight it: I maximized concentration (0.5 rad
packets) to make the fragility legible; sparse meetings degrade gracefully toward the handled
belt case. The lens also says nothing about how to build the fix — the merge-join hint above is
one sentence, not a design. Untested here: the slack skin (`b-encounter-skin`) — cadence, not
discovery, is untouched by these scenes; and 3-D inclined crossings. The golden discovery of this
run (group by period, union sort catches the standing battle at 19× fewer pairs, zero misses) is
a positive result the fragility framing almost hid.
