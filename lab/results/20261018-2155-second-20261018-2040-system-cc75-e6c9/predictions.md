# Predictions (written before the decisive flights)

The checker's named experiment, flown: cc75's claim said the far `seen` stream is a no-op machine
above K ≈ 3×10³ (the sky FULL at 786 = 2π/8×10⁻³ cells; near set ~358 flat). Gold needs the
deletion flown: the far rows served from a window-membership record at fitted zoom, wire and gather
falling from O(K) to O(2π/θ_f) + O(window), digest unchanged. This run builds that server
(`view::sky_server`: near tier + fleet + star walked fresh; far tier one record entry per body,
revisited at margin 0.5 × its predicted next cell crossing; one aggregate per multi-member cell,
exact row per singleton) and flies it beside the shipped oracle gather on the same scene as cc75
(`plane_extra`, seed 1, rtf 100, coast).

Tuned on (shakedown only): K = 10³ and 10⁴, ≤ 14 and ≤ 8 frames, seed 1, floor 8×10⁻³. Everything
below is held out: the long flights, K = 10⁵ and 3×10⁵, seed 7, floor 10⁻³, the control arms, the
horizon law at K > 10³.

- **P1 (the walk).** The server's own per-frame cost stays ≤ 10 ms at every rung (near walk
  ~2.5 ms for ~310–330 bodies + fleet ~40 + star, serve loop over ≤ 786 cells, due ≈ 0), while the
  oracle gather grows ~linearly in K (~230 ms at 10⁴ on this box): the deletion is ≥ 20× at 10⁴,
  ≥ 100× at 10⁵, ≥ 300× at 3×10⁵.
- **P2 (the readout count and the churn law).** Readouts per frame = near + fleet + star + due ≈
  350–380, flat in K. Due events: 0 observed in every flown window (≤ 120 frames), with the
  measured horizon distribution pricing the steady state at K/E[horizon] ≈ 0.005/frame at 10³
  (measured in shakedown: p50 7.1×10⁴ frames) and ≤ 5/frame at 3×10⁵ (E[horizon] roughly flat in
  K — the belt's angular rates do not depend on how many ships ride it).
- **P3 (the wire).** Served bytes per frame ≈ 3.0–3.3×10⁵ B flat in K at floor 8×10⁻³
  (~786 cell rows + ~360 fresh rows ≈ 1,145 rows at 10⁴, held to 10⁵ and 3×10⁵), against the full
  stream's linear growth (2.7 MB at 10⁴ → 27 MB at 10⁵ → ~81 MB at 3×10⁵): a wire fall of ~9× at
  10⁴, ~90× at 10⁵, ~270× at 3×10⁵. At floor 10⁻³ (the ratchet): served ≈ 6,284 + 360 rows ≈
  1.8–2.0 MB at 10⁵, a ~15× fall — the zoom tax is the cell count, one arm of 8×.
- **P4 (display exactness, at the instrument).** wrong_cell = cells_wrong = missing = extra =
  tier_err = 0 at every rung, floor and seed; px_max (singleton stored direction vs the oracle's)
  ≤ 10⁻⁵ rad ≪ θ_f = 8×10⁻³; per-cell Σ luminosity rel error p50 ≤ 10⁻⁵, max ≤ 10⁻³; the fresh
  near/fleet rows bit-identical to the oracle's (near_dmax = near_dls = near_dshift = 0).
- **P5 (the digest).** The engine digest, taken before and after the server ran, is identical at
  every probed frame (every 10th); the end digest of each serve arm equals its control arm (same
  seed, frames, budget, no server); the shipped bench digest on this patched tree equals the
  original run's unpatched bench digest (the patch adds code, touches no shipped path).
- **P6 (seed 7).** The same laws hold at 10⁴ (cells 786 FULL, audits zero, costs flat).

Kill criteria (any firing kills the "flown deletion" claim as stated):

- K1: wrong_cell > 1% of far rows at any rung — the first-order ω predictor with margin 0.5 does
  not hold the record sound; the record needs the tube-native crossing time (a real finding, not a
  tuning knob).
- K2: steady due/frame > K/1000 — the maintenance is itself an O(N)-class term (a churn wall).
- K3: server total_ms > oracle_ms/20 at 10⁵ — no deletion worth the adoption.
- K4: missing + tier_err > 0.5% of oracle rows — a completeness hole in the served stream.
- K5: any digest mismatch — the server wrote; the read-only contract is broken.

Blind spots accepted and named: zoom/belt-zoom re-window unflown (ee30's drain prices it); the
hot-set trigger (a kicked body re-entering the resolvable tier) unflown — coast only; the
aggregate's patina carried as sums (count, Σlum, lum-weighted colour/shift), no per-cell variance
on the wire; flights ≤ 120 frames, so cell crossings are priced by the measured horizon
distribution rather than observed en masse; one scene class (the ladder belt), the formation crowd
remains the ruin class cc75 named.
