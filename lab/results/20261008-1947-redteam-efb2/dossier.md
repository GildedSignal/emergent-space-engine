# Dossier — 20261008-1947-redteam-efb2 (premise red-team, docs/representation.md)

**Claim:** The design's light-cone crossing solver ("Newton from the previous frame's") survives every
γ up to 2×10⁶ in the tube's own frame, but the view's "one sample per pixel" becomes a lying instrument
at the game's signature speeds — a periodic emitter whose received stream exceeds ~1 orbit per frame
(γ ≳ 125 for a 0.3c compact pair at 60 fps) renders frozen or strobed (measured 75–100 % frozen), and
no rung would catch it; separately, the same solver written in raw observer-frame magnitudes silently
mis-locates the emission event at the queue's target γ = 10⁶.

**Bottleneck:** the view/observation premise (representation.md §2, lens item 5), not a compute
bottleneck. Gain: prevents shipping a view that is wrong exactly when the player flies fast toward
something — the game's promise ("lets the player feel what living at high c would feel like"). Deletes
nothing; adds one memo table (k-averaged sprites) and one spec line (the crossing's number form).

## Evidence (float, ~30 s per run; commands reproduce everything)

Machine: GitHub Actions Linux, 8 vCPU, load 0.67 (idle), 13 GB free, numpy 1.26.4. Counts, not
timings — machine-independent.

```
cd lab/results/20261008-1947-redteam-efb2/work && python3 gather_falsifier.py     # ~30 s
```

Scene: 32 emitters on a ring R = 0.2 light-s at orbital speed β_o; observer coasts toward them at
closing β; 60 frames/s of observer **proper** time, 200 frames; D0 = 100 ls (2×10⁷ ls at γ = 2×10⁶).
Both readings solve for the same emission event (same physical scene, same tube parameter t′):
A = arrival equation in raw observer-frame quantities, B = in the tube's (doll) frame,
C = rate-extrapolated guess + Newton (control). Truth: bisection (F strictly monotone).

| γ | β_o | A iters/fail/wrong | B iters/fail/wrong | received orbits/frame | apparent Δφ/frame |
|---|---|---|---|---|---|
| 1–70.7 | 0–0.3 | ≤3.2 / ≤0.1 % / 0 | ≤2.9 / 0 % / 0 | ≤0.56 | = true (clean) |
| 125 | 0.3 | 2.8 / 0.1 % / 0 | 2.1 / 0 / 0 | **0.995** | **+0.000 (75 % frozen)** vs true −0.033 |
| 245–255 | 0.3 | 2.6 / ≤0.2 % / 0 | 1.5 / 0 / 0 | **1.95–2.03** | +0.000 (**87–98 % frozen**) |
| 2×10⁶ | 0.01–0.3 | 2.0–2.9 / 0.2–3.3 % / **6156–6353 of 6336** | 4.0–9.7 / **0** / **0** | 530–1.6×10⁴ | ≈0 (**81–100 % frozen**) |

- **B (doll frame) never fails and never picks a wrong root at any γ ≤ 2×10⁶.** Iterations grow with
  emitter speed β_o (contraction ≈ β_o), not with γ: staleness is free because F is globally
  near-linear in the tube parameter.
- **A (raw observer frame) at γ = 2×10⁶:** ~99 % of solves it reports as converged sit > 10 s of
  emitter time from the true root (up to ~10⁴ s ⇒ fully wrong orbital phase), 0.2–3.3 % cannot polish
  at all. Cause, verified directly: F is a difference of terms ~8×10¹³ s (ulp = 0.0156 s) with slope
  ~10⁻⁶ s/s ⇒ root ambiguity ≈ ulp/slope ≈ 10⁴ s. At reachable γ it is harmless (γ = 70, D0 = 4 ly,
  β_o = 0.3: worst phase error 1.5×10⁻³ rad, still 4 decades worse than B's 4×10⁻⁸).
- **Frozen/strobe (the player-visible failure):** once ≥ ~1 orbit of emitter history arrives per frame
  (k·Δτ ≳ T, k = √((1+β)/(1−β))), one instant sample per pixel cannot represent what the observer
  receives. Measured apparent phase advance ≈ 0 while the true received sweep is 1–16,000 orbits per
  frame. Boundary: γ ≈ T/(2·Δτ)/2 ⇒ 63–126 for a 0.3c compact pair (half-orbit smear at 63), 377–753
  for β_o = 0.05, ≈1.9×10³ for β_o = 0.01 at 60 fps — the last sits *inside* the plane's γ = 2,000
  envelope, and γ = 10⁶ is a queued build ("γ to 10⁶"). Below the boundary the render is honest
  (γ = 2.3, β_o = 0.05: apparent = true = +0.018 rad/frame).

## Predictions (predictions.md, written before the run)

- P1 ✓, P2 ✓ (inertial: 1 iteration at all γ; β = 0.9 matches H0213's working 0.9c gather).
- **P3 ✗ and P5 ✗ (doll frame): falsified — and that is the result.** My predicted failure onset γ*
  and ≥90 % failures at 10⁶ assumed the stale root leaves Newton's basin; in fact the arrival equation
  in the tube's parameter is globally near-linear, so the first Newton step absorbs any staleness. The
  premise survives. P5 holds only for the raw observer-frame reading (99 % wrong roots).
- P4 ✗ unnecessary: rate extrapolation (C) buys nothing over B (equal at high γ, slightly worse
  mid-range). P6 ✓ in the doll frame; in float, quantization (not multiple roots) defeats the
  monotone-function guarantee in the observer frame.

## Ranked attacks (lens deliverable)

1. **The view's temporal sampling (player-visible, no gate).** "One sample per pixel" + "aggregates
   are one sample each" alias any periodic emitter whose received stream exceeds ~1 orbit/frame:
   frozen or backward-rotating forward systems at γ ≳ 10² (0.3c pair) — the wagon wheel, in the
   signature maneuver. **Rung: none.** r6 is unwritten and scoped as "Newton iterations and samples
   per frame" — counts, no γ axis, no temporal-truth criterion; B16 is the lens's deflection, B7 clock
   rates, B18b belt tails. Proposed r6 criterion: over γ ∈ {1 … 10⁶}, a periodic emitter's rendered
   stream must equal its received history's average (k-averaged sprite law passes; the instant-sample
   law must fail).
2. **The crossing's number form (correctness rot at the queue's γ).** Same sentence, other reading:
   in raw observer-frame magnitudes the emission event is mis-located by up to ~10⁴ s at γ = 10⁶
   (verified: ulp/slope). The fix is one spec line: solve in the tube's frame, in cell-relative
   differences (the law's own integers are safe; a float replica in raw magnitudes is not). **Rung:
   none** — B8 checks bit-identity, not conditioning; r6 must add "polish to the law's quantum at
   γ ∈ {1…10⁶} in the shipped number form; a raw-magnitudes control must fail."
3. **Doc rot (premise 2).** representation.md still presents the in-band Binet/Minsky map as "the
   primary in-cell solution" and "crossing a ring conserves E and L" (river refraction) — both killed
   (law.md: space-darwin16-v1 replaced the in-band map for a first-order slope error at every turning
   point; r1/H0204 killed refraction). The kick layer also omits the re-anchor rule (df81) that law.md
   carries. A builder reading the design doc rebuilds killed configurations. r1 **did** catch river
   refraction; the miss is doc governance (principle 11: "delete when built").
4. **B11's tolerance absorbs what it should falsify (premise 1).** Precession allowance
   (1 % + 2·8/p) reaches ~80 % at p = 20 M, exactly where the ν-only-in-energy-map's 2PN error is
   largest: the gate cannot falsify the two-body doll at the strong end. Letter weakness, same class
   as the integrator's r2/r3 criteria (a criterion that cannot fail is a control). Named: B11.
5. **Premises 3, 4, 6 — no new attack; they stand with named open risks.** Kicks + cycle derivatives:
   survives only with df81's re-anchor (C·drift², ~730 correlated kicks). Dense ≡ sparse: defended by
   the tie rule; open items are already named (root-clock keys across dolls; mid-interval reads).
   Cost ≈ 0 for undisturbed bodies: unmeasured (H_live), B10 defers — the §6 table is an estimate,
   honestly labelled.

## What would make it wrong

The frozen metric is a median-phase statistic across 32 emitters (it can hide structure, though the
≥1-orbit/frame cases are analytic aliasing regardless); the boundary γ scales with frame rate (∝ fps),
so 144 Hz moves it √(144/60)-fold higher; A's breakage is float64-magnitude-specific — the integer
law's band arithmetic might avoid it, untested on the real crates (I did not run the engine). The
γ ≥ 60 cases need the player to fly at speeds the plane only reaches near its refusal limit — but
"feel living at high c" is the goal, not an edge case (Julien: "we need to build towards GR … the rest
are stepping stones").

## Cost of adopting, and fit with PRINCIPLES

Adoption: (a) k-averaged sprites — one memo per (spectral type, log k), additions, per §2's own
"type × log k table"; the per-pixel sample cap is unchanged. (b) One line pinning the crossing's
number form to the tube's frame. (c) r6 written with a γ axis and both controls. Fit: principle 28 —
"The view is an instrument … your dials are made up and hold no informations": a frozen forward system
is a dial that lies. Principle 32 — the doll-frame solve is the symmetry made explicit: same physics,
trivial conditioning. Principle 34 — "the oracles are guards, not shepherds": r6 must exist to fail an
instant-sample law, not to size the view.

## The lens

A premise red-team overweights exotic cases; I ranked by player visibility, but my strongest measured
failure still needs γ ≳ 60–125 or the queue's γ = 10⁶, and I spent the run on the view premise (lens
item 5) after only desk-checking items 1–4 against r3 v3/B11/df81/H0204 rather than re-running them.
What this lens may have missed: a same-budget attack on the AI-perception premise (the same gather at
each AI's own light cone — if each of 10⁶ AIs gathers like the player, the aliasing boundary applies
to every AI's decisions, not just pixels), and the fleet-scale case (differential Doppler across a
formation at γ = 2.3 shears the ring — real physics, but I did not check whether the gather's
"previous frame's crossing" cache survives a whole fleet crossing the aliasing boundary mid-flight).
