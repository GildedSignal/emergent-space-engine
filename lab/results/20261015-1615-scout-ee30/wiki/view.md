topic: view
status: open
closed-by:
valid-while:
updated: 20261015-1615-scout-ee30

# The view: the observer's past light cone, lensing, kinked tubes

## Current best

**The missing engine half is priced and it is free: the birth/death feed that replaces the 240-frame membership rescan (this page's p99 owner) costs the observer's own orbital sweep of the map window through the belt — 2.4–3.4×10⁻⁸ flips/s per belt body (one flip per body per ~year), ~10⁻⁴ cores composed at 10⁹ against the scan's 8.75 — and at fitted zoom the belt is envelope-disjoint from the window (margin 79–86×W, permanent at coast, held under a 0.05c burn: 0 events), so the tracked set is O(locals) and the Θ(N) term deletes at every N (20261015-1615-scout-ee30, scout).** Float replica on the ladder scene's own birth law with the shipped client's map criterion verbatim (drawMap: star's-frame box centred on the observer's current position, retarded offsets; fitted W = 3.5 ls, belt W = 750 ls): steady coast 3.3e-3 events/s at 10⁵ (held-out seed 3.4e-3; per-body rates 2.4–3.4e-8 across N and orbital phase), a 0.05c radial burn adds 507 entries at 10⁵ with worst frame 6, and the one moment needing a drain is the zoom-out fill: worst frame 2,722 entries at 10⁵ (9.5 ms at 3.5 µs/entry) and 5,539 at 2×10⁵ (19.4 ms — the 16.7 ms budget crossing sits between 10⁵ and 2×10⁵, linear in N; ~1 s at 10⁹ un-drained). The certificate form to wire: a group envelope (window box vs belt annulus in retarded coordinates, O(1), re-checked on burns and zooms), a per-tracked-row next-boundary time that is a 1-D root on the observer's compiled tube computed at emission-step time (rides the doll's clock, no new state), and the zoom drain. Prior art mapped: kinetic data structures (scheduled certificates; the flight plan is the compiled orbit), incremental view maintenance (the map is a materialized view; cost ∝ delta), netcode interest management (boundary hysteresis). The row-value rail remains the steady engine cost: emission steps × in-window fraction × ~4 µs → ~0.14 cores at 10⁹ at full zoom; the view's engine-side total ~0.15 cores, 25× under budget.

**The in-band gather is priced and its floor is measured exact: between the tube's own time quanta a view row is bit-reproducible from one cached emission and the fresh observer state, so the shipped per-frame O(N) crossing walk buys literally zero information change on far rows — at 10⁵, 99,701/100,028 far rows are bit-exact (p99 drift 3.1e-17) through the flight while the gather crawls at rtf 0.68 (196.6 s of wall for 80 frames, the engine ≤0.06 ms of each); the free-run horizon at the map half-pixel is 2.7e4 frames p99 at 10³ and unbounded-by-window at 10⁴-10⁵, the burn does not touch it (drift 6.02e-8 vs 6.10e-8 rad/frame coast vs L8 at 10³; at 10⁵ coast and L8 are digit-identical at 3.084e-17; L15 bit-frozen 4e-16 with the emission step at the same curv… (20261015-1338-components-649c; unchanged)]

**Checker's regime correction (649c): the 10⁴-10⁵ exactness windows end before the belt's first light.** Those arms stop at game 433/133 s while the first emission steps land at 356-543 game-s (≈ the inner belt's light time; before first light `view.rs` returns the tick-0 state, constant by construction), so their bit-exactness (8.5e-18 / 3.1e-17) and "unbounded-by-window" horizons are the pre-light regime, and "9,714/10,028 rows never step in 260 frames" is contradicted by the same arm's own max slope (4.16e-7 ⇒ at least one stepper; ≥99% is what is measured). The permanent regime is the run's own 10³ 899-frame arm: far drift 1.96e-7 rad/frame p99 — the emission point advancing along the emitter's orbit, not observer parallax (it scales with the frame's gam…

**The row-set deletion is built on the shipped crossings and the flyable frame collapses: steady map frames ≈ 1-3 ms p50 at 10³-10⁶ at both the fitted and the belt zoom (86-160× at 10³, ~10³× at 10⁶ against the linear law), display-exact to ≤ 0.1-2% of drawn rows per frame, and the turn costs the server nothing (20261014-1221-second-20261014-1137-inversion-62c1-2df1).** [unchanged]

**Checker's correction (2df1, silver): the collapse is p50-only.** The probe's steady p99 is Θ(N) — the birth/death scan stand-in costs ~3.5 µs/body (37 ms at 10⁴, 360 at 10⁵, 3,480 ms at 10⁶, recurring every 240 frames), so against the smoothness rule the probe still crosses 16.7 ms at ~10⁴ until the engine's birth feed replaces the scan. [scout-ee30 now prices that feed: the replacement composes to ~10⁻⁴ cores at 10⁹ vs the scan's 8.75; the drain is required at the zoom fill (worst frame ~2.7e7 entries ≈ 95 s at 10⁹) and, per the checker's recomposition, at the burn too at 10⁹ (worst frame ~6e4 entries ≈ 0.2 s — the dossier's "2 ms, under budget" was a 100× scaling slip on the worst frame)]

**The flyable frame is the view's, and the view's Θ(N) row set is a far-row tax: 93-99.9% of its rows buy zero pixels in map mode on the ladder scenes, so the flyable ceiling is ~10³ bodies, not the gate's 10⁶ (62c1, silver, reproduced by its checker to 3×10⁵).** [unchanged]

## Refuted

- **The 240-frame membership rescan as a needed component (2df1's stand-in):** the set it recomputes changes at 2.4–3.4×10⁻⁸ flips/s per belt body (the observer's orbital sweep of the window; one flip per body per ~year, confirmed over a full observer year at 3.08×10⁻⁸ by the checker), and at fitted zoom the belt is envelope-disjoint from the window with margin 79–86×W on the author's 5×10⁶-s window, 68–71×W over a full observer year and 31×W at the all-e=0.4 tail (checker), permanent at coast and held under a 0.05c burn — the scan's 8.75 cores at 10⁹ buy nothing the envelope plus per-row boundary roots do not (20261015-1615-scout-ee30).
- **View open 3's "the served set is then O(visible)" for the burn (2df1's contract):** measured on the shipped crossings, a burn (L8; L15 same) changes only the observer side of a far row, which the closed form takes fresh; far-row drift is unchanged to 1.3% in the run's own windows (6.02e-8 vs 6.10e-8 rad/frame — but those windows end before the belt's first light; see the regime correction above). The burn's re-read set is the near set, O(313), not O(visible). (20261015-1338-components-649c)
- [unchanged entries: "10⁶ bodies in the flyable engine" (62c1/2df1 reading); "the display-quantum row cache is dead" (0e54's plane-scene domain); "the turn is a burst the server must pay"; the physics holes (time transfer, deflection key, crosses-once)]

## Open directions

1. **Wire the feed (scout-ee30's certificate form, the engine half 2df1 named):** the group envelope (window box vs belt annulus in retarded coordinates, O(1)) replaces the rescan at fitted zoom; per tracked row, the next-boundary time is a 1-D root on the observer's compiled tube computed at emission-step time (rides the doll's clock); the zoom drain (budgeted admission, the 4487 pattern — worst frame 19.4 ms at 2×10⁵ undrained, 27,321 entries ≈ 96 ms at 10⁶ (checker, linear in N), ~2.7e7 entries ≈ 95 s at 10⁹) and the burn drain (checker: worst frame ~6e4 entries ≈ 0.2 s at 10⁹) sit inside the presented-tick discipline; digest-neutral by 2df1's display-exactness.
2. **The sky's near field:** unchanged — O(locals) rows move a measurable fraction of a pixel per frame; 649c folds the burn into this same set (observer-side closed form on frozen rows, exact). The sky mode's log-polar placement is not feed-priced (scout-ee30's domain gap).
3. ~~The burn burst~~ — answered at the physics level (649c): observer-side, exact, O(near); what remains unmeasured is the wire/draw cost of re-aberrating O(visible) rows client-side (a page question, not an engine readout question).
4. Build the converged memo (delay(b) beside deflection(b), keyed (b, sense|Q), plus the k = 0 image pair). [unchanged]
5. The Σμ = 1 sum rule as a magnification-conservation check (9f4a). [unchanged]
6. Newborn photon-ring images at the shadow rim — grade a616 before trusting the k = 0 fix at the rim. [unchanged]
7. The gated cache on the M1 (08f7) and the 6-9 µs row (0e54) — row µs, now secondary to row-set deletion at scale. [unchanged]
8. The aliasing boundary (efb2). [unchanged]
9. Unmeasured physics: eccentric emitters for the timing error, Kerr timing, multi-mass composition; the fleet seam (2fa4). [unchanged]
10. The one-line fleet fix and its gate (2fa4). [unchanged]

## Contradictions

None open. 649c's bit-frozen far rows vs 2df1's "≥99.6% of sky rows are pixel-static per frame" (62c1): the same fact at two resolutions — 649c measures the staticness exact (1e-16) between the tube's time quanta and attributes the residual per-frame motion to observer parallax; 62c1 measured it at pixel scale. 7b86's reads/body/frame 2.5-3.8 vs 649c's 1.5-2.0: different scenes (plane vs ladder). scout-ee30's steady flux (3.3e-3/s at 10⁵) vs 2df1's 240-frame rescan cadence: not a contradiction — the rescan was a stand-in, and the feed's measured rates are what its replacement must serve.

## Runs
- 20261015-1615-scout-ee30 (silver): the birth/death feed priced — steady flux 2.4-3.4e-8/s per body (3.08e-8 over a full observer year, checker), ~10⁻⁴ cores at 10⁹ vs the scan's 8.75; fitted-zoom envelope disjoint (79-86×W author window, 68-71×W full year, 31×W e-tail, checker); drain required at zoom (95 s at 10⁹) and burn (0.2 s at 10⁹, checker's recomposition); certificate form + KDS/IVM/interest-management mapping.
- 20261015-1338-components-649c (awaiting grade): in-band gather priced (19-22 µs/body/frame, ≥97% of the flown frame at 10⁵) and floored exactly: far rows bit-reproducible between tube time quanta (first step 355-542 game-s), horizon 2.7e4/8.3e3 frames p99 map (4.5e3/1.4e3 sky), burn-exempt (drift unchanged, readouts/emitter 1.96-2.00), near set O(313) the per-frame reads.
- 20261014-1221-second-20261014-1137-inversion-62c1-2df1: the deletion built and measured; delta wire; the turn free; the fill is the one Θ(N) moment left.
- 20261013-0350-system-7b86: partial's per-read field term deletable (~35 lines).
- 20261014-0059-redteam-2fa4: moving-observer instruments exact to 1.4e-10/6.4e-15°.
- 20261014-1137-inversion-62c1: the flyable frame crosses 16.7 ms at ~10³; the far-row tax.
- [prior runs unchanged, see git history of this page]
