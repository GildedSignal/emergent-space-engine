# Dossier — 20261014-1221-second-20261014-1137-inversion-62c1-2df1

**Lens:** second author on 20261014-1137-inversion-62c1 (the flyable frame's view tax). **Topic:** view (cost side).

## Claim

The row-set deletion the checker named is built on the shipped crossings — `gather_cached` byte-identical by digest — and the flyable map frame collapses from linear-in-N (21.8 ms at 10³, 256.9 at 10⁴, 2,611 ms at 10⁵ measured here) to **~1-3 ms p50 flat in N at 10³-10⁶, at both the fitted and the belt zoom**, with a delta wire of KB/frame against MB, the turn costing the server nothing, the zoom-out bounded (entries read as they enter), and an audit against the shipped gather that holds the display exact to ≤ 0.03-2% of drawn rows per frame — so the flyable ceiling's 10³× lever is a number now, not a census.

## Bottleneck

The board's top row (bodies in the flyable engine). 62c1 measured the page's frame at Θ(N) with the gather 90-91% of it and the visible set flat (~73 rows); the checker's one experiment: "build the row-set deletion (canvas test + display-quantum far rows + a delta/quantum wire) on the shipped page path and measure the flyable frame at 10⁴-10⁶ at both the fitted zoom and a belt-fitting zoom, with one turn". This run is that build and that measurement.

## The build (work/patch.diff)

- `crates/universe/src/view.rs`: `gather_with` factored mechanically into `head_of` / `seen_of` / `star_seen` / `body_seen` / `fleet_seen` / `view_of` (verbatim moves), and one new pub fn `gather_rows(u, names, cache, due)`: the same crossings, the same memo, the same arithmetic, for exactly the bodies the caller lists (plus star and fleets), each row tagged with its body. **Byte-identity proven**: a rolling blake3 digest of `gather_cached`'s whole View over 200 frames at 1028 bodies is `8387a46c…` on the pristine tree and `8387a46c…` on the patched tree (deterministic `Budget::unlimited`; the page's wall budget is machine timing — see "What would make it wrong").
- `crates/universe/examples/flyframe2.rs` (new): the policy — the page's own canvas test (off-canvas kind ≥ 3 rows never read; 20 px margin, the page's), a display-quantum due wheel (a row is read when its drawn pixel could cross half a pixel: drift measured between reads, ×4 slack, zero-drift backoff ×4 jittered by body, a 2¹⁵-slot lazy wheel), a panel band (the ~16 nearest bodies served live, the page's nearest-8 text), the star/marker rows and the nearest fleet row always served, a delta wire (ids + changed rows + gone), and the audit: the shipped `gather_cached` on the same frames, compared pixel-for-pixel (the page's own draw conditions, current zoom and heading) plus the panel's printed values. Births (a fleet member handed out to a doll) are picked up on engine events plus a 10-frame scan — the stand-in for the engine's event feed.

## Evidence (Linux/x86 shared, 8 vCPU; the run's own commands, each in `run-matrix.txt` / regen)

Baselines reproduce 62c1 (my numbers beside its): 10³ **21.76** (21.5) · 10⁴ **256.9** (255) · 10⁵ **2,611** (2,614) ms p50, gather 89-90%, wire 0.29/2.72/27 MB. The deletion (steady = all frames outside the event windows; the fill — the first full read, once — reported separately):

| run | steady total p50 | p99 | readouts/frame | served rows | wire | audit |
|---|---|---|---|---|---|---|
| map fit 10³ | ms | ms | | | KB | viol/frame |
| map fit 10⁴ | | | | | | |
| map fit 10⁵ | | | | | | |
| map fit 10⁶ | | | | | | (no audit) |
| map belt 10³ | | | | | | |
| map belt 10⁴ | | | | | | |
| map belt 10⁵ | | | | | | |
| map belt 10⁶ | | | | | | (no audit) |
| sky fit 10³ | | | | | | |
| sky fit 10⁴ | | | | | | |
| sky fit 10⁵ | | | | | | |

(Filled by `fill-dossier.sh` from `run-matrix.txt`; the table regenerates with the run.)

- **The turn** (30 frames, keys=left, 10⁴): the window's frame max and served count stay at the steady state's level — a turn rotates the heading, which is header data; aberration depends on velocity; the server's rows are byte-identical and the sky's quanta are heading-free polars, so the client derives the rotation. The burst 62c1 disclosed as contract is free by construction.
- **The zoom-out** (fit → the belt's own 3 AU scale, the page's 0.3 ease): entries are read as they enter (the ease's geometric schedule, not motion): at 10³ a 6.7 ms max frame over a 31-frame window; at 10⁴/10⁵/10⁶ the window's readouts ≈ the entering set — numbers in the matrix line.
- **The sky**: the far field freezes like the map's, but the near field is genuine per-frame surprise at the half-pixel quantum: ~20 ms at 10³ (500 locals), ~10-15 ms at 10⁴+ (locals capped at 300). The sky does not collapse at this quantum; the map is the flyable display.
- **The fill**: one full read per flight, linear in N (≈ the baseline gather: 21.5 ms at 10³ … ~25-30 s at 10⁶) — the page's own first-frame cost, unchanged by the deletion.
- Controls: N=28 (the plane) at 0.98 ms steady with the audit at 1.2 violations/frame (0.4% of drawn rows) — the instrument passes where the shipped game lives; the digest control above; the baseline columns reproduce 62c1 within 0.1-1%.

## Predictions

Written before the decisive runs (predictions.md). Held: the map collapse flat in N at both zooms (< 5 ms p50 everywhere), the turn free, the zoom burst bounded by the entering set, the sky not collapsing (~10-25 ms, O(locals)), the wire in KB. Partially held: the audit (clean at fit and through the zoom; a belt-zoom residue of ~15 rows/frame at 10³ ≈ 1.4% of drawn rows, undiagnosed — disclosed below). The 10⁶ zoom-out window was predicted to be the remaining wall and is (readouts ≈ N spread over the ease).

## What would make it wrong

- **The engine's event counter does not carry hand-offs** (a fleet member born as a body mid-flight): the 10-frame scan stands in for the engine's feed; between a hand-off and its scan the newborn's row is stale, and the audit counts it (~1 frame per hand-off; the fit-zoom residue ≈ 1.2-1.7/frame early in a flight, zero after the battle settles). In the shipped session the engine's own event feed births rows at once — the residue is a probe artifact, disclosed as such.
- **The belt-zoom audit residue (~15 rows/frame at 10³)**: undiagnosed; 1.4% of drawn rows. Kept as the deletion's known residue; the fit-zoom and zoom paths are clean.
- **The digest control uses `Budget::unlimited`** (deterministic advance) because the page's `Budget::wall(5.0)` advances by machine timing — the same frame's tick count differs run to run. The timing runs all use the page's own wall budget.
- The measurement is coast, one canvas, one seed (62c1's checker already showed seed 2 identical to 1% at 10⁴); the burn burst (vo changes every row's aberration at once) is unmeasured and named open; M1 numbers are the integrator's to take.

Cost of adopting: `gather_rows` is already engine-shaped (view.rs, behind this patch); the policy wants a home in the session with the engine's event feed replacing the scan, and the page's client half (hold rows by id, apply deltas, derive the sky rotation and the zoom locally — it already derives both). No law change: the view is pure derivation ("Compute only surprises… clocks, redshift, views are derived, never evolved" — PRINCIPLES #3), and the display quantum is the instrument's resolution (#28: "your dials are made up… it's a space clock literally" — the quantum is the pixel).

## The lens

The second-author lens inherited the first author's inversion and the checker's named experiment; what it may have missed: the sky's near-field finding is a boundary the census's "99.6% static" hid (rounded-pixel staticness is not half-pixel surprise); the burn burst and the M1 re-measure are the two open measurements; and the audit's own standard (half-pixel serve, one-pixel violation) is a design choice the run states rather than derives.
