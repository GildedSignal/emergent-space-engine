# Dossier — run 20261018-0035-redteam-22d1 (premise red-team)

## Claim

The page's proposed cure for §2's missing opacity — "static occlusion is one interval test
per row" (e59e's direction 5, the cheapest wiring of representation.md L59's screen cap) —
is the wrong law at the game's own velocities, in both of its natural forms: the snapshot
test mis-times every eclipse by the full light time d/c (100 s at fleet distances) and puts
the blackout in a disjoint sky patch once β·d/R ≳ 2, and even the render-consistent sprite
wiring (everything drawn retarded) is not parity, its onset error unbounded in d (+15 s at
d = 100 ls, β = 0.5; +125 s at β = 0.9) — only the exact per-row segment-vs-worldtube test
is the law, and it prices at ~70–80 ns/row (not the bill).

## Bottleneck

The view's correctness half (`view`, 45 runs; the board's "not here" list puts cost with
r6). The blocker removed: the wiring decision for the occluder test, which must be frozen
before the lensing memo lands (e59e's open directions 2 and 5). No 10× compute gain; a
wrong-representation kill (principle 19): both cheap wirings carry an error that grows
with d and β, so no cadence or budget fixes them — the geometry is wrong.

## Evidence

All numbers: `eclipse_parity.py` (exact 2-D flat-geometry float64, c = 1, N = 10⁴ static
sky emitters on a far circle, as e59e; deterministic; ~8 s). Command:

```
cd lab/results/20261018-0035-redteam-22d1 && python3 eclipse_parity.py
```

Wirings: W1 snapshot (occluder at frame time — the letter's static test), W2 sprite (the
occluder exactly where its own light shows it, exact quadratic retarded-time solve), W2p
(the naive per-row offset d·cosψ), W3 worldtube (exact segment-vs-worldline test, the law).

- **Controls.** Static arcs reproduce e59e exactly: 1667/10⁴ (16.67%) at d = 2R, 319
  (3.19%) at 10R, 32 (0.32%) at 100R. Negative control fires: W1 at β·d/R ≥ 5 is disjoint
  from W3 (Jaccard 0.000). Shapiro instrument: quadrature = exact closed form (8.5084 s);
  the 4r_E·r_O/b² log shortcut is +1.8% at b/r ≈ 0.1 (use the closed form).
- **W1 onset error = the light time**, speed-independent to first order: −1.6…−2.0 s at
  d = 2R, −9.6…−10.2 s at 10R, −99.6…−100.6 s at 100R (the analytic −d/c plus the measured
  duration-dilation correction R(√(1+β²)−1)/β; slow-β onsets carry the scan grid's ±0.8 s
  quantization).
- **Arc misclassification (mid-transit Jaccard vs W3):** 1.000 at planet-realistic
  β = 10⁻⁴; 0.847/0.335/0.000 (2R/10R/100R) at β = 0.1; 0.401/0.000/0.000 at β = 0.5;
  0.079/0.000/0.000 at β = 0.9. Held-out oblique 45° arm is worse (0.493 at β = 0.1, 10R).
  The ruler is β·d/R: below ~0.1 every wiring passes, above ~2 the snapshot arc is a
  different piece of sky.
- **W2 (exact sprite) is not parity either:** Jaccard 0.855–0.875 at β = 0.5, 0.42–0.45 at
  β = 0.9; onset error +1.25 s (10R, β0.5), +9.30 s (10R, β0.9), +15.05 s (100R, β0.5),
  **+125.13 s (100R, β0.9)**. Mechanism: the sprite's retarded time (light from occluder
  to observer) is not the encounter retarded time (when the emitter's ray met the
  worldline); the difference grows as ~β²·d, unbounded in d. Rim onset errors confirm the
  same (+0.75 s at 2R, +1.82 s at 10R, β0.5).
- **W2p (naive per-row offset) is worse than the sprite at speed** (at β = 0.5:
  0.784 vs W2's 0.855 at 2R, 0.307 vs 0.865 at 10R, 0.000 vs 0.875 at 100R; at β = 0.9:
  0.522 vs 0.420 at 2R, 0.000 elsewhere): the encounter retarded time carries the sweep
  factor (1+β²)⁻¹, so the cheap per-ray form is not the worldtube test.
  frame-consistent (2/10⁴ grid-edge rows) — the observable that fails is the arc size, so
  a gate on static arcs judges the wrong instrument.
- **Strong field (Arm B):** sprite-consistent differential Shapiro delay across a transit
  at r_o = 20M, b = 10.26M, R_p = 1M is 0.782 s — 19.6% of a β = 0.5 transit's duration
  (4 s), invisible at planet β (0.004%). The naive no-cancel delay (8.66 s) is not the
  observable. delay(b) (5977's missing memo) re-owns eclipse timing at these scales.
- **Price:** the exact W3 test costs 69–79 ns/row vectorised on this box across reruns
  (order of magnitude, shared x86): 10⁵ rows ≈ 7–8 ms/frame worst case, under the screen
  cap. The geometry, not the cost, was the wrong representation.

## Predictions

`predictions.md` was written before the decisive run. P1 held (−d/c, with the measured
correction); P4 held (disjointness threshold β·d/R ≈ 1–2; ≥ 0.969 at planet β); P6 held
(0.78 s, 19.6% ≥ 5% at β = 0.5, invisible at planet β); P7 held (~70–80 ns/row).
**P2 and P3 are refuted by the run, and the misses are the result:** the sprite wiring's
error is not the bounded rim form I predicted (d(1−cosψ), ≤ 0.15 d/c) but an unbounded
~β²·d term (measured +15.05 s and +125.13 s); and the naive per-ray offset is not the
worldtube test (the encounter retarded time is shifted by the sweep factor). P5's
cross-check clause held (17.58/49.77 vs 17.6/49.8) and its "≥ 10% rows misclassified"
clause is refuted — row parity is frame-consistent; the failing observable is the seen
arc size.

## What would make it wrong

The wirings are exact closed-form tests, so the numbers cannot be wrong inside flat
geometry; what would undo the claim: (a) the game never places occluders with β·d/R ≳ 0.1
in view (false — ladder scenes carry a 0.9c stream, r6's standard scene is β 0.5–0.9999,
and a planet at 2R while the player flies past at β 0.5 already sits at β·d/R = 1);
(b) lensing near strong sources dominates before the kinematic term matters (Arm B shows
they compose: 0.78 s delay vs 2.0 s snapshot error at the same scene); (c) the engine's
gather never implements occlusion at all (then e59e's 16.7%-of-sky hole stands instead —
one of the two findings bites either way).

Cost of adopting: the occluder test becomes one exact quadratic per row per occluder
(~20 flops; 69–79 ns/row measured) instead of an interval test on a cached arc — same
order, no new component; the eclipse-parity rung (e59e's proposal) freezes the worldtube
form with the snapshot and sprite wirings as its negative controls, judged in the
observer's frame at player β (17.6°/49.8°, not 30°), plus a duration-distortion bar at
strong field.

Fit with PRINCIPLES: principle 19 — "a fix signals the wrong representation… bandaids
accumulate": both cheap occlusion wirings are bandaids whose error grows with d and β;
the worldtube test is the representation that "does the job like cutting butter"
(the segment test is the same quadratic the contact resolver already is, representation.md
L48: "a ring crossing and a contact are the same operation"). Principle 2 — "behaviours
matter, not continuum fidelity: error type over error size": the snapshot error is a
one-signed light-time offset (a wrong-order-of-events error the player sees as stars
winking in the wrong sequence), the type that matters. Principle 23 — "nothing past c":
the snapshot wiring is precisely an influence placed where the occluder is *now*.

## The ranked attacks (this lens's list, by player visibility)

1. **NEW (this run): the occlusion cure is the wrong law at game velocities** — measured
   above. Rung that should have caught it: none exists; the proposed eclipse-parity rung
   must take the worldtube form (spec in the wiki page's direction 2).
2. Kick-as-multiply-add + ~50 ns (L67/L114): refuted on cost (34.8–75.6 µs, exact memo
   0%; 12db, b063). No rung gates per-kick cost (B9/B10 gate counts and exponents).
3. §2's observable set lacks opacity outright (e59e: 16.7% of sky at a 2R planet, 25% at
   r_o = 6M); now with the wiring law measured (this run).
4. The view's other physics holes: multi-image (6eae), time transfer (5977, gold, no
   gate), moving-lens deflection key (8be2, gold, B16 exists).
5. Binet cells (L32): dead letter, replaced by Darwin (law.md L20); binet-cells page owns.
6. Dense ≡ sparse (L70): survives, guarded by r5 and r5-starve on every axis this lab can
   reach.
7. Two-body doll, ν only in the energy map (L37): survives (r3 v3, B11; licensed
   p̄ ≳ 65M at ν ≤ 0.25).
8. Undisturbed ≈ 0 (L113): survives by rate, not cost (a4ed; kick-cadence owns the crest).

A premise that survives this run is worth as much as one that dies: **the price premise
was right** — occlusion at one test per row is affordable at the screen cap; only the
geometry had to change.

## The lens

Premise red-teams overweight exotic cases; this attack is the opposite corner (a planet
passing a star while the player flies), and its numbers are exact-flat-geometry — the
strong-field composition (Arm B) is first-order only, verified against quadrature but not
against integrated null geodesics (e59e's shadow arcs own that regime). The lens may have
missed: occluder and observer moving together (neither arm composes both — the terms add
to first order but the composition is unmeasured), extended occluders (a fleet doll's
radius vs its members'), and aggregate emitters (one sample each) whose eclipse is a
partial dimming, not a row drop.
