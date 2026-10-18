# Dossier — 20261018-2040-system-cc75 (system lens)

**Claim.** The view's per-frame `seen` stream — the ladder's first N-growing per-body term on
current main (dcf1: 5.0 µs/seen body, linear) — is a no-op machine at the observer above
K ≈ 3×10³: the sky (a circle in this 2-D universe) is measured FULL at the 800-pixel floor
from K = 10⁴ up (786 = 2π/8×10⁻³ cells occupied, alone-in-cell fraction 0.0001 at 10⁴, 0.0000
at 10⁵, 12–127 rows per pixel) and full at the 1-pixel ratchet floor at 10⁵ (6,284 = 2π/10⁻³
cells), while the resolvable content — the near set — stays ~3.5×10² rows, flat in K,
alone-in-cell 1.000 at every rung; so the gather, the scan and the kick boundary are three
faces of one threshold (the observer's resolution) and one cure (the window-membership record
over the cold crowd that scan-locality already built), not three problems.

**Bottleneck.** The board's first live question (bodies: 28 flown toward 10⁹) and dcf1's
finding that on current main the view gather is the ladder's first N-growing term. This run
does not speed the engine; it kills the premise of the per-row stream at scale, which sizes
what the 10⁶-10⁹ gather must be (O(window) rows + O(sky cells) aggregates, not O(N) rows), and
it unifies that requirement with the scan's already-flown record (687c) — a component
deletion at wiring time, priced below.

**Evidence** (all from the shipped binary `xtask universe --bench`, seed 1, coast, rtf 100,
unpaced, frames 30 and 90; patch = `work/patch.diff`: an `ES_LADDER` scene knob calling the
shipped `plane_extra`, plus a print-only census of the wire's own `seen` array — angles from
the serialised `direction`, split far/near at light-seconds 100; no engine state is touched,
the digest is the shipped one; ~4 min total, `regen.sh`):

| K | far rows | sky cells @8×10⁻³ (cap 785.4) | alone @8×10⁻³ | alone @10⁻³ | alone @10⁻⁴ | rows/px @8×10⁻³ | near rows (alone @10⁻⁴) | wire B/row |
|---|---|---|---|---|---|---|---|---|
| 0 | 18 | 15 | 0.78 | 0.78 | 0.89 | 0.07 | 58 (0.93–1.00) | 284 |
| 10³ | 718 | 471 | 0.42 | 0.87 | 0.99 | 0.91 | 358 (1.00) | 272 |
| 10⁴ | 9,718 | **786 = FULL** | **0.0001** | 0.20 | 0.84 | 12.4 | 358 (1.00) | 270 |
| 10⁵ | 99,718 | 786 = FULL | 0.0000 | **0.0000 (6,284 = FULL at 10⁻³)** | 0.20 | 127 | 358 (1.00) | 270 |
| 3×10⁵ | (regen; the flight ran past this window's write deadline — same law, occupancy ~381/px) | | | | | | | |

- NN angle p50 among far rows: 5.8×10⁻³ → 4.1×10⁻⁴ → 4.1×10⁻⁵ rad (∝1/K, the uniform-angle
  law); frame 90 identical to frame 30 to three digits (the census is stable in flight time).
- Wire: 26.96 MB serialised per frame at 10⁵ (1.62 GB/s at 60 Hz) for ≤ ~6.6×10³
  distinguishable sky places at the ratchet floor (6,284) + 358 near rows. At 10⁶ the same
  law pays ~284 MB/frame for the same ~6.6×10³ places (occupancy ~1.6×10³ rows/px).
- seen = K + 76 rows at every rung (dcf1's law confirmed on this instrument); bench reports
  with the view_gather/view_json/wire shares per rung are in `work/bench*.json` (10⁴: gather
  90%+ of frame, the 62c1 law reproduced).
- Controls, both sides: K = 0 (the shipped plane): sky sparse (15/18 cells, alone 0.78) —
  the row stream is legitimate exactly where it was born (28 bodies + crowd); the near set is
  sparse and flat at every rung (alone 1.000 @10⁻⁴) — the deletion's residue is the
  instrument's real content, and it is O(10²).

**Predictions** (`predictions.md`, written before the flights): P1 held (seen = K+76); P2 held
with margin (predicted alone < 5% at 10⁴, measured 0.01%; predicted cells saturate ≈ 6–8×10²,
measured 786 = 2π/θ_f exactly); P3 held (near set flat, alone ≥ 95% — measured 100% at 10⁻⁴);
P5 held (284 B/row, 27 MB/frame at 10⁵); P4's timing half is in `work/bench*.json` (linear
gather), not re-claimed as a headline (dcf1's instrument is better). No kill criterion fired.

**What would make it wrong.** (1) A display standard that resolves rows below θ_f = 10⁻³ on
the sky (none exists: an 800-px band gives 8×10⁻³; a full-circle 1-px ratchet is 10⁻³ and
already full at 10⁵). (2) The sub-pixel crowd's aggregate signals (brightness = count,
colour/shift spread) needing per-row precision the aggregate cannot carry — unmeasured here.
(3) Zoom: belt-zoom puts ~N rows on-canvas (62c1's checker); the record must re-window and
ee30 measured the drain at 95 s at 10⁹ — the deletion is a fitted-zoom statement plus a
bounded re-window, not a blanket one. (4) Formations: a standing crowd (taleb-09b5's class)
concentrates rather than uniform-fills; the cell census there is the next probe (the
uniform-angle law predicts capacity at even lower K — concentration only fills cells sooner).

**Cost of adopting.** Small and already half-paid: 2df1's row-set deletion is built and
display-exact; 687c's window-membership record is built for the scan; the adoption is to serve
the view's far rows from the same record (one range query per frame per open floor) and emit
per-cell aggregates (count + colour/shift spread) below the floor — deleting the O(N) crossing
walk (e401: 0.95 of the gather) and the O(N) wire at fitted zoom for every crowd that is cold
(649c: far rows bit-reproducible between tube time quanta). The hot-set trigger (a kicked or
separating body re-enters the resolvable tier) rides the kick stream, whose rate is measured
(cd3b: ~0.22 contacts/game-s at 10⁹; the burn mint rate is 2403's).

**Fit with PRINCIPLES.** #3 "Nothing is evolved that can be derived when looked at (clocks,
redshift, views)" — the far row at the tick is derived, and below resolvability it is not even
looked at; #24 "The memory floor is information … the floor is what the player can
differentiate" (bottleneck 5; Julien's early-cinema line) — the seen stream's information
floor is 2π/θ_f cells + the near set, ~10³ places, flat in N; #33 "a raindrop is an event for
an ant and nothing for a lion" — the belt below one sky pixel is the raindrop; #1 the
cheapest compute is the row not serialised. #28 "the view is an instrument … real vs
displayed is not the same thing."

**The lens.** What it may have made me miss: the whole-system eye looks for one structure and
will find one; the three no-op machines share a *threshold*, but their *costs* are different
currencies (CPU for the gather, bytes for the scan, cadence for the comb), and e401 already
corrected one over-unification on this exact page ("they share the census walk, nothing
more"). My unification is at the record level, not the lever level, and its hardest case is
the formation (a crowd that is all hot set): there the record degenerates to the phase-word
tier e401 bounded at 13×, and taleb-09b5 killed the pairwise tier outright — the
one-structure sentence must not be read as "one lever". Also: one seed, one scene (the
ladder's uniform belt), coast only; the burn's mint stream changes the hot set's rate, not
its size class.

## Files

- `work/patch.diff` — the whole edit (print-only; `git apply` then `regen.sh`).
- `analyze.py` → `metrics.json`; `work/seen*.txt` (the census lines), `work/bench*.json`
  (the shipped bench reports, digests included).
- `wiki/view.md` — the page with this result folded in.
