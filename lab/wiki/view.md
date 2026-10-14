topic: view
status: open
closed-by:
valid-while:
updated: 20261014-1137-inversion-62c1

# The view: the observer's past light cone, lensing, kinked tubes

## Current best

**The flyable frame is the view's, and the view's Θ(N) row set is a far-row tax: 93–99.9% of its rows buy zero pixels in map mode on the ladder scenes, so the flyable ceiling is ~10³ bodies, not the gate's 10⁶ — the deletion lever is the row set (off-canvas in map mode, display-static in sky mode), not the row's µs (20261014-1137-inversion-62c1).** Gate N1 (merged 14 October) certified "10⁶ bodies, the frame flat in N" on the engine slice alone; the page the player flies POSTs /frame per browser frame and `Session::step` = engine (≤5 ms) + `gather_cached` + `view_json` + wire, and `gather_with` walks **every alive body** (a Newton crossing + a Seen push each; no zoom, frustum or brightness test — view.rs's bodies loop), the wire carrying name+kind+9 floats per row every fra…

**The row's most expensive term is measured invisible on every shipped scene, and the missing slot it re-derives is the same one two other bottlenecks asked for by name (20261013-0350-system-7b86).** The physics holes stand as below. The cost side gains its deletion candidate: `observe::partial`'s per-read `force::field` evaluation — the 81%-of-readout term that makes the view the frame's constraint — computes, over the real read windows (τ = ¼–2 steps, the gather's own domain), a position change ≤ 9.8×10⁻⁶ root ticks (p99 ≤ 7.9×10⁻⁶), and **exactly zero on plain scenes** (coast, held burns L8, brake) — deletable (~35 lines, no law change). [7b86]

**The view's physics is measured wrong three ways near a compact mass — no time-transfer law, a one-argument deflection key, "crosses once" — and every refutation converges on the same one-step fix: a richer memo (delay(b) beside deflection(b), keyed (b, sense|Q), plus the k=0 image pair). The kinked-tube premise survives on shipped code. On the plane, the view — not the engine — is the frame constraint, and the display re-splat is the only over-budget component.**

**The timing hole (two golds, two silvers, four independent oracles).** [ace6, 0b45, 5977, fb64 — unchanged; see Refuted]

**The deflection key (two golds).** [8be2, 9f4a — unchanged]

**"Crosses once" is wrong by an integer (two silvers).** [6eae, 8f00 — unchanged]

**The moving-observer instruments are now measured, and exact to the float floor (20261014-0059-redteam-2fa4).** [unchanged: Seen.shift/direction ≤ 1.4e-10 / 6.4e-15° on the stream class; the fleet seam's member rate omits √(1−v²) (view.rs:397): colour γ−1, luminosity γ⁴; the nested-doll Doppler numerator Galilean; a burning observer's vo+dv exact in the root doll]

**What survives.** Kinked tubes at closing β → 1 (94dc, gold); Newton's crossing ~1.0–1.1 readouts/emitter on the plane (f22e, 3102, 70b0) — 1.16–1.96 readouts/row on the ladder scenes at 10³–10⁵ (62c1), the cache stays near-perfect: the row cost is the readout itself, which is why row-set deletion, not row µs, is the lever.

**Cost: the view is the frame constraint — now measured through the ladder's N, and the constraint is the row set.** The unbudgeted O(all-bodies) view path (gather + json + wire) took 56–93% of every frame at ~6–8 µs/body on the bench (f22e, 97fd, acff; 28–948 bodies), 95–97% of the gather the per-body crossing loop (51bf, 3102), the crossing cache near-perfect. At the ladder's N the same path is 90–91% of a flyable frame that crosses the display budget at the gate's own first rung (10³, 62c1) — the composition the gate's definition excluded.

## Refuted

- "10⁶ bodies in the flyable engine" (the scoreboard's reading of gate N1): the flyable frame crosses 16.7 ms at ~10³ (21.5 ms p50 at 1,028 bodies; 255 at 10⁴; 2,614 at 10⁵) — the engine slice is flat in N and 0.04–4% of the page's frame (20261014-1137-inversion-62c1).
- "The display-quantum row cache is dead" (0e54) — dead **on plane scenes at 28–948 bodies** (5.5–31.2% served); on the ladder scenes ≥99.6% of sky rows are pixel-static per frame and the served fraction is ≤0.4% (20261014-1137-inversion-62c1). Not a contradiction: a domain boundary; 0e54's verdict stands where it was measured.
- [unchanged:] "a fleet member's seen colour/luminosity is read out relativistically like a body's" (2fa4); "the gather has a time-transfer law" (ace6, 5977, 0b45, fb64); "deflection(b) alone is a sufficient memo key" (8be2, 9f4a); "each visible tube crosses the observer's past light cone once" (6eae, 8f00); "winding images need placement in the memo" (9f4a, 8f00); "the strong-kink regime threatens the gather" (94dc); "the display-quantum row cache is the lever [on plane scenes]" (0e54); "recurrence of order ≤ 96 compresses multi-orbit view streams" (8202); fb64's ISCO row artifact; efb2's post-flyby aggregates.

## Open directions

1. **Row-set deletion (the flyable-frame lever, 62c1): the view reads (a) rows on the canvas at the current zoom and (b) far rows only when their displayed pixel (or display quantum) moves — at the fitted zoom O(visible + moved) ≈ 10² rows/frame at every N measured (checker to 3×10⁵), but **at a belt-fitting zoom the on-canvas set is ~N itself (10,060 of 10,028 at 10⁴; 300,067 of 300,028 at 3×10⁵ — checker), so zoom-out is capped only by the display quantum, not the canvas test**. Contract to settle: the zoom change (a zoom-out is a burst of re-reads — amortize or quantize), the turn (heading rotates all sky dots; re-derive staticness in the rotated frame), and the wire (serve deltas or the display quantum, not 9 floats × N). This subsumes 7b86's field-term deletion (a row-µs lever, still real) and 48cf's re-splat.
2. **Build the converged memo** — delay(b) beside deflection(b), keyed (b, sense|Q), plus the k = 0 image pair and a magnification cutoff (ace6, 9f4a, 8f00, fb64, 5977).
3. The Σμ = 1 sum rule as a magnification-conservation check (9f4a).
4. Newborn photon-ring images at the shadow rim — grade a616 before trusting the k = 0 fix at the rim.
5. The gated cache on the M1 (08f7) and the 6–9 µs row (0e54) — row µs, secondary to row-set deletion at scale.
6. The aliasing boundary (efb2).
7. Unmeasured physics: eccentric emitters for the timing error, Kerr timing, multi-mass composition (ace6, 5977); the fleet seam below (2fa4).
8. The one-line fleet fix and its gate (2fa4: the member's rate × √(1−|v|²) at view.rs:397; freeze the first Seen-value criterion in r6).

## Contradictions

None open. [Prior resolutions unchanged: 6eae→8f00; fb64's artifact refined; 8be2's 2.37× replaced by 3.32×; efb2 narrowed; 7b86's reads/body/frame = 2.5–3.8 vs 1.0–1.92 — different scenes; 62c1's readouts/row 1.16–1.96 on ladder scenes sits between them.]

## Runs
- 20261006-0030-m-obscure-8202 (silver): view streams: single-orbit recurrence exact (5e-14); incommensurate eccentric pairs admit no order ≤ 96.
- 20261006-1029-constraint-f22e (silver): unbudgeted O(all-bodies) view path is the frame constraint (60%, 6–8 µs/body); crossing cache near-perfect.
- 20261008-0458-constraint-3102 (silver): gather 67.7% of frame, bodies loop 97% of it, 1.065 readouts/emitter, 12.3 µs/live body.
- 20261008-0945-second-20261008-0743-constraint-4588-0e54 (silver): display-quantum row cache killed: 5.5–31.2% of rows served; attack the 6–9 µs row.
- 20261008-1521-quant-97fd (silver): gather owns the flown frame 59–71% across seeds and rtf; the paced-tax headline was a load artifact.
- 20261008-2113-second-20261008-2031-constraint-4b27-08f7 (silver): gated view cache holds: gather 3.6–3.9× faster, readouts 62→2–7, digest bit-identical.
- 20261008-2349-constraint-70b0 (missing): ungraded: gather 66–74% at rtf 1–1000; 97% of it the ramped readout.
- 20261009-0621-constraint-51bf (silver): gather anatomy: crossing loop 95%, field evals re-read per emitter per Newton step are 81%.
- 20261009-1649-second-20261009-1556-redteam-18fc-94dc (gold): kinked tubes survive: 0 drops, dense kinked = straight cost; strong-kink regime empty by physics.
- 20261009-2120-redteam-ace6 (gold): no time-transfer law: flat light-time off 2–176° within ~50 M; fix Δt(b) beside deflection(b).
- 20261010-0541-system-d51f (silver): deadlines, gather and news gravity re-derive one doll-chain readout; arrival rate already stored per frame.
- 20261010-2052-redteam-8be2 (gold): deflection(b) key broken for rotating dolls: needs (b, sense) (3.32× at χ 0.998) and (b, Q); Shapiro unmemoized.
- 20261010-2141-second-20261010-2052-redteam-8be2-9f4a (gold): winding images ≤ 0.084% of brightest: the (b, sense|Q)+delay(b) memo needs no winding placement.
- 20261010-2314-redteam-0b45 (silver): flat light-time draws 6–20 M emitters 7°–86° out of phase; r_e = 6 M ≥ 42° wrong at all phases.
- 20261011-0006-constraint-48cf (silver): display re-splat is the only over-budget component: 36–110 ms, flat in change (rtf-independent).
- 20261011-0614-redteam-a616 (missing): ungraded: Newton-from-previous-frame misses 100% of newborn photon-ring images.
- 20261011-0924-redteam-5977 (gold): no memo, gate or rung carries light delay: 4.3–10.1° phase error near a mass; one delay(b) column fixes it.
- 20261011-1234-redteam-6eae (silver): "crosses once" wrong: ≥ 2–3 images on 100% of azimuths at r_o 100–3.2 M; 4 images 99% at 3.2 M.
- 20261011-1332-constraint-acff (silver): mean engine cost is not the constraint: O(N) gather 62–72%; single items run past the whole 5 ms budget.
- 20261011-1332-second-20261011-1234-redteam-6eae-8f00 (silver): player-visible error is the k=0 pair (43–84% of azimuths); windings never visible; fix = pair + cutoff.
- 20261011-1917-redteam-fb64 (silver): arrival delay renders 1–97 px wrong within ~60 M; delay(b) memo collapses error 40–150× at r_e ≥ 60.
- 20261012-0138-redteam-0fe0 (silver): representation red-team; for the view: no view gate exists, and Newton's crossing holds at 3.00 iterations for every β warm-started (cold seeds leave the bracket at β ≥ 0.9, its check).
- 20261013-0350-system-7b86 (pending grade): partial's per-read field term ≤ 10⁻⁵ read quanta, zero on plain scenes; one acceleration slot asked for by view, gravity ring and burn waterfall.
- 20261014-0059-redteam-2fa4 (awaiting grade): moving-observer instruments exact to 1.4e-10/6.4e-15°; fleet members' seen colour Newtonian (γ−1/γ⁴−1); no gate judges a seen value.
- 20261008-0945-second-20261008-0743-constraint-4588-0e54 (silver): display-quantum row cache killed on plane scenes: 5.5–31.2% of rows served; attack the 6–9 µs row.
- 20261008-1521-quant-97fd (silver): gather owns the flown frame 59–71% across seeds and rtf.
- 20261010-0541-system-d51f (silver): deadlines, gather and news gravity re-derive one doll-chain readout.
- 20261010-2052-redteam-8be2 (gold): deflection(b) key broken for rotating dolls: needs (b, sense) and (b, Q); Shapiro unmemoized.
- 20261010-2314-redteam-0b45 (silver): flat light-time draws 6–20 M emitters 7°–86° out of phase.
- 20261011-0006-constraint-48cf (silver): display re-splat is the only over-budget component: 36–110 ms, flat in change.
- 20261011-0924-redteam-5977 (gold): no memo, gate or rung carries light delay: 4.3–10.1° phase error near a mass.
- 20261011-1234-redteam-6eae (silver): "crosses once" wrong: ≥ 2–3 images on 100% of azimuths at r_o 100–3.2 M.
- 20261011-1332-second-20261011-1234-redteam-6eae-8f00 (silver): player-visible error is the k=0 pair; windings never visible.
- 20261012-0138-redteam-0fe0 (silver): for the view: no view gate exists; Newton's crossing holds at 3.00 iterations warm.
- 20261014-0059-redteam-2fa4 (awaiting grade): moving-observer instruments exact to 1.4e-10/6.4e-15°; fleet members' seen colour Newtonian; no gate judges a seen value.
- 20261014-1137-inversion-62c1 (this run): the flyable frame crosses the display budget at the gate's own first rung (21.5 ms at 10³, 255 at 10⁴, 2,614 at 10⁵; gather 90%); the visible set is ~73 rows flat in N; 99.6–99.96% of sky rows pixel-static; the lever is the row set. Checker: reproduced (21.4 ms at 10³, seed 2 same at 10⁴); the linear law exact at 3×10⁵ (7.83 s p50, 77.5 rows on-canvas); belt-zoom puts ~N rows on-canvas — the O(10²) visible set is a fitted-zoom fact.
