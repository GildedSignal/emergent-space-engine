# Dossier — second author on 20261011-1234-redteam-6eae (the view's "once" premise)

## Claim

The view's "each visible tube crosses the observer's past light cone once" is player-visibly
wrong by exactly **two** — the direct k=0 image and its Einstein partner on the mirror sky
half, jointly visible (>1/50 relative magnification) for **43% (r_o=100M) to 84% (r_o=3.2M)
of emitter azimuths** — while the winding families that make the count unbounded are
**never player-visible anywhere** (max relative magnification 0.0111, per-winding decay
≈ e^{−2π} ≈ 1/535), so the fix is the k=0 branch pair plus a magnification cutoff, **not**
the winding-indexed multi-sheet memo the original proposed; the record now regenerates, and
the repaired weak-field control validates the instrument against the Schwarzschild
deflection series to 3PN (2×10⁻⁴ relative).

## Bottleneck

Not cost: correctness of the plane's own measured bottleneck (the view gather is 83% of a
light frame, H0210), before r6 (view) freezes. The ladder deletes the proposed multi-sheet
memo and names the cutoff number r6 needs. The original claim's count table stands
bit-for-bit; what changes is which of those images a player can see.

## Evidence

All from this folder, on the lab Linux box (each command single-process, ≪ 2 GB):

- `python3 view_images.py` (255 s) → `view_images.json`. The sweep section, the capture
  control, the flat control and the emitter-behind directions are **bit-identical to the
  shipped record** (verified by JSON equality). Only `control_weak_field` changed.
- `python3 ladder.py` (299 s) → `ladder.json` — the checker's named experiment, the
  visibility ladder. Same `trace()` instrument; images of (r_e, φ_e) = crossings of Φ(ψ)
  at levels φ_e+2πk (same side) and 2π−φ_e+2πk (mirror side); μ = |dψ/dφ_e| = 1/|Φ'(ψ)|;
  rel = μ/μ_brightest(φ_e). Probe 32768 rays (the shipped sweep) + log-spaced low-ψ
  extension + corridor zoom 131072; 360 uniform emitter azimuths + geometric refinement to
  ε=10⁻⁴ from alignment. `python3 diag.py` (4 s) unchanged.
- `python3 bands.py` (10 s) → `bands.json` (bit-identical to shipped) + `bands_jet.json`
  (the fixed jet probe).

**The repaired weak-field control (the record defect).** The shipped 0.018 does not
regenerate (shipped code: 0.0 — the ray is born below its own escape cut), and 0.018 was
itself doubly artifactual: `total_phi` is step-quantized (0.018 = 6h) and the M=0
comparison ray was launched at b·√(1−2M/r_o) instead of b (contamination 2Mb/r_o² ≈ 4×10⁻⁴).
The v4 control launches both rays at the same b = 200M from r_o = 998M and reads the
instrument's own interpolated outbound crossing of r = 999M: **bend = 0.020304** (h=3e-3),
0.020304 (h=1e-3), R-converged — the Schwarzschild series 4M/b + (15π/4)(M/b)² + (128/3)(M/b)³
= 0.0200299 to **2.1×10⁻⁴ relative**. Plain 4M/b is off by +1.52% at b=200M: that is the
real 2PN term, not error. The control now passes and is stronger than the original design.

**The ladder (the named experiment).** Static emitters, threshold 1/50:

| r_o | partner (mirror k=0) med rel | p90 | >1/50 | >1/10 | >1/3 | band (>1/50), φ_e | max rel any k≥1 | visible ≥2 @1/50 |
|---|---|---|---|---|---|---|---|---|
| 100M | 0.0137 | 0.250 | 0.433 | 0.194 | 0.078 | [1.78, π] | 0.00076 | 0.433 |
| 10M | 0.058 | 0.519 | 0.703 | 0.394 | 0.175 | [0.94, π] | 0.0039 | 0.703 |
| 5M | 0.070 | 0.551 | 0.778 | 0.425 | 0.192 | [0.71, π] | 0.0084 | 0.778 |
| 3.5M | 0.078 | 0.569 | 0.825 | 0.447 | 0.203 | [0.56, π] | 0.0106 | 0.825 |
| 3.2M | 0.080 | 0.573 | 0.839 | 0.453 | 0.206 | [0.52, π] | 0.0111 | 0.839 |

- The direct image (same k=0) exists for every emitter at every radius and is always the
  brightest (median μ_abs 0.49–0.78).
- The **partner** exists for every emitter everywhere, is visible (>1/50) on a behind-band
  covering 43%→84% of azimuths as r_o goes 100M→3.2M, and merges to equal brightness at
  alignment (rel → 1.0 at ε=10⁻⁴; the Einstein-ring pair) — the band edge moves from
  φ_e=1.78 rad (100M) to 0.52 rad (3.2M).
- **No winding image (k ≥ 1) is above 1/50 at any radius, for any emitter**: medians
  4×10⁻⁴ (100M) to 3.5×10⁻³ (3.2M), max 0.0111; visible multiplicity ≥3 is 0.0% everywhere
  at 1/50. Per-winding decay μ_{k+1}/μ_k ≈ 0.0018–0.0023 for k≥1 — essentially e^{−2π} —
  at every radius (k0→k1: 0.0004 at 100M rising to 0.0035 at 3.2M). The tail the original
  run unbounded is real as a count and invisible as a display, with 1.8× margin at 1/50
  (max 0.0111 vs 0.02); a cutoff at 1/100 would need the k=1 sheet at r_o ≤ 3.5M.

**Validation (all in ladder.json).** Aligned r_o=10 emitter: images at ψ = 141.111° and
152.289° (checker's independent RK4: 141.11°, 152.29°); rel(k=1) = 0.001392 vs the checker's
1/740 = 0.001351. The checker's absolute values (12.13, 0.0164) are exactly mine × 57.2958
= 180/π — their probe mixed degrees and radians; ratios were unaffected. Flat M=0: μ
matches the closed-form projection to 0.084%. Flanking-ray shots vs curve secants: max
0.08% (14 checks, μ ≥ 10⁻⁴; below that the flank Φ-difference drowns in integration noise —
the v1 outliers were k=2 windings at μ≈10⁻⁵). Crossing counts match the shipped
multiplicity() counter exactly (max diff 0).

**The jet probe (the checker's third finding).** The "complex root" was the coding slip
(x = 1/L, wrong root). Fixed (x = 1/L², root nearest 1/p, adaptive hL): all four
p−p_sep ∈ {1.0, 0.5, 0.2, 0.1} at e = 0.9 stay bound, and the jet is real:
|dΔφ/dL| grows **35.8×** and |dΔφ/dp| grows **11.2×** from p−p_sep = 1.0 to 0.1. The
original prediction D splits cleanly: the derivative blow-up holds; the model-error part
still fails (m16 stays ≤ 0.53%, bands.json unchanged).

**Instrument history of this run** (recorded in the code): ladder v1 lacked a low-ψ ray
extension, so at r_o ≤ 3.5M the near-radial direct images fell below the shipped grid's
ψ=0.02 floor and faked a k=1 "visibility band" on 0.5% of azimuths (diagnosed: the direct
image's crossing exists at ψ < 0.02); v2 adds the log-spaced extension (0.003–0.02, h=10⁻⁴)
and the band disappears (same_k1 max rel 0.96 → 0.011). Numbers above are v2 only.

## Predictions (`predictions.md`, written before the runs)

- **Held:** V1 (positions exact; aligned ratio 718× ≈ the checker's 740× — and the
  validation exposed their deg/rad factor), V2 (0.08%), L1 (brightest is always k=0),
  L2 mostly (100M partner band 43%, inside the predicted 15–50%; same_k1 median 3.8×10⁻⁴,
  just under the predicted range), J1–J3 (jet: all bound, 35.8× and 11.2×, inside 20–40
  and 8–12).
- **Missed, all in one direction — winding visibility overestimated 10–100×:** L3–L5
  (k=1 medians 0.0022–0.0035 vs predicted 0.005–0.6; visible bands 0% vs 5–50%;
  ≥3 visible at 3.2M: 0% vs ≥80%) and L7 (K=0 at every radius at 1/50, not 0/1/2/3).
  Root cause, found by the flat-projection validation: I anchored the pre-registration on
  the checker's "~60× demagnified versus a typical off-axis primary", which was itself the
  57.3 = 180/π unit artifact; the true typical demagnification of the first winding is
  ~450× (10M). Every winding-visibility prediction inherited the bad anchor.
- L6 partial: the decay sits at the small end (≈ e^{−2π}), with no clear r_o trend for
  k≥1 (0.0018–0.0023 flat); only k0→k1 grows toward 3.2M.

## What would make it wrong

The ladder is static emitters and observer: motion shifts magnifications continuously
(aberration, B16), moving band edges, not the two-image structure near a mass. The
conclusion is threshold-dependent by construction: 1/50 is a 50×-squeezed sprite — if the
game draws icons rather than sprites, the threshold drops, and below 1/100 the k=1 sheet
enters at r_o ≤ 3.5M (max rel 0.0111, measured). It would be irrelevant only if no
compact mass is ever on screen with emitters behind it — but black holes are in the goal
(B19) and the partner band covers 43% of azimuths already at 100M. The count-level claims
(≥3 images for 100% of positions, unbounded with resolution) are reproduced bit-for-bit
and stand.

## Cost of adoption, and fit with PRINCIPLES

The gather enumerates the k=0 pair (2 crossings per emitter, both expressible by the
existing single-valued deflection(b) — the partner is a moderately bent k=0 ray on the
other sky half) plus a magnification test μ_rel > cutoff; the memo stays single-sheet per
impact parameter. This is cheaper than the original proposal (2 crossings, not 2–4
winding-indexed ones) and deletes the multi-sheet memo. r6 can now freeze: (i) multiplicity
2 on the behind-band with the measured fractions vs r_o (0.43→0.84); (ii) branch continuity
through the Einstein ring (the pair merges, rel → 1.0); (iii) the magnification cutoff,
with the k≥1 tail bounded at 0.0111 max (1.8× margin at 1/50). Fit: principle 28, "The view
is an instrument. 'real vs displayed is not the same thing'" — the winding images are real
for the count and invisible for the display, and the cutoff is the instrument's choice, not
physics'; principle 34, "the oracles are guards, not shepherds" — the count oracle guarded
the invariant, and the ladder keeps the representation from chasing an invisible tail;
principle 1, "the cheapest compute is compute not done" — the fix deletes work the original
verdict would have added.

## The lens

A second-author lens inherits the first checker's numbers as anchors; one of them (the
~60×) carried the checker's own unit slip, and my pre-registered winding magnitudes
inherited it — caught only because the flat-projection validation pinned the absolute
scale. What this lens may still have missed: the moving-lens interaction (aberration × the
partner band), the emitter's own angular extent (a sprite spanning a fold smears the ring
pair; magnification of an extended source was not measured), and the gather's added cost
per branch — visibility is measured, cost is not (the original author's admitted miss,
still open). The threshold-to-pixel mapping (what 1/50 means at a given sprite size and
screen) is left to the integrator; the ladder supplies the curve, not the budget.
