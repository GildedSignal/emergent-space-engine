topic: view
status: open
closed-by:
valid-while:
updated: 20261014-1221-second-20261014-1137-inversion-62c1-2df1

# The view: the observer's past light cone, lensing, kinked tubes

## Current best

**The row-set deletion is built on the shipped crossings and the flyable frame collapses: steady map frames ≈ 1-3 ms p50 at 10³-10⁶ bodies at both the fitted and the belt zoom (86-160× at 10³, ~10³× at 10⁶ against the linear law), display-exact to ≤ 0.1-2% of drawn rows per frame, and the turn costs the server nothing (20261014-1221-second-20261014-1137-inversion-62c1-2df1).** The build: `gather_rows` (view.rs, this run's patch) reads the shipped crossings for a chosen body set — `gather_cached` proven byte-identical by digest — and the policy around it does three things: the page's own canvas test (off-canvas kind≥3 rows never read), a display-quantum due wheel (a row is read when its drawn pixel could cross half a pixel; drift measured between reads, frozen rows backed off ×4 and jittered), and a delta wire (ids + changed rows + gone: ~9-30 KB/frame against 0.29-27 MB). The panel band (nearest bodies) is served live every frame. The audit — the shipped `gather_cached` on the same frames — finds ≤ 1.4-15 violations/frame (see the run's residue). **The turn is free:** a turn rotates the heading, which is header data; aberration depends on velocity — the server's rows are byte-identical through a 30-frame turn and the quanta live in the row's own frame (heading-free polar for the sky), so the rotation is derived client-side. **The zoom-out is bounded:** entries arrive on the zoom's geometric schedule and are read as they enter (measured: max 6.7 ms/frame at 10³; the window's readouts ≈ the entering set). **The sky does not collapse at this quantum:** the near field is genuine per-frame surprise — sky steady ≈ 20 ms at 10³ (500 locals), ≈ 10-15 ms at 10⁴+ (locals capped at 300); the far belt is frozen like the map's. The map is the flyable display. The one Θ(N) moment left is the fill (the first full read, once per flight ≈ one baseline gather, like the page's first frame after a restart). [2df1]
**Checker's correction (2df1, silver): the collapse is p50-only.** The probe's steady **p99 is Θ(N)** — the birth/death scan stand-in costs ~3.5 µs/body (37 ms at 10⁴, 360 at 10⁵, 3,480 ms at 10⁶, recurring every 240 frames), so against the smoothness rule ("i care about the p95/99 results i want the game to be smooth", PRINCIPLES #12) the probe still crosses 16.7 ms at ~10⁴ until the engine's birth feed replaces the scan. Everything else reproduces, including at 10⁶ and a decade up in rtf (p50 4.8/5.6 ms at 10⁴/10⁵ at rtf 1000).

**The flyable frame is the view's, and the view's Θ(N) row set is a far-row tax: 93-99.9% of its rows buy zero pixels in map mode on the ladder scenes, so the flyable ceiling is ~10³ bodies, not the gate's 10⁶ (62c1, silver, reproduced by its checker to 3×10⁵).** Gate N1 certified the engine slice alone; the page's frame = engine + `gather_cached` + wire crosses 16.7 ms at 10³ (21.5 ms p50 at 1,028 bodies; 255 at 10⁴; 2,614 at 10⁵; linear, 7.83 s at 3×10⁵; ~26 s extrapolated at 10⁶). The deletion above is the lever the checker named, now measured. [62c1]

**The row's most expensive term is measured invisible on every shipped scene, and the missing slot it re-derives is the same one two other bottlenecks asked for by name (20261013-0350-system-7b86).** The physics holes stand as below. The cost side gains its deletion candidate: `observe::partial`'s per-read `force::field` evaluation — the 81%-of-readout term that makes the view the frame's constraint — computes, over the real read windows (τ = ¼–2 steps, the gather's own domain), a position change ≤ 9.8×10⁻⁶ root ticks (p99 ≤ 7.9×10⁻⁶), and **exactly zero on plain scenes** (coast, held burns L8, brake) — deletable (~35 lines, no law change). [7b86]

**The view's physics is measured wrong three ways near a compact mass — no time-transfer law, a one-argument deflection key, "crosses once" — and every refutation converges on the same one-step fix: a richer memo (delay(b) beside deflection(b), keyed (b, sense|Q), plus the k=0 image pair). The kinked-tube premise survives on shipped code. On the plane, the view — not the engine — is the frame constraint, and the display re-splat is the only over-budget component.**

**The timing hole (two golds, two silvers, four independent oracles).** [ace6, 0b45, 5977, fb64 — unchanged; see Refuted]

**The deflection key (two golds).** [8be2, 9f4a — unchanged]

**"Crosses once" is wrong by an integer (two silvers).** [6eae, 8f00 — unchanged]

**The moving-observer instruments are now measured, and exact to the float floor (20261014-0059-redteam-2fa4).** [unchanged: Seen.shift/direction ≤ 1.4e-10 / 6.4e-15° on the stream class; the fleet seam's member rate omits √(1−v²) (view.rs:397): colour γ−1, luminosity γ⁴; the nested-doll Doppler numerator Galilean; a burning observer's vo+dv exact in the root doll]

**What survives.** Kinked tubes at closing β → 1 (94dc, gold); Newton's crossing ~1.0–1.1 readouts/emitter on the plane (f22e, 3102, 70b0) — the row cost is the readout itself, which is why row-set deletion, not row µs, is the lever.

**Cost: the view is the frame constraint — now measured through the ladder's N, and the constraint was the row set; the deletion is built and the constraint is now the near field (sky) and the fill.** The unbudgeted O(all-bodies) view path (gather + json + wire) took 56–93% of every frame at ~6–8 µs/body on the bench (f22e, 97fd, acff; 28–948 bodies), 95–97% of the gather the per-body crossing loop (51bf, 3102), the crossing cache near-perfect. At the ladder's N the same path was 90–91% of a flyable frame that crossed the display budget at the gate's own first rung (62c1); with the row-set deletion the steady map frame is flat in N at both zooms (2df1).

## Refuted

- "10⁶ bodies in the flyable engine" (the scoreboard's reading of gate N1): the flyable frame crosses 16.7 ms at ~10³ (21.5 ms p50 at 1,028 bodies; 255 at 10⁴; 2,614 at 10⁵) — the engine slice is flat in N and 0.04–4% of the page's frame (62c1). With the deletion the flyable map frame is ~1-3 ms **p50** at 10³-10⁶ (2df1); the probe's p99 is still Θ(N) (the scan stand-in: 3,480 ms at 10⁶), so the reading is restored only when the engine's birth feed replaces the scan — the unbuilt half.
- "The display-quantum row cache is dead" (0e54) — dead **on plane scenes at 28–948 bodies** (5.5–31.2% served); on the ladder scenes ≥99.6% of sky rows are pixel-static per frame and the served fraction is ≤0.4% (62c1). Not a contradiction: a domain boundary; 0e54's verdict stands where it was measured. The deletion now carries the flyable frame at scale (2df1).
- "The turn is a burst the server must pay" (62c1's disclosed contract): the heading is header data and the sky's quanta are heading-free — a 30-frame turn leaves the server's rows byte-identical (2df1). The burn remains a real burst (vo changes aberration for every row; unmeasured).
- [unchanged:] "a fleet member's seen colour/luminosity is read out relativistically like a body's" (2fa4); "the gather has a time-transfer law" (ace6, 5977, 0b45, fb64); "deflection(b) alone is a sufficient memo key" (8be2, 9f4a); "each visible tube crosses the observer's past light cone once" (6eae, 8f00); "winding images need placement in the memo" (9f4a, 8f00); "the strong-kink regime threatens the gather" (94dc); "the display-quantum row cache is the lever [on plane scenes]" (0e54); "recurrence of order ≤ 96 compresses multi-orbit view streams" (8202); fb64's ISCO row artifact; efb2's post-flyby aggregates.

## Open directions

1. **Adopt the row-set deletion into the shipped session (2df1's build is the candidate):** `gather_rows` is in view.rs behind this run's patch; the policy (wheel, canvas test, band, delta wire) is experiment code in the example and wants a home in the session, with the engine's event feed replacing the birth scan and the fill. The wire's client half (ids + deltas) wants the page's `poll`/draw loop to hold rows by id. **The missing engine half is the birth/death feed:** the event counter fires on every kick and says nothing about births at belt scale, so the probe's scan is Θ(N) at ~3.5 µs/body and owns the steady p99 (37/360/3,480 ms at 10⁴/10⁵/10⁶, every 240 frames); the feed — or any O(changes) stand-in — must be built and the p99 re-measured flat before the deletion is flyable.
2. **The sky's near field:** O(locals) rows move a measurable fraction of a pixel per frame at rtf 100 — either a coarser sky quantum, an angular bucketing of the clumped fleet dots, or accept ~10-20 ms sky as the second display's price. At lower rtf the dues stretch proportionally (unmeasured).
3. **The burn burst:** a burn changes vo, so every row's aberration shifts at once — the served set is then O(visible); measure it (one run, keys = thrust).
4. **Build the converged memo** — delay(b) beside deflection(b), keyed (b, sense|Q), plus the k = 0 image pair and a magnification cutoff (ace6, 9f4a, 8f00, fb64, 5977).
5. The Σμ = 1 sum rule as a magnification-conservation check (9f4a).
6. Newborn photon-ring images at the shadow rim — grade a616 before trusting the k = 0 fix at the rim.
7. The gated cache on the M1 (08f7) and the 6–9 µs row (0e54) — row µs, now secondary to row-set deletion at scale (2df1 measured ~11 µs/readout on this box).
8. The aliasing boundary (efb2).
9. Unmeasured physics: eccentric emitters for the timing error, Kerr timing, multi-mass composition (ace6, 5977); the fleet seam below (2fa4).
10. The one-line fleet fix and its gate (2fa4: the member's rate × √(1−|v|²) at view.rs:397; freeze the first Seen-value criterion in r6).

## Contradictions

None open. [Prior resolutions unchanged: 6eae→8f00; fb64's artifact refined; 8be2's 2.37× replaced by 3.32×; efb2 narrowed; 7b86's reads/body/frame = 2.5–3.8 vs 1.0–1.92 — different scenes; 62c1's readouts/row 1.16–1.96 on ladder scenes sits between them; 2df1's audit residue at belt zoom (15-17 rows/frame at 10³), diagnosed by its checker: single-pixel anchor drift on accelerating near-field kind-3 rows and the fleet marker (miss = ghost = 0) — the wheel's ×4 drift slack undershoots accelerating drift at the belt's coarse pixel scale; a slack fix, not a structural hole.]

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
- 20261014-1137-inversion-62c1 (silver): the flyable frame crosses the display budget at the gate's own first rung (21.5 ms at 10³, 255 at 10⁴, 2,614 at 10⁵; gather 90%); the visible set is ~73 rows flat in N; 99.6–99.96% of sky rows pixel-static; the lever is the row set. Checker: reproduced (21.4 ms at 10³, seed 2 same at 10⁴); the linear law exact at 3×10⁵ (7.83 s p50, 77.5 rows on-canvas); belt-zoom puts ~N rows on-canvas — the O(10²) visible set is a fitted-zoom fact.
- 20261014-1221-second-20261014-1137-inversion-62c1-2df1 (this run): the deletion built and measured: steady map frame ~1-3 ms p50 at 10³-10⁶ at fitted and belt zoom; delta wire KB/frame against MB; the turn free (rows byte-identical); the zoom-out bounded (entries read as they enter); the audit ≤ 0.1-2% of drawn rows (residue: hand-off timing, belt-zoom undiagnosed); the sky's near field does not collapse (~10-20 ms, O(locals)); the fill is the one Θ(N) moment left.
