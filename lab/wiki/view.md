topic: view
status: open
closed-by:
valid-while:
updated: 20261018-0932-system-0d46

# The view: the observer's past light cone, lensing, kinked tubes

## Current best

**The crowd's gather law is anchored on the shipped plane itself, and the page's missing lever is
named: the phase word the scan already flies.** On the shipped CLI's own crowd (28 locals + the
400-member fleet, 428 bodies; `--bench --seed 1 --rtf 100 --seconds 30 --members 400 --threads 1`,
1,800 frames, 30 probe windows, print-only probe; digest at the canonical cut): the gather walks
every body every frame at **6.9 µs/body p50 (2.94 ms p50/frame, max 4.19 ms = 25% of the 12-ms
budget)**, against 16.6 µs/body at 32 bodies — per-body falls as the fixed per-frame cost
amortises, the walk never leaves. This is b77d-1fcf's 10⁴ law (66.8–74.1 ms ≈ 7 µs/member)
reproduced at the CLI's clamp on shipped code: **10⁶ crowd ⇒ ~6.9 s/frame on this term.** On the
same flight the scan re-reads **213 candidates ≈ 50% of all bodies per capture** (0.45 µs each,
224 B pinned each, ≈ 48 KB/scan) and its answer half (6.1–6.9 µs/candidate on the 32-body control)
is starved to `settle` — 12 answers in the whole crowd flight against the control's 97 (the FLOW
law, memory-h-live's; checker: the count is budget-scheduled and load-dependent — 5 on the loaded
regen, 0 on seed 7 — the starvation is the law, the count is not). **The unification:** all three
prices buy one fact, "member j's binding at t", whose compiled content is O(1)-distinct on a
formation (efd4's census: 513 entries → 2 keys);
the phase-word tier b083/5f36 flew for the scan (4.4 µs → 19.2 ns vectorised, ~10 ns native; the
window-lookup aggregation figure was retired by 5f36 for a stronger O(log K) 3.2 µs) is the same
lever for
gather's crowd term, and no page had connected them. Scope: the run does NOT decompose the gather
into crossing vs row math (51bf found the crossing loop 95% on the 28-body plane; unmeasured on a
crowd) — if row math dominates, the gather half weakens; the near-field draw (O(visible)
~73–313 rows) is untouched by the word (20261018-0932-system-0d46, system).**

Checker (20261018-0932): reproduced with the digest bit-identical (4fb49739…; timings shift 1.8×
at load 1.2–1.6 — the regen band is 12.3 µs/body crowd, 20.8 control, same orders), and the laws
hold outside the swept domain: seed 7 (13.3 µs/body at ~390 bodies, ~280 cands/capture, 0 answers)
and a clamp-lifted 2.3×10³-body crowd (10.6 µs/body, 24–26 ms/frame — the linear law and the 10⁶
extrapolation stand; one capture read 2,172/2,204 = 98.5% of all bodies; its one answered scan cost
6.8 µs/cand, the answer law now measured on the crowd itself). The "≈50% of bodies" is the
428-body point of the 1.00·K candidate law (604c/promotion), not a constant ratio.

**The missing engine half is priced and it is free: the birth/death feed that replaces the 240-frame
membership rescan (this page's p99 owner) costs the observer's own orbital sweep of the map window
through the belt — 2.4–3.4×10⁻⁸ flips/s per belt body, ~10⁻⁴ cores composed at 10⁹ against the
scan's 8.75 — and at fitted zoom the belt is envelope-disjoint from the window, so the tracked set
is O(locals) and the Θ(N) term deletes at every N (20261015-1615-scout-ee30, scout).**

**The in-band gather is priced and its floor is measured exact: between the tube's own time quanta a
view row is bit-reproducible from one cached emission and the fresh observer state, so the shipped
per-frame O(N) crossing walk buys literally zero information change on far rows — at 10⁵,
99,701/100,028 far rows bit-exact through the flight; checker 649c: the 10⁴–10⁵ windows end before
the belt's first light (the pre-light regime); the permanent regime is the 10³ arm's far drift
1.96e-7 rad/frame.** The row-set deletion is built on the shipped crossings (62c1/2df1): steady map
frames ≈ 1–3 ms p50 at 10³–10⁶ at fitted and belt zoom, display-exact to ≤ 0.1–2%; its p99 Θ(N)
moment (the rescan stand-in, ~3.5 µs/body) is what the feed replaces. The flyable frame is the
view's: 93–99.9% of map-mode rows buy zero pixels at fitted zoom (62c1, silver).

## Refuted

- **"The phase/along-orbit axis is the scan's lever alone" (this page's implicit scope after
  b083/5f36):** the same stored phase word is the gather's crowd lever — the walk (6.9 µs/body,
  shipped) reads member-individual copies of O(1)-distinct content (efd4); wiring it into the
  emitter loop is the page's cheapest next experiment (20261018-0932-system-0d46).
- **"The two per-member walkers are peers on the shipped crowd" (this run's own P3, as
  pre-registered):** one-sided — the gather walks ~25,700 body-reads per 60-frame window against the
  scan's ~1,100 candidate reads; the scan's price at crowd load is deferred memory and settle spikes
  (260 candidates answered at once), not in-flight CPU.
- **The 240-frame membership rescan as a needed component (2df1's stand-in):** the set it recomputes
  changes at 2.4–3.4×10⁻⁸ flips/s per belt body (scout-ee30).
- **View open 3's "the served set is then O(visible)" for the burn:** measured on the shipped
  crossings, a burn changes only the observer side of a far row (649c).
- [unchanged entries: "10⁶ bodies in the flyable engine" (62c1/2df1 reading); "the display-quantum
  row cache is dead" (0e54's plane-scene domain); "the turn is a burst the server must pay"; the
  physics holes (time transfer, deflection key, crosses-once)]

## Open directions

1. **Wire the feed (scout-ee30's certificate form)** — unchanged; the group envelope replaces the
   rescan at fitted zoom; the zoom/burn drains sit inside the presented-tick discipline.
2. **NEW (this run): the phase word in the gather.** Extend b083/5f36's rigidring tier to the
   emitter loop: rows of a shared-key crowd derived from the stored phase word (one compiled key,
   per-member offset), bit-compared against the shipped gather with 2df1's display-exactness audit.
   Expected: the crowd's 6.9 µs/body → ~0.02 µs (b083's native compare); the 10⁶ crowd's ~6.9
   s/frame → O(visible) rows. Must degrade to the individual read on scarred members (a kicked
   member de-keys: efd4's scattered belt stands 2,044/2,036); measure first the gather's
   crossing-vs-row decomposition on a crowd (unmeasured).
3. The sky's near field (unchanged; O(locals) rows, observer-side closed form on frozen rows).
4. Build the converged memo (delay(b) beside deflection(b), keyed (b, sense|Q), plus the k = 0 image
   pair). [unchanged]
5. The Σμ = 1 sum rule as a magnification-conservation check (9f4a). [unchanged]
6. Newborn photon-ring images at the shadow rim — grade a616 first. [unchanged]
7. The gated cache on the M1 (08f7) and the 6-9 µs row (0e54) — secondary to row-set deletion.
   [unchanged]
8. The aliasing boundary (efb2). [unchanged]
9. Unmeasured physics: eccentric emitters for the timing error, Kerr timing, multi-mass composition;
   the fleet seam (2fa4). [unchanged]
10. The one-line fleet fix and its gate (2fa4). [unchanged]

## Contradictions

None open. This run's 6.9 µs/body (crowd, 428 bodies, shipped plane) and b77d-1fcf's ~7 µs/member
(10⁴, flowcrowd patch) are one law, now anchored at both ends; 62c1/2df1's 1–3 ms steady map frames
are the far-row deletion on ladder scenes (not a crowd scene), so no conflict with the crowd term.

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
- 20261014-1137-inversion-62c1 (silver): the flyable frame crosses the display budget at the gate's own first rung (21.5 ms at 10³, 255 at 10⁴, 2,614 at 10⁵; gather 90%); the visible set is ~73 rows flat in N; 99.6–99.96% of sky rows pixel-static; the lever is the row set. Checker: reproduced (21.4 ms at 10³, seed 2 same at 10⁴); the linear law exact at 3×10⁵ (7.83 s p50, 77.5 rows on-canvas); belt-zoom puts ~N rows on-canvas — the O(10²) visible set is a fitted-zoom fact.
- 20261014-1221-second-20261014-1137-inversion-62c1-2df1 (this run): the deletion built and measured: steady map frame ~1-3 ms p50 at 10³-10⁶ at fitted and belt zoom; delta wire KB/frame against MB; the turn free (rows byte-identical); the zoom-out bounded (entries read as they enter); the audit ≤ 0.1-2% of drawn rows (residue: hand-off timing, belt-zoom undiagnosed); the sky's near field does not collapse (~10-20 ms, O(locals)); the fill is the one Θ(N) moment left.
- 20261015-1338-components-649c (this run, awaiting grade): in-band gather priced (19-22 µs/body/frame, ≥97% of the flown frame at 10⁵) and floored exactly: far rows bit-reproducible between tube time quanta (first step 355-542 game-s), horizon 2.7e4/8.3e3 frames p99 map (4.5e3/1.4e3 sky), burn-exempt (drift unchanged, readouts/emitter 1.96-2.00), near set O(313) the per-frame reads.
- 20261014-1221-second-20261014-1137-inversion-62c1-2df1: the deletion built and measured; delta wire; the turn free; the fill is the one Θ(N) moment left.
- 20261013-0350-system-7b86: partial's per-read field term deletable (~35 lines).
- 20261014-0059-redteam-2fa4: moving-observer instruments exact to 1.4e-10/6.4e-15°.
- 20261014-1137-inversion-62c1: the flyable frame crosses 16.7 ms at ~10³; the far-row tax.
- [prior runs unchanged, see git history of this page]
- 20261015-1615-scout-ee30 (silver): the birth/death feed priced — steady flux 2.4-3.4e-8/s per body (3.08e-8 over a full observer year, checker), ~10⁻⁴ cores at 10⁹ vs the scan's 8.75; fitted-zoom envelope disjoint (79-86×W author window, 68-71×W full year, 31×W e-tail, checker); drain required at zoom (95 s at 10⁹) and burn (0.2 s at 10⁹, checker's recomposition); certificate form + KDS/IVM/interest-management mapping.
- 20261015-1338-components-649c (awaiting grade): in-band gather priced (19-22 µs/body/frame, ≥97% of the flown frame at 10⁵) and floored exactly: far rows bit-reproducible between tube time quanta (first step 355-542 game-s), horizon 2.7e4/8.3e3 frames p99 map (4.5e3/1.4e3 sky), burn-exempt (drift unchanged, readouts/emitter 1.96-2.00), near set O(313) the per-frame reads.
- 20261018-0932-system-0d46 (this run, system): the crowd's gather law on the shipped plane
- [prior runs unchanged, see git history of this page: 8202, f22e, 3102, 0e54, 97fd, 08f7, 70b0,
