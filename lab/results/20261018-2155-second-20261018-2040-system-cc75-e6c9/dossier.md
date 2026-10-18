# Dossier — 20261018-2155-second-20261018-2040-system-cc75-e6c9 (second author on 20261018-2040-system-cc75)

**Claim.** The checker's named experiment is flown and holds: the view's far rows served from a
window-membership record over the sky circle (near tier + fleet + star walked fresh; far bodies
revisited only at their predicted cell crossings; one aggregate per multi-member cell) delete the
O(K) gather walk and the O(K) wire at fitted zoom on cc75's own scene — readouts ~351–374/frame
flat in K from 10³ to 3×10⁵, serving path 177×/198× below the oracle gather and wire 89×/268×
below the full stream at 10⁵/3×10⁵, the per-frame audit against the oracle's own rows clean
(wrong-cell/missing/tier errors 0; fresh rows bit-identical; singleton drift ≤ 4.3×10⁻⁵ rad ≪
θ_f; per-cell Σlum error p50 ≤ 1.1×10⁻⁵), and the engine digest unchanged in flight, in control
and against the unpatched bench.

**Bottleneck.** The board's first live question (bodies 28 → 10⁹) via dcf1's finding that the view
gather is the ladder's first N-growing per-body term. cc75 certified the *content* (the sky FULL at
786 = 2π/8×10⁻³ cells from K = 10⁴; near set ~358 flat) and designed the cure but did not fly it —
the checker held the run at silver for exactly that. This run flies the deletion: the gather's
per-frame readout count stops growing at ~360 (the near window + a handful of due events), so the
10⁶–10⁹ view costs O(window) + O(2π/θ_f) rows on the wire, not O(N).

**Evidence** (all from the shipped scene builder `plane_extra` (cc75's `ES_LADDER` ladder), coast,
seed 1 [seed 7 at 10⁴], rtf 100, the shipped `gather_cached` as oracle beside the additive server
`view::sky_server` (patch = `work/patch.diff`: additive code in view.rs + a driver; no shipped line
semantically touched); ~12 min total, `regen.sh` → `metrics.json`):

| K | readouts/frame (near+fleet+star+due) | cells @8×10⁻³ | served rows | wire full → served | oracle gather p50 | serving p50 (near+due+serve) | fall |
|---|---|---|---|---|---|---|---|
| 10³ | 351 | 470 | 823 | 290 KB → 221 KB (1.3×) | 20 ms | 2.9 ms | 7× |
| 10⁴ | 359 | **786 = FULL** | 1,143 | 2.72 MB → 302 KB (9.0×) | 232 ms | 3.7 ms | 62× |
| 10⁵ | 361 | 786 | 1,145 | 27.0 MB → 302 KB (**89×**) | 2,383 ms | 13.4 ms | **177×** |
| 3×10⁵ | 365 | 786 | 1,145 | 80.8 MB → 302 KB (**268×**) | 7,078 ms | 35.8 ms | **198×** |

- **The ratchet floor (θ_f = 10⁻³) holds too:** 6,284 = 2π/10⁻³ cells FULL, served 6,643 rows
  (15.7× wire fall), due rate 1.9/frame, wrong_cell ≤ 1 of 99,717 far rows (0.001%), one cell's
  Σlum off by 5.3×10⁻² at worst (the stale-lum residue of a crossing at the finer floor).
- **The churn law (the record's maintenance), measured:** the cold pass measures every far body's
  angular rate by one finite difference; the resulting next-crossing horizon distribution is
  K-independent (p50 ≈ 6.9–7.1×10⁴ frames at every rung; p10 ≈ 1.3×10⁴; mean 1.6×10⁵→2.2×10⁶),
  pricing steady due events at 0.005 / 0.031 / 0.18 / 0.14 per frame at 10³/10⁴/10⁵/3×10⁵ —
  observed due p50 0–2 per frame, each a single `crossing` readout. The record held one fast body
  (hz_min 3–18 frames) sound across the whole flight: it pops, crosses (churn), reschedules.
- **Display exactness, audited per frame against the oracle's own rows:** wrong_cell =
  cells_wrong = missing = extra = tier_err = 0 at 10³–10⁵ at both floors and at seed 7 (the one
  10⁵ ratchet-frame exception above); the fresh near/fleet rows bit-identical to the oracle's
  (near_dmax = near_dls = near_dshift = 0.000e0 — the crossing is start-independent, as the view's
  own doc claims); singleton stored-row angular drift ≤ 4.3×10⁻⁵ rad over 90 frames (θ_f = 8×10⁻³);
  per-cell Σ luminosity rel error p50 ≤ 1.1×10⁻⁵, max 2.7×10⁻⁵ at the 800-px floor.
- **Completeness, the hole the shakedown found and closed:** handed-out fleet members become
  bodies mid-flight (fleet 48→37 over 12 frames at 10³); the server now walks them fresh from the
  `n_bodies()` growth event (the handout is the trigger), and the audit counts any unserved oracle
  near row (tier_err = 0 everywhere).
- **The digest, three ways:** identical before/after the server ran at every probed frame (every
  10th, all rungs); the serve arms' end digests equal the control arms' (same seed, frames,
  budget, no server) at 10⁴/10⁵/3×10⁵; and the shipped bench on the patched tree digests
  `1b801358…` — equal to cc75's unpatched bench0. The server is read-only, as `gather` is.
- **Honest residues, measured not hidden:** (1) the serve loop rebuilds cell aggregates from
  members each frame — the one O(K)-shaped term left (10.7 ms of the 13.4 at 10⁵, ~100 ns/member
  row-adds; 33 ms at 3×10⁵) — deletable to O(cells) by running sums maintained on the same due
  events, no new mechanism; (2) the cold start is one walk (frame 2's ω pass, due = K once); (3)
  the K = 10³ rung is the honest control: wire fall 1.3× — below saturation the stream *is*
  information, exactly where cc75 said the row tier is legitimate.

**Predictions** (`predictions.md`, written before the decisive flights; tuned only on ≤ 14 frames
at 10³/10⁴): P1 held with the serving-path reading (177× ≥ 100× at 10⁵, 198× at 3×10⁵; the
coarser total_ms including my audit walk gives 46× — the audit is instrumentation, reported
separately); P2 held (readouts 351–374 flat, due p50 0–2, horizons K-independent); P3 held (wire
falls 9.0×/89×/268×, ratchet 15.7× ≈ the predicted ~15×, served ~302 KB flat); P4 held (audits
zero, px_max ≤ 4.3×10⁻⁵ ≤ 10⁻⁵? — no: 4.3×10⁻⁵ against a predicted ≤ 10⁻⁵, a 4× miss on a
constant 200× under the floor, reported as a miss); P5 held exactly (all three digest checks);
P6 held (seed 7: 786 FULL, audits zero, 9.1×). No kill criterion fired: K1 wrong_cell max 0 (one
frame of 1 at the ratchet floor, 0.001%); K2 due ≪ K/1000; K3 serving 13 ms ≪ 120 ms; K4 zero;
K5 zero. One instrument bug was found and fixed *before* the decisive flights (the due loop
dropped the reschedule; the audit caught it as monotone wrong_cell growth at 10⁴ — the fixed
build reschedules and the growth vanished).

**What would make it wrong.** (1) A formation crowd (taleb-09b5's class): a standing crowd is all
hot set — the record degenerates to walking it (unflown; the ruin class cc75 and e401 both name).
(2) Zoom: belt-zoom re-instantiates rows at the finer floor (the 10⁻³ arm shows the shape: 6,284
cells, 8× the churn, 15.7× not 89×); the re-window drain is ee30's 95 s at 10⁹. (3) The hot-set
trigger: a kicked body must re-enter the resolvable tier at the kick that makes it hot — coast
only here; the trigger is the kick stream (cd3b). (4) The aggregate's patina is carried as sums
(count, Σlum, lum-weighted colour/shift); a display that resolves intra-cell colour variance
would need the spread term (measured residue: the 5.3×10⁻² worst cell at the ratchet floor).
(5) Flights ≤ 120 frames: mass crossings are priced by the measured horizon law, not observed
en masse.

**Cost of adopting.** The mechanism is additive to the view (one record per observer per open
floor; ~530 lines in view.rs incl. the audit probe, of which the serving path is ~150); the cold
start is one walk; the fleet/star/near walk is the shipped row math factored for one body. What
still must be built for the engine: running cell sums (deletes the O(K) aggregate rebuild), the
hot-set trigger on the kick stream, and the zoom re-window. It composes with 2df1's display-side
row-set deletion (same tier structure, wire side) and with 687c's scan-side record (one record
class, two windows — the scan half is the remaining unification).

**Fit with PRINCIPLES.** #3 "Nothing is evolved that can be derived when looked at (clocks,
redshift, views)" — the far row at the tick is derived on demand from membership + the cell's
aggregate, and the membership itself moves only at crossing events; #1 the cheapest compute is
the row not walked (K walks → ~360 + due); #24 the floor is what the player can differentiate —
θ_f is that floor and the record's cost is 2π/θ_f; #33 the raindrop and the lion — the belt below
one sky pixel is the raindrop, entering as an aggregate; #13 errors never compound — the record
self-heals at each due event and the audit shows zero drift at the floor.

**The lens.** The second-author lens repairs the record, not the claim: I may have under-weighted
what the flight says about *costs in different currencies* — the walk fell 177× but the wire's
89× is the player-facing number on this box, and the aggregate rebuild is the term that will bite
at 10⁶ if left naive (100 ns × 10⁶ = 0.1 s/frame). Also one scene class (the uniform ladder
belt); the formation remains the shared ruin class of this whole line, and my run does not touch
it. And the audit oracle is the shipped gather itself — agreement between server and oracle is
not independence of the row math (both use `crossing`); the digest checks are the independent
half.

## Files

- `work/patch.diff` — the whole edit (additive: the server in view.rs, the skyserv driver, one
  dispatch arm; the shipped bench digests identically).
- `analyze.py` → `metrics.json`; `work/serve*.log` (the flights, one SKYSERV line per frame),
  `work/ctl*.log` (the no-server controls), `work/bench0.json` + `work/orig_bench0.json` (the
  digest-neutrality cross-check).
- `wiki/view.md` — the page with this result folded in.
