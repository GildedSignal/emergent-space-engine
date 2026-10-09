# Dossier — run 20261009-1556-redteam-18fc (premise red-team)

## Claim

The view-gather premise ("each tube crosses the observer's past light cone once; Newton from the
previous frame's crossing finds it", representation.md §2) **survives its hardest regime on the
shipped code** — emitters closing at β up to 0.99999 and the mutual case (observer 0.9c × emitter
0.9999c) — with zero dropped emitters, zero cold-vs-memo disagreements and ≤ 1.84 readouts per
emitter per frame; the red-team's predicted failure mode (slope-clamp lag → dropped emitters) is
falsified, and the surviving risk moves to unmeasured kinked tubes and to AI-perception Doppler
bunching, both of which r6/r7 (open rungs) own.

## Bottleneck

Not a bottleneck mover: this is a premise audit on the design's §7 ladder before adoption. It
removes the last unmeasured extreme (near-c closing content, the design's own worst case:
bottleneck 5's "near-c 50 cm missile", the "γ to 10⁶" queue item) from the view premise, at the
cost of one 5-second example (`view_extreme`) that any later run can rerun.

All numbers from the shipped crate (main tree, no edits to library code; one new example added),
Linux x86, ~5 s per invocation. Raw tables: `work/rtf1.txt`, `work/rtf100.txt`, `work/rtf1000.txt`;
the harness itself: `work/view_extreme.rs` (also `crates/universe/examples/view_extreme.rs`).

```
cargo run --release -p emergent-universe --example view_extreme -- 1 600      # real time
cargo run --release -p emergent-universe --example view_extreme -- 100 600   # the plane's flying speed
cargo run --release -p emergent-universe --example view_extreme -- 1000 200
```

rtf 1 (3383 ticks/frame, 600 frames, 24 emitters at 1e6 ticks, Toward):

| case | reads/em | max/frame | drops | disagree |
|---|---|---|---|---|
| slow across (control) | 1.00 | 25 | 0 | 0 |
| 0.9c across (control) | 1.06 | 48 | 0 | 0 |
| 0.9c toward (view_rel's top case) | 1.16 | 43 | 0 | 0 |
| 0.999c toward | 1.68 | 67 | 0 | 0 |
| 0.9999c toward | 1.73 | 87 | 0 | 0 |
| 0.99995c toward | 1.70 | 86 | 0 | 0 |
| 0.99999c toward | 1.64 | 76 | 0 | 0 |
| observer 0.9c × 0.9999c toward | 1.84 | 72 | 0 | 0 |

rtf 100 and rtf 1000: same shape — 1.0–1.2 reads/emitter average, worst frame ≤ 163 readouts
(≈ 7 per emitter), zero drops, zero disagreements. Full tables in `work/`.

Why it survives (read off the code, `crates/universe/src/view.rs::crossing`): with the
relativistic rate `g′ = 1 + n·β`, `g` is exactly linear in the emission tick for a straight
tube, so one bracketed Newton step lands on the root from any guess; the slope clamp (1e4,
`ViewCache::put`) only degrades the *guess*, never the result, because the walk is bracketed
and the answer is the bracket, not the iterate. The prior red-team (20261003-2306-redteam-4570)
already fixed the Newtonian rate reading; this run shows the fix holds to the design's worst
case.

## Predictions

`predictions.md` was written before the run. P1, P2 (controls, reproduction) held. **P3/P4
(drops at 0.99999 / mutual-speed from clamp lag) are falsified** — no drop in any of the 2400
gathered frames per configuration. P5 (arrival compression: the whole 1.2e9-tick approach of a
0.9999c emitter is seen in ≈ 0.35 frames at rtf 100) is real and visible as the worst-frame
readout bursts, but was not instrumented per crossing tick.

## What would make it wrong

- All emitters here are **bare tubes** (straight worldlines, no force): the exact-linearity
  argument above fails for kinked tubes (thrusts, kicks, doll handoffs at relativistic speed),
  which are precisely the game's combat content. One experiment away: the same harness with a
  thrusting emitter.
- Apparent-position *correctness* was only cross-checked cold vs memo (bit-identical), not
  against an independent retarded-time oracle; a shared bug in both paths would hide. The
  lens's blind spot (exotic-case overweighting) applies: the player more likely sees a *cost*
  p99 spike than a wrong pixel.

## Cost of adopting

Nothing to adopt in the engine; keep `view_extreme` as the r6 ladder's cheap edge case
(β = 0.9999, 0.99995, 0.99999, mutual 0.9 × 0.9999) and fold "no drop, cold = memo" into r6's
criteria when it is frozen (r6 is open: law.md line 88).

## The lens: ranked attacks, each with the rung that owns it

1. **View gather at closing β → 1** (premise 5, this run): **survives, measured.** Rung: r6 —
   open, none has run; this run is the first data at β ≥ 0.999.
2. **AI-perception Doppler bunching** (the new lead): the same 1/(1−β) compression that the
   gather survives means an approaching relativistic emitter delivers its entire perceptible
   history bunched into ~1/(1−β) observer frames (up to 1e6 at the mutual case). "An AI is
   recomputed only when what it sees crosses its perception threshold" (representation.md §2)
   then schedules a decision burst — the p99 risk the cost table's "AI decisions" row does not
   price. Rung: r7 (exists, unrun). No rung criterion covers burst arrival compression.
3. **Dense ≡ sparse bit-identity** (premise 4): not re-attacked; guarded by gate B8 and one
   fixture (H0207's battle, bit-identical), r5 open. Say so, don't redo.
4. **Cycle readout cost** (premise 6): representation.md's "reading one out takes a
   multiply-add" is stale against law.md's honest "one Newton solve inside a panel" — a doc
   line to fix at adoption, not a physics risk; measured gather cost above supports the ≈ 0 row.
5. **Near-separatrix cycle derivatives** (premise 3): analytic check only — ∂T/∂E diverges as
   e→1 but the first-order cycle update stays exact to O((δE/E)²) ≈ 10⁻⁶ for a 10⁻³ kick; the
   failure needs δE/|E| ≳ 0.1, which is not a perturbation. Not worth a run. Rung: B9 already
   covers e ≤ 0.99.
6. **Binet cells, EOB doll** (premises 1–2): survivors by prior evidence (r1 in H0205; r3 v3
   confirmed, ν 500/504) — not re-attacked; no new attack found that their frozen criteria miss.

## Fit with PRINCIPLES

- Principle 34 ("the oracles are guards, not shepherds") and 10 ("measure before claiming"):
  the premise was believed on β ≤ 0.99; it is now measured at the design's own worst case.
- Principle 20 ("behaviours over many seeds"): 24 bearings × 600 frames × 3 rtf per case; every
  frame, both evaluation orders.
- The lesson of the 5 October memo artifact (agreement ≠ independence when one harness produces
  both paths) is why the cold-vs-memo identity here is reported as *weak* evidence of
  correctness and the kinked-tube gap is left open.

## The lens's blind spot

A red-team overweighting exotic cases would have shipped P3/P4 as "likely broken"; the clamp
looked fatal from analysis and was not. What this lens may still have missed is the *cost* side
under heat and the kinked-tube regime (attack 1's caveat), both outside a 60-minute window on a
shared machine.
