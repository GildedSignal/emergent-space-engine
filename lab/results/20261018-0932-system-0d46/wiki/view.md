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

- 20261018-0932-system-0d46 (this run, system): the crowd's gather law on the shipped plane
  (6.9 µs/body p50, 25% of budget at 428 bodies; 10⁶ ⇒ ~6.9 s/frame), the scan's 50%-of-bodies
  candidate law and settle-starved answers (12 vs 97) on the same scene, and the unification:
  b083/5f36's phase word is the gather's lever too.
- [prior runs unchanged, see git history of this page: 8202, f22e, 3102, 0e54, 97fd, 08f7, 70b0,
  51bf, 18fc-94dc, ace6, d51f, 8be2, 9f4a, 0b45, 48cf, a616, 5977, 6eae, 8f00, fb64, 0fe0, 7b86,
  2fa4, 62c1, 2df1, 649c, ee30]
