# Predictions — written before the decisive runs

The build (this run's patch): `gather_rows` in view.rs — the shipped crossings read for a chosen body set,
`gather_cached` byte-identical (digest `8387a46c…`, 200 frames, 1028 bodies, `Budget::unlimited`) — plus the
display policy in the example: a canvas test (the page's own draw condition, 20 px margin), a display-quantum
due wheel (serve at half a pixel, drift measured between reads, ×4 slack, ×4 zero-drift backoff, jittered), a
panel band (nearest bodies served live), a delta wire (ids + changed rows + gone), and an audit that compares,
per frame, what the client would draw (from its held rows, at the current zoom and heading) against the
shipped `gather_cached`'s exact pixels.

## Held-out cases (not tuned on; the pilot touched only N ≤ 1,028 at fit zoom, coast)

1. **Map, fitted zoom, coast, N = 10⁴/10⁵/10⁶:** steady frame (engine + policy gather + delta wire) stays
   under 5 ms p50 at every N — flat in N (the census's flat visible set plus the band). Readouts/frame
   settle between 50 and 300; served rows between 50 and 200; wire under 60 KB/frame.
2. **Map, belt zoom (3 AU across), coast, same N:** same collapse — the quantum, not the canvas test, does
   the work; the belt is display-frozen (the log display and the 0.29 px/light-second scale freeze it). I
   predict the same < 5 ms p50 and readouts/frame within 2× of the fitted zoom's.
3. **The fill (the first full read, once per flight):** linear in N, ≈ the baseline gather (19-23 ms at
   10³, ~2.4 s at 10⁵, ~25-30 s at 10⁶ on this box) — the one unavoidable Θ(N) moment, like the page's
   first frame after a restart.
4. **The turn (30 frames, keys = left):** the server's rows do not change (a turn rotates the heading, which
   is header data; aberration depends on velocity, not heading) — so the turn window's gather and wire stay
   at the steady state's level, and the audit stays clean. The burst, if any, is the engine's own battle
   events, not the view.
5. **The zoom-out (fit → belt, the page's 0.3 ease):** a bounded burst — rows enter on the zoom's geometric
   schedule; the entering set per eased frame is what is read. At 10³ I measured a 6.7 ms max. I predict the
   zoom window's total readouts scale with the entering set (≈ the on-canvas count at belt zoom ≈ locals +
   belt ≈ N at 10⁴+), so at 10⁵ the burst frames reach tens of ms and the window's total is ≈ one baseline
   gather (the fill again, spread over the ease). At 10⁶ the zoom-out is the remaining wall.
6. **Audit:** at fit zoom and through the zoom, violations ≤ 2 per frame averaged (≈ 0.1% of drawn rows):
   the residue I could not remove at small N is hand-off timing (a fleet member born as a body mid-flight;
   the engine's event counter does not carry hand-offs, so a 10-frame scan stands in). At belt zoom I
   measured ~15/frame at 10³ (1.4% of drawn rows) before these fixes and did not re-diagnose — I predict it
   stays within a few per cent and disclose whatever it is.
7. **The sky display:** the far field freezes like the map's, but the near field does not: the locals'
   polar moves a measurable fraction of a pixel per frame at rtf 100, so sky-mode reads are O(locals) ≈ 500
   at 10³, 300 (capped) at 10⁴+ — I predict sky steady ≈ 10-25 ms at 10³ and ≈ 8-15 ms at 10⁴-10⁶: the sky
   does NOT collapse to ~ms at this quantum. The map is the flyable display; the sky's near field is
   genuine per-frame surprise.
8. **Wire:** the delta wire is under 60 KB/frame steady at every N (vs 0.29-27 MB shipped), and the fill
   frame excepted, no frame's wire exceeds 1 MB even through the zoom (the entering rows are served once).

## What would kill the claim

- Steady map frames (either zoom) above ~16.7 ms at any N ≤ 10⁶.
- Audit violations above a few per cent of drawn rows (the deletion would be display-wrong, not just late).
- The turn costing the server anything (would refute the heading-free quantum design).
