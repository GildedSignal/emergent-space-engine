Grade: gold

**Abstract (for the integrator).** Claim: when concentrated packets cross, real contacts are
Θ(n_A·n_B) — p_pair ≈ 0.021 flat from n=50 to my n=1600 — so at 10⁶ ships/fleet pairwise exact
processing faces ~2.1×10¹⁰ real events and no discovery certificate can help: the events are the
workload, and "flat work per encounter" is the wrong invariant. The escape is measured and works:
per-ship flux λ_i = ρ·2R·L_i through the opposing packet's measured density grid (co-rotating
frame, O(n), zero parameters), ratios 0.87–1.04 on all scenes, held-out geometry in-window
0.95–1.01. Reproduced bit-for-bit. My attacks: fresh seeds to n=1600 (ratio ≤1.04), steeper
e=0.8 crossing (0.99), ρ=1e-4 (0.98) — all pass. One boundary found: a ~300:1-aspect packet
fails (0.52, frozen-grid shear); the μ-trigger needs a compactness condition. Cost: one tier in
the encounters design, no engine change.

**Reasons.**

1. **Reproduction, exact.** Clean tree, empty patch.diff (no repo edits — everything in the run
   folder), `diff -r` confirms the lib is verbatim `crates/encounters` with only `bulk.rs` added.
   All four commands rerun: every physics number in `bulk.jsonl`/`analysis.txt` matches the
   author's output exactly (12 scenes; exponent 1.935; τ-slope 0.02078; w-factor 7.98; in-window
   1.009/0.948; belt 0.42417/ship/orbit). Only wall times and load differ. The arithmetic checks:
   0.0208×10⁶ = 20,777 ≈ 21k/ship; 0.021×10¹² = 2.1×10¹⁰.

2. **The truth is sound and independent.** `radial_pairs` keeps every pair with
   `rmin_j ≤ rmax_i + 2ρ` — provably complete for contacts (< ρ). The conservative-advancement
   bound can't step over a sub-ρ dip (coarse steps only when a rigorous lower bound proves
   d ≥ 1.5ρ; fine mode inside 2ρ; dips bracketed by r·v sign change, Newton-refined; Halley
   states vs the aggregate's plain states — no shared solver path).

3. **Predictions were frozen first and mostly held.** `predictions.md` (12:43) predates the
   sweeps (`bulk.jsonl` 12:53); kill criteria pre-registered. P1 held (1.935 ∈ [1.9, 2.1]; flat
   p_pair), P2 held (2.1×10¹⁰ ≥ 10⁹), P4 held (8.0, band edge, direction pre-committed), P5 held
   (0.87–1.04; held-out in-window 0.95–1.01; no fudge factor), P6 held and refined (var/mean up
   to 91, corr 0.83–0.99; saturation to 0.90 at μ≈72 correctly described). P3 missed (belt 0.42
   vs <0.05, K3 triggered as written) — reported as a miss, diagnosed (thin dense belt is mildly
   collisional, same order as r8 v2's 1.1), and converted into the run's real lesson: per-event
   multiplicity μ separates the regimes, not per-orbit rate. That miss produced the invariant,
   which is the adoptable part.

4. **Adversarial cases (mine, fresh seeds S0+211…216, machine load 0.8–2.1, 4 threads, well
   under 2 GB).**
   - *Fresh seeds, n = 100/400/800/1600 (2× the author's max):* exponent 2.172 (stepwise 2.38,
     1.88, 2.05 — inside the author's disclosed swing 1.62–2.51), p_pair 0.015–0.026, aggregate
     ratios 0.994–1.039, corr 0.97–0.99, agg cost 257·(n_A+n_B) confirmed at n=1600 (822,400
     evals vs 2.56M cross pairs; truth 45.9 s). The quadratic law and the escape both hold
     beyond the measured range.
   - *Steeper crossing (a=2.0, e=0.8, ν=1.93 rad — past the author's held-out e=0.6):* ratio
     0.990, corr 0.79. Holds.
   - *Contact radius ρ=1e-4 (10× smaller):* truth 205 ≈ 1976/10 and pred 201, ratio 0.979 — the
     flux's linear-in-R scaling is confirmed against the truth; "zero free parameters" survives
     a 10× parameter change.
   - *Extended packet (B m0-jitter 0.3 rad, aspect ~300:1, μ≈8):* **ratio 0.518** — the
     aggregate undercounts 2×. Same signature as the author's disclosed instrument note (frozen
     grid vs rotation), here from internal shear: the static density grid measured at t* cannot
     follow a long packet's differential rotation over the ±0.5-orbit window. Still inside the
     pre-registered ×[0.5,2] band (barely), but the μ-trigger as written in the dossier would
     route this case to the aggregate and be 2× wrong. **Adoption amendment, one line:** the
     trigger needs a compactness condition (measured: aspect ≲50:1 fine, 300:1 fails), computable
     from the same packet summaries (extent, area) the design already holds.

5. **Novelty.** No HISTORY entry, doc or board item prices bulk-crossing contact counts or
   validates a contact-flux aggregate. taleb-3ebf measured the interception and punted on
   exactly this regime (per the dossier; its branch is not in this checkout, so the b2-300 "tie
   to its numbers" is unverifiable here). taleb-09b5's gold is the co-orbital *candidate* tier —
   a different failure (within-formation discovery), and this run's premise correction (the
   certificates' "flat work per encounter" invariant is the wrong one when the events themselves
   are Θ(n²)) answers the board's top scaling risk for the crossing regime. The flux/optical-
   depth mechanism is prior art from transport physics, cited as such per principle #26 —
   correct use of "steal what works". archive/engine.md's "one surprise rate per region,
   computed from its macrostate (density, relative speeds)" is the same shape, but was never
   built or validated against a truth; this run grounds it.

6. **Goal fit.** Directly on the board's top scaling risk and the adopted taleb-09b5 risk;
   deletes pair enumeration for the game's central extreme event. PRINCIPLES: #3 "Compute only
   surprises" — a bulk crossing is one surprise, not 2×10¹⁰; #33 the ant/lion dial is exactly μ;
   #6 aggregates become the source. The regime-number framing (μ ≪ 1 pairwise, μ ≳ 1 fluid,
   saturation var/mean < 1 at μ≈72) is a dimensionless trigger, not a category (#4).

**What the author missed.**

- The packet-*extent* axis: the w-series swept the sweeping fleet's width, never the swept
  fleet's; my wb-400 shows the frozen grid fails under shear at high aspect (0.518). The
  dossier flags "extreme aspect ratios untested" but the tier's trigger text omits the needed
  compactness condition.
- "It also covers the within-fleet quadratic" overstates: within-fleet contacts are *priced*
  (126,959 at x-800, ~n², 9.4× the cross count; ~2×10¹¹ at 10⁶/fleet — the larger ruin) but no
  aggregate predicts them in this run; nothing here owns that tier. The co-moving formation is
  a different flux problem (near-parallel, drift-speed tubes) and is untested.
- predictions.md P5 names the held-out geometry a=1.5, e=0.4; the run used a=2.0, e=0.6
  (harder — no convenience, but the pre-registration text and the run differ; disclose such
  changes).
- The dip-vs-pair distinction: the truth counts distance minima, the flux counts pairs entering
  the tube; a pair dipping twice in-window would count once in the prediction. Immaterial at
  these ratios (single crossings), but worth one line in the tier spec.
- Identity resolution at μ ≫ 1 (who dies) is untested — the author says so; the λ-weighted
  sampling is the adopter's next probe, and the allocator/spike consequence the author raised
  (one crossing = one O(n) synchronized spike; board bottleneck 4) is real and unowned.

Machine state: shared 8-vCPU Linux runner, load 0.79–2.14 across my runs, ≤4 threads, peak
scene n=3200 bodies (s-1600) well under the 2 GB cap. All numbers regenerable:
`cd /tmp/check2 && cargo build --release --bin bulk && ./target/release/bulk adv` (adversarial
scenes s/e/wb/r; RHO env var threads the contact radius).
