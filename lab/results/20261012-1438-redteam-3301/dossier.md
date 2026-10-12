# Dossier: the view gather's Newton premise breaks exactly where the game lives

Run: 20261012-1438-redteam-3301, lens premise red-team, 12 October 2026. All numbers from
`python3 falsifier.py` (< 25 s, Linux cloud, dimensionless iteration counts — no timing
claims). `metrics.json` holds the full table.

## Claim (one sentence)

The design's view gather — "each visible tube crosses the observer's past light cone once;
Newton's method finds the crossing, starting from the previous frame's" (representation.md
§2) — diverges and renders the sprite up to 23° wrong on exactly the scenes the game sells
(a relativistic orbit or first-sight approach at β ≳ 0.9–0.99), no rung guards it (r6 was
never frozen), and one poisoned frame cascades through the seed chain with no self-healing.

## Bottleneck

Not a hot path today; a correctness hole in the player's only instrument (principle 28:
"the view is an instrument"; principle 30: navigation and knowledge must be perfect). The
view has the hardest deadline (representation.md §3) and the cost row "≤ 1 sample per pixel
per frame" (§6): measured p99 Newton iterations go 2 → 7 (3.5× readouts per emitter) at
β_orb = 0.99, and capped frames are deadline breaches or wrong crossings. Gain: adopting the
fix (bracketed fallback + cascade re-seed + the r6 rung below) deletes a whole class of
wrong-sprite bugs before the plane's gather grows roots in it.

## Evidence (falsifier: flat 2D, c = 1, 60 Hz observer frames, cap 8 iterations, tol 1e-7 s)

Scenes: A constant-β head-on; B circular orbit at β_orb, observer at D0 orbit-radii; C close
flyby at impact parameter b; D1 smooth chase (rapidity linear in proper time, β → 0.998);
D2 the same with an impulsive reversal (a decision kink). Ground truth: bisection over a
provably enclosing bracket. Controls both sides: β ≤ 0.1 passes in ≤ 3 iterations with zero
caps (positive); a cold-start solver (no previous-frame cache) fails 30–46 % of frames at
β ≥ 0.9 in scene B (negative — the cache is load-bearing, and insufficient).

| scene | it p99/max | capped | worst sprite error | note |
|---|---|---|---|---|
| A0.1 / A0.999 | 2 / 2 | 0 | — | compression 1000×, still 2 iters |
| B0.1@3, B0.6@3 | 3 / 4 | 0 | — | control |
| B0.9@3 | 4 / 8 | 1 | 6.7° | first-sight cascade |
| B0.99@3 | 7 / 8 | 11 | **23.3°** | cascade frames 0–10, root jumped ~6×10⁵ s |
| B0.99@10 | 5 / 8 | 0 | — | borderline every orbit |
| B0.995@10 | 5 / 8 | 6 | 9.1° | start cascade + isolated caps at frames 100, 479 |
| B0.999@10 | 5 / 8 | 2 | 7.5° | isolated mid-run cap at frame 102 |
| C (all) | ≤ 3 / 4 | 0 | — | flybys are safe |
| D1chase | 3 / 4 | 0 | — | smooth burn is safe |
| D2flip | 3 / 4 | 0 seeded | — | but cold solver: 1570/2040 capped, permanent |

Mechanisms (distinct, verified by run-structure): (1) **first-sight cascade** — at first
acquisition, when \|n̂·v\| ≳ 0.9, the static seed guess is wrong by the full retarded lag
D/(1−n̂·v), Newton oscillates across the slope dip, and every later frame inherits the
garbage root (no self-healing; 11 consecutive frames at β = 0.99); (2) **periodic slope
dips** — when the emitter's velocity aligns with the line of sight at β ≳ 0.995, g′ = 1−n̂·v
< 0.005 while orbital curvature is O(1): isolated single-frame cap hits mid-run. The
arrival-time compression dt_e/dT reaches 1/(1−β) = 1000 (scene A) harmlessly, so the
premise's failure is not compression alone but curvature × compression.

## Predictions (predictions.md, written before the run)

P1 uniqueness HOLDS (one root per frame everywhere; g′ ≥ 1−β > 0 as derived — the "crosses
once" letter survives). P2 controls HOLD (instrument valid). P3 constant-β compression
HARMLESS — held exactly (2 iterations at β = 0.999). P4 flyby breaks — **missed**: flybys
are safe at every b, β tested. P5 orbit breaks — held (table above). P6 chase breaks —
**missed** for the smooth chase; the impulsive-flip variant instead breaks the cold solver
permanently. Two of four break-predictions held, both misses are reported as such, and the
two that held carry the finding.

## What would make it wrong

A gather implementation that already brackets (bisection or Newton-hybrid fallback) and
re-seeds after a capped frame would show none of the sprite errors — the attack then only
convicts the text of representation.md §2 (and law.md's "gathered at the observer's past
light cone" with no fallback specified). Curved space adds lensed crossings (handled
separately by the deflection memo), so flat-space failure is a fortiori. The plane's current
gather (H0210/H0211: "Newton from the last frame's") has no documented fallback.

## Cost of adoption, fit with PRINCIPLES

Cheap: the arrival map A(τ) is monotone, so a bracketed Newton (Illinois/bisection hybrid)
converges in ≤ ~12 evaluations always; re-seed on cap. This is not a bandaid: carrying the
previous root as *state* and stepping it by the compression factor 1/(1−n̂·v) before
correcting is the representation-native fix — "every quantity is kept in the form in which
its change is an addition" (thesis §3). It respects principle 12 (p95/99 smoothness: the
fallback bounds the worst frame) and principle 13 (errors never compound: no cascade).

## The ranked attacks (the lens deliverable)

1. **View gather Newton premise — BROKEN as specified** (numbers above). Rung that should
   catch it: **r6 (view), listed in the falsifier ladder and assigned to GLM in law.md, but
   never frozen — none exists.** B16 covers moving-lens deflection, not the crossing solve;
   B7 covers clocks; B9/B15 cover cost per body, not per view sample. Proposed r6 criteria:
   over scenes {orbit β ∈ {0.9, 0.99, 0.999} at D0 ∈ {3, 10}, flyby, smooth chase, first
   acquisition}, p99 Newton+fallback evaluations ≤ 4 and zero frames whose crossing lands
   > 0.1° from the bisection truth; negative control: the unbracketed seeded-Newton law
   (this falsifier) must fail.
2. **Two texts disagree on the in-cell mechanism.** representation.md §1 still names the
   Minsky/Binet band rotation "the primary in-cell solution"; law.md line 20 records it was
   killed and replaced by the Darwin-phase compiled cycle on 30 September (band-centre
   tangents carried a first-order slope error at turning points). Any builder reading the
   design builds the dead mechanism. Also r1's sweep stopped at e ≤ 0.7 (B9 covers e ≤ 0.99
   only for cost). Rung: r1's letter (it tested the dead mechanism and passed it at e ≤ 0.7);
   nothing re-tests the *compiled* cycle at e > 0.7 precession — B1's 256 seeds sample p
   log-uniformly, e ≤ 0.7.
3. **The kick multiply-add vs the measured recompile reality.** representation.md §3: "a
   kick updates the cycle by a multiply-add." The plane recompiles on ~99 % of distinct
   kicks (taste log, 5–6 October; the quantized kick memo is already "not adopted",
   law.md line 35, re-anchor jet at 0.05 compiles/kick). Unguarded remainder: no rung judges
   the *first-order Taylor* of the jet for large kicks (a close satellite flyby changes E, L
   by more than the derivative window); B13 judges ΔE, ΔL themselves, not the predicted
   post-kick cycle. Rung: none — B12/B13 stop at the kick magnitudes.
4. **Dense/sparse bit-identity for the new Fermi-frame dense order.** Premise: "Both orders
   give identical bits" (law.md §Causality). r5 was never frozen (lab/rungs/ has none);
   the bit-identity ever measured (H0207) was on the old Clohessy–Wiltshire frame with a
   linear epicycle, since replaced by Fermi normal coordinates with re-anchoring. B8 promises
   the check at the law's freeze. Rung that should catch it: r5/B8 — unrun. Risk point: a
   re-anchor event mid-window in the dense lockstep.
5. **Two-body doll (EOB, ν in the energy map only) — SURVIVES, with a bounded corner.**
   Confirmed by r3 v3 (precession 1024/1024, periods 632/632, ν 500/504, assists 64/64) and
   B11. Held-out corner: B11 admits ν ≤ 0.25, e ≤ 0.6 and its own next-term band 8/p; the
   comparable-mass high-e merger corner degrades to truncation error there — the design
   already routes inspiral to Peters' generator. No action.
6. **"Undisturbed orbits ≈ 0" — SURVIVES structurally, with one leak to note.** Compiled
   tubes make per-orbit work zero (B9 gates it). The leak: cells hold integer mass moments
   of everything, and a streaming fleet crossing rings must update two cells' moments per
   crossing — O(traffic), not O(surprises) — unless the moments are derived from population
   programs (shipmem's path) rather than maintained. Worth one line in the design.

Principles check (the lens's second question): the unbracketed Newton is the only place
found where the design asks for an unbounded synchronous claim on the frame, which plane.md
§7 (bounded work per frame) already forbids for every other component — the gather was
simply never given the same treatment.

## The lens

Red-teams overweight exotic cases; I ranked by player visibility: orbits at β ≳ 0.9 near a
compact mass and first acquisition of a fast approacher are core scenes (B15's ladder
already includes a 0.9c stream; B19's Kerr χ = 0.998), not exotica. What this lens may have
missed: everything instrument-level (memory layout, GPU), and the AI-perception side of the
same gather ("an AI's perception is the same gather at its own past light cone") — the
recompute-threshold mechanics (r7) interact with these crossings in a way this run did not
test.
