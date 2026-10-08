# Dossier — red-team of `docs/representation.md` (run 20261008-1613-redteam-7922)

## Claim

The design's kick→cycle premise ("a kick updates the cycle by a multiply-add",
representation.md §3; law.md's jet at "≈0.05 compiles per kick") has no
separatrix carve-out, and its recompile horizon is not a constant of the law
but shrinks as (1−e)^(2/3): measured 25 kicks at e = 0.99 vs 342 at e = 0.5
(0.073 measured vs 0.074 predicted), which concentrates belt compile cost
~112× on the e = 0.99 body and puts 15% of a B18b belt's compile crossings on
its top 1% — and no rung, gate or history entry measures any of it.

## Bottleneck

Board focus items 1 and 4 (fewer kicks per orbit; smoothness/the allocator).
Expected gain: none in physics; the finding sizes a mis-budgeted cost and
names the dimensionless trigger that must own it. If unadopted, the risk is
p99 body cost ~50–100× median in exactly the frozen belt scene (B18b),
against principle 12 ("i care about the p95/99 results i want the game to be
smooth").

## Evidence

Commands (float, 3.3 s total, Linux x86):

```
cd lab/results/20261008-1613-redteam-7922 && python3 falsifier.py
```

Model: Kepler (the two-body doll's weak-field limit at belt scale), banded p,
exact re-solve after each orbit-averaged kick vs law.md's jet (cycle compiled
once from (E,L), offsets exact, cycle updated by stored ∂T/∂E). Floor 1e-6
relative (law.md's). Kicks δE = 1e-7·GM/2p per orbit (averaged-tide scale;
all *ratios* are kick-size independent, absolute horizons scale as δ^(-2/3)).

- **Horizon n\*(e)** (kicks before the periapsis-epoch error crosses 1e-6):
  e = 0/0.3/0.5/0.7/0.8/0.9/0.95/0.99/0.995 → 543/428/342/243/186/117/74/25/16.
  Scaling checks: n\*(0.99)/n\*(0.5) = 0.073 vs (1−e)^(2/3) = 0.074;
  n\*(0)/n\*(0.5) = 1.588 vs 2^(2/3) = 1.587. The cause: at fixed periapsis
  |E| ∝ (1−e), so every physical kick is relatively huge near the separatrix
  (δE/|E| ∝ 1/(1−e)), and ∂²T/∂E² ∝ (1−e)^(−7/2).
- **The failure is confined to the time channel.** The angle channel (apsidal
  advance; GR 1PN 6πM/L² depends on L only, and L² = p(1+e)GM stays finite as
  e→1) sits 300×–10⁵× below the floor at every horizon. The memo's Δφ is
  safe; its Δt/epoch is not.
- **Correlated (secular) kicks are the worst case**: random-sign kicks survive
  5–16× longer (n² vs n³ error growth), so secular tides — the belt's actual
  kick mode — are the regime that mis-sizes.
- **Belt arithmetic** (B18b's own scene: Rayleigh e, σ = 0.3; 0.3 kicks/orbit
  from H0190; crossings per cycle 2m·log₂((1+e)/(1−e))+8 from B9): median
  body 0.027 compile-crossings/orbit; p99 = 7×; p99.9 = 46×; the e = 0.99
  body = 112×; bodies with e > 0.9 (1.1% of the belt) carry 15% of total
  compile crossings. Compiles/kick at e = 0.99 is 0.04 — already at law.md's
  0.05 budget at *averaged-tide* kick scale, and that budget was measured
  once (df81: ~730 correlated quantum kicks) without an e-sweep.
- **A2 (secondary, analytic Darwin 1959): strong deflection is outside every
  light gate.** α(b) ≈ −ln(b/b_c−1) − 0.400 diverges logarithmically
  (2.14 windings at (b−b_c)/b_c = 1e-6); the first relativistic image of an
  aligned source sits 0.58/0.88/1.15 mrad outside the shadow edge at
  r_o = 10/6/4 M (0.6–1.1 px at 1080p, 60° FOV). r1's light seeds and B3
  draw b log-uniform in [10, 1000] while b_c = 5.196 M: the entire
  strong-deflection regime is unmeasured, and a single-valued, uniform-b
  deflection memo cannot place even the n = 1 image (needs (b−b_c)/b_c
  resolution ~1e-3 and winding bookkeeping).

## Predictions

`predictions.md` was written before the run. **P1 held** (0.073 vs 0.074
point, band [0.03, 0.15]). **P2 held** (angle channel ≥300× under floor).
**P5 held** (random ≥5× longer). **P4 held after a sign fix I caught in my
own A2 table** (first image 5.8e-4 rad at 10 M vs predicted ~5e-4; my first
run's 1.3 mrad was an e^{∓C0} sign error, now corrected in the script).
**P3 half-held, honestly reported**: the top 1% does concentrate cost (15%
of crossings; 14–112× the median body), but my predicted p99 > 100× median
was wrong — measured p99 = 7×; the >100× concentration lives beyond p99.9,
not at p99. The belt tail is smoother than I predicted; the premise hit
stands on the p99.9/tail bodies and the 15% share, not on p99.

## Ranked attacks (the lens's deliverable), by player-visible likelihood

1. **A1 — the separatrix has no carve-out** (measured above). Rung that
   should catch it: **none**. r1's bound seeds stop at e = 0.7; B5's growth
   exponent is a median-seed statistic; B9 gates crossings per cycle
   (creation cost) at e ≤ 0.99 but never multiplies by the recompile rate;
   B11 (e ≤ 0.6), B14 (e₀ ≤ 0.3), B17 (e₀ = 0.02) all sit low; H0178 even
   pins the oracle to "bound, non-separatrix anchors". df81's horizon and the
   0.05 budget were measured without an e-sweep. The resonance got its
   carve-out ("averaging only away from resonance", representation.md §3);
   the separatrix needs the same sentence, and the re-anchor trigger must
   carry per-cycle C ∝ (1−e)^(−7/2) (equivalently: trigger on the
   dimensionless (δE/|E|)·n^(3/2), not on a global rate). Cheap criterion
   for a rung: recompile rate and compile-crossings per orbit across the
   e-tail of a B18b belt, median and p99, negative control = a global-rate
   trigger planted to fail at e > 0.95.
2. **A2 — strong deflection / photon ring ungated** (analytic + numeric
   above). Rung: **none** (r6 is unwritten; r1/B3 light seeds never approach
   b_c; B19 classifies capture at b± but never deflection approaching it).
   Proposed r6 criterion: at r_o ∈ {4, 6, 10} M the gather places the n = 1
   relativistic image of an aligned source within 1 px of Darwin's offset
   with bounded Newton iterations; negative control = single-winding
   uniform-b memo.
3. **A3 — process premise: two of the ladder's rungs do not exist.**
   representation.md §7 freezes r5 (dense = sparse, bit-identical) and r6
   (view); `lab/rungs/` contains neither file (checked 8 October). The two
   premises that carry §6's cost table are judged nowhere; B8 covers contacts
   only. Rung: none, by construction.
4. **A4 — 1PN EOB's ν-blindness ends before the plunge** (comparable masses,
   a ≲ 10 M: ν enters the effective potential at 2PN+, so plunge timing and
   the ISCO of an equal-mass pair are off in a regime the player will visit
   once mergers fly). Known and queued (plunge tubes, rotating holes, B19);
   B11's seed gate (next-term 5/a²) excludes it by construction. Cited, not
   probed: no new evidence here.
5. **A5 — representation.md's primary in-cell solution is already dead.**
   §1 still presents the Binet/Minsky rotation as "the primary in-cell
   solution"; law.md replaced it with `space-darwin16-v1` because band-centre
   tangents carry a first-order slope error in every cell holding a turning
   point. Caught during the build by r1's `repeat`/`prec` criteria family;
   the doc is stale on its own headline claim.
6. **A survivor (worth pinning): the flat-space gather premise is true.**
   "Each visible tube crosses the observer's past light cone once"
   (representation.md §2): F(τ) = τ + d(τ) has F′ = 1 − β·n̂ ≥ 1 − β > 0 for
   any subluminal emitter — bound, unbound or kinked, per tube segment, in
   flat spacetime. Multi-imaging is purely gravitational (A2's regime).
   This proof should be r6's positive control (a flat gather converging in
   ≤ K Newton iterations at all β), so the multi-crossing work is spent only
   where gravity causes it.

## What would make it wrong

The jet model is Kepler with analytic GR scalings, not the integer darwin16
cycle; if the shipped re-anchor trigger already uses per-cycle C (law.md's
√(floor/C) is ambiguous between per-cycle and global), the *error* stays
bounded and only my cost numbers stand; if it is a global rate, the error
compounds at high e exactly as measured. One look at the crates decides — I
did not run them (float-only lens budget). Kick size 1e-7/orbit is my tide
scale; horizons scale as δ^(-2/3), ratios do not move. The belt arithmetic
inherits B18b's Rayleigh-0.3 and B9's crossings formula. A2's offsets are
Darwin's asymptotic form (exact to ~% near b_c; Bozza 2002).

## Cost of adopting, and fit with PRINCIPLES

Adoption is one sentence in law.md (the separatrix trigger) plus two rung
criteria (recompile-vs-e on the belt scene; image placement near b_c for
r6) — hours, not a component. It fits principle 3 ("Compute only surprises":
the surprise rate *is* δE/|E|, which spikes at the separatrix, so the
compute must follow it there), principle 12 (the p99/p95 smoothness the tail
attacks), and principle 33 ("a body resolves only the influences that are
significant at its own scale" — near the separatrix a tide stops being
small). It contradicts nothing in PRINCIPLES; it sizes a promise the design
made without a number.

## The lens

A premise red-team overweights exotic cases; I ranked by what a player meets
(belts and flybys daily, black-hole close passes occasionally). What the lens
may have missed: I did not run the integer crates (so the shipped trigger's
per-cycle-vs-global reading is unverified), I left the dense/sparse premise
(A3 in the lens list) at the process level rather than probing it, and the
two-body doll's 1PN claim was taken as settled by r3 v3 rather than
re-attacked. The "≈0 cost for undisturbed bodies" premise survives for
motion (cycle additions) but its per-body p99 dies through A1's tail.
