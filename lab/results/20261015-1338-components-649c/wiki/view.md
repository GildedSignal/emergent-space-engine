topic: view
status: open
closed-by:
valid-while:
updated: 20261015-1338-components-649c

# The view: the observer's past light cone, lensing, kinked tubes

## Current best

**The in-band gather is priced and its floor is measured exact: between the tube's own time quanta a view row is bit-reproducible from one cached emission and the fresh observer state, so the shipped per-frame O(N) crossing walk buys literally zero information change on far rows — at 10⁵, 99,701/100,028 far rows are bit-exact (p99 drift 3.1e-17) through the flight while the gather crawls at rtf 0.68 (196.6 s of wall for 80 frames, the engine ≤0.06 ms of each); the free-run horizon at the map half-pixel is 2.7e4 frames p99 at 10³ and unbounded-by-window at 10⁴-10⁵, the burn does not touch it (drift 6.02e-8 vs 6.10e-8 rad/frame coast vs L8 at 10³; at 10⁵ coast and L8 are digit-identical at 3.084e-17; L15 bit-frozen 4e-16 with the emission step at the same curve frame as coast — an arm-independent tube quantum), and the per-frame read set is O(near) ≈ 308-322 rows at every N (20261015-1338-components-649c, components).** The instrument (`view_floor`, the page's own loop order): at 10³/10⁴/10⁵ the gather is 19-22 µs/body per frame (readouts/emitter 1.5-2.0), and at 10⁵ it owns ≥97% of the flown frame — the nladder page's rtf-0.7/~2 s-frame crawl is this gather. The deletion 2df1 built for the map is therefore not a display approximation on far rows but an exactness: the shipped crossings return a bit-constant emission point for ≥213 frames (first step 355-542 game-s after freeze; steps are the tube's own time quanta, not the frame), and the per-frame direction motion of a far row (≈6e-8 rad/frame at rtf 100) is pure observer parallax, reproduced by the observer-side closed form to 1e-16. Burn L8: readouts/emitter 1.96 vs 1.67, far-row drift unchanged; L15 same (≤3.0). View open 3's presumption ("a burn shifts every row's aberration at once — served set O(visible)") is wrong at the physics level: aberration is observer-side and exact on a frozen row; the burn adds only the near set, like the sky's near field (open 2).

**Checker's regime correction (649c): the 10⁴-10⁵ exactness windows end before the belt's first light.** Those arms stop at game 433/133 s while the first emission steps land at 356-543 game-s (≈ the inner belt's light time; before first light `view.rs` returns the tick-0 state, constant by construction), so their bit-exactness (8.5e-18 / 3.1e-17) and "unbounded-by-window" horizons are the pre-light regime, and "9,714/10,028 rows never step in 260 frames" is contradicted by the same arm's own max slope (4.16e-7 ⇒ at least one stepper; ≥99% is what is measured). The permanent regime is the run's own 10³ 899-frame arm: far drift 1.96e-7 rad/frame p99 — the emission point advancing along the emitter's orbit, not observer parallax (it scales with the frame's game-time: 1.1e-5 rad/frame at rtf 10⁴) — horizon 8.3e3 frames map / 1.4e3 sky, far demand ~0.12/frame at 10³ (~12 at 10⁵ by row count). The O(near) per-frame read set and the ~300× deletion survive unchanged. Checker cases: L15 at 10³ freeze 260 (partially live — the belt itself is still pre-first-light there) leaves far rows near-exact (p99 1e-17) where coast drifts 6.1e-8; N=3×10⁵ holds (price linear ~23-25 µs/body, near set 338, 786 MB; the "far rows exact" there is the same pre-light regime). Second checker (check2), live-regime staircase at 10⁴ (1000 frames, freeze 100, window crossing the belt's first light): far drift p99 2.00e-7 rad/frame, horizon 8.17e3 frames map, far demand 1.23/frame against 10,028 shipped, readouts/emitter 1.75 with every row stepping — the drift is N-independent as predicted (P6's ≥5,000-frame horizon holds in the live regime by direct measurement); the same staircase under L15 drifts 2.47e-7 (1.26× coast).

**The row-set deletion is built on the shipped crossings and the flyable frame collapses: steady map frames ≈ 1-3 ms p50 at 10³-10⁶ at both the fitted and the belt zoom (86-160× at 10³, ~10³× at 10⁶ against the linear law), display-exact to ≤ 0.1-2% of drawn rows per frame, and the turn costs the server nothing (20261014-1221-second-20261014-1137-inversion-62c1-2df1).** [unchanged]

**Checker's correction (2df1, silver): the collapse is p50-only.** The probe's steady p99 is Θ(N) — the birth/death scan stand-in costs ~3.5 µs/body (37 ms at 10⁴, 360 at 10⁵, 3,480 ms at 10⁶, recurring every 240 frames), so against the smoothness rule the probe still crosses 16.7 ms at ~10⁴ until the engine's birth feed replaces the scan. [unchanged; 649c's measured horizons now justify the wheel's slack on far rows exactly rather than by drift estimate]

**The flyable frame is the view's, and the view's Θ(N) row set is a far-row tax: 93-99.9% of its rows buy zero pixels in map mode on the ladder scenes, so the flyable ceiling is ~10³ bodies, not the gate's 10⁶ (62c1, silver, reproduced by its checker to 3×10⁵).** [unchanged; 649c prices the same tax in-band: 19-22 µs/body/frame every frame]

## Refuted

- **View open 3's "the served set is then O(visible)" for the burn (2df1's contract):** measured on the shipped crossings, a burn (L8; L15 same) changes only the observer side of a far row, which the closed form takes fresh; far-row drift is unchanged to 1.3% in the run's own windows (6.02e-8 vs 6.10e-8 rad/frame — but those windows end before the belt's first light; see the regime correction above). The burn's re-read set is the near set, O(313), not O(visible). (20261015-1338-components-649c)
Checker, blind, strengthened it: L15 at 10³ freeze 260 (a partially-live window — the p99 belt row is still pre-first-light there) leaves far rows near-exact (p99 1e-17, max 2.8e-7), readouts/emitter 1.99, µs/body 1.09× coast. Second checker (check2), in the fully live regime — the 999-frame staircase whose window crosses the belt's first light, where coast drifts 1.96e-7 p99: L15 far drift 2.47e-7 p99 (1.26× coast, horizon 6.6e3 frames; not identical — a receding relativistic burn also retards the emission ticks through the observer's (1−n·β_obs), a closed-form observer term: the probe row's t_e pins at 60.6 s from k≈51), readouts/emitter 1.99; and rows frozen before the burn onset stay bit-exact (≤4e-16) for 248 of 249 frames across it.
- [unchanged entries: "10⁶ bodies in the flyable engine" (62c1/2df1 reading); "the display-quantum row cache is dead" (0e54's plane-scene domain); "the turn is a burst the server must pay"; the physics holes (time transfer, deflection key, crosses-once)]

## Open directions

1. **Adopt the row-set deletion into the shipped session (2df1's build is the candidate):** with 649c's measured horizons the wheel's slack on far rows can be the emission-step event itself (bit-exact between steps), not a drift estimate; the near set (~313 rows, drift ~3e-3 rad/frame) is the per-frame read set; the missing engine half is still the birth/death feed (the p99 owner).
2. **The sky's near field:** unchanged — O(locals) rows move a measurable fraction of a pixel per frame; 649c folds the burn into this same set (observer-side closed form on frozen rows, exact).
3. ~~The burn burst~~ — answered at the physics level (649c): observer-side, exact, O(near); what remains unmeasured is the wire/draw cost of re-aberrating O(visible) rows client-side (a page question, not an engine readout question).
4. Build the converged memo (delay(b) beside deflection(b), keyed (b, sense|Q), plus the k = 0 image pair). [unchanged]
5. The Σμ = 1 sum rule as a magnification-conservation check (9f4a). [unchanged]
6. Newborn photon-ring images at the shadow rim — grade a616 before trusting the k = 0 fix at the rim. [unchanged]
7. The gated cache on the M1 (08f7) and the 6-9 µs row (0e54) — row µs, now secondary to row-set deletion at scale. [unchanged]
8. The aliasing boundary (efb2). [unchanged]
9. Unmeasured physics: eccentric emitters for the timing error, Kerr timing, multi-mass composition; the fleet seam (2fa4). [unchanged]
10. The one-line fleet fix and its gate (2fa4). [unchanged]

## Contradictions

None open. 649c's bit-frozen far rows vs 2df1's "≥99.6% of sky rows are pixel-static per frame" (62c1): the same fact at two resolutions — 649c measures the staticness exact (1e-16) between the tube's time quanta and attributes the residual per-frame motion to observer parallax; 62c1 measured it at pixel scale. 7b86's reads/body/frame 2.5-3.8 vs 649c's 1.5-2.0: different scenes (plane vs ladder).

## Runs
- 20261015-1338-components-649c (this run, awaiting grade): in-band gather priced (19-22 µs/body/frame, ≥97% of the flown frame at 10⁵) and floored exactly: far rows bit-reproducible between tube time quanta (first step 355-542 game-s), horizon 2.7e4/8.3e3 frames p99 map (4.5e3/1.4e3 sky), burn-exempt (drift unchanged, readouts/emitter 1.96-2.00), near set O(313) the per-frame reads.
- 20261014-1221-second-20261014-1137-inversion-62c1-2df1: the deletion built and measured; delta wire; the turn free; the fill is the one Θ(N) moment left.
- 20261013-0350-system-7b86: partial's per-read field term deletable (~35 lines).
- 20261014-0059-redteam-2fa4: moving-observer instruments exact to 1.4e-10/6.4e-15°.
- 20261014-1137-inversion-62c1: the flyable frame crosses 16.7 ms at ~10³; the far-row tax.
- [prior runs unchanged, see git history of this page]
